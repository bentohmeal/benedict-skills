---
name: "update-study-guides"
description: "Updates Y5S1 study guides (MDA, MPW, TF) with print-ready, concise notes for new weekly content from local slides and notes. Use when: update study guides, update my notes, add week to study guide, Sunday study guide update, rebuild study guide."
---

# Update Study Guides

Adds each new week to the MDA, MPW and TF study guides (.docx). The guides are **printed for open-book exams**, so they must be complete on concepts but SHORT. Work happens on the user's computer via device_bash (edit the .docx in place with python-docx) — no Google API calls.

## Length budget (hard rule)

- Target **4–8 printed pages per week** (TF: up to ~8; MDA/MPW: 3–5). Whole guide for a semester should stay around **40–60 pages**. If a week runs over, cut before delivering.
- **Never paste or reproduce source text** (readings, slide text, statutes, rule books, blank forms, articles). The guide is *notes about* the sources, not a copy of them. The originals stay in the week folder.
- Do not embed full page renders of forms/slides. Embed only figures that carry information a table or a sentence cannot (process flows, ladders, hand-drawn diagrams), each sized small (max ~4.5in wide, ~2.8in tall; whole-page diagrams up to ~3.6in tall). If two images show the same example (e.g. lecturer whiteboard vs the student's own redraw), keep only the clearer one.
- Prefer tables over prose for comparisons, checklists, article-by-article rule summaries, and per-bank/per-instrument feature lists. One row per item, one line per rule.
- Rule books (UCP 600, URC 522, Incoterms, etc.): give a **key-rules table** (article → the exam-relevant rule, numbers, time limits, who bears what). Do not reproduce article text.
- Body font 9.5pt, margins ~0.75in, tight paragraph spacing. Skip filler sentences ("Sources covered…" can be one line).
- Before saving, convert to PDF (soffice --headless --convert-to pdf) and check the page count against the budget; look at a few pages as images.

## Folder layout

`$HOME/mnt/Y5S1/` on the device: `MDA/`, `MPW/`, `TF/`, each with `<MOD> Study Guide — Y5S1.docx` and `Week N/` folders. The connected `Y5S1` folder must be the Nextcloud one (`C:\Users\user\Nextcloud\GDrive\00. School\Y5S1`), not the old `Documents\Google Drive` copy, which is stale since Drive was retired on 2 Nov 2026; if you can't tell or `$HOME/mnt` has no `Y5S1`, say so. **No device (e.g. the Sunday cloud routine):** use the Nextcloud connector instead (ToolSearch "nextcloud"): the same tree is at `GDrive/00. School/Y5S1/` on the server. List folders to find new files (use `last_modified` for the 8-day window), read sources with `parse_document: "auto"`, fetch the guide .docx with `parse_document: "raw"` (base64) into the sandbox, edit it there, and write it back to the same path with the read's `etag` as `if_match` (content type `application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64`). Write the backup the same way. Never use Google Drive.

Source files: MDA = lecture PDFs (+ Excel exercises); MPW = AFTER CLASS PDF, Summary Email PDF, `Week X.docx`; TF = lecture PDFs/PPTX, .doc/.docx readings, personal `Week X.docx`, whiteboard/diagram photos.

## Workflow

### 0. Backup (always, before touching a guide)
Copy `<MOD> Study Guide — Y5S1.docx` to `<MOD> Study Guide — Y5S1 (backup).docx` (overwrite it) and verify sizes match. For a full rebuild, also clear the body (keep sectPr) rather than appending.
**Exactly one backup per module.** Always overwrite that single `(backup).docx`; never create dated, named ("pre-acronyms") or numbered copies. Build and check the new version in a scratch copy, then replace the guide. If any other backup copies exist at the end of a run, delete them (ask first if the environment blocks deletion).

### 1. Detect new content
`find "$HOME/mnt/Y5S1" -type f \( -name '*.pdf' -o -name '*.docx' -o -name '*.doc' -o -name '*.pptx' -o -name '*.png' -o -name '*.jpg' \) -mtime -8 | sort`. Group by module/week. Skip modules with nothing new. For a rebuild, process every week folder in order.

### 2. Read everything, then condense
Read **every** file in the week folder (stage with device_stage_files; convert .doc/.pptx with LibreOffice; OCR image-only PDFs; look at photos). Priority: personal notes (primary lens) → after-class/summary → lecture slides → readings. Then write **notes**, not a transcript. Capture, in this order of importance:
1. **Concepts/instruments/frameworks** – name, what it is, how it works (parties, steps), when it applies, how it differs from related items.
2. **Definitions** – exam-ready; quote a formal definition only if it is short and standard, with rule reference.
3. **Formulas/calculations (MDA and TF – never omit)** – formula, variables, worked example from the material (dates, fees, limits), edge cases.
4. **Rules/regulation citations** – article numbers with the one-line rule, deadlines and numbers.
5. **Process/document flows** – numbered steps, decision rules, traps.
6. **Worked examples/case studies** – one or two lines each: what it illustrates and the takeaway.
7. **Exam signals** – anything flagged by the professor.

Details that matter to an open-book exam but are easy to skip: checklists (e.g. documents to check, common discrepancies), time limits, who bears what risk/cost, and any number the lecturer used.

### 3. Flag conflicts and unclear items — do not silently fix
If notes contradict a rule book or each other (dates that don't add up, copy-paste errors in a flow, different names in text vs diagram, differing fee figures), keep the lecturer's version and add a short orange **callout** (`FLAG – …`) saying what differs. Note illegible/uncertain text instead of guessing.

### 4. Build with Style 1 — Claude Orange
Use the shared helpers (colors ORANGE E8673A, DARK 1A1A1A, MID 555555, peach FFF4F0): `week_heading`, `section_head`, `sub_head`, `concept`, `body`, `bullet`, `step`, `takeaway`, `formula_box`, `callout`, `table` (orange header row, alternating rows, header repeat, explicit column widths incl. tblGrid), `embed_original_image`.

Document structure rules:
- Week title = real Word **Heading 1** (page break before) with Style 1 look; each section (Key Concepts, Definitions, Formulas, Rules, Process, Case Examples, Exam Takeaways) = real **Heading 2** with Style 1 look, so the navigation pane and TOC work.
- A **Table of Contents field** (`TOC \o "1-2" \h \z \u`) sits at the top, pre-populated with page numbers (compute from a first-pass PDF) and marked dirty so Word can update it (right-click → Update Field).
- Images: extract originals from the source (pptx/docx media, PDF crops, photos); never redraw. `embed_original_image()` must preserve aspect ratio, scale to the size caps above, cross-reference duplicates by md5 instead of re-embedding, and keep a ledger (embedded / duplicate / skipped-decorative) for the report. Skip logos and decorative clip-art.
- Module section sets — MDA: Key Concepts, Definitions, Formulas/Models, Excel Skills & Functions, Exam Takeaways. MPW: Theories & Frameworks, Key Concepts & Definitions, Research Findings, Application Examples, Exam Takeaways. TF: Key Concepts & Instruments, Definitions, Formulas/Calculations, Legal & Regulatory Rules, Process & Document Flow, Case Examples, Exam Takeaways.
- No placeholders ("...", "see slides"). If a section has nothing for the week, write one sentence saying why.

### 5. Save and deliver
Save in place (or commit the rebuilt file with device_commit_files using the recorded mtime so a newer edit is never overwritten). Do not touch modules the user did not ask about.

### 6. Report (short)
Weeks processed; images embedded vs cross-referenced vs skipped; final page count and word count; conflicts flagged; anything that could not be read (e.g. XFA/dynamic PDF forms only show "Please wait…" — read their template fields instead); where the backup is.

## Module reference

| Module | Course | Extraction targets |
|---|---|---|
| MDA | Modeling & Data Analytics (COR1305) | Excel functions + syntax, modeling techniques, formulas with worked examples, interpretation |
| MPW | Managing People at Work (OBHR101) | OB theories, research evidence, applications, compare/contrast across weeks |
| TF | Trade Finance (FNCE310) | Instruments, party obligations, document flows, UCP/URC rule numbers, numerical calculations (fees, tenors, maturity dates, credit limits) |