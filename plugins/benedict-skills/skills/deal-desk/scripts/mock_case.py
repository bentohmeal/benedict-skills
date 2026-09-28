"""Case Gym: generate a fresh mock case in the format of Benedict's real tests.

    python mock_case.py lbo|pf out_dir [--seed N] [--minutes 105]

Creates in out_dir:
  Brief – <name>.docx        the test brief (what the candidate reads)
  Inputs – <name>.xlsx       only the data a real test would hand over
  _answer/ (do not open)     case.json + the full answer model built by build_lbo.py / build_pf.py
Grade later with:  python grade.py "<his file>.xlsx" "_answer/Answer – <name>.xlsx" lbo|pf --md score.md
"""
import json
import os
import random
import subprocess
import sys

from docx import Document
from docx.shared import Pt
from openpyxl import Workbook

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from xlstyle import NUM, PCT, _font, header_row, label, put, section, setup  # noqa: E402


def title(ws, text, sub=None):
    """Plain title for the candidate's input pack (it imitates a firm's file, not the house style)."""
    ws["B2"] = text
    ws["B2"].font = _font(bold=True, size=12)
    if sub:
        ws["B3"] = sub
        ws["B3"].font = _font(italic=True)

HERE = os.path.dirname(os.path.abspath(__file__))

LBO_SECTORS = [
    ("Pawsome", "a chain of veterinary clinics in Malaysia", "clinics"),
    ("BrightSmile", "a dental group in Singapore", "clinics"),
    ("Little Oaks", "a childcare operator in Australia", "centres"),
    ("Brew Lab", "a specialty coffee chain in Hong Kong", "outlets"),
    ("ColdLink", "a cold-storage logistics business in Thailand", "warehouses"),
    ("FitNation", "a boutique gym chain in New Zealand", "studios"),
    ("CleanCo", "a commercial cleaning services firm in Singapore", "contracts"),
]
PF_TECH = [("solar", (0.19, 0.29), (0.15, 0.24)), ("onshore wind", (0.30, 0.40), (0.25, 0.33))]


def r2(x, step):
    return round(round(x / step) * step, 6)


def lbo_case(rng):
    name, desc, unit = rng.choice(LBO_SECTORS)
    rev = r2(rng.uniform(40000, 160000), 500)
    gm0 = rng.uniform(0.55, 0.92)
    opex0 = gm0 - rng.uniform(0.14, 0.28)
    ebitda0 = rev * (gm0 - opex0)
    dep0 = r2(rev * rng.uniform(0.01, 0.03), 1)
    int0 = r2(rev * rng.uniform(0.003, 0.01), 0.1)
    pbt0 = ebitda0 - dep0 - int0
    growth = [r2(rng.uniform(0.02, 0.10), 0.005) for _ in range(5)]
    growth.sort(reverse=True)
    gms = [r2(gm0 + rng.uniform(-0.02, 0.03), 0.005) for _ in range(5)]
    opx = [r2(opex0 + rng.uniform(-0.03, 0.04), 0.005) for _ in range(5)]
    mult = r2(rng.uniform(5.0, 9.0), 0.25)
    price = r2(ebitda0 * mult, 1000)
    loan = r2(price * rng.uniform(0.25, 0.5), 1000)
    c = {
        "company": name, "case": f"Mock PE case – {name} ({desc})", "units": "$'000", "years": 5,
        "historical": {"revenue": rev, "cogs": r2(rev * (1 - gm0), 1), "opex": r2(rev * opex0, 1), "depreciation": dep0,
                       "interest": int0, "tax": r2(max(pbt0, 0) * 0.2, 0.01)},
        "drivers": {"revenue_growth": growth, "gross_margin": gms, "opex_pct": opx,
                    "capex": [r2(rev * rng.uniform(0.01, 0.04), 100) for _ in range(5)],
                    "nwc_pct": [r2(rng.uniform(0.02, 0.08), 0.005) for _ in range(5)]},
        "opening": {"nwc": r2(rev * rng.uniform(0.02, 0.07), 100), "equity_book": r2(price * rng.uniform(0.4, 0.8), 1000)},
        "dep": {"existing_per_year": r2(dep0 * rng.uniform(0.85, 0.95), 10), "new_asset_life": rng.choice([5, 8, 10]), "same_year": 1},
        "tax_rate": rng.choice([0.17, 0.20, 0.24, 0.25, 0.30]),
        "deal": {"purchase_price": price, "entry_cost_pct": rng.choice([0.01, 0.015, 0.02]), "exit_cost_pct": rng.choice([0.01, 0.02]),
                 "exit_multiple": r2(mult + rng.uniform(-1.0, 0.5), 0.5), "min_cash": 0, "distribute_fcfe": 1},
        "loan": {"name": "Term loan", "amount": loan, "rate": r2(rng.uniform(0.045, 0.085), 0.0025),
                 "upfront_fee_pct": rng.choice([0.01, 0.015, 0.02]), "tenor": rng.choice([5, 6, 7]), "interest_on_average": 0},
        "dcf": {"cost_of_equity": r2(rng.uniform(0.11, 0.15), 0.005), "terminal_growth": 0.025, "mid_year": 0},
        "assumptions_log": ["Answer-key assumptions follow references/case-lbo.md defaults: cash-free/debt-free price, fees in uses, "
                            "interest on opening balance, capex depreciated from year of spend, FCFE distributed annually."],
    }
    if c["loan"]["tenor"] > 5:
        c["loan"]["amort_pct"] = [1 / c["loan"]["tenor"]] * 5
    c["_unit"] = unit
    return c


def pf_case(rng):
    tech, p50r, p90r = rng.choice(PF_TECH)
    mw = rng.choice([50, 100, 150, 200, 300])
    p50 = r2(rng.uniform(*p50r), 0.005)
    p90 = r2(min(p50 - 0.03, rng.uniform(*p90r)), 0.005)
    epc_per_mw = rng.uniform(0.7, 1.4) if tech == "solar" else rng.uniform(1.2, 1.8)
    c = {
        "project": f"{mw} MW {tech} project", "case": f"Mock project finance case – {mw} MW {tech}", "start": [2025, 1, 1],
        "construction_months": rng.choice([12, 18, 24]) if tech != "solar" else 12, "ppa_years": rng.choice([15, 20, 25]),
        "first_repayment_months_after_cod": rng.choice([3, 6]), "capacity_mw": mw, "cuf": {"P50": p50, "P90": p90},
        "energy_case": "P50", "degradation": 0.004 if tech == "solar" else 0.0,
        "seasonality": [0.33, 0.36, 0.155, 0.155] if tech == "solar" else [0.30, 0.20, 0.20, 0.30],
        "tariff": r2(rng.uniform(55, 95), 1), "om": {"fixed_per_mw": r2(rng.uniform(8000, 30000), 500),
                                                        "variable_per_mwh": r2(rng.uniform(2, 12), 0.5), "escalation": 0.02, "base_year": 2025},
        "tax_rate": 0.0, "capex": {"land": r2(mw * rng.uniform(0.05, 0.25), 1), "epc": r2(mw * epc_per_mw, 1), "development": r2(mw * 0.04, 1)},
        "depreciation_years": 25, "debt": {"tenor_years": 0, "gearing": rng.choice([0.70, 0.75, 0.80, 0.85]),
                                          "min_dscr": rng.choice([1.20, 1.25, 1.30, 1.35]), "upfront_fee": rng.choice([0.01, 0.0125, 0.015]),
                                          "swap": r2(rng.uniform(0.03, 0.05), 0.0025), "margin_pre": 0.0225, "margin_post": 0.0175,
                                          "repayment": "sculpted"},
        "target_equity_irr": rng.choice([0.10, 0.11, 0.12]),
    }
    c["debt"]["tenor_years"] = int(c["construction_months"] / 12 + c["ppa_years"] - rng.choice([2, 3, 4]))
    c["depreciation_years"] = max(c["ppa_years"], 25)
    c["dsra"] = {"on": rng.choice([0, 1]), "quarters": 2}   # half the mocks ask for a lender DSRA
    return c


def brief_lbo(c, minutes, path):
    d = Document()
    st = d.styles["Normal"]
    st.font.name, st.font.size = "Arial", Pt(10.5)
    d.add_heading(f"PE Associate Programme – Technical Assessment ({c['company']})", 1)
    d.add_paragraph(f"Duration: {minutes} minutes. Work in the Excel file provided and label each answer with its question number. "
                    "You will be assessed on your thought process; marks are awarded for each line item modelled correctly. "
                    "State any assumption you make.")
    d.add_heading("Background", 2)
    d.add_paragraph(f"A private equity firm is considering acquiring 100% of {c['company']}, {c['case'].split('(')[1][:-1]}. "
                    f"The vendor is asking ${c['deal']['purchase_price']/1000:,.1f} million.")
    d.add_heading("Part I", 2)
    for q in ["(a) Prepare a 5-year projection of the P&L.",
              "(b) Prepare a 5-year projection of FCFF and FCFE (a full balance sheet is not required; show workings).",
              "(c) Compute Net debt / EBITDA and the debt service coverage ratio (annual, LTM basis).",
              "(d) Complete a sources and uses table.",
              "(e) Compute the equity IRR and equity multiple for a 5-year hold.",
              "(f) Show the sensitivity of IRR to (i) purchase multiple vs exit multiple and (ii) gearing vs interest rate."]:
        d.add_paragraph(q)
    d.add_heading("Part II", 2)
    d.add_paragraph(f"(a) Calculate WACC, assuming a cost of equity of {c['dcf']['cost_of_equity']:.1%}. (b) Value the business with a DCF. "
                    "(c) Propose an alternative valuation method and describe the steps.")
    d.add_heading("Bonus", 2)
    d.add_paragraph("Prepare 1–2 PowerPoint slides introducing the target to the investment committee.")
    d.add_heading("Key assumptions", 2)
    L, dl = c["loan"], c["deal"]
    items = [
        "Acquisition completes at the end of Year 0; all acquisition-related costs are recognised in that period.",
        f"Year 0 net working capital: ${c['opening']['nwc']:,.0f}k. Year 0 shareholders' equity: ${c['opening']['equity_book']:,.0f}k.",
        f"Depreciation of existing fixed assets is ${c['dep']['existing_per_year']:,.0f}k per year; new fixed assets are depreciated over "
        f"{c['dep']['new_asset_life']} years.",
        f"Financing: a loan of ${L['amount']/1000:,.1f} million; upfront fee {L['upfront_fee_pct']:.1%} of the loan; all-in interest "
        f"{L['rate']:.2%}; straight-line amortisation over {L['tenor']} years.",
        f"Tax: {c['tax_rate']:.0%} of taxable income.",
        f"Entry and exit transaction costs: {dl['entry_cost_pct']:.1%} and {dl['exit_cost_pct']:.1%} of the respective price.",
        f"Exit at {dl['exit_multiple']:.1f}x EV/EBITDA on exit-year EBITDA, 5 years after closing.",
        "Annual forecasts are in the Excel file (Assumptions tab).",
        "For marking, assume: interest on the opening loan balance; new capex depreciated from the year it is spent (full year); "
        "all free cash flow to equity paid to the sponsor each year; any loan still outstanding at exit repaid from exit proceeds; "
        "WACC weights from the deal's capital structure at close.",
    ]
    for it in items:
        d.add_paragraph(it, style="List Bullet")
    d.save(path)


def inputs_lbo(c, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Historical P&L"
    setup(ws)
    title(ws, f"{c['company'].upper()} – Consolidated P&L", "$'000 · Year 0 = latest actual")
    h = c["historical"]
    ebitda = h["revenue"] - h["cogs"] - h["opex"]
    ebit = ebitda - h["depreciation"]
    pbt = ebit - h["interest"]
    rows = [("Revenue", h["revenue"]), ("Cost of sales", -h["cogs"]), ("Gross profit", h["revenue"] - h["cogs"]),
            ("Operating expenses", -h["opex"]), ("EBITDA", ebitda), ("Depreciation", -h["depreciation"]), ("EBIT", ebit),
            ("Interest expense", -h["interest"]), ("Profit before tax", pbt), ("Income tax expense", -h["tax"]),
            ("Profit after tax", pbt - h["tax"])]
    header_row(ws, 5, ["Year 0"], 4)
    for i, (lab, v) in enumerate(rows):
        label(ws, 6 + i, lab)
        put(ws, f"D{6+i}", round(v, 2), NUM)
    a = wb.create_sheet("Assumptions")
    setup(a)
    title(a, "Annual forecasts")
    header_row(a, 5, [f"Year {t}" for t in range(1, 6)], 4)
    dr = c["drivers"]
    for i, (lab, k, f) in enumerate([("Revenue growth", "revenue_growth", PCT), ("Gross margin (% of revenue)", "gross_margin", PCT),
                                     ("Operating expenses (% of revenue)", "opex_pct", PCT), ("Capex ($'000)", "capex", NUM),
                                     ("Net working capital (% of revenue)", "nwc_pct", PCT)]):
        label(a, 6 + i, lab)
        for t, v in enumerate(dr[k]):
            put(a, f"{chr(68+t)}{6+i}", v, f)
    s = wb.create_sheet("Sources and Uses")
    setup(s)
    title(s, "Sources and uses (to complete)")
    section(s, 5, "Uses of funds", last_col=5)
    section(s, 12, "Sources of funds", last_col=5)
    wb.save(path)


def brief_pf(c, minutes, path):
    d = Document()
    d.styles["Normal"].font.name = "Arial"
    d.add_heading(f"Analyst Programme – Financial Modelling Test ({c['project']})", 1)
    d.add_paragraph(f"Suggested time: {minutes} minutes. Build the model from scratch. You are assessed on logic, model structure and "
                    "layout, understanding of financial concepts, presentation and ease of use, accuracy, and no circularity. "
                    "Highlight any assumption you make.")
    dd = c["debt"]
    items = [
        f"Capacity {c['capacity_mw']} MWac; PPA of {c['ppa_years']} years from completion at a fixed USD {c['tariff']:.0f}/MWh.",
        f"EPC (lump sum) USD {c['capex']['epc']:,.0f}m and development costs USD {c['capex']['development']:,.0f}m, spent equally over "
        f"{c['construction_months']} months; land USD {c['capex']['land']:,.0f}m paid before construction starts.",
        f"O&M: fixed USD {c['om']['fixed_per_mw']:,.0f}/MW/yr and variable USD {c['om']['variable_per_mwh']:.2f}/MWh "
        f"({c['om']['base_year']} real), escalating {c['om']['escalation']:.1%} a year.",
        f"Capacity factor: P50 {c['cuf']['P50']:.1%}, P90 {c['cuf']['P90']:.1%}. Degradation {c['degradation']:.1%} a year. "
        f"Seasonality Q1–Q4: {', '.join(f'{s:.1%}' for s in c['seasonality'])}.",
        f"Debt: tenor {dd['tenor_years']} years from construction start; gearing up to {dd['gearing']:.0%} of total project cost; "
        f"minimum sizing DSCR {dd['min_dscr']:.2f}x; upfront fee {dd['upfront_fee']:.2%}; margin SOFR + {dd['margin_pre']:.2%} "
        f"pre-completion and + {dd['margin_post']:.2%} after; SOFR 100% hedged at {dd['swap']:.2%}.",
        f"IDC payable monthly and part of project costs. Quarterly repayments start {c['first_repayment_months_after_cod']} months "
        "after completion. Cash after debt service is paid out as dividends.",
        f"Model start date 1 January {c['start'][0]}. Straight-line depreciation over {c['depreciation_years']} years. "
        f"Client minimum equity IRR {c['target_equity_irr']:.0%}.",
        "For marking, assume: P50 case; no tax; equity is drawn before debt during construction; IDC on the opening monthly balance; "
        "land is not depreciated; depreciation starts at completion; 8,760 hours a year.",
    ]
    if c.get("dsra", {}).get("on"):
        items.append("Lenders require a debt service reserve account (DSRA) holding the next 6 months (2 quarters) of senior debt "
                     "service, funded at completion as part of project cost, topped up from available cash and released at maturity; "
                     "no interest is earned on the DSRA.")
    for it in items:
        d.add_paragraph(it, style="List Bullet")
    d.add_heading("Required", 2)
    for q in ["Total financing cost during construction (incl. IDC)", "Total revenue and opex over the project life",
              "Maximum debt from the sizing parameters", "Debt repayment profile", "Minimum and average DSCR",
              "Project and equity IRR", "3-way financial statements",
              "Bonus: lowest tariff the client can bid; sculpt repayments to a flat DSCR"]:
        d.add_paragraph(q, style="List Number")
    d.save(path)


if __name__ == "__main__":
    kind, out = sys.argv[1], os.path.abspath(sys.argv[2])
    seed = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else random.randrange(10**6)
    minutes = int(sys.argv[sys.argv.index("--minutes") + 1]) if "--minutes" in sys.argv else (105 if kind == "lbo" else 240)
    rng = random.Random(seed)
    os.makedirs(os.path.join(out, "_answer"), exist_ok=True)
    for attempt in range(25):  # redraw until the answer key passes every check (e.g. no negative cash)
        c = lbo_case(rng) if kind == "lbo" else pf_case(rng)
        name = c["company"] if kind == "lbo" else c["project"]
        c.pop("_unit", None)
        cfg = os.path.join(out, "_answer", "case.json")
        json.dump(c, open(cfg, "w", encoding="utf-8"), indent=1)
        ans = os.path.join(out, "_answer", f"Answer – {name}.xlsx")
        builder = "build_lbo.py" if kind == "lbo" else "build_pf.py"
        res = subprocess.run([sys.executable, os.path.join(HERE, builder), cfg, ans], capture_output=True, text=True)
        if res.returncode == 0:
            break
        os.remove(ans)
    else:
        sys.exit("could not generate a clean case in 25 draws: " + res.stdout[-2000:])
    if kind == "lbo":
        brief_lbo(c, minutes, os.path.join(out, f"Brief – {name}.docx"))
        inputs_lbo(c, os.path.join(out, f"Inputs – {name}.xlsx"))
    else:
        brief_pf(c, minutes, os.path.join(out, f"Brief – {name}.docx"))
    print(f"seed {seed} (draw {attempt + 1}) · {kind} · {name} · answer key verified")
    print(out)
