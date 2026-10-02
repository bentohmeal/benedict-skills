# Slide layouts: pick a shape for each message

Read this **before planning any deck**. Build the plan with `deck-pipeline.md` (the `layout_match.py plan` table), show it to Benedict, then build. See every layout rendered in `Claude Things\output\_Deal Desk Toolkit\Deck Layout Gallery.pptx` (rebuild it with `scripts/layout_gallery.py`). A worked before/after: Keppel V2 vs V3 in `Interview Prep\Case Studies\_Worked examples\Keppel Tough Love\`.

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

## The layout library: one catalogue of every layout (`assets/layout_library.json`)
297 records, each with use when / don't use when, sections, data type, item range, slots and a thumbnail (`assets/layout_thumbs/`):
- **Coded components** (`table`, `fin_table`, `football_field`, `side_tabs`, `risk_matrix`…): drawn by `ibdeck.py`. Their pictures are `code_<id>.png`, cropped to just the component (rebuild: wrap the component methods, run `layout_gallery.py`, crop each one's shapes).
- **Bank page designs** (`bk01`–`bk58`, 49 kept from his review): recurring layouts from the real bank pages, rebuilt in house style. Fill with `d.bank(s, "bk13", box=..., data={...})`; copy the data shape from `bank_samples.SAMPLE["bk13"]`. Deal tables carry logos: `bk21` / `bk23` take `logos={name: image path}`, and `bk21` with `bar_col=None` is a plain deal-details table with no chart. Specs in `bank_specs.py`, drawing in `bank_layouts.py`.
- **Page recipes** (`page_market`, `page_overview`, `page_geography`, `page_landscape`, `page_deals`, `page_text`, `page_thesis`, `page_risks`): full dense pages copied from real bank pages; see the gallery's Dense Pages section.
- **Infographics** (`ig001`–`ig211`): PwC's originals, restyled (colours, fonts, sizes and shadows only; lessons #29). Use them for shapes the components lack: cycle, pyramid, funnel, Venn, bridge, map. 16 are text-free (maps, icon sets): label them beside with `d.text`.
- **Real bank pages:** `assets/real_deck_pages.json` holds 389 pages from `Real IB-PE Decks`, each tagged with the layouts it uses. The library lists the best 4 under each layout as `exemplars` (deck, page, thumb). Real banks build most pages from `table`, `fin_table` and `page_text`, with `column`, `line` and `heatmap` next; infographics almost never appear, so use one only where its shape *is* the message.
- **Combine layouts freely (his rule, 2 Oct 2026):** one exhibit or slide may join several layouts, e.g. an infographic with a table beside it, two infographics side by side, or a funnel with a stat strip. In the plan, write the pick as `"ig075+table"` (lead first); `layout_match.py plan` checks each part. Combine when the pieces add information together, not to fill space.

**Pick a layout for each slide:** follow `deck-pipeline.md` (chunk → `layout_match.py match` → pick with a reason and 2 alternatives → `layout_match.py plan`). Look at each candidate sheet and open the exemplar page before choosing. For a quick one-off lookup, `python scripts/layout_tag.py find <section> [data_type] [items]` still gives a shortlist.

**Insert an infographic with its text filled:**
```python
d.layout(s, "ig075", variant=1, box=(x, y, w, h),
         data={"head": ["Pricing", "Sites", ...], "text": [...], "num": ["1", "2", ...]},
         drop=("v1.text6",), highlight=None)
```
- `data` takes role lists (`head` / `num` / `text`, filled in the slot order from the record's `variants[].slots`) or single slot names (`"v1.head2": "..."`).
- Unused optional pieces are removed; other unused slots are blanked. `drop` removes a whole piece.
- The variant (one sub-diagram of a PwC page) is scaled into `box`.
- Text that won't fit, even at 12pt and then 10pt, is reported by `save()` as a `LAYOUT WARNING`. Shorten the text or pick a bigger variant.
- `d.infographic(s, no)` still pastes the whole PwC page unfilled (for editing by hand).
- Rebuild or check the library: `layout_tag.py build`, then `validate` (after `scan` and `name` if `infographic_library.py` rebuilt the pptx). Hand tags live in `assets/layout_tags.json`; never edit the built JSON.

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
| The same grid (3 equal columns: header, chart, bullets) on every slide | Template feel; nothing adapts to the content | Pick from the layout library above and vary it |
| ■ square bullets, and walls of bullets (3+ bullet blocks on a slide) | Unedited AI output | `side_tabs`, `pill_rows`, `numbered_steps`, `pros_cons`, a table |
| A thin rule under every block header | Looks unfinished next to real bank decks | Filled navy header bars |
| Decorative icons with no meaning | Clip-art feel | An icon only where it names the number or item next to it |
| Shadows, glows or a gradient "aura" on lines and shapes | python-pptx's default theme style; looks cheap | `_line()` / `_shape()` (flat, solid) |
| Many font sizes on one slide | Looks unplanned | 20 / 16 / 12 / 10, plus 8 italic for sources |
| Two filled bands stacked: a navy header bar with a navy table header row right under it | Heavy and templated; no real bank page does it | Keep the bar; table column headers bold black with a navy rule (`table()` auto) |

`lint()` (run by `save()`) prints `AI TELL:` lines for all of these except decorative icons. Treat them like layout warnings: fix them before handing over.

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
