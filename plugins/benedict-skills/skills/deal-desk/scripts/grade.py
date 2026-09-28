"""Grade a candidate workbook against an answer-key workbook, line by line (Case Gym / post-test review).

    python grade.py candidate.xlsx answer.xlsx lbo|pf [--tol 0.001] [--md report.md]

How it works: both files are recalculated in Excel (copies, originals untouched). For each key line it finds the
candidate row whose label matches (synonyms below), then looks for the run of numbers in that row that best matches
the answer (any column position, sign ignored). A line scores if every year is within tolerance (default 0.1%: tests mark each line right or wrong).
It is a first pass: Claude reviews every MISS / NOT FOUND by hand before telling Benedict the score.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))

# key: (answer-key label in deal-desk models, candidate synonyms (regex), kind: series|scalar)
SPECS = {
    "lbo": [
        ("Revenue", "Revenue", r"^(total )?(net )?revenues?$|^sales$|^turnover$", "series"),
        ("Gross profit", "Gross profit", r"gross profit", "series"),
        ("EBITDA", "EBITDA", r"^ebitda$|^ebitda \(", "series"),
        ("Depreciation", "Depreciation", r"^\(?[-+]?\)?\s*depreciation|^d&a$", "series"),
        ("EBIT", "EBIT", r"^ebit$|operating profit", "series"),
        ("Interest expense", "Interest expense", r"interest expense|interest paid|finance cost", "series"),
        ("Tax", "Income tax", r"^(?!.*(before|after|pre|post)[- ]tax)(?!.*rate)(?!.*unlevered).*\btax(es)?\b", "series"),
        ("Profit after tax", "Profit after tax", r"profit after tax|net (income|profit)|npat|pat$", "series"),
        ("Capex", "Less: capex", r"cap(ital)? ?ex", "series"),
        ("Change in NWC", "Less: increase in NWC", r"(working capital|nwc)", "series"),
        ("FCFF", "Free cash flow to firm (FCFF)", r"fcff|free cash flow to (the )?firm|unlevered", "series"),
        ("FCFE", "Free cash flow to equity (FCFE)", r"fcfe|free cash flow to equity|levered free", "series"),
        ("Debt balance", "Closing balance", r"(closing|ending).*(debt|balance)|debt.*(closing|ending)", "series"),
        ("Net debt / EBITDA", "Net debt / EBITDA", r"net debt ?/ ?ebitda|leverage", "series"),
        ("DSCR", "DSCR (CFADS / debt service)", r"dscr|debt service cover", "series"),
        ("Equity IRR", "Equity IRR", r"\birr\b|internal rate", "scalar"),
        ("Equity multiple", "Equity multiple (MoM)", r"mom|moic|multiple of money|money.?on.?money|equity multiple|cash.?on.?cash", "scalar"),
        ("WACC", "WACC", r"^wacc|weighted average cost", "scalar"),
    ],
    "pf": [
        ("Total project cost", "Total project cost (incl. IDC, fee and DSRA)", r"total project cost|total uses|total funding", "scalar"),
        ("IDC", "Interest during construction", r"\bidc\b|interest during construction", "scalar"),
        ("Upfront fee", "Upfront fee", r"upfront fee|arrangement fee", "scalar"),
        ("Maximum debt", "Maximum debt = lower of the two", r"(max(imum)?|total|senior) debt|debt (amount|size|sizing)", "scalar"),
        ("Total revenue", "Total revenue", r"total revenue|revenue", "scalar"),
        ("Total opex", "Total operating costs", r"total (opex|operating cost)|opex", "scalar"),
        ("Minimum DSCR", "Minimum DSCR (repayment period)", r"min(imum)? dscr", "scalar"),
        ("Average DSCR", "Average DSCR (repayment period)", r"av(era)?ge? dscr", "scalar"),
        ("Project IRR", "Project IRR (pre-financing, XIRR)", r"project irr|unlevered irr", "scalar"),
        ("Equity IRR", "Equity IRR (XIRR)", r"equity irr|levered irr", "scalar"),
        ("DSRA at COD", "DSRA initial funding at COD", r"dsra|debt service reserve", "scalar"),
        ("Minimum LLCR", "Minimum LLCR (includes the DSRA balance)", r"llcr|loan life cover", "scalar"),
    ],
}


def recalc_copy(path):
    tmp = os.path.join(tempfile.mkdtemp(), os.path.basename(path))
    shutil.copy(path, tmp)
    subprocess.run([sys.executable, os.path.join(HERE, "office.py"), "recalc", tmp], capture_output=True, text=True)
    return tmp


def rows_of(path):
    """[(sheet, row, label, [numbers in column order])] for every row that has a text label."""
    wb = load_workbook(path, data_only=True)
    out = []
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            lab, nums = None, []
            for c in row:
                v = c.value
                if isinstance(v, str) and v.strip() and lab is None and not re.match(r"^[\d.,%()x-]+$", v.strip()):
                    lab = v.strip()
                elif isinstance(v, (int, float)) and not isinstance(v, bool):
                    nums.append(float(v))
            if lab:
                out.append((ws.title, row[0].row, lab, nums))
    return out


def close(a, b, tol):
    return abs(abs(a) - abs(b)) <= max(tol * abs(b), 0.5 if abs(b) > 50 else 1e-4)


def best_window(cand, ans, tol):
    """Best alignment of the answer series inside the candidate's numbers (sign ignored)."""
    n = len(ans)
    best = (0, None)
    for i in range(0, max(1, len(cand) - n + 1)):
        win = cand[i:i + n]
        if len(win) < n:
            break
        hits = sum(close(a, b, tol) for a, b in zip(win, ans))
        if hits > best[0]:
            best = (hits, win)
    return best


def grade(cand_path, ans_path, kind, tol=0.001):
    cand, ans = rows_of(recalc_copy(cand_path)), rows_of(recalc_copy(ans_path))
    results = []
    for name, ans_label, pattern, typ in SPECS[kind]:
        pref = {"Model": 0, "Outputs": 0, "Dashboard": 0, "Ops": 1, "Operations": 1, "Debt": 1}
        arow = next((r for r in sorted(ans, key=lambda r: pref.get(r[0], 2)) if r[2] == ans_label and r[3]), None)
        if not arow:
            results.append((name, "n/a in answer key", "", "SKIP"))
            continue
        target = arow[3]
        if typ == "series":
            target = target[-5:] if len(target) >= 5 else target  # forecast years
        else:
            target = target[:1]
        rx = re.compile(pattern, re.I)
        best = (0, None, None, (-1, -1))
        for sh, rn, lab, nums in cand:
            if not nums or not rx.search(lab.lower()):
                continue
            hits, win = best_window(nums, target, tol)
            key = (hits, len(nums))  # most matches first, then the fullest row (the working, not the input tab)
            if best[2] is None or key > best[3]:
                best = (hits, win, f"{sh}!{rn} '{lab[:40]}'", key)
        hits, win, where = best[:3]
        if where is None:
            results.append((name, fmt(target), "not found", "NOT FOUND"))
        else:
            status = "OK" if hits == len(target) else ("PARTIAL" if hits else "MISS")
            results.append((name, fmt(target), f"{fmt(win) if win else '—'}  [{where}]", status))
    return results


def fmt(v):
    if v is None:
        return "—"
    return ", ".join(f"{x:,.4f}" if abs(x) < 10 else f"{x:,.1f}" for x in v)


def report(results, md=None):
    score = sum(r[3] == "OK" for r in results)
    total = sum(r[3] != "SKIP" for r in results)
    lines = [f"Score: {score} / {total} key lines match the answer key", "",
             "| Line | Answer key | Candidate [where found] | Result |", "|---|---|---|---|"]
    lines += [f"| {a} | {b} | {c} | {d} |" for a, b, c, d in results]
    text = "\n".join(lines)
    print(text)
    if md:
        open(md, "w", encoding="utf-8").write(text + "\n")
    return score, total


if __name__ == "__main__":
    args = sys.argv[1:]
    tol = float(args[args.index("--tol") + 1]) if "--tol" in args else 0.001
    md = args[args.index("--md") + 1] if "--md" in args else None
    report(grade(args[0], args[1], args[2], tol), md)
