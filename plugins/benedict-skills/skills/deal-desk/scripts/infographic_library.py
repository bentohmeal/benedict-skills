"""Infographic library: copy PwC's original infographics (native shapes, tables, charts, groups, not redrawn) into a
16:9 deck in the house style: navy ramp + greys, Arial, sizes 20 / 12 / 10 / 8 only, no shadows.

    python infographic_library.py [src.pptx] [out.pptx]
      default src: ...\\Investment Banking Library\\Slide Inspiration\\PwC Infographic Templates (2014).pptx
      default out: Claude Things\\output\\Infographic Library.pptx   (+ assets/infographic_index.json)

Stage 1 (python-pptx, temp copy): every colour -> house palette (per slide: chromatic colours spread over NAVY_RAMP by
lightness; neutrals -> nearest grey; text -> black / white), chart fonts, shadows / 3-D removed.
Stage 2 (PowerPoint COM): house chrome from ibdeck, paste each slide's objects, scale to the body box, font roles
(short number >=14pt -> 20 bold, heading 13-17pt -> 12 bold, <=8pt -> 8, else 10), overflow guard.
Stage 3: audit (colours, fonts, sizes) and the index JSON. Library shapes are named "IG ..." (lint skips them).
"""
import colorsys
import json
import os
import re
import shutil
import sys
import tempfile
import time

from lxml import etree
from pptx import Presentation
from pptx.oxml.ns import qn

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ibdeck  # noqa: E402
from ibdeck import NAVY_RAMP, BLACK, WHITE, DGREY, GREY, LGREY, PALEGREY, L, R_, W  # noqa: E402

SRC = (r"C:\Users\user\Documents\Google Drive\01. IB PE\Investment Banking Library\Slide Inspiration"
       r"\PwC Infographic Templates (2014).pptx")
OUT = r"C:\Users\user\Documents\Google Drive\Claude Things\output\_Deal Desk Toolkit\Infographic Library.pptx"
INDEX = os.path.join(HERE, "..", "assets", "infographic_index.json")

BODY = (L, 1.35, W - L - R_, 5.15)          # x, y, w, h in inches: under the title rule, above the sources line
NEUTRALS = [BLACK, DGREY, GREY, LGREY, PALEGREY, WHITE]
PALETTE = set(NAVY_RAMP) | set(NEUTRALS)
KEEP_FONTS = {"Wingdings", "Wingdings 2", "Wingdings 3", "Symbol", "Webdings"}

# (first, last PwC slide, section = header and contents-bar label)
SECTIONS = [(4, 11, "Arrows"), (13, 74, "Circular Diagrams"), (76, 97, "Other Shapes"),
            (99, 139, "Processes"), (141, 163, "Maps"), (166, 199, "Icons"), (201, 209, "Audit Pages"),
            (216, 228, "Graphic Sets")]
SKIP = {164, 204}   # 164 section divider (165 = business card); 204 = PwC awards page (third-party logos)
NOTE_TEXT = ("new slide", "active chart", "not activated", "hints:", "above values are fixed", "bottom chart is active",
             "can be edited to different layouts", "objects can be ungrouped", "with animation",
             "remove gradient shading", "pwc.com", "need to enter web", "need to amend hyperlink",
             "originally printed on a3")   # PwC's own usage notes and stickers, matched in lower case
BRAND_LABELS = ("pwc logo", "cv photo", "spark logo")
BRAND_SHAPES = {170: ("Group 68", "Oval 127")}     # PwC slide -> logo shapes (Spark logo, PwC logo circle)


def scope():
    out = []
    for a, b, sec in SECTIONS:
        for n in range(a, b + 1):
            if n not in SKIP:
                out.append((n, sec))
    return out


# ---------------------------------------------------------------- colour maths
def hex2rgb(h):
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def rgb2hex(c):
    return "".join(f"{max(0, min(255, round(v * 255))):02X}" for v in c)


def hls(h):
    return colorsys.rgb_to_hls(*hex2rgb(h))


RAMP_L = [hls(c)[1] for c in NAVY_RAMP]
NEUTRAL_L = [hls(c)[1] for c in NEUTRALS]
PRESET = {"black": "000000", "white": "FFFFFF", "red": "FF0000", "green": "008000", "blue": "0000FF",
          "yellow": "FFFF00", "gray": "808080", "grey": "808080", "orange": "FFA500"}


def apply_mods(hexv, el):
    """Apply DrawingML colour modifiers (lumMod, lumOff, tint, shade) to get the colour actually shown."""
    r, g, b = hex2rgb(hexv)
    for m in el:
        tag = etree.QName(m).localname
        v = int(m.get("val", "100000")) / 100000
        if tag in ("lumMod", "lumOff"):
            h, l_, s = colorsys.rgb_to_hls(r, g, b)
            l_ = l_ * v if tag == "lumMod" else min(1, l_ + v)
            r, g, b = colorsys.hls_to_rgb(h, l_, s)
        elif tag == "tint":
            r, g, b = (c + (1 - c) * (1 - v) for c in (r, g, b))
        elif tag == "shade":
            r, g, b = (c * v for c in (r, g, b))
    return rgb2hex((r, g, b))


def theme_colours(prs):
    master = prs.slide_masters[0]
    xml = next(r.target_part.blob for r in master.part.rels.values() if r.reltype.endswith("/theme")).decode("utf8")
    th = {k: v for k, v in re.findall(r"<a:(dk1|lt1|dk2|lt2|accent\d|hlink|folHlink)>\s*<a:\w+Clr [^>]*?(?:val|lastClr)=\"(\w{6})\"", xml)}
    cmap = master._element.find(qn("p:clrMap"))
    for alias in ("bg1", "tx1", "bg2", "tx2"):
        th[alias] = th.get(cmap.get(alias) if cmap is not None else {"bg1": "lt1", "tx1": "dk1", "bg2": "lt2", "tx2": "dk2"}[alias], "000000")
    return th


COLOUR_TAGS = {qn("a:srgbClr"), qn("a:schemeClr"), qn("a:prstClr"), qn("a:sysClr"), qn("a:scrgbClr"), qn("a:hslClr")}


def resolve(el, theme):
    tag = etree.QName(el).localname
    if tag == "srgbClr":
        base = el.get("val")
    elif tag == "schemeClr":
        base = theme.get(el.get("val"), "000000")      # phClr: the colour sits on the style reference
    elif tag == "sysClr":
        base = el.get("lastClr", "000000")
    elif tag == "prstClr":
        base = PRESET.get(el.get("val"), "808080")
    else:
        base = "808080"
    return apply_mods(base, el)


def is_text(el):
    p = el.getparent()
    while p is not None:
        n = etree.QName(p).localname
        if n in ("rPr", "defRPr", "endParaRPr", "fontRef"):
            return True
        if n in ("spPr", "tcPr", "ln", "fillRef", "lnRef", "bgPr"):
            return False
        p = p.getparent()
    return False


def nearest_neutral(h):
    l_ = hls(h)[1]
    return NEUTRALS[min(range(len(NEUTRALS)), key=lambda i: abs(NEUTRAL_L[i] - l_))]


def chromatic(h):
    hh, l_, s = hls(h)
    return s > 0.15 and 0.04 < l_ < 0.97


def ramp_map(colours):
    """Distinct chromatic colours on one slide -> navy ramp, keeping their order by lightness and keeping them apart
    (up to 6; beyond that, colours of similar lightness share a shade)."""
    cols = sorted(set(colours), key=lambda c: hls(c)[1])
    n, out, prev = len(cols), {}, -1
    for k, c in enumerate(cols):
        l_ = hls(c)[1]
        t = min(range(6), key=lambda i: abs(RAMP_L[i] - l_))
        if k == 0 and l_ > 0.12:
            t = min(t, 1)                          # the darkest brand colour becomes the main navy
        if n <= 6:
            t = max(t, prev + 1)                   # keep different colours different
            t = min(t, 6 - (n - k))                # leave room for the lighter colours still to come
        else:
            t = max(t, prev)
        t = max(0, min(t, 5))
        out[c] = NAVY_RAMP[t]
        prev = t
    return out


def recolour_tree(roots, theme, text_default_black=True):
    """roots: XML elements for one slide (spTree + chart spaces). Rewrites every colour to a plain house hex."""
    els = [e for r in roots for e in r.iter() if e.tag in COLOUR_TAGS]
    info = []
    for e in els:
        v = resolve(e, theme)
        info.append((e, v, is_text(e)))
    ramp = ramp_map([v for e, v, t in info if not t and chromatic(v)])
    for e, v, t in info:
        if t:
            new = (WHITE if hls(v)[1] > 0.75 else BLACK) if chromatic(v) else nearest_neutral(v)
        else:
            new = ramp[v] if chromatic(v) else nearest_neutral(v)
        alpha = [m for m in e if etree.QName(m).localname == "alpha"]
        new_el = etree.Element(qn("a:srgbClr"))
        new_el.set("val", new)
        for a in alpha:
            new_el.append(a)
        e.getparent().replace(e, new_el)
    return len(els)


def flatten_effects(root):
    """No shadows, glows, bevels or 3-D (his 'no shadows' rule)."""
    for tag in ("a:effectLst", "a:effectDag", "a:scene3d", "a:sp3d"):
        for e in list(root.iter(qn(tag))):
            if tag == "a:effectLst":
                for c in list(e):
                    e.remove(c)
            else:
                e.getparent().remove(e)
    for e in root.iter(qn("a:effectRef")):
        e.set("idx", "0")


def chart_fonts(root):
    for e in root.iter():
        n = etree.QName(e).localname if isinstance(e.tag, str) else ""
        if n in ("defRPr", "rPr", "endParaRPr"):
            if e.get("sz"):
                e.set("sz", "800" if int(e.get("sz")) <= 850 else "1000")
            for f in e.findall(qn("a:latin")):
                if f.get("typeface") not in KEEP_FONTS:
                    f.set("typeface", "Arial")


# ---------------------------------------------------------------- stage 1: restyle a temp copy
def title_parts(slide):
    for ph in slide.placeholders:
        if ph.placeholder_format.type is not None and "TITLE" in str(ph.placeholder_format.type):
            return [t.strip() for t in re.split(r"[\v\n]", ph.text_frame.text) if t.strip()]
    return []


def clean_sub(txt, section, n):
    if 216 <= n <= 221:
        return "Editable graphics"
    if n >= 222:
        return "Icon set"
    t = re.sub(r"\s*\(as of[^)]*\)", "", txt or "")
    t = re.sub(r"\bPwC\b\s*", "", t).strip(" –-")
    t = re.sub(r"(interactive documents).*", r"\1", t)
    if not t or t.lower() == section.lower():
        t = section.rstrip("s") if section.endswith("s") else section
    if t.lower() == "uk history":
        t = "Timeline"
    return t[0].upper() + t[1:] if t else section


def restyle(src, tmp):
    prs = Presentation(src)
    theme = theme_colours(prs)
    meta = []
    wanted = dict(scope())
    for n, slide in enumerate(prs.slides, 1):
        if n not in wanted:
            continue
        parts = title_parts(slide)
        sub_raw = parts[1] if len(parts) > 1 else (parts[0] if parts else "")
        roots = [slide.shapes._spTree]
        for rel in slide.part.rels.values():
            if rel.reltype.endswith("/chart"):
                roots.append(rel.target_part._element)
        count = recolour_tree(roots, theme)
        for r in roots:
            flatten_effects(r)
        for r in roots[1:]:
            chart_fonts(r)
        meta.append({"pwc": n, "section": wanted[n], "type": clean_sub(sub_raw, wanted[n], n), "colours": count})
    prs.save(tmp)
    return meta


# ---------------------------------------------------------------- stage 2: chrome + paste (PowerPoint COM)
def chrome(meta, path):
    d = ibdeck.Deck(sections=[s for _, _, s in SECTIONS])
    for i, m in enumerate(meta, 1):
        s = d.slide(m["section"], m["type"])
        d.footer(s, sources=f"PwC Infographic Templates (2014), slide {m['pwc']}; restyled",
                 notes=f"Library no. {i}. Objects are the originals (edit text, values and gold highlight in place)")
    set_theme(d.prs)
    d.prs.save(path)


def set_theme(prs):
    """Library theme: navy ramp accents + Arial, so anything still theme-linked (e.g. chart auto colours) stays on-palette."""
    master = prs.slide_masters[0]
    part = next(r.target_part for r in master.part.rels.values() if r.reltype.endswith("/theme"))
    xml = part.blob.decode("utf8")
    cols = {"dk1": BLACK, "lt1": WHITE, "dk2": NAVY_RAMP[1], "lt2": PALEGREY, "accent1": NAVY_RAMP[1],
            "accent2": NAVY_RAMP[3], "accent3": NAVY_RAMP[4], "accent4": GREY, "accent5": NAVY_RAMP[2],
            "accent6": LGREY, "hlink": NAVY_RAMP[2], "folHlink": GREY}
    for k, v in cols.items():
        xml = re.sub(rf"(<a:{k}>)\s*<a:\w+Clr [^/]*/>", rf'\1<a:srgbClr val="{v}"/>', xml)
    xml = re.sub(r'(<a:(?:major|minor)Font>\s*<a:latin typeface=")[^"]+"', r'\1Arial"', xml)
    part._blob = xml.encode("utf8")


SKIP_PH = (1, 3, 13, 15, 16)   # ppPlaceholderTitle, CenterTitle, SlideNumber, Footer, Date
EMU_IN = 72.0                  # COM works in points


def _iter(shape):
    yield shape
    if shape.Type == 6:        # msoGroup
        for k in range(1, shape.GroupItems.Count + 1):
            yield shape.GroupItems(k)


def _frames(shape):
    """Text ranges inside a shape (and its group children / table cells)."""
    out = []
    for sh in _iter(shape):
        try:
            if sh.HasTable:
                t = sh.Table
                for r in range(1, t.Rows.Count + 1):
                    for c in range(1, t.Columns.Count + 1):
                        out.append((t.Cell(r, c).Shape, True))
                continue
        except Exception:
            pass
        try:
            if sh.HasTextFrame and sh.TextFrame.HasText:
                out.append((sh, False))
        except Exception:
            pass
    return out


def house_size(orig, text):
    """Size by role: a big number (ring %, KPI; >=18pt) keeps its weight at 20 bold; a smaller number or a short
    heading -> 12 bold; prose -> 10 (bold kept as it was); small print (<=9pt) -> 8."""
    t = text.strip()
    number = len(t) <= 8 and any(ch.isdigit() for ch in t)
    if orig >= 18 and number:
        return 20, True
    if orig >= 13 and (number or len(t) <= 40):
        return 12, True
    if orig < 9.5:
        return 8, None
    return 10, None


STEP = {20: 16, 16: 12, 12: 10, 10: 8, 8: 8}


def fonts(shape):
    fixed = 0
    for sh, in_table in _frames(shape):
        tr = sh.TextFrame.TextRange
        text = tr.Text
        try:
            lines0 = tr.Lines().Count
        except Exception:
            lines0 = None
        for bad in ("PricewaterhouseCoopers", "PwC"):
            if bad in text:
                tr.Replace(bad, "Company")
                text = tr.Text
        k = 1
        while k <= tr.Runs().Count:        # runs can merge once they match, so re-count every time
            try:
                f = tr.Runs(k).Font
                size, bold = house_size(f.Size, text)
                if f.Name not in KEEP_FONTS:
                    f.Name = "Arial"
                f.Size = size
                if bold:
                    f.Bold = True
                f.Italic = False
                fixed += 1
            except Exception:              # odd runs (field codes, symbol fonts): the XML pass in finish() fixes them
                pass
            k += 1
        t = text.strip()
        if not in_table and len(t) <= 8 and any(ch.isdigit() for ch in t):
            try:
                sh.TextFrame.WordWrap = 0      # a number never breaks across lines ("201 / 2")
            except Exception:
                pass
        # keep the original line breaks: if the new sizes make the text wrap more, or spill out of its shape,
        # step every run down one house size (at most three times)
        for _ in range(3):
            try:
                more_lines = lines0 is not None and tr.Lines().Count > lines0
                tf2 = sh.TextFrame2
                spill = (not in_table and tf2.AutoSize == 0 and tf2.WordWrap and sh.Height > 4
                         and tf2.TextRange.BoundHeight > sh.Height * 1.08 + 3)
            except Exception:
                break
            if not (more_lines or spill):
                break
            k = 1
            while k <= tr.Runs().Count:
                try:
                    tr.Runs(k).Font.Size = STEP.get(int(round(tr.Runs(k).Font.Size)), 8)
                except Exception:
                    pass
                k += 1
    return fixed


def shape_text(sh):
    """All text in a shape, its group children and table cells."""
    out = []
    for s_, _ in _frames(sh):
        try:
            out.append(s_.TextFrame.TextRange.Text)
        except Exception:
            pass
    return " ".join(out)


def fit(rng, box):
    shapes = [rng(k) for k in range(1, rng.Count + 1)]
    x0 = min(s.Left for s in shapes)
    y0 = min(s.Top for s in shapes)
    x1 = max(s.Left + s.Width for s in shapes)
    y1 = max(s.Top + s.Height for s in shapes)
    bx, by, bw, bh = (v * EMU_IN for v in box)
    f = min(bw / max(x1 - x0, 1), bh / max(y1 - y0, 1), 1.25)
    ox = bx + (bw - (x1 - x0) * f) / 2
    oy = by + (bh - (y1 - y0) * f) / 2
    for s in shapes:
        cx = ox + (s.Left + s.Width / 2 - x0) * f
        cy = oy + (s.Top + s.Height / 2 - y0) * f
        try:
            is_table = s.HasTable
        except Exception:
            is_table = False
        if is_table:
            t = s.Table
            for c in range(1, t.Columns.Count + 1):
                t.Columns(c).Width = t.Columns(c).Width * f
            for r in range(1, t.Rows.Count + 1):
                t.Rows(r).Height = t.Rows(r).Height * f
        else:
            s.LockAspectRatio = 0
            s.Width, s.Height = s.Width * f, s.Height * f
        s.Left, s.Top = cx - s.Width / 2, cy - s.Height / 2
    return f


def assemble(tmp, out, meta):
    from office import _powerpoint, _quit_ppt
    pp = _powerpoint()
    try:
        src = pp.Presentations.Open(os.path.abspath(tmp), True, False, False)
        dst = pp.Presentations.Open(os.path.abspath(out), False, False, False)
        for i, m in enumerate(meta, 1):
            ss, ds = src.Slides(m["pwc"]), dst.Slides(i)
            idx = []
            for k in range(1, ss.Shapes.Count + 1):
                sh = ss.Shapes(k)
                if sh.Type == 14:   # placeholder
                    if m["pwc"] in (216, 222) or sh.PlaceholderFormat.Type in SKIP_PH:
                        continue
                txt = " ".join(shape_text(sh).split()).lower()
                if txt and len(txt) < 300 and any(t in txt for t in NOTE_TEXT):
                    continue
                if m["pwc"] in BRAND_SHAPES and (sh.Type == 13 or sh.Name in BRAND_SHAPES[m["pwc"]]
                                                 or any(b in txt for b in BRAND_LABELS)):
                    continue            # PwC / Spark logos and the CV photo
                idx.append(k)
            if not idx:
                print(f"{i:3d} PwC {m['pwc']:3d}: nothing to copy")
                continue
            for attempt in range(5):
                try:
                    ss.Shapes.Range(idx).Copy()
                    time.sleep(0.15)
                    rng = ds.Shapes.Paste()
                    break
                except Exception as e:
                    time.sleep(0.8)
                    if attempt == 4:
                        raise RuntimeError(f"paste failed for PwC slide {m['pwc']}: {e}")
            for k in range(1, rng.Count + 1):
                rng(k).Name = "IG " + rng(k).Name
            m["scale"] = round(fit(rng, BODY), 3)
            m["runs"] = sum(fonts(rng(k)) for k in range(1, rng.Count + 1))
            m["objects"] = rng.Count
            print(f"{i:3d} PwC {m['pwc']:3d} {m['type'][:38]:38s} objects {rng.Count:4d}  scale {m['scale']:.2f}", flush=True)
        dst.Save()
        dst.Close()
        src.Close()
    finally:
        _quit_ppt(pp)


HOUSE_SZ = (800, 1000, 1200, 1600, 2000)


def finish(out):
    """XML pass for what COM leaves behind: theme / Georgia typefaces on empty paragraphs and line ends, sizes on
    end-of-paragraph marks. Library shapes only."""
    prs = Presentation(out)
    for s in prs.slides:
        for sh in list(s.shapes):
            if not sh.name.startswith("IG "):
                continue
            # PwC usage notes can sit inside groups: remove them at any depth
            for sp in list(sh._element.iter(qn("p:sp"))):
                txt = " ".join("".join(t.text or "" for t in sp.iter(qn("a:t"))).split()).lower()
                if txt and len(txt) < 300 and any(n in txt for n in NOTE_TEXT):
                    sp.getparent().remove(sp)
            if sh._element.getparent() is None:
                continue
            for e in list(sh._element.iter()):
                if e.tag == qn("a:schemeClr") and etree.QName(e.getparent()).localname not in \
                        ("fillRef", "lnRef", "fontRef", "effectRef"):
                    new = etree.Element(qn("a:srgbClr"))     # pin anything still theme-linked
                    new.set("val", {"tx1": BLACK, "dk1": BLACK, "bg1": WHITE, "lt1": WHITE}.get(e.get("val"), NAVY_RAMP[1]))
                    e.getparent().replace(e, new)
                elif e.tag == qn("a:latin") and e.get("typeface") not in KEEP_FONTS:
                    e.set("typeface", "Arial")
                elif e.tag in (qn("a:rPr"), qn("a:endParaRPr"), qn("a:defRPr")) and e.get("sz")                         and int(e.get("sz")) not in HOUSE_SZ:
                    e.set("sz", str(min(HOUSE_SZ, key=lambda v: abs(v - int(e.get("sz"))))))
    prs.save(out)


# ---------------------------------------------------------------- stage 3: audit + index
USES = [  # keyword in the PwC type -> what the layout is good for in an IB / PE deck
    ("venn", ["overlap", "synergies", "strategic fit"]), ("pie", ["mix", "split"]),
    ("percentage", ["mix", "market share", "margin"]), ("doughnut", ["mix", "market share"]),
    ("speedometer", ["scoring", "utilisation", "leverage vs covenant"]), ("heat map", ["risk", "scoring"]),
    ("cycle", ["value creation loop", "operating model"]), ("hub", ["business model", "ecosystem"]),
    ("pyramid", ["hierarchy", "capital structure", "priorities"]), ("hexagon", ["pillars", "capabilities"]),
    ("octogan", ["pillars"]), ("spider", ["competitive scoring"]), ("radar", ["competitive scoring"]),
    ("jigsaw", ["fit", "integration", "building blocks"]), ("cog", ["operating model", "integration"]),
    ("bridge", ["EBITDA bridge", "value bridge"]), ("waterfall", ["EBITDA bridge", "value bridge"]),
    ("thermometer", ["progress vs target"]), ("bar chart", ["ranking", "peers"]), ("line chart", ["trend"]),
    ("bottle", ["constraint", "bottleneck"]), ("maze", ["complexity", "process"]),
    ("linear flow", ["process", "deal steps"]), ("list", ["key points", "thesis"]), ("scale", ["rating", "maturity"]),
    ("funnel", ["deal pipeline", "buyer funnel", "TAM to SOM"]), ("phase", ["100-day plan", "workstreams"]),
    ("option", ["strategic options"]), ("road map", ["roadmap", "value creation plan"]),
    ("timeline", ["history", "milestones", "deal timetable"]), ("gantt", ["deal timetable", "workstreams"]),
    ("calendar", ["timetable"]), ("balance", ["pros vs cons", "trade-off"]),
    ("map", ["footprint", "geographic mix"]), ("globe", ["global footprint"]), ("territory", ["footprint"]),
    ("icons", ["icon source"]), ("silhouette", ["people", "headcount"]), ("traffic", ["RAG status"]),
    ("people", ["headcount", "customers"]), ("segment", ["segments"]), ("layer", ["layers", "stack"]),
    ("rating", ["rating", "scoring"]), ("quote", ["management quote", "customer quote"]),
    ("risk", ["risk map"]), ("testing", ["workplan"]), ("scope", ["scope"]), ("arrow", ["process", "flow"]),
    ("section", ["pillars", "segments"]), ("petal", ["pillars"]), ("relationship", ["relationships"]),
    ("graphics", ["icon source"]), ("process", ["process"]), ("circular bar", ["ranking"]),
]


def uses(m):
    t = (m["type"] + " " + m["section"]).lower()
    u = []
    for k, v in USES:
        if k in t:
            u += [x for x in v if x not in u]
    return u or ["general diagram"]


def audit(out):
    prs = Presentation(out)
    bad_col, bad_font, bad_size, pics = {}, {}, {}, []
    for i, s in enumerate(prs.slides, 1):
        roots = [sh._element for sh in s.shapes if sh.name.startswith("IG ")]
        for rel in s.part.rels.values():
            if rel.reltype.endswith("/chart"):
                roots.append(rel.target_part._element)
        for r in roots:
            for e in r.iter():
                if e.tag == qn("a:srgbClr") and e.get("val") not in PALETTE:
                    bad_col.setdefault(i, set()).add(e.get("val"))
                elif e.tag in COLOUR_TAGS and e.tag != qn("a:srgbClr") and \
                        etree.QName(e.getparent()).localname not in ("fillRef", "lnRef", "fontRef", "effectRef"):
                    bad_col.setdefault(i, set()).add(etree.QName(e).localname + ":" + str(e.get("val")))
                elif e.tag == qn("a:latin") and e.get("typeface") not in KEEP_FONTS | {"Arial"} \
                        and not e.get("typeface", "").startswith("+"):
                    bad_font.setdefault(i, set()).add(e.get("typeface"))
                elif e.tag in (qn("a:rPr"),) and e.get("sz") and int(e.get("sz")) not in (800, 1000, 1200, 1600, 2000):
                    bad_size.setdefault(i, set()).add(int(e.get("sz")) / 100)
                elif e.tag == qn("a:blip"):
                    pics.append(i)
    print(f"audit: off-palette colours on {len(bad_col)} slide(s)"
          + "".join(f"\n   slide {k}: {sorted(v)[:8]}" for k, v in list(bad_col.items())[:15]))
    print(f"audit: other fonts on {len(bad_font)} slide(s)"
          + "".join(f"\n   slide {k}: {sorted(v)}" for k, v in list(bad_font.items())[:15]))
    print(f"audit: off-house sizes on {len(bad_size)} slide(s)"
          + "".join(f"\n   slide {k}: {sorted(v)}" for k, v in list(bad_size.items())[:15]))
    print(f"audit: pictures (not recoloured) on slides {sorted(set(pics))}")
    return bad_col, bad_font, bad_size, sorted(set(pics))


def main(src=SRC, out=OUT):
    tmpdir = tempfile.mkdtemp()
    tmp = os.path.join(tmpdir, "pwc_restyled.pptx")
    shutil.copy(src, os.path.join(tmpdir, "pwc_src.pptx"))
    meta = restyle(os.path.join(tmpdir, "pwc_src.pptx"), tmp)
    print(f"restyled {len(meta)} slides")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    chrome(meta, out)
    assemble(tmp, out, meta)
    finish(out)
    _, _, _, pics = audit(out)
    index = [{"no": i, "pwc": m["pwc"], "section": m["section"], "type": m["type"], "use": uses(m),
              "picture": i in pics, "objects": m.get("objects", 0)} for i, m in enumerate(meta, 1)]
    with open(INDEX, "w", encoding="utf8") as f:
        json.dump({"library": out, "source": src, "slides": index}, f, indent=1, ensure_ascii=False)
    print(f"saved {out}\nindex {os.path.abspath(INDEX)}")
    shutil.rmtree(tmpdir, ignore_errors=True)


def contact_sheet(out=OUT, pdf=None):
    """Numbered thumbnails, 12 per page, so Benedict can say 'use 67'."""
    from PIL import Image, ImageDraw, ImageFont
    import office
    pdf = pdf or out.replace(".pptx", " – index.pdf")
    with open(INDEX, encoding="utf8") as f:
        idx = {m["no"]: m for m in json.load(f)["slides"]}
    tmp = tempfile.mkdtemp()
    files = office.render(out, tmp, 800, 450)
    font = ImageFont.truetype("arialbd.ttf", 20)
    small = ImageFont.truetype("arial.ttf", 16)
    cols, rows, tw, th, pad = 3, 4, 800, 450, 30
    pages = []
    for p in range(0, len(files), cols * rows):
        page = Image.new("RGB", (cols * (tw + pad) + pad, rows * (th + 60) + pad), "white")
        dr = ImageDraw.Draw(page)
        for k, fpath in enumerate(files[p:p + cols * rows]):
            no = p + k + 1
            x, y = pad + (k % cols) * (tw + pad), pad + (k // cols) * (th + 60)
            page.paste(Image.open(fpath).convert("RGB"), (x, y + 34))
            dr.rectangle([x, y + 34, x + tw, y + 34 + th], outline=(191, 191, 191))
            m = idx.get(no, {})
            dr.text((x, y + 6), str(no), fill=(31, 56, 100), font=font)
            dr.text((x + 55, y + 8), f"{m.get('section', '')} · {m.get('type', '')}"[:85], fill=(0, 0, 0), font=small)
        pages.append(page)
    pages[0].save(pdf, save_all=True, append_images=pages[1:], resolution=100)
    shutil.rmtree(tmp, ignore_errors=True)
    print(pdf)
    return pdf


if __name__ == "__main__":
    if sys.argv[1:2] == ["index"]:
        contact_sheet()
    elif sys.argv[1:2] == ["finish"]:     # re-run the XML clean-up + audit on the built library (no PowerPoint)
        finish(OUT)
        audit(OUT)
        contact_sheet()
    else:
        main(*(sys.argv[1:3]))
        contact_sheet(sys.argv[2] if len(sys.argv) > 2 else OUT)
