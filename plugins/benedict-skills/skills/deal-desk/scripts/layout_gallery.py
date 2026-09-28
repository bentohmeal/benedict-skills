"""Layout gallery: one slide per family of ibdeck layouts, filled with Tough Love case data, so Benedict can pick
favourites and Claude can see every option before planning a deck.

    python layout_gallery.py "C:\\Users\\user\\Documents\\Google Drive\\Claude Things\\output\\_Deal Desk Toolkit\\Deck Layout Gallery.pptx"
Figures marked (illustrative) are placeholders for layout only; real decks read every number from the model.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ibdeck import Deck  # noqa: E402

out = sys.argv[1] if len(sys.argv) > 1 else "Deck Layout Gallery.pptx"
SECTIONS = ["Key Numbers", "Financials", "Markets", "Thesis", "Plans", "Drivers", "Risks", "Dense Pages"]
NOTE = "Layout samples on Tough Love case data; (illustrative) marks placeholder figures"

d = Deck(sections=SECTIONS)
d.title_slide("Deck layout gallery", "Every ibdeck layout on one page each: pick favourites, avoid repeats",
              date="Sep 2026", name="deal-desk")

# 1 ---------------- key numbers ----------------
s = d.slide("Key Numbers", "Icon stats, a stat strip, a headline number and a pictogram")
x, y, w, h = d.grid(0, 3)
d.header(s, x, y, w, "stat_icons: icon, number, label")
d.stat_icons(s, x, y + 0.5, w, 4.3, [
    ("building-store", "150", "Studios across all 7 states and territories"),
    ("cash", "$75.0m", "Year 0 revenue"),
    ("chart-bar", "$16.4m", "Year 0 EBITDA (21.9% margin)"),
    ("scale", "4.9x", "Asking price of $80.0m / Year 0 EBITDA")], cols=2)
x, y, w, h = d.grid(1, 3)
d.header(s, x, y, w, "stat_strip under a chart: revenue ($m)")
d.column(s, x, y + 0.4, w, 3.1, ["Yr 0", "Yr 1", "Yr 2", "Yr 3", "Yr 4", "Yr 5"],
         [("Revenue", [75.0, 80.3, 85.1, 89.3, 92.0, 94.8])], number_format="0.0", gap=45)
d.stat_strip(s, x, y + 3.7, w, 0.9, [("4.8%", "Revenue CAGR, Yr 0–5"), ("$19.0m", "Year 5 EBITDA"),
                                     ("20.0%", "Year 5 margin")])
x, y, w, h = d.grid(2, 3)
d.header(s, x, y, w, "hero_number: the one number that matters")
d.hero_number(s, x, y + 0.45, w, 1.9, "18.5%", "Equity IRR, 5-year hold",
              ["**2.1x** money multiple", "**4.9x** in, **5.0x** out", "**0.9x** peak leverage"])
d.header(s, x, y + 2.65, w, "pictogram: a share you can count")
d.pictogram(s, x, y + 3.15, w, 1.8, 64 / 150, total=20, cols=10,
            label="**43%** of studios (64 of 150) are in NSW and VIC")
d.footer(s, sources="Keppel case pack; deal-desk model", notes=NOTE)

# 1b ---------------- financials (bank format: Goldman / Evercore board books, assets/references/bank-financials) ---
REV = [75.0, 80.3, 85.1, 89.3, 92.0, 94.8]
EBITDA = [16.4, 12.8, 14.5, 17.0, 18.4, 19.0]
YRS = [f"Y{k}{'A' if k == 0 else 'E'}" for k in range(6)]
growth = [None] + [REV[k] / REV[k - 1] - 1 for k in range(1, 6)]
s = d.slide("Financials", "A bank-style table for line items, a chart with a % strip for the trend")
x, y, w, h = d.grid(0, 2, weights=[1.25, 1])
d.header(s, x, y, w, "fin_table: P&L summary ($m)")
d.fin_table(s, x, y + 0.5, w, YRS, [
    ("Revenue", REV, "key"),
    ("% Growth", growth, "pct"),
    ("Gross profit", [r * 0.94 for r in REV]),
    ("% Margin", [0.94] * 6, "pct"),
    ("EBITDA", EBITDA, "key"),
    ("% Margin", [e / r for e, r in zip(EBITDA, REV)], "pct"),
], row_h=0.3)
d.takeaway(s, x, y + 3.0, w, 0.75, "Table when readers need the line items (projections, appendix); chart + % strip "
           "when the point is the trend. Units once, in the header bar; periods marked A / E.")
x, y, w, h = d.grid(1, 2, weights=[1.25, 1])
d.header(s, x, y, w, "fin_chart: revenue ($m)")
d.fin_chart(s, x, y + 0.5, w, 3.2, YRS, REV, strip=growth, strip_label="% Growth",
            cagr=[(1, 5, f"Y1E–Y5E CAGR: {(REV[5] / REV[1]) ** 0.25 - 1:.1%}")], split=1)
d.footer(s, sources="Keppel case pack; deal-desk model", notes=NOTE)

# 2 ---------------- shares and markets ----------------
s = d.slide("Markets", "Rings for shares, nested circles for market size")
x, y, w, h = d.grid(0, 2, weights=[1, 1.1])
d.header(s, x, y, w, "stat_rings: share of a whole")
d.stat_rings(s, x, y + 0.5, w, 2.35, [(0.94, "Gross margin"), (0.72, "Operating costs / revenue"),
                                      (0.43, "Studios in NSW + VIC")])
d.header(s, x, y + 3.15, w, "logo_row: peers, buyers or sponsors")
d.logo_row(s, x, y + 3.65, w, 1.35, ["Unity Gym", "Pumping Iron", "Tough Love", "Squats & Shakes", "Fit Mamas", "Other"],
           highlight="Tough Love", cols=3)
x, y, w, h = d.grid(1, 2, weights=[1, 1.1])
d.header(s, x, y, w, "tam_sam_som: market sizing (illustrative)")
d.tam_sam_som(s, x, y + 0.55, w, 3.3, [
    ("TAM", "A$3.2bn", "Australian gym and fitness market (illustrative)"),
    ("SAM", "A$1.1bn", "Budget and 24/7 studio segment (illustrative)"),
    ("SOM", "A$75m", "Tough Love revenue today, about 7% of SAM")])
d.takeaway(s, x, y + 4.1, w, 0.75, "takeaway(): the 'so what' in a dashed outline. **No pale box with a coloured "
           "side bar**, which is the classic AI tell.")
d.footer(s, sources="Keppel case pack", notes=NOTE)

# 3 ---------------- thesis ----------------
s = d.slide("Thesis", "Each pillar argues: claim, evidence, what it means for returns")
x, y, w, h = d.grid(0, 2)
d.header(s, x, y, w, "side_tabs: investment thesis (claim + so what)")
# lessons #35: argument rows = (bold claim, evidence -> so what -> "For returns:"); a fact list here is THIN ARGUMENT
d.side_tabs(s, x, y + 0.45, w, h - 0.45, [
    ("Scale", ("A national footprint that rivals would take years to copy",
               "Tough Love is Australia's #3 chain by outlets, with 150 studios across all 7 states and territories, "
               "spreading brand and overhead costs over a large base. **For returns:** a platform to add studios, not a "
               "single-site bet.")),
    ("Economics", ("Each member dollar is highly profitable",
                   "Gross margin is 94%, and the business earned $16.4m EBITDA (21.9% margin) and $12.1m profit after tax "
                   "in Year 0. **For returns:** cash flow services the debt from day one and funds new studios.")),
    ("Returns", ("Returns hold up even after a weak first year",
                 "At an $80.0m entry the case delivers an 18.5% IRR and 2.1x money in 5 years, after absorbing the Year 1 "
                 "margin reset. **For returns:** the base case does not need margin expansion to work.")),
    ("Low debt", ("Low leverage leaves room for error",
                  "Leverage peaks at only 0.9x, so the Year 1 cost step-up (EBITDA dips to $12.8m) does not strain the "
                  "balance sheet. **For returns:** the equity absorbs a soft year without new capital.")),
], tab_w=1.4)
x, y, w, h = d.grid(1, 2)
d.header(s, x, y, w, "pill_rows: business overview")
d.pill_rows(s, x, y + 0.45, w, h - 0.45, [
    ("Built from scratch\nFounded 2015", ["Grown from 1 to 150 studios in about 10 years", "Owner-operated model"]),
    ("National footprint\n7 of 7 states", ["NSW and VIC hold 43% of studios", "Room to fill in WA, SA, TAS and NT"]),
    ("High margin\n94% gross", ["Operating costs are the main expense (72% of revenue)", "$12.1m profit after tax"]),
])
d.footer(s, sources="Keppel case pack; deal-desk model", notes=NOTE)

# 4 ---------------- plans and history ----------------
s = d.slide("Plans", "Chevrons for the plan, a timeline for the history")
x, y, w, h = d.grid(0, 1)
d.header(s, x, y, w, "chevrons: value-creation plan (illustrative)")
d.chevrons(s, x, y + 0.45, w, 2.05, [
    ("Stabilise costs", ["Reset opex back to 72% of revenue", "Renegotiate the top 20 leases"]),
    ("Fill the map", ["Add studios in WA, SA and TAS", "Target 190 studios by Year 5"]),
    ("Lift yield", ["Premium tier and PT packages", "Price up 2–3% a year"]),
    ("Exit", ["Sell to a strategic or sponsor at 5.0x+", "Year 5 EBITDA of $19.0m"]),
])
d.header(s, x, y + 2.75, w, "timeline: company history (illustrative dates)")
d.timeline(s, x, y + 3.2, w, 1.85, [
    ("2015", "First studio", "Founded in Sydney"), ("2017", "25 studios", "Enters VIC and QLD"),
    ("2019", "75 studios", "National brand launch"), ("2022", "120 studios", "All 7 states and territories"),
    ("2025", "150 studios", "#3 chain by outlets"), ("Year 0", "Sale", "$80.0m asking price")], highlight=5)
d.footer(s, sources="Keppel case pack", notes=NOTE)

# 5 ---------------- drivers, steps, scoring ----------------
s = d.slide("Drivers", "Hub-and-spoke, numbered steps and Harvey balls")
x, y, w, h = d.grid(0, 3, weights=[1.25, 1, 1])
d.header(s, x, y, w, "hub_spoke: growth drivers")
d.hub_spoke(s, x, y + 0.4, w, h - 0.4, "Tough Love", [
    ("map-pin", "New studios", "Gaps in WA, SA, TAS"), ("users", "Members", "Retention and referrals"),
    ("cash", "Pricing", "2–3% a year"), ("barbell", "Premium tier", "PT and classes"),
    ("building-store", "Tuck-ins", "Buy small chains")])
x, y, w, h = d.grid(1, 3, weights=[1.25, 1, 1])
d.header(s, x, y, w, "numbered_steps: first 100 days")
d.numbered_steps(s, x, y + 0.5, w, h - 0.5, [
    ("Cost review", "Find the drivers of the 5-point opex step-up"),
    ("Lease plan", "Rank studios by rent / revenue"),
    ("Pricing test", "Trial a premium tier in 10 studios"),
    ("Pipeline", "Sign 8 new sites for Year 1"),
    ("Reporting", "Weekly studio KPIs to the board")])
x, y, w, h = d.grid(2, 3, weights=[1.25, 1, 1])
d.header(s, x, y, w, "harvey: peer scoring (illustrative)")
d.harvey(s, x, y + 0.45, w, ["Unity Gym", "Pumping Iron", "Tough Love", "Squats & Shakes", "Fit Mamas"],
         ["Scale", "Margin", "Growth"], [[4, 2, 1], [3, 3, 2], [3, 4, 3], [1, 2, 4], [1, 1, 3]], row_h=0.5)
d.footer(s, sources="Keppel case pack", notes=NOTE)

# 6 ---------------- risks ----------------
s = d.slide("Risks", "Risks beside their mitigants, then strengths and watch-points")
x, y, w, h = d.grid(0, 2, weights=[1.3, 1])
d.header(s, x, y, w, "risk_matrix: title + impact → action + what remains")
# lessons #35: each side = (bold title, 1-2 sentences); mitigants end with "What remains:"
d.risk_matrix(s, x, y + 0.5, w, h - 0.5, [
    (("Cost step-up", "Opex rises from 72% to 77% of revenue in Year 1, cutting EBITDA to $12.8m and testing the entry "
                      "price."),
     ("Price the reset in", "The $80.0m entry already assumes the Year 1 step-up; diligence its drivers. **What "
                            "remains:** a longer or deeper reset.")),
    (("Competition", "Unity Gym has 253 outlets, well ahead of Tough Love's 150, and could undercut on price in shared "
                     "catchments."),
     ("Differentiate on access", "A lower price point and 24/7 access in every studio keep members loyal. **What "
                                 "remains:** a price war in key suburbs.")),
    (("Lease exposure", "Rent is the largest fixed cost, so a dip in revenue falls straight to profit while lease "
                        "payments stay fixed."),
     ("Stagger and review leases", "Expiries are staggered; review the top 20 leases in diligence. **What remains:** "
                                   "rent resets at renewal.")),
    (("Key people", "The business has been founder-led since 2015, so a founder exit could disrupt strategy and new "
                    "openings."),
     ("Lock in management", "Management rolls over equity and the founder stays for a 12-month transition. **What "
                            "remains:** execution after the handover.")),
], levels=[4, 2, 2, 1])
x, y, w, h = d.grid(1, 2, weights=[1.3, 1])
d.pros_cons(s, x, y, w, h, [
    "**Scale:** #3 by outlets", "**Margin:** 94% gross", "**Cash:** profitable today", "**Leverage:** only 0.9x peak"],
    ["**Year 1 reset:** EBITDA dips to $12.8m", "**Rent:** fixed-cost heavy", "**Founder:** key-person risk"])
d.footer(s, sources="Keppel case pack; deal-desk model", notes=NOTE)

# 7 ---------------- dense pages (bank density standard, lessons #32) ----------------
# Recipes copied from real bank pages in 01. IB PE\Investment Banking Library\Real IB-PE Decks\ (see _Index.md), filled
# with the sourced Singapore data-centre figures (assets/examples/sg_dc_slides.py DATA) and Tough Love case data.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "examples"))
from sg_dc_slides import DATA, CBRE, IMG  # noqa: E402
from ibdeck import L, W, R_, TOP, BOTTOM, GUTTER, NAVY, STEEL, LIGHT  # noqa: E402
from pptx.enum.shapes import MSO_SHAPE  # noqa: E402
from pptx.enum.text import PP_ALIGN  # noqa: E402

x0, bw = L, W - L - R_
mk = DATA["markets"]
sg_live, sg_up = mk["Singapore"]
DSRC = f"{CBRE}; TechDirectory (Jul 2026); company releases"

# D1 framing strip + three exhibits (Qatalyst Autonomy p4)
s = d.slide("Dense Pages", "Market page: framing strip over three exhibits (Qatalyst p4)")
half = (bw - 1.0) / 2
d.header(s, x0, TOP, half, "Framing strip: left side")
d.bullets(s, x0, TOP + 0.38, half, 0.95, [
    "**Big Tech capex +61% in 2026:** AI training and inference need large, power-dense halls",
    "**Two bold lead-in bullets per side**, each carrying a number, set up the tension the exhibits prove"])
d._shape(s, MSO_SHAPE.RIGHT_ARROW, x0 + half + 0.15, TOP + 0.35, 0.7, 0.6, fill=STEEL)
d.header(s, x0 + half + 1.0, TOP, half, "Framing strip: right side")
d.bullets(s, x0 + half + 1.0, TOP + 0.38, half, 0.95, [
    f"**Pipeline is thin:** {sg_up}MW upcoming vs {sg_live}MW live in Singapore",
    "**The arrow** carries the reader from the cause to the constraint"])
y2 = TOP + 1.45
ew = (bw - 2 * GUTTER) / 3
d.header(s, x0, y2, ew, "Exhibit 1: column chart (US$bn)")
d.exhibit_takeaway(s, x0, y2 + 0.33, ew, "exhibit_takeaway(): the finding, bold, above the chart")
d.column(s, x0, y2 + 0.75, ew, BOTTOM - y2 - 0.75, [c for c, _ in DATA["capex"]],
         [("US$bn", [v for _, v in DATA["capex"]])], gap=80)
e2 = x0 + ew + GUTTER
order = sorted(mk, key=lambda m: -(mk[m][1] / mk[m][0]))
d.header(s, e2, y2, ew, "Exhibit 2: two-series bar (MW)")
d.exhibit_takeaway(s, e2, y2 + 0.33, ew, f"Singapore's pipeline is {sg_up / sg_live:.0%} of live stock")
d.bar(s, e2, y2 + 0.75, ew, BOTTOM - y2 - 0.75, order,
      [("Live", [mk[m][0] for m in order]), ("Upcoming", [mk[m][1] for m in order])], colors=[NAVY, LIGHT], gap=40)
e3 = e2 + ew + GUTTER
d.header(s, e3, y2, ew, "Exhibit 3: evidence table")
d.exhibit_takeaway(s, e3, y2 + 0.33, ew, "Tables work as exhibits too: who, what, when")
d.table(s, e3, y2 + 0.78, ew, [["Who", "Commitment", "Timing"],
                               ["AWS", "S$12bn more (S$23bn+ total)", "To 2028"],
                               ["Digital Realty", "S$4.3bn+ for new builds", "Apr 2026"],
                               ["DC-CFA2", "200MW to four operators", "Aug 2026"],
                               ["Equinix", "SG6: US$260m+, 20MW", "Q1 2027"],
                               ["Keppel", "25MW floating DC", "2028"]],
        col_widths=[0.95, ew - 1.75, 0.8], num_cols=(), row_h=0.42)
d.footer(s, sources=DSRC, notes="Recipe: framing strip + 3 exhibits, each with header bar, one-line finding and units")

# D2 photo + fact strip + chart
s = d.slide("Dense Pages", "Overview page: photo, fact strip, chart and commentary")
lw = 3.85
d.header(s, x0, TOP, lw, "photo(): crop-to-fill, credit auto-added")
d.photo(s, os.path.join(IMG, "photo-dc-racks.jpg"), x0, TOP + 0.4, lw, 1.75)
d.bullets(s, x0, TOP + 2.25, lw, BOTTOM - TOP - 2.25, [
    f"**Anchor hub:** {sg_live}MW live, on a par with Seoul and Mumbai",
    "**Near-full:** occupancy above 95%; a landlord's market",
    f"**Premium pricing:** {DATA['sg_rent_range']} per kW a month",
    "**Rule:** a photo earns its place only beside the fact it shows, never as decoration",
    "**Source:** fetch_image.py logs the licence and author; footer() prints the credit on the slide"])
rx = x0 + lw + GUTTER
rw = W - R_ - rx
d.header(s, rx, TOP, rw, "stat_icons(): five key numbers across the top")
d.stat_icons(s, rx, TOP + 0.42, rw, 1.3, [("server", f"{sg_live}MW", "Live capacity"),
                                          ("trending-up", f"{sg_up}MW", "Upcoming"),
                                          ("percentage", ">95%", "Occupancy"),
                                          ("cash", DATA["sg_rent_range"], "Rent per kW per month"),
                                          ("bolt", "~7%", "Share of electricity")], icon_size=0.42)
y2 = TOP + 1.95
cw = 4.75
d.header(s, rx, y2, cw, "bar(): long category names, one gold highlight")
order = sorted(mk, key=lambda m: -mk[m][0])
d.exhibit_takeaway(s, rx, y2 + 0.33, cw, "Use bar(), not column(), when labels would rotate")
d.bar(s, rx, y2 + 0.72, cw, BOTTOM - y2 - 0.72, order, [("Live MW", [mk[m][0] for m in order])],
      highlight=order.index("Singapore"), gap=35)
bx = rx + cw + GUTTER
d.header(s, bx, y2, W - R_ - bx, "Commentary beside the chart")
d.bullets(s, bx, y2 + 0.4, W - R_ - bx, BOTTOM - y2 - 0.4, [
    "**Connectivity:** 28 subsea cables land in Singapore, with at least 13 more planned",
    "**Hyperscalers:** AWS plans a further S$12bn to 2028; Digital Realty targets ~S$7bn",
    "**Barriers:** US$14.5/W to build, second only to Tokyo",
    "**Rule:** each bullet = bold lead-in + one number, and the column runs to the bottom"])
d.footer(s, sources=DSRC + "; CSIS (Sep 2025); Turner & Townsend (2025)", notes="Recipe: photo + fact strip + chart")

# D3 map + pins + comparison table
s = d.slide("Dense Pages", "Geography page: labelled map beside a comparison table")
mw_, mh = 5.2, BOTTOM - TOP - 0.4
d.header(s, x0, TOP, mw_, "photo(map) + pin(): native labels on a map")
my = TOP + 0.4
d.photo(s, os.path.join(IMG, "map-sg-strait-navy.png"), x0, my, mw_, mh)
jx, jy = x0 + 0.13 * mw_, my + 0.06 * mh
sx, sy = x0 + 0.33 * mw_, my + 0.20 * mh
btx, bty = x0 + 0.47 * mw_, my + 0.40 * mh
d.pin(s, jx, jy, ["**Johor (Malaysia)**", f"{mk['Johor'][0]}MW live · 2,500MW+ upcoming"],
      (x0 + 2.2, my + 0.08, 2.85, 0.48))
d.pin(s, sx, sy, ["**Singapore**", f"{sg_live}MW live · {sg_up}MW upcoming"], (x0 + 2.75, my + 1.18, 2.35, 0.48),
      hot=True)
d.pin(s, btx, bty, ["**Batam (Indonesia)**", "NDP1: up to 144MW"], (x0 + 0.1, my + 2.55, 2.9, 0.48))
tx = x0 + mw_ + GUTTER
tw = W - R_ - tx
d.header(s, tx, TOP, tw, "table(): the places compared on one grid")
d.table(s, tx, TOP + 0.4, tw, [["Metric", "Singapore", "Johor", "Batam"],
                               ["Live capacity, Q1 2026 (MW)", f"{sg_live}", f"{mk['Johor'][0]}", "n.a."],
                               ["Upcoming capacity (MW)", f"{sg_up}", "2,500+", "144 (NDP1)"],
                               ["Live capacity growth, 2025", "6–8%", "53%", "n.a."],
                               ["Indicative cap rate, Q1 2026", "5.25–6.50%", "6.50–8.00%", "n.a."],
                               ["Main role", "Interconnection", "Hyperscale and AI", "Overflow"]],
        col_widths=[2.25, 1.65, 1.45, tw - 5.35], row_h=0.3)
y2 = TOP + 2.45
d.header(s, tx, y2, tw, "Commentary: what moves where")
d.bullets(s, tx, y2 + 0.4, tw, BOTTOM - y2 - 0.4, [
    "**Johor is the pressure valve:** live capacity grew 53% in 2025, the fastest in APAC",
    "**Built to order:** most Johor capacity is pre-let, so oversupply risk is low",
    "**Batam connects directly:** NDP1 links to Changi via the Nongsa–Changi cable",
    "**Map rules:** recolour to the navy ramp; gold pin for the subject; one-line labels with numbers",
    "**Maps come from** Wikimedia via fetch_image.py; crop so the places fill the frame"])
d.footer(s, sources=DSRC + "; BW Digital (2026)", notes="Recipe: map + comparison table")

# D4 logo wall
s = d.slide("Dense Pages", "Landscape page: logo wall by segment beside a chart (Qatalyst p8)")
logos = {n: os.path.join(IMG, f) for n, f in [
    ("Google", "logo-google.png"), ("Microsoft", "logo-microsoft.png"), ("AWS", "logo-aws.png"),
    ("Meta", "logo-meta.png"), ("ByteDance", "logo-bytedance.png"), ("Equinix", "logo-equinix.png"),
    ("Digital Realty", "logo-digital-realty.png"), ("ST Telemedia GDC", "logo-st-telemedia.png"),
    ("Keppel", "logo-keppel.png"), ("Singtel (Nxera)", "logo-singtel.png"), ("NTT", "logo-ntt.png"),
    ("CapitaLand", "logo-capitaland.png"), ("KKR", "logo-kkr.png"), ("Blackstone", "logo-blackstone.png")]}
lw, c1, c2 = 7.3, 2.0, 3.1
c3 = lw - c1 - c2 - 0.3
ly = TOP + 0.85
for cx_, cw_, head, role in ((x0, c1, "Segment 1", "Hyperscalers and cloud"),
                             (x0 + c1 + 0.15, c2, "Segment 2 (two columns)", "Colocation operators"),
                             (x0 + c1 + c2 + 0.3, c3, "Segment 3", "Owners and capital")):
    d.header(s, cx_, TOP, cw_, head)
    d.exhibit_takeaway(s, cx_, TOP + 0.33, cw_, role, h=0.5)
d.logo_row(s, x0, ly, c1, BOTTOM - ly, ["Google", "Microsoft", "AWS", "Meta", "ByteDance"], cols=1, logos=logos,
           outline=False, pad=0.08)
d.logo_row(s, x0 + c1 + 0.15, ly, c2, BOTTOM - ly, ["Equinix", "Digital Realty", "ST Telemedia GDC", "AirTrunk",
                                                     "Keppel", "Singtel (Nxera)", "NTT", "Global Switch", "GDS",
                                                     "Princeton Digital"], cols=2, logos=logos, outline=False, pad=0.08)
d.logo_row(s, x0 + c1 + c2 + 0.3, ly, c3, BOTTOM - ly, ["Keppel DC REIT", "Digital Core REIT", "CapitaLand", "KKR",
                                                         "Blackstone"], cols=1, logos=logos, outline=False, pad=0.08)
rx = x0 + lw + GUTTER
rw = W - R_ - rx
fac = DATA["facilities"]
d.header(s, rx, TOP, rw, "Scale exhibit beside the wall (MW)")
d.exhibit_takeaway(s, rx, TOP + 0.33, rw, "Flagship builds run from 20MW to ~80MW")
d.bar(s, rx, TOP + 0.72, rw, 2.2, [f for f, _ in fac], [("MW", [v for _, v in fac])], gap=40)
d.bullets(s, rx, TOP + 2.98, rw, BOTTOM - TOP - 2.98, [
    "**logo_row(logos=…, outline=False):** loose logos, no boxes, as real decks do",
    "**No logo on Wikimedia?** the name shows in bold 12pt instead",
    "**A one-line role** under each segment header tells the reader why the group matters",
    "**Logos are names:** the SPARSE lint counts each logo as one word, like a name in a table"])
d.footer(s, sources="TechDirectory (Jul 2026); CBRE (Apr 2026). Logos: Wikimedia Commons", notes="Recipe: logo wall")

# D5 full-width table + chart + takeaways (Evercore Diversey p8)
s = d.slide("Dense Pages", "Deal page: full-width table, chart and takeaways (Evercore p8)")
d.header(s, x0, TOP, bw, "table(): full width, units once in the header bar (US$m unless stated)")
rows = [["Date", "Target", "Market", "Buyer", "Price", "Capacity (MW)", "Price per MW", "Type"]]
for dt, tg, mkt, by, px, mwv, ty in DATA["deals"]:
    pm = px / mwv if (ty == "Asset" and mwv) else None
    rows.append([dt, tg, mkt, by, f"{px:,.0f}", (f"{mwv:,.1f}" if mwv < 100 else f"{mwv:,.0f}") if mwv else "n.d.",
                 f"{pm:.1f}" if pm else ("n.m." if ty == "Platform" else "n.d."), ty])
d.table(s, x0, TOP + 0.4, bw, rows, col_widths=[0.85, 2.6, 1.1, 3.0, 1.1, 1.2, 1.2, bw - 11.05], num_cols=(4, 5, 6),
        row_h=0.26)
y2 = TOP + 0.4 + 0.26 * len(rows) + 0.25
assets = sorted([(t, p / m) for _, t, _, _, p, m, ty in DATA["deals"] if ty == "Asset" and m], key=lambda z: -z[1])
d.header(s, x0, y2, 6.1, "bar(): the ratio the table implies (US$m per MW)")
d.bar(s, x0, y2 + 0.35, 6.1, BOTTOM - y2 - 0.35, [a for a, _ in assets], [("US$m/MW", [v for _, v in assets])],
      number_format="0.0", gap=40)
rx = x0 + 6.1 + GUTTER
d.header(s, rx, y2, W - R_ - rx, "Takeaways")
d.bullets(s, rx, y2 + 0.4, W - R_ - rx, BOTTOM - y2 - 0.4, [
    "**Platforms attract the largest cheques:** KKR / Singtel paid S$6.6bn for 82% of STT GDC",
    "**Asset deals cleared at US$15–37m per MW** across APAC",
    "**Rule:** n.m. / n.d. explained in Notes, never left blank",
    "**Rule:** numbers right-aligned, one decimal where precision matters"])
d.footer(s, sources=f"{CBRE} (MSCI RCA); STT GDC and Keppel press releases",
         notes="Recipe: full-width table + chart + takeaways; platform per-MW n.m. (includes pipeline)")

# D6 text page: framing box, then two-level bullets in two full-height columns (GS PowerSchool p3, Centerview Endeavor p4)
s = d.slide("Dense Pages", "Text page: framing box, then two-level bullets (GS p3)")
d.takeaway(s, x0, TOP, bw, 0.5, "**Framing box:** one sentence on why this page exists, e.g. the recommendation to "
                                "the board. takeaway() draws it dashed, never an accent-bar card.")
half = (bw - GUTTER) / 2
yb = TOP + 0.7
d.header(s, x0, yb, half, "Situation: why a sale makes sense now")
d.bullets(s, x0, yb + 0.4, half, BOTTOM - yb - 1.35, [
    "**Market backdrop supports a sale:** Australian fitness is growing and Tough Love trades from strength",
    ("150 studios across all 7 states and territories make it #3 by outlets, behind Unity Gym (253)", 1),
    ("Year 0 revenue of $75.0m and EBITDA of $16.4m give a 21.9% margin", 1),
    ("Revenue grows at a 4.8% CAGR to $94.8m by Year 5; EBITDA reaches $19.0m (20.0% margin)", 1),
    ("A 94% gross margin absorbs the Year 1 cost reset without closing studios", 1),
    "**The asking price is reasonable against the cash flows**",
    ("$80.0m asks 4.9x Year 0 EBITDA; the model returns an 18.5% equity IRR and 2.1x over 5 years", 1),
    ("Peak leverage of 0.9x keeps covenants comfortable, even through the Year 1 dip to $12.8m EBITDA", 1),
    ("Exit at 5.0x Year 5 EBITDA of $19.0m implies ~$95m enterprise value before net debt", 1),
], gap=6)
rx = x0 + half + GUTTER
d.header(s, rx, yb, half, "Recommendation: bid, with conditions and a tight process")
d.bullets(s, rx, yb + 0.4, half, BOTTOM - yb - 1.35, [
    "**Proceed to a bid, with three conditions**",
    ("Diligence the opex step-up from 72% to 77% of revenue before signing", 1),
    ("Secure a 12-month founder transition and a management rollover of at least 10% (illustrative)", 1),
    ("Review the top 20 leases, the largest fixed cost, for expiry clustering and above-CPI rent reviews", 1),
    "**Run a targeted auction over eight weeks to keep tension without a public sale**",
    ("Week 1: approach 4 strategic buyers (incl. Unity Gym) and 6 fitness-focused sponsors (illustrative)", 1),
    ("Week 4: non-binding bids with a 2-page financing letter; data room opens to 3 shortlisted parties", 1),
    ("Week 8: binding bids and SPA mark-ups; target signing within 10 weeks of launch", 1),
    "**Rule for text pages:** 200+ words, a number in every sub-point, columns running to the bottom",
], gap=6)
d.stat_strip(s, x0, BOTTOM - 0.8, bw, 0.8, [("$80.0m", "Asking price"), ("4.9x", "Year 0 EBITDA multiple"),
                                         ("18.5%", "Equity IRR, 5 years"), ("2.1x", "Money multiple"),
                                         ("0.9x", "Peak leverage")], align=PP_ALIGN.CENTER)
d.footer(s, sources="Keppel case pack; deal-desk model", notes=NOTE + "; recipe: text page (~250 words, no exhibit needed)")

d.save(out)
print(out)
