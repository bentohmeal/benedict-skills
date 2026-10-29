"""Where things live on any machine (Windows PC or Mac). Skills sit in <Root>/Claude Things/.claude/skills/<skill>/ (<Root> = the Nextcloud GDrive folder)."""
import os
from pathlib import Path

_here = Path(__file__).resolve()
WORKSPACE = Path(os.environ.get("BENEDICT_WORKSPACE") or next(
    (p for p in _here.parents if p.name == "Claude Things"), _here.parents[4]))
DRIVE = WORKSPACE.parent
# The workspace may be a copy outside the files root, so fall back to the Nextcloud desktop folder.
if not any(DRIVE.glob("01. IB*")):
    _nc = next((p for p in (Path.home() / "Nextcloud" / "GDrive", Path("C:/Users/user/Nextcloud/GDrive")) if p.is_dir()), None)
    if _nc:
        DRIVE = _nc
# Nextcloud shows "01. IB：PE" (full-width colon); older Drive copies used "01. IB PE" / "01. IB:PE".
_ib = next(DRIVE.glob("01. IB*"), DRIVE / "01. IB：PE")
APPS = _ib / "Application Stuff (28 Aug 2026)" / "2026 Summer Applications"
BANK = WORKSPACE / "Interview Prep" / "Master Bank"
TECH_BANK = WORKSPACE / "Interview Prep" / "Technical Bank"
TRACKER = WORKSPACE / "Weekly Tracker" / "Recruiting" / "recruiting-tracker.md"
