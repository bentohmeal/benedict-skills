# Real IB-PE Decks library: how it was built (27 Sep 2026)

Run from a scratch folder, in this order (Python 3.12 full path; see SKILL.md):
1. `curl` the 10xebitda page to `10x.html`, then `parse10x.py` → `10x_manifest.json` (bank, deal, link).
2. `dl10x.py` downloads every deck into `01. IB PE\Investment Banking Library\Real IB-PE Decks\<Bank>\` (SEC `.htm`
   decks are stitched from their page images into PDFs) and adds the BIWS, Citi–Chindata and Keppel DC REIT files.
3. `strips.py` renders each page's title strip and measures its fill (`measure.py`, same method as `office.py density`).
4. `ocr.ps1 -Dir titles -Out titles.tsv` reads the titles with Windows' built-in OCR (most SEC decks are scans).
5. `index.py` writes `_Index.md` (hand-picked pages + best page per section + all decks).
