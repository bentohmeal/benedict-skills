# Case type 2: project finance model, built from scratch

**Real example:** SMBC 2024 Analyst Programme: a 250 MWac greenfield solar bid, 20-year PPA at USD 80/MWh, EPC 200m, land 50m, 80% max gearing, 1.30x sizing DSCR, SOFR swap 4.5% + 2.0% / 1.5% margins, monthly IDC, quarterly repayments starting 6 months after completion. Brief: `…\Financial Models\SMBC Analyst Test\2024 SMBC Analyst Program.docx`.

**Graded on:** logic, structure and layout (tabs), understanding of the concepts, presentation and ease of use, accuracy, and **no circularity**. List every assumption you add.

## Concepts to explain in one line each
- **CFADS** (cash flow available for debt service) = revenue − opex − tax (− maintenance capex / reserve movements if any)
- **DSCR** = CFADS / (interest + principal) for the period. The sizing DSCR (1.30x) caps how much debt the cash flows can carry.
- **Debt sizing** = the lower of:
  - gearing × total project cost
  - PV of CFADS over the repayment period (at the debt rate) ÷ minimum DSCR
- **Sculpting:** set each period's debt service = CFADS / target DSCR, so repayments follow the cash flow shape (seasonality). The DSCR is flat, and the debt repays exactly at maturity.
- **IDC:** interest charged during construction, when there's no revenue. It's capitalised and funded by more debt, so it becomes part of project cost. That's why fees and IDC create circularity.
- **Project IRR** (unlevered: capex vs CFADS) vs **equity IRR** (equity injections vs dividends). Leverage lifts the equity IRR when the project IRR is above the after-tax cost of debt.
- **P50 / P90:** the energy yield exceeded with 50% / 90% probability. Lenders usually size on P90; equity looks at P50.
- **Lowest bid tariff:** the tariff at which the equity IRR = the client's minimum (12%). Debt re-sizes at every tariff, so solve it, don't eyeball it.

## Avoiding circularity (say this in the interview)
Fees and IDC depend on debt size, and debt size depends on total project cost, which includes them. Two clean options:
1. **Solver + paste** (what `build_pf.py` does): solve debt and project cost outside the calculation chain, paste them as inputs (blue on yellow), and show a check that pasted = live calculation. Re-run the solver after any input change (`build_pf.py --resolve`). This is the "copy-paste macro" banks use.
2. **Closed form:** with pro-rata funding at gearing g and monthly rate r, the debt balance follows D_m = D_{m−1}(1 + g·r) + g·C_m, and the fee term can be solved algebraically. It's elegant but harder to explain under time pressure.

## Build order (take-home: aim for a clean first version in ~4 hours)
1. **Timeline:** monthly construction (financial close → COD), quarterly operations (COD → PPA end), with flags for construction, operations and repayment periods and the operating year
2. **Generation:** MW × 8,760 × capacity factor × seasonality × (1 − degradation)^(operating year − 1)
3. **Revenue and O&M:** fixed per MW and variable per MWh, both escalated from the base year → EBITDA → CFADS
4. **Construction funding:** capex, fee, IDC, equity first then debt (or pro-rata; state which)
5. **Sizing:** gearing cap vs DSCR cap, and show which one binds
6. **Debt schedule:** interest-only until the first repayment, then sculpted or straight-line; DSCR by quarter; min and average
7. **Dividends** (all cash after debt service), then project and equity **XIRR with real dates**
8. **Annual 3 statements:** IDC and fees capitalised into plant; depreciation from COD; the balance sheet must balance every year
9. **Answers sheet:** one line per question, then the bonus (lowest tariff, sculpting)

## Traps
- **Straight-line repayment with seasonal generation:** in the SMBC case, equal quarterly principal gives a DSCR of 0.83x in Q3/Q4 and a cash shortfall. The model flags it; this is why banks sculpt.
- **Forgetting the grace period** before the first repayment (interest-only quarters)
- **Fee on the initial rather than the final debt amount,** and IDC not included in project cost
- **Degradation applied from Year 0** instead of the second operating year
- **Using annual periods** when the brief says quarterly repayments and gives seasonal factors
- **MINIFS / XLOOKUP:** they don't exist in Excel 2016 (use a helper row)
- **Depreciating land**

## Generator
`python scripts/build_pf.py case.json out.xlsx` builds 12 sheets in lender order:
- Cover · Inputs · **Timing** (flags)
- Construction (monthly)
- **Operations · Debt · Waterfall** (quarterly, on one column grid)
- Annual (IS / CF / BS + annual DSCR) · Returns (dated XIRR / XNPV)
- **Scenarios** (6 re-solved cases + a tariff × capacity factor data table) · **Dashboard** (answers, lender metrics, CFADS vs debt service chart) · Checks

It cross-checks 14 outputs against an independent Python engine, runs the format lint and solves the lowest bid tariff.

**Lender features:**
- **DSRA** (`"dsra": {"on": 1, "quarters": 2}`): the next N quarters of senior debt service
  - funded at COD in project cost
  - topped up only from cash after debt service, and released when the target falls or at maturity
  - COD must fall on a quarter end
- **Ratios:** DSCR, LLCR (including the DSRA) and PLCR each quarter, with minimums
- **Waterfall:** CFADS → interest → principal → DSRA → cash available for distribution → dividends

**JSON:** see `assets/examples/smbc-solar.json`. Switches: `energy_case` P50/P90, `debt.repayment` sculpted/straight, `tax_rate`.

**SMBC base answers (P50, sculpted):**

| | Brief only (DSRA off) | V2 worked example (DSRA on) |
|---|---|---|
| Debt (gearing binds) | 215.2m | 224.5m |
| Project cost | 269.0m | 280.6m |
| IDC / fee / DSRA | 6.30 / 2.69 / – | 6.17 / 2.81 / 11.64 |
| Flat DSCR | 1.86x | 1.79x |
| Min LLCR / PLCR | 1.86x / 2.03x | 1.82x / 1.94x |
| Project IRR | 13.5% | 13.5% |
| Equity IRR | 31.2% | 29.5% |
| Lowest tariff (12% equity IRR) | USD 60.75/MWh | USD 61.89/MWh |

Defence sheet: `Interview Prep/Case Studies/_Worked examples/SMBC Solar/V2/Defence – SMBC Solar.md`.

## Defence questions
1. Which sizing constraint binds, and what happens under P90? (P90 with a 1.6x DSCR: the DSCR binds at 202.7m.)
2. Why sculpt? (Seasonality; flat DSCR; maximises debt for a given minimum DSCR.)
3. How did you avoid circularity? (Solver + paste with a check; or the closed form.)
4. Why is the equity IRR so far above the project IRR? (80% gearing at 6% all-in vs a 13.5% project return.)
5. What reserves would lenders add? (DSRA of 6 months' debt service: built in V2, and it costs about 1.7 points of equity IRR; MRA; a distribution lock-up at 1.10–1.15x.)
6. What's the lowest bid, and what are its risks? (Tariff sensitivity; P90 downside; O&M escalation.)
