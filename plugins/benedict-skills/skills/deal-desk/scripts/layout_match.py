"""Research -> slide mapping: shortlist layouts for each block of each slide (references/deck-pipeline.md).

  python layout_match.py match topics.json [k]   # k (default 5) candidates per block -> <stem>_match/ (PNG sheets)
  python layout_match.py plan  topics.json       # the slide plan table from the picks + rule checks

topics.json is written by Claude from the research (chunk step). One topic = one slide; one block = one exhibit:
{"deck": "Singapore Data Centres", "topics": [
  {"slide": 1, "section": "market", "message": "Asia's premium data centre hub, over 95% occupancy",
   "blocks": [
     {"what": "Key market metrics", "data_type": "kpi_set", "about": "live MW, occupancy, rent, power share",
      "content": ["821MW live capacity", ">95% occupancy", ...],     # or give "items", "words", "numbers" directly
      "pick": "stat_icons", "alts": ["stat_strip", "table"], "why": "5 headline numbers, each with an icon"}]}]}
The first block is the slide's lead exhibit. "pick" / "alts" / "why" are added in the select step.
"""
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")
LIB_JSON = os.path.join(ASSETS, "layout_library.json")
PAGES_JSON = os.path.join(ASSETS, "real_deck_pages.json")

# how well a layout of one data type carries content of another (1 = same type)
NEAR = {
    "kpi_set": {"icons": .6, "composition": .4, "comparison": .3},
    "time_series": {"comparison": .3, "process": .2},
    "process": {"cycle": .5, "time_series": .4, "list": .3},
    "cycle": {"process": .5, "relationship": .4},
    "list": {"text": .5, "comparison": .3, "relationship": .3, "process": .2},
    "text": {"list": .6},
    "comparison": {"matrix": .5, "list": .3, "kpi_set": .2},
    "matrix": {"comparison": .5},
    "composition": {"kpi_set": .4, "hierarchy": .3},
    "hierarchy": {"composition": .3, "relationship": .3},
    "relationship": {"list": .3, "cycle": .3, "hierarchy": .3},
    "range": {"comparison": .3},
    "bridge": {"composition": .3, "time_series": .2},
    "geography": {"comparison": .2},
    "icons": {"kpi_set": .5},
}
# layouts that cannot be drawn without numbers
NUMERIC = {"fin_chart", "fin_table", "column", "bar", "stacked", "line", "football_field", "heatmap", "stat_icons",
           "stat_strip", "stat_rings", "hero_number", "pictogram", "tam_sam_som"}
# rule 3: at least one of these per deck
VISUAL = {"stat_icons", "stat_rings", "pill_rows", "side_tabs", "chevrons", "timeline", "hub_spoke", "harvey",
          "pictogram", "hero_number", "numbered_steps", "tam_sam_som", "logo_row", "map_pins"}
STOP = set("a an the and or of to in on for with by at from as is are be per each one two three four into than vs use "
           "not no more less over under it its this that their your which who what how when where only".split())
NUM_RE = re.compile(r"(?<![A-Za-z])\d")       # a number, not the 2 in "DC-CFA2"
DATE_RE = re.compile(r"\b(19|20)\d\d\b|\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\b|\b[1-4]h\b|\bq[1-4]\b",
                     re.I)
CHARTS = {"bar", "column", "stacked", "line", "fin_chart", "football_field"}


def _load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def toks(text):
    out = set()
    for w in re.findall(r"[a-z][a-z/&-]+", (text or "").lower()):
        for p in re.split(r"[/&-]", w):
            if len(p) < 3 or p in STOP:
                continue
            for suf in ("ing", "es", "s", "ed"):
                if p.endswith(suf) and len(p) - len(suf) >= 4:
                    p = p[:-len(suf)]
                    break
            out.add(p)
    return out


def _sim(a, b):
    return len(a & b) / math.sqrt(len(a) * len(b)) if a and b else 0.0


def shape(block):
    """Content shape of a block: items, words, numbers (from 'content' when given, else the stated values)."""
    c = block.get("content")
    if isinstance(c, list):
        items, text = len(c), " ".join(map(str, c))
    else:
        items, text = None, c or ""
    lines = [str(x) for x in c] if isinstance(c, list) else []
    num_share = sum(bool(NUM_RE.search(DATE_RE.sub("", x))) for x in lines) / len(lines) if lines else None
    dated = bool(lines) and sum(bool(DATE_RE.search(x)) for x in lines) / len(lines) >= 0.6
    sh = {"data_type": block.get("data_type", ""),
          "items": block.get("items", items if items is not None else 1),
          "words": block.get("words", len(text.split())),
          "numbers": block.get("numbers", bool(NUM_RE.search(DATE_RE.sub("", text)))),   # dates alone are not data
          "query": toks(" ".join([block.get("what", ""), block.get("about", "")]))}
    # a short "label + number" per item is a data series: chart it rather than tabulate it
    # ("unit" = the one measure every value shares, e.g. "MW"; mixed measures belong in a table)
    sh["series"] = bool(block.get("unit") and sh["numbers"] and sh["data_type"] in ("comparison", "time_series", "composition", "range")
                        and sh["items"] >= 3 and sh["words"] <= 4 * sh["items"]
                        and (num_share is None or num_share >= 0.8) and not dated)
    sh["dated"] = dated               # events with dates: a timeline, not a chart
    sh["names"] = bool(lines) and not sh["numbers"] and len(lines) >= 3 and sh["words"] <= 2.5 * len(lines)
    return sh


def _capacity(r, n):
    """Rough word capacity of a layout holding n items (None when unknown)."""
    if r["id"] == "table":
        return None                     # rows can run as wide as the page
    if r.get("words"):
        return max(n, r["items"][0]) * sum(r["words"].values())
    if r.get("variants"):
        chars = max(sum(int(v.split("|")[-1]) for v in var["slots"].values() if v.split("|")[-1].strip().isdigit())
                    for var in r["variants"])
        return chars / 6 or None
    return None


class Matcher:
    def __init__(self):
        lib = _load(LIB_JSON)
        self.lib = {r["id"]: r for r in lib["layouts"]}
        pg = _load(PAGES_JSON) if os.path.exists(PAGES_JSON) else {"pages": [], "root": ""}
        self.root, self.pages = pg.get("root", ""), pg["pages"]
        # a bank design (bk##) counts the real pages it was drawn from as its own
        drawn = defaultdict(list)
        for r in self.lib.values():
            for pid in r.get("examples", []):
                drawn[pid].append(r["id"])
        self.uses = {p["id"]: drawn[p["id"]] + list(p["layouts"]) for p in self.pages}
        self.by_sec = defaultdict(Counter)      # section -> layout -> real pages
        for p in self.pages:
            for lid in self.uses[p["id"]]:
                self.by_sec[p["section"]][lid] += 1
        self.top_all = max((r.get("real_pages", 0) for r in self.lib.values()), default=1) or 1

    def score(self, r, sh, section):
        """(score, reasons) for one layout record against one block's content shape."""
        why = []
        dt = sh["data_type"]
        aff = 1.0 if r.get("data_type") == dt else NEAR.get(dt, {}).get(r.get("data_type"), 0)
        s = 3 * aff
        if aff == 1:
            why.append(dt)
        if section in r.get("sections", []) or "any" in r.get("sections", []):
            s += 1
        n = sh["items"]
        lo, hi = (r.get("items") or [1, 99])[:2]
        if lo <= n <= hi:
            s += 1
        else:
            s -= min(2, 0.5 * (lo - n if n < lo else n - hi))
            why.append(f"{n} items vs {lo}-{hi}")
        if not sh["numbers"] and (r["id"] in NUMERIC or (r.get("source") == "bank" and r.get("numbers"))):
            s -= 2.5
            why.append("needs numbers")
        elif not sh["numbers"] and r.get("numbers"):
            s -= 0.5
        elif sh["numbers"] and not r.get("numbers"):
            s -= 0.5
        cap = _capacity(r, n)
        if cap and sh["words"] > 1.6 * cap:
            s -= 1
            why.append(f"{sh['words']} words > ~{cap:.0f}")
        elif cap and cap > 40 and r["id"] not in NUMERIC and sh["words"] < 0.2 * cap:
            s -= 0.5
            why.append("too little text")
        if sh["series"] and r["id"] in CHARTS:
            s += 1.5
            why.append("data series")
        if sh["names"] and r["id"] == "logo_row":
            s += 1.5
            why.append("names only")
        elif sh["series"] and r["id"] == "table":
            s -= 0.5
        if sh["dated"] and r["id"] == "timeline":
            s += 1.5
            why.append("dated events")
        elif sh["dated"] and r["id"] in CHARTS:
            s -= 1
        fit =_sim(sh["query"], toks(r.get("use_when", "") + " " + r.get("name", "")))
        dont = _sim(sh["query"], toks(re.sub(r"\(use [^)]*\)", "", r.get("dont_use_when", ""))))
        s += 2.5 * fit - 1.0 * dont
        hit = sh["query"] & toks(r.get("use_when", ""))
        if hit:
            why.append("fits: " + ", ".join(sorted(hit)[:3]))
        sec_max = max(self.by_sec[section].values(), default=0)
        sec_n = self.by_sec[section][r["id"]]
        if sec_max:
            s += 1.5 * math.log1p(sec_n) / math.log1p(sec_max)
        s += 0.5 * math.log1p(r.get("real_pages", 0)) / math.log1p(self.top_all)
        if r.get("real_pages"):
            why.append(f"{r['real_pages']} real pages ({sec_n} {section})")
        return round(s, 2), why

    def exemplar(self, lid, section):
        """The real bank page closest to this use: same section first, layout as lead, fullest."""
        hits = [p for p in self.pages if lid in self.uses[p["id"]]]
        if not hits:
            return None
        hits.sort(key=lambda p: (p["section"] != section, self.uses[p["id"]].index(lid) > 0, -p["fill"]))
        p = hits[0]
        return {"bank": p["bank"], "deck": p["deck"], "page": p["page"], "note": p["note"],
                "thumb": os.path.join(self.root, p["thumb"]) if self.root else p["thumb"]}

    def recipe(self, topic, tops):
        """Best full-page recipe for a slide: same section, shares the blocks' top layouts, fits the message."""
        q = toks(topic["message"] + " " + " ".join(b.get("what", "") for b in topic["blocks"]))
        best = None
        for r in self.lib.values():
            if r.get("kind") != "page" or topic["section"] not in r["sections"]:
                continue
            fit = _sim(q, toks(r["use_when"] + " " + r["name"]))
            s = 1 + len(set(r.get("components", [])) & set(tops)) + 2 * fit
            if fit >= 0.1 and s >= 2 and (best is None or s > best[0]):
                best = (round(s, 2), r)
        return best

    def candidates(self, block, section, k=5):
        sh = shape(block)
        pool = [r for r in self.lib.values()
                if r.get("kind") == "layout" or r.get("source") == "bank"      # bank pages carry a whole slide
                or (r.get("kind") == "map" and sh["data_type"] == "geography")
                or (r.get("kind") == "icon_set" and sh["data_type"] == "icons")]
        ranked = sorted(((*self.score(r, sh, section), r) for r in pool), key=lambda t: -t[0])
        out = []
        for sc, why, r in ranked[:k]:
            out.append({"id": r["id"], "score": sc, "name": r.get("name", ""), "why": "; ".join(why),
                        "use_when": r.get("use_when", ""), "real_pages": r.get("real_pages", 0),
                        "thumb": os.path.join(ASSETS, r["thumb"]) if r.get("thumb") else "",
                        "exemplar": self.exemplar(r["id"], section)})
        return out


def sheet(rows, out_png, cell=(330, 186)):
    """One PNG per slide: a row per block, its candidates' thumbnails left to right, then the top pick's real page."""
    from PIL import Image, ImageDraw, ImageFont
    cw, ch = cell
    cap = 34
    ncol = max(len(c) for _, c in rows) + 1
    img = Image.new("RGB", (ncol * (cw + 10) + 10, len(rows) * (ch + cap + 30) + 10), "white")
    dr = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 13)
        bold = ImageFont.truetype("arialbd.ttf", 14)
    except OSError:
        font = bold = ImageFont.load_default()
    y = 10
    for title, cands in rows:
        dr.text((10, y), title[:140], fill="black", font=bold)
        y += 22
        tiles = [(c["thumb"], f"{i + 1}. {c['id']}  ({c['score']})") for i, c in enumerate(cands)]
        ex = cands[0]["exemplar"] if cands else None
        if ex:
            tiles.append((ex["thumb"], f"real: {ex['bank'][:18]} p{ex['page']}"))
        for j, (path, label) in enumerate(tiles):
            x = 10 + j * (cw + 10)
            dr.rectangle([x, y, x + cw, y + ch], outline="#BBBBBB")
            if path and os.path.exists(path):
                im = Image.open(path).convert("RGB")
                im.thumbnail((cw - 2, ch - 2))
                img.paste(im, (x + 1 + (cw - 2 - im.width) // 2, y + 1 + (ch - 2 - im.height) // 2))
            else:
                dr.text((x + 8, y + ch // 2), "(no thumbnail: coded component)", fill="#888888", font=font)
            dr.text((x, y + ch + 4), label, fill="#1F3864" if j < len(cands) else "#7F6000", font=font)
        y += ch + cap
    img.save(out_png)


def match(path, k=5):
    m = Matcher()
    doc = _load(path)
    stem = os.path.splitext(path)[0]
    outdir = stem + "_match"
    os.makedirs(outdir, exist_ok=True)
    result = []
    for t in doc["topics"]:
        rows, tops = [], []
        print(f"\n== Slide {t['slide']} [{t['section']}] {t['message']}")
        for i, b in enumerate(t["blocks"]):
            cands = m.candidates(b, t["section"], k)
            sh = shape(b)
            print(f"  block {i + 1}: {b.get('what', '')}  ({sh['data_type']}, {sh['items']} items, {sh['words']} words, "
                  f"{'numbers' if sh['numbers'] else 'no numbers'})")
            for j, c in enumerate(cands):
                ex = c["exemplar"]
                seen = f" | e.g. {ex['bank']} p{ex['page']}" if ex else ""
                print(f"    {j + 1}. {c['id']:<15} {c['score']:>5}  {c['why'][:70]}{seen}")
            rows.append((f"Block {i + 1}: {b.get('what', '')}", cands))
            result.append({"slide": t["slide"], "block": i + 1, "what": b.get("what", ""), "candidates": cands})
            tops.append(cands[0]["id"] if cands else "")
        rec = m.recipe(t, tops)
        if rec:
            sc, r = rec
            print(f"  page recipe: {r['id']} ({sc}): {r['use_when'][:90]}")
            rows.append((f"Whole-page option: {r['id']}", [{"id": r["id"], "score": sc,
                         "thumb": os.path.join(ASSETS, r["thumb"]), "exemplar": m.exemplar(r["id"], t["section"])}]))
            result.append({"slide": t["slide"], "page_recipe": r["id"], "score": sc})
        sheet(rows, os.path.join(outdir, f"slide{int(t['slide']):02d}.png"))
    with open(os.path.join(outdir, "candidates.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, indent=1, ensure_ascii=False)
    print(f"\nsheets + candidates.json -> {os.path.abspath(outdir)}")


def plan(path):
    """Print the slide plan table (picks + alternatives) and check the deck rules. Returns the number of errors."""
    m = Matcher()
    doc = _load(path)
    errs, warns = [], []
    print("| # | Section | Message | Layouts (lead first) | Alternatives | Why |")
    print("|---|---|---|---|---|---|")
    leads, used = [], set()
    for t in doc["topics"]:
        picks, alts, whys = [], [], []
        n_bullets = 0
        for i, b in enumerate(t["blocks"]):
            pk = b.get("pick")
            if not pk:
                errs.append(f"slide {t['slide']} block {i + 1}: no pick")
                continue
            ids = [x.strip() for x in pk.split("+") if x.strip()]  # "ig075+table" = combined on one exhibit
            bad = [x for x in ids if x not in m.lib]
            if bad or not ids:
                errs.append(f"slide {t['slide']} block {i + 1}: {', '.join(bad) or pk!r} not in layout_library.json")
                continue
            r = m.lib[ids[0]]
            sh = shape(b)
            lo, hi = (r.get("items") or [1, 99])[:2]
            if len(ids) == 1 and not lo <= sh["items"] <= hi:
                warns.append(f"slide {t['slide']} {pk}: {sh['items']} items, layout takes {lo}-{hi}")
            top = [c["id"] for c in m.candidates(b, t["section"], 5)]
            picks.append(pk + ("" if ids[0] in top else "*"))
            if i == 0:
                alts = b.get("alts", [])          # alternatives shown for the lead exhibit
            if b.get("why"):
                whys.append(b["why"])
            used.update(ids)
            n_bullets += ids.count("bullets")
        if n_bullets > 2:
            warns.append(f"slide {t['slide']}: {n_bullets} bullet blocks (max 2)")
        if t["blocks"] and all(m.lib.get(x.strip(), {}).get("data_type") == "text"
                               for b in t["blocks"] for x in (b.get("pick") or "").split("+")):
            warns.append(f"slide {t['slide']}: text only; add an exhibit (Rule 0)")
        lead = t["blocks"][0].get("pick") if t["blocks"] else None
        if leads and lead and lead == leads[-1]:
            warns.append(f"slide {t['slide']}: same lead layout as the slide before ({lead})")
        leads.append(lead)
        print(f"| {t['slide']} | {t['section']} | {t['message']} | {', '.join(picks)} | {', '.join(alts[:3])} | "
              f"{'; '.join(whys)[:160]} |")
    if not (used & VISUAL or any(u.startswith("ig") for u in used)):
        warns.append("no visual layout in the deck (Rule 3)")
    print("\n* = picked from outside the top 5 (fine if the reason says why)")
    for w in warns:
        print("WARN:", w)
    for e in errs:
        print("ERROR:", e)
    print(f"{len(doc['topics'])} slides, {len(errs)} errors, {len(warns)} warnings")
    return len(errs)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        sys.stdout.reconfigure(encoding="utf-8")
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "match" and len(sys.argv) > 2:
        match(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 5)
    elif cmd == "plan" and len(sys.argv) > 2:
        sys.exit(1 if plan(sys.argv[2]) else 0)
    else:
        sys.exit(__doc__)
