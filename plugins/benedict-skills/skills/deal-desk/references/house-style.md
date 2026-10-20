# House style: classic IB, navy ramp + greys + one gold highlight

Use this unless a firm template or a case brief says otherwise. At work, the firm's template always wins: turn it into a style with `financial-analysis:ppt-template-creator` and pass it to `Deck(template=...)`.

## Slides (`scripts/ibdeck.py`)
- **Format:** 16:9 (13.33 × 7.5 in), Arial throughout (safe on every PC, so the text renders the same on the grader's machine).
- **Colours:** one hue in six shades, greys, and one muted accent. Finance decks use a primary colour in 3–6 shades plus greys, with at most one accent used sparingly ([Deckary](https://deckary.com/blog/powerpoint-color-schemes), [Art of Presentations](https://artofpresentations.com/monochromatic-color-scheme-for-powerpoint/), [Darien Group](https://www.dariengroup.com/insights/color-beyond-navy-how-to-build-a-distinct-palette)).

  | Role | Hex |
  |---|---|
  | Navy ramp, deep → near-white (`NAVY_RAMP`) | `0B1F3A` · `1F3864` (main) · `2F5597` · `5B7DB8` · `9DB4D8` · `DCE5F1` |
  | Greys | `404040` (secondary text) · `7F7F7F` (subheader, labels) · `BFBFBF` (lines) · `EDEDED` (ring remainder, pale cells) |
  | Gold accent (`GOLD`) | `B08D3F`: **one highlight per slide only** (the target in a peer chart, the base case, "today" on a timeline), never a large fill |

  - Series step through the ramp: `1F3864`, `5B7DB8`, `9DB4D8`, `BFBFBF`
  - Nested or stacked shapes use light → dark shades (TAM `9DB4D8`, SAM `5B7DB8`, SOM `1F3864`)
- **Slide header:**
  - **Main header** (navy, 20pt bold): the contents section the slide belongs to, e.g. "Company Overview" or "Industry Overview"
  - **Subheader** (grey `7F7F7F`, 16pt): a few words introducing the slide
  - Each is one line and at most one sentence; `lint()` flags anything longer
- **Font sizes (max 4 per slide):**
  - 20: main header
  - 16: subheader
  - 12: block header bars, the contents bar, and big key numbers (bold)
  - 10: all other text (body, tables, charts, labels, pills, tabs)
  - Sources / Notes and the page number are always 8pt; Sources / Notes are also italic
- **Every content slide has:**
  - the header and subheader, then the navy title rule
  - Sources / Notes on two lines: "Sources: …", then "Notes: …"
  - a table of contents flush to the bottom (`Deck(sections=[...])`): a real one-row table, the same width as the title rule, 12pt bold white text, white separators; current section solid navy `1F3864`, the others the same navy at 50% transparency
  - a page number (8pt) on the same row, just right of the table
- **Text colour:** body text, labels, key numbers (bold, incl. ring %, TAM/SAM/SOM values), pill labels, Harvey column headers, table and chart text are **black**. Navy text is only for slide headers and the highlighted name tile. Grey is only for footnote-type text (Sources / Notes, the page number, the subheader) and the italic % rows in financials (fin_table % rows, fin_chart strip).
- **Outlines:** name tiles are outlined in navy `1F3864` (the highlighted one in gold); nested circles (TAM / SAM / SOM) have no outline and white tags
- **Financials on slides** follow real bank board books (see `assets/references/bank-financials/`):
  - **Table** (`fin_table()`) when readers need the line items: units once in the header bar ("P&L summary ($m)"); header row = periods with A/E ("Y0A", "2025E"), bold black, no fill, navy rule under; key lines bold with "$"; every row white fill (no bands); "% Growth" / "% Margin" rows italic, grey (`7F7F7F`) and indented under their line; Arial 10 in every cell, same row height; negatives in brackets
  - **Chart** (`fin_chart()`) when the point is the trend: navy columns with values on top, bold CAGR label with an arrow, dashed line where forecasts start, italic grey % strip centred under the bars
  - Never put units in column headers ("$m", "% of revenue"); lint flags it
- **Sensitivity tables on slides** look exactly like the model's (`heatmap()` uses the same colours as `xlstyle.heat_map`): red `F8696B` (worst), white at the median, green `63BE7B` (best; `better="low"` flips for costs); axis row and column unfilled with black rules; base case bold, boxed in black
- **Alignment:** blocks in the same row start at the same height (use one `ROW2`-style constant per slide) and, where possible, end at the same height. `lint()` flags block headers on one slide that are less than 1in apart vertically but not level
- **Side tabs** are a real 2-column table: navy label cells (white bold 10pt caps) split by thick white rules; white content cells, text centred, thin grey rule under each row
- **Pill labels:** 12pt black, first line bold, sub-line regular. **Hub-and-spoke labels:** centred
  - no confidentiality line
- **Lines and shapes:** plain and solid. No shadows, glows, gradients or 3-D. `_flat()` strips the theme shadow python-pptx adds, and `lint()` flags any that remain.
- **Layouts:** plan every deck with `slide-layouts.md` (slide → message → layout). Vary the body layout from slide to slide; the chrome stays fixed.
- **Block headers:** filled navy bar, white bold centred text (`header()`). The thin-rule style (`style="rule"`) is only for dense sub-blocks.
- **Never the accent-bar card:** no thin coloured strip on the side or top of a pale box, in any colour or role. Key numbers go in `stat_icons` / `stat_strip` / `hero_number` / `stat_rings`; the "so what" goes in a dashed `takeaway()`.
- **Icons:** Tabler line icons (MIT licence, `assets/icons/`, list with `Deck.icons()`), always navy (grey for "off" states). Use an icon only when it names the number or item beside it.
- **Density (bank standard, lessons #32).** Measured on 400 pages of 14 real bank decks (SEC filings in `01. IB PE\Investment Banking Library\Real IB-PE Decks\`): body fill median 0.75, no empty bands; market pages 0.83–0.93. The old "2–3 blocks, ≤5 bullets" rule produced a 0.49-fill deck.
  - Every content slide has at least one **exhibit** (chart, table, map / photo, logo wall, timeline, infographic) **plus commentary that carries numbers**
  - 3–5 blocks per slide. Market / overview slides carry 2–3 exhibits side by side, each with a header bar, a bold one-line finding above it (`exhibit_takeaway()`) and its units
  - Text blocks: bold lead-in bullets, one number in each; up to ~6–8 per block, or full-width two-level bullets (`bullets([... ("sub-point", 1)])`) on a text page. **This rule is for data and market commentary only, not for argument blocks** (below)
- **Argument blocks (lessons #35):** investment thesis, key considerations, recommendations, "why now", risks and mitigants must explain, not list.
  - Thesis page: a dashed `takeaway()` "**Why invest:** …" line on top (the pitch in one or two sentences), then `side_tabs` with `(claim, text)` rows. Name pillars as return drivers (secure income, rising rents, build-to-core, liquid exit), not market facts
  - Each pillar: bold one-line claim, then 2–3 sentences: evidence with numbers → why it matters → "**For returns:** …". About 45–60 words
  - Each risk: bold short title + 1–2 sentences on what could go wrong and how it hurts returns, quantified where a source allows. Each mitigant: bold action + how it works + "**What remains:** …". About 25–35 words a cell
  - Own calculations (e.g. value change between cap rates) are fine if the inputs are sourced; say so in Notes
  - Too long for one slide at 10pt → a thesis slide and a risks slide, each with its own exhibit or stat strip. Never shrink below 10pt
  - No contractions in slide text (cannot, does not)
  - `lint()` flags `THIN ARGUMENT`: a pillar under 35 words, a risk / mitigant cell under 15, or fact-list tabs under a thesis-type header
  - 120+ body words (banks' median 123; Qatalyst pitch book 224); a logo counts as a name
  - A pure text page needs no exhibit if it carries 200+ words in full-height columns (GS PowerSchool p3 fills 0.88); close it with a stat strip rather than leave a band
  - Blocks run to the bottom of the body: no floating boxes, no empty band over ~0.8in. Close a short column with a dashed `takeaway()` "so what"
  - Photos, maps and logos are welcome when they sit beside the fact they support: `fetch_image.py` (Wikimedia, credit logged) → `photo()` / `logo_row(logos=...)` / `pin()` for map labels
  - At most 2 bullet blocks per slide (lint); turn a third into a table or stat strip
- **Charts** (native, editable):
  - Data labels on, value axis hidden, no gridlines
  - Units go in the header ("Revenue and EBITDA ($m)")
- **Tables:** one filled band per block, never two stacked. Under a navy header bar (the usual case), column headers are bold black on white with a navy rule underneath; `table()` does this automatically. A navy header row is only for a table standing alone with no bar above. Thin grey row rules, numbers right-aligned, totals bold with a rule above. Real pages: BofA Taro p11, Citi Chindata p5, Evercore Diversey p50 (lessons #34).
- **Numbers:**
  - `$75.0m`, `18.5%`, `4.9x`; one decimal unless precision matters
  - Same units across a slide
  - Every number is read from the model file, never typed (see `assets/examples/keppel_slides_v3.py`)
- **Components:**
  - Frame: `slide`, `grid`, `header`, `footer`, `section_tracker`, `divider`, `title_slide`
  - Numbers: `stat_icons`, `stat_strip` (old `kpis` maps here), `hero_number`, `stat_rings`, `pictogram`, `tam_sam_som`
  - Images: `photo` (crop-to-fill, credit added to Sources), `logo_row(logos=..., outline=False)` (logo wall), `pin` (map labels), `exhibit_takeaway`
  - Structure: `side_tabs`, `pill_rows`, `chevrons`, `timeline`, `numbered_steps`, `hub_spoke`, `pros_cons`, `risk_matrix`, `harvey`, `logo_row`
  - Data: `table`, `heatmap` (sensitivities), `column` / `bar` / `stacked` / `line`, `football_field`
  - Text: `bullets`, `takeaway` (old `callout` maps here), `icon`
- **Before handing over:**
  - `save()` runs `lint()`: `LAYOUT WARNING` for anything past the footer line or the right margin, `AI TELL` for accent-bar cards, repeated layouts, a deck with no visual layout, bullet walls, shadows, font sizes outside 20/16/12/10/8, or headers longer than one line, and `SPARSE` for a slide with no exhibit, under 120 body words or an empty band. All must be empty
  - Then run `office.py density deck.pptx`: every slide ≥ 0.70 fill with no empty band, deck median ~0.80 (it renders the PNGs too)
  - **Look at every PNG**: tables grow when text wraps; chart labels rotate when categories are long (use `bar()`)

## Excel (`scripts/xlstyle.py`, house style v2; rules and their sources in `lessons.md`)
- **Colour code** (Benedict's rules, enforced by `model_lint.py`):

  | What | Look |
  |---|---|
  | Hardcode / typed number | blue `0000FF` |
  | Pure link to another sheet | green `008000` |
  | Formula | black |
  | Link to another workbook | red `FF0000` |
  | Assumption / input cell | blue on `FFFFCC` with a hair box (`input_cell()`) |

  Solver-pasted values are inputs too (yellow, with a "<<" note). Nothing else gets a fill except bars, the band, and grey N/A cells (`na_cell()`).
- **Top of every sheet:** the navy header band (`sheet_header()`): case name (bold), sheet purpose, then the timeline rows inside the band (Financial year / Actual–Forecast, or Quarter ending / Year / Phase) and the Units / Input (or Value) headers. Freeze panes under it. **Never** a big title + subtitle.
- **Grid (same on every sheet):**
  - A: an "x" marker on each section (Ctrl+↓ navigation)
  - B: labels
  - C: units (grey italic)
  - D/E: constants (inputs or single answers)
  - F onwards: periods
  - "<<" notes in grey italic to the right
  - Sheets end with an "End" bar
- **Bars:** `part()` = navy (main parts); `section()` = light grey `D9D9D9`, bold black, with the question tag when the test numbers its questions ("Part I (b) – FCFF and FCFE"); `subsection()` = pale blue.
- **Rows:**
  - One line item per row, with the same formula across it
  - Totals bold with a thin top rule; grand totals (net profit, FCFF/FCFE) with a double underline
  - Margins and growth in italic, indented
- **Key answers:** `output_box()` = bold with a thin box, **no fill**
- **Sensitivities** (`sensitivity()`, one call per table):
  - real Excel data table; 5×5 on its own uniform columns, next to the labels
  - output linked in the corner; column title centred above; row title to the left
  - **base case exactly in the centre, bold and boxed** (the build fails otherwise); symmetric steps
  - 3-colour heat map with **green = better** (`better="low"` for costs)
  - the input cells must be on the same sheet (use blank override cells, as in `build_lbo.py`)
- **Sources & Uses** (`sources_uses()`): stacked Sources table then Uses table; navy header ($ · % of total · x EBITDA); plug noted; totals double-ruled; Sources = Uses on Checks.
- **Formats:** `#,##0_);(#,##0);"–"_)` money · `0.0%` · `0.00"x"` · negatives in brackets · checks `[>=0.0005]0.000;[<=-0.0005](0.000);"OK"`. Arial 10 everywhere (`workbook_defaults()` also sets empty cells).
- **Structure:**
  - Cover (contents, colour key, boxed key outputs, assumptions log, style version) → Inputs → calculations → Dashboard / answers → Checks
  - PF: Timing → Construction → Operations → Debt → Waterfall → Annual → Returns → Scenarios
- **Formulas:**
  - Every number that isn't an input is a formula
  - **No number typed inside a formula**, except 0, 1, 3, 4, 12, 100, 1000, 365, 8760 and 0.5. Hours and unit conversions are inputs.
  - No circular references: use opening balances, closed forms, or a solver-and-paste with a check. Remember Excel flags a loop by formula *links*, even inside an unused IF branch.
- **Compatibility:** Excel 2016. **Don't use** MINIFS, MAXIFS, IFS, SWITCH, XLOOKUP, LET, FILTER, UNIQUE, SORT, SEQUENCE, TEXTJOIN, CONCAT or dynamic arrays. For a conditional minimum, return "" outside the window and use MIN (it ignores text); otherwise INDEX/MATCH, SUMIFS, AVERAGEIFS.
- **Before handing over:**
  - `model_lint.py` shows 0
  - `office.py preview` on every sheet (`"Sheet!A1:T60"` for wide ones), and look at every PNG
