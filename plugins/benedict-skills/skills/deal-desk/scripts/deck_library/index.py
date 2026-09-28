import json, re, os, collections
ROOT = r"C:\Users\user\Documents\Google Drive\01. IB PE\Investment Banking Library\Real IB-PE Decks"
P = json.load(open("pages.json"))
decks, pages = P["decks"], P["pages"]
for d in decks:
    if d["title"] == "here":
        d["title"] = "Kinder Morgan transaction summary (company document, not a bank deck)"
ocr = {}
for ln in open("titles.tsv", encoding="utf-8-sig"):
    if "\t" in ln:
        k, v = ln.rstrip("\n").split("\t", 1); ocr[k] = v
JUNK = re.compile(r"(?i)10xebitda|for more investment banking|confidential|preliminary draft|subject to|^\W*\d*\W*$|strictly|draft|privileged|attorney|review and|significant revision")
def title(p):
    lines = [l.strip() for l in ocr.get(os.path.basename(p["strip"]), "").split("|")]
    lines = [l for l in lines if l and not JUNK.search(l) and len(l) > 3]
    return " – ".join(lines[:2])[:110]
SECTIONS = [
 ("Executive summary / situation overview", r"executive summary|situation overview|summary of (the )?(proposal|situation)|key considerations|perspectives"),
 ("Industry / market overview", r"industry|market (overview|update|dynamics|environment|landscape)|sector|competitive landscape|macro|trends"),
 ("Company / business overview", r"company overview|business overview|company profile|at a glance|overview of [A-Z]|business description|key (operating )?metrics"),
 ("Share price / trading performance", r"share price|stock price|price performance|trading (history|performance)|shareholder"),
 ("Financial projections / management plan", r"projection|management (plan|case|forecast)|financial (overview|summary|forecast)|long[- ]range plan|business plan"),
 ("Trading comparables", r"comparable compan|trading comparables|selected (publicly )?traded|trading statistics|peer|benchmark"),
 ("Precedent transactions", r"precedent|selected (precedent )?transactions|transaction comparables"),
 ("Premiums paid", r"premiums? paid"),
 ("DCF", r"discounted cash flow|\bdcf\b"),
 ("LBO / sponsor returns", r"\blbo\b|leveraged buyout|sponsor returns|illustrative (lbo|returns)|ability to pay"),
 ("Valuation summary / football field", r"valuation summary|summary of (financial )?analys|football|preliminary valuation|valuation overview|implied (value|valuation)"),
 ("Buyer universe / parties", r"buyer|potential (acquirer|partner|counterpart)|sponsor universe|strategic (parties|buyers)|financial sponsors|universe"),
 ("Process / timeline / next steps", r"process|timeline|next steps|calendar|key dates"),
 ("Capital structure / financing", r"capital structure|financing|sources (and|&) uses|debt|liquidity|credit"),
 ("Accretion / dilution / pro forma", r"accretion|dilution|pro forma|contribution analysis|exchange ratio"),
]
def year(d):
    m = re.findall(r"(19|20)\d\d", d.get("title", "") + " " + d.get("file", ""))
    m = re.findall(r"(?:19|20)\d\d", d.get("title", "") + " " + d.get("file", ""))
    return int(m[-1]) if m else 0
rows = collections.defaultdict(list)
for p in pages:
    t = title(p); p["title"] = t
    if p["fill"] < 0.3 or not t:
        continue
    for name, rx in SECTIONS:
        if re.search(rx, t, re.I):
            rows[name].append(p); break
def ref(p):
    d = decks[p["deck"]]
    return f"{d['bank']} – {d['title']}", d["file"], p["page"]
out = ["# Real IB-PE Decks – index", "",
       "Real banker decks filed with the SEC (fairness / discussion materials, a few pitch books), downloaded from "
       "[10xebitda](https://www.10xebitda.com/investment-banking-presentations/) on 27 Sep 2026, plus BIWS training "
       "pitch books ([M&I](https://mergersandinquisitions.com/investment-banking-pitch-books/)), Citi's Chindata "
       "data-centre deck (SEC 13E-3) and Keppel DC REIT decks. Used by the deal-desk skill as the reference for "
       "slide layout and density (see `references/slide-layouts.md`).", "",
       "**Density bar measured on these decks:** body fill median 0.75 (25th pct 0.62), no empty bands; market pages "
       "0.83–0.93. Check a deck with `office.py density deck.pptx`.", "",
       "## Hand-picked reference pages (looked at, 27 Sep 2026)", "",
       "| Use it for | Deck | Page | What it shows |", "|---|---|---|---|",
       "| Market / industry page | Qatalyst Pitch Book on Autonomy (Jan-2011) (`Qatalyst\Qatalyst-Pitch-Book-on-Autonomy-Jan-2011.pdf`) | 4 | Framing strip (structured vs unstructured, facts each side) over 3 exhibits (Venn, line, bar with CAGR arrow); each exhibit has a header bar, a bold one-line finding and units |",
       "| Company page with logos | Qatalyst Pitch Book on Autonomy (Jan-2011) | 8 | Logo wall: segment header bands (Partners; Customers by vertical) over loose logos in columns, no boxes |",
       "| Full-width text page | Goldman Sachs Presentation to PowerSchool (05-Mar-2024) (`Goldman Sachs\Goldman-Sachs-Presentation-to-PowerSchool-05-Mar-2024.pdf`) | 3 | Framing box, then 2 bold lead bullets with 4–5 dash sub-points each, every one with a number (~250 words) |",
       "| Full-page table | Evercore Presentation to Diversey (01-Feb-2023) (`Evercore\Evercore-Investment-Banking-Presentation-to-Diversey-01-Feb-2023.pdf`) | 8 | Analysis at various prices: full width and height, grouped header bands, offer column boxed |",
       "| Deal summary / metrics | Citi Presentation to Chindata Special Committee (11-Aug-2023) (`_Data centres & REITs`) | 2, 5 | Navy label column + content boxes; side-by-side valuation and net debt tables |",
       "| Data-centre content | Keppel DC REIT Investor Presentation (Aug-2025) (`_Data centres & REITs`) | 9–11 | Portfolio, contract types and expiries, client base: SG data-centre metrics in an owner's format |",
       "",
       "## Best pages by section (found automatically: fullest, most recent first)", "",
       "Page titles are read by OCR from scanned SEC filings, so small spelling errors remain.", "", "| Section | Deck | Page | Page title (OCR) |", "|---|---|---|---|"]
for name, _ in SECTIONS:
    cand = sorted(rows[name], key=lambda p: (-(year(decks[p["deck"]]) >= 2019), -p["fill"]))
    seen = set(); k = 0
    for p in cand:
        if p["deck"] in seen: continue
        seen.add(p["deck"]); k += 1
        label, f, pg = ref(p)
        out.append(f"| {name if k == 1 else ''} | {label} (`{f}`) | {pg} | {p['title']} |")
        if k == 3: break
out += ["", "## All decks", "", "| Bank | Deal | Deck | Pages | File |", "|---|---|---|---|---|"]
for d in sorted(decks, key=lambda d: (d["bank"], d.get("deal", ""), d["title"])):
    out.append(f"| {d['bank']} | {d.get('deal', '')} | {d['title']} | {d.get('pages') or ''} | `{d['file']}` |")
out += ["", "Not included: Alexander Jarvis's collection (the free tier is page images only; the PDFs are paid)."]
open(os.path.join(ROOT, "_Index.md"), "w", encoding="utf-8").write("\n".join(out))
json.dump(pages, open("pages_titled.json", "w"), indent=0)
print({k: len(v) for k, v in rows.items()})
