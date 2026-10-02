"""Singapore Data Centres – Sector Overview (10 content slides). Worked example of the density standard (lessons #32):
every slide pairs 1–3 exhibits with commentary that carries numbers, fills the body, and cites its sources.

    python sg_dc_slides.py            -> Claude Things/output/Singapore Data Centres/Singapore Data Centres Sector Overview.pptx

All figures live in DATA below with their source; the slides only read from it.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
from ibdeck import Deck, L, W, R_, TOP, BOTTOM, GUTTER, NAVY, STEEL, LIGHT  # noqa: E402
from pptx.enum.shapes import MSO_SHAPE  # noqa: E402
from pptx.enum.text import PP_ALIGN  # noqa: E402

IMG = os.path.join(HERE, "..", "images")
sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
import paths  # noqa: E402
OUT = str(paths.WORKSPACE / "output" / "Singapore Data Centres" / "Singapore Data Centres Sector Overview.pptx")

# ---------------------------------------------------------------- data (every number, with its source)
CBRE = "CBRE, 2026 APAC Data Centre Trends & Outlook (Apr 2026 data)"
DATA = {
    # CBRE market key stats, Q1 2026: (live MW, upcoming MW = under construction + committed/announced)
    "markets": {"Shanghai": (1286, 737), "Tokyo": (1086, 2544), "Sydney": (950, 1531), "Seoul": (869, 1412),
                "Singapore": (821, 247.5), "Mumbai": (800, 750), "Hong Kong": (687, 653), "Johor": (476, 2500)},
    # CBRE indicative hyperscale cap rates, Q1 2026 (%, shell & core low end, fitted high end)
    "cap_rates": [("Tokyo", 3.35, 4.35), ("Hong Kong", 5.00, 6.00), ("Sydney", 5.00, 6.25), ("Seoul", 5.25, 6.00),
                  ("Melbourne", 5.25, 6.50), ("Singapore", 5.25, 6.50), ("Shanghai", 6.00, 7.50),
                  ("Johor", 6.50, 8.00)],
    # colocation asking rents, US$/kW/month (CBRE via The Real Deal, Jun 2026; SG range from TechDirectory 2026)
    "rents": [("Singapore", 403), ("Hong Kong", 295), ("Tokyo", 280), ("Sydney", 188)],
    "sg_rent_range": "US$330–475",
    # Big Tech 2026 AI spend plans, US$bn (CBRE citing company guidance)
    "capex": [("Amazon", 200), ("Google", 180), ("ByteDance", 23)],
    # flagship Singapore facilities, MW IT load (TechDirectory operator table, Jul 2026; CBRE for Keppel floating DC)
    "facilities": [("AirTrunk SGP1", 78), ("Nxera DC Tuas", 58), ("Digital Realty SIN12", 50),
                   ("STT GDC Defu", 40), ("Keppel floating DC (u/c)", 25), ("Equinix SG6 (u/c)", 20)],
    # APAC transactions (CBRE Figures 11–12 from MSCI RCA; STT GDC and Keppel press releases)
    # (date, target, market, buyer, price US$m, MW, type)
    "deals": [("Mar 2026", "Colt DCS Keihanna", "Japan", "CapitaLand Ascendas REIT / Mitsui fund", 997, 45.9, "Asset"),
              ("Feb 2026", "ST Telemedia GDC (82% stake)", "12 markets", "KKR / Singtel", 5100, 2300, "Platform"),
              ("Nov 2025", "Colt DCS Inzai 4", "Japan", "Keppel DC REIT / Keppel", 533, 19.8, "Asset"),
              ("Jul 2025", "Yondr Group", "8 markets", "DigitalBridge / La Caisse", 5800, 1000, "Platform"),
              ("Jun 2025", "TIM portfolio (3 DCs)", "Philippines", "Equinix", 180, 12.2, "Asset"),
              ("Mar 2025", "Gotemba", "Japan", "Mitsui & Co", 664, 18.0, "Asset"),
              ("Dec 2024", "Global Switch Sydney West & East", "Australia", "DigiCo Infrastructure REIT", 1260.5, 43.6,
               "Asset"),
              ("Nov 2024", "Keppel DC Singapore 7 & 8", "Singapore", "Keppel DC REIT", 1380 / 1.34, None, "Asset")],
    # Keppel DC REIT, 1H 2026 results presentation (as at 30 Jun 2026): AUM and Singapore share p19; leverage p9;
    # occupancy (95.3% ex-Cardiff), WALE by area / by rent, reversion p12; rent expiring by 2030 p13; tenants p14.
    # rev_prev = 1H 2025 reversion (Aug 2025 investor presentation)
    "kdcr": {"aum": "S$6.3bn", "sg_share": "62.8%", "hyperscale": "70.4%", "top_client": "45%", "occupancy": "92.5%",
             "reversion": "~10%", "rev_prev": "~51%", "wale": "6.7 yrs", "wale_rent": "4.5 yrs", "exp_2030": "~42%",
             "leverage": "34.0%"},
}


def per_mw(price, mw):
    return price / mw if mw else None


def build():
    d = Deck(sections=["Market Overview", "Demand & Supply", "Competitive Landscape", "Deal Activity",
                       "Investment View"])
    d.title_slide("Singapore Data Centres", "Sector overview: market, supply, competition, deals and investment view",
                  date="September 2026", name="Benedict Toh")
    x0, bw = L, W - L - R_
    mk = DATA["markets"]
    sg_live, sg_up = mk["Singapore"]

    # ------------------------------------------------------------ 1. Market at a glance
    s = d.slide("Market Overview", "Asia's premium data centre hub, running at over 95% occupancy")
    lw = 3.85
    d.header(s, x0, TOP, lw, "Singapore at a glance")
    d.photo(s, os.path.join(IMG, "photo-dc-racks.jpg"), x0, TOP + 0.4, lw, 1.75)
    d.bullets(s, x0, TOP + 2.25, lw, BOTTOM - TOP - 2.25, [
        f"**Anchor hub:** {sg_live}MW live, on a par with Seoul and Mumbai, on a 744km² island",
        f"**Near-full:** occupancy above 95%; CBRE calls it a landlord's market",
        f"**Premium pricing:** colocation asks {DATA['sg_rent_range']} per kW a month, the highest in APAC",
        f"**Controlled growth:** only {sg_up}MW upcoming, released by government tender",
        "**Power-intensive:** data centres use ~7% of national electricity; new builds must run ≥50% green",
    ])
    rx = x0 + lw + GUTTER
    rw = W - R_ - rx
    d.header(s, rx, TOP, rw, "Key market metrics")
    d.stat_icons(s, rx, TOP + 0.42, rw, 1.3, [
        ("server", f"{sg_live}MW", "Live capacity, Q1 2026"),
        ("trending-up", f"{sg_up}MW", "Under construction or announced"),
        ("percentage", ">95%", "Occupancy"),
        ("cash", DATA["sg_rent_range"], "Rent per kW per month"),
        ("bolt", "~7%", "Share of national electricity"),
    ], icon_size=0.42)
    y2 = TOP + 1.95
    cw = 4.75
    d.header(s, rx, y2, cw, "Live capacity by market, Q1 2026 (MW)")
    d.exhibit_takeaway(s, rx, y2 + 0.33, cw, "Singapore matches Seoul and Mumbai on a fraction of the land")
    order = sorted(mk, key=lambda m: -mk[m][0])
    d.bar(s, rx, y2 + 0.72, cw, BOTTOM - y2 - 0.72, order, [("Live MW", [mk[m][0] for m in order])],
          highlight=order.index("Singapore"), gap=35)
    bx = rx + cw + GUTTER
    d.header(s, bx, y2, W - R_ - bx, "What sets Singapore apart")
    d.bullets(s, bx, y2 + 0.4, W - R_ - bx, BOTTOM - y2 - 0.4, [
        "**Connectivity:** 28 subsea cables land here, with at least 13 more planned",
        "**Hyperscaler base:** AWS plans a further S$12bn to 2028; Digital Realty targets ~S$7bn in total",
        "**Capital depth:** listed DC REITs plus platform buyers such as KKR / Singtel",
        "**High barriers to entry:** US$14.5/W to build, second only to Tokyo",
    ])
    d.footer(s, sources=f"{CBRE}; TechDirectory, Data Centres in Singapore (Jul 2026); CSIS, Subsea Cables: Singapore "
                        "(Sep 2025); Turner & Townsend, DC Cost Index 2025; SingStat (land area, end-2025)",
             notes="Live = operational IT capacity; upcoming = under construction and announced; rents are asking "
                   "rents for colocation")

    # ------------------------------------------------------------ 2. Demand vs supply
    s = d.slide("Demand & Supply", "Cloud and AI demand far outruns what Singapore can add")
    half = (bw - 1.0) / 2
    d.header(s, x0, TOP, half, "Demand: accelerating")
    d.bullets(s, x0, TOP + 0.38, half, 0.95, [
        "**Big Tech capex +61% in 2026:** AI training and inference need large, power-dense halls",
        "**Global hyperscale demand growing 14% a year**, with neoclouds adding a new tenant type",
    ])
    ax = x0 + half + 0.15
    d._shape(s, MSO_SHAPE.RIGHT_ARROW,
                   ax, TOP + 0.35, 0.7, 0.6, fill=STEEL)
    ox = x0 + half + 1.0
    d.header(s, ox, TOP, half, "Supply: capped")
    d.bullets(s, ox, TOP + 0.38, half, 0.95, [
        f"**Pipeline is thin:** {sg_up}MW upcoming vs {sg_live}MW live, the lowest of the eight markets shown",
        "**Capacity only by tender:** 80MW in 2023, 200MW in Aug 2026; next call reviewed in 18–24 months",
    ])
    y2 = TOP + 1.45
    ew = (bw - 2 * GUTTER) / 3
    # exhibit 1: capex
    d.header(s, x0, y2, ew, "Big Tech AI spend plans, 2026 (US$bn)")
    d.exhibit_takeaway(s, x0, y2 + 0.33, ew, "Two US hyperscalers alone plan US$380bn of AI spend in 2026")
    d.column(s, x0, y2 + 0.75, ew, 2.05, [c for c, _ in DATA["capex"]], [("US$bn", [v for _, v in DATA["capex"]])],
             gap=80)
    d.stat_strip(s, x0, y2 + 2.9, ew, BOTTOM - y2 - 2.9, [
        ("+61%", "Big Tech capex growth, 2026"), ("US$11.6bn", "APAC DC investment, 2025")], align=PP_ALIGN.CENTER)
    # exhibit 2: live vs upcoming
    e2 = x0 + ew + GUTTER
    order = sorted(mk, key=lambda m: -(mk[m][1] / mk[m][0]))
    d.header(s, e2, y2, ew, "Live vs upcoming capacity, Q1 2026 (MW)")
    d.exhibit_takeaway(s, e2, y2 + 0.33, ew, f"Singapore's pipeline is {sg_up / sg_live:.0%} of live stock, "
                                             "the lowest of the eight markets")
    d.bar(s, e2, y2 + 0.75, ew, BOTTOM - y2 - 0.75, order,
          [("Live", [mk[m][0] for m in order]), ("Upcoming", [mk[m][1] for m in order])], colors=[NAVY, LIGHT],
          gap=40)
    # exhibit 3: commitments table
    e3 = e2 + ew + GUTTER
    d.header(s, e3, y2, ew, "Recent commitments to Singapore")
    d.exhibit_takeaway(s, e3, y2 + 0.33, ew, "Operators keep committing capital despite the cap")
    d.table(s, e3, y2 + 0.78, ew, [
        ["Who", "Commitment", "Timing"],
        ["AWS", "S$12bn more (S$23bn+ in total)", "To 2028"],
        ["Digital Realty", "S$4.3bn+ for new builds (~S$7bn total)", "Apr 2026"],
        ["DC-CFA2", "200MW: Digital Realty, Equinix, Keppel, STT GDC", "Aug 2026"],
        ["Equinix", "SG6: US$260m+, 20MW", "Opens Q1 2027"],
        ["Keppel", "25MW floating DC, pre-let to a hyperscaler", "Live 2028"],
        ["DC-CFA1", "80MW: Equinix, Microsoft, GDS, AirTrunk–ByteDance", "Jul 2023"],
    ], col_widths=[0.95, ew - 1.8, 0.85], num_cols=(), row_h=0.38)
    d.footer(s, sources=f"{CBRE} (capex from company guidance, via Bloomberg); TechDirectory (Jul 2026); Equinix "
                        "(19 Nov 2024) and Digital Realty (9 Apr 2026) press releases; IMDA (Jul 2023); EDB / IMDA (21 Aug 2026)",
             notes="Upcoming = under construction and announced capacity; bars sorted by upcoming ÷ live")

    # ------------------------------------------------------------ 3. Policy and power
    s = d.slide("Demand & Supply", "Power and land, not demand, cap new supply")
    d.header(s, x0, TOP, bw, "From moratorium to controlled allocation")
    d.timeline(s, x0, TOP + 0.35, bw, 2.2, [
        ("2019", "Moratorium", "New builds paused over power and land use"),
        ("Jul 2022", "Pilot DC-CFA", "Pause lifted, with strict efficiency rules"),
        ("Jul 2023", "80MW awarded", "Equinix, Microsoft, GDS, AirTrunk–ByteDance"),
        ("May 2024", "Green DC Roadmap", "≥300MW near term, more via green energy"),
        ("Oct 2025", "Jurong Island park", "20ha low-carbon park, ~700MW potential"),
        ("Dec 2025", "DC-CFA2 launched", "≥200MW call; 20 proposals received"),
        ("Aug 2026", "DC-CFA2 awarded", "50MW each: Digital Realty, Equinix, Keppel, STT GDC"),
    ], highlight=6)
    y2 = TOP + 2.7
    tw = 6.1
    d.header(s, x0, y2, tw, "Entry bar for new capacity (DC-CFA2)")
    d.table(s, x0, y2 + 0.4, tw, [
        ["Test", "Requirement"],
        ["Green energy", "≥50% from eligible green pathways (biomethane, low-carbon ammonia, hydrogen, solar)"],
        ["Efficiency", "PUE of 1.25 or better at 100% IT load"],
        ["Building", "BCA-IMDA Green Mark for Data Centres 2024, Platinum"],
        ["IT equipment", "Singapore Standard SS 715:2025 on IT energy efficiency"],
        ["Size", "≥200MW in total; more for innovative green-energy projects"],
    ], col_widths=[1.2, tw - 1.2], num_cols=(), row_h=0.35)
    cx = x0 + tw + GUTTER
    cwid = W - R_ - cx
    d.header(s, cx, y2, cwid, "Capacity released by policy vs live stock (MW)")
    chart_w = 3.2
    d.bar(s, cx, y2 + 0.35, chart_w, BOTTOM - y2 - 0.35,
          ["Live stock, Q1 2026", "Jurong Island (potential)", "DC-CFA2 (Aug 2026)", "DC-CFA1 (2023)"],
          [("MW", [sg_live, 700, 200, 80])], highlight=0, gap=45)
    d.bullets(s, cx + chart_w + 0.1, y2 + 0.4, cwid - chart_w - 0.1, BOTTOM - y2 - 0.4, [
        "**Power:** data centres use ~7% of electricity; EMA is upgrading the grid for new load",
        "**Land:** new sites are steered to Jurong Island; building elsewhere is hard",
        "**Time:** each tranche takes years to deliver, so tight supply persists",
    ])
    d.footer(s, sources="EDB / IMDA, DC-CFA2 call (1 Dec 2025) and results (21 Aug 2026); Morgan Lewis (Mar 2026); Reed Smith "
                        f"(2025); IMDA Green DC Roadmap (May 2024); EMA (27 Oct 2025); TechDirectory (Jul 2026); {CBRE}",
             notes="DC-CFA = Data Centre Call for Application; PUE = power usage effectiveness (total facility power ÷ "
                   "IT power); Jurong Island ~700MW is long-term potential, not an allocation")

    # ------------------------------------------------------------ 4. Corridor
    s = d.slide("Demand & Supply", "Overflow demand is moving to Johor and Batam")
    mw_, mh = 5.2, BOTTOM - TOP - 0.4
    d.header(s, x0, TOP, mw_, "The Singapore–Johor–Batam corridor")
    my = TOP + 0.4
    d.photo(s, os.path.join(IMG, "map-sg-strait-navy.png"), x0, my, mw_, mh)
    P = lambda fx, fy: (x0 + fx * mw_, my + fy * mh)  # noqa: E731
    jx, jy = P(0.13, 0.06)
    sx, sy = P(0.33, 0.20)
    btx, bty = P(0.47, 0.40)
    d.pin(s, jx, jy, [f"**Johor (Malaysia)**", f"{mk['Johor'][0]}MW live · 2,500MW+ upcoming"],
          (x0 + 2.2, my + 0.08, 2.85, 0.48))
    d.pin(s, sx, sy, [f"**Singapore**", f"{sg_live}MW live · {sg_up}MW upcoming"],
          (x0 + 2.75, my + 1.18, 2.35, 0.48), hot=True)
    d.pin(s, btx, bty, ["**Batam (Indonesia), ~20km south**", "NDP1: 24MW phase 1 · up to 144MW"],
          (x0 + 0.1, my + 2.55, 2.9, 0.48))
    tx = x0 + mw_ + GUTTER
    tw = W - R_ - tx
    d.header(s, tx, TOP, tw, "Singapore vs its overflow markets")
    d.table(s, tx, TOP + 0.4, tw, [
        ["Metric", "Singapore", "Johor", "Batam"],
        ["Live capacity, Q1 2026 (MW)", f"{sg_live}", f"{mk['Johor'][0]}", "n.a."],
        ["Upcoming capacity (MW)", f"{sg_up}", "2,500+", "144 (NDP1 full)"],
        ["Live capacity growth, 2025", "6–8%", "53%", "n.a."],
        ["Indicative cap rate, Q1 2026", "5.25–6.50%", "6.50–8.00%", "n.a."],
        ["Main role", "Interconnection, premium colo", "Hyperscale and AI", "Emerging overflow"],
    ], col_widths=[2.25, 1.65, 1.45, tw - 5.35], row_h=0.3)
    y2 = TOP + 2.45
    d.header(s, tx, y2, tw, "Where the next wave of capacity goes")
    d.bullets(s, tx, y2 + 0.4, tw, BOTTOM - y2 - 0.4, [
        "**Johor is the pressure valve:** live capacity grew 53% in 2025, the fastest in APAC",
        "**Built to order:** most Johor capacity is pre-let to hyperscale, large-tech and AI users, so CBRE sees "
        "little oversupply risk",
        "**Platforms trading:** AirTrunk is marketing a majority stake in JHB1 (150MW) for ~US$1.5bn; Vantage, GIC "
        "and ADIA bought Yondr Malaysia (300MW)",
        "**Batam connects directly:** BW Digital's NDP1 links to Changi via the new Nongsa–Changi cable",
        "**Johor tightening too:** rising build costs and scarcer power push users to look further afield",
    ])
    d.footer(s, sources=f"{CBRE}; The Real Deal citing CBRE (Jun 2026); DCD and BW Digital on NDP1 (2025–26)",
             notes="Batam market-wide capacity is not published on a comparable basis; NDP1 = Nongsa Digital Park 1")

    # ------------------------------------------------------------ 5. Competitive landscape
    s = d.slide("Competitive Landscape", "A concentrated field of global operators and hyperscalers")
    logos = {n: os.path.join(IMG, f) for n, f in [
        ("Google", "logo-google.png"), ("Microsoft", "logo-microsoft.png"), ("AWS", "logo-aws.png"),
        ("Meta", "logo-meta.png"), ("ByteDance", "logo-bytedance.png"), ("Equinix", "logo-equinix.png"),
        ("Digital Realty", "logo-digital-realty.png"), ("ST Telemedia GDC", "logo-st-telemedia.png"),
        ("Keppel", "logo-keppel.png"), ("Singtel (Nxera)", "logo-singtel.png"), ("NTT", "logo-ntt.png"),
        ("CapitaLand", "logo-capitaland.png"), ("KKR", "logo-kkr.png"), ("Blackstone", "logo-blackstone.png")]}
    lw = 7.3
    c1, c2 = 2.0, 3.1
    c3 = lw - c1 - c2 - 2 * 0.15
    ly = TOP + 0.85
    lh = BOTTOM - ly
    for cx_, cw_, role in ((x0, c1, "Run their own cloud and AI regions"),
                           (x0 + c1 + 0.15, c2, "Lease halls to hyperscalers, enterprises and network providers"),
                           (x0 + c1 + c2 + 0.3, c3, "REITs and funds that own the platforms")):
        d.exhibit_takeaway(s, cx_, TOP + 0.33, cw_, role, h=0.5)
    d.header(s, x0, TOP, c1, "Hyperscalers and cloud")
    d.logo_row(s, x0, ly, c1, lh, ["Google", "Microsoft", "AWS", "Meta", "ByteDance"], cols=1, logos=logos,
               outline=False, pad=0.08)
    x2 = x0 + c1 + 0.15
    d.header(s, x2, TOP, c2, "Colocation operators")
    d.logo_row(s, x2, ly, c2, lh, ["Equinix", "Digital Realty", "ST Telemedia GDC", "AirTrunk", "Keppel",
                                   "Singtel (Nxera)", "NTT", "Global Switch", "GDS", "Princeton Digital"],
               cols=2, logos=logos, outline=False, pad=0.08)
    x3 = x2 + c2 + 0.15
    d.header(s, x3, TOP, c3, "Owners and capital")
    d.logo_row(s, x3, ly, c3, lh, ["Keppel DC REIT", "Digital Core REIT", "CapitaLand", "KKR", "Blackstone"],
               cols=1, logos=logos, outline=False, pad=0.08)
    rx = x0 + lw + GUTTER
    rw = W - R_ - rx
    d.header(s, rx, TOP, rw, "Selected flagship facilities (MW IT load)")
    d.exhibit_takeaway(s, rx, TOP + 0.33, rw, "New flagship builds run from 20MW to ~80MW each")
    fac = DATA["facilities"]
    d.bar(s, rx, TOP + 0.72, rw, 2.2, [f for f, _ in fac], [("MW", [v for _, v in fac])], gap=40)
    d.bullets(s, rx, TOP + 2.98, rw, BOTTOM - TOP - 2.98, [
        "**Landlord's market:** >95% occupancy lets operators pick creditworthy, efficient tenants",
        "**Legacy sites stay competitive:** legacy halls compete on embedded connectivity, but many need AI retrofits",
        "**Scale needs allocation:** the Aug 2026 tender gave Digital Realty, Equinix, Keppel and STT GDC 50MW each",
        "**Global capital behind them:** KKR, Singtel, Blackstone and Keppel back the largest platforms",
    ])
    d.footer(s, sources=f"TechDirectory, operator comparison (Jul 2026); {CBRE}; EDB / IMDA (21 Aug 2026); company websites. "
                        "Logos: Wikimedia Commons",
             notes="Not exhaustive; AirTrunk is owned by Blackstone, STT GDC by KKR / Singtel (on completion); u/c = "
                   "under construction")

    # ------------------------------------------------------------ 6. Pricing
    s = d.slide("Competitive Landscape", "Scarcity gives Singapore the highest rents in the region")
    ew = (bw - 2 * GUTTER) / 3
    d.header(s, x0, TOP, ew, "Colocation asking rents (US$ per kW per month)")
    r = DATA["rents"]
    sg_r = dict(r)["Singapore"]
    d.exhibit_takeaway(s, x0, TOP + 0.33, ew, f"Singapore runs {sg_r / dict(r)['Tokyo'] - 1:.0%} above Tokyo and "
                                              f"{sg_r / dict(r)['Sydney']:.1f}x Sydney")
    d.column(s, x0, TOP + 0.75, ew, BOTTOM - TOP - 0.75, [m for m, _ in r], [("US$/kW/month", [v for _, v in r])],
             highlight=0, gap=60)
    e2 = x0 + ew + GUTTER
    d.header(s, e2, TOP, ew, "Cost to build and run in Singapore")
    d.table(s, e2, TOP + 0.4, ew, [
        ["Item", "Singapore", "Context"],
        ["Build cost (US$/W, 2025)", "14.5", "2nd globally; Tokyo 15.2"],
        ["Industrial power (US$/kWh)", "0.21–0.24", "Early 2025"],
        ["Green energy required", "≥50%", "DC-CFA2 entry test"],
        ["Design PUE required", "≤1.25", "At 100% IT load"],
    ], col_widths=[1.75, 0.85, ew - 2.6], num_cols=(1,), row_h=0.36)
    d.header(s, e2, TOP + 2.4, ew, "Keppel DC REIT: pricing power in action")
    k = DATA["kdcr"]
    d.stat_strip(s, e2, TOP + 2.85, ew, 0.85, [(k["reversion"], "Rent reversion, 1H 2026"),
                                               (k["occupancy"], "Occupancy"),
                                               (k["wale"], "WALE by area")],
                 align=PP_ALIGN.CENTER)
    d.bullets(s, e2, TOP + 3.85, ew, BOTTOM - TOP - 3.85, [
        f"**Positive every period:** renewals re-let {k['rev_prev']} higher in 1H 2025, {k['reversion']} in 1H 2026",
        f"**Internet firms, mainly hyperscalers,** pay {k['hyperscale']} of the REIT's rent",
    ])
    e3 = e2 + ew + GUTTER
    d.header(s, e3, TOP, ew, "What it means for owners")
    d.bullets(s, e3, TOP + 0.4, ew, BOTTOM - TOP - 0.4, [
        "**Rents holding up:** CBRE expects stable to slightly higher rents through 2026, with occupancy above 95%",
        "**Tenants compete for space:** creditworthy, efficient customers get priority",
        "**High replacement cost:** US$14.5/W build cost plus scarce land and power keep new supply out",
        "**AI retrofit upside:** many legacy halls cannot host AI densities, creating upgrade projects",
        "**Arbitrage:** latency-sensitive, interconnected workloads stay; bulk compute moves to Johor or Batam",
    ])
    d.takeaway(s, e3, BOTTOM - 1.3, ew, 1.3,
               "**So what:** Singapore should stay APAC's most expensive market. Supply is capped by policy, and "
               f"Keppel DC REIT ({float(k['sg_share'].rstrip('%')):.0f}% Singapore by AUM) keeps re-letting renewals "
               f"higher ({k['rev_prev']} in 1H 2025, {k['reversion']} in 1H 2026).")
    d.footer(s, sources="The Real Deal citing CBRE (Jun 2026); TechDirectory (Jul 2026); Turner & Townsend, DC Cost "
                        "Index 2025; IMDA DC-CFA2; Keppel DC REIT, 1H 2026 results (22 Jul 2026); Keppel DC REIT, Aug 2025 investor presentation",
             notes="Rents are average asking rents; Singapore range US$330–475. Reversion = new rent ÷ expiring rent on "
                   "contracts renewed in the period; Keppel occupancy 95.3% excluding Cardiff. WALE = weighted average lease expiry")

    # ------------------------------------------------------------ 7. Transactions
    s = d.slide("Deal Activity", "Capital keeps paying up for scarce APAC platforms and assets")
    d.header(s, x0, TOP, bw, "Selected APAC data centre transactions, 2024–26 (US$m unless stated)")
    rows = [["Date", "Target", "Market", "Buyer", "Price", "Capacity (MW)", "Price per MW", "Type"]]
    for dt, tg, mkt, by, px, mwv, ty in DATA["deals"]:
        pm = per_mw(px, mwv) if ty == "Asset" else None
        rows.append([dt, tg, mkt, by, f"{px:,.0f}", f"{mwv:,.1f}" if mwv and mwv < 100 else
                     (f"{mwv:,.0f}" if mwv else "n.d."), f"{pm:.1f}" if pm else ("n.m." if ty == "Platform" else "n.d."),
                     ty])
    d.table(s, x0, TOP + 0.4, bw, rows, col_widths=[0.85, 2.6, 1.1, 3.0, 1.1, 1.2, 1.2, bw - 11.05],
            num_cols=(4, 5, 6), row_h=0.26)
    y2 = TOP + 0.4 + 0.26 * len(rows) + 0.25
    lw = 6.1
    assets = sorted([(t, per_mw(p, m)) for _, t, _, _, p, m, ty in DATA["deals"] if ty == "Asset" and m],
                    key=lambda z: -z[1])
    d.header(s, x0, y2, lw, "Price per MW, asset deals (US$m)")
    d.bar(s, x0, y2 + 0.35, lw, BOTTOM - y2 - 0.35, [a for a, _ in assets], [("US$m/MW", [v for _, v in assets])],
          number_format="0.0", gap=40)
    rx = x0 + lw + GUTTER
    d.header(s, rx, y2, W - R_ - rx, "Takeaways")
    d.bullets(s, rx, y2 + 0.4, W - R_ - rx, BOTTOM - y2 - 0.4, [
        "**Singapore assets rarely trade:** recent deals are Keppel and CapitaLand moving assets into their REITs",
        "**Platforms attract the largest cheques:** KKR / Singtel paid S$6.6bn for 82% of STT GDC, an S$13.8bn EV",
        "**Record capital:** APAC direct DC investment reached US$11.6bn in 2025",
        "**Recycling wave:** stakes in Bridge DC (Bain, US$5bn valuation), BDx (~US$2bn) and Princeton Digital "
        "are reportedly in play",
    ])
    d.footer(s, sources=f"{CBRE} (from MSCI RCA); STT GDC press release (4 Feb 2026); Keppel press release "
                        "(19 Nov 2024)",
             notes="Platform prices are for stakes and include pipeline and other markets, so per-MW is not meaningful "
                   "(n.m.); Keppel DC SGP 7 & 8 = S$1.38bn at S$1.34/US$, MW not disclosed (n.d.)")

    # ------------------------------------------------------------ 8. Valuation
    s = d.slide("Deal Activity", "What Singapore data centre assets are worth today")
    lw = 5.9
    d.header(s, x0, TOP, lw, "Hyperscale cap rates, Q1 2026 (%)")
    d.exhibit_takeaway(s, x0, TOP + 0.33, lw, "Singapore prices mid-pack: tighter than Johor, wider than Tokyo")
    cr = DATA["cap_rates"]
    d.football_field(s, x0, TOP + 0.75, lw, BOTTOM - TOP - 0.75, cr, fmt="0.0",
                     highlight=[c[0] for c in cr].index("Singapore"), label_fmt="{:.2f}–{:.2f}", axis=False,
                     vmin=3.0, vmax=8.2)
    rx = x0 + lw + GUTTER
    rw = W - R_ - rx
    d.header(s, rx, TOP, rw, "Listed benchmark: Keppel DC REIT")
    d.stat_strip(s, rx, TOP + 0.45, rw, 0.85, [(k["aum"], "AUM, 30 Jun 2026"), (k["sg_share"], "Singapore share"),
                                               (k["hyperscale"], "Rent from internet firms"),
                                               (k["leverage"], "Aggregate leverage")])
    d.header(s, rx, TOP + 1.55, rw, "Reading the benchmarks")
    d.bullets(s, rx, TOP + 1.95, rw, 1.75, [
        "**Cap rates:** Singapore hyperscale assets at 5.25–6.50%; CBRE reports slight compression as investors "
        "chase scarce existing stock",
        f"**Price per MW:** APAC asset deals cleared at US${min(v for _, v in assets):.0f}–"
        f"{max(v for _, v in assets):.0f}m per MW; platforms trade on EV including pipeline",
        "**Minority top-ups are accretive:** buying the last 10% / 1% of KDC SGP 3 & 4 (S$49.3m) added 0.8% to DPU",
        "**Implication:** entry prices already reflect scarcity; returns depend on rent reversion and AI upgrades",
    ])
    cy = TOP + 3.75
    d.header(s, rx, cy, rw, "Singapore reference deal: Keppel DC SGP 7 & 8 (Nov 2024)")
    d.table(s, rx, cy + 0.42, rw, [
        ["Price", "Lettable area", "Tenants", "WALE", "DPU accretion", "AUM after deal"],
        ["S$1.38bn", "150,455 sq ft", "100% hyperscale", "4.5 yrs", "+8.1%", "S$5.2bn (+36%)"],
    ], num_cols=(), row_h=0.4)
    d.footer(s, sources=f"{CBRE}; Keppel DC REIT, 1H 2026 results (22 Jul 2026); Keppel DC REIT, acquisition presentation (16 Dec 2025); Keppel press "
                        "release (19 Nov 2024)",
             notes="Cap-rate range: low end shell & core, high end fully fitted; DPU = distribution per unit; AUM as "
                   "at 30 Jun 2026, before Tokyo DC 4 & 5 (announced 1 Sep 2026)")

    # ------------------------------------------------------------ 9. Investment thesis (lessons #35: argue, don't list)
    assets_pm = sorted(per_mw(p, m) for _, _, _, _, p, m, ty in DATA["deals"] if ty == "Asset" and m)
    pm_lo, pm_hi = assets_pm[0], assets_pm[-1]
    pm_med = assets_pm[len(assets_pm) // 2]
    build_pm = 14.5                                   # US$/W = US$m per MW (Turner & Townsend, DC Cost Index 2025)
    cap_lo, cap_hi = 5.25, 6.50                       # Singapore hyperscale cap rates (CBRE)
    tokyo, sydney = dict(DATA["rents"])["Tokyo"], dict(DATA["rents"])["Sydney"]
    johor_up = 2500
    s = d.slide("Investment View", "Own scarce, powered capacity; grow through the corridor")
    d.takeaway(s, x0, TOP, bw, 0.5,
               "**Why invest:** Singapore data centres earn income that competitors cannot easily undercut and that "
               "rises at each renewal, with clear ways to add value and to sell. The play: buy powered Singapore "
               "capacity, grow through Johor and Batam, and sell to a REIT or platform buyer.")
    y1 = TOP + 0.62
    lw = 8.6
    d.header(s, x0, y1, lw, "Investment thesis")
    d.side_tabs(s, x0, y1 + 0.4, lw, BOTTOM - y1 - 0.4, [
        ("Secure income", (
            "Income is protected because competitors cannot add supply",
            f"Singapore's pipeline is {sg_up}MW, just {sg_up / sg_live:.0%} of its {sg_live}MW live stock and the "
            "lowest of eight APAC markets, because new capacity is released only by government tender. Occupancy is "
            "above 95%. **For returns:** low vacancy risk and predictable cash flow, which support a steady yield and "
            "debt financing.")),
        ("Rising rents", (
            "Rents reset higher at renewal, so income grows without new capital",
            f"Rents average US${sg_r}/kW a month, {sg_r / tokyo - 1:.0%} above Tokyo. Keppel DC REIT "
            f"({float(k['sg_share'].rstrip('%')):.0f}% Singapore) has re-let renewals higher in every recent period: "
            f"{k['rev_prev']} in 1H 2025 and {k['reversion']} in 1H 2026. About {k['exp_2030'][1:]} of its rent "
            "expires by 2030, so much of the rent roll reprices within a typical 5–7 year hold. **For returns:** "
            "repricing existing leases is the core driver of income growth.")),
        ("Build-to-core", (
            "Building and leasing new capacity creates value",
            f"A new Singapore build costs about US${build_pm}m per MW, while finished APAC assets sold for "
            f"US${pm_lo:.0f}–{pm_hi:.0f}m per MW in 2024–26 (median ~US${pm_med:.0f}m). Johor ({johor_up:,}MW+ "
            "upcoming, mostly pre-let) and Batam (NDP1, up to 144MW, cabled to Changi) give room to build what "
            "Singapore cannot. **For returns:** each pre-let MW built can be worth well above its cost, which is the "
            "main source of equity upside.")),
        ("Liquid exit", (
            "Many buyers compete for finished assets, so the value can be realised",
            "Sponsors sell finished assets into listed REITs (Keppel DC REIT paid S$1.38bn for Keppel DC SGP 7 & 8), "
            "and global capital buys whole platforms (KKR / Singtel valued STT GDC at an S$13.8bn EV). APAC data "
            "centre investment hit a record US$11.6bn in 2025. **For returns:** the exit can be underwritten at the "
            f"cautious {cap_hi:.2f}% cap rate; selling at {cap_lo:.2f}% instead would lift value by "
            f"~{cap_hi / cap_lo - 1:.0%}.")),
    ], tab_w=1.5)
    rx = x0 + lw + GUTTER
    rw = W - R_ - rx
    d.header(s, rx, y1, rw, "Return drivers in numbers")
    d.stat_icons(s, rx, y1 + 0.5, rw, BOTTOM - y1 - 0.5, [
        ("server", f"{sg_up / sg_live:.0%}", "Pipeline as a share of live stock"),
        ("percentage", ">95%", "Market occupancy"),
        ("trending-up", f"{k['reversion']} / {k['rev_prev']}", "Keppel DC REIT reversion, 1H26 / 1H25"),
        ("calendar", k["exp_2030"], "Keppel DC REIT rent expiring by 2030"),
        ("building-factory", f"US${build_pm}m vs ~{pm_med:.0f}m", "Build cost vs APAC sale price per MW"),
        ("cash", f"+{cap_hi / cap_lo - 1:.0%}", f"Value uplift, exit at {cap_lo:.2f}% vs {cap_hi:.2f}% cap rate"),
    ], cols=2, icon_size=0.4)
    d.footer(s, sources=f"{CBRE}; The Real Deal citing CBRE (Jun 2026); Keppel DC REIT (Aug 2025, Jul 2026); STT GDC "
                        "(4 Feb 2026); Turner & Townsend (2025); EDB / IMDA (Aug 2026)",
             notes=f"Own calculations: sale price per MW = APAC asset deals on slide 7 (Japan, Australia, Philippines; "
                   f"Singapore MW not disclosed); build cost is construction only, excl. land, power and fit-out; "
                   f"value uplift = {cap_hi:.2f} ÷ {cap_lo:.2f} − 1 at constant income")

    # ------------------------------------------------------------ 10. Risks and mitigants
    s = d.slide("Investment View", "Each key risk has a clear mitigant")
    d.header(s, x0, TOP, bw, "Key risks and mitigants")
    end = d.risk_matrix(s, x0, TOP + 0.4, bw, BOTTOM - TOP - 1.45, [
        (("Power and green rules tighten",
          "Data centres already use ~7% of Singapore's electricity, and new capacity must run ≥50% green at a PUE of "
          "1.25 or better. Tighter rules would raise running costs or block expansion."),
         ("Buy sites with secured power and a green plan",
          "Favour assets with committed grid capacity and a credible green-energy pathway, and price upgrade capex "
          "into the bid. **What remains:** rule changes can still lift costs market-wide.")),
        (("Rent depends on a few hyperscalers",
          f"Internet firms, mainly hyperscalers, pay {k['hyperscale']} of Keppel DC REIT's rent and its largest "
          f"client alone {k['top_client']}, so losing one tenant at renewal would cut income sharply."),
         ("Lock in long leases and widen the tenant mix",
          f"A {k['wale'].replace(' yrs', '-year')} WALE locks in income, and with market occupancy above "
          "95% vacated space re-lets fast. Add cloud, internet and telco tenants. **What remains:** re-letting risk at big "
          "expiries.")),
        (("Legacy halls cannot host AI",
          "Many older halls lack the power density and cooling AI tenants need, so they risk losing tenants or "
          "re-letting at lower rents as demand shifts to AI."),
         ("Budget liquid-cooling and power upgrades upfront",
          "Put retrofit capex in the entry model and pre-let upgraded space before spending, turning the risk into a "
          f"reinvestment project. **What remains:** cost overruns, with builds at US${build_pm}/W.")),
        (("Johor and Batam pull demand away",
          f"Johor is adding {johor_up:,}MW+, {johor_up / sg_up:.0f} times Singapore's {sg_up}MW pipeline, so "
          "price-sensitive bulk AI and hyperscale workloads can move there and cap Singapore rent growth."),
         ("Own interconnection-rich sites that cannot move",
          "28 subsea cables land in Singapore, so latency-sensitive workloads stay. Underwrite rent growth on that "
          "demand, not bulk compute. **What remains:** slower growth if bulk tenants leave.")),
        (("Higher rates widen cap rates",
          f"Singapore hyperscale assets trade at {cap_lo:.2f}–{cap_hi:.2f}%. A move from the bottom to the top of "
          f"that range cuts value by ~{1 - cap_lo / cap_hi:.0%} for the same income."),
         (f"Underwrite the exit at {cap_hi:.2f}%, the top of the range",
          "Returns then come from rent growth and reversion, not falling cap rates, so a rate rise does not break the "
          f"case. **What remains:** cap rates moving above {cap_hi:.2f}%.")),
    ], levels=[3, 2, 3, 2, 2])
    sy = end + 0.15
    d.stat_strip(s, x0, sy, bw, BOTTOM - sy, [
        ("~7%", "Singapore electricity used by data centres"),
        (k["top_client"], "Keppel DC REIT rent from its largest client"),
        (f"US${build_pm}/W", "Build cost, 2nd highest globally"),
        (f"{johor_up:,}MW+", "Johor pipeline, 10x Singapore's"),
        (f"−{1 - cap_lo / cap_hi:.0%}", f"Value hit, {cap_lo:.2f}% → {cap_hi:.2f}% cap rate"),
    ], align=PP_ALIGN.CENTER)
    d.footer(s, sources=f"{CBRE}; Keppel DC REIT, 1H 2026 results (Jul 2026); EDB / IMDA, DC-CFA2 (Dec 2025); "
                        "Turner & Townsend (2025); CSIS (Sep 2025)",
             notes=f"Risk level: Harvey ball, full = highest; illustrative view for discussion. Own calculations: "
                   f"value hit = 1 − {cap_lo:.2f} ÷ {cap_hi:.2f} at constant income; Johor ÷ Singapore pipeline")

    d.save(OUT)
    print(OUT)


if __name__ == "__main__":
    build()
