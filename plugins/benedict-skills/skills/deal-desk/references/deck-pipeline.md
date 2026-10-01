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
Add to each block in `topics.json`: `"pick"`, `"alts"` (2 ids) and `"why"` (one line). Usually the top match; override when the sheet or the message says otherwise (e.g. a framing strip of bullets over a table). Then:
```
python scripts/layout_match.py plan topics.json
```
- Prints the plan table (slide · section · message · layouts, lead first · alternatives · why). A pick outside the top 5 is marked `*`; justify it.
- Errors (exit 1): missing pick, unknown id. Warnings: items out of the layout's range, 3+ bullet blocks, a slide with no visual, the same lead layout on two slides in a row, no visual layout in the deck. Fix all of them.
- **Show him the table and get his OK.** He can swap any block to one of its alternatives.

## 4. Build and QA
- Build with `ibdeck.py`: fill library layouts with `d.layout(s, "<id>", variant, box, data={...})`; code the rest with the matching `Deck` component.
- Read every number from the model or a cited source.
- `save()`: no `LAYOUT WARNING`, `AI TELL`, `SPARSE` or `THIN ARGUMENT`.
- `office.py render deck.pptx <dir>` → look at every PNG. `office.py density <dir>` → every slide ≥ 0.70.
- Then `qa-checklist.md` → Deck.

## Check it worked (SG DC rebuild, 2 Oct 2026)
- Matcher vs the hand-built deck: top-1 32/36 blocks, top-3 33/36. Misses: stat_strip vs stat_icons, bar vs column (same chart turned sideways), and one framing strip overridden at select.
- Rebuilt deck: density median 0.82 (original 0.81), all slides ≥ 0.70, lint clean.
