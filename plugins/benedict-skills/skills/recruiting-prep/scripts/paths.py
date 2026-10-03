"""Where things live on any machine (Windows PC or Mac). Skills sit in <Drive>/Claude Things/.claude/skills/<skill>/."""
import os
from pathlib import Path

_here = Path(__file__).resolve()
WORKSPACE = Path(os.environ.get("BENEDICT_WORKSPACE") or next(
    (p for p in _here.parents if p.name == "Claude Things"), _here.parents[4]))
DRIVE = WORKSPACE.parent
# Mac: the workspace may be a mirrored copy outside Drive, so fall back to the Google Drive folder.
if not any(DRIVE.glob("01. IB*")):
    _gd = next(Path.home().glob("Library/CloudStorage/GoogleDrive-*/My Drive"), None)
    if _gd:
        DRIVE = _gd
# The PC names the folder "01. IB PE"; the Mac shows "01. IB:PE".
_ib = next(DRIVE.glob("01. IB*"), DRIVE / "01. IB PE")
APPS = _ib / "Application Stuff (28 Aug 2026)" / "2026 Summer Applications"
BANK = WORKSPACE / "Interview Prep" / "Master Bank"
TECH_BANK = WORKSPACE / "Interview Prep" / "Technical Bank"
TRACKER = WORKSPACE / "Weekly Tracker" / "Recruiting" / "recruiting-tracker.md"
