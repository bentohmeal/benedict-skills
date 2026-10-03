r"""Self-improving layout eval: judges set the answers, a blind tester picks, an analyst fixes the wording, keep or revert.

  python layout_loop.py judge-prep [--batches 4] [--judges 3]   # contact sheets + judge tasks -> eval/runs/judge/
  python layout_loop.py consensus [--audit 20]                  # judges' answers -> golden.jsonl (silver / pending)
  python layout_loop.py analyst-prep <run_dir> [<run_dir> ...] --round N   # train misses -> analyst task
  python layout_loop.py apply <proposal.json> --round N         # wording fixes -> layout_notes.json, rebuild library
  python layout_loop.py revert --round N                        # undo round N's fixes, rebuild library
  python layout_loop.py notes                                   # what the loop has changed so far

Loop (references/deck-pipeline.md, "Self-improving loop"):
  1. Judges: 3 independent subagents each see a contact sheet per row (the real page + shuffled candidate layout
     pictures) and name the layout that rebuilds the exhibit the way the bank drew it (+ others that would also do).
     Majority with no objection from the third -> "silver" (counts as an answer); otherwise "pending" for Benedict.
     A random 20 silver rows are flagged "audit": his spot check of the judges (ingest prints the agreement).
  2. Tester: `layout_eval.py blind --set train-a|train-b|dev|final` -> a subagent that sees only task.md picks.
  3. Analyst: reads train misses only (never dev or final) and proposes use_when / dont_use_when rewrites.
  4. Apply, re-test dev: keep if dev top-1 and top-3 do not drop and one of them rises, else revert. Max 3 rounds.
  5. Final (hold-out) is scored before round 1 and after the last kept round only.
"""
import json
import os
import random
import shutil
import subprocess
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import layout_eval as le  # noqa: E402
import layout_match as lm  # noqa: E402

JUDGE = os.path.join(le.RUNS, "judge")
NOTES = os.path.join(le.EVAL, "layout_notes.json")
NOTES_HIST = os.path.join(le.EVAL, "notes_history")
PY = sys.executable


def _load(p, default=None):
    if default is not None and not os.path.exists(p):
        return default
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def _catalogue(lib):
    out = []
    for r in lib.values():
        if r.get("kind") == "reference":
            continue
        lo, hi = (r.get("items") or [1, 99])[:2]
        out.append(f"- `{r['id']}` {r.get('name', '')} ({r.get('kind')}, {r.get('data_type', '')}, {lo}-{hi} items): "
                   f"{r.get('use_when', '')} | Don't: {r.get('dont_use_when', '')}")
    return "\n".join(out)


def _font(n):
    from PIL import ImageFont
    for f in ("arialbd.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(f, n)
        except OSError:
            pass
    return ImageFont.load_default()


def _fit(im, w, h):
    im = im.convert("RGB")
    im.thumbnail((w, h))
    return im


def _sheet(r, cands, lib, root, path):
    """Left: the real page (if any). Right: candidate layout pictures in a 2-wide grid, captioned A · id · name."""
    from PIL import Image, ImageDraw
    PW, PH = (900, 700) if r.get("thumb") else (0, 700)
    cols = 2 if PW else 4
    TW, TH, CAP = (380, 150, 24) if PW else (400, 300, 24)
    rows_n = (len(cands) + cols - 1) // cols
    W = PW + cols * (TW + 12) + 12
    H = max(PH, rows_n * (TH + CAP + 12) + 12)
    sh = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(sh)
    if PW and os.path.exists(r["thumb"]):
        pg = _fit(Image.open(r["thumb"]), PW - 10, PH - 10)
        sh.paste(pg, (5, 5))
        d.rectangle([4, 4, 6 + pg.width, 6 + pg.height], outline="#999999")
    f = _font(17)
    for k, lid in enumerate(cands):
        x = PW + 12 + (k % cols) * (TW + 12)
        y = 12 + (k // cols) * (TH + CAP + 12)
        d.text((x, y), f"{chr(65 + k)} · {lid} · {lib.get(lid, {}).get('name', '')}"[:44], fill="#1F3864", font=f)
        pic = le.layout_link(lib.get(lid, {}), root)
        if pic and os.path.exists(pic):
            im = _fit(Image.open(pic), TW, TH)
            sh.paste(im, (x, y + CAP))
            d.rectangle([x - 1, y + CAP - 1, x + im.width, y + CAP + im.height], outline="#BBBBBB")
        else:
            d.text((x, y + CAP + 10), "(no picture)", fill="#999999", font=f)
    sh.save(path, quality=85)


def _candidates(r, m):
    c = [r["label"], *(r.get("alternates") or r.get("acceptable") or [])[:2]]
    c += [x["id"] for x in m.candidates(r["block"], r["section"], 5)]
    return list(dict.fromkeys(i for i in c if i in m.lib))[:8]


def judge_prep(batches=4, judges=3, out="judge", scope="all"):
    """scope 'silver' re-judges only rows the judges answered before (not his accepted rows)."""
    m = lm.Matcher()
    lib, root = m.lib, m.root
    allrows = le.load_rows()
    rows = [r for r in allrows if r["status"] != "rejected" and (scope == "all" or r["status"] == scope)]
    page = {}
    for r in allrows:
        if r["status"] != "rejected" and r.get("ref"):
            page.setdefault(r["ref"], []).append(r)
    run = os.path.join(le.RUNS, out)
    os.makedirs(run, exist_ok=True)
    os.makedirs(os.path.join(JUDGE, "sheets"), exist_ok=True)
    cat = _catalogue(lib)
    chunks = [rows[i::batches] for i in range(batches)]
    for b, chunk in enumerate(chunks, 1):
        for j in range(1, judges + 1):
            qs = []
            for r in chunk:
                cands = _candidates(r, m)
                random.Random(f"{r['id']}|{j}").shuffle(cands)
                path = os.path.join(JUDGE, "sheets", f"{r['id']}_j{j}.jpg")
                if not os.path.exists(path):
                    _sheet(r, cands, lib, root, path)
                b_ = r["block"]
                qs.append({"row": r["id"], "sheet": path, "has_page": bool(r.get("thumb")), "section": r["section"],
                           "message": r["message"], "exhibit": b_.get("what", ""), "data_type": b_.get("data_type", ""),
                           "about": b_.get("about", ""), "content": b_.get("content", []),
                           "same_page": [{"row": o["id"], "exhibit": o["block"].get("what", ""),
                                          "content": (o["block"].get("content") or [])[:3]}
                                         for o in page.get(r.get("ref"), []) if o["id"] != r["id"]],
                           "candidates": cands})
            ans = os.path.join(run, f"ans_b{b}_j{j}.json")
            with open(os.path.join(run, f"task_b{b}_j{j}.md"), "w", encoding="utf-8") as f:
                f.write(JUDGE_TASK.format(ans=ans, n=len(qs)) + "\n## Layout catalogue (id name (kind, data type, items): "
                        "use when | don't)\n" + cat + "\n\n## Rows\n```json\n" + json.dumps(qs, indent=1, ensure_ascii=False)
                        + "\n```\n")
    print(f"{len(rows)} rows, {batches} batches x {judges} judges -> {run}\\task_b<b>_j<j>.md")


JUDGE_TASK = """# Layout judge
You are setting the answer key for a slide-layout test. Work alone: use only this file and the sheet images it names.
Do not open golden.jsonl, scores.md, examples.md, swaps.md or any other file in the eval folder.

For each of the {n} rows below, open its `sheet` image with the Read tool. The left side is a real bank page (or, when
`has_page` is false, there is no page: judge from the written block). The right side shows candidate layouts from the
deck builder's library, lettered A, B, C... with their ids.

The question for every row: **which layout id would rebuild this exhibit (the `exhibit` / `content` fields: one chart,
table or list on the page, not the whole page) the way the bank actually drew it?** For rows without a page: which
layout would a top bank analyst choose for this content and message?
- Look at the shape of what the bank drew: chart type and orientation, table with or without bars / heat colours,
  number of panels, text boxes vs bullets, map, logos. Match that, not just the topic.
- You may name any id from the catalogue below, not only the candidates on the sheet, if it fits better.
- **Combos are allowed:** when the bank drew the exhibit with two layouts together (e.g. an infographic with a table
  beside it, two infographics side by side), answer `best` as `"<lead id>+<second id>"`. Only when both are really
  there; a single layout stays a single id.
- `ok`: other ids a demanding banker would also accept for this exhibit (0-3). Leave it empty if only one fits.
- `why`: one line naming what you saw (e.g. "horizontal bars ranked, 6 items, values at bar end").
- `flag`: "" for a good row. Otherwise one of:
  - `fragment`: the block is only part of one exhibit (half of a table, the text that belongs to a chart or funnel
    beside it, one column of a grid), so its layout can't be judged on its own.
  - `duplicate`: it repeats the content of a row in `same_page` (same items or the same exhibit). Flag only the row
    whose id sorts later, so one copy survives.
  - `garbled`: the text is unreadable or does not match the page.
  - `footnote`: notes, sources or filler, not an exhibit.
  Flag strictly: a good self-contained exhibit with plain text is NOT a fragment. Still give `best` for a flagged row.

Write `{ans}` as
{{"<row id>": {{"best": "<id or id+id>", "ok": ["<id>", ...], "why": "...", "flag": ""}}, ...}}
covering every row. Be decisive and consistent; other judges answer the same rows independently.
"""


# 2+ judges flagging fragment/duplicate sends the row to his review; it is never dropped on the judges' word alone
# (3 Oct 2026: he overturned 7 of 8 judge rejects)
REJECT_FLAGS = ("fragment", "duplicate")


def consensus(audit_n=20, out="judge", reject_audit=0):
    rows = le.load_rows()
    by_id = {r["id"]: r for r in rows}
    lib = lm.Matcher().lib
    run = os.path.join(le.RUNS, out)
    votes = {}
    for fn in sorted(os.listdir(run)):
        if fn.startswith("ans_") and fn.endswith(".json"):
            for rid, a in _load(os.path.join(run, fn)).items():
                ids = le.parts(a.get("best"))
                if rid in by_id and ids and all(i in lib for i in ids):
                    a["best"], a["combo"] = ids[0], ids[1:]
                    a["ok"] = [p for i in a.get("ok", []) for p in le.parts(i) if p in lib and p != a["best"]]
                    a["flag"] = a.get("flag") or ("garbled" if a.get("doubt") else "")
                    votes.setdefault(rid, []).append(a)
    stats, silver, judged_bad = Counter(), [], []
    for rid, vs in votes.items():
        r = by_id[rid]
        if len(vs) < 3:
            stats["fewer than 3 judges"] += 1
            continue
        r.pop("audit", None)
        # his rule: only fragments and duplicates reject a row; garbled/footnote are noted, not dropped
        flags = Counter(v["flag"] for v in vs if v["flag"] in REJECT_FLAGS)
        if sum(flags.values()) >= 2:
            r["judges"] = [{k: v.get(k) for k in ("best", "combo", "ok", "why", "flag")} for v in vs]
            r["status"], r["flagged"] = "pending", flags.most_common(1)[0][0]
            stats[f"judges flag ({r['flagged']}) -> his review"] += 1
            # still answer the layout, so a row he keeps has picks to choose from
        else:
            r.pop("flagged", None)
        best = Counter(v["best"] for v in vs)
        okset = [{v["best"], *v["ok"]} for v in vs]
        top, cnt = best.most_common(1)[0]
        objection = [s for s in okset if top not in s]
        reach = Counter(i for s in okset for i in s)
        others = [i for i, n in reach.most_common() if i != top]
        r.setdefault("claude_label", r["label"])
        r["judges"] = [{k: v.get(k) for k in ("best", "combo", "ok", "why", "flag")} for v in vs]
        r["label"] = top
        combo = Counter(c for v in vs if v["best"] == top for c in v["combo"])
        r["combo"] = [c for c, n in combo.items() if n >= 2]
        if not r["combo"]:
            r.pop("combo")
        if cnt >= 2 and not objection and not r.get("flagged"):
            r["status"] = "silver"
            r["acceptable"] = [i for i in others if reach[i] >= 2]
            r["alternates"] = (r["acceptable"] + [i for i in others if i not in r["acceptable"]])[:2]
            r["why"] = f"judges {cnt}/3 agree: {vs[0].get('why', '')[:120]}"
            stats["silver (unanimous)" if cnt == 3 else "silver (2 + 1 also OK)"] += 1
            silver.append(r)
        else:
            r["status"] = "pending"
            r["acceptable"] = others[:2]
            r["alternates"] = others[:2]
            r["why"] = "judges split: " + " / ".join(f"{v['best']} ({v.get('why', '')[:60]})" for v in vs)
            if r.get("flagged"):
                r["why"] = f"judges flag {r['flagged']}; layout votes: " + " / ".join(v["best"] for v in vs)
            else:
                stats["judges split -> his review"] += 1
    for r in random.Random(le.today()).sample(silver, min(audit_n, len(silver))):
        r["audit"] = True
    for r in random.Random(le.today() + "x").sample(judged_bad, min(reject_audit, len(judged_bad))):
        r["audit"] = True
    le.save_rows(rows)
    agree_me = sum(by_id[i]["label"] == by_id[i].get("claude_label") for i in votes)
    print(dict(stats))
    print(f"judges' answer = my earlier top pick on {agree_me}/{len(votes)} rows; spot checks flagged: "
          f"{min(audit_n, len(silver))} silver + {min(reject_audit, len(judged_bad))} judge rejects")


ANALYST_TASK = """# Layout analyst, round {rnd}
A blind tester picked slide layouts from the catalogue below (by reading only each layout's name, use when and don't
use when) and got the rows in `misses` wrong. Your job: rewrite the wording so the next tester picks right.

Rules
- Change only `use_when` and/or `dont_use_when`, for at most {cap} layouts. Fix patterns, not single rows: prefer a
  confusion that repeats (same right vs picked pair, or same cause) across 2+ misses.
- Describe the content shape and the look (data type, item count, numbers or not, chart / table style, panels), in
  general words. Never name a company, deal, bank or figure from the misses.
- Keep the "(use <id>)" pointers in dont_use_when for the usual mix-up. Max ~240 characters per field.
- A fix must not steal correct picks from other layouts: check the catalogue for layouts with similar wording.
- Some answers may be wrong rather than the wording (the answer key was set by judges). List those in
  `suspect_labels` instead of bending the wording to fit them.
- Use only this file. Do not open golden.jsonl, scores.md or any other eval file.
{history}
Write `{out}` as
{{"patterns": ["<one line per confusion you found, with the count>"],
  "notes": {{"<layout id>": {{"use_when": "<new text, or omit>", "dont_use_when": "<new text, or omit>",
                             "why": "<which pattern this fixes>"}}}},
  "suspect_labels": [{{"row": "<row id>", "why": "..."}}]}}

## Misses ({n}, from the train split)
```json
{misses}
```

## Current catalogue (id name (kind, data type, items): use when | don't)
{cat}
"""


def analyst_prep(run_dirs, rnd, cap=8):
    lib = lm.Matcher().lib
    misses = []
    for d in run_dirs:
        p = os.path.join(d, "misses.json")
        name = open(os.path.join(d, "set.txt")).read().strip()
        if not name.startswith("train"):
            sys.exit(f"{d} is a {name} run: the analyst only sees train misses")
        misses += _load(p)
    hist = _load(NOTES, {}).get("history", [])
    h = ""
    if hist:
        h = "\nEarlier rounds (do not repeat a reverted change):\n" + "\n".join(
            f"- round {x['round']}: {x['result']} (dev top-1 {x.get('dev_top1', '?')}, top-3 {x.get('dev_top3', '?')}); "
            f"changed {', '.join(x['ids'])}" for x in hist) + "\n"
    out_dir = os.path.join(le.RUNS, f"analyst_r{rnd}")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "proposal.json")
    with open(os.path.join(out_dir, "task.md"), "w", encoding="utf-8") as f:
        f.write(ANALYST_TASK.format(rnd=rnd, cap=cap, history=h, out=out, n=len(misses),
                                    misses=json.dumps(misses, indent=1, ensure_ascii=False), cat=_catalogue(lib)))
    print(f"{len(misses)} train misses -> {os.path.join(out_dir, 'task.md')}")


def _rebuild():
    for cmd in ("build", "validate"):
        p = subprocess.run([PY, os.path.join(HERE, "layout_tag.py"), cmd], capture_output=True, text=True,
                           encoding="utf-8", env={**os.environ, "PYTHONIOENCODING": "utf-8"})
        print(p.stdout.strip().splitlines()[-1] if p.stdout.strip() else p.stderr[-400:])


def apply(proposal, rnd):
    lib = lm.Matcher().lib
    prop = _load(proposal)
    cur = _load(NOTES, {"notes": {}, "history": []})
    os.makedirs(NOTES_HIST, exist_ok=True)
    with open(os.path.join(NOTES_HIST, f"before_r{rnd}.json"), "w", encoding="utf-8") as f:
        json.dump(cur, f, indent=1, ensure_ascii=False)
    ids = []
    for lid, n in prop.get("notes", {}).items():
        if lid not in lib:
            print("SKIPPED unknown id", lid)
            continue
        e = cur["notes"].setdefault(lid, {"was_use_when": lib[lid].get("use_when", ""),
                                          "was_dont_use_when": lib[lid].get("dont_use_when", "")})
        for k in ("use_when", "dont_use_when"):
            if n.get(k):
                e[k] = n[k].strip()
        e["round"], e["why"] = rnd, n.get("why", "")
        ids.append(lid)
    cur["history"].append({"round": rnd, "ids": ids, "result": "applied, not yet tested",
                           "suspect_labels": prop.get("suspect_labels", [])})
    with open(NOTES, "w", encoding="utf-8") as f:
        json.dump(cur, f, indent=1, ensure_ascii=False)
    print(f"round {rnd}: {len(ids)} layouts reworded: {', '.join(ids)}")
    _rebuild()


def verdict(rnd, result, dev):
    cur = _load(NOTES)
    for x in cur["history"]:
        if x["round"] == rnd:
            x["result"], x["dev_top1"], x["dev_top3"] = result, f"{dev['top1']:.0%}", f"{dev['top3']:.0%}"
    with open(NOTES, "w", encoding="utf-8") as f:
        json.dump(cur, f, indent=1, ensure_ascii=False)


def revert(rnd):
    src = os.path.join(NOTES_HIST, f"before_r{rnd}.json")
    hist = _load(NOTES)["history"]
    prev = _load(src)
    prev["history"] = hist                                   # keep the record that round N was tried and reverted
    with open(NOTES, "w", encoding="utf-8") as f:
        json.dump(prev, f, indent=1, ensure_ascii=False)
    print(f"round {rnd} reverted")
    _rebuild()


def notes():
    cur = _load(NOTES, {"notes": {}, "history": []})
    for x in cur["history"]:
        print(f"round {x['round']}: {x['result']} · {', '.join(x['ids'])}")
    for lid, n in cur["notes"].items():
        print(f"\n{lid} (round {n.get('round')}): {n.get('why', '')}")
        for k in ("use_when", "dont_use_when"):
            if n.get(k):
                print(f"  {k}: {n['was_' + k][:100]}\n    -> {n[k]}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    cmd = a[0] if a else ""

    def opt(k, d):
        return a[a.index(k) + 1] if k in a else d
    if cmd == "judge-prep":
        judge_prep(int(opt("--batches", 4)), int(opt("--judges", 3)), opt("--out", "judge"), opt("--scope", "all"))
    elif cmd == "consensus":
        consensus(int(opt("--audit", 20)), opt("--out", "judge"), int(opt("--reject-audit", 0)))
    elif cmd == "analyst-prep" and "--round" in a:
        analyst_prep([x for x in a[1:a.index("--round")]], int(opt("--round", 1)))
    elif cmd == "apply" and len(a) > 1 and "--round" in a:
        apply(a[1], int(opt("--round", 1)))
    elif cmd == "verdict" and "--round" in a:
        verdict(int(opt("--round", 1)), opt("--result", "kept"), _load(opt("--dev", "")))
    elif cmd == "revert" and "--round" in a:
        revert(int(opt("--round", 1)))
    elif cmd == "notes":
        notes()
    else:
        sys.exit(__doc__)
