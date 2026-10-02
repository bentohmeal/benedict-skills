# Capital IQ pull → `deal_data.json`

Use this when a model or deck needs real company figures, trading comps or precedent deals. The output, `deal_data.json`, feeds the model and deck scripts in place of hand-typed `DATA` dicts.

## Rules
- **Access.** He has Capital IQ Pro only through SMU single sign-on, so the S&P (Kensho) connector can't sign in. Use Claude in Chrome on the Capital IQ website. **He logs in himself**; never type or handle credentials.
- **Licence.** Personal and academic use only. Make small, targeted pulls: one company, its peer screen and one deal screen. No bulk scraping or looping over many tickers. Keep the "personal and academic use" note in `deal_data.json`.
- **Exports only.** Page tables don't come through `get_page_text`, so always use Capital IQ's own Excel export. It lands in `~/Downloads` as `SPGlobal_*.xlsx`.
- **Folder.** `output/_Deal Desk Toolkit/capiq/<TICKER>/`
  - `raw/` holds the six exports, renamed: `income_statement`, `balance_sheet`, `cash_flow`, `multiples`, `peer_comps`, `precedents` (.xlsx).
  - `curation.json` is written by hand.
  - `deal_data.json` is built by the parser.

## 1. Company financials (4 exports)
1. Top search box → type the company → open its **Corporate Profile**.
2. Left menu → Financials → Templated:
   - Income Statement
   - Balance Sheet
   - Cash Flow Statement
   - Multiples
3. On each page, use Export (top right) → **Export to Excel as Data**.
4. Default range is the last 5 fiscal years, which is standard bank history. The range slider doesn't drag reliably, so accept 5 years.

## 2. Trading comps (1 export)
1. Profile → **Peer Comps** (or Screener → Companies). Set the screen:
   - Public company, operating.
   - The target's primary industry.
   - A size band.
2. Delete obvious misfits from the list. Capital IQ backfills to its top-10 rank, so deleted names come back as others.
   - **Don't fight it:** export everything and pick the peers in `curation.json`.
3. Set Export to **Results As Values** → **EXPORT** → click **"Results are ready for download"**.
4. The export has three data sheets, and the parser merges all three:
   - Sheet1: financials (LTM).
   - Sheet2: margins, growth and leverage.
   - Sheet3: multiples (LTM and forward).

## 3. Precedent transactions (1 export)
1. Screener → **Transactions** → New Screen. Add from Recommended Criteria:
   - Transaction Type = **M&A**.
   - Transaction Status = **Completed**.
   - Announced Date **Between** 01/01/<year−10> and today. Click "In" to switch it to Between.
   - Total Transaction Value **> 300** ($M).
   - Transaction Industry (MI): type in the search box, e.g. "Leisure Products", "Housewares", "Footwear".
     - **Ticking:** clicks on the tick boxes don't register. Click the row, then press **Space**.
   - Click **Add** after each criterion, then **Run Screen**.
2. **DISPLAY COLUMNS** → field search. From Deal Ratios/Multiples → S&P Capital IQ Deal Ratios/Multiples, add:
   - Implied Enterprise Value/ EBITDA
   - Implied Enterprise Value/ Total Revenue
   - Implied Enterprise Value/ NTM EBITDA
   - Implied Enterprise Value/ NTM Revenue
3. Apply → **EXPORT** (Results As Values) → download link.
4. **Known gaps:**
   - Industry tags miss some well-known deals (e.g. Helen of Troy/Osprey, Crocs/HEYDUDE).
   - The value floor drops small ones.
   - List them under `precedents_missing` in `curation.json`. Don't invent their multiples.

## 4. Curate: `curation.json` (by hand, then he reviews it)
- `ticker`.
- `peers_core`: tickers, plus `peer_notes` giving one line per peer explaining why it's in or out.
- `precedents_core` and `precedents_reference` (MI Transaction IDs), plus `precedent_notes`.
  - Exclude minority stakes, spin-offs, misclassified targets and multiple outliers.
  - Use "Reference" for deals with a revenue multiple only, or an adjacent sector.
- `precedents_missing`.
- Worked example: `capiq/YETI/curation.json`.

## 5. Parse and check
```
python scripts/capiq_parse.py build "<...>/capiq/<TICKER>" --accessed YYYY-MM-DD
python scripts/capiq_parse.py check "<...>/capiq/<TICKER>"
```
- **Units:** all money is in **US$ m** (Capital IQ's $000 ÷ 1,000). Per-share figures stay in $, shares stay actual, margins in %, multiples in x.
- **Source tags:** each table has `src` = "S&P Capital IQ, accessed <date> (<file>)". Cite it in the model's Sources tab and in slide footnotes.
- **What `check` does:**
  - Prints the headline figures.
  - Ties out gross profit = revenue − COGS, assets = liabilities + equity, and CFO + CFI + CFF + FX = change in cash.
  - Lists the comps and core precedents by role.
  - Exits 1 on any failed tie-out.
- **Then compare against the screen.** Open the company's Financial Highlights and match at least 10 figures (cash, total assets, net debt, total debt, equity, revenue) across 3 years.

## `deal_data.json` shape
- `company`: name, listing, MI key, CIQ key.
- `accessed`, `licence`, `missing`: the raw files not found.
- `income_statement` / `balance_sheet` / `cash_flow`:
  - `periods`: label, period_end, filing_date.
  - `lines`: label → list of values, oldest first.
  - Labels are Capital IQ's own (e.g. "Total Revenue", "EBITDA", "Net Debt", "Cash from Ops.").
- `multiples.series`: metric → average/high/low/close → date → x.
- `comps.rows`: one dict per company. Contains ticker, exchange, `role` (target / core / excluded), `note` and every exported field (e.g. "Total Enterprise Value (CIQ)", "TEV/ EBITDA", "TEV/ Forward EBITDA").
- `precedents.rows`: one dict per deal. Contains `role` (core / reference / excluded), `note`, value and multiples. `precedents.not_in_screen` lists the known gaps.

## Gotchas (from the first pull, YETI, 3 Oct 2026)
- **Cookie banner:** click Reject All.
- **ChatIQ pop-up** can cover the download link; close it first.
- **"Couldn't determine which page":** call `tabs_context_mcp` again, then retry.
- **Guessed URLs fail** (`#company/searchResult?...`). Use the search box.
- **Balance sheet supplemental block** is headed "($)", but its debt and book-value lines are $000. The parser handles this; check per-share lines if a new template appears.
- **Live price drifts from the export** (e.g. $41.37 exported vs $40.87 later). The `accessed` date is the as-of date for market data.
