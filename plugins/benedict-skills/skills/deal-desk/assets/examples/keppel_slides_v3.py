"""Worked example V3: the Keppel "Tough Love" slides rebuilt with the layout library (no AI tells).

    python keppel_slides_v3.py model.xlsx out.pptx
Same data as keppel_slides.py (every number read from the model); different layouts: icon stats, side tabs,
pills, hero number, dashed takeaway. Compare the two renders to see what changed.
"""
import os
import sys

from openpyxl import load_workbook

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts"))
from ibdeck import Deck  # noqa: E402

model_path, out = sys.argv[1], sys.argv[2]
wb = load_workbook(model_path, data_only=True)
m, deal = wb["Model"], wb["Deal"]


def row(label, sheet=m):
    """Model grid (house style v2): label in B, constants in D, Year 0..5 in F..K. Returns [Year 0..5] or [constant]."""
    for r in range(1, sheet.max_row + 1):
        v = sheet.cell(r, 2).value
        if isinstance(v, str) and v.strip() == label:
            yrs = [sheet.cell(r, c).value for c in range(6, 12)]
            if sheet is m and any(isinstance(x, (int, float)) for x in yrs):
                return yrs
            return [sheet.cell(r, 4).value]   # Deal sheet and single-value lines: column D
    raise KeyError(label)


def named(name):
    """Values of a named range (e.g. a sensitivity table) as a list of rows."""
    dn = wb.defined_names[name]
    (sheet, rng), = list(dn.destinations)
    return [[c.value for c in r] for r in wb[sheet][rng.replace("$", "")]]


rev, ebitda = row("Revenue"), row("EBITDA")
margin = row("EBITDA margin")
gm, npat = row("Gross margin"), row("Profit after tax")
opex_share = -row("Operating expenses")[0] / rev[0]
irr, mom = row("Equity IRR")[0], row("Equity multiple (MoM)")[0]
lev = row("Net debt / EBITDA")
ev_m, ev_g = row("Enterprise value – exit multiple method")[0], row("Enterprise value – perpetuity method")[0]
imp_x = row("Implied exit multiple from perpetuity method")[0]
wacc = row("WACC")[0]
price = row("Purchase price used", deal)[0]
entry_x = row("Implied entry EV / Year 0 EBITDA", deal)[0]
uses = [(lab, row(lab, deal)[0]) for lab in ("Purchase price (100% stake)", "Entry transaction costs",
                                                "Upfront financing fee", "Cash to balance sheet")]
equity, loan, total = row("Sponsor equity", deal)[0], row("Term loan", deal)[0], row("Total uses", deal)[0]
grid = named("Sens_Entry_Exit")            # corner, entry multiples across the top, exit multiples down the side
sens_cols = grid[0][1:]
sens_rows = [r[0] for r in grid[1:]]
sens = [r[1:] for r in grid[1:]]

m_ = lambda v: f"${v/1000:,.1f}m"  # noqa: E731  ($'000 -> $m)
SECTIONS = ["Target Overview", "Investment Case"]
d = Deck(sections=SECTIONS)
peak_lev = max(v for v in lev if isinstance(v, (int, float)))
gp = row("Gross profit")

# ---------------- Slide 1: target overview ----------------
s = d.slide("Target Overview", "Australia's #3 gym chain by outlets, profitable today")
wts = [1, 1.05, 1.1]
x, y, w, h = d.grid(0, 3, weights=wts)
d.header(s, x, y, w, "At a glance")
d.stat_icons(s, x, y + 0.45, w, 2.35, [
    ("building-store", "150", "Studios in all 7 states and territories"),
    ("cash", m_(rev[0]), "Year 0 revenue"),
    ("chart-bar", m_(ebitda[0]), f"Year 0 EBITDA ({margin[0]:.1%} margin)"),
    ("scale", f"{entry_x:.1f}x", f"Asking price {m_(price)} / Year 0 EBITDA")], cols=2, icon_size=0.42)
d.header(s, x, y + 2.95, w, "P&L summary ($m)")
d.fin_table(s, x, y + 3.35, w, ["Year 0A"], [
    ("Revenue", [rev[0] / 1000], "key"),
    ("Gross profit", [gp[0] / 1000]),
    ("% Margin", [gp[0] / rev[0]], "pct"),
    ("EBITDA", [ebitda[0] / 1000], "key"),
    ("% Margin", [ebitda[0] / rev[0]], "pct"),
    ("Profit after tax", [npat[0] / 1000]),
    ("% Margin", [npat[0] / rev[0]], "pct"),
])

x, y, w, h = d.grid(1, 3, weights=wts)
d.header(s, x, y, w, "Top 5 Australian gym chains by outlets")
d.bar(s, x, y + 0.4, w, 2.4, ["Unity Gym", "Pumping Iron", "Tough Love", "Squats & Shakes", "Fit Mamas"],
      [("Outlets", [253, 176, 150, 91, 84])], number_format="0", highlight=2, gap=45)
d.header(s, x, y + 2.95, w, "Studios by state / territory")
d.column(s, x, y + 3.3, w, 1.8, ["NSW", "VIC", "QLD", "WA", "SA", "TAS", "NT"], [("Studios", [35, 29, 26, 22, 18, 11, 9])],
         number_format="0", gap=40)

x, y, w, h = d.grid(2, 3, weights=wts)
d.header(s, x, y, w, "Why it stands out")
d.pill_rows(s, x, y + 0.5, w, h - 0.5, [
    ("Built from scratch\nFounded 2015", ["1 to 150 studios in about 10 years"]),
    ("National footprint\n7 of 7 states", ["NSW and VIC hold 43% of studios; room to grow in WA, SA, TAS, NT"]),
    (f"High margin\n{gm[0]:.0%} gross", [f"Operating costs are the main expense ({opex_share:.0%} of revenue)"]),
    ("Profitable today", [f"{m_(ebitda[0])} EBITDA and {m_(npat[0])} profit after tax"]),
], label_w=1.45, max_row_h=1.1)
d.footer(s, sources="Company information provided in the case pack", notes="Year 0 = latest historical P&L; $ figures as provided")

# ---------------- Slide 2: investment case ----------------
s = d.slide("Investment Case", f"Returns, funding and valuation at the {m_(price)} asking price")
wts = [1.1, 1, 1.05]
ROW2 = 2.5                                  # every second-row block header starts here (aligned)
x, y, w, h = d.grid(0, 3, weights=wts)
d.header(s, x, y, w, "Returns: 5-year hold")
d.hero_number(s, x, y + 0.4, w, 1.9, f"{irr:.1%}", "Equity IRR", [
    f"**{mom:.2f}x** money multiple", f"**{entry_x:.1f}x** entry, **5.0x** exit", f"**{peak_lev:.1f}x** peak leverage"])
d.header(s, x, y + ROW2, w, "EBITDA and margin ($m)")
yrs = [f"Y{k}{'A' if k == 0 else 'E'}" for k in range(6)]
cagr_15 = (ebitda[5] / ebitda[1]) ** (1 / 4) - 1
d.fin_chart(s, x, y + ROW2 + 0.4, w, 1.5, yrs, [v / 1000 for v in ebitda], strip=margin, strip_label="% Margin",
            cagr=[(1, 5, f"Y1E\u2013Y5E CAGR: {cagr_15:.1%}")], split=1)
d.takeaway(s, x, y + ROW2 + 1.95, w, 0.75,
           f"Opex steps up from 72% to 77% of revenue in Year 1: EBITDA dips to {m_(ebitda[1])} "
           f"({margin[1]:.1%}) before recovering to {m_(ebitda[5])}. Price is {price/ebitda[1]:.1f}x Year 1 EBITDA.")

x, y, w, h = d.grid(1, 3, weights=wts)
d.header(s, x, y, w, "Sources and uses ($m)")
short = {"Purchase price (100% stake)": "Purchase price", "Entry transaction costs": "Transaction costs",
         "Upfront financing fee": "Financing fee", "Cash to balance sheet": "Cash to B/S"}
rows = [["Uses", "", "Sources", ""]]
srcs = [("Term loan", loan), ("Sponsor equity", equity)]
used = [(short.get(ul, ul), uv) for ul, uv in uses if abs(uv) > 1e-9]
for i in range(max(len(used), len(srcs))):
    ul, uv = used[i] if i < len(used) else ("", None)
    sl, sv = srcs[i] if i < len(srcs) else ("", None)
    rows.append([ul, "" if uv is None else f"{uv/1000:,.1f}", sl, "" if sv is None else f"{sv/1000:,.1f}"])
rows.append(["Total", f"{total/1000:,.1f}", "Total", f"{total/1000:,.1f}"])
d.table(s, x, y + 0.45, w, rows, col_widths=[w * 0.34, w * 0.15, w * 0.36, w * 0.15], bold_rows=(len(rows) - 1,),
        num_cols={1, 3})
y2 = y + ROW2
d.header(s, x, y2, w, "Valuation cross-check ($m)")
d.stat_strip(s, x, y2 + 0.4, w, 0.7, [(m_(price), "Asking price"), (m_(ev_m), "DCF, 5.0x exit"),
                                        (m_(ev_g), "DCF, 2.5% growth")])
d.stat_rings(s, x, y2 + 1.2, w, 1.5, [(equity / total, "Funded by sponsor equity"), (loan / total, "Funded by term loan")],
             )

x, y, w, h = d.grid(2, 3, weights=wts)
d.header(s, x, y, w, "IRR: exit (rows) vs entry (columns) EV / EBITDA")
d.heatmap(s, x, y + 0.45, w, "Exit / entry", [f"{v:.2f}x" for v in sens_cols], [f"{v:.2f}x" for v in sens_rows], sens,
          base=(2, 2))
d.header(s, x, y + ROW2, w, "Points for the committee")
d.side_tabs(s, x, y + ROW2 + 0.45, w, 2.25, [
    ("Low leverage", f"Debt peaks at {peak_lev:.1f}x EBITDA; more debt would lift the IRR"),
    ("Safe exit", f"5.0x exit vs {imp_x:.1f}x implied by a 2.5% perpetuity DCF"),
    ("Key risk", "The Year 1 cost step-up: diligence what drives the extra 5% of revenue in opex"),
], tab_w=1.2, max_row_h=0.75)
d.footer(s, sources="Case pack assumptions; deal-desk model", notes="Acquisition at end of Year 0; exit at 5.0x Year 5 EBITDA; 2% entry and exit costs")

d.save(out)
print(out)
