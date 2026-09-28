# Case type 4: investment pitch deck built on a model

**Real examples:**
- Favour Capital Elite Program 2025 written test (Hims & Hers: 9 slides + P&L / valuation / beta / capital structure workbook); files in `…\Financial Models\Favour Capital Case Study\`
- Stonepeak FreezerCo (model + short deck)

## Storyline (9–12 slides; each title is the takeaway)
1. **Title**
2. **Investment summary:** the thesis in 3 points, valuation range, recommendation
3. **Company overview:** what it sells, to whom, how it makes money, key numbers
4. **Market:** size and growth (TAM/SAM), cited to 2+ sources
5. **Trends / growth drivers** (technology, consumer, regulation, economics)
6. **Competitive position:** peers table, differentiation, market share
7. **Business model / unit economics** (subscription, retention, CAC/LTV where relevant)
8. **Financials:** history + forecast, margin bridge
9. **Valuation:** DCF + comps (+ precedents); football field; sensitivities
10. **Risks and mitigants**
11. **Recommendation and next steps**

## Route
| Need | Skill |
|---|---|
| Peer multiples table | `financial-analysis:comps-analysis` |
| DCF with sensitivities | `financial-analysis:dcf-model` (build in Excel; recalc with `office.py`, not LibreOffice) |
| Competitive landscape slide | `financial-analysis:competitive-analysis` |
| One-page company profile | `investment-banking:strip-profile` / `investment-banking:one-pager` |
| Filling a firm's deck template | `investment-banking:pitch-deck` |
| Building slides from scratch | `scripts/ibdeck.py` (house style) |
| Final QA | `financial-analysis:ib-check-deck` + `office.py render` |

## Rules
- **Every number on a slide comes from the model or a cited source.** Put a "Source: … Notes: …" line on every slide (your Favour deck did this well).
- **Market data:** name the source and year on the slide. Where sources disagree, show the range and say which one you used.
- **Valuation:** show more than one method, state the WACC and g (or exit multiple), and put the result on a football field next to the current or offered price.
- **Recommendation:** a clear buy / pass / price range, with the one or two things that would change your mind.

## Traps
- Titles that are topics ("Market overview") rather than takeaways
- Charts pasted as pictures (not editable), mismatched units between slides, a number on a slide that differs from the model (run `ib-check-deck`)
- **Data tables in the model with a dead axis** (the Stonepeak workbook's IRR table repeats the same value across every exit multiple, because the axis wasn't wired to the model's input)
- Too many colours (the Favour deck used 6 accents; house style is one navy ramp + greys, with gold for a single highlight)
