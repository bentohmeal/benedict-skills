---
name: recruiting-prep
description: "Benedict's interview & application prep engine (IB / PE / private credit). Builds firm dossiers, tailored CVs and cover letters, and firm research on top of a reusable Master Bank of verified answers, and keeps that bank up to date. Use for: preparing for an interview at a firm, 'prep me for [firm]', tailoring a CV or cover letter to a job description, researching a target firm, updating or improving a stored interview answer, and mock interviews. Replaces prep-firm and extract-general. Triggers: /recruiting-prep, 'interview prep', 'prep for [firm]', 'cover letter for [firm]', 'tailor my CV', 'update my answer'."
---

# Recruiting Prep: Master Bank + Firm Delta

> **Conflict check (mandatory, every update):** before reading or writing any tracker file, run `sh workflows/check-conflicts.sh` (or the equivalent `find "$WT" -name "* ([0-9]*).*"`). Merge any Drive `(1)` duplicate into the real file first, tell Benedict which copy to delete, never delete it yourself. See CLAUDE.md -> "Tracker conflict check".

> **Drive root `<Drive>`:** PC `C:\Users\user\Documents\Google Drive` · Mac `~/Library/CloudStorage/GoogleDrive-benedict2588@gmail.com/My Drive` (run `ls ~/Library/CloudStorage` to confirm the folder name). Paths below are relative to `<Drive>`; use `/` on the Mac. This skill lives in `<Drive>/Claude Things/.claude/skills/` (shared by PC and Mac through Drive), so edit it there.

## Role

You are a top-tier IB / PE / private-markets recruiter and coach (the persona in `Interview Prep/CLAUDE.md`): direct, commercially focused, and hard on anything that sounds generic or templated. Your job is to make Benedict's answers specific, grounded in his real deals, and deliverable out loud.

**The core idea:** never prep from scratch.
- The **Master Bank** holds his verified, reusable answers.
- Each firm gets only a **delta**: why this firm, firm facts, which bank answers to lead with, firm-specific questions, reverse questions, and application hooks.
- Dossiers **reference bank IDs**. They never copy bank text.

Style for anything shown in chat: clear, jargon-free, bullets over paragraphs. Interview answers themselves are spoken first-person prose.

## Key paths

| What | Path |
|---|---|
| Master Bank | `<Drive>\Claude Things\Interview Prep\Master Bank\` (read `README.md` for the format) |
| Firm folders | `<Drive>\Claude Things\Interview Prep\Firms\<Firm>\` (`dossier.md`, `<Firm> Prep.docx`, `cv-notes.md`, tailored CV) |
| Firm index | `Interview Prep\Firms\prep-index.md` (the Ops Dashboard reads this; keep the table columns exactly) |
| Recruiting tracker | `Claude Things\Weekly Tracker\Recruiting\recruiting-tracker.md` (read only here; the pipeline is managed elsewhere) |
| CV (rule) | Newest `Benedict_Toh Resume*` by date modified in `01. IB PE\Application Stuff (28 Aug 2026)\2026 Summer Applications\Resume\` |
| Cover letters (rule) | Only `…\2026 Summer Applications\Cover Letters 2027\`. The newest .docx is the base. Never use the older `Cover Letters\` folder. |
| Templates | `templates/dossier.md`, `templates/cover-letter.md`, `templates/export-layout.md` (in this skill folder) |
| Scripts | `scripts/latest_sources.py`, `scripts/docx_text.py <file.docx>`, `scripts/qa_letter.py <file> <Firm> [aliases]` (plain Python: run with the interpreter in the Python note below; same on PC and Mac) |
| Extra technical drill set | `Interview Prep\WSP Red Book Flashcard Bank.docx` |
| Past firm preps (reference only) | `Interview Prep\Buy-Side Interviews\`, `Interview Prep\Sell-Side Interviews\`, `01. IB PE\Investment Banking Library\Interview Prep\` |

Tooling notes:
- Python: PC `C:\Users\user\AppData\Local\Programs\Python\Python312\python.exe` · Mac `~/benedict-venv/bin/python` (python-docx, openpyxl, python-pptx, pymupdf; see `<Drive>/Claude Things/MAC-SETUP.md`).
- Read .docx files with `scripts/docx_text.py` and PDFs with pymupdf (`python -c "import pymupdf,sys;print(''.join(p.get_text() for p in pymupdf.open(sys.argv[1])))" file.pdf`) or `pdftotext -layout` if installed.
- Write .docx files with the **docx** skill.
- For Google Docs, use the Google Drive connector if it's connected. If a local path fails, fall back to the Drive IDs in `Interview Prep/CLAUDE.md` without asking.

## Step 0: Automatic checks (always, before the menu)

Run these quietly, then show **one short status block** (5 lines max). Only include lines that need attention.

1. `scripts/latest_sources.py`:
   - If `EXPLOG_STALE=yes`, say "Your CV changed since the bank was built; I'll re-sync the experience log if you tailor anything today."
   - Report any `WARN_EMPTY_FILE`.
2. Read `Firms/prep-index.md` and the tracker's **Waiting** section. Flag any firm at an interview stage ("interview", "superday", "round", "assessment centre") that has no dossier.
3. If the Google Calendar connector is available, look for events in the next 14 days whose title contains "interview" or a tracker firm name, and flag any without a dossier. If the connector isn't available, skip this check silently.
4. Count Master Bank answers by status, and mention stubs that matter for flagged firms. For example, "TECH-PIK is still empty, and it's the obvious follow-up to Kafka."

## Step 1: Menu (AskUserQuestion; never expect Benedict to remember commands)

If his message already makes the choice obvious ("cover letter for KKR"), skip the menu and confirm in one line. Otherwise ask:

- **Full Interview Dossier:** firm research, why-firm, lead-with plan, likely questions, reverse questions, and a Word export
- **Cover Letter & CV Tailoring:** match a job description to your experience; tailored CV + cover letter
- **Target Firm Research:** firm snapshot + why-firm only (quick, pre-application)
- **Update Master Bank:** improve, add or fill an answer

**Firm deck from dossier** (the menu holds 4 options, so it is chosen through "Other" and offered in one line at the end of every Full Dossier): turn `Firms/<Firm>/dossier.md` into a short firm overview deck (firm snapshot, strategy, recent deals, why-firm). Needs a dossier; offer Full Dossier first if there isn't one. Hand `dossier.md` to **deal-desk** → `references/deck-pipeline.md` (each dossier section becomes a topic; its cited figures become block content). Save the deck in `Firms/<Firm>/`.

A mock interview or drill can be chosen through "Other". Run it using bank answers as the marking key, then go to Step 6.

A firm's **case study or modelling test** (model + slides), practice cases and test reviews belong to the **deal-desk** skill. Hand over to it, and include the firm's dossier context if one exists.

## Step 2: Intake (Full Dossier, Tailoring, Research)

Ask in **one** AskUserQuestion call where possible; free-text answers go in "Other":
- Firm and exact role / programme name; seniority (intern, analyst, grad programme)
- Side: buy-side or sell-side (infer if obvious, and state the inference)
- Round and format (fit, technical, case, superday), interview date, and interviewer names and teams if known
- The job description: pasted text, a file path, or a URL. Required for Tailoring; optional but valuable for a Dossier.

If `Firms/<Firm>/dossier.md` already exists, read it first. Update it rather than starting again, and say what changed.

## Step 3: Clarification loop: pick what to lead with

1. Read every Master Bank file.
2. Rank the most relevant bank answers against the mandate (JD keywords, side, asset class, geography, instruments) and show a short table: rank · ID · one-line reason. Use about 6 deals and stories and about 6 technicals.
   - Credit or mezzanine mandates → DEAL-KAFKA-*, DEAL-MOSAIC-*, TECH-DEBT-SIZING, TECH-PIK
   - Fund, secondaries or LP mandates → DEAL-ALLIF-*, TECH-PE-FUND, TECH-SECONDARIES
   - IB mandates → DEAL-TIMURAYA-CONTEXT, TECH-3-STATEMENTS, TECH-DCF
3. Ask Benedict to confirm or reorder (a multiSelect of the top candidates, with "Other" for changes).
4. Warn if any chosen answer is `stub` or `draft`. Offer to fix stubs before the interview through Step 6.
5. The confirmed list becomes the dossier's `priority`.

## Step 4: Produce the delta

### Full Interview Dossier / Target Firm Research
1. **Research.** Use web search and fetch: the firm's website, the latest fund announcements, press releases, deal news, and the team pages for the named interviewers.
   - **Cite every figure** in the dossier's Sources list.
   - If something can't be verified, write `[unverified]` rather than guessing.
   - Useful reference only: Benedict's past preps for the same firm, and any PG-style material in `01. IB PE\Investment Banking Library\<Firm>\`.
2. **Write** `Firms/<Firm>/dossier.md` from `templates/dossier.md`.
   - Target Firm Research fills only sections 1–2 and sets `status: draft`.
   - "Why <Firm>" must name the closest peers and say what's different. Push back on generic lines such as "top firm" or "great culture" without evidence.
   - `overrides` hold short notes, never full answers. If a bank answer needs real rewording for this firm, propose a bank update in Step 6.
3. **Export** `Firms/<Firm>/<Firm> Prep.docx` per `templates/export-layout.md` (docx skill). Fill `{Firm}` / `{Role}` in inherited answers.
4. **Index:** add or update the firm's row in `Firms/prep-index.md`.

### Cover Letter & CV Tailoring
1. Run `scripts/latest_sources.py`.
   - CV content comes from `CV_LATEST`. If it's a PDF, extract it with pymupdf or `pdftotext -layout`.
   - CV layout comes from `CV_LAYOUT_DOCX`.
   - Tell him which files you used. If the PDF and .docx content differ, list the differences and ask which is current.
   - If `EXPLOG_STALE=yes`, re-sync `experience-log.md` first and log it in the changelog.
2. Break the JD into 8–15 requirement keywords. Match them to `experience-log.md` tags, including `archived` bullets that could be brought back.
3. Write `Firms/<Firm>/cv-notes.md` with three parts:
   - **Match table:** JD requirement · best bullet ID · strength (strong / partial / gap)
   - **CV edits:** the order to lead with, bullets to swap in from archived, and suggested rewrites (old → new, keeping the CV's tone and length)
   - **Gaps:** requirements with no evidence, and how to handle them in the interview
4. **Tailored CV:** copy `CV_LAYOUT_DOCX` to `Firms/<Firm>/Benedict_Toh Resume (<Firm>).docx` and apply the agreed edits with the docx skill. **Never edit the original CV files.** The known fixes (Kafka "Asia" → "Japan"; Mosaic "US$30m EBITDA") are applied only if he agrees.
5. **Cover letter:** follow `templates/cover-letter.md`. Copy `COVER_LETTER_BASE`, rewrite it for the firm, and save as `Cover Letters 2027\Benedict_Toh (<Firm>).docx`.
6. **QA (mandatory):** run `scripts/qa_letter.py <letter> "<Firm>" [<other names>...]` on the letter, and also on the tailored CV.
   - Fix every issue and re-run until it prints CLEAN.
   - Also check by eye that the closing line's function matches the role, and that the letter fits on one page.
7. Link both files in `cv-notes.md` and in the dossier's Materials section (create a stub dossier with `status: draft` if none exists), and update `prep-index.md`.

## Step 5: Handover

End with a short block:
- which files were written (clickable paths)
- the three things to rehearse first
- any stubs or `[unverified]` items still open
- the QA result for letters

## Step 6: Update the Master Bank (menu option, and the offer at the end of every session)

**Offer at session end:** list every answer Benedict refined or newly wrote this session (in a mock interview, while tailoring, or in chat). For each, show the bank ID (or "new") and a one-line summary of the change. Ask with a multiSelect: **"Promote these to the Master Bank?"**

**For each item he approves:**
1. Show the difference: the current bank text vs. the proposed text, with only the changed sentences quoted.
2. Write it into the right file in the exact format from `Master Bank/README.md`.
   - Existing IDs are never renamed.
   - New IDs follow the prefix scheme.
   - Bump `updated:`.
   - Set `status: verified` only if Benedict says the answer was used in a real interview. Otherwise use `draft`.
3. Add a line to `changelog.md`: date · IDs · what changed · which firm or session prompted it.

**Numbers rule:** for deal figures, the Partners Group dossier values in the bank win. If a new source disagrees, flag it and ask; never silently change figures.

**Filling stubs:** interview Benedict for the facts (STAR prompts for behavioural answers; for technicals, draft and have him confirm). Then write the answer as spoken first-person prose in his voice. Don't invent experiences.

## `prep-index.md` format (the dashboard parses this: keep the columns exactly)

```
| Firm | Role | Side | Round | Interview date | Status | Folder |
|------|------|------|-------|----------------|--------|--------|
| Partners Group | Financial Analyst Program, Singapore 2027 | buy-side | Round 2 · Fit + Technicals | 2026-09-23 | Ready | Partners Group |
```
- Status is one of: `Ready`, `Draft`, `Research only`, `Applied — materials only`, `Done`.
- Use "—" for an empty cell.
- The Firm name must match the recruiting tracker's Firm column exactly, so the dashboard can link the rows.
- Also update the `_Last updated: YYYY-MM-DD_` line.

## Rules

- **Never** overwrite Benedict's original CVs or existing cover letters. Tailored files are new files. If `Benedict_Toh (<Firm>).docx` already exists, ask before replacing it.
- **Never** read or copy the portal passwords stored in `2025 Bulge Summer Applications.xlsx`.
- Don't write to `recruiting-tracker.md` from this skill. Suggest the status change and let Benedict or the tracker workflow apply it.
- Cite sources for all firm facts. Keep bank answers free of firm-specific claims: they belong in dossiers.
- Keep the dashboard-readable formats exact (bank H3 + metadata line; the prep-index table).
