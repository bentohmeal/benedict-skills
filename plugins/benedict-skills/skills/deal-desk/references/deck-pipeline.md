# Deck pipeline: research → slide plan → build

Use this for every deck (case study, sector overview, firm deck from a dossier). It replaces the hand-picked slide plan: the matcher shortlists layouts from `assets/layout_library.json`, scored against the real bank pages, and you choose from the shortlist.

Read `slide-layouts.md` (house rules) and `lessons.md` first.

## 1. Chunk: research → `topics.json`
One topic is one slide. One block is one exhibit on that slide.

- **Topic:** `slide`, `section` (cover, exec_summary, company, market, thesis, financials, valuation, returns, structure, risks, process, recommendation, appendix), `message` (the subheader: one line, the slide's point, not its subject).
- **Block:** `what` (block header), `data_type` (kpi_set, time_series, comparison, composition, range, bridge, process, cycle, list, text, matrix, relationship, hierarchy, geography, icons), `about` (a few words on what it covers), `content` (the actual lines from the research, one per item).
- **Rules:**
  - The **first block is the lead exhibit**. It sets the slide's layout and is what the "same layout twice in a row" check looks at.
  - 2–4 blocks per slide. Aim for one visual block (chart, stats, map, timeline) per slide; at most 2 bullet blocks.
  - Add `"unit": "MW"` (or `US$bn`, `%`…) **only when every item is the same measure**. This marks the block as chartable; without it, numbers go to a table or stats.
  - **12+ items:** split into one block per group (e.g. 20 players → hyperscalers / colos / REITs).
  - Dates are not numbers: "Aug 2026: DC-CFA2 awards" is a dated item and leans to a timeline.
  - Names with no detail (logos, buyers, sponsors) lean to `logo_row`.

```json
{"deck": "Singapore Data Centres", "topics": [
  {"slide": 1, "section": "market", "message": "Asia's premium data centre hub, over 95% occupancy",
   "blocks": [
     {"what": "Key market metrics", "data_type": "kpi_set", "about": "live MW, occupancy, rent, power share",
      "content": ["821MW live capacity", ">95% occupancy", "US$330-475 per kW a month"]},
     {"what": "Live capacity vs APAC peers", "data_type": "comparison", "unit": "MW",
      "content": ["Shanghai 1,286", "Tokyo 1,086", "Singapore 821"]}]}]}
```

## 2. Match: shortlist per block
```
python scripts/layout_match.py match topics.json [k]
```
- Gives k (default 5) candidates per block, scored on data-type fit, section, item count, numbers, text capacity, use_when / dont_use_when, and how often real banks use that layout in that section.
- Writes `<stem>_match/slideNN.png` (a thumbnail of each candidate plus the closest real bank page) and `candidates.json`. **Look at the sheets** before choosing.
- A whole-page recipe (e.g. `page_overview`) is offered per slide when it fits the section and message.

## 3. Select: pick, give a reason, keep 2 alternatives
First read `assets/eval/examples.md` (reviewed layout choices, grouped by data type) and follow its precedents unless the block differs.
Add to each block in `topics.json`: `"pick"`, `"alts"` (2 ids) and `"why"` (one line). Usually the top match; override when the sheet or the message says otherwise (e.g. a framing strip of bullets over a table). Then:
```
python scripts/layout_match.py plan topics.json
```
- Prints the plan table (slide · section · message · layouts, lead first · alternatives · why). A pick outside the top 5 is marked `*`; justify it.
- Errors (exit 1): missing pick, unknown id. Warnings: items out of the layout's range, 3+ bullet blocks, a slide with no visual, the same lead layout on two slides in a row, no visual layout in the deck. Fix all of them.
- **Show him the table and get his OK.** He can swap any block to one of its alternatives.
- **Once he OKs it, log the plan:** on any block he swapped, set `"swapped_from": "<old pick>"`, then
  `python scripts/layout_eval.py add-plan topics.json --source "<deck name>" --approved`.
  Each block becomes an accepted row in the golden set; swaps go to `assets/eval/swaps.md` (lessons loop).

## 4. Build and QA
- Build with `ibdeck.py`: fill library layouts with `d.layout(s, "<id>", variant, box, data={...})`; code the rest with the matching `Deck` component.
- Read every number from the model or a cited source.
- `save()`: no `LAYOUT WARNING`, `AI TELL`, `SPARSE` or `THIN ARGUMENT`.
- `office.py render deck.pptx <dir>` → look at every PNG. `office.py density <dir>` → every slide ≥ 0.70.
- Then `qa-checklist.md` → Deck.

## Check it worked (SG DC rebuild, 2 Oct 2026)
- Matcher vs the hand-built deck: top-1 32/36 blocks, top-3 33/36. Misses: stat_strip vs stat_icons, bar vs column (same chart turned sideways), and one framing strip overridden at select.
- Rebuilt deck: density median 0.82 (original 0.81), all slides ≥ 0.70, lint clean.

## Eval: is the layout choice getting better?
`scripts/layout_eval.py` keeps a golden set (`assets/eval/golden.jsonl`) of blocks with the right layout, and scores the matcher and a blind selector against it.
- **Sources:** real bank pages (the bank's layout is the label; page text OCR'd and chunked blind), past worked cases (SG DC hand-built deck), and every approved plan (above).
- **His review:** `layout_eval.py review` writes `output\_Deal Desk Toolkit\golden_review.xlsx`. Each row shows the source page and pictures of 3 picks: the top pick and 2 runner-ups (labelled against the full menu: components, page recipes, bank designs, infographics). He picks a Decision: `top` / `alt 1` / `alt 2` (that pick is right) / `other` (none fit; choose the id in Other id) / `reject` (row itself broken: garbled, not an exhibit). "Others also OK?" = no drops the other picks from the acceptable list. A Guide tab explains this; a Layouts tab lists every id with name, kind, data type and use when. Re-running review keeps his decisions and refuses while the file is open in Excel; `layout_eval.py ingest` reads it back (chosen pick → label; changes from the top pick go to `swaps.md`). Only reviewed rows count; `--all` gives a provisional score that includes pending rows.
- **Infographic test rows** (`ig_t_*`): 40 written blocks (cycle, funnel, pyramid, maps, gauges, Harvey, radar…) so infographic choices are tested too; real bank pages rarely use them.
- **Split:** a hash of the row id puts 1 in 5 rows in a fixed hold-out. `layout_eval.py examples` writes the other 80% to `assets/eval/examples.md` (the few-shot list for step 3). Hold-out rows never appear in prompts.
- **Score:**
  - `layout_eval.py matcher`: top-1 / top-3 of `layout_match.py` on the hold-out. Seconds, no tokens.
  - `layout_eval.py blind` → `assets/eval/runs/<stamp>/task.md` (pipeline rules + catalogue + train examples + hold-out blocks, no labels). Give it to a subagent that sees only that file; it writes `answers.json`. Then `layout_eval.py score <answers.json>`: top-1, top-3 (pick or alternatives) and a reasoning check (names the content shape; the pick doesn't break its own "don't use when").
  - Both append to `assets/eval/scores.md`.
- **Rule:** run `matcher` (and `blind` for prompt changes) before and after any change to `layout_match.py`, `layout_library.json`, this file or `examples.md`. Keep the change only if top-1 and top-3 don't drop.
- **Self-improving loop** (`scripts/layout_loop.py`, so he does not check every row):
  1. **Judges set the answers.** `judge-prep` builds one contact sheet per row (the real page + shuffled candidate layout pictures) and 4 batches × 3 judge tasks. Three Opus subagents answer alone. `consensus`: a majority id the third judge also accepts → `silver` (counts like accepted). Otherwise → `pending` for his review. A random 20 silver rows are flagged `audit` as his spot check.
  2. **His review shrinks** to the split rows + the 20 spot checks (the review sheet's Check column says which). `ingest` prints judges-vs-him agreement on the spot checks: under 90% means fix the judge step before trusting a score.
  3. **Rounds (max 3):** testers on `blind --set train-a`, `train-b` and `dev` (one subagent each; the train halves use each other as examples) → `analyst-prep <train run dirs> --round N` → an analyst subagent rewrites `use_when` / `dont_use_when` for ≤ 8 layouts (patterns only, no deal names; suspected wrong answers are listed, not fitted) → `apply proposal.json --round N` (writes `assets/eval/layout_notes.json`, rebuilds the library) → re-test dev. Keep if dev top-1 and top-3 don't drop and one rises; else `revert --round N`. `verdict` records it.
  4. **Final (hold-out)** is scored before round 1 and once after the last kept round. The analyst never sees dev or final rows.
  - `layout_loop.py notes` lists every wording change with the old text. The changes apply to the matcher and to real deck builds (both read the library).
  - Rows the analyst lists in `suspect_labels` get a `suspect` field (the tester's pick + why) and go into his review as "tester disagrees", with the tester's pick shown as alt 1. Never reword a layout to fit them.
  - **First run (2 Oct 2026):** round 1 kept (dev 85→90% top-1, 100% top-3), round 2 reverted (dev 88%; its bk07 rewording caused a new miss), stopped (dev headroom = 4 rows ≈ noise). Hold-out blind 83/96 → 87/98, reasoning 91 → 88; matcher hold-out 45/66 → 43/66 (one row, wording only steers the blind selector).
- **Lessons loop:** the same swap twice in `swaps.md` → add a `dont_use_when` line to the losing layout in `layout_tag.py`, rebuild the library, re-run the eval.
