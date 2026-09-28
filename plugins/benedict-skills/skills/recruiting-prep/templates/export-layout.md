# `<Firm> Prep.docx` export layout

Build with the docx skill. Follow the conventions of Benedict's existing prep docs (Pentagreen and Lazard Prep):
- numbered H1 sections
- `x.y` H2 subsections
- every topic opens with a bold **The Pitch:** line
- tables instead of long bullet lists
- 📌 coaching tips after answers

| H1 | Content | Source |
|---|---|---|
| 1. FIRM OVERVIEW | Dossier §1 (keep the sources as a short list at the end of the section) | dossier.md |
| 2. WHY <FIRM> | Dossier §2 | dossier.md |
| 3. LEAD WITH | Dossier §3 table, then the **full text** of each listed bank answer, pulled from the Master Bank by ID, with any `overrides` note shown as a 📌 under that answer | dossier + Master Bank |
| 4. FIT & BEHAVIOURAL | `WALK-TMAY`, `FIT-STRENGTH`, `FIT-WEAKNESS`, `FIT-PRESSURE`, `FIT-CONFLICT`, plus any other `FIT-*` in `priority`; `{Firm}`/`{Role}` filled in | Master Bank |
| 5. FIRM-SPECIFIC QUESTIONS | Dossier §4 | dossier.md |
| 6. TECHNICALS | `TECH-*` in `priority`, then the rest of the `TECH-*` whose tags match the side (pc / pe / ib / infra). Technicals follow Definition → Mechanics → Follow-up traps. | Master Bank |
| 7. QUESTIONS TO ASK | Dossier §5 | dossier.md |
| Appendix | Deal skeletons (`DEAL-*-SKELETON`) on one page for last-minute review | Master Bank |

**Rules:**
- Answers with `status: stub` are never exported. List them in a "Gaps before this interview" box at the top instead.
- Mark `draft` answers with "(draft)" after the heading, so Benedict knows they haven't been tested.
- Put a footer on every page: "Generated <date> from Master Bank + <Firm> dossier. Edit the markdown, not this file."
