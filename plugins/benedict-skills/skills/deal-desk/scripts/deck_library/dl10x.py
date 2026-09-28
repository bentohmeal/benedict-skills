"""Download every 10xebitda deck into Real IB-PE Decks/<Bank>/, plus SEC htm decks stitched to PDF, BIWS, Citi-Chindata, Keppel."""
import json, os, re, time, urllib.request, shutil, glob
import pymupdf
ROOT = r"C:\Users\user\Documents\Google Drive\01. IB PE\Investment Banking Library\Real IB-PE Decks"
BANK = {'BofA-Securities-Logo.jpg': 'BofA Securities', 'Jefferies-Logo.jpg': 'Jefferies', 'SVB-Securities-Logo.jpg': 'SVB Securities - Leerink',
        'evercore-logo.png': 'Evercore', 'goldman-sachs-logo.png': 'Goldman Sachs', 'lgoo-perella-weinberg.png': 'Perella Weinberg',
        'logo-barclays.png': 'Barclays', 'logo-centerview-partners.png': 'Centerview', 'logo-citi.png': 'Citi', 'logo-credit-suisse.png': 'Credit Suisse',
        'logo-deutsche-bank.png': 'Deutsche Bank', 'logo-duff-phelps.png': 'Duff & Phelps', 'logo-houlihan-lokey.png': 'Houlihan Lokey',
        'logo-jp-morgan.png': 'J.P. Morgan', 'logo-lazard.png': 'Lazard', 'logo-liontree.png': 'LionTree', 'logo-moelis-company.png': 'Moelis',
        'logo-morgan-stanley.png': 'Morgan Stanley', 'logo-qatalyst.png': 'Qatalyst', 'pjt-logo.png': 'PJT Partners'}
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36"}
SEC_UA = {"User-Agent": "Benedict Toh research benedict2588@gmail.com"}
def get(url, hdr=UA):
    for k in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=hdr), timeout=120) as r:
                return r.read()
        except Exception as e:
            err = e; time.sleep(3)
    raise err
def sec_htm_to_pdf(url, out):
    """SEC exhibit pages are HTML with one JPG/GIF per slide: stitch them into a PDF."""
    page = get(url, SEC_UA).decode("latin-1")
    base = url.rsplit("/", 1)[0]
    imgs = re.findall(r'<img[^>]+src="([^"]+)"', page, re.I)
    doc = pymupdf.open()
    for im in imgs:
        data = get(im if im.startswith("http") else f"{base}/{im}", SEC_UA); time.sleep(0.15)
        pic = pymupdf.open(stream=data, filetype=im.rsplit(".", 1)[1].lower())
        doc.insert_pdf(pymupdf.open("pdf", pic.convert_to_pdf()))
    doc.save(out)
    return len(imgs)
def safe(s):
    return re.sub(r'[\/:*?"<>|]', "-", s).strip()
log = []
man = json.load(open("10x_manifest.json"))
for m in man:
    bank = BANK[m["logo"]]; d = os.path.join(ROOT, bank); os.makedirs(d, exist_ok=True)
    url = m["url"]
    try:
        if url.lower().endswith(".pdf"):
            fn = url.rsplit("/", 1)[1]; out = os.path.join(d, fn)
            if not os.path.exists(out):
                open(out, "wb").write(get(url)); time.sleep(0.5)
        else:
            fn = safe(m["title"]) + ".pdf"; out = os.path.join(d, fn)
            if not os.path.exists(out):
                sec_htm_to_pdf(url, out)
        pages = pymupdf.open(out).page_count
        log.append({**m, "bank": bank, "file": os.path.relpath(out, ROOT), "pages": pages, "ok": True})
    except Exception as e:
        log.append({**m, "bank": bank, "ok": False, "error": str(e)[:200]})
    print(len(log), bank, m["title"][:60], log[-1].get("pages", log[-1].get("error")), flush=True)
# extras
ex = os.path.join(ROOT, "_Training pitch books"); os.makedirs(ex, exist_ok=True)
for nm in ["Jazz-Pharmaceuticals-Investment-Banking-Pitch-Book", "KeyBank-First-Niagara-MA-Discussion", "Netflix-Equity-Debt-Convertible-Investment-Banking-Pitch-Book"]:
    for ext in ("pdf", "pptx"):
        out = os.path.join(ex, f"{nm}.{ext}")
        try:
            if not os.path.exists(out):
                open(out, "wb").write(get(f"https://biws-support.s3.amazonaws.com/Pitch-Books/{nm}.{ext}"))
            log.append({"bank": "BIWS (training)", "deal": nm.replace("-", " "), "title": nm, "file": os.path.relpath(out, ROOT), "ok": True,
                        "pages": pymupdf.open(out).page_count if ext == "pdf" else None, "url": f"https://biws-support.s3.amazonaws.com/Pitch-Books/{nm}.{ext}"})
        except Exception as e:
            log.append({"bank": "BIWS (training)", "title": nm + "." + ext, "ok": False, "error": str(e)[:200]})
dc = os.path.join(ROOT, "_Data centres & REITs"); os.makedirs(dc, exist_ok=True)
here = os.path.dirname(os.path.abspath(__file__))
cit = os.path.join(dc, "Citi Presentation to Chindata Special Committee (11-Aug-2023).pdf")
doc = pymupdf.open()
for j in sorted(glob.glob(os.path.join(here, "citi", "*.jpg"))):
    doc.insert_pdf(pymupdf.open("pdf", pymupdf.open(j).convert_to_pdf()))
doc.save(cit)
log.append({"bank": "Citi", "deal": "Take-private of Chindata by Bain Capital (data centres)", "title": "Citi Presentation to Chindata Special Committee (11-Aug-2023)",
            "file": os.path.relpath(cit, ROOT), "pages": doc.page_count, "ok": True,
            "url": "https://www.sec.gov/Archives/edgar/data/1807192/000119312523222651/d439052dex99c2.htm"})
for src, nm, url in [("kdc_aug25.pdf", "Keppel DC REIT Investor Presentation (Aug-2025).pdf", "https://www.keppeldcreit.com/en/file/investor-relations/presentations/2025/kdcreit-aug-2025-presentation.pdf"),
                     ("kdc_acq.pdf", "Keppel DC REIT Acquisition of Keppel DC Singapore 3 & 4 (Dec-2025).pdf", "https://www.keppeldcreit.com/en/file/investor-relations/presentations/2025/kdcreit-acquisition-of-remaining-interests-in-sgp-3-and-4.pdf")]:
    shutil.copy(os.path.join(here, src), os.path.join(dc, nm))
    log.append({"bank": "Keppel DC REIT (issuer)", "deal": nm[:-4], "title": nm[:-4], "file": os.path.relpath(os.path.join(dc, nm), ROOT),
                "pages": pymupdf.open(os.path.join(dc, nm)).page_count, "ok": True, "url": url})
json.dump(log, open(os.path.join(here, "library_log.json"), "w"), indent=1)
print("DONE ok=", sum(l["ok"] for l in log), "failed=", sum(not l["ok"] for l in log))
