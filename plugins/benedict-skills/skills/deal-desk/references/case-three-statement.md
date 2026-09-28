# Case type 3: integrated 3-statement model from given accounts (+ DCF)

**Real example:** PwC Deals CF test (ABCDE Corp, 10-K data, 2005–06 actuals). Pack:
- a `.doc` of financial statements
- an `.xls` worksheet with tabs Instructions · Cover · IS · BS · CF · Debt Schedule · DCF, with the driver notes pre-typed

Folder: `…\Financial Models\PwC Case Study\` (your attempt, a Claude attempt and a practice copy are there).

## Route
The worksheet **is** the template, so use `financial-analysis:3-statement-model`: it fills an existing template and keeps its layout. `.xls` files open with openpyxl only after conversion. Save a copy as `.xlsx` through Excel (office.py / COM) first, and keep the original layout.

## What the instructions usually say (PwC example)
- **Growth and margins:**
  - Revenue +3%
  - COGS −20 bps and SG&A −10 bps of revenue a year
  - D&A % of revenue flat
  - Tax 40%
  - Minority interest flat
- **Normalise the history:** find the one-off items in the historical IS and adjust COGS, expenses and tax
- **Balance sheet ratios** kept at the last actual year; short-term borrowings go into the revolver
- **Capex:** the actual from the 10-K, then $40m a year. **Dividends:** no growth in DPS
- **Debt schedule:**
  - Minimum cash 15
  - Interest: cash 4%, tranches 8%, revolver = last year's weighted average short-term rate
  - Watch the 2011 mandatory repayment ("use logic")
- **DCF** at a 15% WACC. Current capital structure from the last actual BS; diluted shares by the treasury stock method at the given price (13.06)
- **"Finish the statements before the DCF"**

## Build order
IS (to EBIT) → BS ratios → CF (without interest) → debt schedule (cash available for debt repayment → revolver draw / repay with MAX/MIN, respecting minimum cash) → interest → finish IS → BS check → DCF.

## Interest without circularity
Charge interest on **opening** balances (say so). If the template demands average balances, add a circularity switch (1 = average with iterative calculation on, 0 = opening), default 0.

## Checks
- Balance sheet balances every year
- Cash ≥ minimum cash
- Revolver ≥ 0
- The CF's ending cash = the BS cash
- Retained earnings roll forward (+ NI − dividends)
- DCF equity value per share uses **diluted** shares

## Traps
- Leaving the one-off items in the forecast margin base
- Revolver sign errors (a draw shown as a repayment)
- A mandatory repayment larger than available cash (the 2011 trap): the revolver must fund it, or cap it and explain
- Treasury method using basic shares, or options out of the money counted
- The DCF using the equity value as the EV

## Defence questions
1. Which items did you normalise, and why? 2. How does the revolver work in your model? 3. What happens in 2011? 4. Walk me from EV to value per share. 5. Why is interest on opening balances acceptable?
