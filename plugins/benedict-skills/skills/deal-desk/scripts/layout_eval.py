r"""Layout-choice eval: golden dataset, review sheet, fixed 80/20 split, scoring (references/deck-pipeline.md, "Eval").

  python layout_eval.py seed-pages <out.jsonl> [n]      # stratified real bank pages + their text, for blind chunking
  python layout_eval.py add-chunks <chunks.json>        # chunked real pages -> pending golden rows (bank's layout = label)
  python layout_eval.py add-plan <topics.json> --source NAME [--approved]
                                                        # picked slide plan -> rows (--approved: he OK'd it = accepted)
  python layout_eval.py review                          # pending rows -> golden_review.xlsx in the toolkit folder
  python layout_eval.py ingest                          # his top / alt / other / reject picks -> golden.jsonl
  python layout_eval.py examples [--all]                # train rows -> assets/eval/examples.md (few-shot for select)
  python layout_eval.py matcher [--set final|dev|train] [--all]   # score layout_match.py -> scores.md
  python layout_eval.py blind [--set final|dev|train-a|train-b] [--all]
                                                        # blind task for a subagent -> assets/eval/runs/<stamp>_<set>/task.md
  python layout_eval.py score <answers.json> [--all]    # score the subagent's answers -> scores.md (+ misses.json)
  python layout_eval.py stats

Rows with status "accepted" (his review) or "silver" (3 judges agreed, layout_loop.py) count; --all also counts
"pending" ones (a provisional score, labelled as such).
Split (a hash of the row id, so it never moves when rows are added): 1 in 5 -> final (the hold-out, scored once per
tuning run), 1 in 5 -> dev (decides whether a wording change is kept), the rest -> train (examples.md, and the misses
the analyst learns from; train-a / train-b are its halves, each tested with the other half as examples).
Final and dev rows are never written into examples.md or a task's examples.

Row: {"id", "source", "ref", "thumb", "section", "message", "block": {what, data_type, about, content, unit?},
      "label", "acceptable": [ids that also count as right], "alternates"?: [2 runner-ups shown in review], "why", "status", "reviewer", "added", "flag"?}
"""
import datetime
import hashlib
import itertools
import json
import os
import re
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import layout_match as lm  # noqa: E402

ASSETS = os.path.join(HERE, "..", "assets")
EVAL = os.path.join(ASSETS, "eval")
GOLDEN = os.path.join(EVAL, "golden.jsonl")
SCORES = os.path.join(EVAL, "scores.md")
EXAMPLES = os.path.join(EVAL, "examples.md")
SWAPS = os.path.join(EVAL, "swaps.md")
RUNS = os.path.join(EVAL, "runs")
PIPELINE = os.path.join(HERE, "..", "references", "deck-pipeline.md")
sys.path.insert(0, HERE)
import paths  # noqa: E402
TOOLKIT = os.environ.get("DEAL_DESK_TOOLKIT", str(paths.TOOLKIT))
REVIEW_XLSX = os.path.join(TOOLKIT, "golden_review.xlsx")

# layouts that do the same job (a bank's bar is as right as our column): counted as right by default
EQUIV = {"bar": ["column"], "column": ["bar"], "fin_table": ["table"], "table": ["fin_table"],
         "stat_strip": ["stat_icons"], "stat_icons": ["stat_strip"], "chevrons": ["numbered_steps"],
         "numbered_steps": ["chevrons"], "pill_rows": ["side_tabs"], "side_tabs": ["pill_rows"],
         "bullets": ["takeaway"]}
# a bank page's whole-page label -> the block layout that carries it
PAGE_TO_BLOCK = {"page_text": "bullets", "page_risks": "risk_matrix", "page_thesis": "side_tabs",
                 "page_deals": "table", "page_landscape": "logo_row", "page_geography": "map_pins",
                 "page_overview": "stat_icons", "page_market": "bullets"}
SHAPE_WORDS = re.compile(r"\b(\d+|items?|numbers?|figures?|series|unit|dated|dates|periods?|years?|words?|text|"
                         r"rows?|columns?|steps?|stages?|names?|kpi|trend|ranking|rank|compar\w*|composition|mix|"
                         r"range|matrix|grid|process|sequence|cycle|loop|hierarchy|geograph\w*|map|sites?)\b", re.I)


def today():
    return datetime.date.today().isoformat()


def _h(rid):
    return int(hashlib.sha1(rid.encode()).hexdigest(), 16)


def holdout(rid):
    return _h(rid) % 5 == 0


def split(rid):
    """final (hold-out) / dev (keeps or reverts a change) / train-a / train-b (examples + analyst's misses)."""
    k = _h(rid) % 5
    return "final" if k == 0 else "dev" if k == 1 else "train-a" if (_h(rid) // 5) % 2 == 0 else "train-b"


def in_set(rid, name):
    s = split(rid)
    return s == name or (name == "train" and s.startswith("train"))


def load_rows():
    if not os.path.exists(GOLDEN):
        return []
    with open(GOLDEN, encoding="utf-8") as f:
        return [json.loads(x) for x in f if x.strip()]


def save_rows(rows):
    os.makedirs(EVAL, exist_ok=True)
    with open(GOLDEN, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def add_rows(new):
    rows = load_rows()
    have = {r["id"] for r in rows}
    added = [r for r in new if r["id"] not in have]
    save_rows(rows + added)
    print(f"{len(added)} rows added ({len(new) - len(added)} already there); golden.jsonl now {len(rows) + len(added)}")
    return added


def usable(rows, include_pending):
    ok = {"accepted", "silver", "pending"} if include_pending else {"accepted", "silver"}
    return [r for r in rows if r["status"] in ok]


def _affinity(dt, lid, lib):
    r = lib.get(lid, {})
    return 1.0 if r.get("data_type") == dt else lm.NEAR.get(dt, {}).get(r.get("data_type"), 0)


# ---------- seeding ----------

def seed_pages(out, n=0):
    """Stratified pick of real bank pages by lead layout (rare layouts all in, common ones capped), with page text."""
    import pymupdf
    pg = lm._load(lm.PAGES_JSON)
    root, pages = pg["root"], pg["pages"]
    by_lead = defaultdict(list)
    for p in pages:
        by_lead[p["layouts"][0]].append(p)
    cap = {lead: 4 for lead in by_lead}
    for lead, ps in by_lead.items():
        if len(ps) > 30:
            cap[lead] = 6
        elif len(ps) > 9:
            cap[lead] = 5
    picked = []
    for lead, ps in sorted(by_lead.items(), key=lambda kv: len(kv[1])):
        ps = sorted(ps, key=lambda p: (-p["fill"], p["id"]))
        seen_decks = Counter()
        for p in ps:                                  # spread across decks before taking a second page from one
            if len([q for q in picked if q["layouts"][0] == lead]) >= cap[lead]:
                break
            if seen_decks[p["deck"]] >= 1 and len(ps) > cap[lead] * 2:
                continue
            seen_decks[p["deck"]] += 1
            picked.append(p)
    picked = picked[:n] if n else picked
    # most SEC decks are scans with no text layer: render those pages and read them with Windows OCR (ocr.ps1)
    import subprocess
    import tempfile
    texts, scans = {}, tempfile.mkdtemp(prefix="layout_eval_ocr_")
    for p in picked:
        doc = pymupdf.open(os.path.join(root, p["file"]))
        page = doc[p["page"] - 1]
        texts[p["id"]] = page.get_text()
        if len(texts[p["id"]].strip()) < 150:
            page.get_pixmap(matrix=pymupdf.Matrix(2400 / page.rect.width, 2400 / page.rect.width)).save(
                os.path.join(scans, p["id"] + ".png"))
        doc.close()
    if os.listdir(scans) and sys.platform != "win32":
        print("  (scanned pages need Windows OCR (ocr.ps1): skipped on this machine, re-run on the PC)")
    elif os.listdir(scans):
        ocr_out = os.path.join(scans, "ocr.tsv")
        subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
                        os.path.join(HERE, "deck_library", "ocr.ps1"), scans, ocr_out], check=True)
        with open(ocr_out, encoding="utf-8-sig") as f:
            for ln in f:
                k, _, v = ln.rstrip("\n").partition("\t")
                if v and v != "ERR":
                    texts[k[:-4]] = v.replace(" | ", "\n")
    with open(out, "w", encoding="utf-8") as f:
        for p in picked:
            text = re.sub(r"[ \t]+", " ", re.sub(r"\n{2,}", "\n", texts[p["id"]])).strip()[:2400]
            f.write(json.dumps({"page_id": p["id"], "title": p["title"], "section": p["section"],
                                "exhibits": len(p["layouts"]), "text": text}, ensure_ascii=False) + "\n")
    print(f"{len(picked)} pages -> {out}")
    print(Counter(p["layouts"][0] for p in picked).most_common())


def add_chunks(path):
    """Chunker output [{"page_id", "section", "message", "blocks": [...]}] -> pending rows; block i <-> bank layout i."""
    lib = lm.Matcher().lib
    pg = lm._load(lm.PAGES_JSON)
    pages = {p["id"]: p for p in pg["pages"]}
    new = []
    for t in lm._load(path):
        p = pages[t["page_id"]]
        labs = [PAGE_TO_BLOCK.get(x, x) for x in p["layouts"]]
        # the bank tags say which layouts are on the page, not which exhibit is which: pair them by best data-type fit
        # (ties keep reading order)
        best = max(itertools.permutations(labs, min(len(labs), len(t["blocks"]))),
                   key=lambda perm: (sum(_affinity(b.get("data_type", ""), lab, lib) for b, lab in zip(t["blocks"], perm)),
                                     -sum(labs.index(lab) != i for i, lab in enumerate(perm))))
        for i, (b, lab) in enumerate(zip(t["blocks"], best)):
            row = {"id": f"rp_{p['id']}_b{i + 1}", "source": "real_page",
                   "ref": f"{p['bank']} · {p['deck']} p{p['page']}", "thumb": os.path.join(pg["root"], p["thumb"]),
                   "section": t.get("section") or p["section"], "message": t.get("message", p["title"]),
                   "block": b, "label": lab, "acceptable": EQUIV.get(lab, []),
                   "why": f"bank's choice: {p['note']}", "status": "pending", "reviewer": "", "added": today()}
            if _affinity(b.get("data_type", ""), lab, lib) < 0.3:
                row["flag"] = f"check: chunk says {b.get('data_type')}, bank layout is {lab}"
            new.append(row)
    add_rows(new)


def add_plan(path, source, approved=False):
    """Slide plan with picks -> rows. With --approved (he OK'd the plan table) they go straight in as accepted."""
    m = lm.Matcher()
    doc = lm._load(path)
    slug = re.sub(r"[^a-z0-9]+", "_", source.lower()).strip("_")
    new, swaps = [], []
    for t in doc["topics"]:
        for i, b in enumerate(t["blocks"]):
            pk = b.get("pick")
            if not pk:
                continue
            blk = {k: b[k] for k in ("what", "data_type", "about", "content", "unit") if k in b}
            top = m.candidates(b, t["section"], 1)
            top1 = top[0]["id"] if top else ""
            row = {"id": f"{slug}_s{int(t['slide']):02d}_b{i + 1}", "source": f"{'plan' if approved else 'case'}:{source}",
                   "ref": f"{doc.get('deck', source)} slide {t['slide']}", "thumb": "",
                   "section": t["section"], "message": t["message"], "block": blk, "label": pk,
                   "acceptable": sorted(set(b.get("acceptable", EQUIV.get(pk, [])))),
                   "why": b.get("why", ""), "status": "accepted" if approved else "pending",
                   "reviewer": "Benedict (plan approval)" if approved else "", "added": today(), "matcher_top1": top1}
            if b.get("swapped_from"):
                row["swapped_from"] = b["swapped_from"]
            new.append(row)
            if approved and (b.get("swapped_from") or (top1 and pk != top1 and top1 not in row["acceptable"])):
                swaps.append((row, b.get("swapped_from") or top1))
    add_rows(new)
    _log_swaps(swaps)


def _log_swaps(swaps):
    """Lessons loop: each swap is a candidate 'dont_use_when' line for the layout that lost."""
    if not swaps:
        return
    new = not os.path.exists(SWAPS)
    with open(SWAPS, "a", encoding="utf-8") as f:
        if new:
            f.write("# Layout swaps (lessons loop)\nEach line: the layout the matcher or Claude offered, what he chose "
                    "instead, and the block. Two or more swaps of the same pair -> add a `dont_use_when` line to the "
                    "losing layout in layout_tag.py, rebuild, and re-run the eval.\n\n")
        for row, lost in swaps:
            b = row["block"]
            f.write(f"- {row['added']} · {lost} -> **{row['label']}** · {b.get('what', '')} ({b.get('data_type', '')}, "
                    f"{len(b.get('content', []))} items) · {row['ref']}\n")
    pairs = Counter((lost, row["label"]) for row, lost in swaps)
    print("swaps logged to eval/swaps.md:", ", ".join(f"{a}->{b} x{n}" for (a, b), n in pairs.items()))


# ---------- his review ----------

GUIDE = [
    ("What this sheet is for", "Each row is one block of content (a chart, table, list...) from a real bank page or a "
     "written infographic test. Three Claude judges looked at the page and the layout pictures; the Top pick is their "
     "answer (or most votes), the runner-ups are the next choices. Only rows where they split, plus a random spot "
     "check, are here; the rest are settled. Your answers become the answer key the deck builder is tested against."),
    ("The one question", "For every row: which of the three pictures is the best way to show this block? Compare the "
     "page on the left with the three layout pictures. Click a layout name to open it full size."),
    ("top", "The Top pick is the best fit."),
    ("alt 1 / alt 2", "That runner-up fits better than the Top pick. It becomes the answer."),
    ("top + alt 1 (etc.)", "The best answer combines two of the pictures in one exhibit, e.g. an infographic with a "
     "table beside it. The first named is the lead layout. Both become the answer."),
    ("other", "None of the three is best. Type or pick the right layout id in 'Other id' (dropdown, or browse the "
     "Layouts tab, which has a picture link for every layout). For a combination, type both ids joined by +, lead "
     "first (e.g. ig075+table)."),
    ("reject", "The row itself is broken, so it should not be tested at all: garbled text, the block does not match the "
     "page, or it is not a real exhibit (cover, disclaimer, divider). Rejected rows are dropped. If your thought is "
     "'wrong layout', that is alt 1 / alt 2 / other, not reject."),
    ("Others also OK?", "yes (or blank) = the two pictures you did not choose would also be acceptable, so the deck "
     "builder is not marked wrong for picking them. no = only your choice counts as right."),
    ("Check", "judges split = three Claude judges disagreed, so your call is the answer. spot check = the judges "
     "agreed; these are a random sample to test whether the judges can be trusted (if you agree with ~90% of them, "
     "their other answers stand). judges flag (fragment / duplicate) = two or more judges think the row is broken; their layout answer is still the Top pick; choose reject if you agree, or the right layout if the row is fine. tester disagrees = the blind tester's pick looked better than the judges' answer; the tester's pick is shown as alt 1. Infographic test rows have no page, only the written block."),
    ("Blank", "Still to do. You can review over several sittings; refreshing the sheet keeps what you have entered."),
    ("When done", "Save and close the file, then tell Claude 'ingest the layout review'."),
]
DECISIONS = ["top", "alt 1", "alt 2", "other", "reject"]
# combined answers: one exhibit built from two of the pictures, lead first
COMBOS = {"top + alt 1": (0, 1), "top + alt 2": (0, 2), "alt 1 + alt 2": (1, 2), "alt 1 + top": (1, 0), "alt 2 + top": (2, 0)}
MENU = DECISIONS[:3] + list(COMBOS) + DECISIONS[3:]
HEAD = ["Row id", "Check", "Page / slide", "Block", "Top pick", "Runner-up 1", "Runner-up 2", "Decision", "Other id",
        "Others also OK?", "Note"]
COL = {h: i for i, h in enumerate(HEAD, 1)}


def _exemplar_thumb(rec, root):
    ex = rec.get("exemplars") or []
    if isinstance(ex, str):
        import ast
        try:
            ex = ast.literal_eval(ex)
        except (ValueError, SyntaxError):
            ex = []
    for e in ex:
        if e.get("thumb") and root and os.path.exists(os.path.join(root, e["thumb"])):
            return os.path.join(root, e["thumb"])
    return ""


def layout_link(rec, root):
    """A picture of the layout: a crop of just that component (code_<id>.png, cut from the layout gallery), else its own
    thumb, else the real bank page it was modelled on."""
    own = os.path.join(ASSETS, "layout_thumbs", f"code_{rec.get('id', '')}.png")
    if os.path.exists(own):
        return os.path.abspath(own)
    if rec.get("thumb") and os.path.exists(os.path.join(ASSETS, rec["thumb"])):
        return os.path.abspath(os.path.join(ASSETS, rec["thumb"]))
    return _exemplar_thumb(rec, root)


def _small(src, w, h):
    """A small JPEG copy of a picture for embedding (cached in the toolkit's review_thumbs folder)."""
    from PIL import Image
    out_dir = os.path.join(TOOLKIT, "review_thumbs")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, hashlib.sha1(f"{src}|{w}|{h}".encode()).hexdigest()[:16] + ".jpg")
    if not os.path.exists(out) or os.path.getmtime(out) < os.path.getmtime(src):
        im = Image.open(src).convert("RGB")
        im.thumbnail((w * 2, h * 2))          # 2x for a sharp picture when zoomed
        im.save(out, quality=82)
    return out


def _place(ws, path, row, col, w, h, top_px=0):
    from openpyxl.drawing.image import Image as XLImage
    from openpyxl.drawing.spreadsheet_drawing import AnchorMarker, OneCellAnchor
    from openpyxl.drawing.xdr import XDRPositiveSize2D
    from openpyxl.utils.units import pixels_to_EMU
    from PIL import Image
    iw, ih = Image.open(path).size
    s = min(w / iw, h / ih)
    pic = XLImage(path)
    pic.anchor = OneCellAnchor(_from=AnchorMarker(col=col - 1, row=row - 1, colOff=pixels_to_EMU(4),
                                                  rowOff=pixels_to_EMU(top_px)),
                               ext=XDRPositiveSize2D(pixels_to_EMU(int(iw * s)), pixels_to_EMU(int(ih * s))))
    ws.add_image(pic)


def _prior_decisions():
    """Decisions already typed in the review sheet, so a refresh never wipes them (current layout of the sheet only)."""
    if not os.path.exists(REVIEW_XLSX):
        return {}
    from openpyxl import load_workbook
    ws = load_workbook(REVIEW_XLSX).worksheets[0]
    if [ws.cell(4, j).value for j in range(1, len(HEAD) + 1)] != HEAD:
        return {}                                                  # an older sheet layout: nothing carried over
    out = {}
    for i in range(5, ws.max_row + 1):
        vals = tuple(ws.cell(i, COL[h]).value or "" for h in ("Decision", "Other id", "Others also OK?", "Note"))
        if ws.cell(i, 1).value and any(vals):
            out[ws.cell(i, 1).value] = vals
    return out


def _picks(r):
    alts = r.get("alternates") or r["acceptable"]
    picks = [r["label"], *alts[:2]]
    sp = (r.get("suspect") or {}).get("pick")
    if sp and sp not in picks:  # show the tester's pick beside the judges' answer
        picks = [r["label"], sp, *alts[:1]]
    return picks


def review():
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.worksheet.datavalidation import DataValidation
    if os.path.exists(os.path.join(TOOLKIT, "~$" + os.path.basename(REVIEW_XLSX))):
        sys.exit("golden_review.xlsx is open in Excel. Save and close it first, then run review again "
                 "(your decisions are kept).")
    m = lm.Matcher()
    lib, root = m.lib, m.root
    prior = _prior_decisions()
    # judges split (pending) + a random spot check of rows they agreed on (audit); file order keeps a page together
    rows = [r for r in load_rows() if r["status"] == "pending" or r.get("suspect")
            or (r["status"] == "silver" and r.get("audit"))
            or (r["status"] == "rejected" and r.get("reject_by") == "judges" and r.get("audit"))]
    band = PatternFill("solid", fgColor="1F3864")
    link = Font(color="0563C1", underline="single", bold=True, size=9)
    PAGE_W, PAGE_H, LAY_W, LAY_H, ROW_PX = 260, 150, 175, 132, 168
    wb = Workbook()

    ws = wb.active
    ws.title = "Review"
    ws["A1"] = "Layout eval: pick the best layout for each block"
    ws["A1"].font = Font(bold=True, size=14, color="FFFFFF")
    ws["A2"] = ("Compare the page with the three layout pictures.   top = Top pick is best   ·   alt 1 / alt 2 = that "
                "runner-up is better   ·   other = none of them (fill 'Other id')   ·   reject = the row is broken.   "
                "Full guide: Guide tab.")
    ws["A2"].font = Font(italic=True, size=9, color="FFFFFF")
    for row in (1, 2):
        for col in range(1, len(HEAD) + 1):
            ws.cell(row, col).fill = band
    for j, h in enumerate(HEAD, 1):
        c = ws.cell(4, j, h)
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="bottom")
    ids = sorted(lib, key=lambda k: (lib[k].get("kind") != "layout", k.startswith("ig"), k))
    dv = DataValidation(type="list", formula1='"' + ",".join(MENU) + '"', allow_blank=True)
    dv_to = DataValidation(type="list", formula1=f"=Layouts!$A$5:$A${len(ids) + 4}", allow_blank=True,
                           showErrorMessage=True, errorStyle="warning",
                           error="Not in the list. Fine for a combination (id+id, lead first); otherwise pick from the list.")
    dv_ok = DataValidation(type="list", formula1='"yes,no"', allow_blank=True)
    for d in (dv, dv_to, dv_ok):
        ws.add_data_validation(d)
    kept = 0
    for i, r in enumerate(rows, 5):
        b = r["block"]
        content = b.get("content", [])
        content = " · ".join(map(str, content[:6])) if isinstance(content, list) else str(content)
        dec = prior.get(r["id"], ("", "", "", ""))
        kept += any(dec)
        block = (f"{b.get('what', '')}\n[{r['section']} · {b.get('data_type', '')}]\n{content[:260]}\n"
                 f"Slide message: {r['message']}")
        page = r["ref"] if r.get("thumb") else "Written test block (no page)"
        check = "tester disagrees" if r.get("suspect") else "spot check" if r["status"] == "silver" else \
            f"judges reject ({r.get('reject_why', '')})" if r["status"] == "rejected" else             f"judges flag ({r['flagged']})" if r.get("flagged") else "judges split" if r.get("judges") else ""
        vals = [r["id"], check, page, block, "", "", "", *dec]
        for j, v in enumerate(vals, 1):
            c = ws.cell(i, j, v)
            c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.cell(i, 3).font = Font(size=8, color="595959")
        ws.cell(i, 4).font = Font(size=9)
        if r.get("thumb") and os.path.exists(r["thumb"]):
            ws.cell(i, 3).hyperlink = r["thumb"]
            _place(ws, _small(r["thumb"], PAGE_W, PAGE_H), i, 3, PAGE_W, PAGE_H, top_px=16)
        for j, lid in enumerate(_picks(r), COL["Top pick"]):
            rec = lib.get(lid, {})
            c = ws.cell(i, j, f"{lid} · {rec.get('name', '?')}"[:42])
            c.alignment = Alignment(vertical="top")
            pic = layout_link(rec, root)
            if pic:
                c.hyperlink, c.font = pic, link
                _place(ws, _small(pic, LAY_W, LAY_H), i, j, LAY_W, LAY_H, top_px=18)
            else:
                c.font = Font(size=9, bold=True)
        if check in ("judges split", "tester disagrees"):
            ws.cell(i, 2).font = Font(bold=True, color="C00000")
        dv.add(ws.cell(i, COL["Decision"]))
        dv_to.add(ws.cell(i, COL["Other id"]))
        dv_ok.add(ws.cell(i, COL["Others also OK?"]))
        ws.row_dimensions[i].height = ROW_PX * 0.75
    for col, w in zip("ABCDEFGHIJK", (16, 9, 39, 40, 27, 27, 27, 10, 12, 9, 24)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "B5"
    ws.sheet_view.showGridLines = False

    g = wb.create_sheet("Guide")
    g["A1"] = "How to review"
    g["A1"].font = Font(bold=True, size=14, color="FFFFFF")
    for col in (1, 2):
        g.cell(1, col).fill = band
    for i, (k, v) in enumerate(GUIDE, 3):
        g.cell(i, 1, k).font = Font(bold=True)
        g.cell(i, 1).alignment = Alignment(vertical="top")
        g.cell(i, 2, v).alignment = Alignment(wrap_text=True, vertical="top")
    g.column_dimensions["A"].width = 18
    g.column_dimensions["B"].width = 100
    g.sheet_view.showGridLines = False

    lt = wb.create_sheet("Layouts")
    lt["A1"] = "Every layout the deck builder can pick"
    lt["A1"].font = Font(bold=True, size=14, color="FFFFFF")
    lt["A2"] = ("Click an id to see it. Order: coded components and pages, bank designs (bk..), PwC infographics (ig..), "
                "then recipes.")
    lt["A2"].font = Font(italic=True, size=9, color="FFFFFF")
    for row in (1, 2):
        for col in range(1, 6):
            lt.cell(row, col).fill = band
    for j, h in enumerate(["Id", "Name", "Kind", "Type of data", "Use when"], 1):
        lt.cell(4, j, h).font = Font(bold=True)
    for i, k in enumerate(ids, 5):
        rec = lib[k]
        for j, v in enumerate([k, rec.get("name", ""), rec.get("kind", ""), rec.get("data_type", ""),
                               rec.get("use_when", "")], 1):
            lt.cell(i, j, v).alignment = Alignment(wrap_text=True, vertical="top")
        pic = layout_link(rec, root)
        if pic:
            lt.cell(i, 1).hyperlink = pic
            lt.cell(i, 1).font = Font(color="0563C1", underline="single")
    for col, w in zip("ABCDE", (12, 32, 10, 14, 80)):
        lt.column_dimensions[col].width = w
    lt.freeze_panes = "A5"
    lt.sheet_view.showGridLines = False

    os.makedirs(TOOLKIT, exist_ok=True)
    wb.save(REVIEW_XLSX)
    print(f"{len(rows)} pending rows -> {REVIEW_XLSX} ({kept} earlier decisions kept)")


def ingest():
    from openpyxl import load_workbook
    if os.path.exists(os.path.join(TOOLKIT, "~$" + os.path.basename(REVIEW_XLSX))):
        sys.exit("golden_review.xlsx is open in Excel. Save and close it first so no decisions are missed.")
    lib = lm.Matcher().lib
    ws = load_workbook(REVIEW_XLSX).worksheets[0]
    if [ws.cell(4, j).value for j in range(1, len(HEAD) + 1)] != HEAD:
        sys.exit("golden_review.xlsx is an older layout of the sheet: run review again first.")
    rows = load_rows()
    by_id = {r["id"]: r for r in rows}
    n, swaps, bad, audit = Counter(), [], [], Counter()
    for i in range(5, ws.max_row + 1):
        rid = ws.cell(i, 1).value
        dec = str(ws.cell(i, COL["Decision"]).value or "").strip().lower()
        other = str(ws.cell(i, COL["Other id"]).value or "").strip()
        also = str(ws.cell(i, COL["Others also OK?"]).value or "").strip().lower() != "no"
        note = str(ws.cell(i, COL["Note"]).value or "").strip()
        r = by_id.get(rid)
        if not r or not dec:
            continue
        dec = " + ".join(x.strip() for x in dec.split("+"))
        if dec not in MENU:
            bad.append(f"{rid}: decision {dec!r} is not one of {', '.join(MENU)}")
            continue
        if r.get("audit") and (r["status"] == "silver" or r.get("reject_by") == "judges"):
            judged_bad = r.get("reject_by") == "judges"
            if dec == "reject" or judged_bad:  # a layout choice is checked below
                r["audit_result"] = "agree" if (dec == "reject") == judged_bad else "disagree"
                audit[r["audit_result"]] += 1
        if dec == "reject":
            r["status"] = "rejected"
            r["reject_by"] = "Benedict"
        else:
            picks = _picks(r)
            if dec == "other":
                parts = [x.strip() for x in other.split("+") if x.strip()]
                if not parts or any(x not in lib for x in parts):
                    bad.append(f"{rid}: other id {other!r} is not a layout id (or id+id)")
                    continue
            else:
                idx = COMBOS.get(dec) or (DECISIONS.index(dec),)
                if max(idx) >= len(picks):
                    bad.append(f"{rid}: {dec!r} points at an empty picture (only {len(picks)} shown)")
                    continue
                parts = [picks[k] for k in idx]
            chosen, combo = parts[0], parts[1:]
            if r["status"] == "silver" and r.get("audit") and not r.get("audit_result"):
                r["audit_result"] = "agree" if set(parts) & {r["label"], *r["acceptable"], *r.get("combo", [])} else "disagree"
                audit[r["audit_result"]] += 1
            if combo:
                r["combo"] = combo
            else:
                r.pop("combo", None)
            if chosen != r["label"]:
                swaps.append((r, r["label"]))
                r["why"] = f"{r['why']} | {dec}: {r['label']} -> {chosen} in review"
            rest = [p for p in picks if p not in parts] if also else []
            r["label"] = chosen
            r["acceptable"] = list(dict.fromkeys(rest + EQUIV.get(chosen, [])))
            r["status"] = "accepted"
        if note:
            r["note"] = note
        r["reviewer"] = "Benedict"
        if "suspect" in r:  # answered: keep the tester's view for the record, off the review list
            r["suspect_seen"] = r.pop("suspect")
        r["reviewed"] = today()
        r.pop("flag", None)
        n[dec] += 1
    save_rows(rows)
    _log_swaps(swaps)
    print(dict(n), "| still pending:", sum(r["status"] == "pending" for r in rows))
    done = [r for r in rows if r.get("audit_result")]
    if done:
        ok = sum(r["audit_result"] == "agree" for r in done)
        print(f"judges vs you on spot checks: {ok}/{len(done)} = {ok / len(done):.0%} "
              f"({'trust the judges' if ok / len(done) >= 0.9 else 'below 90%: fix the judge step before tuning'})")
    for b in bad:
        print("SKIPPED", b)


# ---------- examples, scoring ----------

def _line(r):
    b = r["block"]
    sh = lm.shape(b)
    unit = f", unit {b['unit']}" if b.get("unit") else ""
    alts = f" (also right: {', '.join(r['acceptable'])})" if r["acceptable"] else ""
    if r.get("combo"):
        alts = f" + {' + '.join(r['combo'])} (combined)" + alts
    return (f"- [{r['section']}] {b.get('what', '')}: {sh['data_type']}, {sh['items']} items, {sh['words']} words, "
            f"{'numbers' if sh['numbers'] else 'no numbers'}{unit} -> **{r['label']}**{alts}. {r['why'][:140]}")


def examples(include_pending=False):
    rows = [r for r in usable(load_rows(), include_pending) if in_set(r["id"], "train")]
    lines = ["# Layout choice examples (train split)",
             f"Built {today()} by `layout_eval.py examples` from {len(rows)} reviewed rows"
             + (" (includes unreviewed rows: provisional)" if include_pending else "") +
             ". Dev and final (hold-out) rows are never listed here. Read before the select step of deck-pipeline.md.", ""]
    by_dt = defaultdict(list)
    for r in rows:
        by_dt[r["block"].get("data_type", "")].append(r)
    for dt in sorted(by_dt):
        lines.append(f"## {dt}")
        lines += [_line(r) for r in sorted(by_dt[dt], key=lambda r: r["id"])]
        lines.append("")
    with open(EXAMPLES, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"{len(rows)} examples -> {EXAMPLES}")


def _test(include_pending, name="final"):
    rows = usable(load_rows(), include_pending)
    test = [r for r in rows if in_set(r["id"], name)]
    if not test:
        sys.exit(f"no {name} rows yet: review some rows (or pass --all for a provisional score)")
    return test


def _rubric(r, ans, lib):
    """Reasoning check: names the content shape, and the pick does not break its own 'don't use when'."""
    why = ans.get("why", "")
    cites = bool(SHAPE_WORDS.search(why))
    sh = lm.shape(r["block"])
    pk = (parts(ans.get("pick", "")) or [""])[0]
    dont = lm._sim(sh["query"], lm.toks(re.sub(r"\(use [^)]*\)", "", lib.get(pk, {}).get("dont_use_when", ""))))
    clean = dont < 0.25 and not (pk in lm.NUMERIC and not sh["numbers"])
    return (cites + clean) / 2


def _log(selector, rows, include_pending, top1, top3, rubric, note="", name="final"):
    new = not os.path.exists(SCORES)
    accepted = sum(r["status"] == "accepted" for r in rows)
    with open(SCORES, "a", encoding="utf-8") as f:
        if new:
            f.write("# Layout eval scores\nHold-out = the fixed 1-in-5 split of golden.jsonl. Keep a prompt or "
                    "library change only if it does not lower top-1 or top-3 on the same set.\n\n"
                    "| Date | Selector | Set | n (accepted) | Top-1 | Top-3 | Reasoning | Note |\n"
                    "|---|---|---|---|---|---|---|---|\n")
        rub = f"{rubric:.0%}" if rubric is not None else "n/a"
        kind = "provisional (incl. pending)" if include_pending else "accepted + silver"
        f.write(f"| {today()} | {selector} | {kind if name == 'final' else kind + ' · ' + name} | "
                f"{len(rows)} ({accepted}) | {top1:.0%} | {top3:.0%} | {rub} | {note} |\n")


def parts(pick):
    """'ig075+table' -> ['ig075', 'table'] (a combo: several layouts carry one exhibit together)."""
    return [p.strip() for p in str(pick or "").split("+") if p.strip()]


def _hit(r, ids):
    ok = {r["label"], *r["acceptable"], *r.get("combo", []), *EQUIV.get(r["label"], [])}
    return any(p in ok for i in ids for p in parts(i))


def matcher(include_pending=False, note="", name="final"):
    m = lm.Matcher()
    test = _test(include_pending, name)
    t1 = t3 = 0
    misses = []
    for r in test:
        ids = [c["id"] for c in m.candidates(r["block"], r["section"], 3)]
        t1 += _hit(r, ids[:1])
        t3 += _hit(r, ids)
        if not _hit(r, ids[:1]):
            misses.append(f"  {r['id']}: label {r['label']}, matcher {', '.join(ids)}")
    n = len(test)
    print(f"matcher on {n} {name} rows: top-1 {t1 / n:.0%}, top-3 {t3 / n:.0%}")
    print("\n".join(misses))
    _log("layout_match.py", test, include_pending, t1 / n, t3 / n, None, note, name)


def blind(include_pending=False, name="final"):
    """Task file for a blind selector (a subagent): pipeline select rules + catalogue + train examples + test blocks.
    final / dev: all train rows as examples. train-a / train-b: the other half only (a row never sees its own answer)."""
    lib = lm.Matcher().lib
    rows = usable(load_rows(), include_pending)
    test = [r for r in rows if in_set(r["id"], name)]
    other = {"train-a": "train-b", "train-b": "train-a"}.get(name, "train")
    train = [r for r in rows if in_set(r["id"], other)]
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out = os.path.join(RUNS, f"{stamp}_{name}")
    os.makedirs(out, exist_ok=True)
    with open(PIPELINE, encoding="utf-8") as f:
        pipe = f.read()
    rules = pipe.split("## 4.")[0]
    cat = []
    for r in lib.values():
        if r.get("kind") not in ("layout", "page", "map", "icon_set"):
            continue
        lo, hi = (r.get("items") or [1, 99])[:2]
        cat.append(f"- `{r['id']}` {r.get('name', '')} ({r.get('data_type', '')}, {lo}-{hi} items"
                   f"{', numbers' if r.get('numbers') else ''})"
                   f": {r.get('use_when', '')} | Don't: {r.get('dont_use_when', '')}")
    qs = []
    for i, r in enumerate(test, 1):
        sh = lm.shape(r["block"])
        qs.append({"q": f"q{i:02d}", "section": r["section"], "message": r["message"], "block": r["block"],
                   "shape": {k: sh[k] for k in ("data_type", "items", "words", "numbers", "series", "dated")}})
    with open(os.path.join(out, "task.md"), "w", encoding="utf-8") as f:
        f.write("# Blind layout selection\nYou are the select step of a slide pipeline. For each question, pick the one "
                "layout id that best carries the block, two alternatives, and a one-line reason that names the content "
                "shape (data type, item count, numbers) and why the pick beats the alternatives.\n"
                "A pick may be a combo `id+id` (e.g. an infographic + a table) when two layouts together carry the "
                "block better than one; use it only then, lead layout first.\n"
                "Use only this file. Do not open golden.jsonl, scores.md or any other eval file.\n\n"
                f"Write `{os.path.join(out, 'answers.json')}` as "
                '{"q01": {"pick": "...", "alts": ["...", "..."], "why": "..."}, ...}.\n\n'
                "## Pipeline rules\n" + rules + "\n## Layout catalogue (id, data type, items: use when | don't)\n"
                + "\n".join(cat) + "\n\n## Worked examples (reviewed choices)\n" + "\n".join(_line(r) for r in train)
                + "\n\n## Questions\n```json\n" + json.dumps(qs, indent=1, ensure_ascii=False) + "\n```\n")
    with open(os.path.join(out, "key.json"), "w", encoding="utf-8") as f:
        json.dump({q["q"]: r["id"] for q, r in zip(qs, test)}, f, indent=1)
    with open(os.path.join(out, "set.txt"), "w") as f:
        f.write(name)
    print(f"{len(test)} questions ({name}), {len(train)} examples -> {os.path.join(out, 'task.md')}")


def score(answers_path, include_pending=False, note=""):
    lib = lm.Matcher().lib
    answers = lm._load(answers_path)
    key = lm._load(os.path.join(os.path.dirname(answers_path), "key.json"))
    by_id = {r["id"]: r for r in load_rows()}
    keep = {"accepted", "silver"} | ({"pending"} if include_pending else set())
    gone = [q for q in key if by_id.get(key[q], {}).get("status") not in keep]
    key = {q: rid for q, rid in key.items() if q not in gone}
    if gone:
        print(f"  {len(gone)} questions skipped (row rejected or pending since the run)")
    test = [by_id[key[q]] for q in key]
    run = os.path.dirname(answers_path)
    sp = os.path.join(run, "set.txt")
    name = open(sp).read().strip() if os.path.exists(sp) else "final"
    t1 = t3 = rub = combos = 0
    misses = []

    def card(i):
        x = lib.get(i, {})
        return {"id": i, "name": x.get("name", ""), "data_type": x.get("data_type", ""),
                "use_when": x.get("use_when", ""), "dont_use_when": x.get("dont_use_when", "")}
    for q, rid in key.items():
        r, a = by_id[rid], answers.get(q, {})
        ids = [a.get("pick", "")] + list(a.get("alts", []))[:2]
        combos += "+" in ids[0]
        t1 += _hit(r, ids[:1])
        t3 += _hit(r, ids)
        rub += _rubric(r, a, lib)
        if not _hit(r, ids[:1]):
            print(f"  {q} {rid}: label {r['label']}, picked {', '.join(ids)} | {a.get('why', '')[:90]}")
            misses.append({"row": rid, "section": r["section"], "message": r["message"], "block": r["block"],
                           "right": card(r["label"]), "also_right": r["acceptable"] + r.get("combo", []),
                           "picked": card((parts(ids[0]) or [""])[0]),
                           "alts": ids[1:], "why": a.get("why", ""), "in_top3": _hit(r, ids)})
    n = len(key)
    with open(os.path.join(run, "misses.json"), "w", encoding="utf-8") as f:
        json.dump(misses, f, indent=1, ensure_ascii=False)
    res = {"set": name, "n": n, "top1": t1 / n, "top3": t3 / n, "reasoning": rub / n, "combo_picks": combos}
    with open(os.path.join(run, "score.json"), "w") as f:
        json.dump(res, f)
    print(f"blind selector on {n} {name}: top-1 {t1 / n:.0%}, top-3 {t3 / n:.0%}, reasoning {rub / n:.0%}"
          f" (combo picks: {combos})")
    _log("blind subagent", test, include_pending, t1 / n, t3 / n, rub / n, note, name)
    return res


def stats():
    rows = load_rows()
    print("status:", dict(Counter(r["status"] for r in rows)))
    print("source:", dict(Counter(r["source"].split(":")[0] for r in rows)))
    print("split:", dict(Counter(split(r["id"]) for r in rows)))
    print("labels:", Counter(r["label"] for r in rows).most_common())
    print("flagged:", sum(bool(r.get("flag")) for r in rows))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    allp = "--all" in a
    note = a[a.index("--note") + 1] if "--note" in a else ""
    cmd = a[0] if a else ""
    sname = a[a.index("--set") + 1] if "--set" in a else "final"
    if cmd == "seed-pages" and len(a) > 1:
        seed_pages(a[1], int(a[2]) if len(a) > 2 else 0)
    elif cmd == "add-chunks" and len(a) > 1:
        add_chunks(a[1])
    elif cmd == "add-plan" and len(a) > 1 and "--source" in a:
        add_plan(a[1], a[a.index("--source") + 1], "--approved" in a)
    elif cmd == "review":
        review()
    elif cmd == "ingest":
        ingest()
    elif cmd == "examples":
        examples(allp)
    elif cmd == "matcher":
        matcher(allp, note, sname)
    elif cmd == "blind":
        blind(allp, sname)
    elif cmd == "score" and len(a) > 1:
        score(a[1], allp, note)
    elif cmd == "stats":
        stats()
    else:
        sys.exit(__doc__)
