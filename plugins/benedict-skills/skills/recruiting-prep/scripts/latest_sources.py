"""Finds the files Benedict's rule says to use (memory: cv-cover-letter-sources):
  CV           = newest "Benedict_Toh Resume*" by date modified
  CV layout    = newest "Benedict_Toh Resume*.docx" (used when the newest CV is a PDF)
  Cover letter = newest .docx in "Cover Letters 2027" (base template)
Also reports whether experience-log.md was built from an older CV. Works on Windows and Mac.
Usage: python latest_sources.py"""
import datetime
import re
import sys

from paths import APPS, BANK


def day(p):
    return datetime.datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d")


def newest(files):
    return max(files, key=lambda p: p.stat().st_mtime, default=None)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    cvs = [p for p in (APPS / "Resume").iterdir() if p.is_file() and p.name.startswith("Benedict_Toh Resume")]
    cv = newest(cvs)
    cv_docx = newest([p for p in cvs if p.suffix.lower() == ".docx"])
    letters = APPS / "Cover Letters 2027"
    cl = newest(list(letters.glob("*.docx")))
    print(f"CV_LATEST={cv}\nCV_LATEST_DATE={day(cv)}")
    print(f"CV_LAYOUT_DOCX={cv_docx}\nCV_LAYOUT_DATE={day(cv_docx)}")
    print(f"COVER_LETTER_BASE={cl}\nCOVER_LETTER_BASE_DATE={day(cl)}")
    for e in letters.iterdir():
        if e.is_file() and e.stat().st_size == 0:
            print(f"WARN_EMPTY_FILE={e}")
    head = "".join((BANK / "experience-log.md").read_text(encoding="utf-8-sig").splitlines(True)[:5])
    m = re.search(r"Built from: `([^`]+)` \(modified (\d{4}-\d{2}-\d{2})\)", head)
    if m:
        print(f"EXPLOG_BUILT_FROM={m.group(1)} ({m.group(2)})")
        print("EXPLOG_STALE=" + ("yes" if m.group(1) != cv.name or m.group(2) != day(cv) else "no"))
    else:
        print("EXPLOG_STALE=unknown")


if __name__ == "__main__":
    main()
