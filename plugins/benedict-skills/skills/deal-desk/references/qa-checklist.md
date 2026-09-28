# QA before anything is handed over

## Model
- [ ] Read `lessons.md` before building; every rule there is met
- [ ] `model_lint.py file.xlsx` shows **0 violations** (header band, Arial, colour code, input fills, heat maps, no numbers inside formulas, Excel 2016)
- [ ] `office.py preview` on every sheet (use `Sheet!A1:T60` for wide ones), and **look at every PNG**: no cut-off labels, sensitivities centred on the base case with heat maps, S&U aligned, outputs boxed (not filled)
- [ ] `office.py recalc file.xlsx` returns `"status": "success"`: zero #REF!/#DIV/0!/#VALUE!/#NAME?/#N/A, no circular references
- [ ] The Checks sheet total = 0 (sources = uses, balance sheet balances, cash ≥ minimum, debt ≥ 0 and repaid, NPV at IRR = 0)
- [ ] Key outputs cross-checked independently: the generators do this; for a hand-built model, recompute the IRR / EV in a few lines of Python from the model's own cash flows
- [ ] No hard-codes in the calculation rows (scan: a number typed inside a formula, or a blue value outside Inputs). Use `financial-analysis:audit-xls` for a full pass
- [ ] Colour code applied; units in column C; signs consistent (costs negative or positive, never mixed in one block)
- [ ] Sensitivity tables move on **both** axes; the base cell sits in the centre and equals the model output; green = better
- [ ] Only Excel-2016-safe functions (no MINIFS/MAXIFS/XLOOKUP/LET/IFS/dynamic arrays)
- [ ] Question tags on each answer when the test numbers its questions; assumptions listed on the Cover
- [ ] Saved under the name the firm asked for (default `Benedict Toh – <Firm> <Test>.xlsx`)

## Deck
- [ ] Every number is read from the model (script) or a cited source, and `financial-analysis:ib-check-deck` finds no mismatches
- [ ] **No stale facts:** search for news dated after the newest source (tender results, deals, guidance, rule changes) and update the deck; the SG DC deck missed the Aug 2026 DC-CFA2 awards until QC
- [ ] **Density:** `save()` prints no `SPARSE`; `office.py density deck.pptx` shows every slide ≥ 0.70 fill, no empty band; the page follows the reference chosen in `slide-layouts.md` → Which reference to use
- [ ] ib-check-deck's number script groups all % values together: treat its flags as prompts and check each against its source by hand
- [ ] `save()` printed no LAYOUT WARNING; `office.py render deck.pptx <dir>`, then **look at every PNG**: no overflow, no overlap, nothing cut off, charts readable
- [ ] `save()` printed no `AI TELL`: no accent-bar cards (thin strip plus pale box, any colour), no two slides in a row with the same body layout, at least one visual layout, at most 2 bullet blocks per slide
- [ ] The layout plan (slide → message → layout from `slide-layouts.md`) was shown before building
- [ ] Main header = the contents section (20pt navy); subheader = one line (16pt grey); only 20 / 16 / 12 / 10 sizes, with Sources / Notes on two lines, 8pt italic
- [ ] No shadows or glows on lines or shapes; table of contents (filled navy / light-navy table, full width, flush to the bottom) with the page number just right of it; body text black (grey only for sources, page number, subheader); no confidentiality line
- [ ] Palette only (navy ramp + greys); gold on at most one item per slide
- [ ] Every row of blocks is aligned (same header height; bottoms level where possible); sensitivity tables use the model's red / white / green heat map with the base case boxed
- [ ] Tables: no filled table header right under a filled header bar (bold black headers + navy rule instead); numbers right-aligned, totals bold; units stated once per block
- [ ] Spelling and names (firm, target, people) checked against the brief
- [ ] **Argument blocks argue (lessons #35):** thesis opens with a "Why invest" line; each pillar is a bold claim + evidence → so what → "For returns:"; each risk is quantified where possible and each mitigant says how it works and "What remains:"; `save()` printed no `THIN ARGUMENT`; no contractions

## Defence sheet (for every case and every real deliverable)
10 likely follow-up questions. For each, the answer in 1–2 sentences and the model cell that proves it. Save it as `Defence – <Firm>.md` next to the deliverable.
