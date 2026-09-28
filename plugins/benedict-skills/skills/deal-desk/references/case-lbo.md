# Case type 1: PE buyout (LBO), timed Excel test + 1–2 slides

**Real example:** Keppel KAP 2026 "Tough Love" (1h45, live on Teams; the Excel file is password-protected and the password is sent in the chat). Brief: `01. IB PE\Investment Banking Library\Financial Models\Keppel Test\`. Similar: Stonepeak FreezerCo (infra PE, model + deck).

## What they ask (typical)
1. A 5-year P&L projection from growth, margin, capex and NWC drivers
2. FCFF and FCFE (a full balance sheet is often *not* required, but they want the workings)
3. Covenants: Net debt / EBITDA and DSCR on an annual LTM basis
4. Sources and uses
5. Equity IRR and money multiple over the hold
6. Two sensitivity tables (purchase price multiple vs exit multiple; gearing vs interest rate). Use the house layout: base case in the centre, boxed; symmetric steps; heat map with green = higher IRR (`xlstyle.sensitivity()`)
7. Part II: WACC, a DCF, and an alternative valuation method in words
8. Bonus: 1–2 slides introducing the target to the investment committee

**Graded on:** "thought process" and "points for each line item modelled correctly". That means clear labels, question tags, one row per item, and no hard-codes. The slides are graded on accuracy, organisation and look ("infographics help").

## Build order and time split (1h45 = 105 min)
| Min | Step |
|---|---|
| 0–8 | Read the whole brief once. List every question, its tag and any ambiguous assumption (write them on the Cover as you go) |
| 8–15 | Set up the timeline (Year 0 actual + Years 1–5), paste the drivers as blue inputs, and the colour code |
| 15–35 | P&L: revenue → gross profit → opex → EBITDA → D&A schedule → EBIT → interest (from the debt schedule, on the **opening** balance) → tax (MAX 0) → NPAT |
| 35–50 | NWC balance and change, capex, FCFF (tax on EBIT), debt schedule, FCFE, cash / distributions |
| 50–58 | Covenants, sources & uses (price + fees + costs = debt + equity plug) |
| 58–70 | Exit (EV − costs − debt + cash), sponsor cash flows, IRR, MoM, then **check NPV at the IRR = 0** |
| 70–80 | Two data tables (inputs on the same sheet; typed axis values; confirm both axes move the result) |
| 80–92 | WACC, DCF (both terminal methods, show the implied multiple and growth), alternative-method text |
| 92–105 | Slides if attempted (the Keppel pattern: overview + investment case), final check pass, save as the requested name |

## Formulas worth knowing cold
- **FCFF** = EBIT × (1 − t) + D&A − capex − ΔNWC
- **FCFE** = NPAT + D&A − capex − ΔNWC − debt repaid (+ new debt). Reconcile: FCFE = FCFF − interest + (tax on EBIT − actual tax) − repayment.
- **DSCR** = CFADS / (interest + scheduled principal), where CFADS = EBITDA − tax paid − capex − ΔNWC
- **Exit equity** = exit EBITDA × multiple − exit costs − debt outstanding + cash
- **IRR:** `=IRR(Year 0 : Year N)`, with Year 0 = −sponsor equity; **MoM** = total inflows / equity
- **WACC** = E/(D+E)·Ke + D/(D+E)·Kd·(1 − t). The after-tax Kd goes in the WACC, not the pre-tax one.
- **Terminal value (Gordon)** = FCFF_N × (1 + g) / (WACC − g). Discount at N (year-end) or N − 0.5 for flows with mid-year.
- **Implied exit multiple** = TV_Gordon / EBITDA_N; **implied g** = (TV·WACC − FCFF)/(TV + FCFF)

## Traps seen in real submissions (don't repeat them)
- **Sale proceeds left at 0,** so the IRR only captures the interim cash flows
- **IRR range includes an empty column,** or starts at Year 1 instead of Year 0
- **After-tax cost of debt calculated, but the pre-tax rate used in the WACC**
- **Ignoring the brief's financing terms** (e.g. "a $15m loan" replaced with an assumed 60% LTV) and the loan fee
- **Depreciation as % of revenue** when the brief gives a policy (existing $740k/yr + new capex over 10 years). Every line below then misses.
- **Hard-typed forecast numbers** (e.g. cost of sales typed in): they lose the line-item marks
- **Data table with one dead axis** (Stonepeak file: every column identical, because the row-input cell wasn't the cell the model uses, or the axis was linked to the input)
- **Entry costs and fees missing from uses,** so the equity cheque is understated and the IRR overstated
- **Silent assumptions:** always write them on the Cover (cash-free / debt-free, timing of fees, depreciation convention)

## Build it fast with the generator
`python scripts/build_lbo.py case.json out.xlsx` builds all of the above, adds the data tables, recalculates in Excel and cross-checks against plain Python.

**JSON fields** (see `assets/examples/keppel-tough-love.json`):
- `first_year` (fiscal year of Year 0, e.g. 2025): **always set it when the company's years are known.** The timeline then reads FY2025, FY2026 … and labels say "FY2030 EBITDA". Leave it out only when the case uses generic years (e.g. Keppel's "Year 0"). Same field works in `build_lbo_template.py --fill`.
- `historical` (Year 0 P&L, costs positive)
- `drivers` (lists per year)
- `opening.nwc`
- `dep`: `existing_per_year`, `new_asset_life`, `same_year`
- `tax_rate`
- `deal`: price, cost %, exit multiple, min cash, `distribute_fcfe`
- `loan`: amount, rate, fee %, tenor or `amort_pct` list, `interest_on_average`
- `dcf`: Ke, g, `mid_year`
- `sensitivity.steps` (optional; default ±0.25x entry/exit, ±5% gearing, ±1% rate; the axes are always centred on the exact base case), `tags` (question labels), `assumptions_log`, `alt_method`

**Limits:** one amortising term loan, no cash sweep, no revolver, asset life ≥ forecast years. For a revolver, several tranches and a cash sweep use `scripts/build_lbo_template.py` (blank standard PE LBO; `--fill case.json` fills and verifies it, fields in `assets/examples/lbo-template-test.json`). For a full balance sheet, extend the generated file or use `financial-analysis:lbo-model` with it as the template.

## Defence questions (prepare an answer tied to a cell)
1. Why does EBITDA fall in Year 1? (Keppel: opex steps up from 72% to 77% of revenue, so the price is 4.9x LTM but 6.2x Year 1.)
2. What drives the IRR: EBITDA growth, deleveraging or multiple? (Split the value creation.)
3. Why is the DCF value so different from the price? (Implied exit multiple vs the 5.0x assumed.)
4. How much more debt could it carry? (Net debt/EBITDA < 1x, DSCR > 2.7x.)
5. What would you diligence first? (The cost step-up, studio-level economics, lease terms, churn.)
6. Is 5.0x exit fair? (Entry multiple, peers, no multiple expansion assumed.)
