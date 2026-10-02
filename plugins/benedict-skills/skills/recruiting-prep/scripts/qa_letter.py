"""QA for a tailored cover letter or CV (.docx or .txt/.md). Works on Windows and Mac.
Flags: (1) any firm name other than the target, (2) present-tense verbs about finished internships,
       (3) leftover {Firm}/{Role}/[placeholder] tokens, (4) deal figures that don't match the Master Bank.
Usage: python qa_letter.py "<file>" "<Firm>" [alias ...]        Exit code 0 = clean, 1 = issues found."""
import re
import sys

from docx_text import docx_text
from paths import APPS, TRACKER

COMMON = ["Barclays", "Goldman Sachs", "J.P. Morgan", "JPMorgan", "Morgan Stanley", "Citi", "Citigroup", "Bank of America",
          "BofA", "UBS", "Deutsche Bank", "HSBC", "Jefferies", "Lazard", "Macquarie", "Nomura", "Mizuho", "SMBC", "MUFG",
          "BNP Paribas", "Standard Chartered", "Blackstone", "KKR", "Carlyle", "EQT", "CVC", "TPG", "Bain Capital",
          "Warburg Pincus", "Apollo", "Ares", "Brookfield", "Temasek", "GIC", "Pantheon", "Partners Group", "BlackRock",
          "Hamilton Lane", "Ardian", "Coller", "HarbourVest", "Pentagreen", "Keppel", "PwC", "EY"]
# Firms legitimately named in Benedict's own experience or deals: never flagged.
OWN = {"partners group", "pantheon", "pantheon ventures", "pwc", "pricewaterhousecoopers", "cap 1",
       "cap 1 financial group", "eqt", "shikoku", "archipelago capital partners", "smu"}


def main(path, firm, aliases):
    sys.stdout.reconfigure(encoding="utf-8")
    text = docx_text(path) if path.lower().endswith(".docx") else open(path, encoding="utf-8-sig").read()
    names = set(COMMON)
    if TRACKER.exists():
        for line in TRACKER.read_text(encoding="utf-8-sig").splitlines():
            m = re.match(r"^\|\s*([^|]+?)\s*\|", line)
            if m and not re.match(r"^\|\s*(Firm|-+)\s*\|", line):
                names.add(m.group(1))
    for d in (APPS / "Cover Letters 2027", APPS / "Cover Letters"):
        if d.exists():
            for f in d.iterdir():
                m = re.search(r"\(([^)]+)\)", f.stem)
                if f.is_file() and m:
                    names.add(m.group(1))
    target = [firm] + aliases
    issues = []
    for n in sorted(names):
        if n == "—" or len(n) < 2:
            continue
        if any(t.lower() == n.lower() or t.lower() in n.lower() or n.lower() in t.lower() for t in target):
            continue
        if n.lower() in OWN:
            continue
        for m in re.finditer(r"(?<![A-Za-z])" + re.escape(n) + r"(?![A-Za-z])", text):
            s = max(0, m.start() - 50)
            issues.append(f"WRONG FIRM '{n}': ..." + re.sub(r"\s+", " ", text[s:s + 110]) + "...")
    if firm not in text:
        issues.append(f"TARGET MISSING: '{firm}' does not appear anywhere")
    for v in ("I support", "I execute", "I conduct", "I analyse", "I analyze", "I build", "I work on", "I am interning", "I currently"):
        if re.search(re.escape(v) + r"(?![A-Za-z])", text):
            issues.append(f"TENSE: '{v}' - internship is finished, use past tense")
    for m in re.finditer(r"\{Firm\}|\{Role\}|\[(?:PLACEHOLDER|placeholder|to fill|confirm)[^\]]*\]", text):
        issues.append(f"PLACEHOLDER: {m.group(0)}")
    if re.search(r"3\.7\s?bn|3\.7 billion", text):
        issues.append("FIGURE: Kafka EV should be ~USD 3.6bn (Master Bank)")
    if re.search(r"5\.25x|6\.0x total", text):
        issues.append("FIGURE: Mosaic leverage should be ~5.3x (Master Bank)")
    if issues:
        print("ISSUES FOUND:")
        for i in sorted(set(issues)):
            print(f" - {i}")
        return 1
    print("CLEAN: no wrong firm names, tense problems, placeholders or conflicting figures found.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3:]))
