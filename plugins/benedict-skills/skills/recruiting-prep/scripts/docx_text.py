"""Prints the plain text of a .docx (one paragraph per line; headings prefixed with [StyleName]).
Usage: python docx_text.py "<file.docx>"
Uses regex, not an XML parser, because some of Benedict's docs contain malformed XML. Works on Windows and Mac."""
import html
import re
import sys
import zipfile


def docx_text(path):
    with zipfile.ZipFile(path) as z:
        x = z.read("word/document.xml").decode("utf-8", errors="replace")
    out = []
    for m in re.finditer(r"<w:p[ >].*?</w:p>", x, re.S):
        t = html.unescape("".join(re.findall(r"<w:t(?: [^>]*)?>([^<]*)</w:t>", m.group(0))))
        if t.strip():
            st = re.search(r'<w:pStyle w:val="(Heading[^"]*|Title)"', m.group(0))
            out.append(f"[{st.group(1)}] {t}" if st else t)
    return "\n".join(out)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(docx_text(sys.argv[1]))
