# Slide layouts: pick a shape for each message

Read this **before planning any deck**. First write the plan as a table (slide → one-line message → body layout), show it to Benedict, then build. See every layout rendered in `Claude Things\output\_Deal Desk Toolkit\Deck Layout Gallery.pptx` (rebuild it with `scripts/layout_gallery.py`). A worked before/after: Keppel V2 vs V3 in `Interview Prep\Case Studies\_Worked examples\Keppel Tough Love\`.

## Which reference to use (decide per slide, before laying it out)
1. **The look:** the firm's template or brief wins (case tests, work decks); otherwise the house style. References never change the palette or fonts.
   - **Quality bar:** only real bank / PE-firm decks set how a page looks (`Real IB-PE Decks`; Pantheon for PE-specific pages). Case tests, student and competition decks in `Slide Inspiration\` never do.
2. **The page structure:** pick by what the slide *is*, in this order:

| Slide / deck type | First look at | Then | Why |
|---|---|---|---|
| Case test or recruiting deck | `Real IB-PE Decks\_Index.md` for how each page looks | The brief (and any firm sample it includes) for what the deck must cover | Graders reward bank-quality pages; the brief sets scope, not style |
| Banker pages: exec summary, situation overview, valuation, comps, precedents, football field, premiums, process, buyer universe | `Real IB-PE Decks\_Index.md`, best page for that section | `assets/references/bank-financials/` for financial tables | 126 real SEC-filed bank decks; strongest on exactly these pages |
| Industry / market overview | Hand-picked market pages in `_Index.md` (Qatalyst p4) + the Dense Pages in the gallery | The sector's own investor decks (e.g. Keppel DC REIT for data centres) | The library has few market pages; issuer decks show which metrics that industry reports (MW, WALE, reversion...) |
| PE / private-markets deck (IC memo, fund, portfolio review) | `Real IB-PE Decks` for structure and density | Pantheon's decks in `Slide Inspiration\` (a real PE firm) for PE-specific pages: fund terms, portfolio, market update | The library has no PE IC decks; Pantheon fills that gap without lowering the bar |
| A shape the coded layouts lack (cycle, pyramid, funnel, map) | Infographic Library | — | Real PwC objects, restyled |

3. **The numbers:** the model first, then primary sources (filings, regulators, company releases), then research houses (CBRE, JLL...), then press. Press-only figures are cited as such ("The Real Deal citing CBRE"). Before handing over, search for news after the newest source date (tender results, deals, guidance) so nothing is stale.
4. **Every page, whatever the reference:** the density standard (Rule 0) applies.

Gallery: `output\_Deal Desk Toolkit\Deck Layout Gallery.pptx` → the **Dense Pages** section shows six full-page recipes, built by `scripts/layout_gallery.py`. Worked example: `assets/examples/sg_dc_slides.py` → `output\Singapore Data Centres Sector Overview.pptx`.

## Dense page recipes (copied from real bank pages)
| Recipe | Build | Real page |
|---|---|---|
| Framing strip + 3 exhibits (market page) | two header bars with 2 bullets each and an arrow between; below, 3 columns of header + `exhibit_takeaway` + chart / table | Qatalyst Autonomy p4; Gallery: Dense Pages 1 |
| Photo + fact strip + chart | photo and bullets on the left; `stat_icons` across the top right; chart + bullets below | Gallery: Dense Pages 2; SG DC deck slide 1 |
| Map + comparison table | `photo(map)` + `pin()` labels on the left; comparison table and bullets on the right | Gallery: Dense Pages 3; SG DC deck slide 4 |
| Logo wall by segment + chart | a header bar per segment with a one-line role under it; `logo_row(logos=…, outline=False, cols=1–2)`; chart + bullets on the right | Qatalyst Autonomy p8; Gallery: Dense Pages 4 |
| Full-width table + chart + takeaways | table across the top (units in the header bar); bar chart and bullets below | Evercore Diversey p8; Gallery: Dense Pages 5 |
| Full-width two-level text | framing box, then bold lead bullets with 3–5 dash sub-points, each with a number (~250 words) | GS PowerSchool p3; Gallery: Dense Pages 6 |
| Thesis page | dashed "Why invest" `takeaway` on top; `side_tabs` with (claim, text) rows left; "Return drivers in numbers" `stat_icons` (2 cols) right | SG DC deck slide 10; Gallery: Thesis |
| Risks page | full-width `risk_matrix` with (title, text) cells and Harvey balls; `stat_strip` of the risk numbers underneath | SG DC deck slide 11; Gallery: Risks |

## Rules
0. **Fill the page (lessons #32).** At least one exhibit plus numbered commentary per slide; blocks run to the bottom; `lint()` SPARSE and `office.py density` must pass (see `house-style.md` → Density).
1. **Fixed chrome, varied body.** Title, rule, section tag, source line, page number and header bars sit in the same place on every slide. Banks insist on that consistency. The **body layout changes** to fit the message.
2. **No two slides in a row share a body layout.** `lint()` flags it.
3. **At least one visual layout per deck** (icons, rings, pills, side tabs, chevrons, timeline, hub, Harvey balls). An all charts + tables + bullets deck looks basic.
4. **One message per slide.** The main header names the contents section (e.g. "Company Overview"). The subheader introduces the slide in a few words, on one line. The numbers and the "so what" go in the body.
5. **Numbers never sit in boxed tiles.** Show them with icons, a stat strip, rings or one hero number.
6. **Header bars are filled navy** (`header()`). Keep the thin-rule style (`style="rule"`) for dense sub-blocks only.
7. **Palette:** navy ramp + greys (see `house-style.md`). Use shades for layers and series. **Gold marks one item per slide** (the target, the base case); everything else stays navy or grey.
8. **Four font sizes:** 20 header / 16 subheader / 12 header bars, contents bar and key numbers / 10 everything else. Sources are 8pt italic.
9. **Plain lines:** no shadows or glows on any line or shape.

## Tells to avoid (these make a deck look Claude-made)
| Tell | Why it reads as AI | Use instead |
|---|---|---|
| **Accent-bar card:** a thin coloured strip down the side or across the top of a pale filled box, in any colour, used as a KPI tile, callout or quote | Claude's default card, reused in every deck with only the colours changed | `stat_icons`, `stat_strip`, `hero_number`, or `takeaway` (dashed outline) |
| The same grid (3 equal columns: header, chart, bullets) on every slide | Template feel; nothing adapts to the content | Pick from the catalogue below and vary it |
| ■ square bullets, and walls of bullets (3+ bullet blocks on a slide) | Unedited AI output | `side_tabs`, `pill_rows`, `numbered_steps`, `pros_cons`, a table |
| A thin rule under every block header | Looks unfinished next to real bank decks | Filled navy header bars |
| Decorative icons with no meaning | Clip-art feel | An icon only where it names the number or item next to it |
| Shadows, glows or a gradient "aura" on lines and shapes | python-pptx's default theme style; looks cheap | `_line()` / `_shape()` (flat, solid) |
| Many font sizes on one slide | Looks unplanned | 20 / 16 / 12 / 10, plus 8 italic for sources |
| Two filled bands stacked: a navy header bar with a navy table header row right under it | Heavy and templated; no real bank page does it | Keep the bar; table column headers bold black with a navy rule (`table()` auto) |

`lint()` (run by `save()`) prints `AI TELL:` lines for all of these except decorative icons. Treat them like layout warnings: fix them before handing over.

## Catalogue: message → layout options
Inspiration files are in `01. IB PE\Investment Banking Library\Slide Inspiration\` (slide numbers in brackets). "Seen in" records where a layout was first spotted. **The case tests and student decks there (Favour test, Tesla, FMI, CRFA, strategy projects…) are not style references:** Benedict judged them below the Real IB-PE Decks (27 Sep 2026). Take page structure and polish from `Real IB-PE Decks` only.

| Content | Layout options (ibdeck call) | Seen in |
|---|---|---|
| **Key numbers / company at a glance** | `stat_icons` grid (icon, number, label) · `stat_strip` under a chart · `hero_number` with 2–3 support points · `pictogram` for a share | Favour test (3); Pantheon Korea (2); PwC pack (186) |
| **Shares, margins, mix** | `stat_rings` (% in the centre) · stacked column · `pictogram` | PwC (67, 68, 186); Sygnum pitch (22) |
| **Market sizing** | `tam_sam_som` nested circles · column chart with CAGR in the header | Favour (4); PwC (13, 15) |
| **Investment thesis / summary** | `side_tabs` with (claim, text) rows: bold claim + evidence → so what → "For returns:" (lessons #35), under a "Why invest" takeaway · `pill_rows` · numbered theses | Favour (2, 8); Pantheon (3); SG DC slide 10 |
| **Business overview / model** | `pill_rows` · `hub_spoke` (company in the centre) · icon row of segments | Pantheon (3, 9); PwC (47, 56) |
| **Peers / buyers / sponsors** | `logo_row` tiles (target highlighted) · bar chart with the target navy, the rest grey · `harvey` scoring grid | Keppel V3 (1); PwC (118) |
| **Growth drivers** | `hub_spoke` · icon row (`stat_icons` with text labels) · `chevrons` | Favour (6); SATS (6) |
| **Process / plan / 100-day plan** | `chevrons` · `numbered_steps` (down or across) | PwC (107–116, 124, 126); SATS value chain (5) |
| **History / milestones** | `timeline` (labels alternate above / below; highlight today) | PwC (129–131); Sygnum (19) |
| **Risks** | `risk_matrix` with (title, text) cells: risk = impact on returns, quantified; mitigant = action + "What remains:" (lessons #35); severity Harvey ball · `pros_cons` for strengths / watch-points | Favour (2); NSE (12, 13); SG DC slide 11 |
| **Financials** | `fin_chart` for the trend (CAGR, A/E split, % strip) · `fin_table` for line items (bank format; `assets/references/bank-financials/`) + `takeaway` · `hero_number` for the headline metric | Favour (9); Keppel V3 (2) |
| **Valuation / returns** | `football_field` · `heatmap` · `stat_strip` of EVs vs price · `hero_number` IRR | Keppel V3 (2); SATS (15) |
| **Funding / sources & uses** | S&U table · `stat_rings` for the debt / equity split | Keppel V3 (2) |
| **Recommendation** | `hero_number` (Buy / price / IRR) with `side_tabs` (claim, text) rows for the reasons · `takeaway` | SATS conclusion (16) |
| **Deck navigation** | `section_tracker(sections, current)` on every content slide | SATS, NSE, Sygnum decks |

## Infographic Library (PwC originals, restyled)
When a message needs a shape the coded layouts don't have, use the library:
- **Files:** `Claude Things\output\_Deal Desk Toolkit\Infographic Library.pptx`, numbered thumbnails in `…\_Deal Desk Toolkit\Infographic Library – index.pdf`, and `assets/infographic_index.json` (number → PwC slide, type, uses, picture flag).
- **What's in it:** 211 of PwC's Infographic Templates (2014) copied as the original objects. Tables are still tables, charts are still native charts with data, and groups and freeforms are editable.
- **What changed:** colours, fonts, sizes and shadows only (lessons #29).
- **Insert:** `d.infographic(s, no, box=(x, y, w, h), highlight=["IG Oval 12"])`. It scales into the box; `highlight` fills one shape gold.
- **After inserting:**
  - Edit the placeholder text ("Text", "[ ]") in place with real content.
  - Delete the sub-diagrams you don't need: most PwC slides show 2–5 variants side by side.
  - Render and look.

| Message | Library numbers |
|---|---|
| Process / deal steps / flow | Arrows 1–8 · linear flow 101–107 · process charts 108–115 · bottleneck / maze 98–100 |
| Overlap, synergies, strategic fit | Venn 9–10 |
| Pillars, segments, mix | Sections / pie sections 11–19 · sections and percentages 61–68 · hexagons / octagon 74–78 · petals 45–46 |
| Value creation loop, operating model | Cycles 20–28 and the other circular diagrams to 70 · cogs 89–92 |
| Scoring, utilisation, leverage vs covenant | Speedometers 57–58 · heat map 59 · circular bar chart 60 · spider / radar 79–80 · rating 184 · traffic lights 171 |
| Business model / ecosystem | Hub and spoke 70 · jigsaw 81–88 |
| Hierarchy, capital structure, priorities | Pyramids 71–73 · layers (icons in action) 172–190 |
| EBITDA / value bridge | Bridge (native chart) 93 · thermometer 94 · bar / line charts 95–97 |
| Pipeline / buyer funnel / TAM → SOM | Funnel 116 |
| Workstreams, 100-day plan, options | Phases / options 118–120 · road maps 121–122 · Gantt 126 |
| History, milestones, timetable | Timelines 123–130 · balance (trade-off) 132–133 |
| Footprint / geographic mix | UK maps 134–143 · world maps 144–146 · regional maps 147–153 · globes 154–156 |
| Key numbers with icons | Icons in action 172–190 · quotes / speech bubbles 157 |
| Risk map / scoping | Audit pages 191–198 (risk map 196) |
| Icon sources | PwC icons 158–170 · editable graphics 199–204 · icon sets 205–211 |

## What credible sources say
- **Consistency of chrome, variety of visuals:**
  - Titles, logos, page numbers and footers sit in identical places on every slide, and one concept goes on each page.
  - Charts and infographics replace text wherever the data allows.
  - Sources: [Wall Street Prep: Investment Banking Pitchbook](https://www.wallstreetprep.com/knowledge/investment-banking-pitchbook/), [Deckary: pitch book structure](https://deckary.com/blog/investment-banking-pitch-book), [FE Training: pitch books](https://www.fe.training/free-resources/investment-banking/investment-banking-pitch-book/)
- **Standard sections, so the audience knows where they are:**
  - A pitch book runs through the same standard sections every time.
  - A section tracker helps a reader in a long book.
  - Sources: [Mergers & Inquisitions: pitch books](https://mergersandinquisitions.com/investment-banking-pitch-books/), [Macabacus: how to write a pitch book](https://macabacus.com/blog/investment-banking-pitch-book) (its Dynamic Agendas feature is this tracker)
- **Real private-markets decks** (Pantheon's Korea market update in the Slide Inspiration folder):
  - filled header bars
  - icon + number rows under charts
  - rounded label pills beside bullets
  - dashed takeaway boxes
  - one dark colour plus greys

  No accent-bar cards.
