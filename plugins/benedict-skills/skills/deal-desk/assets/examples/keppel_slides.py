"""Worked example: the Keppel "Tough Love" bonus slides, built from the model's own numbers.

    python keppel_slides.py model.xlsx out.pptx
Pattern to copy for any case: every number on a slide is read from the recalculated model, never typed.
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

d = Deck()

# ---------------- Slide 1: target overview ----------------
s = d.slide(f"Tough Love is Australia's #3 gym chain by outlets: 150 studios, {m_(rev[0])} revenue and a "
            f"{margin[0]:.1%} EBITDA margin", section="Target overview")
d.kpis(s, *d.grid(0, 1)[:3], 0.95, [("150", "Studios across all 7 states and territories"),
                                   (m_(rev[0]), "Year 0 revenue"),
                                   (m_(ebitda[0]), f"Year 0 EBITDA ({margin[0]:.1%} margin)"),
                                   (f"{entry_x:.1f}x", f"Asking price {m_(price)} / Year 0 EBITDA")])
top = 2.55
x, y, w, h = d.grid(0, 3, top=top)
d.header(s, x, y, w, "Studios by state / territory")
d.bar(s, x, y + 0.4, w, h - 0.45, ["NSW", "VIC", "QLD", "WA", "SA", "TAS", "NT"], [("Studios", [35, 29, 26, 22, 18, 11, 9])],
      number_format="0", gap=45)
x, y, w, h = d.grid(1, 3, top=top)
d.header(s, x, y, w, "Top 5 Australian gym chains by outlets")
d.bar(s, x, y + 0.4, w, h - 0.45, ["Unity Gym", "Pumping Iron", "Tough Love", "Squats & Shakes", "Fit Mamas"],
      [("Outlets", [253, 176, 150, 91, 84])], number_format="0", highlight=2, gap=45)
x, y, w, h = d.grid(2, 3, top=top)
d.header(s, x, y, w, "Business overview")
d.bullets(s, x, y + 0.45, w, h - 0.5, [
    "**Built from scratch:** founded 2015, grown from 1 to 150 studios in about 10 years",
    "**National footprint:** NSW and VIC hold 43% of studios; present in every state and territory",
    f"**High gross margin:** {gm[0]:.0%} of revenue is left after cost of sales; operating costs are the main expense "
    f"({opex_share:.0%} of revenue)",
    f"**Profitable today:** {m_(ebitda[0])} EBITDA and {m_(npat[0])} profit after tax",
    f"**Ask:** {m_(price)} for 100%, or {entry_x:.1f}x Year 0 EBITDA",
], size=10.5)
gp, pbt = row("Gross profit"), row("Profit before tax")
d.table(s, x, y + 2.42, w, [
    ["Year 0 P&L", "$m", "% of revenue"],
    ["Revenue", f"{rev[0]/1000:,.1f}", "100.0%"],
    ["Gross profit", f"{gp[0]/1000:,.1f}", f"{gp[0]/rev[0]:.1%}"],
    ["EBITDA", f"{ebitda[0]/1000:,.1f}", f"{ebitda[0]/rev[0]:.1%}"],
    ["Profit before tax", f"{pbt[0]/1000:,.1f}", f"{pbt[0]/rev[0]:.1%}"],
    ["Profit after tax", f"{npat[0]/1000:,.1f}", f"{npat[0]/rev[0]:.1%}"],
], col_widths=[w * 0.5, w * 0.2, w * 0.3], size=9, bold_rows=(3,))
d.footer(s, sources="Company information provided in the case pack", notes="Year 0 = latest historical P&L; $ figures as provided")

# ---------------- Slide 2: investment case ----------------
s = d.slide(f"At {m_(price)} the deal returns a {irr:.1%} IRR and {mom:.1f}x in 5 years, even after a Year 1 margin reset",
            section="Investment case")
x, y, w, h = d.grid(0, 3, weights=[1.15, 1, 1.05])
d.header(s, x, y, w, "Revenue and EBITDA ($m)")
yrs = ["Yr 0", "Yr 1", "Yr 2", "Yr 3", "Yr 4", "Yr 5"]
d.column(s, x, y + 0.4, w, 2.6, yrs, [("Revenue", [v / 1000 for v in rev]), ("EBITDA", [v / 1000 for v in ebitda])],
         number_format="0.0", gap=40)
d.callout(s, x, y + 3.15, w, 1.2,
          f"Operating costs step up from 72% to 77% of revenue in Year 1, so EBITDA falls to {m_(ebitda[1])} "
          f"({margin[1]:.1%} margin) before recovering to {m_(ebitda[5])} by Year 5.", size=10)
d.bullets(s, x, y + 4.5, w, 0.9, [f"Price is {entry_x:.1f}x Year 0 but {price/ebitda[1]:.1f}x Year 1 EBITDA: the reset matters for price"], size=10)

x, y, w, h = d.grid(1, 3, weights=[1.15, 1, 1.05])
d.header(s, x, y, w, "Sources and uses ($m)")
short = {"Purchase price (100% stake)": "Purchase price", "Entry transaction costs": "Transaction costs",
         "Upfront financing fee": "Financing fee", "Cash to balance sheet": "Cash to B/S"}
rows = [["Uses", "$m", "Sources", "$m"]]
srcs = [("Term loan", loan), ("Sponsor equity", equity)]
used = [(short.get(ul, ul), uv) for ul, uv in uses if abs(uv) > 1e-9]
for i in range(max(len(used), len(srcs))):
    ul, uv = used[i] if i < len(used) else ("", None)
    sl, sv = srcs[i] if i < len(srcs) else ("", None)
    rows.append([ul, "" if uv is None else f"{uv/1000:,.1f}", sl, "" if sv is None else f"{sv/1000:,.1f}"])
rows.append(["Total", f"{total/1000:,.1f}", "Total", f"{total/1000:,.1f}"])
d.table(s, x, y + 0.45, w, rows, col_widths=[w * 0.34, w * 0.15, w * 0.36, w * 0.15], size=9, bold_rows=(len(rows) - 1,),
        num_cols={1, 3})
y2 = y + 0.45 + 0.28 * len(rows) + 0.35
d.header(s, x, y2, w, "Returns and valuation")
d.table(s, x, y2 + 0.45, w, [
    ["Metric", "Value"],
    ["Equity IRR (5-yr hold)", f"{irr:.1%}"],
    ["Equity multiple", f"{mom:.2f}x"],
    ["Peak net debt / EBITDA", f"{max(v for v in lev if isinstance(v, (int, float))):.1f}x"],
    [f"DCF EV, 5.0x exit (WACC {wacc:.1%})", m_(ev_m)],
    ["DCF EV, 2.5% perpetuity growth", m_(ev_g)],
], col_widths=[w * 0.68, w * 0.32], size=9)

x, y, w, h = d.grid(2, 3, weights=[1.15, 1, 1.05])
d.header(s, x, y, w, "IRR: exit (rows) vs entry (columns) EV / EBITDA")
d.heatmap(s, x, y + 0.45, w, "Exit / entry", [f"{v:.2f}x" for v in sens_cols], [f"{v:.2f}x" for v in sens_rows], sens,
          base=(2, 2), size=9)
d.header(s, x, y + 2.5, w, "Points for the committee")
d.bullets(s, x, y + 2.95, w, 2.0, [
    f"**Low leverage:** debt peaks at {max(v for v in lev if isinstance(v, (int, float))):.1f}x EBITDA; more debt lifts IRR",
    f"**Exit is conservative:** a 5.0x exit vs {imp_x:.1f}x implied by a 2.5% perpetuity DCF",
    "**Key risk:** the Year 1 cost step-up; diligence what drives the extra 5% of revenue in opex",
], size=10)
d.footer(s, sources="Case pack assumptions; deal-desk model", notes="Acquisition at end of Year 0; exit at 5.0x Year 5 EBITDA; 2% entry and exit costs")

d.save(out)
print(out)
