"""Where things live on any machine (Windows PC or Mac). Skills sit in <Drive>/Claude Things/.claude/skills/<skill>/."""
import os
from pathlib import Path

_here = Path(__file__).resolve()
WORKSPACE = Path(os.environ.get("BENEDICT_WORKSPACE") or next(
    (p for p in _here.parents if p.name == "Claude Things"), _here.parents[4]))
DRIVE = WORKSPACE.parent
APPS = DRIVE / "01. IB PE" / "Application Stuff (28 Aug 2026)" / "2026 Summer Applications"
BANK = WORKSPACE / "Interview Prep" / "Master Bank"
TECH_BANK = WORKSPACE / "Interview Prep" / "Technical Bank"
TRACKER = WORKSPACE / "Weekly Tracker" / "Recruiting" / "recruiting-tracker.md"
