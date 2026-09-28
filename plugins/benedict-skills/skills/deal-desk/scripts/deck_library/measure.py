import fitz, glob, os, sys, statistics as st
import numpy as np
GX, GY = 24, 14   # grid cells over the body
def pix_metrics(pix):
    a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)[:, :, :3]
    ink = (a.min(axis=2) < 235)
    h, w = ink.shape
    body = ink[int(.15*h):int(.88*h), int(.03*w):int(.97*w)]
    bh, bw = body.shape
    cells = [[body[int(i*bh/GY):int((i+1)*bh/GY), int(j*bw/GX):int((j+1)*bw/GX)].mean() > 0.004 for j in range(GX)] for i in range(GY)]
    fill = np.mean(cells)
    rows = [any(r) for r in cells]
    # longest run of empty rows (as share of body height)
    run = best = 0
    for r in rows:
        run = 0 if r else run + 1; best = max(best, run)
    return fill, best / GY
def pdf(path, pages=None):
    d = fitz.open(path); out = []
    for i, p in enumerate(d):
        if pages and i not in pages: continue
        r = p.rect
        words = [w for w in p.get_text("words") if r.height*.15 < w[1] < r.height*.88]
        f, gap = pix_metrics(p.get_pixmap(dpi=40))
        out.append((len(words), len(p.get_images()), f, gap))
    return out
def imgs(pattern):
    return [(None, None) + pix_metrics(fitz.Pixmap(f)) for f in sorted(glob.glob(pattern))]
def summ(name, rows):
    rows = [r for r in rows if r[2] > 0.05]  # skip blank / divider pages
    w = [r[0] for r in rows if r[0] is not None]
    print(f"{name:34s} n={len(rows):3d}  words med={st.median(w) if w else '-':>5}  img/pg={round(st.mean(r[1] for r in rows),1) if w else '-':>4}  fill med={st.median(r[2] for r in rows):.2f}  max-gap med={st.median(r[3] for r in rows):.2f}")
lib = r"C:/Users/user/Documents/Google Drive/01. IB PE/Investment Banking Library/Slide Inspiration/"
#summ("Citi board deck (Chindata, SEC)", imgs("citi/*.jpg"))
#summ("Keppel DC REIT acquisition deck", pdf("kdc_acq.pdf"))
#summ("Keppel DC REIT investor pres Aug25", pdf("kdc_aug25.pdf"))
#summ("Brookfield Infra investor day 2024", pdf("bip.pdf"))
#summ("KKR investor day 2024 (p1-120)", pdf("kkr.pdf", set(range(120))))
#summ("Pantheon Global Select VII (lib)", pdf(lib + "Pantheon Global Select VII_November 2024.pdf"))
for d in sys.argv[1:]:
    summ(os.path.basename(d.rstrip('/')), imgs(d + "/*.png"))
