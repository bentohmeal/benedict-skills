"""Where things live, on any machine (Windows PC or Mac).

The skills sit in <Drive>/Claude Things/.claude/skills/<skill>/, so everything is found from this file's own
location: no user names, drive letters or hard-coded paths. Override with BENEDICT_WORKSPACE if the folder moves.

    import paths
    paths.WORKSPACE   # .../Claude Things
    paths.DRIVE       # the Google Drive root that holds Claude Things, 01. IB PE, 00. School ...
    paths.TOOLKIT     # .../Claude Things/output/_Deal Desk Toolkit
    paths.IBPE        # .../01. IB PE
    paths.REAL_DECKS  # .../01. IB PE/Investment Banking Library/Real IB-PE Decks
    paths.SLIDE_INSPIRATION
"""
import os
from pathlib import Path


def _workspace():
    env = os.environ.get("BENEDICT_WORKSPACE")
    if env:
        return Path(env)
    here = Path(__file__).resolve()
    for p in here.parents:
        if p.name == "Claude Things":
            return p
    return here.parents[4]          # scripts -> deal-desk -> skills -> .claude -> Claude Things


WORKSPACE = _workspace()
DRIVE = WORKSPACE.parent
TOOLKIT = WORKSPACE / "output" / "_Deal Desk Toolkit"
IBPE = DRIVE / "01. IB PE"
LIBRARY = IBPE / "Investment Banking Library"
REAL_DECKS = LIBRARY / "Real IB-PE Decks"
SLIDE_INSPIRATION = LIBRARY / "Slide Inspiration"
IS_WINDOWS = os.name == "nt"
