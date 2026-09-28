# Case Gym: timed practice and post-test review

Live tests (Keppel-style: proctored, password sent over Teams) don't allow AI while they run. The gains come **before** (timed reps) and **after** (a line-by-line review). All Gym files go in `Interview Prep/Case Studies/_Gym/`.

## A. Timed mock (LBO or project finance)
1. Ask with a menu:
   - which case type (LBO · project finance · 3-statement · deck + model)
   - time limit (the real test's: LBO 105 min, PF take-home ~4h)
   - whether slides are in scope
2. Generate: `python scripts/mock_case.py lbo|pf "<_Gym>/<YYYY-MM-DD> <type>" [--minutes N]`. This writes `Brief – X.docx`, `Inputs – X.xlsx` (LBO) and `_answer/` (hidden: case.json + the verified answer model). **Never show or quote `_answer/` before he submits.**
3. Tell him: open the brief, start a timer, build in his own workbook `<Name> – Benedict.xlsx` in the same folder, and say "done" (or send the file).
4. Grade: `python scripts/grade.py "<his file>" "_answer/Answer – X.xlsx" lbo|pf --md "<folder>/Score.md"`.
5. **Review every MISS / PARTIAL / NOT FOUND yourself** before reporting. The grader matches labels and numbers; it can miss a correct line with an unusual label, or a defensible different assumption. For each real miss, find the **first** line where his numbers diverge and explain the root cause (e.g. "depreciation as % of revenue instead of the brief's policy → every line below misses").
6. Report in chat (5 lines max):
   - score
   - time used
   - top 3 root causes
   - one habit to fix next time
   - the path to Score.md
7. Log a row in `Interview Prep/Case Studies/_Gym/log.md` (create it if missing): `| Date | Type | Minutes | Score | Root causes | Fix |`. Next time, choose a case type and assumptions that hit his logged weak spots.

**3-statement and deck + model mocks:** no generator. Use a past pack from `01. IB PE\Investment Banking Library\Financial Models\` with fresh numbers (e.g. change the growth and margin notes on the PwC worksheet). Build the answer key with `financial-analysis:3-statement-model` first, into `_answer/`.

## B. Post-test review (after a real test)
1. He drops the brief + his submission into `Interview Prep/Case Studies/<Firm> <test>/`.
2. Build the answer key from the brief (write the case JSON; `build_lbo.py` / `build_pf.py`), recording every assumption the brief left open.
3. Grade, then review as in A5. Separate **errors** from **defensible alternative assumptions**. Graders usually accept a stated assumption.
4. Output `Review – <Firm>.md`:
   - score
   - what was right
   - root causes of the misses
   - the 5 questions the interviewer is most likely to ask about his model, with answers tied to his cells
   - the one habit to fix

## C. Drills (10 minutes, no Excel)
Ask 5 rapid questions from the case guides' "Formulas worth knowing cold" and "Traps" sections (e.g. "Your IRR range starts at Year 1. What happens?"). Mark each one and log the weak ones.
