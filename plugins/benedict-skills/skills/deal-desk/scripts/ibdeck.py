"""Classic IB house style (navy ramp + greys + one gold highlight) for python-pptx decks. Native, editable charts.

    import sys; sys.path.insert(0, "<Claude Things>/.claude/skills/deal-desk/scripts")
    from ibdeck import Deck
    d = Deck(sections=["Company Overview", "Industry Overview", "Valuation"])   # contents bar on every slide
    s = d.slide("Company Overview", "Australia's #3 gym chain by outlets")        # header 20 navy + subheader 16 grey
    x, y, w, h = d.grid(0, 2)            # left half of the body
    d.header(s, x, y, w, "Studio footprint")          # filled navy bar
    d.stat_icons(s, x, y + 0.45, w, 1.6, [("building-store", "150", "Studios")])
    d.footer(s, sources="Company data", notes="As at Year 0")
    d.save("out.pptx")                  # runs lint(): layout + "AI tells" (incl. font sizes, shadows)
Font sizes: only 20 (header) / 16 (subheader) / 12 (header bars, contents bar, key numbers in bold) / 10 (all other
text), plus 8 italic for Sources / Notes (and the page number).
See ../references/house-style.md for the rules and ../references/slide-layouts.md for which layout to use when.
Icons: Tabler outline icons (MIT) in ../assets/icons/<name>.svg; list them with Deck.icons().
"""
import math
import os
import re

from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION, XL_TICK_LABEL_POSITION
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE, MSO_SHAPE_TYPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

# Palette: one hue in six shades + greys + one muted accent for a single highlight per slide
# (sources in ../references/house-style.md)
NAVY_RAMP = ["0B1F3A", "1F3864", "2F5597", "5B7DB8", "9DB4D8", "DCE5F1"]   # deep -> near-white
DEEP, NAVY, MID, STEEL, LIGHT, PALE = NAVY_RAMP
DGREY, GREY, LGREY, PALEGREY = "404040", "7F7F7F", "BFBFBF", "EDEDED"
MIDGREY = LGREY
GOLD = "B08D3F"
HEAT_RED, HEAT_MID, HEAT_GREEN = "F8696B", "FFFFFF", "63BE7B"   # = xlstyle.heat_map (the model's sensitivities)            # highlight only (the target, the base case); never a large fill
BLACK, WHITE = "000000", "FFFFFF"
SERIES = [NAVY, STEEL, LIGHT, LGREY, MID]
FONT = "Arial"

F_TITLE, F_SUB, F_HEAD, F_BODY, F_SRC = 20, 16, 12, 10, 8
SIZES = {F_TITLE, F_SUB, F_HEAD, F_BODY, F_SRC}

W, H = 13.333, 7.5
L, R_ = 0.45, 0.45
TOP, BOTTOM = 1.3, 6.5
GUTTER = 0.3
Y_SRC, Y_BAR, BAR_H = 6.6, 7.06, 0.3      # sources / notes, contents table (flush to the bottom), its height

HERE = os.path.dirname(os.path.abspath(__file__))
ICON_DIR = os.path.join(HERE, "..", "assets", "icons")
ICON_CACHE = os.path.join(ICON_DIR, "_png")
import sys as _sys
_sys.path.insert(0, HERE)
import paths  # noqa: E402
TOOLKIT = os.environ.get("DEAL_DESK_TOOLKIT", str(paths.TOOLKIT))
LIBRARY = os.path.join(TOOLKIT, "Infographic Library.pptx")   # infographic()

# components that count as "visual" layouts for the AI-tells lint (a deck needs some of these)
VISUAL = {"icon", "stat_icons", "stat_rings", "hero_number", "pictogram", "tam_sam_som", "pill_rows", "side_tabs",
          "chevrons", "timeline", "numbered_steps", "hub_spoke", "pros_cons", "risk_matrix", "harvey", "logo_row",
          "infographic", "layout", "photo"}
CHROME = {"header", "footer", "section_tracker", "takeaway", "icon", "exhibit_takeaway", "pin"}  # not in the layout sig.
# exhibits: every content slide needs at least one (density standard, lessons #32)
EXHIBITS = {"table", "fin_table", "heatmap", "column", "bar", "stacked", "line", "fin_chart", "football_field", "photo",
            "logo_row", "infographic", "layout", "timeline", "harvey", "risk_matrix", "tam_sam_som", "stat_rings", "pictogram",
            "side_tabs"}
# argument blocks (lessons #35): a thesis pillar = bold claim + evidence -> so what -> implication; a risk / mitigant
# cell = bold title + 1-2 sentences. Fewer words than this is a bare fact fragment.
ARG_MIN_THESIS, ARG_MIN_CELL = 35, 15
ARG_HEADS = re.compile(r"thesis|merits|why invest|why now|key consideration|recommendation|reasons to", re.I)
MIN_BODY_WORDS = 120   # real bank pages: median 123 words where text is extractable; Qatalyst pitch book 224
MAX_EMPTY_BAND = 0.8   # inches of body height with nothing in it (bank decks: none)
TEXT_PAGE_WORDS = 200  # a text-only page is fine at this density (GS PowerSchool p3: ~250 words)


def rgb(h):
    return RGBColor.from_string(h)


class Deck:
    def __init__(self, template=None, sections=None):
        self.prs = Presentation(template) if template else Presentation()
        if not template:
            self.prs.slide_width, self.prs.slide_height = Inches(W), Inches(H)
        self.sections = list(sections or [])
        self.heads = {}       # slide_id -> (header, subheader)
        self.hdr_y = {}       # slide_id -> tops of block header bars (alignment check)
        self.bars = {}        # slide_id -> (x, y, w, h) of filled header bars (no second filled band right under one)
        self.n = 0
        self.used = {}        # slide_id -> [component names, in order]
        self.content = []     # slide_ids made with slide()
        self.credits = {}     # slide_id -> image credits, appended to the Sources line by footer()
        self.args = {}        # slide_id -> [(kind, label, words)] for argument blocks (THIN ARGUMENT lint, lessons #35)
        self.overflow = []    # layout(): slots whose text may not fit, unknown slot names

    # ---------- layout helpers ----------
    @property
    def body(self):
        return L, TOP, W - L - R_, BOTTOM - TOP

    def grid(self, i, n, span=1, top=None, bottom=None, weights=None):
        """Box for column i of n (optionally spanning columns, or with custom width weights)."""
        x0, y0, bw, bh = self.body
        y0 = top if top is not None else y0
        bh = (bottom if bottom is not None else BOTTOM) - y0
        weights = weights or [1] * n
        unit = (bw - GUTTER * (n - 1)) / sum(weights)
        x = x0 + sum(weights[:i]) * unit + GUTTER * i
        w = sum(weights[i:i + span]) * unit + GUTTER * (span - 1)
        return x, y0, w, bh

    def _tag(self, s, name):
        self.used.setdefault(s.slide_id, []).append(name)

    def _blank(self):
        layout = self.prs.slide_layouts[6] if len(self.prs.slide_layouts) > 6 else self.prs.slide_layouts[-1]
        s = self.prs.slides.add_slide(layout)
        for ph in list(s.placeholders):
            ph._element.getparent().remove(ph._element)
        self.n += 1
        return s

    def _text(self, s, x, y, w, h, text, size=F_BODY, bold=False, color=BLACK, align=PP_ALIGN.LEFT,
              anchor=MSO_ANCHOR.TOP, italic=False, wrap=True):
        tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = wrap
        tf.margin_left = tf.margin_right = Inches(0.02)
        tf.margin_top = tf.margin_bottom = Inches(0.02)
        tf.vertical_anchor = anchor
        lines = text if isinstance(text, list) else [text]
        for i, ln in enumerate(lines):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = align
            self._runs(p, ln, size, bold, color, italic)
        return tb

    @staticmethod
    def _runs(p, text, size, bold, color, italic=False):
        """Supports **bold** fragments inside text."""
        parts = text.split("**")
        for j, part in enumerate(parts):
            if not part:
                continue
            r = p.add_run()
            r.text = part
            f = r.font
            f.name, f.size, f.color.rgb, f.italic = FONT, Pt(size), rgb(color), italic
            f.bold = bold or (j % 2 == 1)

    def _line(self, s, x1, y1, x2, y2, color=NAVY, width=1.0, dash=None):
        ln = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
        ln.line.color.rgb = rgb(color)
        ln.line.width = Pt(width)
        if dash:
            ln.line.dash_style = dash
        self._flat(ln)
        return ln

    def _shape(self, s, kind, x, y, w, h, fill=NAVY, line=None, line_w=1.0, dash=None):
        r = s.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
        if fill:
            r.fill.solid()
            r.fill.fore_color.rgb = rgb(fill)
        else:
            r.fill.background()
        if line:
            r.line.color.rgb = rgb(line)
            r.line.width = Pt(line_w)
            if dash:
                r.line.dash_style = dash
        else:
            r.line.fill.background()
        r.shadow.inherit = False
        self._flat(r)
        return r

    @staticmethod
    def _flat(shp):
        """Drop the theme style python-pptx attaches (its effectRef is a drop shadow = the 'aura' on lines)."""
        el = shp._element
        st = el.find(qn("p:style"))
        if st is not None:
            el.remove(st)
        spPr = el.find(qn("p:spPr"))
        if spPr is not None and spPr.find(qn("a:effectLst")) is None:
            eff = spPr.makeelement(qn("a:effectLst"), {})
            ln = spPr.find(qn("a:ln"))
            if ln is not None:
                ln.addnext(eff)
            else:
                spPr.append(eff)

    def _rect(self, s, x, y, w, h, fill=NAVY, line=None):
        return self._shape(s, MSO_SHAPE.RECTANGLE, x, y, w, h, fill=fill, line=line)

    def _shape_text(self, shp, text, size=10, bold=False, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE,
                    margin=0.05):
        tf = shp.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(margin)
        tf.margin_top = tf.margin_bottom = Inches(0.02)
        tf.vertical_anchor = anchor
        lines = text if isinstance(text, list) else text.split("\n")
        for i, ln in enumerate(lines):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = align
            self._runs(p, ln, size, bold, color)

    # ---------- slides ----------
    def title_slide(self, title, subtitle="", date="", name=""):
        s = self._blank()
        self._rect(s, 0, 0, W, H, fill=NAVY)
        self._text(s, L, 2.4, 11.5, 1.1, title, size=F_TITLE, bold=True, color=WHITE, anchor=MSO_ANCHOR.BOTTOM)
        self._line(s, L, 3.6, L + 1.2, 3.6, WHITE, 2.0)
        self._text(s, L, 3.75, 11.5, 0.9, subtitle, size=F_SUB, color=LIGHT)
        self._text(s, L, 6.5, 8, 0.4, "  ·  ".join(t for t in (name, date) if t), size=F_BODY, color=LIGHT)
        return s

    def divider(self, number, title):
        s = self._blank()
        self._rect(s, 0, 0, 4.2, H, fill=NAVY)
        self._text(s, 0.6, 2.8, 3.2, 1.5, f"{number:02d}" if isinstance(number, int) else str(number), size=F_TITLE, bold=True, color=WHITE)
        self._text(s, 4.8, 3.1, 8, 1.2, title, size=F_TITLE, bold=True, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)
        return s

    def slide(self, header, subheader="", section=None):
        """Content slide. header = the contents section it belongs to (navy 20, one line); subheader = a few words
        introducing the slide (grey 16, one line). Old call slide(title, section=...) still works (section -> header).
        Draws the rule, the contents bar (when Deck(sections=...)) and the page number."""
        if section:
            header, subheader = section, header
        s = self._blank()
        self.content.append(s.slide_id)
        self.used.setdefault(s.slide_id, [])
        self.heads[s.slide_id] = (header, subheader)
        self._text(s, L, 0.28, W - L - R_, 0.42, header, size=F_TITLE, bold=True, color=NAVY, anchor=MSO_ANCHOR.BOTTOM,
                   wrap=False)
        if subheader:
            self._text(s, L, 0.72, W - L - R_, 0.36, subheader, size=F_SUB, color=GREY, wrap=False)
        self._line(s, L, 1.15, W - R_, 1.15, NAVY, 1.5)
        if self.sections:
            cur = next((sec for sec in self.sections if sec.lower() == header.lower()), None)
            self.section_tracker(s, self.sections, cur)
        # page number: far right, on the contents-table row, in the margin beyond the table
        self._text(s, W - R_ + 0.02, Y_BAR, 0.3, BAR_H, str(self.n), size=F_SRC, color=GREY,
                   align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        return s

    def section_tracker(self, s, sections, current):
        """Table of contents along the bottom: a real one-row table, full width of the title rule, 12pt bold white
        text in every cell. Current section: solid navy; the others: navy at 50% transparency; white separators
        (NSE / SATS style). slide() draws it when Deck(sections=...)."""
        if "section_tracker" in self.used.get(s.slide_id, []):
            return
        self._tag(s, "section_tracker")
        n = len(sections)
        shp = s.shapes.add_table(1, n, Inches(L), Inches(Y_BAR), Inches(W - L - R_), Inches(BAR_H))
        tbl = shp.table
        tblPr = tbl._tbl.tblPr
        style = tblPr.find(qn("a:tableStyleId"))
        if style is None:
            style = tblPr.makeelement(qn("a:tableStyleId"), {})
            tblPr.append(style)
        style.text = "{2D5ABB26-0587-4C30-8999-92F81FD0307C}"  # "No Style, No Grid"
        tblPr.set("firstRow", "0")
        tblPr.set("bandRow", "0")
        tbl.rows[0].height = Inches(BAR_H)
        for k, name in enumerate(sections):
            tbl.columns[k].width = Inches((W - L - R_) / n)
            cell = tbl.cell(0, k)
            hot = bool(current) and name.lower() == current.lower()
            cell.fill.solid()
            cell.fill.fore_color.rgb = rgb(NAVY)
            if not hot:
                self._alpha(cell._tc.tcPr.find(qn("a:solidFill")), 50)
            cell.margin_left = cell.margin_right = Inches(0.04)
            cell.margin_top = cell.margin_bottom = Inches(0.02)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            para = cell.text_frame.paragraphs[0]
            para.alignment = PP_ALIGN.CENTER
            self._runs(para, name, F_HEAD, True, WHITE)
            self._all_borders(cell, WHITE, 1.5)

    @staticmethod
    def _alpha(solid_fill, pct):
        """Add transparency to a solidFill: pct = opacity in % (50 = half transparent)."""
        clr = solid_fill[0]
        for old in clr.findall(qn("a:alpha")):
            clr.remove(old)
        clr.append(clr.makeelement(qn("a:alpha"), {"val": str(int(pct * 1000))}))

    @staticmethod
    def _all_borders(cell, color, width=0.75):
        tcPr = cell._tc.get_or_add_tcPr()
        for tag in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
            for old in tcPr.findall(qn(tag)):
                tcPr.remove(old)
        for i, tag in enumerate(("a:lnL", "a:lnR", "a:lnT", "a:lnB")):
            ln = tcPr.makeelement(qn(tag), {"w": str(Emu(Pt(width)))})
            sf = ln.makeelement(qn("a:solidFill"), {})
            sf.append(sf.makeelement(qn("a:srgbClr"), {"val": color}))
            ln.append(sf)
            tcPr.insert(i, ln)

    # ---------- icons ----------
    @staticmethod
    def icons():
        return sorted(f[:-4] for f in os.listdir(ICON_DIR) if f.endswith(".svg"))

    def _icon_png(self, name, color, stroke=1.6):
        os.makedirs(ICON_CACHE, exist_ok=True)
        out = os.path.join(ICON_CACHE, f"{name}_{color}_{stroke}.png")
        if not os.path.exists(out):
            import pymupdf
            src = os.path.join(ICON_DIR, f"{name}.svg")
            if not os.path.exists(src):
                raise KeyError(f"icon '{name}' not found; available: {', '.join(self.icons())}")
            svg = open(src, encoding="utf-8").read().replace("currentColor", f"#{color}")
            svg = svg.replace('stroke-width="2"', f'stroke-width="{stroke}"')
            doc = pymupdf.open(stream=svg.encode(), filetype="svg")
            doc[0].get_pixmap(matrix=pymupdf.Matrix(20, 20), alpha=True).save(out)
        return out

    def icon(self, s, name, x, y, size=0.45, color=NAVY):
        """Line icon (Tabler, MIT) recoloured and placed as a crisp PNG. size = inches (square)."""
        self._tag(s, "icon")
        return s.shapes.add_picture(self._icon_png(name, color), Inches(x), Inches(y), Inches(size), Inches(size))

    # ---------- block headers ----------
    def header(self, s, x, y, w, text, style="bar"):
        """Block header. 'bar' (default): filled navy bar, white bold centred text, 0.3in tall.
        'rule': navy bold text with a thin navy rule underneath (use sparingly, e.g. inside a dense column)."""
        self._tag(s, "header")
        self.hdr_y.setdefault(s.slide_id, []).append(round(y, 3))
        if style == "rule":
            self._text(s, x, y, w, 0.3, text, size=F_HEAD, bold=True, color=NAVY)
            self._line(s, x, y + 0.3, x + w, y + 0.3, NAVY, 0.75)
            return
        bar = self._rect(s, x, y, w, 0.3, fill=NAVY)
        self._shape_text(bar, text, size=F_HEAD, bold=True, color=WHITE)
        self.bars.setdefault(s.slide_id, []).append((x, y, w, 0.3))

    # ---------- text ----------
    def bullets(self, s, x, y, w, h, items, size=F_BODY, gap=4):
        """items: 'text' or ('text', level). '**Lead-in:** rest' makes the lead-in bold."""
        self._tag(s, "bullets")
        tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.02)
        for i, it in enumerate(items):
            text, lvl = (it, 0) if isinstance(it, str) else it
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.space_after = Pt(gap)
            bullet = "•" if lvl == 0 else "–"
            pPr = p._p.get_or_add_pPr()
            pPr.set("marL", str(Emu(Inches(0.16 + 0.2 * lvl))))
            pPr.set("indent", str(-Emu(Inches(0.16))))
            clr = pPr.makeelement(qn("a:buClr"), {})
            clr.append(clr.makeelement(qn("a:srgbClr"), {"val": NAVY}))
            pPr.append(clr)
            pPr.append(pPr.makeelement(qn("a:buSzPct"), {"val": "100000"}))
            pPr.append(pPr.makeelement(qn("a:buFont"), {"typeface": FONT}))
            pPr.append(pPr.makeelement(qn("a:buChar"), {"char": bullet}))
            self._runs(p, text, size, False, BLACK)
        return tb

    def takeaway(self, s, x, y, w, h, text, size=F_BODY, align=PP_ALIGN.CENTER):
        """The 'so what': dashed navy outline, no fill, no side bar (Pantheon style)."""
        self._tag(s, "takeaway")
        box = self._shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, fill=None, line=NAVY, line_w=1.0,
                          dash=MSO_LINE_DASH_STYLE.DASH)
        box.adjustments[0] = 0.12
        self._shape_text(box, text, size=size, color=BLACK, align=align, margin=0.12)
        return box

    def callout(self, s, x, y, w, h, text, size=F_BODY):
        """Kept for old scripts: now draws the dashed takeaway box (the pale box + side bar is banned)."""
        return self.takeaway(s, x, y, w, h, text, size=size, align=PP_ALIGN.LEFT)

    # ---------- key numbers (no boxed tiles) ----------
    def stat_icons(self, s, x, y, w, h, items, cols=None, size=F_HEAD, label_size=F_BODY, icon_size=0.5):
        """Icon, big number, label; no box (Favour / Pantheon). items = [(icon, value, label)]. Grid if cols < len."""
        self._tag(s, "stat_icons")
        cols = cols or len(items)
        rows = math.ceil(len(items) / cols)
        cw, ch = w / cols, h / rows
        for i, (ic, val, lab) in enumerate(items):
            cx, cy = x + (i % cols) * cw, y + (i // cols) * ch
            self.icon(s, ic, cx + (cw - icon_size) / 2, cy + 0.02, icon_size)
            self._text(s, cx, cy + icon_size + 0.06, cw, max(size / 72 * 1.35, 0.25), val, size=size, bold=True, color=BLACK,
                       align=PP_ALIGN.CENTER)
            ly = cy + icon_size + 0.08 + max(size / 72 * 1.35, 0.25)
            self._text(s, cx + 0.05, ly, cw - 0.1, max(ch - (ly - cy), 0.3), lab, size=label_size, color=BLACK,
                       align=PP_ALIGN.CENTER)

    def stat_strip(self, s, x, y, w, h, items, size=F_HEAD, label_size=F_BODY, align=PP_ALIGN.LEFT):
        """Numbers separated by thin vertical grey dividers; no fill (sits well under a chart or title).
        items = [(value, label)]."""
        self._tag(s, "stat_strip")
        n = len(items)
        cw = w / n
        pad = 0.18
        for i, (val, lab) in enumerate(items):
            cx = x + i * cw
            if i:
                self._line(s, cx, y + 0.05, cx, y + h - 0.05, LGREY, 1.0)
            tx = cx + (pad if i else 0)
            tw = cw - pad - (pad if i else 0)
            self._text(s, tx, y, tw, h * 0.55, val, size=size, bold=True, color=BLACK, align=align,
                       anchor=MSO_ANCHOR.BOTTOM, wrap=False)
            self._text(s, tx, y + h * 0.57, tw, h * 0.43, lab, size=label_size, color=BLACK, align=align)

    def kpis(self, s, x, y, w, h, items, cols=None):
        """Old name: now a stat_strip (no pale boxes with side bars)."""
        return self.stat_strip(s, x, y, w, h, items)

    def stat_rings(self, s, x, y, w, h, items, size=F_HEAD, label_size=F_BODY, hole=72):
        """Doughnut rings with the % in the centre (PwC / Sygnum). items = [(share 0-1, label)]."""
        self._tag(s, "stat_rings")
        n = len(items)
        cw = w / n
        d = min(cw - 0.2, h - 0.55)
        for i, (p, lab) in enumerate(items):
            cx = x + i * cw + (cw - d) / 2
            cd = CategoryChartData()
            cd.categories = ["a", "b"]
            cd.add_series("s", [p, max(1 - p, 0)])
            gf = s.shapes.add_chart(XL_CHART_TYPE.DOUGHNUT, Inches(cx), Inches(y), Inches(d), Inches(d), cd)
            ch = gf.chart
            ch.has_legend = False
            ch.has_title = False
            plot = ch.plots[0]
            plot.has_data_labels = False
            for k, col in enumerate(([NAVY, MID, STEEL][i % 3], PALEGREY)):
                pt = plot.series[0].points[k]
                pt.format.fill.solid()
                pt.format.fill.fore_color.rgb = rgb(col)
                pt.format.line.fill.background()
            dn = plot._element
            hs = dn.find(qn("c:holeSize"))
            if hs is None:
                hs = dn.makeelement(qn("c:holeSize"), {})
                dn.append(hs)
            hs.set("val", str(hole))
            self._text(s, cx, y + d / 2 - 0.25, d, 0.5, f"{p:.0%}" if isinstance(p, float) else str(p), size=size,
                       bold=True, color=BLACK, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            self._text(s, x + i * cw + 0.05, y + d + 0.05, cw - 0.1, h - d - 0.05, lab, size=label_size, color=BLACK,
                       align=PP_ALIGN.CENTER)

    def hero_number(self, s, x, y, w, h, value, label, points=(), size=F_HEAD, split=0.4):
        """One big number with its label; optional supporting points to the right of a thin grey divider."""
        self._tag(s, "hero_number")
        lw = w * split if points else w
        self._text(s, x, y + h / 2 - 0.3, lw, 0.28, value, size=size, bold=True, color=BLACK, anchor=MSO_ANCHOR.BOTTOM,
                   wrap=False)
        self._text(s, x, y + h / 2, lw, h / 2, label, size=F_BODY, color=BLACK)
        if points:
            self._line(s, x + lw + 0.1, y + 0.1, x + lw + 0.1, y + h - 0.1, LGREY, 1.0)
            tb = self.bullets(s, x + lw + 0.3, y + 0.05, w - lw - 0.3, h - 0.1, list(points), size=F_BODY, gap=5)
            tb.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
            self.used[s.slide_id].pop()  # these bullets are part of the hero block

    def pictogram(self, s, x, y, w, h, share, total=20, cols=10, icon="person-filled", label=None, size=None):
        """Row(s) of icons, `share` of them navy and the rest light grey (Pantheon labour-force style)."""
        self._tag(s, "pictogram")
        rows = math.ceil(total / cols)
        lab_h = 0.45 if label else 0
        gx = w / cols
        sz = size or min(gx * 0.82, (h - lab_h) / rows * 0.82)
        gy = sz * 1.3
        on = round(share * total)
        for k in range(total):
            r, c = divmod(k, cols)
            self.icon(s, icon, x + c * gx + (gx - sz) / 2, y + r * gy + (gy - sz) / 2, sz, NAVY if k < on else LGREY)
        if label:
            self._text(s, x, y + rows * gy + 0.08, w, lab_h, label, size=F_BODY, color=BLACK)

    def tam_sam_som(self, s, x, y, w, h, levels, size=F_HEAD):
        """Nested, bottom-aligned circles with the values listed to the right.
        levels = [(tag, value, description)] from largest (TAM) to smallest (SOM)."""
        self._tag(s, "tam_sam_som")
        dia = [h, h * 0.68, h * 0.38]
        fills = [LIGHT, STEEL, NAVY]
        cx = x + h / 2
        tag_y = []
        for k, (dd, f) in enumerate(zip(dia, fills)):
            self._shape(s, MSO_SHAPE.OVAL, cx - dd / 2, y + h - dd, dd, dd, fill=f)
            ty = y + h - dd + (0.1 if k < 2 else dd / 2 - 0.15)
            tag_y.append(ty)
            self._text(s, cx - 0.6, ty, 1.2, 0.3, levels[k][0], size=F_BODY, bold=True, color=WHITE,
                       align=PP_ALIGN.CENTER)
        tx = x + h + 0.35
        rh = h / 3
        for k, (tag, val, desc) in enumerate(levels):
            ry = y + k * rh
            self._line(s, cx + 0.62 if k < 2 else cx + dia[2] / 2, tag_y[k] + 0.15, tx - 0.08, ry + 0.25, LGREY, 0.75,
                       dash=MSO_LINE_DASH_STYLE.SQUARE_DOT)
            self._text(s, tx, ry + 0.05, w - (tx - x), 0.3, [f"{val}"], size=size, bold=True, color=BLACK)
            self._text(s, tx, ry + 0.35, w - (tx - x), rh - 0.38, f"**{tag}:** {desc}", size=F_BODY, color=BLACK)

    # ---------- structure layouts ----------
    def pill_rows(self, s, x, y, w, h, rows, label_w=None, size=F_BODY, gap=0.14, max_row_h=1.2):
        """Rounded outlined label on the left, bullets on the right (Pantheon 'Global leader' slide).
        rows = [(label, [bullets])]; label may be 'Title\\nsub-line'."""
        self._tag(s, "pill_rows")
        n = len(rows)
        rh = min((h - gap * (n - 1)) / n, max_row_h)
        lw = label_w or min(2.1, w * 0.36)
        for i, (lab, pts) in enumerate(rows):
            ry = y + i * (rh + gap)
            pill = self._shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, ry, lw, rh, fill=WHITE, line=NAVY, line_w=1.5)
            pill.adjustments[0] = 0.18
            parts = lab.split("\n")
            lines = [f"**{parts[0]}**"] + parts[1:]
            self._shape_text(pill, lines, size=F_HEAD, color=BLACK, margin=0.08)
            tb = self.bullets(s, x + lw + 0.2, ry, w - lw - 0.2, rh, pts, size=size, gap=3)
            tb.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
            self.used[s.slide_id].pop()

    def side_tabs(self, s, x, y, w, h, rows, tab_w=1.7, size=F_BODY, max_row_h=1.2, gap=None):
        """A real 2-column table (Favour investment summary; Benedict's edit): navy label cells with white bold text,
        separated by thick white rules; content cells white, thin grey rule under each row.
        rows = [(label, body)]. body is one of:
          - (claim, text): an ARGUMENT row (thesis pillar, key consideration, reason to invest; lessons #35): the bold
            one-line claim on its own line, then 2-3 sentences evidence -> so what -> implication, left-aligned.
            Aim for 45-60 words; under ARG_MIN_THESIS words is flagged THIN ARGUMENT.
          - [bullets] or "text": a DATA row (facts / summary), centred. Not for a thesis (lint flags it there)."""
        self._tag(s, "side_tabs")
        n = len(rows)
        rh = min(h / n, max_row_h)
        shp = s.shapes.add_table(n, 2, Inches(x), Inches(y), Inches(w), Inches(rh * n))
        shp.name = f"Side tabs {shp.shape_id}"
        tbl = shp.table
        tblPr = tbl._tbl.tblPr
        style = tblPr.find(qn("a:tableStyleId"))
        if style is None:
            style = tblPr.makeelement(qn("a:tableStyleId"), {})
            tblPr.append(style)
        style.text = "{2D5ABB26-0587-4C30-8999-92F81FD0307C}"  # "No Style, No Grid"
        tblPr.set("firstRow", "0")
        tblPr.set("bandRow", "0")
        tbl.columns[0].width = Inches(tab_w)
        tbl.columns[1].width = Inches(w - tab_w)
        for i, (lab, body) in enumerate(rows):
            tbl.rows[i].height = Inches(rh)
            tab, cell = tbl.cell(i, 0), tbl.cell(i, 1)
            for c, fill in ((tab, NAVY), (cell, WHITE)):
                c.fill.solid()
                c.fill.fore_color.rgb = rgb(fill)
                c.vertical_anchor = MSO_ANCHOR.MIDDLE
                c.margin_left = c.margin_right = Inches(0.1)
            p = tab.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            self._runs(p, lab.upper(), F_BODY, True, WHITE)
            argument = isinstance(body, tuple) and len(body) == 2
            if argument:
                claim, text = body
                cell.margin_left = cell.margin_right = Inches(0.15)
                self.args.setdefault(s.slide_id, []).append(
                    ("thesis", lab, len(f"{claim} {text}".replace("**", "").split())))
                p = cell.text_frame.paragraphs[0]
                p.space_after = Pt(3)
                self._runs(p, claim.replace("**", ""), size, True, BLACK)
                p = cell.text_frame.add_paragraph()
                self._runs(p, text, size, False, BLACK)
            else:
                self.args.setdefault(s.slide_id, []).append(("data_tabs", lab, 0))
            items = [] if argument else ([body] if isinstance(body, str) else list(body))
            for k, it in enumerate(items):
                p = cell.text_frame.paragraphs[0] if k == 0 else cell.text_frame.add_paragraph()
                p.alignment = PP_ALIGN.CENTER
                p.space_after = Pt(2)
                if not isinstance(body, str):
                    pPr = p._p.get_or_add_pPr()
                    pPr.set("marL", str(Emu(Inches(0.16))))
                    pPr.set("indent", str(-Emu(Inches(0.16))))
                    clr = pPr.makeelement(qn("a:buClr"), {})
                    clr.append(clr.makeelement(qn("a:srgbClr"), {"val": NAVY}))
                    pPr.append(clr)
                    pPr.append(pPr.makeelement(qn("a:buSzPct"), {"val": "100000"}))
                    pPr.append(pPr.makeelement(qn("a:buFont"), {"typeface": FONT}))
                    pPr.append(pPr.makeelement(qn("a:buChar"), {"char": "•"}))
                self._runs(p, it, size, False, BLACK)
            self._borders(tab, bottom=WHITE if i < n - 1 else None, width=2.25)
            self._borders(cell, bottom=LGREY, width=1.0)
        return shp

    def chevrons(self, s, x, y, w, h, steps, chev_h=0.55, size=F_BODY, highlight=None):
        """Process / plan as a row of chevrons with text underneath. steps = [(title, text or [bullets])].
        All navy; pass highlight=i to make one navy and the rest steel."""
        self._tag(s, "chevrons")
        n = len(steps)
        ov = 0.12
        cw = (w + ov * (n - 1)) / n
        for i, (title, body) in enumerate(steps):
            cx = x + i * (cw - ov)
            kind = MSO_SHAPE.PENTAGON if i == 0 else MSO_SHAPE.CHEVRON
            col = NAVY_RAMP[1 + min(i, 2)] if highlight is None else (NAVY if highlight == i else STEEL)
            shp = self._shape(s, kind, cx, y, cw, chev_h, fill=col)
            shp.adjustments[0] = 0.35
            self._shape_text(shp, title, size=size, bold=True, color=WHITE, margin=0.25 if i else 0.1)
            by = y + chev_h + 0.12
            if isinstance(body, str):
                self._text(s, cx + 0.05, by, cw - ov - 0.1, h - chev_h - 0.12, body, size=size, color=BLACK)
            else:
                self.bullets(s, cx + 0.05, by, cw - ov - 0.1, h - chev_h - 0.12, body, size=size, gap=3)
                self.used[s.slide_id].pop()

    def timeline(self, s, x, y, w, h, events, size=F_BODY, highlight=None):
        """Milestones on a horizontal line, labels alternating above / below. events = [(date, title, text)]."""
        self._tag(s, "timeline")
        n = len(events)
        mid = y + h / 2
        self._line(s, x, mid, x + w, mid, NAVY, 1.75)
        step = w / n
        half = h / 2 - 0.2
        for i, (date, title, text) in enumerate(events):
            cx = x + step * (i + 0.5)
            hot = highlight is None or highlight == i
            d = 0.2
            dot = GOLD if highlight == i else NAVY
            self._shape(s, MSO_SHAPE.OVAL, cx - d / 2, mid - d / 2, d, d, fill=dot if hot else WHITE, line=dot, line_w=1.5)
            tw = min(step * 1.7, 2.6)
            tx = min(max(cx - tw / 2, x), x + w - tw)   # keep labels inside the block
            if i % 2 == 0:
                self._line(s, cx, mid - 0.1, cx, mid - 0.3, LGREY, 0.75)
                self._text(s, tx, y, tw, half - 0.1, [f"**{date}**", f"**{title}**", text], size=size,
                           color=BLACK, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.BOTTOM)
            else:
                self._line(s, cx, mid + 0.1, cx, mid + 0.3, LGREY, 0.75)
                self._text(s, tx, mid + 0.32, tw, half - 0.1, [f"**{date}**", f"**{title}**", text], size=size,
                           color=BLACK, align=PP_ALIGN.CENTER)

    def numbered_steps(self, s, x, y, w, h, steps, size=F_BODY, direction="down", d=0.42):
        """Numbered navy circles joined by a thin line, each with a bold title and a line of text.
        steps = [(title, text)]. direction 'down' (list) or 'across'."""
        self._tag(s, "numbered_steps")
        n = len(steps)
        if direction == "down":
            rh = h / n
            self._line(s, x + d / 2, y + d / 2, x + d / 2, y + (n - 1) * rh + d / 2, LGREY, 1.0)
            for i, (title, text) in enumerate(steps):
                ry = y + i * rh
                c = self._shape(s, MSO_SHAPE.OVAL, x, ry, d, d, fill=NAVY)
                self._shape_text(c, str(i + 1), size=F_HEAD, bold=True, margin=0)
                self._text(s, x + d + 0.18, ry - 0.02, w - d - 0.18, rh, [f"**{title}**", text], size=size)
        else:
            cw = w / n
            self._line(s, x + cw / 2, y + d / 2, x + cw * (n - 0.5), y + d / 2, LGREY, 1.0)
            for i, (title, text) in enumerate(steps):
                cx = x + i * cw
                c = self._shape(s, MSO_SHAPE.OVAL, cx + (cw - d) / 2, y, d, d, fill=NAVY)
                self._shape_text(c, str(i + 1), size=F_HEAD, bold=True, margin=0)
                self._text(s, cx + 0.05, y + d + 0.1, cw - 0.1, h - d - 0.1, [f"**{title}**", text], size=size,
                           align=PP_ALIGN.CENTER)

    def hub_spoke(self, s, x, y, w, h, centre, spokes, size=F_BODY):
        """Company in the middle, drivers around it. spokes = [(icon or None, title, text)] (4–6 work best)."""
        self._tag(s, "hub_spoke")
        cx, cy = x + w / 2, y + h / 2
        cd = min(1.5, h * 0.36)
        n = len(spokes)
        rx, ry = w * 0.25, h * 0.37
        sd = 0.6
        pts = []
        for i in range(n):
            a = -math.pi / 2 + 2 * math.pi * i / n + (math.pi / n if n % 2 == 0 else 0)
            pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
        for px, py in pts:
            self._line(s, cx, cy, px, py, LGREY, 1.0)
        c = self._shape(s, MSO_SHAPE.OVAL, cx - cd / 2, cy - cd / 2, cd, cd, fill=NAVY)
        self._shape_text(c, centre, size=F_HEAD, bold=True, margin=0.05)
        tw = w / 2 - rx - sd / 2 - 0.15 + w * 0.1
        for (px, py), (ic, title, text) in zip(pts, spokes):
            self._shape(s, MSO_SHAPE.OVAL, px - sd / 2, py - sd / 2, sd, sd, fill=WHITE, line=NAVY, line_w=1.5)
            if ic:
                self.icon(s, ic, px - 0.17, py - 0.17, 0.34)
            right = px >= cx - 0.01
            if abs(px - cx) < 0.05:   # top / bottom spoke: text beside it on the right
                right = True
            tx = px + sd / 2 + 0.1 if right else max(x, px - sd / 2 - 0.1 - tw)
            tww = min(tw, x + w - tx) if right else px - sd / 2 - 0.1 - tx
            self._text(s, tx, py - 0.35, tww, 0.8, [f"**{title}**", text], size=size,
                       align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

    def pros_cons(self, s, x, y, w, h, pros, cons, titles=("Strengths", "Watch-points"), size=F_BODY, max_row_h=0.6):
        """Two columns with filled header bars; ticks (navy) and crosses (grey) instead of bullets."""
        self._tag(s, "pros_cons")
        cw = (w - 0.25) / 2
        for k, (items, title, ic, col) in enumerate(((pros, titles[0], "check", NAVY), (cons, titles[1], "x", BLACK))):
            cx = x + k * (cw + 0.25)
            self.header(s, cx, y, cw, title)
            rh = min((h - 0.45) / max(len(items), 1), max_row_h)
            for i, it in enumerate(items):
                ry = y + 0.45 + i * rh
                self.icon(s, ic, cx, ry + 0.02, 0.26, col)
                self._text(s, cx + 0.36, ry, cw - 0.36, rh, it, size=size)

    def risk_matrix(self, s, x, y, w, h, rows, heads=("Key risk", "Mitigant"), size=F_BODY, levels=None, max_row_h=1.2):
        """Risk -> mitigant rows joined by a small arrow; optional severity Harvey ball (0-4) per risk.
        rows = [(risk, mitigant)]; each side is either
          - (title, text): bold short title on its own line + 1-2 sentences (lessons #35). Risk: what could go wrong
            and how it hurts returns, quantified where a source allows. Mitigant: the action, how it works, and
            "**What remains:**" the residual risk. Aim for 25-35 words a cell; under ARG_MIN_CELL is THIN ARGUMENT.
          - "text": a one-line cell (old style; the lint flags it as THIN ARGUMENT).
        Returns the y of the last row's bottom."""
        self._tag(s, "risk_matrix")
        lv_w = 0.55 if levels else 0
        rw = (w - lv_w - 0.5) / 2
        self._text(s, x + lv_w, y, rw, 0.25, heads[0].upper(), size=F_BODY, bold=True, color=BLACK)
        self._text(s, x + lv_w + rw + 0.5, y, rw, 0.25, heads[1].upper(), size=F_BODY, bold=True, color=BLACK)
        if levels:
            self._text(s, x, y, lv_w, 0.25, "LEVEL", size=F_BODY, bold=True, color=BLACK, align=PP_ALIGN.CENTER)
        self._line(s, x, y + 0.28, x + w, y + 0.28, NAVY, 1.0)
        n = len(rows)
        rh = min((h - 0.35) / n, max_row_h)

        def cell(v, side):
            if isinstance(v, tuple):
                title, text = v
                words = len(f"{title} {text}".replace("**", "").split())
                lines = [f"**{title.replace('**', '')}**", text]
            else:
                words, lines = len(v.replace("**", "").split()), [v]
            self.args.setdefault(s.slide_id, []).append((side, lines[0].replace("**", ""), words))
            return lines

        for i, (risk, mit) in enumerate(rows):
            ry = y + 0.35 + i * rh
            if levels:
                self._harvey_ball(s, x + lv_w / 2 - 0.13, ry + rh / 2 - 0.13, 0.26, levels[i])
            self._text(s, x + lv_w, ry, rw, rh, cell(risk, "risk"), size=size, anchor=MSO_ANCHOR.MIDDLE)
            a = self._shape(s, MSO_SHAPE.RIGHT_ARROW, x + lv_w + rw + 0.12, ry + rh / 2 - 0.1, 0.26, 0.2, fill=STEEL)
            a.adjustments[0] = 0.5
            self._text(s, x + lv_w + rw + 0.5, ry, rw, rh, cell(mit, "mitigant"), size=size, anchor=MSO_ANCHOR.MIDDLE)
            if i < n - 1:
                self._line(s, x, ry + rh, x + w, ry + rh, LGREY, 0.75)
        return y + 0.35 + n * rh

    def _harvey_ball(self, s, x, y, d, q):
        """q = 0..4 quarters filled, from 12 o'clock clockwise."""
        self._shape(s, MSO_SHAPE.OVAL, x, y, d, d, fill=WHITE, line=NAVY, line_w=1.0)
        if q >= 4:
            self._shape(s, MSO_SHAPE.OVAL, x, y, d, d, fill=NAVY, line=NAVY, line_w=1.0)
        elif q > 0:
            pie = self._shape(s, MSO_SHAPE.PIE, x, y, d, d, fill=NAVY)
            pie.adjustments[0] = 270 * 0.6
            pie.adjustments[1] = ((270 + 90 * q) % 360) * 0.6

    def harvey(self, s, x, y, w, row_labels, col_labels, scores, size=F_BODY, first_w=None, row_h=0.42):
        """Scoring grid with Harvey balls (peer / option comparison). scores[i][j] = 0..4."""
        self._tag(s, "harvey")
        fw = first_w or w * 0.34
        cw = (w - fw) / len(col_labels)
        for j, c in enumerate(col_labels):
            self._text(s, x + fw + j * cw, y, cw, 0.4, c, size=size, bold=True, color=BLACK, align=PP_ALIGN.CENTER,
                       anchor=MSO_ANCHOR.BOTTOM)
        self._line(s, x, y + 0.45, x + w, y + 0.45, NAVY, 1.0)
        for i, r in enumerate(row_labels):
            ry = y + 0.5 + i * row_h
            self._text(s, x, ry, fw, row_h, r, size=size, anchor=MSO_ANCHOR.MIDDLE)
            for j in range(len(col_labels)):
                self._harvey_ball(s, x + fw + j * cw + cw / 2 - 0.13, ry + row_h / 2 - 0.13, 0.26, scores[i][j])
            self._line(s, x, ry + row_h, x + w, ry + row_h, LGREY, 0.75)
        return y + 0.5 + len(row_labels) * row_h

    def logo_row(self, s, x, y, w, h, names, highlight=None, cols=None, size=F_BODY, logos=None, outline=True,
                 pad=0.1):
        """Tiles for peers / buyers / sponsors / operators. logos = {name: png path} puts the real logo in the tile
        (fitted, centred, own colours); names without a logo show as text. Navy outline; the highlight in gold."""
        self._tag(s, "logo_row")
        logos = logos or {}
        cols = cols or len(names)
        rows = math.ceil(len(names) / cols)
        g = 0.12
        cw, ch = (w - g * (cols - 1)) / cols, (h - g * (rows - 1)) / rows
        for i, nm in enumerate(names):
            cx, cy = x + (i % cols) * (cw + g), y + (i // cols) * (ch + g)
            hot = highlight is not None and (nm == highlight or i == highlight)
            if outline or hot:
                t = self._shape(s, MSO_SHAPE.ROUNDED_RECTANGLE, cx, cy, cw, ch, fill=WHITE,
                                line=GOLD if hot else NAVY, line_w=1.75 if hot else 1.0)
                t.adjustments[0] = 0.15
            else:
                t = None
            if nm in logos:
                self._fit_picture(s, logos[nm], cx + pad, cy + pad, cw - 2 * pad, ch - 2 * pad)
            elif t is not None:
                self._shape_text(t, nm, size=size, bold=hot, color=NAVY if hot else BLACK)
            else:   # no logo file: the name in bold, standing in for the wordmark
                self._text(s, cx, cy, cw, ch, nm, size=F_HEAD, bold=True, color=BLACK, align=PP_ALIGN.CENTER,
                           anchor=MSO_ANCHOR.MIDDLE)

    # ---------- images ----------
    @staticmethod
    def _img_size(path):
        import pymupdf
        pm = pymupdf.Pixmap(path)
        return pm.width, pm.height

    def _fit_picture(self, s, path, x, y, w, h):
        """Place an image inside the box, whole, keeping its shape (logos)."""
        iw, ih = self._img_size(path)
        k = min(w / iw, h / ih)
        pw, ph = iw * k, ih * k
        return s.shapes.add_picture(path, Inches(x + (w - pw) / 2), Inches(y + (h - ph) / 2), Inches(pw), Inches(ph))

    def photo(self, s, path, x, y, w, h, credit=None, focus=(0.5, 0.5)):
        """Photo or map that fills the box exactly: cropped, never stretched. focus = (x, y) share of the image to
        keep in view when cropping. credit (or the fetch_image manifest entry) is added to the slide's Sources."""
        self._tag(s, "photo")
        iw, ih = self._img_size(path)
        pic = s.shapes.add_picture(path, Inches(x), Inches(y), Inches(w), Inches(h))
        box, img = w / h, iw / ih
        if img > box:      # too wide: crop the sides
            keep = box / img
            left = (1 - keep) * focus[0]
            pic.crop_left, pic.crop_right = left, 1 - keep - left
        elif img < box:    # too tall: crop top and bottom
            keep = img / box
            top = (1 - keep) * focus[1]
            pic.crop_top, pic.crop_bottom = top, 1 - keep - top
        if credit is None:
            try:
                from fetch_image import credit as _cr
                credit = _cr(os.path.splitext(os.path.basename(path))[0])
            except ImportError:
                credit = ""
        if credit:
            self.credits.setdefault(s.slide_id, []).append(credit)
        return pic

    def pin(self, s, x, y, text, box, hot=False, d=0.16, size=F_BODY):
        """Map marker: a dot at (x, y) joined by a thin line to a white label box = (bx, by, bw, bh) with a navy
        outline (gold dot and outline for the one highlighted place). Use on top of photo() maps."""
        self._tag(s, "pin")
        col = GOLD if hot else NAVY
        bx, by, bw, bh = box
        self._line(s, x, y, min(max(x, bx), bx + bw), by + bh / 2 if not (bx <= x <= bx + bw) else (by if by > y else by + bh), col, 1.0)
        self._shape(s, MSO_SHAPE.OVAL, x - d / 2, y - d / 2, d, d, fill=col, line=WHITE, line_w=1.0)
        lab = self._shape(s, MSO_SHAPE.RECTANGLE, bx, by, bw, bh, fill=WHITE, line=col, line_w=1.25 if hot else 0.75)
        self._shape_text(lab, text, size=size, color=BLACK, align=PP_ALIGN.LEFT, margin=0.06)
        return lab

    def exhibit_takeaway(self, s, x, y, w, text, h=0.4, size=F_BODY):
        """Bold one-line (max two) finding directly under an exhibit's header bar, above the chart (Qatalyst style:
        'Data needing protection in 2020 is the size of the entire digital universe in 2018')."""
        self._tag(s, "exhibit_takeaway")
        return self._text(s, x, y, w, h, text, size=size, bold=True, color=BLACK, align=PP_ALIGN.CENTER,
                          anchor=MSO_ANCHOR.MIDDLE)

    # ---------- tables and charts ----------
    def table(self, s, x, y, w, rows, col_widths=None, size=F_BODY, row_h=0.28, bold_rows=(), shade_rows=(),
              num_cols=None, highlight_cell=None, header=True, header_style=None):
        """rows[0] = header. Numbers should be pre-formatted strings. Returns the table shape.
        header_style: "fill" = navy row, white text (a table standing alone); "rule" = bold black text, no fill, navy
        rule underneath (bank style: BofA Taro p11, Citi Chindata p5, Evercore Diversey p50). Default: "rule" when a
        filled header bar sits just above the table (never two filled bands in a row, lessons #34), else "fill"."""
        self._tag(s, "table")
        if header_style is None:
            under_bar = any(abs((by + bh) - y) < 0.9 and bx < x + w - 0.05 and x < bx + bw - 0.05
                            for bx, by, bw, bh in self.bars.get(s.slide_id, []))
            header_style = "rule" if under_bar else "fill"
        filled_head = header_style == "fill"
        nr, nc = len(rows), len(rows[0])
        shp = s.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(w), Inches(row_h * nr))
        tbl = shp.table
        tblPr = tbl._tbl.tblPr
        style = tblPr.find(qn("a:tableStyleId"))
        if style is None:
            style = tblPr.makeelement(qn("a:tableStyleId"), {})
            tblPr.append(style)
        style.text = "{2D5ABB26-0587-4C30-8999-92F81FD0307C}"  # "No Style, No Grid"; fills and rules set below
        tblPr.set("firstRow", "0")
        tblPr.set("bandRow", "0")
        cw = col_widths or [w / nc] * nc
        for j, cwj in enumerate(cw):
            tbl.columns[j].width = Inches(cwj)
        num_cols = set(range(1, nc)) if num_cols is None else set(num_cols)
        for i in range(nr):
            tbl.rows[i].height = Inches(row_h)
            for j in range(nc):
                cell = tbl.cell(i, j)
                cell.margin_left = cell.margin_right = Inches(0.06)
                cell.margin_top = cell.margin_bottom = Inches(0.02)
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                is_head = header and i == 0
                fill = NAVY if (is_head and filled_head) else (PALE if i in shade_rows else WHITE)
                if highlight_cell and (i, j) == highlight_cell:
                    fill = LIGHT
                cell.fill.solid()
                cell.fill.fore_color.rgb = rgb(fill)
                tf = cell.text_frame
                tf.word_wrap = True
                p = tf.paragraphs[0]
                p.alignment = PP_ALIGN.RIGHT if (j in num_cols) else PP_ALIGN.LEFT
                self._runs(p, str(rows[i][j]), size, is_head or i in bold_rows,
                           WHITE if (is_head and filled_head) else BLACK)
                self._pin_font(p, size)
                self._borders(cell, bottom=(LGREY if not is_head else NAVY), top=(BLACK if i in bold_rows and i > 0 else None),
                              width=1.25 if (is_head and not filled_head) else 0.75)
        return shp

    @staticmethod
    def _pin_font(p, size):
        """Set the end-of-paragraph font too: an empty cell otherwise uses PowerPoint's 18pt default and makes the
        whole row taller than the others (Benedict's critique of the Keppel P&L table, 26 Sep 2026)."""
        end = p._p.get_or_add_endParaRPr()
        end.set("sz", str(int(size * 100)))
        for old in end.findall(qn("a:latin")):
            end.remove(old)
        end.append(end.makeelement(qn("a:latin"), {"typeface": FONT}))

    def fin_table(self, s, x, y, w, periods, lines, label_w=None, size=F_BODY, row_h=0.23):
        """Financial summary table as banks put it on a slide (Goldman / Evercore board books; examples in
        ../assets/references/bank-financials/):
        - units once, in the block header above ("P&L summary ($m)"), never in the columns
        - header row = the periods only ("Year 0A", "2025E"): bold black, no fill, navy rule underneath
        - lines = [(label, [values...], kind)], kind:
            "key"  (alias "total"): bold, white fill like every row, "$" on the values (Revenue, EBITDA, net income)
            "line": regular weight
            "pct":  "% Growth" / "% Margin" row: italic, indented, directly under its line item
        - one font and size in every cell (Arial 10), every row the same height; negatives in brackets,
          missing values "-"; thin grey rule under each block."""
        label_w = label_w or w * (0.55 if len(periods) == 1 else 0.3)
        cw = [label_w] + [(w - label_w) / len(periods)] * len(periods)

        def fmt(v, kind):
            if v is None or v == "":
                return "\u2013"
            if isinstance(v, str):
                return v
            if kind == "pct":
                return f"({abs(v):.1%})" if v < 0 else f"{v:.1%}"
            n = f"({abs(v):,.1f})" if v < 0 else f"{v:,.1f}"
            return "$ " + n if kind == "key" else n

        rows = [[""] + list(periods)]
        kinds = []
        for ln in lines:
            lab, vals, kind = ln if len(ln) == 3 else (ln[0], ln[1], "line")
            kind = "key" if kind == "total" else kind
            rows.append([lab] + [fmt(v, kind) for v in vals])
            kinds.append(kind)
        shp = self.table(s, x, y, w, rows, col_widths=cw, size=size, row_h=row_h)
        self.used[s.slide_id][-1] = "fin_table"
        tbl = shp.table
        nc = len(rows[0])
        for j in range(nc):                                   # header: no fill, bold black, navy rule
            c = tbl.cell(0, j)
            c.fill.solid()
            c.fill.fore_color.rgb = rgb(WHITE)
            for r in c.text_frame.paragraphs[0].runs:
                r.font.color.rgb = rgb(BLACK)
                r.font.bold = True
            self._borders(c, bottom=NAVY, width=1.0)
        for i, kind in enumerate(kinds, 1):
            nxt = kinds[i] if i < len(kinds) else None
            rule = None if nxt == "pct" else LGREY            # rule under the whole block, not inside it
            for j in range(nc):
                cell = tbl.cell(i, j)
                runs = cell.text_frame.paragraphs[0].runs
                if kind == "key":                             # bold only; every row white (Benedict, 26 Sep 2026)
                    for r in runs:
                        r.font.bold = True
                if kind == "pct":
                    for r in runs:
                        r.font.italic = True
                        r.font.color.rgb = rgb(GREY)       # % rows grey (Benedict, 26 Sep 2026)
                    if j == 0:
                        cell.margin_left = Inches(0.22)
                self._borders(cell, bottom=rule)
        return shp

    def fin_chart(self, s, x, y, w, h, periods, values, strip=None, strip_label="% Margin", cagr=None, split=None,
                  number_format="#,##0.0", label_w=0.75, highlight=None):
        """Bank-style trend chart (Goldman p.16 / Evercore p.34 in ../assets/references/bank-financials/):
        columns with the value on top, period labels under the bars, an optional strip of % values
        (growth or margin) centred under each bar, CAGR labels with arrows above (cagr=[(i, j, "text")]),
        and a dashed line where forecasts start (split = index of the first forecast period).
        Units go in the block header above. One font, one size (Arial 10) throughout."""
        self._tag(s, "fin_chart")
        n = len(periods)
        top_h = 0.42 if cagr else 0.0
        lab_h = 0.22
        strip_h = 0.24 if strip is not None else 0.0
        cx, cw = x + label_w, w - label_w                   # bar area; label column on the left for the strip
        ch_y, ch_h = y + top_h, h - top_h - lab_h - strip_h
        slot = cw / n
        centre = [cx + (k + 0.5) * slot for k in range(n)]
        nums = [0 if v is None else v for v in values]
        ch = self._chart(s, cx, ch_y, cw, ch_h, XL_CHART_TYPE.COLUMN_CLUSTERED, list(periods), [("Value", nums)],
                         number_format=number_format, legend=False, gap=70)
        if highlight is not None:
            pt = ch.series[0].points[highlight]
            pt.format.fill.solid()
            pt.format.fill.fore_color.rgb = rgb(GOLD)
        ch.value_axis.minimum_scale = 0
        ch.value_axis.maximum_scale = max(nums) * 1.45 if max(nums) > 0 else 1   # room for the labels
        ch.category_axis.tick_label_position = XL_TICK_LABEL_POSITION.NONE
        pa = ch._chartSpace.chart.plotArea                   # plot area = the whole frame, so bar k sits at centre[k]
        lay = pa.find(qn("c:layout"))
        if lay is None:
            lay = pa.makeelement(qn("c:layout"), {})
            pa.insert(0, lay)
        for old in list(lay):
            lay.remove(old)
        ml = lay.makeelement(qn("c:manualLayout"), {})
        for tag, val in (("c:layoutTarget", "inner"), ("c:xMode", "edge"), ("c:yMode", "edge"),
                         ("c:x", "0"), ("c:y", "0"), ("c:w", "1"), ("c:h", "1")):
            ml.append(ml.makeelement(qn(tag), {"val": val}))
        lay.append(ml)
        yl = ch_y + ch_h
        for k, p in enumerate(periods):                      # period labels, then the % strip
            self._text(s, centre[k] - slot / 2, yl, slot, lab_h, str(p), align=PP_ALIGN.CENTER,
                       anchor=MSO_ANCHOR.MIDDLE, wrap=False)
        if strip is not None:
            ys = yl + lab_h
            self._text(s, x, ys, label_w, strip_h, strip_label, italic=True, color=GREY, anchor=MSO_ANCHOR.MIDDLE, wrap=False)
            for k, v in enumerate(strip):
                txt = "\u2013" if v is None else (f"({abs(v):.1%})" if v < 0 else f"{v:.1%}")
                self._text(s, centre[k] - slot / 2, ys, slot, strip_h, txt, italic=True, color=GREY, align=PP_ALIGN.CENTER,
                           anchor=MSO_ANCHOR.MIDDLE, wrap=False)
            self._line(s, x, ys + strip_h, x + w, ys + strip_h, LGREY, 0.75)
        if split:
            sx = cx + split * slot
            self._line(s, sx, y, sx, yl + lab_h + strip_h, GREY, 1.0, dash=MSO_LINE_DASH_STYLE.DASH)
        for (i0, i1, txt) in (cagr or []):
            x0, x1 = centre[i0] - slot * 0.4, centre[i1] + slot * 0.4
            self._text(s, x0, y, x1 - x0, 0.2, txt, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.BOTTOM)
            ln = self._line(s, x0, y + 0.25, x1, y + 0.25, NAVY, 1.0)
            end = ln.line._get_or_add_ln()
            end.append(end.makeelement(qn("a:tailEnd"), {"type": "triangle", "w": "med", "len": "med"}))
        return ch

    @staticmethod
    def _borders(cell, bottom=None, top=None, width=0.75):
        tcPr = cell._tc.get_or_add_tcPr()
        for tag in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):  # replace any earlier borders
            for old in tcPr.findall(qn(tag)):
                tcPr.remove(old)
        # schema order: lnL, lnR, lnT, lnB must come before the cell fill
        for i, (tag, color) in enumerate((("a:lnL", None), ("a:lnR", None), ("a:lnT", top), ("a:lnB", bottom))):
            ln = tcPr.makeelement(qn(tag), {"w": str(Emu(Pt(width))) if color else "0"})
            if color:
                sf = ln.makeelement(qn("a:solidFill"), {})
                sf.append(sf.makeelement(qn("a:srgbClr"), {"val": color}))
                ln.append(sf)
            else:
                ln.append(ln.makeelement(qn("a:noFill"), {}))
            tcPr.insert(i, ln)

    def heatmap(self, s, x, y, w, corner, col_head, row_head, values, fmt="{:.1%}", base=None, size=F_BODY, row_h=0.3,
                better="high"):
        """Sensitivity grid formatted exactly like the model's (xlstyle.sensitivity / heat_map): 3-colour scale, red
        (worst) -> white (median) -> green (best; better="low" flips it for costs); axis rows / columns unfilled
        with black rules; base=(i, j) bold and boxed in black."""
        rows = [[corner] + [str(c) for c in col_head]]
        for rh, vr in zip(row_head, values):
            rows.append([str(rh)] + [fmt.format(v) for v in vr])
        shp = self.table(s, x, y, w, rows, size=size, row_h=row_h, num_cols=range(0, len(col_head) + 1))
        self.used[s.slide_id][-1] = "heatmap"
        tbl = shp.table
        flat = sorted(v for r in values for v in r)
        lo, hi = flat[0], flat[-1]
        n = len(flat)
        med = flat[n // 2] if n % 2 else (flat[n // 2 - 1] + flat[n // 2]) / 2
        worst, best = (HEAT_RED, HEAT_GREEN) if better == "high" else (HEAT_GREEN, HEAT_RED)

        def mix(c1, c2, f):
            a, b = [int(c1[k:k + 2], 16) for k in (0, 2, 4)], [int(c2[k:k + 2], 16) for k in (0, 2, 4)]
            return "".join(f"{round(a[k] + (b[k] - a[k]) * max(0.0, min(1.0, f))):02X}" for k in range(3))

        def colour(v):
            if v <= med:
                return mix(worst, HEAT_MID, 1.0 if med == lo else (v - lo) / (med - lo))
            return mix(HEAT_MID, best, 0.0 if hi == med else (v - med) / (hi - med))

        nc = len(col_head) + 1
        for j2 in range(nc):                     # axis row: no fill, bold black, black rule underneath
            c = tbl.cell(0, j2)
            c.fill.solid()
            c.fill.fore_color.rgb = rgb(WHITE)
            for r in c.text_frame.paragraphs[0].runs:
                r.font.color.rgb = rgb(BLACK)
                r.font.bold = True
            self._cell_lines(c, bottom=BLACK, right=BLACK if j2 == 0 else None)
        for i2, vr in enumerate(values):
            c0 = tbl.cell(i2 + 1, 0)             # axis column: no fill, black rule on the right
            c0.fill.solid()
            c0.fill.fore_color.rgb = rgb(WHITE)
            self._cell_lines(c0, right=BLACK)
            for j2, v in enumerate(vr):
                cell = tbl.cell(i2 + 1, j2 + 1)
                cell.fill.solid()
                cell.fill.fore_color.rgb = rgb(colour(v))
                if base and (i2, j2) == base:
                    for r in cell.text_frame.paragraphs[0].runs:
                        r.font.bold = True
                    self._cell_lines(cell, top=BLACK, bottom=BLACK, left=BLACK, right=BLACK, width=1.5)
                elif base:   # neighbours draw the shared edge too, or PowerPoint drops half the box
                    bi, bj = base
                    k = {"left": (i2, j2 - 1), "right": (i2, j2 + 1), "top": (i2 - 1, j2), "bottom": (i2 + 1, j2)}
                    self._cell_lines(cell, width=1.5, **{e: BLACK for e, pos in k.items() if pos == (bi, bj)})
                else:
                    self._cell_lines(cell)
        if base:   # axis cells next to the base cell
            bi, bj = base
            if bj == 0:
                self._cell_lines(tbl.cell(bi + 1, 0), right=BLACK, width=1.5)
            if bi == 0:
                self._cell_lines(tbl.cell(0, bj + 1), bottom=BLACK, width=1.5)
        return shp

    @staticmethod
    def _cell_lines(cell, top=None, bottom=None, left=None, right=None, width=0.75):
        """Set all four cell borders (None = no line)."""
        tcPr = cell._tc.get_or_add_tcPr()
        for tag in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
            for old in tcPr.findall(qn(tag)):
                tcPr.remove(old)
        for k, (tag, color) in enumerate((("a:lnL", left), ("a:lnR", right), ("a:lnT", top), ("a:lnB", bottom))):
            ln = tcPr.makeelement(qn(tag), {"w": str(Emu(Pt(width))) if color else "0"})
            if color:
                sf = ln.makeelement(qn("a:solidFill"), {})
                sf.append(sf.makeelement(qn("a:srgbClr"), {"val": color}))
                ln.append(sf)
            else:
                ln.append(ln.makeelement(qn("a:noFill"), {}))
            tcPr.insert(k, ln)

    def _chart(self, s, x, y, w, h, kind, categories, series, number_format='#,##0', labels=True, legend=None,
               colors=None, highlight=None, font=F_BODY, gap=60):
        cd = CategoryChartData()
        cd.categories = categories
        for name, vals in series:
            cd.add_series(name, vals)
        gf = s.shapes.add_chart(kind, Inches(x), Inches(y), Inches(w), Inches(h), cd)
        ch = gf.chart
        ch.font.name, ch.font.size = FONT, Pt(font)
        ch.font.color.rgb = rgb(BLACK)
        ch.has_title = False
        multi = len(series) > 1
        ch.has_legend = multi if legend is None else legend
        if ch.has_legend:
            ch.legend.position = XL_LEGEND_POSITION.TOP
            ch.legend.include_in_layout = False
            ch.legend.font.size = Pt(font)
        colors = colors or SERIES
        is_line = kind in (XL_CHART_TYPE.LINE, XL_CHART_TYPE.LINE_MARKERS)
        for i, ser in enumerate(ch.series):
            c = colors[i % len(colors)]
            if is_line:
                ser.format.line.color.rgb = rgb(c)
                ser.format.line.width = Pt(2)
                ser.smooth = False
            else:
                ser.format.fill.solid()
                ser.format.fill.fore_color.rgb = rgb(c)
        if highlight is not None and not is_line:
            for i, ser in enumerate(ch.series):
                for k in range(len(categories)):
                    pt = ser.points[k]
                    pt.format.fill.solid()
                    pt.format.fill.fore_color.rgb = rgb(GOLD if k == highlight else NAVY)
        plot = ch.plots[0]
        if hasattr(plot, "gap_width"):
            plot.gap_width = gap
        if hasattr(plot, "overlap") and kind in (XL_CHART_TYPE.COLUMN_STACKED, XL_CHART_TYPE.BAR_STACKED):
            plot.overlap = 100
        if labels:
            plot.has_data_labels = True
            dl = plot.data_labels
            dl.number_format = number_format
            dl.number_format_is_linked = False
            dl.font.size = Pt(font)
            dl.font.color.rgb = rgb(BLACK)
            if kind in (XL_CHART_TYPE.COLUMN_CLUSTERED, XL_CHART_TYPE.BAR_CLUSTERED):
                dl.position = XL_LABEL_POSITION.OUTSIDE_END
        va = ch.value_axis
        va.has_major_gridlines = False
        va.visible = False
        ca = ch.category_axis
        ca.format.line.color.rgb = rgb(MIDGREY)
        ca.tick_labels.font.size = Pt(font)
        ca.has_major_gridlines = False
        allv = [v for _, vals in series for v in vals if v is not None]
        if allv and min(allv) < 0:
            ca.tick_label_position = XL_TICK_LABEL_POSITION.LOW   # keep category names clear of negative bars
            for ser in ch.series:
                ser.invert_if_negative = False                    # PowerPoint draws negative bars hollow otherwise
            if kind not in (XL_CHART_TYPE.COLUMN_STACKED, XL_CHART_TYPE.BAR_STACKED) and not is_line:
                span = max(max(allv), 0) - min(allv)              # headroom so outside-end labels clear the axis text
                va.minimum_scale = min(allv) - 0.25 * span
                if max(allv) > 0:
                    va.maximum_scale = max(allv) + 0.15 * span
        return ch

    def column(self, s, x, y, w, h, categories, series, **kw):
        self._tag(s, "column")
        return self._chart(s, x, y, w, h, XL_CHART_TYPE.COLUMN_CLUSTERED, categories, series, **kw)

    def bar(self, s, x, y, w, h, categories, series, **kw):
        self._tag(s, "bar")
        ch = self._chart(s, x, y, w, h, XL_CHART_TYPE.BAR_CLUSTERED, categories, series, **kw)
        ch.category_axis.reverse_order = True
        return ch

    def stacked(self, s, x, y, w, h, categories, series, **kw):
        self._tag(s, "stacked")
        return self._chart(s, x, y, w, h, XL_CHART_TYPE.COLUMN_STACKED, categories, series, **kw)

    def line(self, s, x, y, w, h, categories, series, **kw):
        self._tag(s, "line")
        return self._chart(s, x, y, w, h, XL_CHART_TYPE.LINE_MARKERS, categories, series, **kw)

    def football_field(self, s, x, y, w, h, rows, fmt='#,##0', highlight=None, label_fmt=None, axis=True,
                       vmin=None, vmax=None):
        """rows = [(label, low, high)]; horizontal floating bars (valuation / cap-rate ranges).
        highlight = row index shown in gold (the target); label_fmt = e.g. '{:.2f}–{:.2f}%' writes each range at the
        end of its bar (then the value axis can be hidden with axis=False). vmin / vmax set the axis so
        narrow ranges get wide enough bars for their labels."""
        self._tag(s, "football_field")
        cats = [r[0] for r in rows]
        ch = self._chart(s, x, y, w, h, XL_CHART_TYPE.BAR_STACKED, cats,
                         [("low", [r[1] for r in rows]), ("range", [r[2] - r[1] for r in rows])],
                         number_format=fmt, legend=False, gap=50)
        ch.category_axis.reverse_order = True
        ch.series[0].format.fill.background()
        ch.plots[0].has_data_labels = False
        rng = ch.series[1]
        rng.format.fill.solid()
        rng.format.fill.fore_color.rgb = rgb(NAVY)
        if highlight is not None:
            pt = rng.points[highlight]
            pt.format.fill.solid()
            pt.format.fill.fore_color.rgb = rgb(GOLD)
        if label_fmt:
            for k, r in enumerate(rows):
                dl = rng.points[k].data_label
                dl.position = XL_LABEL_POSITION.CENTER
                tf = dl.text_frame
                tf.text = label_fmt.format(r[1], r[2])
                for p in tf.paragraphs:
                    for run in p.runs:
                        run.font.size, run.font.bold, run.font.name = Pt(F_BODY), True, FONT
                        run.font.color.rgb = rgb(WHITE)
        if vmin is not None:
            ch.value_axis.minimum_scale = vmin
        if vmax is not None:
            ch.value_axis.maximum_scale = vmax
        ch.value_axis.visible = axis
        ch.value_axis.tick_labels.number_format = fmt
        ch.value_axis.tick_labels.number_format_is_linked = False
        ch.value_axis.tick_labels.font.size = Pt(F_BODY)
        return ch

    # ---------- infographic library (PwC originals, restyled; built by infographic_library.py) ----------
    _libs = {}

    def infographic(self, s, no, box=None, library=None, highlight=None):
        """Copy library infographic `no` (numbers: assets/infographic_index.json or output/_Deal Desk Toolkit/Infographic Library –
        index.pdf) into slide s: the original objects (freeforms, groups, tables, charts), scaled into box
        (x, y, w, h in inches; default the whole body). Returns the new shapes; edit their text in place.
        highlight = names of shapes (as in the library, e.g. "IG Oval 12") to fill gold (one per slide)."""
        self._tag(s, f"infographic {no}")      # different library numbers = different layouts
        src = self._libslide(no, library)
        shapes = [sh for sh in src.shapes if sh.name.startswith("IG ")]
        if not shapes:
            raise ValueError(f"library slide {no} has no infographic shapes")
        out, _ = self._paste(s, src, shapes, box)
        self._highlight(out, highlight)
        return out

    def _libslide(self, no, library=None):
        path = library or LIBRARY
        if path not in Deck._libs:
            Deck._libs[path] = Presentation(path)
        return Deck._libs[path].slides[no - 1]

    def _paste(self, s, src, shapes, box):
        """Deep-copy library shapes into slide s, scaled (aspect kept) and centred in box. -> (elements, scale)."""
        import copy
        x0 = min(sh.left for sh in shapes)
        y0 = min(sh.top for sh in shapes)
        bw_ = max(sh.left + sh.width for sh in shapes) - x0
        bh_ = max(sh.top + sh.height for sh in shapes) - y0
        bx, by, bw, bh = box or self.body
        f = min(Inches(bw) / bw_, Inches(bh) / bh_)
        ox = Inches(bx) + (Inches(bw) - bw_ * f) / 2
        oy = Inches(by) + (Inches(bh) - bh_ * f) / 2
        tree, out = s.shapes._spTree, []
        for sh in shapes:
            el = copy.deepcopy(sh._element)
            self._relink(el, src.part, s.part)
            xfrm = el.find(qn("p:xfrm"))
            if xfrm is None:
                xfrm = next((e for e in el if e.tag in (qn("p:spPr"), qn("p:grpSpPr"))), el).find(qn("a:xfrm"))
            off, ext = xfrm.find(qn("a:off")), xfrm.find(qn("a:ext"))
            off.set("x", str(int(ox + (int(off.get("x")) - x0) * f)))
            off.set("y", str(int(oy + (int(off.get("y")) - y0) * f)))
            ext.set("cx", str(int(int(ext.get("cx")) * f)))
            ext.set("cy", str(int(int(ext.get("cy")) * f)))
            for tag, attr in (("a:gridCol", "w"), ("a:tr", "h")):     # tables: scale the grid as well
                for e in el.iter(qn(tag)):
                    e.set(attr, str(int(int(e.get(attr)) * f)))
            tree.append(el)
            out.append(el)
        return out, f

    @staticmethod
    def _highlight(out, highlight):
        if highlight:
            for el in out:
                for e in el.iter():
                    if e.tag == qn("p:cNvPr") and e.get("name") in highlight:
                        for clr in e.getparent().getparent().iter(qn("a:srgbClr")):
                            if clr.getparent().tag == qn("a:solidFill") and clr.getparent().getparent().tag == qn("p:spPr"):
                                clr.set("val", GOLD)
        return out

    # ---------- layout library (assets/layout_library.json; built by layout_tag.py) ----------
    _tags = None

    def bank(self, s, bid, box=None, data=None):
        """Draw bank design `bid` ("bk13", see bank_layouts.py / layout_library.json) in box (default: the slide body)
        with data = the keyword arguments of that design (copy the shape from bank_samples.SAMPLE[bid])."""
        import bank_layouts
        fn = getattr(bank_layouts, bid, None)
        if fn is None:
            raise ValueError(f"{bid} is not a bank design (bk01-bk58; see bank_specs.SPECS)")
        x, y, w, h = box or self.body
        self._tag(s, f"layout {bid}")
        return fn(self, s, x, y, w, h, **(data or {}))

    def layout(self, s, lid, variant=1, box=None, data=None, drop=(), highlight=None, library=None):
        """Place one variant (sub-diagram) of library layout `lid` ("ig045") in box and fill its text slots.
        data: role lists in slot order, {"head": [...], "text": [...], "num": [...]}, and/or single slots by name,
        {"head2": "...", "v1.text3": "..."} (slot names: layout_library.json "variants" -> "slots"). A "\\n" in a value
        starts a new paragraph. Unfilled slots are emptied (bare text boxes deleted), so no placeholder text is left.
        drop = slot names whose whole shape should go (an optional arm, a spare segment). Text that would overflow its
        shape steps down 12 -> 10 pt, then is reported as a LAYOUT WARNING by save().
        Coded components and page recipes (ids without "ig") are called directly: see the record's "call"."""
        import layout_tag
        if not lid.startswith("ig"):
            raise ValueError(f"{lid} is a coded component / page recipe; use its call in assets/layout_library.json")
        no = int(lid[2:])
        if Deck._tags is None:
            Deck._tags = layout_tag._load(layout_tag.TAGS, {}).get("ig", {})
        src = self._libslide(no, library)
        vs = layout_tag.variants(src, Deck._tags.get(lid, {}))
        match = [v for v in vs if v[0] == variant]
        if not match:
            raise ValueError(f"{lid} has variants 1-{len(vs)}, not {variant}")
        _, shapes, _, slots = match[0]
        self._tag(s, f"layout {lid}.{variant}")
        out, f = self._paste(s, src, shapes, box)
        self._highlight(out, highlight)
        # copied slot shapes, by slot name
        els = {}
        for el in out:
            for e in el.iter(qn("p:cNvPr")):
                if e.get("name", "").startswith("IG slot:"):
                    els[e.get("name")[8:]] = e.getparent().getparent()
        k = variant
        want = {}
        for key, val in (data or {}).items():
            if isinstance(val, (list, tuple)):
                want.update({f"v{k}.{key}{i}": v for i, v in enumerate(val, 1) if v is not None})
            else:
                want[key if key.startswith("v") and "." in key else f"v{k}.{key}"] = val
        for name in want:
            if name not in els:
                self.overflow.append(f"slide {self.n}: {lid} v{k} has no slot {name} "
                                     f"(slots: {', '.join(n for n, _, _ in slots)})")
        top = {id(e) for e in out}
        for name in drop:
            name = name if "." in name else f"v{k}.{name}"
            el = els.get(name)
            while el is not None and id(el) not in top:   # climb to the top-level shape
                el = el.getparent()
            if el is not None and el.getparent() is not None:
                el.getparent().remove(el)
        for name, sh, b in slots:
            sp = els.get(name)
            if sp is None or sp.getparent() is None:
                continue
            if name in want:
                w_in, h_in = (b[2] - b[0]) * f, (b[3] - b[1]) * f
                self._fill_slot(sp, str(want[name]), w_in, h_in, f"slide {self.n}: {lid} {name}")
            elif id(sp) in top and not layout_tag._filled(sh):
                sp.getparent().remove(sp)                   # spare annotation text box
            else:
                self._fill_slot(sp, "", 1, 1, "")
        return out

    def _fill_slot(self, sp, text, w_in, h_in, where):
        """Replace a copied shape's text, keeping its first run's formatting; shrink to fit, else note an overflow."""
        import copy
        from lxml import etree
        tb = sp.find(qn("p:txBody"))
        if tb is None:
            return
        paras = tb.findall(qn("a:p"))
        p0 = paras[0]
        ppr = p0.find(qn("a:pPr"))
        rpr = next((r.find(qn("a:rPr")) for r in p0.iter(qn("a:r")) if r.find(qn("a:rPr")) is not None), None)
        orig = "\n".join("".join(t.text or "" for t in p.iter(qn("a:t"))) for p in paras)
        for p in paras:
            tb.remove(p)
        size = int(rpr.get("sz")) / 100 if rpr is not None and rpr.get("sz") else F_BODY
        bpr = tb.find(qn("a:bodyPr"))
        nowrap = bpr is not None and bpr.get("wrap") == "none"
        ins = (int(bpr.get("lIns", 91440)) + int(bpr.get("rIns", 91440))) / 914400 if bpr is not None else 0.2
        # capacity = what the shape is drawn to hold (its height) or what the original placeholder held, if more
        cap = max(self._lines(orig, size, w_in - ins, nowrap) or 1, int((h_in * 1.1 + 0.05) / (size * 1.2 / 72)))

        def fits(z):
            n = self._lines(text, z, w_in - ins, nowrap)
            return n is not None and n * z <= cap * size
        if text and size > 10:   # step down (to 12, then 10) until the text fits the shape
            for cand in [size] + [z for z in (12, 10) if z < size]:
                size = cand
                if fits(cand):
                    break
        if text and not fits(size):
            self.overflow.append(f"{where}: text may overflow ({len(text)} chars in {w_in:.1f} x {h_in:.1f} in)")
        for line in text.split("\n"):
            p = etree.SubElement(tb, qn("a:p"))
            if ppr is not None:
                p.append(copy.deepcopy(ppr))
            if line:
                r = etree.SubElement(p, qn("a:r"))
                rp = copy.deepcopy(rpr) if rpr is not None else etree.Element(qn("a:rPr"))
                rp.set("sz", str(int(size * 100)))
                r.append(rp)
                etree.SubElement(r, qn("a:t")).text = line

    @staticmethod
    def _lines(text, size, usable, nowrap=False):
        """Rough Arial word-wrap line count (average glyph 0.5 em); None when one word is wider than the shape."""
        if nowrap:
            return len(text.split("\n"))
        cw, usable, lines = size * 0.5 / 72, max(usable, 0.1), 0
        for para in text.split("\n"):
            n, cur = 1, 0.0
            for word in para.split():
                ww = len(word) * cw
                if ww > usable * 1.15:
                    return None
                if cur and cur + cw + ww > usable:
                    n, cur = n + 1, ww
                else:
                    cur += (cw if cur else 0) + ww
            lines += n
        return lines

    @staticmethod
    def _relink(el, src_part, dst_part):
        """Re-point r:embed / r:id / r:link relationships of copied XML at parts in the destination package
        (pictures, charts with their embedded workbook, hyperlinks)."""
        from io import BytesIO
        from pptx.opc.package import Part
        from pptx.opc.packuri import PackURI
        from pptx.parts.chart import ChartPart
        import re as _re
        rns = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
        pkg = dst_part.package

        def clone(part, parent):
            tmpl = _re.sub(r"\d+(\.\w+)$", r"%d\1", str(part.partname))
            name = pkg.next_partname(tmpl)
            if isinstance(part, ChartPart):
                new = ChartPart.load(name, part.content_type, pkg, part.blob)
            else:
                new = Part.load(PackURI(name), part.content_type, pkg, part.blob)
            for rid, rel in list(part.rels.items()):
                if rel.is_external:
                    new_rid = new.relate_to(rel.target_ref, rel.reltype, is_external=True)
                else:
                    new_rid = new.relate_to(clone(rel.target_part, new), rel.reltype)
                if hasattr(new, "_element") and new_rid != rid:
                    for e in new._element.iter():
                        for a, v in e.attrib.items():
                            if a.startswith(rns) and v == rid:
                                e.set(a, new_rid)
            return new

        for e in el.iter():
            for a, rid in list(e.attrib.items()):
                if not a.startswith(rns) or rid not in src_part.rels:
                    continue
                rel = src_part.rels[rid]
                if rel.is_external:
                    e.set(a, dst_part.relate_to(rel.target_ref, rel.reltype, is_external=True))
                elif rel.reltype.endswith("/image"):
                    _, new_rid = dst_part.get_or_add_image_part(BytesIO(rel.target_part.blob))
                    e.set(a, new_rid)
                elif rel.reltype.endswith("/slide"):
                    del e.attrib[a]                     # link to another library slide: drop
                else:
                    e.set(a, dst_part.relate_to(clone(rel.target_part, dst_part), rel.reltype))

    def footer(self, s, sources=None, notes=None):
        """Two lines, 8pt italic: 'Sources: ...' then 'Notes: ...'."""
        self._tag(s, "footer")
        imgs = self.credits.get(s.slide_id)
        if imgs:
            sources = (f"{sources}; " if sources else "") + "Images: " + "; ".join(dict.fromkeys(imgs))
        lines = [ln for ln in (f"Sources: {sources}" if sources else None, f"Notes: {notes}" if notes else None) if ln]
        if lines:
            self._text(s, L, Y_SRC, W - L - R_, 0.36, lines, size=F_SRC, color=DGREY, italic=True)

    # ---------- checks ----------
    def lint(self):
        """Layout: content past the footer line or right margin. AI tells: see references/slide-layouts.md.
        Table rows can still grow when text wraps, so always render and look as well."""
        issues = []
        for i, s in enumerate(self.prs.slides, 1):
            if s.slide_id not in self.content:
                continue
            for shp in s.shapes:
                if shp.top is None or shp.height is None:
                    continue
                top, bottom = shp.top / 914400, (shp.top + shp.height) / 914400
                right = (shp.left + shp.width) / 914400
                if top >= Y_SRC - 0.03:  # sources, contents bar, page number
                    continue
                if bottom > BOTTOM + 0.05 or right > W - R_ + 0.05:
                    issues.append(f"slide {i}: '{shp.name}' ends at {bottom:.2f}in down / {right:.2f}in across")
        issues += self.overflow
        for msg in issues:
            print("LAYOUT WARNING:", msg)
        tells = self.tells()
        for msg in tells:
            print("AI TELL:", msg)
        sparse = self.sparse()
        for msg in sparse:
            print("SPARSE:", msg)
        thin = self.thin()
        for msg in thin:
            print("THIN ARGUMENT:", msg)
        return issues + tells + sparse + thin

    def thin(self):
        """Argument blocks must explain, not list (lessons #35; Benedict's critique of the SG DC deck, 27 Sep 2026):
        a thesis pillar needs a bold claim + 2-3 sentences (>= ARG_MIN_THESIS words); each risk and mitigant cell a
        bold title + 1-2 sentences (>= ARG_MIN_CELL words). Fact-list tabs under a thesis-type header are flagged."""
        out = []
        idx = {s.slide_id: i for i, s in enumerate(self.prs.slides, 1)}
        for s in self.prs.slides:
            sid = s.slide_id
            if sid not in self.args:
                continue
            i = idx[sid]
            heads = [shp.text_frame.text for shp in s.shapes if shp.has_text_frame and self._solid(shp) == NAVY]
            thesis_page = any(ARG_HEADS.search(hd) for hd in heads)
            for kind, label, words in self.args[sid]:
                if kind == "thesis" and words < ARG_MIN_THESIS:
                    out.append(f"slide {i}: thesis pillar '{label}' has {words} words; give a bold claim plus "
                               f"evidence -> so what -> implication ({ARG_MIN_THESIS}+ words)")
                elif kind == "data_tabs" and thesis_page:
                    out.append(f"slide {i}: '{label}' is a list of facts under a thesis header; pass (claim, text) "
                               "so the tab argues why it matters")
                elif kind in ("risk", "mitigant") and words < ARG_MIN_CELL:
                    out.append(f"slide {i}: {kind} '{label[:40]}' has {words} words; give a bold title plus 1-2 "
                               f"sentences ({ARG_MIN_CELL}+ words: the impact / how it works and what risk is left)")
        return out

    def sparse(self):
        """Density standard (lessons #32), set from 400 pages of real bank decks: every content slide has an exhibit,
        at least MIN_BODY_WORDS words in the body and no empty band taller than MAX_EMPTY_BAND. Shape boxes can be
        taller than their text, so also run `office.py density` on the saved file (pixel check)."""
        out = []
        idx = {s.slide_id: i for i, s in enumerate(self.prs.slides, 1)}
        for s in self.prs.slides:
            if s.slide_id not in self.content:
                continue
            i = idx[s.slide_id]
            comps = {c.split()[0] for c in self.used.get(s.slide_id, [])}
            words, spans = 0, []
            for shp in s.shapes:
                if shp.top is None or shp.height is None:
                    continue
                top, bot = shp.top / 914400, (shp.top + shp.height) / 914400
                if top < TOP - 0.1 or top >= Y_SRC - 0.03:
                    continue
                spans.append((max(top, TOP), min(bot, BOTTOM)))
                if shp.shape_type == MSO_SHAPE_TYPE.PICTURE and shp.width < 914400 * 2.5:
                    words += 1   # a logo names a company, like a word (Qatalyst's logo wall has no other text)
                if shp.has_text_frame:
                    words += len(shp.text_frame.text.split())
                if shp.has_table:
                    words += sum(len(c.text_frame.text.split()) for r in shp.table.rows for c in r.cells)
                if shp.has_chart:
                    try:
                        words += sum(len(str(c).split()) for c in shp.chart.plots[0].categories)
                    except (IndexError, AttributeError):
                        pass
            if not comps & EXHIBITS and words < TEXT_PAGE_WORDS:   # a full-width text page (GS p3) needs no exhibit
                out.append(f"slide {i}: no exhibit (chart, table, photo, logo grid, timeline, infographic...); "
                           f"pair the commentary with one, or make it a full text page ({TEXT_PAGE_WORDS}+ words)")
            if words < MIN_BODY_WORDS:
                out.append(f"slide {i}: {words} words in the body (bank pages carry {MIN_BODY_WORDS}+); add commentary "
                           "with numbers beside the exhibit")
            spans.sort()
            edge, gap_at, gap = TOP, TOP, 0.0
            for a, b in spans + [(BOTTOM, BOTTOM)]:
                if a - edge > gap:
                    gap, gap_at = a - edge, edge
                edge = max(edge, b)
            if gap > MAX_EMPTY_BAND:
                out.append(f"slide {i}: empty band {gap:.1f}in tall from {gap_at:.1f}in down; stretch the blocks to the "
                           "bottom of the body or add an exhibit")
        return out

    @staticmethod
    def _solid(shp):
        try:
            if shp.shape_type != MSO_SHAPE_TYPE.AUTO_SHAPE or shp.auto_shape_type != MSO_SHAPE.RECTANGLE:
                return None
            if shp.fill.type != 1:  # MSO_FILL.SOLID
                return None
            return str(shp.fill.fore_color.rgb)
        except Exception:
            return None

    def tells(self):
        """Patterns that make a deck look Claude-made (Benedict's critique, 26 Sep 2026)."""
        out = []
        slides = list(self.prs.slides)
        idx = {s.slide_id: i for i, s in enumerate(slides, 1)}
        # 0. stacked filled bands: a filled header bar with a filled table header row right under it (lessons #34;
        #    real decks use one filled band per block: BofA Taro p11, Citi Chindata p5, Evercore Diversey p50)
        for i, s in enumerate(slides, 1):
            if s.slide_id not in self.content:
                continue
            bars = [(shp.left / 914400, (shp.top + shp.height) / 914400, shp.width / 914400) for shp in s.shapes
                    if self._solid(shp) == NAVY and shp.height / 914400 <= 0.4]
            for shp in s.shapes:
                if not shp.has_table or shp.name.startswith("IG "):
                    continue
                def _navy(c):
                    try:
                        return c.fill.type == 1 and str(c.fill.fore_color.rgb) == NAVY
                    except Exception:
                        return False
                row0 = [shp.table.cell(0, j) for j in range(len(shp.table.columns))]
                head_fill = all(_navy(c) for c in row0)   # whole top row filled (side_tabs' label column is not)
                tx, ty, tw = shp.left / 914400, shp.top / 914400, shp.width / 914400
                if head_fill and any(0 <= ty - bb < 0.9 and bx < tx + tw - 0.05 and tx < bx + bw - 0.05
                                     for bx, bb, bw in bars):
                    out.append(f"slide {i}: filled header bar with a filled table header right under it; use "
                               "table(header_style='rule') (bold black headers, navy rule) as real bank decks do")
        # 1. accent-bar card: a thin solid strip on the left or top edge of a filled box (any colour)
        for i, s in enumerate(slides, 1):
            rects = []
            for shp in s.shapes:
                if shp.name.startswith("IG "):   # library infographics: PwC's originals, checked when built
                    continue
                col = self._solid(shp)
                if col:
                    rects.append((shp.left / 914400, shp.top / 914400, shp.width / 914400, shp.height / 914400, col))
            for (ax, ay, aw, ah, ac) in rects:
                for (bx, by, bw, bh, bc) in rects:
                    if bc == ac or (bx, by, bw, bh) == (ax, ay, aw, ah):
                        continue
                    side = bw <= 0.15 and aw > 3 * bw and abs(bx - ax) < 0.05 and abs(by - ay) < 0.05 and bh >= 0.6 * ah
                    top = bh <= 0.15 and ah > 3 * bh and abs(by - ay) < 0.05 and abs(bx - ax) < 0.05 and bw >= 0.6 * aw
                    if side or top:
                        out.append(f"slide {i}: accent-bar card (thin strip on the {'left' if side else 'top'} of a "
                                   f"filled box at {ax:.1f}in, {ay:.1f}in); use stat_icons / stat_strip / takeaway")
        # 2. same body layout as the slide before
        prev = None
        for sid in self.content:
            sig = tuple(sorted(c for c in self.used.get(sid, []) if c not in CHROME))
            if sig and sig == prev:
                out.append(f"slide {idx.get(sid)}: same body layout as the slide before ({', '.join(sig)})")
            prev = sig
        # 3. no visual layout anywhere in a deck of 3+ content slides
        comps = {c.split()[0] for sid in self.content for c in self.used.get(sid, [])}
        if len(self.content) > 2 and not comps & VISUAL:
            out.append("deck: only charts / tables / bullets; use at least one visual layout "
                       "(icons, rings, pills, side tabs, chevrons, timeline...)")
        # 5. shadows / glows (theme effect styles) on any shape
        for i, s in enumerate(slides, 1):
            for shp in s.shapes:
                er = shp._element.find(".//" + qn("a:effectRef"))
                if er is not None and er.get("idx", "0") != "0":
                    out.append(f"slide {i}: '{shp.name}' carries a theme shadow; draw it with _line / _shape")
        # 6. font sizes: only 20 / 16 / 12 / 10 (+ 8 for sources and page number)
        for i, s in enumerate(slides, 1):
            if s.slide_id not in self.content:
                continue
            bad = set()
            for shp in s.shapes:
                frames = [shp.text_frame] if shp.has_text_frame else []
                if shp.has_table:
                    frames += [c.text_frame for r in shp.table.rows for c in r.cells]
                for tf in frames:
                    for p in tf.paragraphs:
                        for r in p.runs:
                            if r.font.size is not None and round(r.font.size.pt, 1) not in SIZES:
                                bad.add(round(r.font.size.pt, 1))
            if bad:
                out.append(f"slide {i}: font sizes {sorted(bad)} not allowed (use 20 / 16 / 12 / 10, sources 8)")
        # 9. tables: every cell one typeface and a set size, incl. blank cells (else the row grows to 18pt)
        for i, s in enumerate(slides, 1):
            for shp in s.shapes:
                if not shp.has_table or s.slide_id not in self.content or shp.name.startswith("IG "):
                    continue
                faces, blank = set(), 0
                for r_ in shp.table.rows:
                    for c in r_.cells:
                        for p in c.text_frame.paragraphs:
                            faces |= {r.font.name for r in p.runs}
                            if not p.runs:
                                end = p._p.find(qn("a:endParaRPr"))
                                blank += end is None or end.get("sz") is None
                if blank or len(faces) > 1:
                    out.append(f"slide {i}: table '{shp.name}' has {blank} blank cell(s) at the default 18pt"
                               f"{' and fonts ' + str(sorted(f or '?' for f in faces)) if len(faces) > 1 else ''};"
                               " build tables with table() / fin_table()")
        # 10. units in a table's column headers ("$m", "% of revenue"): banks put units once, in the block header
        for i, s in enumerate(slides, 1):
            if s.slide_id not in self.content:
                continue
            for shp in s.shapes:
                if shp.has_table and not shp.name.startswith("Side tabs"):   # side tabs have no header row
                    heads = [c.text_frame.text for c in shp.table.rows[0].cells]
                    bad = [hd for hd in heads if any(u in hd for u in ("$m", "% of", "($", "$'0", "$bn"))]
                    if bad:
                        out.append(f"slide {i}: table headers {bad} carry units; put them once in the block header "
                                   "('P&L summary ($m)') and use fin_table()")
        # 7. header / subheader: one line, one sentence
        for sid in self.content:
            for kind, txt, cap in zip(("header", "subheader"), self.heads.get(sid, ("", "")), (70, 95)):
                if txt and (len(txt) > cap or txt.rstrip(". ").count(". ")):
                    out.append(f"slide {idx.get(sid)}: {kind} is longer than one line / one sentence: '{txt[:50]}...'")
        # 8. alignment: block header bars on one slide either share a top or sit clearly apart
        for sid in self.content:
            ys = sorted(set(self.hdr_y.get(sid, [])))
            for a, b in zip(ys, ys[1:]):
                if b - a < 1.0:
                    out.append(f"slide {idx.get(sid)}: block headers at {a:.2f}in and {b:.2f}in are not aligned; "
                               "put blocks in the same row at the same height")
        # 4. bullet walls
        for sid in self.content:
            nb = self.used.get(sid, []).count("bullets")
            if nb > 2:
                out.append(f"slide {idx.get(sid)}: {nb} bullet blocks; turn some into a table, pills, steps or pros/cons")
        return out

    def save(self, path):
        self.lint()
        self.prs.save(path)
        return path
