r"""Real bank pages, tagged and linked to the layout library (assets/real_deck_pages.json).

    python pages.py select <pages_titled.json> <pages.json> [n=400]
        Pick ~n measured pages (fill >= 0.55, a recognised section title, at most 3 per deck per section and 8 per
        deck, recent decks first), render 640 px thumbnails to <Real IB-PE Decks>\_pages\ and write
        _pages\selection.json. Inputs: the files strips.py / index.py made (deck list, fill, OCR titles).
    python pages.py sheets <out_dir>
        Contact sheets of the selection (20 per sheet, page ids printed) for hand tagging.
    python pages.py build <page_tags.json>
        Merge hand tags {"<deck>_<page>": "layout ids, comma separated | note"} into assets/real_deck_pages.json.
        layout_tag.py build then lists the best pages under each layout as "exemplars".

Layout ids are those in assets/layout_library.json: coded components (table, fin_table, bar, football_field...),
page recipes (page_market, page_text...) and infographic ids (ig045).
"""
import json
import math
import os
import re
import sys

import pymupdf

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".."))
import paths  # noqa: E402
ROOT = str(paths.REAL_DECKS)
PAGES = os.path.join(ROOT, "_pages")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "assets", "real_deck_pages.json")
SEL = os.path.join(PAGES, "selection.json")

# OCR title -> layout-library section (same patterns as index.py)
SECTIONS = [
    ("exec_summary", r"executive summary|situation overview|summary of (the )?(proposal|situation)|key considerations"),
    ("market", r"industry|market (overview|update|dynamics|environment|landscape)|sector|competitive landscape|macro|trends"),
    ("company", r"company overview|business overview|company profile|at a glance|overview of [A-Z]|business description|key (operating )?metrics"),
    ("valuation", r"share price|stock price|price performance|trading (history|performance)|comparable compan|trading "
                  r"comparables|selected (publicly )?traded|trading statistics|peer|benchmark|precedent|selected "
                  r"(precedent )?transactions|premiums? paid|discounted cash flow|\bdcf\b|valuation summary|summary of "
                  r"(financial )?analys|football|preliminary valuation|valuation overview|implied (value|valuation)"),
    ("financials", r"projection|management (plan|case|forecast)|financial (overview|summary|forecast)|long[- ]range plan|business plan"),
    ("returns", r"\blbo\b|leveraged buyout|sponsor returns|illustrative (lbo|returns)|ability to pay"),
    ("process", r"buyer|potential (acquirer|partner|counterpart)|sponsor universe|strategic (parties|buyers)|financial "
                r"sponsors|universe|process|timeline|next steps|calendar|key dates"),
    ("structure", r"capital structure|financing|sources (and|&) uses|debt|liquidity|credit|accretion|dilution|pro forma|"
                  r"contribution analysis|exchange ratio"),
]
# hand-picked in _Index.md: always included
PINNED = {("Qatalyst-Pitch-Book-on-Autonomy", 4), ("Qatalyst-Pitch-Book-on-Autonomy", 8),
          ("Goldman-Sachs-Presentation-to-PowerSchool", 3), ("Diversey-01-Feb-2023", 8)}


def _year(d):
    m = re.findall(r"(?:19|20)\d\d", d.get("title", "") + " " + d.get("file", ""))
    return int(m[-1]) if m else 0


def _section(title):
    for name, rx in SECTIONS:
        if re.search(rx, title or "", re.I):
            return name
    return None


def select(titled, decks_json, n=400):
    pages = json.load(open(titled))
    decks = json.load(open(decks_json))["decks"]
    for p in pages:
        p["section"] = _section(p.get("title"))
    pinned = [p for p in pages if any(k in decks[p["deck"]]["file"] and p["page"] == pg for k, pg in PINNED)]
    cand = [p for p in pages if p["section"] and p["fill"] >= 0.55 and p not in pinned]
    cand.sort(key=lambda p: (-(_year(decks[p["deck"]]) >= 2019), -p["fill"]))
    per_sec = math.ceil(n / len(SECTIONS))
    chosen, by_deck, by_ds, by_sec = list(pinned), {}, {}, {}
    for p in cand:
        d, s = p["deck"], p["section"]
        if by_deck.get(d, 0) >= 8 or by_ds.get((d, s), 0) >= 3 or by_sec.get(s, 0) >= per_sec:
            continue
        chosen.append(p)
        by_deck[d] = by_deck.get(d, 0) + 1
        by_ds[(d, s)] = by_ds.get((d, s), 0) + 1
        by_sec[s] = by_sec.get(s, 0) + 1
    for p in cand:   # top up from the fullest leftovers when a section ran short
        if len(chosen) >= n:
            break
        if p not in chosen and by_deck.get(p["deck"], 0) < 8:
            chosen.append(p)
            by_deck[p["deck"]] = by_deck.get(p["deck"], 0) + 1
    os.makedirs(PAGES, exist_ok=True)
    out, docs = [], {}
    for p in chosen:
        d = decks[p["deck"]]
        pid = f"{p['deck']:03d}_{p['page']:03d}"
        thumb = os.path.join(PAGES, pid + ".png")
        if not os.path.exists(thumb):
            doc = docs.setdefault(d["file"], pymupdf.open(os.path.join(ROOT, d["file"])))
            pg = doc[p["page"] - 1]
            pg.get_pixmap(matrix=pymupdf.Matrix(640 / pg.rect.width, 640 / pg.rect.width)).save(thumb)
        out.append({"id": pid, "bank": d["bank"], "deck": d["title"], "file": d["file"], "page": p["page"],
                    "year": _year(d), "title": p.get("title", ""), "section": p["section"] or "any",
                    "fill": p["fill"], "thumb": f"_pages/{pid}.png"})
    out.sort(key=lambda r: r["id"])
    json.dump(out, open(SEL, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    secs = {}
    for r in out:
        secs[r["section"]] = secs.get(r["section"], 0) + 1
    print(len(out), "pages ->", SEL, secs)


def sheets(out_dir, per=20, cols=5):
    sel = json.load(open(SEL, encoding="utf-8"))
    os.makedirs(out_dir, exist_ok=True)
    W_, H_ = 400, 225
    for start in range(0, len(sel), per):
        chunk = sel[start:start + per]
        rows = math.ceil(len(chunk) / cols)
        doc = pymupdf.open()
        page = doc.new_page(width=cols * W_, height=rows * (H_ + 16))
        for j, r in enumerate(chunk):
            x, y = (j % cols) * W_, (j // cols) * (H_ + 16)
            page.insert_image(pymupdf.Rect(x + 2, y + 16, x + W_ - 2, y + 16 + H_), filename=os.path.join(ROOT, r["thumb"]))
            page.insert_text((x + 4, y + 12), f"{r['id']}  {r['section']}", fontsize=11, color=(0.8, 0, 0))
        f = os.path.join(out_dir, f"pages-{start // per + 1:02d}.png")
        page.get_pixmap(dpi=96).save(f)
        print(f)


def build(tags_path):
    sel = json.load(open(SEL, encoding="utf-8"))
    tags = json.load(open(tags_path, encoding="utf-8"))
    lib = json.load(open(os.path.join(HERE, "..", "..", "assets", "layout_library.json"), encoding="utf-8"))
    ids = {r["id"] for r in lib["layouts"]}
    out, unknown = [], set()
    for r in sel:
        t = tags.get(r["id"])
        if t is None:
            continue
        lay, _, note = t.partition("|")
        r = dict(r, layouts=[x.strip() for x in lay.split(",") if x.strip()], note=note.strip())
        unknown |= set(r["layouts"]) - ids
        out.append(r)
    if unknown:
        sys.exit(f"unknown layout ids: {sorted(unknown)}")
    doc = {"version": 1, "root": ROOT, "note": "Built by deck_library/pages.py build; thumbs are relative to root",
           "pages": out}
    json.dump(doc, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(len(out), "tagged pages ->", os.path.abspath(OUT))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "select":
        select(sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 400)
    elif cmd == "sheets":
        sheets(sys.argv[2])
    elif cmd == "build":
        build(sys.argv[2])
    else:
        sys.exit(__doc__)
