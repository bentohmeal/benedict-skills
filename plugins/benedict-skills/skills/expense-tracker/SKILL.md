---
name: expense-tracker
description: "Refresh Benedict's expense tracker by pulling DBS PayLah! and iBanking alert emails from Gmail, extracting transactions, categorising them, and writing to expense-tracker.md locally or on Google Drive."
---

# Expense Tracker — Refresh

**Triggers:** "refresh my expense tracker", "update my finances", or any equivalent

**Local path (device-agnostic):** `$WT/Finances/expense-tracker.md`
**Google Drive Folder ID:** `12aFM2fFgGmYNO0JYFDwlCni2ws3mCkhb`

`$WT` is the Weekly Tracker folder. Resolve it at the start of every local command (shell state does not persist); works whether `Claude Things` or `Weekly Tracker` itself is connected in the Claude desktop app:
```bash
WT=""; for d in "$HOME/mnt/Claude Things/Weekly Tracker" "$HOME/mnt/Weekly Tracker" "/c/Users/user/Documents/Google Drive/Claude Things/Weekly Tracker"; do [ -d "$d" ] && WT="$d" && break; done
```

## Step 1 — Read the existing tracker

**Primary — local Cowork folder:**
Use `device_bash` to read the existing file:
```bash
cat "$WT/Finances/expense-tracker.md" 2>/dev/null || echo "FILE_NOT_FOUND"
```
If `$WT` is empty, the local folder isn't connected — use the Google Drive fallback.

**Fallback — Google Drive:**
If local read fails or returns FILE_NOT_FOUND, search Google Drive:
```
mcp__Google_Drive__search_files: query = "name = 'expense-tracker.md' and trashed = false"
```
Read it with `mcp__Google_Drive__read_file_content` if found.

Note the last transaction date in the file to know how far back to pull emails.

## Step 2 — Pull transaction emails from Gmail

Search Gmail for DBS transaction alerts since the last logged date:
```
mcp__Gmail__search_threads:
query = "from:(ibanking.alert@dbs.com OR ibanking.alerts@dbs.com OR donotreply@dbs.com OR alerts@dbs.com) subject:"Card Transaction" after:YYYY/MM/DD"
```
Also search for PayLah! notifications:
```
mcp__Gmail__search_threads:
  query = "DBS PayLah after:YYYY/MM/DD"
```

If no last date is known, default to pulling the last 30 days.

## Step 3 — Extract transactions

For each email, extract:
- **Date** (YYYY-MM-DD)
- **Time** (HH:MM SGT)
- **Amount** (SGD)
- **Merchant / Recipient**
- **Transaction type** (debit card / PayLah! / transfer / etc.)

Skip duplicate transactions already present in the existing file.

## Step 4 — Categorise

Assign each transaction to one of four categories:
- 🍜 **Food & Dining** — restaurants, food delivery, cafes, hawker centres
- 🚌 **Transport & Travel** — Grab, MRT/bus top-up, taxis, flights, petrol
- 🛍 **Shopping & Subscriptions** — retail, online shopping, app subscriptions, streaming
- 👥 **Transfers to Friends (P2P)** — PayLah! peer transfers, PayNow to individuals

If unsure, make the most reasonable call based on the merchant name.

## Step 5 — Write the updated file

Organise by **month → week (Mon–Sun)**. Format:

```markdown
# Expense Tracker
_Last updated: YYYY-MM-DD_

---

## September 2026

### Week of 1 Sep – 7 Sep

| Date | Time | Merchant | Category | Amount |
|------|------|----------|----------|--------|
| 01 Sep | 12:34 | Maxwell Food Centre | 🍜 Food & Dining | $4.50 |
| 02 Sep | 09:10 | Grab | 🚌 Transport | $8.20 |

**Week Total:** $XX.XX

### Week of 8 Sep – 14 Sep
...

**Month Total:** $XX.XX
```

Append new transactions to the correct week. Do not overwrite existing entries.

**Write back:**
- **Primary:** Write via `device_bash` if local folder is connected:
  ```bash
  mkdir -p "$WT/Finances"
  # write updated file
  ```
- **Fallback:** Use `mcp__Google_Drive__update_file` or `mcp__Google_Drive__create_file` in folder `12aFM2fFgGmYNO0JYFDwlCni2ws3mCkhb`

## Step 6 — Display summary

Respond with the expense card format (from MEMORY.md):
- Header box: current month, days in, total spent so far
- Category totals with emoji
- "This Week" day-by-day breakdown of new transactions
- Flag any large or unusual transactions at the bottom

## Notes
- Always use Singapore time (SGT, UTC+8)
- Never announce file reads/writes — just do it
- If Gmail returns no new alerts, say so and show the current totals from the existing file
- Amounts are always in SGD