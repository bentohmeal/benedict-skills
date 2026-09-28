# Cover letter structure

Base file: the newest .docx in `Cover Letters 2027\` (run `scripts/latest-sources.ps1`). Copy it and edit the copy, so the letterhead, font and spacing stay the same.

| # | Paragraph | Rules |
|---|---|---|
| 0 | Header | Name, phone, SMU email, **today's date** (e.g. 24 September 2026). "Dear Hiring Manager," unless a named contact is known. |
| 1 | Opening | Who you are (final-year SMU Finance, graduating Dec 2026) → the exact programme/role name from the JD → **the firm hook** (from dossier section 6). It must name something specific to this firm: a strategy, fund, deal or person. "Leading global bank" alone fails. |
| 2 | Partners Group | **Past tense** (the internship ended Jul 2026). Choose Kafka and/or Mosaic bullets by JD match (`experience-log.md` tags). One concrete result, e.g. "the sponsor assessment helped secure IC approval to the next stage". |
| 3 | Pantheon | ALLIF: fund cash flow model + FX stress test for buy-side and fund roles. GP benchmarking + ESG scorecards for LP or fund-of-funds roles. |
| 4 | PwC | Timuraya sell-side, buyer list, data room. Lead with this paragraph's material for IB roles. |
| 5 | CAP 1 | One or two sentences only; cut it entirely if the letter runs over one page. |
| 6 | Close | Must match the role's **function**: "investment banking" only for IB roles; "private markets", "private credit" or "global markets" as appropriate. Name the target firm and no other. |

**Always check before saving:**
- `scripts/qa-letter.ps1 -Path <file> -Firm "<Firm>" [-Aliases ...]` must print CLEAN.
- The whole letter fits on one page.
- The closing line's function matches the JD. The SMBC Global Markets letter said "investment banking", which is the kind of mismatch this check exists to catch.
- Save as `Cover Letters 2027\Benedict_Toh (<Firm>).docx`. If that file already exists, ask before overwriting; the alternative is to save as `Benedict_Toh (<Firm>) v2.docx`.
