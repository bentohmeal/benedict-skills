---
name: "update-study-guides"
description: "Updates Y5S1 study guides (MDA, MPW, TF) with print-ready, concise notes for new weekly content from local slides and notes. Use when: update study guides, update my notes, add week to study guide, Sunday study guide update, rebuild study guide."
---

# Update Study Guides

Adds each new week's content to the MDA, MPW and TF study guides (.docx). The guides are **printed for open-book exams**, so they must be complete on concepts but SHORT. Work happens on the user's computer via device_bash (edit the .docx in place with python-docx). No Google API calls.

**Layouts differ by module:**
- **MDA and MPW are organised by week.** Each new week is added as its own section at the end.
- **TF is organised by topic (since 1 Nov 2026).** New content is slotted into the matching topic, never added as a week section at the end. See "TF by-topic rules" below.

## Length budget (hard rule)

- MDA/MPW: target **3–5 printed pages per week**, about 40–60 pages per guide. TF is organised by topic and is about 100 pages because diagrams are full width. Keep new TF notes to about 2–4 pages per week of new material.
- **Never paste or reproduce source text** (readings, slide text, statutes, rule books, blank forms, articles). The guide is *notes about* the sources, not a copy. The originals stay in the week folder.
- Do not embed full-page renders of forms or slides. Embed only figures that carry information a table or a sentence cannot (process flows, ladders, diagrams). Lecturer/reading images: max ~4.5in wide, ~2.8in tall (whole-page diagrams up to ~3.6in tall). Benedict's own drawings: see the image rules below (full width).
- Prefer tables over prose for comparisons, checklists, article-by-article rule summaries, and per-bank or per-instrument feature lists. One row per item, one line per rule.
- Rule books (UCP 600, URC 522, ISP 98, Incoterms, etc.): give a **key-rules table** (article → the exam-relevant rule, numbers, time limits, who bears what). Do not reproduce article text.
- Body font 9.5pt, margins ~0.75in, tight paragraph spacing. Skip filler sentences.
- Before saving, convert to PDF (`soffice --headless --convert-to pdf`) on the device, which has the real fonts, check the page count and look at a few pages as images.

## Folder layout

`$HOME/mnt/Y5S1/` on the device: `MDA/`, `MPW/`, `TF/`, each with `<MOD> Study Guide — Y5S1.docx` (+ `(print).pdf` for TF) and `Week N/` folders. TF also has `.study-guide-ledger.json` (files already incorporated). Update the ledger after every TF run. The connected `Y5S1` folder must be the Nextcloud one (`C:\Users\user\Nextcloud\GDrive\00. School\Y5S1`), not the old `Documents\Google Drive` copy, which has been stale since Drive was retired on 2 Nov 2026. If you can't tell, or `$HOME/mnt` has no `Y5S1`, say so.

**No device (e.g. the Sunday cloud routine):** use the Nextcloud connector (ToolSearch "nextcloud"). The same tree is at `GDrive/00. School/Y5S1/` on the server.
- List folders to find new files (use `last_modified` for the 8-day window).
- Read sources with `parse_document: "auto"`.
- Fetch the guide .docx with `parse_document: "raw"` (base64) into the sandbox and edit it there.
- Write it back to the same path with the read's `etag` as `if_match` (content type `application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64`). Write the backup the same way.
- Never use Google Drive.

Source files: MDA = lecture PDFs (+ Excel exercises); MPW = AFTER CLASS PDF, Summary Email PDF, `Week X.docx`; TF = lecture PDFs/PPTX, .doc/.docx readings, personal `Week X.docx`, whiteboard photos and Benedict's own drawings (PNG/JPG).

**Output location:** the updated guide always replaces `<MOD> Study Guide — Y5S1.docx` in its own module folder (and, for TF, `(print).pdf` next to it). Never leave the result only in `Claude Things/output`.

## Workflow

### 0. Backup (always, before touching a guide)
Copy `<MOD> Study Guide — Y5S1.docx` to `<MOD> Study Guide — Y5S1 (backup).docx` (overwrite it) and verify the sizes match.
- **Exactly one backup per module.** Always overwrite that single `(backup).docx`. Never create dated, named or numbered copies.
- Build and check the new version in a scratch copy, then replace the guide.
- If other backup or old copies exist at the end of a run (e.g. `(old, by week)`), delete them; ask first if the environment blocks deletion.
- Scratch files go in `$HOME/work` on the device, or the sandbox, never inside the user's folders. If something must be staged through a connected folder, remove it at the end.

### 1. Detect new content
`find "$HOME/mnt/Y5S1" -type f \( -name '*.pdf' -o -name '*.docx' -o -name '*.doc' -o -name '*.pptx' -o -name '*.png' -o -name '*.jpg' \) -mtime -8 | sort`. Also check the TF ledger for files never processed, which can be older than 8 days. Group by module and week. Skip modules with nothing new.

### 2. Read everything, then condense
Read **every** new file: stage with device_stage_files; convert .doc/.pptx with LibreOffice; OCR image-only PDFs (tesseract on the device); look at every photo and drawing. Priority: personal notes (primary lens) → after-class/summary → lecture slides → readings.

Then write **notes**, not a transcript. Capture, in this order of importance:
1. **Concepts/instruments/frameworks**: name, what it is, how it works (parties, steps), when it applies, how it differs from related items.
2. **Definitions**: exam-ready. Quote a formal definition only if it is short and standard, with the rule reference.
3. **Formulas/calculations (MDA and TF, never omit)**: formula, variables, worked example from the material (dates, fees, limits), edge cases.
4. **Rules/regulation citations**: article numbers with the one-line rule, deadlines and numbers.
5. **Process/document flows**: numbered steps, decision rules, traps.
6. **Worked examples/case studies**: one or two lines each, saying what it illustrates and the takeaway.
7. **Exam signals**: anything the professor flagged.

Details that matter in an open-book exam but are easy to skip: checklists (e.g. documents to check, common discrepancies), time limits, who bears what risk or cost, and any number the lecturer used.

### 3. Flag conflicts and unclear items; do not silently fix
If notes contradict a rule book or each other (dates that don't add up, copy-paste errors in a flow, different names in text and diagram, differing fee figures, step numbers used twice, a cut-off label), keep the source's version and add a short orange **callout** (`FLAG – …`) saying what differs. Note illegible or uncertain text instead of guessing.

### 4. Build with Style 1 (Claude Orange)
Use the shared helpers (colours ORANGE E8673A, DARK 1A1A1A, MID 555555, peach FFF4F0): `week_heading` / `topic_heading`, `section_head`, `src_tag`, `sub_head`, `concept`, `body`, `bullet`, `step`, `takeaway`, `formula_box`, `callout`, `caption`, `table` (orange header row, alternating rows, header repeat, explicit column widths incl. tblGrid).

Document structure rules:
- Week or topic title = real Word **Heading 1** (page break before) with the Style 1 look. Each section = real **Heading 2** with the Style 1 look, so the navigation pane and TOC work.
- A **Table of Contents field** (`TOC \o "1-2" \h \z \u`) sits at the top, pre-populated with page numbers computed from a device-rendered PDF, and marked dirty so Word can update it.
- Module section sets:
  - MDA: Key Concepts, Definitions, Formulas/Models, Excel Skills & Functions, Exam Takeaways.
  - MPW: Theories & Frameworks, Key Concepts & Definitions, Research Findings, Application Examples, Exam Takeaways.
  - TF: Key Concepts & Instruments, Definitions, Formulas/Calculations, Legal & Regulatory Rules, Process & Document Flow, Case Examples, Exam Takeaways (plus the topic's special sections).
- No placeholders ("...", "see slides").

### 5. Image rules
- **Lecturer slides, reading figures, whiteboard photos:** embed the original (pptx/docx media, PDF crops, photos); never redraw these unless asked. Preserve aspect ratio, apply the size caps above, cross-reference duplicates by md5 instead of re-embedding. Skip logos and decorative clip-art.
- **Benedict's own drawings (any module):** **redraw** each one as a clean diagram and embed it at **full text width (~7in)**, never the original photo.
  - Keep his parties, arrows, sequence, step numbers and labels **exactly as drawn**; do not add or correct anything. Anything wrong or unclear goes in a `FLAG –` callout under the caption.
  - The diagram must print legibly in black and white: rounded boxes (orange outline = traders, navy = banks); arrows whose **line style** carries the meaning (solid = contract/apply/issue/advise, dashed = documents, thick = payment, dotted = goods, dash-dot = claim/demand, short-dash with ✗ = failure); numbered circles at the start of each label; a legend strip; minimum ~7.5pt text at print size; white label backgrounds so labels never sit on lines.
  - Render with matplotlib at 300 dpi and check every diagram as an image before embedding, fixing any overlaps or clipped text.
  - Under each diagram: a one-line italic caption ("Figure – what it shows. Redrawn from <file> (Week N)."), set keep-with-next if a FLAG follows.
- Keep a ledger (embedded / redrawn / duplicate / skipped) for the report.

### 6. TF by-topic rules (TF only)
The TF guide's order is:
1. Front matter: title, **Topic Index** table (#, topic, weeks it comes from, page), Quick Finder tables (Topic, Where = "Topic N", Page), Contents.
2. Reference (acronyms).
3. Topics 1–13.
4. Appendix "Sources Covered (by week)".
5. A–Z keyword index.

The topics are:
1. Foundations of International Trade
2. Methods of Payment & the Payments Risk Ladder
3. Documentary Collections (D/P, D/A) – URC 522
4. Documentary Credits (L/Cs) – Fundamentals & UCP 600
5. Sight, Usance & Confirmed L/Cs
6. Shipping Documents, Discrepancies & L/C Application Forms
7. Incoterms 2020
8. Transferable & Back-to-Back L/Cs
9. Anticipatory Credits – Red Clause & Green Clause L/Cs
10. Standby L/Cs & Bank Guarantees
11. Shipping Guarantees, Trust Receipts & Other Banking Facilities
12. Trade Credit Insurance
13. Exam Practice – Sample Midterm, Test 1 Traps & Drill

When adding new weekly content:
- **Split by topic, not by week.** Each concept, definition, formula, rule, flow, case and takeaway goes into the matching topic's section (Key Concepts & Instruments, Definitions, Formulas/Calculations, Legal & Regulatory Rules, Process & Document Flow, Case Examples, Exam Takeaways). Inside a section, blocks are ordered by week, each group headed by a small grey source tag ("From Week 12").
- **Diagrams sit next to the text they explain**, inside that topic (usually Process & Document Flow, or right after the concept). Never park them in a separate figures section or another week.
- **New topic:** if content fits no existing topic, add a new numbered topic before Exam Practice (renumber Exam Practice to stay last), add it to the Topic Index, and say so in the report. Exam-format notes, sample questions and drills go to Exam Practice.
- **Never reword, shorten or remove existing content** when adding to a topic. Existing blocks are only ever moved, not edited. If new material repeats something already there, add only what is new and note the overlap in one line.
- Add the week's "Sources covered" line to the Appendix, and add new diagrams as Quick Finder rows ("1. Flow diagrams" table) plus other Quick Finder tables where relevant.
- **After saving, refresh all page numbers from the device-rendered PDF:** TOC entries (headings found in order), Topic Index pages (topic H1 pages), Quick Finder pages (find each row's anchor text, searching from the Reference section onwards), and the A–Z index (the 3 pages that use each term most).
- Running headers: one Word section per topic, header "TF · TOPIC N · Title ▸ STYLEREF Heading 2". Strip any stray section breaks carried in from copied paragraphs.
- **Completeness check before delivering:** compare every paragraph and table cell of the previous guide with the new one. Everything must still be present, apart from page numbers and captions you deliberately replaced. Report the result.

### 7. Save and deliver
Save in place in the module folder (or commit the rebuilt file with device_commit_files using the recorded mtime so a newer edit is never overwritten). For TF also replace `TF Study Guide — Y5S1 (print).pdf`. Update the TF ledger. Do not touch modules the user did not ask about.

### 8. Report (short)
- Weeks processed, and for TF which topic each new item went into.
- Images embedded / redrawn / cross-referenced / skipped.
- Final page count; conflicts flagged; completeness-check result (TF).
- Anything that could not be read (e.g. XFA/dynamic PDF forms only show "Please wait…"; read their template fields instead).
- Where the guide and backup are.

## Module reference

| Module | Course | Layout | Extraction targets |
|---|---|---|---|
| MDA | Modeling & Data Analytics (COR1305) | By week | Excel functions + syntax, modeling techniques, formulas with worked examples, interpretation |
| MPW | Managing People at Work (OBHR101) | By week | OB theories, research evidence, applications, compare/contrast across weeks |
| TF | Trade Finance (FNCE310) | By topic | Instruments, party obligations, document flows, UCP/URC/ISP rule numbers, numerical calculations (fees, tenors, maturity dates, credit limits, advances) |
