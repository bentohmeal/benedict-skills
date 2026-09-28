import re, json, html
t = open("10x.html", encoding="utf-8").read()
out = []
for m in re.finditer(r'<div id="presentation-group-\d+".*?(?=<div id="presentation-group-\d+"|<!----------- End|\Z)', t, re.S):
    blk = m.group(0)
    logo = re.search(r'presentation-logo-popup" src="([^"]+)"', blk).group(1).rsplit("/", 1)[1]
    for g in re.finditer(r'presentation-group-title">(.*?)</h3>(.*?)(?=presentation-group-title|\Z)', blk, re.S):
        deal = html.unescape(re.sub(r"\s+", " ", g.group(1))).strip()
        for a in re.finditer(r'<a href="([^"]+)"[^>]*>(.*?)</a>', g.group(2), re.S):
            out.append({"logo": logo, "deal": deal, "url": a.group(1), "title": html.unescape(re.sub(r"<[^>]+>|\s+", " ", a.group(2))).strip()})
json.dump(out, open("10x_manifest.json", "w"), indent=1)
print(len(out)); print(sorted({o["logo"] for o in out}))
