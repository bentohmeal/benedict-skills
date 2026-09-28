import pymupdf, json, os, glob
from measure import pix_metrics
ROOT = r"C:\Users\user\Documents\Google Drive\01. IB PE\Investment Banking Library\Real IB-PE Decks"
log = [l for l in json.load(open("library_log.json")) if l["ok"] and l["file"].lower().endswith(".pdf")]
pages = []
for di, l in enumerate(log):
    d = pymupdf.open(os.path.join(ROOT, l["file"]))
    for i, p in enumerate(d):
        r = p.rect
        if r.width < r.height:
            continue
        pix = p.get_pixmap(dpi=40)
        fill, gap = pix_metrics(pix)
        txt = " ".join(w[4] for w in p.get_text("words") if w[1] < r.height * 0.2 and "10xebitda" not in w[4].lower())
        clip = pymupdf.Rect(0, 0, r.width, r.height * 0.2)
        fn = f"titles/{di:03d}_{i+1:03d}.png"
        p.get_pixmap(dpi=110, clip=clip).save(fn)
        pages.append({"deck": di, "page": i + 1, "fill": round(fill, 2), "text_top": txt[:200], "strip": fn})
json.dump({"decks": log, "pages": pages}, open("pages.json", "w"), indent=0)
print(len(log), "decks", len(pages), "pages")
