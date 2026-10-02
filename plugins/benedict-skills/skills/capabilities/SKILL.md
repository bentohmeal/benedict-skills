---
name: capabilities
description: "Lists everything Claude is set up to do for Benedict (skills, automatic routines, dashboard, where data lives) from CAPABILITIES.md, checks the list is still accurate, and offers to start any of them. Triggers: /capabilities, 'what can you do', 'what can you do for me', 'what's set up', 'what do I have', 'remind me what you can do', 'list your skills'."
model: haiku
effort: low
---

# Capabilities: what Claude can do for Benedict

> **Drive root `<Drive>`:** PC `C:\Users\user\Documents\Google Drive` · Mac `~/Library/CloudStorage/GoogleDrive-benedict2588@gmail.com/My Drive` (run `ls ~/Library/CloudStorage` to confirm the folder name). Paths below are relative to `<Drive>`; use `/` on the Mac. This skill lives in `<Drive>/Claude Things/.claude/skills/` (shared by PC and Mac through Drive), so edit it there.

Source of truth: `<Drive>\Claude Things\CAPABILITIES.md`. Read it fully every time. Never answer from memory.

## Step 1: Quick accuracy check (silent unless something is off)
1. List the live routines with `RemoteTrigger` (action `list`). Compare the enabled ones (name, schedule) with section 2 of CAPABILITIES.md.
2. List the skill folders in `<Drive>\Claude Things\.claude\skills\` (and, if present, `~/.claude/skills/`) (ignore `capabilities`, `.trash`) **and the skill folders inside `synced\<id>\`**. Compare them with section 3 of the file. Also compare with the skills listed in the current session's skill list, and the connected apps in the session's tool list. Anything installed or connected that the file doesn't mention gets added.
3. If anything differs (a routine missing from the file, a listed routine that no longer exists or is switched off, a skill not listed), **fix CAPABILITIES.md** and update its `_Last updated_` date. Then mention it in one line at the end ("Updated the list: added X, removed Y").
4. If a tool isn't available, skip that check silently.

## Step 2: Do NOT print the long list
He only wants the menu. Skip listing skills, routines, pages, apps or data locations. Show the full list only if he asks for it ("show the full list", or asks about one area, in which case show just that area with a little more detail). If Step 1 changed CAPABILITIES.md, add one line ("Updated the list: added X, removed Y").

## Step 3: Menu (this is the whole output)
Never build the menu from deadlines or "what's likely useful". Use AskUserQuestion in two steps (max 4 options each). Mention any deadline in the next 7 days from `School/SCHOOL-TRACKER.md` only in the option description.

**Step 3a: "What do you want to start?"**
1. **School**: school work, what's due, study guides
2. **Recruiting & interviews**: firm prep, CV, cover letter, mock interview
3. **Models, decks & case tests**: IB / private markets work
4. **Fitness, money & more**: everything else

**Step 3b: ask a second question for the sub-choice**
- School → School work · What's due · Update study guides
- Recruiting & interviews → Prep for a firm · CV / cover letter · Update an answer · Mock interview
- Models, decks & case tests → Build a model · Make a deck · Case study / practice case · Check my model or deck
- Fitness, money & more → Fitness coach · Expense tracker · Morning brief · Dashboard / other (this last one opens a third question: Dashboard link · Routines · Research / Notion / Gamma / other tools)

Then invoke the matching skill. Every skill and section in the file must be reachable from this menu.
