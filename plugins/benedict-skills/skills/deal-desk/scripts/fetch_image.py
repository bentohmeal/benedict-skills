"""Fetch photos, maps and logos for slides from Wikimedia (Commons or English Wikipedia), with the credit kept.

    python fetch_image.py search "Equinix logo"            # file titles on Commons, then en.wikipedia
    python fetch_image.py get "File:Equinix logo.svg" equinix [--width 800]

    from fetch_image import get, credit
    path = get("File:Equinix logo.svg", "equinix")          # PNG in assets/images/, cached
    credit("equinix")                                       # "Equinix logo.svg (Wikimedia Commons, public domain)"

SVGs come back as Wikimedia's PNG render. Every download is logged in assets/images/manifest.json (source page,
licence, author) so the deck's "Sources:" line can credit it (Deck.photo() does this automatically).
Logos are trademarks: fine on internal / pitch materials, which is how banks use them.
"""
import json
import os
import re
import sys
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.normpath(os.path.join(HERE, "..", "assets", "images"))
MANIFEST = os.path.join(IMG_DIR, "manifest.json")
UA = {"User-Agent": "deal-desk-slides/1.0 (benedict2588@gmail.com)"}
APIS = {"commons": "https://commons.wikimedia.org/w/api.php", "en": "https://en.wikipedia.org/w/api.php"}


def _api(site, **params):
    params.update(format="json", formatversion=2)
    url = APIS[site] + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return json.load(r)


def _manifest():
    try:
        return json.load(open(MANIFEST, encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def search(query, n=8):
    """File titles matching the query: Commons first (free licences), then English Wikipedia (logos, fair use)."""
    out = []
    for site in ("commons", "en"):
        try:
            res = _api(site, action="query", list="search", srsearch=query, srnamespace=6, srlimit=n)
        except (OSError, ValueError, KeyError):
            continue
        out += [(site, h["title"]) for h in res["query"]["search"]]
    return out


def article_image(article, site="en"):
    """The lead image of a Wikipedia article (usually the infobox logo), as a 'File:...' title, or None.
    Use it for logos Commons doesn't hold (e.g. AirTrunk, Princeton Digital Group)."""
    res = _api(site, action="query", titles=article, prop="pageimages", piprop="name", pilicense="any", redirects=1)
    page = res["query"]["pages"][0]
    return f"File:{page['pageimage']}" if "pageimage" in page else None


def _info(title, width):
    for site in ("commons", "en"):
        res = _api(site, action="query", titles=title, prop="imageinfo", iiprop="url|extmetadata|size",
                   iiurlwidth=width)
        page = res["query"]["pages"][0]
        if "imageinfo" in page:
            return site, page["imageinfo"][0]
    raise LookupError(f"{title} not found on Commons or en.wikipedia")


def get(title, name, width=800):
    """Download `title` (a 'File:...' name) as PNG/JPG to assets/images/<name>.<ext>; returns the path."""
    os.makedirs(IMG_DIR, exist_ok=True)
    man = _manifest()
    if name in man and os.path.exists(man[name]["path"]):
        return man[name]["path"]
    site, ii = _info(title, width)
    url = ii.get("thumburl") or ii["url"]
    ext = os.path.splitext(urllib.parse.urlparse(url).path)[1].lower() or ".png"
    ext = ".png" if ext == ".svg" else ext
    path = os.path.join(IMG_DIR, name + ext)
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
        open(path, "wb").write(r.read())
    meta = ii.get("extmetadata", {})
    clean = lambda k: re.sub(r"<[^>]+>", "", meta.get(k, {}).get("value", "")).strip()
    man[name] = {"path": path, "title": title, "site": "Wikimedia Commons" if site == "commons" else "Wikipedia",
                 "page": ii.get("descriptionurl", ""), "licence": clean("LicenseShortName") or "see page",
                 "author": clean("Artist")[:80]}
    json.dump(man, open(MANIFEST, "w", encoding="utf-8"), indent=1)
    return path


def credit(name):
    """One short credit for the Sources line."""
    m = _manifest().get(name)
    if not m:
        return ""
    who = f"{m['author']}, " if m["author"] and "logo" not in m["title"].lower() else ""
    return f"{who}{m['site']} ({m['licence']})"


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "search":
        for site, t in search(" ".join(args)):
            print(site, "|", t)
    elif cmd == "article":
        print(article_image(" ".join(args)))
    elif cmd == "get":
        w = int(args[args.index("--width") + 1]) if "--width" in args else 800
        print(get(args[0], args[1], w))
