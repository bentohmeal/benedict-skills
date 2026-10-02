"""Technical Bank drill helper for the recruiting-prep skill.

Keeps drills cheap: the chat only ever sees the handful of questions being asked,
never the whole bank.

  drill.py status                          one line for the Step 0 status block
  drill.py pick [--topic acc] [--level 2] [--concept C-03] [--tier core]
                [--count 10] [--mode due|weak|new|mock] [--brief]
  drill.py show Q-DCF-014 [Q-...]          full entries (the marking key)
  drill.py log Q-DCF-014=right Q-ACC-003=miss [--date YYYY-MM-DD] [--session mock]
  drill.py summary                         prints + writes progress-summary.md
  drill.py index                           rebuilds sources-index.md
  drill.py lint                            format, table and coverage checks

Run with: C:\\Users\\user\\AppData\\Local\\Programs\\Python\\Python312\\python.exe drill.py <command>
"""
import argparse
import csv
import datetime as dt
import os
import random
import re
import sys
from collections import OrderedDict, defaultdict
from pathlib import Path

BANK = Path(os.environ.get(
    "TECH_BANK",
    r"C:\Users\user\Documents\Google Drive\Claude Things\Interview Prep\Technical Bank"))

TOPICS = OrderedDict([
    ("ACC", "Accounting"),
    ("EV", "Equity value & enterprise value"),
    ("VAL", "Valuation & multiples"),
    ("DCF", "DCF & discount rate"),
    ("MA", "M&A"),
    ("LBO", "LBO & private equity"),
    ("CRD", "Credit & capital markets"),
    ("IND", "Industry"),
    ("ADV", "Analyst-level"),
])
RESULTS = ("right", "half", "miss")
RIGHT_STEPS = (7, 21, 60)          # days until the next ask after 1, 2, 3+ rights in a row
HALF_DAYS, MISS_DAYS = 3, 1
CORE_FIELDS = ("Say it (20s)", "Why", "Example", "Follow-ups", "Traps")
SHORT_FIELDS = ("Say it (20s)", "Why")
PROGRESS_COLS = ["id", "topic", "tier", "level", "last_result", "last_date",
                 "streak", "next_due", "attempts", "misses"]

HEAD_RE = re.compile(r"^### \[(Q-([A-Z]+)-(\d{3}))\] (.+?)\s*$")
SRC_RE = re.compile(r"\b(B25-[A-Z]{2,3}\d{2}|RB-\d{4}|OLD-\d{3})\b")
WALK_RE = re.compile(
    r"(walk (me )?through.*(statement|step))|(three[- ]statements?)|(3 statements)"
    r"|((flow|impact|affect|change).*(financial statements))", re.I)


# ---------- reading the bank ----------

class Q:
    def __init__(self, qid, topic, text, file):
        self.id, self.topic, self.text, self.file = qid, topic, text, file
        self.meta, self.body = {}, []

    @property
    def tier(self):
        return self.meta.get("tier", "")

    @property
    def level(self):
        return self.meta.get("level", "")

    @property
    def body_text(self):
        return "\n".join(self.body).strip()

    def render(self):
        meta = " · ".join(f"{k}: {v}" for k, v in self.meta.items())
        return f"### [{self.id}] {self.text}\n{meta}\n{self.body_text}\n"


def load_bank():
    qs = OrderedDict()
    for f in sorted(BANK.glob("[0-9][0-9]-*.md")):
        cur, want_meta = None, False
        for line in f.read_text(encoding="utf-8").splitlines():
            m = HEAD_RE.match(line)
            if m:
                cur = Q(m.group(1), m.group(2), m.group(4), f.name)
                if cur.id in qs:
                    sys.exit(f"Duplicate ID {cur.id} in {f.name}")
                qs[cur.id] = cur
                want_meta = True
                continue
            if line.startswith("## ") or line.startswith("# "):
                cur = None
                continue
            if cur is None:
                continue
            if want_meta:
                if not line.strip():
                    continue
                for part in line.split(" · "):
                    if ":" in part:
                        k, v = part.split(":", 1)
                        cur.meta[k.strip()] = v.strip()
                want_meta = False
                continue
            cur.body.append(line)
    return qs


def today(args=None):
    d = getattr(args, "date", None)
    return dt.date.fromisoformat(d) if d else dt.date.today()


# ---------- progress ----------

def load_progress(qs):
    path = BANK / "progress.csv"
    rows = OrderedDict()
    if path.exists():
        with path.open(encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                rows[r["id"]] = r
    changed = False
    for q in qs.values():
        r = rows.get(q.id)
        if r is None:
            rows[q.id] = {c: "" for c in PROGRESS_COLS}
            r = rows[q.id]
            r.update(id=q.id, streak="0", attempts="0", misses="0")
            changed = True
        for k, v in (("topic", q.topic), ("tier", q.tier), ("level", q.level)):
            if r.get(k) != v:
                r[k] = v
                changed = True
    if changed:
        save_progress(rows)
    return rows


def save_progress(rows):
    with (BANK / "progress.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=PROGRESS_COLS)
        w.writeheader()
        for r in rows.values():
            w.writerow({c: r.get(c, "") for c in PROGRESS_COLS})


def is_due(r, day):
    return bool(r["next_due"]) and dt.date.fromisoformat(r["next_due"]) <= day


def mastered(r):
    return r["last_result"] == "right" and int(r["streak"] or 0) >= 2


# ---------- commands ----------

def filtered(qs, args):
    out = []
    for q in qs.values():
        if args.topic and args.topic.upper() not in ("ALL", q.topic):
            continue
        if args.level and q.level != str(args.level):
            continue
        if args.tier and q.tier != args.tier:
            continue
        if args.concept and args.concept.upper() not in q.meta.get("concept", "").upper():
            continue
        out.append(q)
    return out


def round_robin(items, key):
    groups = OrderedDict()
    for it in items:
        groups.setdefault(key(it), []).append(it)
    out = []
    while any(groups.values()):
        for g in groups.values():
            if g:
                out.append(g.pop(0))
    return out


def cmd_pick(args):
    qs = load_bank()
    prog = load_progress(qs)
    day = today(args)
    pool = filtered(qs, args)
    rank = {"miss": 0, "half": 1, "right": 2}
    seen = [q for q in pool if prog[q.id]["last_result"]]
    new = [q for q in pool if not prog[q.id]["last_result"]]
    # new questions: core before short, easier before harder, topics interleaved
    new.sort(key=lambda q: (q.tier != "core", q.level))
    if not args.topic or args.topic.upper() == "ALL":
        new = round_robin(new, lambda q: q.topic)
    if args.mode == "weak":
        picked = sorted([q for q in seen if prog[q.id]["last_result"] in ("miss", "half")],
                        key=lambda q: (rank[prog[q.id]["last_result"]], prog[q.id]["next_due"]))
    elif args.mode == "new":
        picked = new
    elif args.mode == "mock":
        rnd = random.Random(args.seed)
        core = [q for q in pool if q.tier == "core"] or pool
        rnd.shuffle(core)
        picked = round_robin(core, lambda q: q.topic)
    else:
        due = sorted([q for q in seen if is_due(prog[q.id], day)],
                     key=lambda q: (rank[prog[q.id]["last_result"]], prog[q.id]["next_due"]))
        picked = due + new
    picked = picked[:args.count]
    if not picked:
        print("Nothing to pick with those filters.")
        return
    print(f"# {len(picked)} question(s) · mode {args.mode} · {day.isoformat()}\n")
    for q in picked:
        r = prog[q.id]
        last = f"last: {r['last_result']} on {r['last_date']}" if r["last_result"] else "new"
        if args.brief:
            print(f"- {q.id} (L{q.level}, {q.tier}, {last}): {q.text}")
        else:
            print(f"<!-- {last} -->")
            print(q.render())


def cmd_show(args):
    qs = load_bank()
    for qid in args.ids:
        q = qs.get(qid.upper())
        print(q.render() if q else f"{qid}: not found")


def cmd_log(args):
    qs = load_bank()
    prog = load_progress(qs)
    day = today(args)
    log_path = BANK / "drill-log.csv"
    new_file = not log_path.exists()
    with log_path.open("a", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        if new_file:
            w.writerow(["date", "session", "id", "result"])
        for item in args.items:
            if "=" not in item:
                sys.exit(f"Use Q-ID=right|half|miss (got {item})")
            qid, res = item.split("=", 1)
            qid, res = qid.upper(), res.lower()
            if qid not in qs:
                sys.exit(f"{qid}: not in the bank")
            if res not in RESULTS:
                sys.exit(f"{res}: use right, half or miss")
            r = prog[qid]
            r["attempts"] = str(int(r["attempts"] or 0) + 1)
            if res == "right":
                streak = int(r["streak"] or 0) + 1
                gap = RIGHT_STEPS[min(streak, len(RIGHT_STEPS)) - 1]
            else:
                streak = 0
                gap = HALF_DAYS if res == "half" else MISS_DAYS
                if res == "miss":
                    r["misses"] = str(int(r["misses"] or 0) + 1)
            r.update(last_result=res, last_date=day.isoformat(), streak=str(streak),
                     next_due=(day + dt.timedelta(days=gap)).isoformat())
            w.writerow([day.isoformat(), args.session, qid, res])
            print(f"{qid}: {res} · next due {r['next_due']}")
    save_progress(prog)
    write_summary(qs, prog, dt.date.today())


def topic_stats(qs, prog, day):
    stats = OrderedDict()
    for code in TOPICS:
        ids = [q.id for q in qs.values() if q.topic == code]
        if not ids:
            continue
        rows = [prog[i] for i in ids]
        stats[code] = dict(
            total=len(ids),
            seen=sum(1 for r in rows if r["last_result"]),
            mastered=sum(1 for r in rows if mastered(r)),
            due=sum(1 for r in rows if is_due(r, day)),
            weak=sum(1 for r in rows if r["last_result"] in ("miss", "half")),
        )
    return stats


def weakest(qs, prog, n=5):
    rows = [r for r in prog.values() if r["last_result"] in ("miss", "half") and r["id"] in qs]
    rows.sort(key=lambda r: (-int(r["misses"] or 0), r["last_result"] != "miss", r["next_due"]))
    return rows[:n]


def weakest_topic(stats):
    seen = {c: s for c, s in stats.items() if s["seen"]}
    if not seen:
        return None
    return max(seen, key=lambda c: (seen[c]["weak"] / seen[c]["seen"], seen[c]["weak"]))


def write_summary(qs, prog, day):
    stats = topic_stats(qs, prog, day)
    lines = ["# Technicals progress", "", f"_Last updated: {day.isoformat()}_", "",
             "| Topic | Questions | Seen | Mastered | Mastery % | Weak | Due today |",
             "|---|---|---|---|---|---|---|"]
    tot = defaultdict(int)
    for code, s in stats.items():
        pct = round(100 * s["mastered"] / s["total"]) if s["total"] else 0
        lines.append(f"| {TOPICS[code]} | {s['total']} | {s['seen']} | {s['mastered']} | {pct}% | {s['weak']} | {s['due']} |")
        for k, v in s.items():
            tot[k] += v
    pct = round(100 * tot["mastered"] / tot["total"]) if tot["total"] else 0
    lines.append(f"| **Total** | {tot['total']} | {tot['seen']} | {tot['mastered']} | {pct}% | {tot['weak']} | {tot['due']} |")
    lines += ["", "## Weakest 5", "", "| ID | Question | Last result | Misses | Next due |", "|---|---|---|---|---|"]
    for r in weakest(qs, prog):
        text = qs[r["id"]].text
        text = text if len(text) <= 90 else text[:87] + "..."
        lines.append(f"| {r['id']} | {text} | {r['last_result']} | {r['misses']} | {r['next_due']} |")
    lines += ["", "Mastered = answered right twice in a row. Weak = last answer was a miss or a half.", ""]
    (BANK / "progress-summary.md").write_text("\n".join(lines), encoding="utf-8")
    return stats, tot


def cmd_summary(args):
    qs = load_bank()
    prog = load_progress(qs)
    write_summary(qs, prog, today(args))
    print((BANK / "progress-summary.md").read_text(encoding="utf-8"))


def cmd_status(args):
    qs = load_bank()
    prog = load_progress(qs)
    stats, tot = write_summary(qs, prog, today(args))
    wt = weakest_topic(stats)
    weak = f", weakest topic {TOPICS[wt]}" if wt else ""
    print(f"Technicals: {tot['due']} due today{weak} ({tot['mastered']}/{tot['total']} mastered)")


# ---------- sources index ----------

def load_sources():
    path = BANK / "_sources" / "source-questions.csv"
    if not path.exists():
        return OrderedDict()
    with path.open(encoding="utf-8", newline="") as fh:
        return OrderedDict((r["key"], r) for r in csv.DictReader(fh))


def source_map(qs):
    mapping = defaultdict(list)
    for q in qs.values():
        for key in SRC_RE.findall(q.meta.get("source", "")):
            mapping[key].append(q.id)
    return mapping


def section_counts(sources, mapping):
    secs = OrderedDict()
    for key, r in sources.items():
        s = secs.setdefault((r["guide"], r["section"]), dict(total=0, mapped=0, skipped=0, missing=[]))
        s["total"] += 1
        if r.get("status", "").startswith("skip"):
            s["skipped"] += 1
        elif key in mapping:
            s["mapped"] += 1
        else:
            s["missing"].append(key)
    return secs


def cmd_index(args):
    qs = load_bank()
    sources = load_sources()
    mapping = source_map(qs)
    secs = section_counts(sources, mapping)
    out = ["# Sources index", "",
           "Generated by `drill.py index`. Do not edit by hand.",
           "Every question in the source guides, and the Technical Bank question that covers it.", "",
           "## Coverage by section", "",
           "| Guide | Section | In guide | In bank | Not a question | Still to add |", "|---|---|---|---|---|---|"]
    for (guide, sec), s in secs.items():
        out.append(f"| {guide} | {sec} | {s['total']} | {s['mapped']} | {s['skipped']} | {len(s['missing'])} |")
    t = lambda k: sum((len(s[k]) if k == "missing" else s[k]) for s in secs.values())
    out.append(f"| **Total** | | {t('total')} | {t('mapped')} | {t('skipped')} | {t('missing')} |")
    last = None
    for key, r in sources.items():
        if (r["guide"], r["section"]) != last:
            last = (r["guide"], r["section"])
            out += ["", f"## {r['guide']} · {r['section']}", "", "| Key | Page | Question | Bank ID |", "|---|---|---|---|"]
        text = r["question"].replace("|", "/")
        text = text if len(text) <= 110 else text[:107] + "..."
        if r.get("status", "").startswith("skip"):
            ids = f"_{r['status']}_"
        else:
            ids = ", ".join(mapping.get(key, [])) or "to add"
        out.append(f"| {key} | {r['page']} | {text} | {ids} |")
    (BANK / "sources-index.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"sources-index.md: {t('total')} source questions, {t('mapped')} in the bank, "
          f"{t('skipped')} not questions, {t('missing')} still to add")


# ---------- lint ----------

def num(cell):
    c = cell.strip().replace("**", "").replace("$", "").replace(",", "").replace("−", "-").replace("–", "-")
    if c in ("", "-", "—", "0"):
        return 0.0
    try:
        return float(c)
    except ValueError:
        return None


def tables(body):
    """Yield statement tables as (header cells, rows of cells)."""
    block = []
    for line in body + [""]:
        if line.strip().startswith("|"):
            block.append([c.strip() for c in line.strip().strip("|").split("|")])
        elif block:
            if len(block) > 2 and block[0][0].lower() == "statement":
                yield block[0], block[2:]
            block = []


def check_table(head, rows):
    errs = []
    for col in range(2, len(head)):
        a = l = 0.0
        cash = ncc = ni_is = ni_cfs = None
        for r in rows:
            if len(r) <= col:
                continue
            st, line, v = r[0].upper(), r[1].lower().replace("**", ""), num(r[col])
            if st.startswith("CHECK") or line.startswith("total"):
                continue
            if v is None:
                errs.append(f"column '{head[col]}': '{r[col]}' is not a number ({r[1]})")
                continue
            if st.startswith("BS (A)"):
                a += v
                if line == "cash":
                    cash = v
            elif st.startswith("BS (L+E)"):
                l += v
            elif st.startswith("BS"):
                errs.append(f"row '{r[1]}': use 'BS (A)' or 'BS (L+E)'")
            elif st.startswith("CFS") and line.startswith("net change in cash"):
                ncc = v
            elif st.startswith("CFS") and line == "net income":
                ni_cfs = v
            elif st.startswith("IS") and line == "net income":
                ni_is = v
        if abs(a - l) > 0.005:
            errs.append(f"column '{head[col]}': assets {a:+g} vs liabilities + equity {l:+g}")
        if cash is not None and ncc is not None and abs(cash - ncc) > 0.005:
            errs.append(f"column '{head[col]}': CFS net change in cash {ncc:+g} vs BS cash {cash:+g}")
        if ni_is is not None and ni_cfs is not None and abs(ni_is - ni_cfs) > 0.005:
            errs.append(f"column '{head[col]}': IS net income {ni_is:+g} vs CFS net income {ni_cfs:+g}")
    return errs


def cmd_lint(args):
    qs = load_bank()
    sources = load_sources()
    mapping = source_map(qs)
    errs, warns = [], []
    concepts = set(re.findall(r"^## \[(C-\d{2})\]", (BANK / "concepts.md").read_text(encoding="utf-8"), re.M)) \
        if (BANK / "concepts.md").exists() else set()
    n_tables = 0
    for q in qs.values():
        where = f"{q.id} ({q.file})"
        if q.tier not in ("core", "short"):
            errs.append(f"{where}: tier must be core or short")
        if q.level not in ("1", "2", "3"):
            errs.append(f"{where}: level must be 1, 2 or 3")
        if "source" not in q.meta:
            errs.append(f"{where}: no source")
        for c in re.findall(r"C-\d{2}", q.meta.get("concept", "")):
            if concepts and c not in concepts:
                errs.append(f"{where}: concept {c} is not in concepts.md")
        body = q.body_text
        for f in (CORE_FIELDS if q.tier == "core" else SHORT_FIELDS):
            if f"**{f}:**" not in body:
                errs.append(f"{where}: missing '{f}'")
        tabs = list(tables(q.body))
        is_walk = q.meta.get("type") == "3fs"
        if WALK_RE.search(q.text) and not is_walk and q.meta.get("type") != "concept":
            warns.append(f"{where}: reads like a statement walkthrough but has no 'type: 3fs'")
        if is_walk and not tabs:
            errs.append(f"{where}: three-statement walkthrough with no numeric table")
        for head, rows in tabs:
            n_tables += 1
            errs += [f"{where}: {e}" for e in check_table(head, rows)]
        for key in SRC_RE.findall(q.meta.get("source", "")):
            if sources and key not in sources:
                errs.append(f"{where}: source key {key} is not in source-questions.csv")
    for (guide, sec), s in section_counts(sources, mapping).items():
        if s["mapped"] and s["missing"]:
            errs.append(f"{guide} · {sec}: {len(s['missing'])} question(s) not in the bank: {', '.join(s['missing'])}")
    bank_ids = set()
    mb = BANK.parent / "Master Bank" / "technicals.md"
    if mb.exists():
        bank_ids = set(re.findall(r"^### \[(TECH-[A-Z0-9-]+)\]", mb.read_text(encoding="utf-8"), re.M))
        for q in qs.values():
            for t in re.findall(r"TECH-[A-Z0-9-]+", q.meta.get("bank", "")):
                if t not in bank_ids:
                    errs.append(f"{q.id}: bank ID {t} is not in the Master Bank")
    by_tier = defaultdict(int)
    for q in qs.values():
        by_tier[q.tier] += 1
    print(f"{len(qs)} questions ({by_tier['core']} core, {by_tier['short']} short) · "
          f"{n_tables} statement tables checked · {len(mapping)} source questions covered")
    for w in warns:
        print("WARN  " + w)
    for e in errs:
        print("ERROR " + e)
    print("LINT CLEAN" if not errs else f"LINT FAILED: {len(errs)} error(s)")
    sys.exit(1 if errs else 0)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description="Technical Bank drill helper")
    sub = p.add_subparsers(dest="cmd", required=True)

    def dated(sp):
        sp.add_argument("--date", help="YYYY-MM-DD (default: today)")
        return sp

    sp = dated(sub.add_parser("pick"))
    sp.add_argument("--topic", help="ACC, EV, VAL, DCF, MA, LBO, CRD, IND, ADV or ALL")
    sp.add_argument("--level", type=int, choices=(1, 2, 3))
    sp.add_argument("--tier", choices=("core", "short"))
    sp.add_argument("--concept", help="e.g. C-03")
    sp.add_argument("--count", type=int, default=10)
    sp.add_argument("--mode", choices=("due", "weak", "new", "mock"), default="due")
    sp.add_argument("--seed", type=int)
    sp.add_argument("--brief", action="store_true", help="IDs and questions only")
    sp.set_defaults(fn=cmd_pick)

    sp = sub.add_parser("show")
    sp.add_argument("ids", nargs="+")
    sp.set_defaults(fn=cmd_show)

    sp = dated(sub.add_parser("log"))
    sp.add_argument("items", nargs="+", help="Q-ID=right|half|miss")
    sp.add_argument("--session", default="drill", help="drill, mock, concept, weak, interview")
    sp.set_defaults(fn=cmd_log)

    dated(sub.add_parser("summary")).set_defaults(fn=cmd_summary)
    dated(sub.add_parser("status")).set_defaults(fn=cmd_status)
    sub.add_parser("index").set_defaults(fn=cmd_index)
    sub.add_parser("lint").set_defaults(fn=cmd_lint)

    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
