# Layout judge
You are setting the answer key for a slide-layout test. Work alone: use only this file and the sheet images it names.
Do not open golden.jsonl, scores.md, examples.md, swaps.md or any other file in the eval folder.

For each of the 46 rows below, open its `sheet` image with the Read tool. The left side is a real bank page (or, when
`has_page` is false, there is no page: judge from the written block). The right side shows candidate layouts from the
deck builder's library, lettered A, B, C... with their ids.

The question for every row: **which layout id would rebuild this exhibit (the `exhibit` / `content` fields: one chart,
table or list on the page, not the whole page) the way the bank actually drew it?** For rows without a page: which
layout would a top bank analyst choose for this content and message?
- Look at the shape of what the bank drew: chart type and orientation, table with or without bars / heat colours,
  number of panels, text boxes vs bullets, map, logos. Match that, not just the topic.
- You may name any id from the catalogue below, not only the candidates on the sheet, if it fits better.
- **Combos are allowed:** when the bank drew the exhibit with two layouts together (e.g. an infographic with a table
  beside it, two infographics side by side), answer `best` as `"<lead id>+<second id>"`. Only when both are really
  there; a single layout stays a single id.
- `ok`: other ids a demanding banker would also accept for this exhibit (0-3). Leave it empty if only one fits.
- `why`: one line naming what you saw (e.g. "horizontal bars ranked, 6 items, values at bar end").
- `flag`: "" for a good row. Otherwise one of:
  - `fragment`: the block is only part of one exhibit (half of a table, the text that belongs to a chart or funnel
    beside it, one column of a grid), so its layout can't be judged on its own.
  - `duplicate`: it repeats the content of a row in `same_page` (same items or the same exhibit). Flag only the row
    whose id sorts later, so one copy survives.
  - `garbled`: the text is unreadable or does not match the page.
  - `footnote`: notes, sources or filler, not an exhibit.
  Flag strictly: a good self-contained exhibit with plain text is NOT a fragment. Still give `best` for a flagged row.

Write `C:\Users\user\benedict-skills\plugins\benedict-skills\skills\deal-desk\scripts\..\assets\eval\runs\judge2\ans_b1_j2.json` as
{"<row id>": {"best": "<id or id+id>", "ok": ["<id>", ...], "why": "...", "flag": ""}, ...}
covering every row. Be decisive and consistent; other judges answer the same rows independently.

## Layout catalogue (id name (kind, data type, items): use when | don't)
- `ig001` Circular arrow loops (layout, cycle, 3-6 items): A loop with no text inside (flywheel, recurring revenue, recycling); label the stages beside it | Don't: Stages that need text inside the shapes (use ig002 v3 or the cycles 20-28)
- `ig002` Four-arrow operating loop (layout, cycle, 3-4 items): A 4-stage repeating loop with a one-word label inside each arrow (plan, analyse, control, track) | Don't: Stages that need a sentence each; more or fewer than 4 stages (v1/v2/v4 are small text-free loops)
- `ig003` Curved arrow shapes (icon_set, , 1-99 items): Icon / arrow shapes to copy into another layout | Don't: As a slide layout on its own
- `ig004` Square arrows: converge, diverge, loop (layout, process, 3-4 items): Four forces pushing in (converge) or out (diverge), a square 4-step loop, or a short 3-chevron flow | Don't: Steps that need text inside (use chevrons or ig101-107)
- `ig005` 2x2 notched quadrant / merging streams (layout, matrix, 2-4 items): Four text blocks in a 2x2 (strengths / weaknesses style), or two streams merging into one (a merger) | Don't: Long text per quadrant; a real 2x2 with axes (use harvey or a table)
- `ig006` Chevron-topped columns (layout, list, 2-6 items): 5-6 parallel workstreams or pillars, each a title plus 3 bullets; or a risks vs opportunities two-panel | Don't: A sequence where order matters (use chevrons)
- `ig007` Clock: four-step cycle (layout, cycle, 4-4 items): A 4-step quarterly or annual cycle (budget, review, report...), each step with a heading and 2-line text | Don't: Steps not tied to a calendar; more than 4 steps
- `ig008` Four inputs to one outcome (layout, relationship, 4-4 items): Four numbered drivers (heading + 2-line text) feeding one central result | Don't: Drivers with no shared outcome (use stat_icons)
- `ig009` Venn diagrams (2-4 circles) (layout, relationship, 2-4 items): Overlap, strategic fit or synergies between 2-4 businesses or capabilities | Don't: Parts that do not overlap (use pie sections or pill_rows)
- `ig010` Four-ellipse Venn with % values (layout, relationship, 4-4 items): Overlap shares between 4 customer groups or products, % in each region | Don't: Fewer than 4 sets (use ig009)
- `ig011` Concentric rings and quadrant discs (layout, hierarchy, 2-4 items): Core-to-periphery layers (core business, adjacencies, new markets) or 4 equal quadrants; label beside | Don't: Real proportions (use stat_rings or a chart)
- `ig012` Pie sections (2-12 equal slices) (layout, composition, 2-12 items): A numbered split into 2-12 equal parts with labels beside (segments, product lines) | Don't: Real proportions (use stacked or stat_rings); the pies are one group, so delete the counts you don't need
- `ig013` 16-part wheel with outer ring (layout, composition, 12-16 items): 12-16 parts around a core (a portfolio of assets, a product range) with short labels in the segments | Don't: Fewer than 8 parts (use ig015 or ig019)
- `ig014` Phase wheels (3-7 segments) (layout, cycle, 3-7 items): 3-7 components or phases around a central title, 1-3 words per segment | Don't: Segments that need sentences (use ig019 or ig036)
- `ig015` Five-section wheel with centre (layout, composition, 2-8 items): Five business pillars or segments around a centre theme, one short line in each segment (v3) | Don't: Numbers per segment (use ig019 with numbered bubbles); v1-v7 are text-free 2-8 part rings
- `ig016` Sectioned rings with arrows (layout, cycle, 2-6 items): A continuous loop of 2-6 stages; text-free, label the stages beside it | Don't: Stages that need text inside
- `ig017` Five-part arrow wheel and pinwheel (layout, cycle, 4-5 items): A 5-step value cycle with 1-2 words per segment, or 4 quadrants with ring labels | Don't: Long text per step
- `ig018` Numbered seven-part wheel (layout, composition, 2-8 items): Up to 7 numbered parts around a wheel, explained in a list beside it | Don't: Text inside the segments
- `ig019` Five pillars around a goal (layout, cycle, 3-8 items): Five numbered strategic pillars around a central goal, one line of text in each segment | Don't: Pillars needing more than ~8 words (use side_tabs)
- `ig020` Three-part ring around a globe (layout, cycle, 3-3 items): A global 3-stage loop (source, make, distribute) with labels on the ring | Don't: Local / single-country stories
- `ig021` Three arrows around a globe; progress rings (layout, cycle, 3-6 items): A global loop of 3 stages (v2); progress rings 1/6 to 6/6 (v1) for completion status | Don't: Stages that need sentences
- `ig022` Core radiating into four segments (layout, relationship, 4-4 items): One core offering serving 4 markets or segments, labels on the ring (v3) | Don't: Unrelated segments
- `ig023` Three-part ring with globe; progress donuts (layout, composition, 3-3 items): A 3-way global split around a globe (v3) | Don't: Exact proportions (use stat_rings)
- `ig024` Circular icon layouts (icon_set, , 1-99 items): Icon / arrow shapes to copy into another layout | Don't: As a slide layout on its own
- `ig025` Six-segment wheel; entry into a loop (layout, cycle, 3-6 items): A 6-part wheel with labels on the segments (v1), or an entry arrow feeding a recurring loop (v2) | Don't: More than 6 stages
- `ig026` M&A deal cycle (layout, process, 4-8 items): The deal lifecycle: strategy, due diligence, financing, execution, post-deal integration (v2); a 4-arc loop (v1) | Don't: A deal timetable with dates (use timeline)
- `ig027` Entry arrow into a four-step cycle (layout, cycle, 4-5 items): Capital entering a repeating cycle (invest, grow, harvest, reinvest), short labels | Don't: One-off sequences (use chevrons)
- `ig028` Twelve-step lifecycle with text blocks (layout, process, 8-12 items): A detailed 8-12 step lifecycle with a header and text block per step (dense one-page process) | Don't: Fewer than 6 steps (use chevrons)
- `ig029` Hubs with radiating arms (layout, relationship, 3-4 items): A centre splitting into 3-4 outputs or channels, short labels on each arm | Don't: A sequence
- `ig030` Three stakeholders around a shared centre (layout, relationship, 3-3 items): Three parties or values converging on one shared centre (company, employer, assignees; values triangle) | Don't: More than 3 parties (use hub_spoke)
- `ig031` Target operating model (layout, relationship, 4-8 items): Operating model: functions across the top, geographies below, the target model in the centre | Don't: Simple org charts (use ig071-073 pyramids or a table)
- `ig032` Core with three satellites; quadrant disc (layout, relationship, 3-4 items): A core with 3 linked satellites (v2) or 4 quadrants with ring labels (v1) | Don't: Sequences
- `ig033` Quadrants with circular arrows; spiral (layout, cycle, 4-4 items): Four stages of a loop set in quadrants, short labels | Don't: Long text
- `ig034` Quadrant background with central loop (layout, matrix, 4-4 items): Four corner labels around a 4-part central loop | Don't: Text-heavy quadrants (use ig005)
- `ig035` Quadrant pie in arrows; 12-part wheel (layout, cycle, 4-12 items): Four quadrants inside a loop of arrows (v1) or a 12-part wheel with ring text (v2) | Don't: Long text
- `ig036` Interlocking numbered pillars with icons (layout, relationship, 3-4 items): 3 (v1) or 4 (v2) numbered pillars, each with icon, heading and 2-line text, around a central heading | Don't: Pillars needing argued paragraphs (use side_tabs)
- `ig037` Four numbered bubbles around a hub (layout, list, 4-4 items): 4 numbered themes, each a title plus ~25 words, of unequal weight (bubble sizes differ) | Don't: Equal-weight items (use ig036 or stat_icons)
- `ig038` Layered target wheel; nested rings with arrows (layout, hierarchy, 4-8 items): Layers from core to edge, 4 quadrants x 3 rings with short labels (v1), or nested rings around a two-way flow (v2) | Don't: Sentences per segment
- `ig039` Four-section ring with bullet corners (layout, list, 4-4 items): Four sections around a centre, each with a title on the ring and 4 bullets in its corner | Don't: More than 4 sections
- `ig040` Four-quadrant ring with corner text (layout, matrix, 4-4 items): Four themes on a ring with a short phrase each and a longer note in each corner | Don't: Long bullet lists (use ig039)
- `ig041` Arrow wheel with icons; four numbered dials (layout, process, 4-6 items): 6 steps with icon, heading and short text around a wheel plus a heading/paragraph (v1); 4 numbered steps as dials (v2) | Don't: More than 6 steps
- `ig042` Six-section wheel with bullet panels (layout, list, 5-6 items): 6 sections on a wheel, each with a title, and bullet panels left and right explaining them | Don't: Fewer than 5 sections (use ig039)
- `ig043` Six pillars of success with risk text (layout, list, 6-6 items): 6 pillars around a goal, each with a 4-5 bullet text block (risk areas, success factors) | Don't: Fewer than 6 pillars
- `ig044` Seven and six-part ringed wheels (layout, composition, 6-7 items): 6 (v2) or 7 (v1) labelled segments around a numbered or titled centre | Don't: Long text
- `ig045` Seven petals with icons (layout, composition, 7-7 items): 7 offerings or values around a central heading, each with icon, title and ~20 words | Don't: Fewer than 6 items
- `ig046` Eight and nine-petal star wheels (layout, composition, 8-9 items): 8-9 numbered parts around a centre, one word each | Don't: Text-heavy items
- `ig047` Nested ring cycles (layout, cycle, 3-4 items): A loop of 3-4 stages inside an outer ring of themes, short labels on the ring | Don't: Sentences
- `ig048` Three-level sunburst (layout, hierarchy, 6-16 items): A 3-level breakdown (group, division, product) as a sunburst with short labels | Don't: Real proportions (use a chart)
- `ig049` Ring of 12 labelled points; ringed 12-part wheel (layout, cycle, 8-12 items): 12 short items around a centre (months, product lines, process points), one or two words each | Don't: Fewer than 8 items
- `ig050` Eight-spoke star; arrows around a core (layout, relationship, 4-8 items): 8 short items radiating from a numbered core (v1), or 4-5 arrows circling a core value (v2) | Don't: Text longer than 3 words
- `ig051` Team wheel (core team and partners) (layout, hierarchy, 6-24 items): A deal or advisory team: core team in the centre, names and titles around, senior partners on the arcs | Don't: Org charts with reporting lines (use ig071-073 or a table)
- `ig052` Main heading with six bubbles and side text (layout, list, 6-8 items): 6-8 themes around a main heading, each with a short heading on the bubble and ~30 words of text outside | Don't: Fewer than 5 themes (use ig036/ig039)
- `ig053` Eight-node flower around a title (layout, composition, 6-8 items): 8 short items around one title (product lines, markets) | Don't: Text longer than 2 words
- `ig054` One central solution with 10 bands (layout, relationship, 8-10 items): One platform serving 8-10 named services or modules, listed in bands left and right | Don't: Unrelated items (use pill_rows)
- `ig055` Concentric bubbles of client value (layout, hierarchy, 8-16 items): A value proposition: a core statement, inner ring of 6-8 strengths, outer ring of 6-8 outcomes, 2-4 words each | Don't: Fewer than 6 items
- `ig056` Labelled sunburst around a core (layout, composition, 12-16 items): A capability or risk universe: 12-16 labelled segments around a core function (e.g. IT assurance, internal audit) | Don't: Fewer than 8 segments
- `ig057` Speedometer gauges (%) (layout, kpi_set, 1-3 items): 1-3 percentage scores shown as gauges (utilisation, occupancy, margin vs target) | Don't: Values with no natural 0-100 scale
- `ig058` Large speedometer with average (layout, kpi_set, 1-1 items): One headline score on a 0-100 scale with an average (customer score, utilisation) | Don't: Several KPIs (use ig057)
- `ig059` Radial heat map (layout, matrix, 6-8 items): Scores for 6-8 areas on a radial scale (maturity or risk assessment by area) | Don't: Exact values (use heatmap)
- `ig060` Circular bar chart (target vs current) (layout, comparison, 10-20 items): Target vs current scores across 10-20 areas in one compact radial chart | Don't: Few data points (use bar)
- `ig061` Four-quadrant stacked ring of % bars (layout, comparison, 4-4 items): 4 categories, each with up to 10 stacked % rings (survey results by region or segment) | Don't: One simple split (use stat_rings)
- `ig062` Alphabet wheel with % markers (layout, composition, 10-26 items): A share split across up to 26 small categories with % markers around the rim | Don't: Fewer than 10 categories
- `ig063` Three donuts with % segments (layout, composition, 3-3 items): Mix by category for 3 entities or years (revenue mix, cost mix), with a shared legend | Don't: More than 4 segments each (use stacked)
- `ig064` Three % rings with captions (layout, kpi_set, 3-3 items): 3 headline percentages, each with a one-line caption (survey answers, adoption rates) | Don't: Numbers that are not shares of a whole
- `ig065` Arc bars by country (3 questions) (layout, comparison, 3-4 items): Survey or market results: 3 questions x 4 countries as arcs with % values | Don't: Exact comparisons (use bar)
- `ig066` Spiral ranking of scores (layout, comparison, 6-9 items): A ranked list of 6-9 items with scores, drawn as concentric arcs | Don't: Values that need precise reading (use bar)
- `ig067` Year-on-year spiral arcs (layout, comparison, 2-2 items): Two years compared as concentric arcs (2011 vs 2012) | Don't: More than 2 periods (use column)
- `ig068` Odds bubbles (risk ratios) (layout, comparison, 2-4 items): Likelihood ratios for 2-3 scenarios shown as bubbles on a line | Don't: Ordinary % data
- `ig069` Radar screen (positioning arcs) (layout, matrix, 3-6 items): Positioning 3-6 players or opportunities on a semicircle by segment and distance from the centre (priority) | Don't: Exact values
- `ig070` Hub of measure bars by risk area (layout, kpi_set, 10-16 items): Scores for 10-16 areas grouped into 3-4 themes around an identify/measure/manage/monitor hub | Don't: Fewer than 8 areas
- `ig071` Pyramids (3-4 levels) (layout, hierarchy, 3-4 items): 3-4 tiers from base to top (customer tiers, capital structure, Maslow-style priorities), short label per tier | Don't: Tiers that need sentences (use ig072)
- `ig072` Governance pyramid with notes (layout, hierarchy, 5-5 items): A 5-tier pyramid (intent, goals, strategy, plans, results) with a note per tier and KPI brackets | Don't: Fewer than 4 tiers (use ig071)
- `ig073` Value pyramid (protection to enhancement) (layout, hierarchy, 8-16 items): Value creation levers in tiers: value protection at the base, enhancement at the top, 3-6 boxes per tier | Don't: Simple 3-tier lists (use ig071)
- `ig074` Hexagon pillars, tabs, honeycomb, network (layout, relationship, 3-7 items): Three-sided strengths around a hexagon (v1), 4 stacked numbered tabs (v2), a honeycomb cluster (v3), or a network of 6 nodes around a hub (v4) | Don't: Long text
- `ig075` Six hexagon columns with icons (layout, list, 4-6 items): 6 numbered pillars, each with icon, heading and ~20 words (capabilities, strengths) | Don't: Fewer than 4 items (use stat_icons)
- `ig076` Honeycomb with section text (layout, list, 6-6 items): 6 sections on a honeycomb around a centre, each with a title and ~25 words beside | Don't: Fewer than 5 sections
- `ig077` Six arrows converging on a hexagon (layout, relationship, 4-6 items): 6 drivers or market forces pushing in on one point, short label on each arrow | Don't: Sentences per driver
- `ig078` Octagon clusters (layout, relationship, 2-3 items): 2-3 linked units each with 8 surrounding parts; text-free, labels beside | Don't: Text inside
- `ig079` Spider diagram with points (layout, matrix, 6-8 items): Plotting 2-4 items on 8 axes (positioning, capability scores) | Don't: Exact values (use a table)
- `ig080` Radar overlay diagram (layout, comparison, 6-8 items): Comparing 2-3 profiles across 6-8 criteria as overlapping shapes (us vs peers) | Don't: Exact values (use harvey or a table)
- `ig081` Jigsaw grid (layout, relationship, 4-30 items): Pieces that fit together (bolt-on acquisitions completing a platform); text-free, colour the key pieces | Don't: Text inside the pieces
- `ig082` Large jigsaw panel (layout, relationship, 4-10 items): Large 2x5 jigsaw for a 'missing piece' story, one piece highlighted | Don't: Text inside the pieces
- `ig083` Jigsaw ring; jigsaw column (layout, relationship, 4-8 items): A ring of 8 interlocking pieces around a core (v2) or 4 stacked pieces (v1); text-free | Don't: Text inside
- `ig084` Loose and locked jigsaw pieces (layout, relationship, 2-4 items): Fit between businesses: loose pieces vs a completed square (strategic fit, merger) | Don't: Text inside
- `ig085` Three-column jigsaw (process, brand, ROI) (layout, relationship, 3-3 items): 3 workstreams as jigsaw columns with short labels on the pieces | Don't: Long text
- `ig086` Two-by-three large jigsaw (layout, relationship, 4-6 items): A 6-piece 'missing piece' visual, text-free (complete the platform) | Don't: Text inside
- `ig087` Jigsaw pattern texture (icon_set, , 1-99 items): Background texture for a cover or divider | Don't: As a slide layout on its own
- `ig088` Eight-piece jigsaw wheel (layout, list, 8-8 items): 8 numbered parts of one whole (e.g. an integrated offering), each with ~20 words, around a centre title | Don't: Fewer than 6 parts
- `ig089` Chain of cog wheels (layout, process, 6-10 items): 6-10 interlocking steps or functions that drive each other, 1-2 words in each cog | Don't: Long text
- `ig090` Two interlocking cogs (layout, relationship, 2-2 items): Two businesses or functions working together (synergy), labels beside | Don't: Text inside
- `ig091` Cogs in a conveyor loop (layout, process, 2-2 items): Two engines driving a continuous loop (operating model, flywheel); text-free | Don't: Text inside
- `ig092` Two cogs with icons and options (layout, relationship, 2-2 items): Two capability engines (4 icons each) with option notes beside | Don't: More than 2 groups
- `ig093` Bridge / waterfall chart (layout, bridge, 3-6 items): Walk from a start value to an end value through 3-6 drivers (EBITDA bridge, value creation bridge) | Don't: Use only when python charts are unavailable; prefer fin_chart / native waterfall
- `ig094` Thermometer (progress to target) (layout, kpi_set, 1-1 items): One measure rising between two years or toward a target (fundraising progress) | Don't: Several measures (use ig096)
- `ig095` Percentage columns with bubbles (layout, kpi_set, 3-5 items): 3-5 categories with a headline % each, drawn as filled columns (utilisation, margin by segment) | Don't: Values that are not %
- `ig096` Four thermometer bars with icons (layout, kpi_set, 4-4 items): 4 numbered measures with a level marker and a short caption each | Don't: More than 4 measures
- `ig097` Dot plot with value labels (layout, time_series, 6-10 items): 8-10 values over time or categories as labelled dots | Don't: Prefer fin_chart line; use only for a stylised look
- `ig098` Bottleneck funnel over time (layout, process, 4-6 items): A shift over time from one model to another (local to shared services), with 4-6 short labels | Don't: Many steps (use chevrons)
- `ig099` Five icon blocks feeding one output (layout, list, 5-5 items): 5 inputs (icon + ~25 words each) combining into one outcome line | Don't: More than 5 inputs
- `ig100` Maze (complexity to clarity) (layout, process, 1-1 items): A complex path we navigate for the client (regulatory approvals, deal complexity); text-free | Don't: Text inside
- `ig101` Three streams into one big arrow (layout, relationship, 3-3 items): 3 inputs merging into one outcome with 3 bullets (how 3 sources combine into the thesis) | Don't: Inputs needing sentences
- `ig102` Bull and bear two-way arrows (layout, comparison, 2-2 items): Upside vs downside case (bull vs bear), each with heading and ~25 words | Don't: More than 2 cases
- `ig103` Nested chevron of six layers (layout, list, 4-6 items): 6 stacked layers ending in one point (6 drivers building to one result), short label each | Don't: Text longer than 6 words
- `ig104` Three numbered branches into blocks (layout, process, 3-3 items): 3 numbered streams branching into 3 stacked blocks with text (fund flows, workstreams) | Don't: More than 3 streams
- `ig105` Diagonal numbered steps; icon list (layout, process, 4-4 items): 4 numbered steps with ~15 words each on a diagonal band (v1) or 4 icon rows with numbered bubbles (v2) | Don't: More than 4 steps
- `ig106` Four steps with icons and text (layout, process, 4-4 items): 4 sequential steps, each with icon, step name and ~30 words to the right (deal process, value plan) | Don't: More than 5 steps (use timeline)
- `ig107` Funnel of inputs to one output (layout, process, 3-12 items): Many inputs narrowing into one output (deal screening: universe to shortlist), short labels | Don't: Exact numbers per stage (use ig127 or a table)
- `ig108` Numbered options with speech panels (layout, list, 4-4 items): 4 numbered options, each with ~40 words in a panel (strategic options, exit routes) | Don't: More than 4 options
- `ig109` House with roots (foundations) (layout, hierarchy, 4-8 items): One roof message supported by 6-8 foundation items (platform built on capabilities) | Don't: Items needing sentences (use ig006)
- `ig110` Five chevrons with notes above and below (layout, process, 4-5 items): 5 sequential phases with a title in each chevron and ~15 words alternating above and below | Don't: More than 6 phases (use timeline)
- `ig111` Numbered milestone rows (layout, process, 5-7 items): 5 milestones with ~20 words each (v1) or 7 numbered steps with one line each (v2) | Don't: Dates on a scale (use timeline)
- `ig112` 1-5 rating scales (layout, matrix, 3-5 items): Rating 3-5 items on a 1-5 scale (maturity, risk score) or strong/average/weak dots (v3) | Don't: Exact values
- `ig113` Branching process (protect vs enhance) (layout, process, 6-12 items): A process that splits into two paths of 4-5 steps (value protection vs value enhancement) | Don't: Single linear process (use chevrons)
- `ig114` Three-step spiral with tasks (layout, process, 3-3 items): 3 steps, each a title in a circular arrow plus 3 task bullets | Don't: More than 3 steps
- `ig115` Converging and diverging arrows (layout, relationship, 2-2 items): Two sets of flows meeting (capital in, returns out; buyers meet sellers); 2 labels | Don't: Text-heavy
- `ig116` Inputs-funnel-outputs (layout, process, 6-6 items): 6 inputs through a funnel into 2 output boxes of bullets (business model, deal sourcing funnel) | Don't: Exact stage counts
- `ig117` Monopoly board timeline (layout, process, 12-16 items): A dense two-year programme with 12-16 boxed steps around a board and a central loop | Don't: Simple processes
- `ig118` Phase chevron rows (layout, process, 5-6 items): 5 phases with name and short description (v1) or 6 numbered phases in 1-2 rows (v2) | Don't: Phases needing more than 8 words (use ig110 or timeline)
- `ig119` Five option columns with icons (layout, list, 3-5 items): 5 options or alternatives, each with number, heading, ~40 words and an icon | Don't: Fewer than 3 options
- `ig120` Three workstreams x three steps (layout, process, 3-3 items): 3 lettered workstreams (A, B, C) each with 3 steps of ~15 words (value creation plan, 100-day plan) | Don't: One workstream (use ig106)
- `ig121` Winding road map (layout, process, 5-7 items): A 6-step journey (prioritise, analyse, target, communicate, implement, develop) with ~25 words per step | Don't: Dated milestones (use timeline)
- `ig122` Snake road with four titled steps (layout, process, 4-4 items): 4 numbered steps down a winding road, each a title and 2 text blocks | Don't: More than 4 steps
- `ig123` Company history timeline (layout, time_series, 6-10 items): A company's history: 8-10 dated milestones on a curved line with ~20 words each | Don't: Future plans (use ig121 or timeline)
- `ig124` Dense dated timeline with team key (layout, time_series, 10-40 items): A detailed project or deal timetable: 20-40 dated events above and below a line, coloured by team | Don't: Fewer than 10 events (use timeline)
- `ig125` Year axis with event markers (layout, time_series, 6-10 items): A 20-year history with 6-10 labelled events and a shaded volume band (company history, market cycles) | Don't: Few events (use timeline)
- `ig126` Gantt chart (layout, time_series, 5-8 items): A workplan or 100-day plan: 5-8 workstreams across weeks or months | Don't: Fewer than 3 workstreams (use timeline)
- `ig127` Methodology cycle with workplan grid (layout, process, 5-5 items): An audit or diligence methodology: a 5-step cycle, phases strip and activity boxes, with side text | Don't: Simple processes
- `ig128` Twelve-month ring with notes (layout, time_series, 6-12 items): An annual cycle by month with 8-10 notes pointing to months (reporting calendar, seasonality) | Don't: Multi-year timelines
- `ig129` Annual communication rings by audience (layout, time_series, 5-5 items): Who gets what update in which month: 5 audiences as rings over 12 months | Don't: Single audience
- `ig130` Annual timetable wheel (layout, time_series, 6-8 items): An annual plan: 12 months in a ring with 6-8 activity sectors (audit cycle, budget cycle) | Don't: Multi-year plans
- `ig131` Year calendar (ring and grid) (layout, time_series, 12-12 items): A full-year calendar to mark key dates; v1 ring, v2 grid | Don't: Anything but a calendar
- `ig132` Balance (seesaw) of two panels (layout, comparison, 2-2 items): Weighing two sides (benefits vs costs, upside vs risks), 3-4 bullets each | Don't: More than 2 sides
- `ig133` Hanging balance panels (layout, comparison, 2-2 items): Two hanging panels compared side by side (before vs after), text added in each | Don't: More than 2 sides
- `ig134` UK and Ireland with region highlight (map, geography, 1-30 items): UK footprint: shade the home region, dots for sites | Don't: Data that is not about places; colour by value only with a legend
- `ig135` UK offices with city labels (map, geography, 1-30 items): UK office or asset locations (30 named cities) | Don't: Data that is not about places; colour by value only with a legend
- `ig136` London street map with site tags (map, geography, 1-30 items): Sites or properties in central London (real estate, offices) | Don't: Data that is not about places; colour by value only with a legend
- `ig137` South East England sites (map, geography, 1-30 items): 6-8 sites in South East England (assets, depots) | Don't: Data that is not about places; colour by value only with a legend
- `ig138` UK nations and counties (map, geography, 1-30 items): Coverage by UK nation (v1) or county (v2) | Don't: Data that is not about places; colour by value only with a legend
- `ig139` UK postcode areas (map, geography, 1-30 items): Coverage or demand by UK postcode area | Don't: Data that is not about places; colour by value only with a legend
- `ig140` UK local authorities (map, geography, 1-30 items): Coverage by UK local authority | Don't: Data that is not about places; colour by value only with a legend
- `ig141` England local authorities with London inset (map, geography, 1-30 items): Regional coverage across England with a London zoom | Don't: Data that is not about places; colour by value only with a legend
- `ig142` London boroughs (map, geography, 1-30 items): Coverage or demand by London borough | Don't: Data that is not about places; colour by value only with a legend
- `ig143` World map with country contact boxes (map, geography, 6-12 items): Global presence: 10-12 countries with a contact or fact box each | Don't: Data that is not about places; colour by value only with a legend
- `ig144` World map (Atlantic centred) (map, geography, 1-30 items): Global footprint by country: shade the countries where the company operates | Don't: Data that is not about places; colour by value only with a legend
- `ig145` World map with Europe enlarged (map, geography, 1-30 items): Global footprint where European countries need to be readable | Don't: Data that is not about places; colour by value only with a legend
- `ig146` World map (Pacific centred) (map, geography, 1-30 items): Asia-Pacific-led global footprint (Asia in the middle) | Don't: Data that is not about places; colour by value only with a legend
- `ig147` World coverage by territory (map, geography, 1-30 items): Global coverage: shade served vs unserved countries in two tones | Don't: Data that is not about places; colour by value only with a legend
- `ig148` Europe by country (map, geography, 1-30 items): European presence or market split by country | Don't: Data that is not about places; colour by value only with a legend
- `ig149` Americas by country (map, geography, 1-30 items): North and South American presence by country | Don't: Data that is not about places; colour by value only with a legend
- `ig150` Asia Pacific by country (map, geography, 1-30 items): APAC presence by country (Singapore, SEA, Australia deals) | Don't: Data that is not about places; colour by value only with a legend
- `ig151` Middle East by country (map, geography, 1-30 items): Middle East presence by country | Don't: Data that is not about places; colour by value only with a legend
- `ig152` Africa by country (map, geography, 1-30 items): African presence by country | Don't: Data that is not about places; colour by value only with a legend
- `ig153` Australia and Pacific Rim (map, geography, 1-30 items): Australia and SEA / Pacific Rim presence | Don't: Data that is not about places; colour by value only with a legend
- `ig154` Globe (Atlantic view) (map, geography, 1-1 items): A single globe for a cover, divider or global theme | Don't: Data that is not about places; colour by value only with a legend
- `ig155` Regional globes (map, geography, 1-6 items): A small globe per region (Africa, Americas, Europe-Asia) as a section icon | Don't: Data that is not about places; colour by value only with a legend
- `ig156` Asia, Australia and Europe globes (map, geography, 1-4 items): A small globe per region as a section icon | Don't: Data that is not about places; colour by value only with a legend
- `ig157` Quote bubbles (3x3) (layout, list, 1-9 items): Short quotes or key messages (management, customer or expert views), up to 15 words each; one variant per bubble | Don't: Long quotes (use a text panel)
- `ig158` Industry sector icons (icon_set, , 1-99 items): Sector icons (aerospace, banking, energy, healthcare, private equity, real estate, TMT, utilities...) for sector lists, coverage pages and deal tombstones | Don't: As a slide layout on its own
- `ig159` Assorted icons (health, finance, green, travel) (icon_set, , 1-99 items): Single icons beside headings: documents, healthcare, calculator, tax, globe, energy, utilities, education | Don't: As a slide layout on its own
- `ig160` Assorted icons (industry, awards, security) (icon_set, , 1-99 items): Single icons: industry, shipping, checklist, trophy, talent, stock exchange, strategy, insurance, savings | Don't: As a slide layout on its own
- `ig161` Assorted icons (charts, clock, mail, travel) (icon_set, , 1-99 items): Single icons: pie chart, line graph, dashboard, transport, clock, email, travel; pin markers (v11) | Don't: As a slide layout on its own
- `ig162` Sustainability icons and symbols (icon_set, , 1-99 items): ESG / sustainability pages: energy, recycling, transport, people, cities, with % call-outs | Don't: As a slide layout on its own
- `ig163` Recycling diagram (icon_set, , 1-99 items): Recycling / waste process illustration (bins, materials) | Don't: As a slide layout on its own
- `ig164` Business, people and industry icons (icon_set, , 1-99 items): Single icons: currency, %, people, industry, health | Don't: As a slide layout on its own
- `ig165` Signs, agriculture, weather, transport icons (icon_set, , 1-99 items): Single icons: safety signs, agriculture, weather, transport modes | Don't: As a slide layout on its own
- `ig166` Miscellaneous icons (money, ideas) (icon_set, , 1-99 items): Single icons: money bags by currency, idea bulb, tools | Don't: As a slide layout on its own
- `ig169` Business people silhouettes (icon_set, , 1-99 items): People silhouettes for team, management or customer pages | Don't: As a slide layout on its own
- `ig170` Assorted people silhouettes (icon_set, , 1-99 items): Single people silhouettes (walking, working, sport) | Don't: As a slide layout on its own
- `ig171` Traffic lights and Harvey rows (layout, matrix, 1-4 items): RAG status of 1-4 items as traffic lights (v1-v4) or a Harvey ball scale per row (v5-v7) | Don't: More than 4 statuses (use harvey or risk_matrix)
- `ig172` Service hubs with icon bubbles (layout, relationship, 2-3 items): 2-3 service lines, each a hub with 5-8 icon bubbles (offering map) | Don't: A sequence
- `ig173` Client network spark (layout, relationship, 8-16 items): A client or partner network radiating from one node (customer base, ecosystem), short labels | Don't: Exact counts (use a chart)
- `ig174` City skyline with six icon panels (layout, list, 6-6 items): 6 facts or themes about a city or location, each ~10 words with an icon (location advantages) | Don't: Not about a place
- `ig175` People portraits with captions (layout, list, 4-8 items): 8 stakeholder or customer types, each with a caption above and below the silhouette (customer personas) | Don't: Fewer than 4 personas
- `ig176` City scene with callouts (layout, list, 4-5 items): 4-5 callouts on a city scene (urban demand drivers, real estate, infrastructure) | Don't: Not about a place
- `ig177` Headline KPIs with icons and rings (layout, kpi_set, 3-6 items): 3-6 headline numbers (hours, payments, % rate) as icon dials with a short explanation below | Don't: Numbers needing a trend (use fin_chart)
- `ig178` Survey donuts with person and icons (layout, composition, 3-8 items): Survey results: two-year donuts, a headline % dial and an icon legend | Don't: Simple splits (use stat_rings)
- `ig179` Donut speech bubbles above people (layout, composition, 4-4 items): Mix split for 4 groups (e.g. tax mix by type), each donut above a person | Don't: More than 3 segments per donut
- `ig180` Icon list rows (layout, list, 3-6 items): 6 points each with an icon and ~30 words (key messages, product list) | Don't: Fewer than 3 points (use pill_rows)
- `ig181` Icon ring; % disc; people pictogram; money disc (layout, kpi_set, 1-12 items): A ring of 12 sector icons (v1), a headline % disc (v3), a 1-in-N people pictogram (v4), or an icon disc (v5-v6) | Don't: Several numbers needing comparison (use bar)
- `ig182` Layered rings with four headings (layout, list, 4-4 items): 4 layers or capabilities, each an icon on a ring with heading and ~25 words to the right | Don't: More than 4 items
- `ig183` Travel map with % bars (map, geography, 8-16 items): Global flows (routes, tourism, trade) with a % bar per city or destination | Don't: No geographic angle
- `ig184` Ranked city rows with icons (layout, comparison, 3-3 items): Ranking 3 metrics across cities (#1-#8) with icon markers (location benchmarking) | Don't: Exact values
- `ig185` Europe map with headed callouts (map, geography, 4-6 items): 5-6 European locations, each with a heading and ~15 words (sites, offices, deals) | Don't: Global footprint
- `ig186` Connectivity hub; stopwatch; client network (layout, relationship, 1-12 items): Connectivity theme with 4 icons (v1), a client at the centre of a network of 12 people (v2), a timing icon (v3) | Don't: Text-heavy pages
- `ig187` Dice net with icons (layout, list, 6-6 items): 6 sides of one business, an icon or number per face | Don't: Text inside
- `ig188` Door hanger cards (layout, list, 4-4 items): 4 numbered actions or principles, each icon, title and ~6 words | Don't: Long text
- `ig189` Paint drops at staggered heights (layout, process, 4-4 items): 4 numbered steps rising or falling, each a title and ~20 words | Don't: More than 4 steps
- `ig190` Single large icons (people, satellite, bulb) (icon_set, , 1-99 items): A single big icon for a section divider | Don't: As a slide layout on its own
- `ig191` Six-step list with three pillars (layout, list, 6-6 items): A numbered 6-step approach plus 3 pillar icons that add up to an outcome (people + approach + technology) | Don't: Fewer than 4 steps
- `ig192` Six-petal flower around a core (layout, relationship, 6-6 items): 6 traits or capabilities around a core idea, 2-3 short lines in each petal | Don't: Long text
- `ig193` Three-circle Venn around a person (layout, relationship, 3-3 items): Three skills or capabilities overlapping in one person or team (management quality), one word per circle | Don't: More than 3 sets (use ig009)
- `ig194` Value cycle with word cloud (layout, cycle, 3-3 items): A 3-stage loop (understand, plan, deliver) around a cloud of 10-16 value words | Don't: Sentences
- `ig195` Funnel of dot pyramids (layout, hierarchy, 3-3 items): Many items filtered down in 3 tiers (risks, deal screening: universe, long list, shortlist) with tier labels | Don't: Exact counts (use ig127 or a table)
- `ig196` Risk map with movement arrows (layout, matrix, 4-8 items): 5-8 numbered risks on likelihood vs impact, with arrows showing change, plus a risk table (v2) | Don't: Fewer than 3 risks
- `ig197` Testing strategy grid (layout, matrix, 10-20 items): 15-20 risks or items rated across 3 groups of columns with marker squares (diligence scope, risk testing) | Don't: Few items (use harvey)
- `ig198` Scope comparison year to year (layout, comparison, 2-2 items): How a structure or scope changes between two years: before and after block diagrams | Don't: One period
- `ig199` Editable line graphics (arrows, rings) (icon_set, , 1-99 items): Outline shapes to build a custom diagram | Don't: As a slide layout on its own
- `ig200` Editable world map outlines (map, , 1-99 items): Outline world maps (line, dot, network styles) as a background | Don't: As a slide layout on its own
- `ig201` Editable flow and hexagon outlines (icon_set, , 1-99 items): Outline flow, timeline and hexagon shapes to build a diagram | Don't: As a slide layout on its own
- `ig202` Editable table and Gantt outlines (icon_set, , 1-99 items): Outline grids and Gantt bars to build a table or plan | Don't: As a slide layout on its own
- `ig203` Editable circle and puzzle outlines (icon_set, , 1-99 items): Outline circles, cogs, puzzles and loops to build a diagram | Don't: As a slide layout on its own
- `ig204` Editable chart and pictogram outlines (icon_set, , 1-99 items): Outline bar charts, pictograms, funnels and pyramids | Don't: As a slide layout on its own
- `ig205` Line icon set: business and general (icon_set, , 1-99 items): Line icons for headings, stat_icons and lists (business, retail, communication) | Don't: As a slide layout on its own
- `ig206` Line icon set: education, science, health (icon_set, , 1-99 items): Line icons: education, science, health, tools | Don't: As a slide layout on its own
- `ig207` Line icon set: finance and strategy (icon_set, , 1-99 items): Line icons: finance, money, banking, strategy, charts (best for IB decks) | Don't: As a slide layout on its own
- `ig208` Line icon set: people and jobs (icon_set, , 1-99 items): Line icons: people, faces, professions | Don't: As a slide layout on its own
- `ig209` Line icon set: arts, design, leisure (icon_set, , 1-99 items): Line icons: design, media, entertainment, leisure | Don't: As a slide layout on its own
- `ig210` Line icon set: nature and animals (icon_set, , 1-99 items): Line icons: agriculture, nature, food, animals (ESG, agri deals) | Don't: As a slide layout on its own
- `ig211` Line icon set: digital and social media (icon_set, , 1-99 items): Line icons: digital, SEO, social media logos, devices | Don't: As a slide layout on its own
- `stat_icons` stat icons (layout, kpi_set, 2-8 items): Company at a glance or key numbers, each with a meaningful icon; return drivers in numbers on a thesis page | Don't: More than 8 numbers (use a table); numbers that need a trend (use fin_chart)
- `stat_strip` stat strip (layout, kpi_set, 3-6 items): A row of 3-6 headline numbers under a chart or risk table | Don't: Numbers that need icons to be understood; more than 6 items
- `stat_rings` stat rings (layout, composition, 2-5 items): Shares, margins, utilisation or a debt / equity split shown as % rings | Don't: Values that are not percentages; shares that must add to 100% across many parts (use stacked or pie)
- `hero_number` hero number (layout, kpi_set, 1-1 items): One headline figure (IRR, offer price, EV) with 2-3 supporting points | Don't: Several numbers of equal weight (use stat_icons)
- `pictogram` pictogram (layout, composition, 1-1 items): One share of a population (1 in 4 customers, 35% of capacity) | Don't: Several shares to compare
- `tam_sam_som` tam sam som (layout, hierarchy, 3-3 items): Market sizing from total to serviceable to obtainable market | Don't: A market trend over time (use fin_chart / column)
- `pill_rows` pill rows (layout, list, 3-6 items): Business overview or summary: a short label pill beside 1-2 lines of text per row | Don't: Rows needing long argued paragraphs (use side_tabs)
- `side_tabs` side tabs (layout, list, 3-5 items): Investment thesis pillars: bold claim + evidence -> so what -> implication (35+ words per pillar) | Don't: Short facts or one-liners (use pill_rows); a process (use chevrons)
- `chevrons` chevrons (layout, process, 3-6 items): A sequence or plan (value creation plan, 100-day plan, deal steps), each step with 1-3 bullets | Don't: Items with no order (use pill_rows / stat_icons)
- `timeline` timeline (layout, time_series, 4-8 items): History and milestones (company, policy or market events), or a deal timetable; highlight today | Don't: Fewer than 4 dates; numeric trends (use a chart)
- `numbered_steps` numbered steps (layout, process, 3-6 items): Next steps, diligence plan or workstreams in order | Don't: Steps that need sub-bullets each (use chevrons)
- `hub_spoke` hub spoke (layout, relationship, 4-6 items): Growth drivers or a business model around one centre (the company, the platform) | Don't: A sequence (use chevrons); more than 6 spokes
- `pros_cons` pros cons (layout, comparison, 2-6 items): Strengths vs watch-points, or two sides of a decision | Don't: A full risk register (use risk_matrix)
- `risk_matrix` risk matrix (layout, matrix, 3-6 items): Key risks with a quantified impact, a mitigant + what remains, and a severity Harvey ball | Don't: Fewer than 3 risks; risks with no mitigant
- `harvey` harvey (layout, matrix, 3-10 items): Scoring peers, buyers or options on several criteria (Harvey balls) | Don't: Exact numbers (use a table)
- `logo_row` logo row (layout, comparison, 3-16 items): Peers, buyers, sponsors, customers or tenants as logo tiles (target highlighted) | Don't: Players that need numbers beside them (use a bar chart with the target navy)
- `table` table (layout, comparison, 2-15 items): Labelled numbers that need exact reading: comps, precedents, sources & uses, deal terms, one-way sensitivities (down / base / up), KPI lists with change vs prior period, requirements with detail | Don't: A trend over time (use a chart); ranking many players on one metric (use bar); 3-6 headline numbers with no extra columns (use stat_strip)
- `fin_table` fin table (layout, time_series, 4-20 items): Income statement / cash flow line items in bank format (A / E periods, % rows) | Don't: A one-metric trend (use fin_chart)
- `fin_chart` fin chart (layout, time_series, 4-12 items): One metric's trend with CAGR, actual / estimate split and a % margin strip | Don't: Several unrelated metrics (use fin_table); two forecast cases compared (use bk11); 2-4 metrics or segments each needing its own chart (use bk36)
- `column` column (layout, time_series, 3-12 items): Market size or volumes over time, or a few series side by side | Don't: Shares of a whole (use stacked / rings)
- `bar` bar (layout, comparison, 3-15 items): Ranking players by one metric (target navy, the rest grey) | Don't: A time series (use column); 2-3 scenario values such as a one-way sensitivity down / base / up (use table)
- `stacked` stacked (layout, composition, 2-10 items): Mix over time (revenue by segment, capacity by operator) | Don't: A single-period split (use stat_rings)
- `line` line (layout, time_series, 6-40 items): Prices, rates or indices over many periods | Don't: Fewer than 6 points (use column)
- `football_field` football field (layout, range, 3-8 items): Valuation ranges by method against the offer / current price | Don't: A single point estimate
- `heatmap` heatmap (layout, matrix, 9-49 items): IRR / MOIC or price sensitivity grid on two drivers (red-white-green) | Don't: One-way sensitivities (use a table or tornado)
- `photo` photo (layout, geography, 1-1 items): An asset, site or map photo beside facts (photo + fact strip + chart recipe) | Don't: Decoration with no information
- `map_pins` map pins (layout, geography, 2-6 items): Sites, markets or a corridor on a map, each pinned with a name and one fact (target pin in gold) | Don't: Places with no spatial story (use a table)
- `bullets` bullets (layout, text, 2-6 items): Numbered commentary beside an exhibit: bold lead-in + evidence + so what, 2-6 points | Don't: The main exhibit of a page (pick a chart, table or diagram); more than 2 bullet blocks on one slide
- `takeaway` takeaway (layout, text, 1-1 items): One framing sentence or 'so what' in a dashed outline (Why invest line, page conclusion) | Don't: Lists or several points (use bullets / pill_rows)
- `page_deals` Deal page: full-width table, chart and takeaways (page, comparison, 4-12 items): Precedent transactions or comps: full-width table, a bar of the implied multiple and takeaways | Don't: Fewer than 4 deals (use a table on a mixed page)
- `page_geography` Geography page: labelled map beside a comparison table (page, geography, 2-5 items): Comparing 2-4 places (sites, countries, cities): map with pins and labels beside a metric table + commentary | Don't: A single location; more than ~5 places (use a table)
- `page_landscape` Landscape page: logo wall by segment beside a chart (page, comparison, 6-20 items): Competitive landscape or buyer universe: logos grouped into 3 segments, a scale bar chart beside it | Don't: Fewer than 6 players (use logo_row)
- `page_market` Market page: framing strip over three exhibits (page, comparison, 3-3 items): A market argument: cause on the left, constraint on the right, then 3 exhibits (chart, bar, evidence table) | Don't: Fewer than 3 pieces of evidence (use page_overview)
- `page_overview` Overview page: photo, fact strip, chart and commentary (page, kpi_set, 4-6 items): An asset or market overview: photo with bullets, 5 key numbers across the top, a ranked bar and commentary | Don't: No real photo of the asset (use page_market)
- `page_risks` Risks page: risk matrix beside strengths and watch-points (page, matrix, 3-5 items): Risk section: 3-5 risks with mitigants and severity, strengths vs watch-points on the right | Don't: No mitigants to show
- `page_text` Text page: framing box, two-level bullets, number strip (page, text, 2-2 items): Executive summary or recommendation: dashed framing sentence, two columns of two-level bullets, 4-6 numbers | Don't: Content that can be shown as a chart or diagram
- `page_thesis` Thesis page: side tabs beside pill rows (page, list, 3-5 items): Investment thesis: 3-5 argued pillars with a supporting overview panel | Don't: Short facts only (use pill_rows)
- `bk01` Offer summary table (+ proposal panel) (layout, comparison, 2-6 items): Showing what an offer (or range of prices / exchange ratios) implies | Don't: No offer price yet; one price only (use a stat strip)
- `bk05` Issue to response pairs (layout, comparison, 3-5 items): Answering objections, diligence findings, buyer concerns | Don't: Risks with no answer (use a risk list); pros vs cons of one option
- `bk06` Projections table + numbered commentary (layout, time_series, 4-10 items): Management case or business plan pages | Don't: Historicals only with no story to tell; more than 8 commentary points
- `bk07` Segment table with side tabs + commentary column (layout, time_series, 2-4 items): Segment or business-unit financials with explanation per segment | Don't: Single-segment business; more than 4 segments
- `bk08` Historical | projection split table (layout, time_series, 4-12 items): Any A/E financial summary, UFCF build | Don't: No forecast columns; when a chart tells it faster
- `bk09` Management vs consensus (layout, comparison, 3-8 items): Testing whether the plan is credible | Don't: No broker consensus available
- `bk10` Revision / variance table (layout, comparison, 3-8 items): Updated plan, bid revisions, model changes | Don't: First presentation of a plan (nothing to compare to)
- `bk11` Plan vs street chart grid (layout, comparison, 2-4 items): Two forecast cases (base vs alternative, plan vs street) compared visually: small charts per metric with both cases side by side, e.g. per-share earnings and book value under each case | Don't: Only one forecast case
- `bk13` DCF page (page, time_series, 4-8 items): Any DCF output page | Don't: No cash-flow forecast; summary valuation page (use a football field)
- `bk14` WACC build (layout, list, 5-12 items): Discount rate support page | Don't: Main valuation summary; when WACC is just an input line
- `bk15` Football field + commentary panel (layout, range, 3-7 items): Valuation summary that needs the why behind each bar | Don't: A single method; more than 8 methods
- `bk17` Methodology overview (layout, list, 2-6 items): Explaining which methods were used and why | Don't: Showing the numbers themselves (use a football field)
- `bk18` EV bridge waterfall (layout, bridge, 3-8 items): Showing how value builds up | Don't: No adjustments between EV and equity
- `bk19` Multiples table with mean/median band (layout, matrix, 3-15 items): Trading comps or precedent transactions | Don't: Fewer than 3 peers; when one multiple is the point (use bk21/bk22)
- `bk20` Comps + implied value range (layout, matrix, 3-10 items): Linking multiples to an implied valuation | Don't: No implied value to show
- `bk21` Precedent table with inline bars (layout, matrix, 4-12 items): A table of deals or peers where one multiple, or its change over time (% or x turns), is the point: names in rows, the value drawn as an inline bar per row, median row at the bottom | Don't: Deals or peers with no multiple shown, e.g. EV and premium only (use table); more than 12 rows (use table)
- `bk22` Ranked columns with median line (layout, comparison, 4-12 items): One current operating or valuation metric per peer (a single value each) shown as ranked columns with a median line | Don't: Change in a multiple across peers, in % or x turns (use bk21); the same multiple for 2+ years or bases side by side (use bk32); many metrics at once (use bk32/bk33)
- `bk23` Logo bars + side stats (layout, comparison, 4-10 items): Precedent multiples with who-bought-whom | Don't: No acquirer/target names to show
- `bk24` Column chart + deal table (layout, matrix, 4-10 items): Precedents where the chart and details are both needed | Don't: More than 10 deals (use bk19/bk21)
- `bk25` Premiums paid (layout, range, 2-5 items): Premium analysis | Don't: Private target (no share price)
- `bk26` Price chart with lettered events (layout, time_series, 3-8 items): Share price history with what moved it | Don't: Private target; no events worth flagging
- `bk27` Price chart with callout boxes (layout, time_series, 2-5 items): Trading during a process, reaction to news | Don't: Private target; more than 5 callouts
- `bk28` Price chart + stats side table (layout, time_series, 3-7 items): Share price context for an offer | Don't: Private target
- `bk29` Indexed performance + table (layout, time_series, 2-5 items): Relative share price performance vs peers / index | Don't: Absolute price levels matter more than relative moves
- `bk30` Volume at price (layout, composition, 5-12 items): Shareholder cost base / where stock traded | Don't: Private target; no volume data
- `bk31` Public market overview (page, kpi_set, 4-10 items): Public company snapshot | Don't: Private target
- `bk32` Benchmarking bar matrix (layout, matrix, 3-6 items): Comparing peers on 2-6 metrics at once, or on one multiple across several years / bases (e.g. two forecast years, NTM vs LTM), as a row of bar columns per metric | Don't: One metric (use bk22); more than 8 peers
- `bk33` Peer small multiples (layout, comparison, 2-4 items): Full peer benchmarking page | Don't: One metric (use bk22)
- `bk35` Company comparison matrix (layout, matrix, 3-5 items): Comparing 3-5 entities or precedent deals on attributes | Don't: More than 5 entities; purely numeric comparison (use bk19)
- `bk36` 2x2 chart dashboard (layout, time_series, 3-4 items): Historical / projected summary as 2-4 small charts, one per metric or segment (e.g. revenue, EBITDA, segment EBITDA with CAGRs), or market data in 2-4 panels | Don't: Only one chart worth showing
- `bk37` Company at-a-glance (page, kpi_set, 3-8 items): Overview of a company in one page | Don't: Deep dive on one topic
- `bk38` Wide table + KPI mini charts (layout, time_series, 4-10 items): Financials where 2-3 KPIs need a visual | Don't: No KPIs beyond the P&L
- `bk39` Debt / liquidity profile (page, composition, 3-8 items): Capital structure and refinancing | Don't: Debt-free company
- `bk40` Mix donuts before / after (layout, composition, 2-4 items): Pro forma mix of revenue, geography, debt | Don't: Only one entity (use a single donut)
- `bk41` Market dynamics panels (page, comparison, 3-3 items): Market argument with segments | Don't: Company-specific argument
- `bk42` Sources & uses (+ pro forma cap table) (layout, bridge, 3-10 items): Funding a deal | Don't: No new money raised
- `bk43` LBO summary page (page, kpi_set, 4-4 items): LBO output on one page | Don't: Strategic merger with no sponsor return
- `bk44` Twin sensitivity tables (layout, matrix, 2-2 items): IRR or price sensitivity on two different pairs of drivers | Don't: Only one pair of drivers matters
- `bk45` Accretion / dilution (layout, comparison, 2-5 items): Merger impact on EPS / DPU | Don't: All-cash deal by a private buyer
- `bk46` Credit stats with highlighted ratios (layout, time_series, 4-8 items): Financing impact on leverage / rating | Don't: No new debt
- `bk47` Financing term sheet (layout, list, 1-4 items): Debt package or financing structure | Don't: Single plain loan (one line of text)
- `bk48` Structure options matrix (layout, comparison, 2-4 items): Collars, earn-outs, consideration options | Don't: Only one structure on the table
- `bk49` Buyer funnel with stage counts (layout, process, 3-6 items): Sale process summary | Don't: Process not yet launched
- `bk50` Calendar timeline (layout, process, 1-3 items): Process timetable with specific dates | Don't: Timeline longer than 3 months (use bk51)
- `bk51` Gantt timeline (layout, process, 4-12 items): Process or integration plan | Don't: Only 3-4 steps (use bk52)
- `bk52` Phase arrows with columns (layout, process, 3-5 items): Process phases with what happens in each | Don't: Exact dates matter (use bk50/bk51)
- `bk55` Buyer profiles table (layout, matrix, 2-6 items): Potential buyers list | Don't: Long buyer list with no detail (use a table)
- `bk57` Two-case comparison (layout, comparison, 2-2 items): Case studies, two scenarios | Don't: More than two cases
- `bk58` Headed box columns (layout, list, 2-6 items): Company overview detail lists | Don't: A single list (use bullets)

## Rows
```json
[
 {
  "row": "sg_dc_s01_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\sg_dc_s01_b1_j2.jpg",
  "has_page": true,
  "section": "market",
  "message": "Asia's premium data centre hub, running at over 95% occupancy",
  "exhibit": "Key market metrics",
  "data_type": "kpi_set",
  "about": "headline numbers: live capacity, upcoming capacity, occupancy, rent, electricity share",
  "content": [
   "821MW live capacity",
   "247.5MW under construction or announced",
   ">95% occupancy",
   "US$330-475 rent per kW per month",
   "~7% share of national electricity"
  ],
  "same_page": [
   {
    "row": "sg_dc_s01_b2",
    "exhibit": "Live capacity by market vs APAC peers",
    "content": [
     "Shanghai 1286",
     "Tokyo 1086",
     "Sydney 950"
    ]
   },
   {
    "row": "sg_dc_s01_b3",
    "exhibit": "Singapore at a glance (with a photo)",
    "content": [
     "Anchor hub: 821MW live on a 744km2 island",
     "Near-full: occupancy above 95%",
     "Premium pricing: highest rents in APAC"
    ]
   },
   {
    "row": "sg_dc_s01_b4",
    "exhibit": "What sets Singapore apart",
    "content": [
     "28 subsea cables, 13 more planned",
     "AWS S$12bn more to 2028",
     "Listed DC REITs plus platform buyers"
    ]
   }
  ],
  "candidates": [
   "table",
   "ig177",
   "stat_icons",
   "bk31",
   "stat_strip"
  ]
 },
 {
  "row": "sg_dc_s02_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\sg_dc_s02_b1_j2.jpg",
  "has_page": true,
  "section": "market",
  "message": "Cloud and AI demand far outruns what Singapore can add",
  "exhibit": "Demand accelerating vs supply capped",
  "data_type": "comparison",
  "about": "two sides: demand drivers against supply constraints, cause and constraint framing",
  "content": [
   "Big Tech capex +61% in 2026",
   "Hyperscale demand +14% a year",
   "Pipeline thin: 247.5MW vs 821MW",
   "Capacity only by tender: 80MW 2023, 200MW 2026"
  ],
  "same_page": [
   {
    "row": "sg_dc_s02_b2",
    "exhibit": "Big Tech AI spend plans 2026 (US$bn)",
    "content": [
     "Amazon 200",
     "Google 180",
     "ByteDance 23"
    ]
   },
   {
    "row": "sg_dc_s02_b3",
    "exhibit": "Live vs upcoming capacity by market (MW)",
    "content": []
   },
   {
    "row": "sg_dc_s02_b4",
    "exhibit": "Recent commitments to Singapore",
    "content": [
     "AWS S$12bn to 2028",
     "Digital Realty S$4.3bn Apr 2026",
     "DC-CFA2 200MW Aug 2026"
    ]
   }
  ],
  "candidates": [
   "ig061",
   "table",
   "bar",
   "page_market",
   "pros_cons",
   "bk33",
   "bk22",
   "bullets"
  ]
 },
 {
  "row": "sg_dc_s03_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\sg_dc_s03_b1_j2.jpg",
  "has_page": true,
  "section": "market",
  "message": "Power and land, not demand, cap new supply",
  "exhibit": "From moratorium to controlled allocation",
  "data_type": "time_series",
  "about": "policy history milestones and dates from 2019 moratorium to 2026 awards",
  "content": [
   "2019 moratorium",
   "Jul 2022 pilot DC-CFA",
   "Jul 2023 80MW awarded",
   "May 2024 Green DC Roadmap",
   "Oct 2025 Jurong Island park",
   "Dec 2025 DC-CFA2 launched",
   "Aug 2026 DC-CFA2 awarded"
  ],
  "same_page": [
   {
    "row": "sg_dc_s03_b2",
    "exhibit": "Entry bar for new capacity (DC-CFA2)",
    "content": [
     "Green energy >=50% from green pathways",
     "PUE 1.25 or better",
     "Green Mark Platinum"
    ]
   },
   {
    "row": "sg_dc_s03_b3",
    "exhibit": "Capacity released by policy vs live stock (MW)",
    "content": [
     "Live 821",
     "Jurong Island 700",
     "DC-CFA2 200"
    ]
   }
  ],
  "candidates": [
   "column",
   "ig125",
   "line",
   "fin_table",
   "bk26",
   "timeline"
  ]
 },
 {
  "row": "sg_dc_s04_b2",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\sg_dc_s04_b2_j2.jpg",
  "has_page": true,
  "section": "market",
  "message": "Overflow demand is moving to Johor and Batam",
  "exhibit": "Singapore vs its overflow markets",
  "data_type": "comparison",
  "about": "metrics across three markets: capacity, growth, cap rate, role",
  "content": [],
  "same_page": [
   {
    "row": "sg_dc_s04_b1",
    "exhibit": "The Singapore-Johor-Batam corridor",
    "content": [
     "Johor 476MW live, 2,500MW+ upcoming",
     "Singapore 821MW live, 247.5MW upcoming",
     "Batam NDP1 24MW, up to 144MW"
    ]
   },
   {
    "row": "sg_dc_s04_b3",
    "exhibit": "Where the next wave of capacity goes",
    "content": []
   }
  ],
  "candidates": [
   "ig184",
   "ig102",
   "ig067",
   "logo_row",
   "bk35",
   "table"
  ]
 },
 {
  "row": "sg_dc_s05_b3",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\sg_dc_s05_b3_j2.jpg",
  "has_page": true,
  "section": "market",
  "message": "A concentrated field of global operators and hyperscalers",
  "exhibit": "Owners and capital",
  "data_type": "comparison",
  "about": "players named with logos, one of three groups",
  "content": [
   "Keppel DC REIT",
   "Digital Core REIT",
   "CapitaLand",
   "KKR",
   "Blackstone"
  ],
  "same_page": [
   {
    "row": "sg_dc_s05_b1",
    "exhibit": "Colocation operators",
    "content": [
     "Equinix",
     "Digital Realty",
     "STT GDC"
    ]
   },
   {
    "row": "sg_dc_s05_b2",
    "exhibit": "Hyperscalers and cloud",
    "content": [
     "Google",
     "Microsoft",
     "AWS"
    ]
   },
   {
    "row": "sg_dc_s05_b4",
    "exhibit": "Selected flagship facilities (MW IT load)",
    "content": [
     "AirTrunk SGP1 78",
     "Nxera Tuas 58",
     "Digital Realty SIN12 50"
    ]
   },
   {
    "row": "sg_dc_s05_b5",
    "exhibit": "How competition works",
    "content": []
   }
  ],
  "candidates": [
   "table",
   "bk05",
   "page_landscape",
   "harvey",
   "logo_row",
   "pros_cons"
  ]
 },
 {
  "row": "sg_dc_s06_b2",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\sg_dc_s06_b2_j2.jpg",
  "has_page": true,
  "section": "market",
  "message": "Scarcity gives Singapore the highest rents in the region",
  "exhibit": "Cost to build and run in Singapore",
  "data_type": "comparison",
  "about": "build cost, power price, green requirement, PUE with context",
  "content": [],
  "same_page": [
   {
    "row": "sg_dc_s06_b1",
    "exhibit": "Colocation asking rents (US$/kW/month)",
    "content": [
     "Singapore 403",
     "Hong Kong 295",
     "Tokyo 280"
    ]
   },
   {
    "row": "sg_dc_s06_b4",
    "exhibit": "What it means for owners",
    "content": []
   }
  ],
  "candidates": [
   "ig102",
   "ig067",
   "table",
   "ig184",
   "logo_row"
  ]
 },
 {
  "row": "sg_dc_s07_b3",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\sg_dc_s07_b3_j2.jpg",
  "has_page": true,
  "section": "valuation",
  "message": "Capital keeps paying up for scarce APAC platforms and assets",
  "exhibit": "Takeaways",
  "data_type": "text",
  "about": "assets rarely trade, platforms largest cheques, record capital, recycling wave",
  "content": [],
  "same_page": [
   {
    "row": "sg_dc_s07_b1",
    "exhibit": "Selected APAC data centre transactions 2024-26",
    "content": []
   },
   {
    "row": "sg_dc_s07_b2",
    "exhibit": "Price per MW, asset deals (US$m)",
    "content": []
   }
  ],
  "candidates": [
   "takeaway",
   "bullets",
   "bk17",
   "pill_rows",
   "ig157",
   "bk47"
  ]
 },
 {
  "row": "sg_dc_s09_b2",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\sg_dc_s09_b2_j2.jpg",
  "has_page": true,
  "section": "thesis",
  "message": "Own scarce, powered capacity; grow through the corridor",
  "exhibit": "Why invest framing line",
  "data_type": "text",
  "about": "one framing sentence: why invest, the play",
  "content": [],
  "same_page": [
   {
    "row": "sg_dc_s09_b1",
    "exhibit": "Investment thesis pillars",
    "content": []
   },
   {
    "row": "sg_dc_s09_b3",
    "exhibit": "Return drivers in numbers",
    "content": [
     "30% pipeline/live",
     ">95% occupancy",
     "~10% / ~51% reversion"
    ]
   }
  ],
  "candidates": [
   "bk47",
   "takeaway",
   "bullets",
   "ig006",
   "ig157",
   "page_text"
  ]
 },
 {
  "row": "rp_004_022_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_004_022_b1_j2.jpg",
  "has_page": true,
  "section": "market",
  "message": "Combined company is more diversified with a comparable asset mix",
  "exhibit": "Industry mix",
  "data_type": "composition",
  "about": "combined company industry shares",
  "content": [
   "Technology",
   "Pharmaceuticals",
   "Real Estate",
   "Insurance",
   "Aerospace and Defense",
   "Wholesale",
   "Other"
  ],
  "same_page": [
   {
    "row": "rp_004_022_b2",
    "exhibit": "Investment type",
    "content": [
     "First Lien",
     "Second Lien",
     "Equity"
    ]
   }
  ],
  "candidates": [
   "stacked",
   "ig044",
   "ig015",
   "bk40",
   "logo_row",
   "ig178"
  ]
 },
 {
  "row": "rp_085_010_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_085_010_b1_j2.jpg",
  "has_page": true,
  "section": "process",
  "message": "Advisor proposes next steps to evaluate the opportunity",
  "exhibit": "Potential next steps",
  "data_type": "list",
  "about": "steps to evaluate transaction",
  "content": [
   "Discuss and agree terms of engagement",
   "Review potential transaction with Napa in context of corporate strategy",
   "Perform due diligence and preliminary valuation analysis",
   "Reconvene with Special Committee to discuss next steps"
  ],
  "same_page": [],
  "candidates": [
   "ig108",
   "pill_rows",
   "ig111",
   "ig006",
   "ig188",
   "numbered_steps",
   "ig119"
  ]
 },
 {
  "row": "rp_013_025_b2",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_013_025_b2_j2.jpg",
  "has_page": true,
  "section": "company",
  "message": "Three alternatives weighed on benefits and considerations",
  "exhibit": "Key issues addressed",
  "data_type": "matrix",
  "about": "wholesale customers, governance, liquidity",
  "content": [
   "Wholesale Customers",
   "Governance / Ownership",
   "Liquidity",
   "Solution to key issues? Provides additional time"
  ],
  "same_page": [
   {
    "row": "rp_013_025_b1",
    "exhibit": "Alternatives comparison",
    "content": [
     "I. Sale to Shepherd: realizable value; Shepherd assumes obligations; eliminates key risks",
     "II. Sale of Spectrum to Dalmatian: net proceeds address funding gap; likely permits refinancing",
     "III. Chapter 11 Restructuring: addresses capital structure; highly uncertain outcome; equity recovery uncertain"
    ]
   }
  ],
  "candidates": [
   "harvey",
   "logo_row",
   "ig040",
   "table",
   "bk35"
  ]
 },
 {
  "row": "rp_108_004_b3",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_108_004_b3_j2.jpg",
  "has_page": true,
  "section": "company",
  "message": "Revised proposal offers $13.25 per share with committed financing",
  "exhibit": "Diligence and timing",
  "data_type": "text",
  "about": "approval and signing timeline",
  "content": [
   "Approved by NMC investment committee",
   "Prepared to sign by July 12, 2024",
   "Discuss management rollover if approved by Special Committee"
  ],
  "same_page": [
   {
    "row": "rp_108_004_b1",
    "exhibit": "Price",
    "content": [
     "$13.25 per share",
     "30.3% premium to closing price of $10.17 on Jan 25, 2024",
     "31.6% premium to 30-day VWAP of $10.07"
    ]
   },
   {
    "row": "rp_108_004_b2",
    "exhibit": "Equity and debt financing",
    "content": [
     "Recapitalization with new third-party debt from Goldman Sachs and JPMorgan",
     "Equity from rollover of NMC existing 32% stake and new cash equity",
     "Customer stockholders invited to roll or increase investment"
    ]
   }
  ],
  "candidates": [
   "bk58",
   "pill_rows",
   "side_tabs",
   "bk17",
   "table",
   "bullets"
  ]
 },
 {
  "row": "rp_091_006_b2",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_091_006_b2_j2.jpg",
  "has_page": true,
  "section": "process",
  "message": "Wide outreach narrowed to one final bid",
  "exhibit": "Process summary",
  "data_type": "text",
  "about": "process headline",
  "content": [
   "Over 70 potential buyers contacted",
   "36 parties received Overview Presentation",
   "6 submitted initial bid",
   "1 submitted final bid",
   "Public announcement February 9, 2015"
  ],
  "same_page": [
   {
    "row": "rp_091_006_b1",
    "exhibit": "Buyer funnel by stage",
    "content": [
     "Contacted: Strategic 11, Financial 60",
     "Signed NDA and received OP: 4 and 32",
     "1st round bid: 2 and 4"
    ]
   }
  ],
  "candidates": [
   "bullets",
   "table",
   "takeaway",
   "ig006",
   "bk49",
   "ig107",
   "pill_rows"
  ]
 },
 {
  "row": "rp_080_023_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_080_023_b1_j2.jpg",
  "has_page": true,
  "section": "valuation",
  "message": "Offer value rises with Luna stock price, incl. synergies",
  "exhibit": "Offer sensitivity to Luna stock price",
  "data_type": "matrix",
  "about": "price $15-$25 vs offer metrics",
  "content": [
   "Luna price $15 to $25",
   "Premium/(discount) (29.4%) to 17.6%",
   "Exchange ratio 0.566x",
   "Stock value per share $8.24 to $13.73",
   "Cash per share $20.00",
   "Value pre-synergies $28.24 to $33.73",
   "PV of synergies $881mm",
   "Synergies per share $2.15",
   "Value incl. synergies $30.39 to $35.88",
   "Premium to Saturn price 16.8% to 37.9%"
  ],
  "same_page": [],
  "candidates": [
   "bk01",
   "table",
   "bk19",
   "bk21",
   "bk20",
   "bk24",
   "heatmap"
  ]
 },
 {
  "row": "rp_072_012_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_072_012_b1_j2.jpg",
  "has_page": true,
  "section": "valuation",
  "message": "Value per share ranges $65 to $106 vs $68.73 current price",
  "exhibit": "Equity value per share by method",
  "data_type": "range",
  "about": "football field of per-share values",
  "content": [
   "Publicly-traded comparables 20.0x-23.0x 2008E EPS",
   "Precedent transactions",
   "DCF 9.5-10.5% WACC, 3.0-3.5% growth",
   "Sum of the parts",
   "LBO 67% leverage, 18-22% return",
   "LBO 62% leverage",
   "Upside case $65.00 - $106.50",
   "Current price $68.73"
  ],
  "same_page": [],
  "candidates": [
   "bk15",
   "football_field",
   "table",
   "bk22",
   "bk09"
  ]
 },
 {
  "row": "rp_001_016_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_001_016_b1_j2.jpg",
  "has_page": true,
  "section": "financials",
  "message": "GPP projections show growing EBITDA and flat $1.82 distribution",
  "exhibit": "EBITDA by segment",
  "data_type": "time_series",
  "about": "2023E-2027E segments stacked",
  "content": [
   "Storage",
   "MVC",
   "Blendstar",
   "Logistics",
   "Trucking",
   "NLR",
   "Corporate",
   "EBITDA axis $10 to $70"
  ],
  "same_page": [
   {
    "row": "rp_001_016_b2",
    "exhibit": "LP distribution per unit",
    "content": [
     "2023E 1.82",
     "2024E 1.82",
     "2025E 1.82"
    ]
   }
  ],
  "candidates": [
   "bk06",
   "bk36",
   "bk08",
   "fin_table",
   "column",
   "stacked",
   "line"
  ]
 },
 {
  "row": "rp_006_003_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_006_003_b1_j2.jpg",
  "has_page": true,
  "section": "valuation",
  "message": "TLP traded in line with AMZ since undisturbed date",
  "exhibit": "Relative price performance",
  "data_type": "time_series",
  "about": "TLP vs AMZ over 5, 10, 20, 30 days",
  "content": [
   "5-day: AMZ 1.6%",
   "10-day, 20-day and 30-day indexed to 100%",
   "Range 97.5% to 105.0%"
  ],
  "same_page": [
   {
    "row": "rp_006_003_b2",
    "exhibit": "Price performance tracker",
    "content": [
     "Date 7/10/18 to 8/13/18",
     "Prices $38.49, $38.20, $38.65, $39.61, $39.95",
     "Offer $38.00"
    ]
   }
  ],
  "candidates": [
   "bk29",
   "bk28",
   "line",
   "bk27",
   "bk26",
   "column"
  ]
 },
 {
  "row": "rp_039_049_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_039_049_b1_j2.jpg",
  "has_page": true,
  "section": "process",
  "message": "Diamond benchmarked against smaller and larger peer universes",
  "exhibit": "Peer trading comparables",
  "data_type": "matrix",
  "about": "multiples, growth, leverage and yield by peer",
  "content": [
   "Diamond FCF yield 3.52%",
   "Smaller: Ashland, Avient, ChampionX, Fuller, Ingevity, Innospec, ISS, Sensient, Stepan",
   "Larger: DuPont, Eastman, Entegris, Sherwin-Williams, Sodexo",
   "EV/EBITDA 2022E 8.8x-19.9x",
   "Sales CAGR 22E-24E 3.0%-6.9%",
   "Leverage 2022E 0.6x-5.3x",
   "Dividend yield 0.6%-3.8%"
  ],
  "same_page": [],
  "candidates": [
   "harvey",
   "bk20",
   "bk55",
   "table",
   "bk19"
  ]
 },
 {
  "row": "rp_000_007_b2",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_000_007_b2_j2.jpg",
  "has_page": true,
  "section": "financials",
  "message": "Margins expand to about 12.5% by FY2028 on stable growth",
  "exhibit": "Commentary",
  "data_type": "text",
  "about": "margin and capex drivers",
  "content": [
   "Gross margin declines then stable",
   "FY24E EBITDA margin dips on G&A and R&D",
   "Margin compression FY29E-FY34E about 60bps from revenue mix",
   "Capex supports continued investment"
  ],
  "same_page": [
   {
    "row": "rp_000_007_b1",
    "exhibit": "Projections summary",
    "content": [
     "Years FY22A to FY34E",
     "Gross margin 55.5% FY24 to 54.3% FY28",
     "EBITDA margin about 12.5% by FY2028"
    ]
   }
  ],
  "candidates": [
   "bk06",
   "bullets",
   "table",
   "fin_table",
   "bk07",
   "bk36"
  ]
 },
 {
  "row": "rp_012_007_b2",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_012_007_b2_j2.jpg",
  "has_page": true,
  "section": "financials",
  "message": "Liquidity fell before bankruptcy and emergence liquidity should be sized at roughly 15-45% of LTM revenue",
  "exhibit": "Emergence liquidity sensitivity",
  "data_type": "matrix",
  "about": "liquidity by LTM revenue and % of revenue",
  "content": [
   "LTM revenue $3,075 to $3,275mm",
   "12.5% of revenue: $384 / $391 / $397 / $403 / $409",
   "15.0%: 461 / 469 / 476 / 484 / 491",
   "17.5%: 538 / 547 / 556 / 564 / 573",
   "20.0%: 615 / 625 / 635 / 645 / 655",
   "22.5%: 692 / 703 / 714 / 726 / 737"
  ],
  "same_page": [
   {
    "row": "rp_012_007_b1",
    "exhibit": "Historical liquidity",
    "content": [
     "2011 $539",
     "2012 $449",
     "2013 $852"
    ]
   }
  ],
  "candidates": [
   "bk09",
   "table",
   "bk32",
   "bk55",
   "bk44",
   "heatmap",
   "bk19"
  ]
 },
 {
  "row": "rp_113_013_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_113_013_b1_j2.jpg",
  "has_page": true,
  "section": "process",
  "message": "13 parties contacted narrowed to few proposals with most recent price indications of $28-31",
  "exhibit": "Process funnel",
  "data_type": "process",
  "about": "parties by stage",
  "content": [
   "Parties contacted 13",
   "NDA signed / initial meeting",
   "Preliminary proposal submitted (verbal)",
   "Post due diligence",
   "Other parties that reached or declined"
  ],
  "same_page": [
   {
    "row": "rp_113_013_b2",
    "exhibit": "Most recent price indication",
    "content": [
     "Party A $28",
     "Party B $31",
     "Party C $30"
    ]
   }
  ],
  "candidates": [
   "numbered_steps",
   "bk51",
   "bk52",
   "table",
   "chevrons",
   "bk49"
  ]
 },
 {
  "row": "rp_104_028_b2",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_104_028_b2_j2.jpg",
  "has_page": true,
  "section": "structure",
  "message": "Lunar financing package provides $3,720mm funded debt and $4,570mm commitments at 4.79% base cost",
  "exhibit": "Summary cost",
  "data_type": "kpi_set",
  "about": "blended financing metrics",
  "content": [
   "WAM 6.6 years",
   "WACD base case 4.79%",
   "Flex 6.61%",
   "Structure flex 6.95%",
   "Total financing fees $69.2mm"
  ],
  "same_page": [
   {
    "row": "rp_104_028_b1",
    "exhibit": "Financing facility terms",
    "content": [
     "Revolver $1,000mm, 5 years, L+250",
     "Term Loan A $1,000mm, 5 years, L+250",
     "Term Loan B $1,900mm, 7 years, L+375, floor 0.75%, OID 99"
    ]
   }
  ],
  "candidates": [
   "stat_strip",
   "bk37",
   "bk43",
   "bk47",
   "table",
   "bk31"
  ]
 },
 {
  "row": "rp_092_009_b2",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_092_009_b2_j2.jpg",
  "has_page": true,
  "section": "process",
  "message": "71 buyers contacted led to six initial bids and one final bid",
  "exhibit": "Public announcement",
  "data_type": "text",
  "about": "timing note",
  "content": [
   "Strategic alternatives process made public on February 9, 2015"
  ],
  "same_page": [
   {
    "row": "rp_092_009_b1",
    "exhibit": "Process funnel by buyer type",
    "content": [
     "Contacted: Strategic 11, Financial 60, total 71",
     "Signed NDA and received OP: Strategic 4, Financial 32, total 36",
     "1st round bids: Strategic 2, Financial 4, total 6"
    ]
   }
  ],
  "candidates": [
   "bk50",
   "table",
   "bk47",
   "takeaway",
   "bullets"
  ]
 },
 {
  "row": "rp_001_023_b2",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_001_023_b2_j2.jpg",
  "has_page": true,
  "section": "process",
  "message": "Take-private could close about 24 weeks after offer submission",
  "exhibit": "Calendar",
  "data_type": "list",
  "about": "May to October calendar",
  "content": [
   "Months May to October",
   "Markers: NYSE holiday, expected earnings release, GPRE or GPP event"
  ],
  "same_page": [
   {
    "row": "rp_001_023_b1",
    "exhibit": "Event timeline",
    "content": [
     "Week 1 GPRE submits offer to GPP board",
     "Week 1 GPP forms conflicts committee and engages advisors",
     "Week 2 GPRE presents to conflicts committee"
    ]
   }
  ],
  "candidates": [
   "bk17",
   "table",
   "ig131",
   "ig006",
   "bk47",
   "bk50"
  ]
 },
 {
  "row": "rp_028_007_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_028_007_b1_j2.jpg",
  "has_page": true,
  "section": "valuation",
  "message": "Valuation methods centre on $30-37 per share around the $36 offer",
  "exhibit": "Equity valuation per share",
  "data_type": "range",
  "about": "football field by methodology",
  "content": [
   "Comparable company analysis",
   "Comparable transaction",
   "Discounted cash flow",
   "52 week high / low",
   "Research analyst price target",
   "Offer $36.00 ($10,948mm)"
  ],
  "same_page": [
   {
    "row": "rp_028_007_b2",
    "exhibit": "Other metrics",
    "content": [
     "CY2004 PF EBITDA multiples 7.3x-10.8x",
     "CY2005 EBITDA multiples 17x-18.8x",
     "CY2004 PF net income multiples"
    ]
   }
  ],
  "candidates": [
   "football_field",
   "bk15",
   "bk25",
   "table",
   "bk22"
  ]
 },
 {
  "row": "rp_032_008_b2",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_032_008_b2_j2.jpg",
  "has_page": true,
  "section": "financials",
  "message": "Case 1 and Case 2 differ in premium growth, underwriting profit and EPS",
  "exhibit": "TBVPS and operating EPS",
  "data_type": "time_series",
  "about": "per-share returns 2014-2022E",
  "content": [
   "Operating EPS CAGR 2016-22: 10.6%",
   "TBVPS growth 2015A-2022E",
   "Operating EPS $470"
  ],
  "same_page": [
   {
    "row": "rp_032_008_b1",
    "exhibit": "Gross written premiums and underwriting profit",
    "content": [
     "GWP CAGR 2017-22: 32%",
     "Underwriting profit $10mm in 2019E, $212mm in 2020E",
     "Combined ratio 90.8%, loss ratio 66.0%"
    ]
   }
  ],
  "candidates": [
   "bk11",
   "bk26",
   "fin_table",
   "bk36",
   "bk07",
   "column"
  ]
 },
 {
  "row": "rp_003_008_b2",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_003_008_b2_j2.jpg",
  "has_page": true,
  "section": "valuation",
  "message": "Neon trades well below IPO price with a $21.79 unaffected price and wide 52-week range",
  "exhibit": "Market statistics",
  "data_type": "matrix",
  "about": "averages and premium to unaffected",
  "content": [
   "Price $31.64",
   "52W high $43.77, 101% premium",
   "52W low $13.35, (39%)",
   "30-day avg $24.43",
   "1-year avg $26.41",
   "2-year avg $32.05, 49%",
   "3-year avg $49.41, 127%",
   "Basic shares 149.7mm",
   "Equity value $3,261mm"
  ],
  "same_page": [
   {
    "row": "rp_003_008_b1",
    "exhibit": "Stock price since IPO",
    "content": [
     "IPO price $26.00",
     "Peak around $43.77",
     "Low $13.35"
    ]
   }
  ],
  "candidates": [
   "bk19",
   "bk28",
   "heatmap",
   "table",
   "stat_strip",
   "bk24",
   "bk20"
  ]
 },
 {
  "row": "rp_082_009_b2",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_082_009_b2_j2.jpg",
  "has_page": true,
  "section": "financials",
  "message": "Management forecast shows capex shifting to Renewables with EBITDA and EPS growth to 2035",
  "exhibit": "Adj. net income and EBITDA",
  "data_type": "time_series",
  "about": "consolidated EBITDA 2024E-2035E",
  "content": [
   "EBITDA $5.1 2024E, $5.2, $4.9",
   "Networks EBITDA CAGR 6.8% through 2035E",
   "Renewables EBITDA ~$10 bn through 2035 with $24 bn+ capex"
  ],
  "same_page": [
   {
    "row": "rp_082_009_b1",
    "exhibit": "Capex and FFO/Debt",
    "content": [
     "2024E $5.2 capex, FFO/Debt 12.3%",
     "2025E $5.0, 12.1%",
     "2027E 10.6%"
    ]
   },
   {
    "row": "rp_082_009_b3",
    "exhibit": "Adj. EPS",
    "content": [
     "2024E $2.28",
     "2025E $2.47",
     "2026E $2.60"
    ]
   }
  ],
  "candidates": [
   "bk06",
   "bk36",
   "stacked",
   "bk07",
   "column",
   "fin_table"
  ]
 },
 {
  "row": "rp_039_044_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_039_044_b1_j2.jpg",
  "has_page": true,
  "section": "financials",
  "message": "Management forecast shows sales growing to about $3.1bn by 2027E with improving margins",
  "exhibit": "Historical and forecast financials",
  "data_type": "matrix",
  "about": "P&L, cash flow items and leverage 2019A-2027E",
  "content": [
   "Net sales 2020A $2,013, 2022LE $2,100, 2024E $2,544, 2025E $2,721, 2027E $3,120",
   "Gross profit margin about 40-43%",
   "EBITDA 2024E $522.7, 2025E $583, 2027E $717.5",
   "Capex about -$34.5 to -$36",
   "Unlevered CF 2027E $267",
   "CAGR 23E-27E 7.0%"
  ],
  "same_page": [],
  "candidates": [
   "bk19",
   "bk08",
   "fin_table",
   "bk32",
   "table",
   "bk09"
  ]
 },
 {
  "row": "rp_121_013_b3",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_121_013_b3_j2.jpg",
  "has_page": true,
  "section": "company",
  "message": "Low leverage of 30.0% and 5.9x interest coverage show a conservative capital structure",
  "exhibit": "Sensitivity on ICR: 100 bps change in interest rate",
  "data_type": "range",
  "about": "ICR under rate change",
  "content": [
   "Decrease 8.6",
   "Base Case 5.9",
   "Increase 4.4"
  ],
  "same_page": [
   {
    "row": "rp_121_013_b1",
    "exhibit": "Key capital management metrics",
    "content": [
     "Aggregate Leverage 30.0% (-20 bps)",
     "Average Cost of Debt 3.0% (-10 bps)",
     "Weighted Average Debt Tenor 3.1 years"
    ]
   },
   {
    "row": "rp_121_013_b2",
    "exhibit": "Sensitivity on ICR: 10% change in EBITDA",
    "content": [
     "Decrease 5.3",
     "Base Case 5.9",
     "Increase 6.4"
    ]
   }
  ],
  "candidates": [
   "stat_strip",
   "football_field",
   "bar",
   "bk15",
   "bk25",
   "table"
  ]
 },
 {
  "row": "rp_071_008_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_071_008_b1_j2.jpg",
  "has_page": true,
  "section": "process",
  "message": "Special committee should run a market-shop process with equal information for all bidders",
  "exhibit": "Management and sponsor buyout path",
  "data_type": "process",
  "about": "steps from sponsor talks to proposal",
  "content": [
   "Management discusses potential buyout with select financial sponsors (Colony Capital, Providence, TPG, Whitehall)",
   "Management and sponsors subject to standstill agreements",
   "Company gives sponsors data room access",
   "Receive and negotiate definitive acquisition proposal",
   "Negotiate fully-committed financing with backstop bridge facility",
   "Proposals not subject to due diligence contingency"
  ],
  "same_page": [
   {
    "row": "rp_071_008_b2",
    "exhibit": "Market shop and announcement",
    "content": [
     "Contract terms provide market shop period and low break-up fees",
     "Publicly announce company will seek better offers",
     "Management stays one year post acquisition"
    ]
   }
  ],
  "candidates": [
   "bk51",
   "ig121",
   "chevrons",
   "ig111",
   "numbered_steps",
   "bk52"
  ]
 },
 {
  "row": "rp_032_011_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_032_011_b1_j2.jpg",
  "has_page": true,
  "section": "valuation",
  "message": "Valuation uses trading, dividend discount, precedent and market-perspective methods on Case 1 and Case 2",
  "exhibit": "Valuation methodologies considered",
  "data_type": "matrix",
  "about": "method versus description",
  "content": [
   "Public trading multiples: P/E, P/BV, P/TBV vs peers; regression of P/BV to ROE; applied to consensus estimates",
   "Dividend discount model: future dividends and terminal equity value, cost of equity discount rate; sum-of-the-parts for Tecmo",
   "Precedent insurance transactions: multiples paid in change of control deals, similar business mix",
   "Precedent minority squeeze-out premia vs undisturbed price",
   "Public market performance: current and recent stock price, analyst price targets"
  ],
  "same_page": [
   {
    "row": "rp_032_011_b2",
    "exhibit": "Peer set note",
    "content": [
     "Peers: AFG, CNA, JRVR, NAVG, PRA, THG, WRB and others"
    ]
   }
  ],
  "candidates": [
   "bk17",
   "risk_matrix",
   "bk20",
   "harvey",
   "bk35",
   "side_tabs",
   "table"
  ]
 },
 {
  "row": "rp_068_021_b2",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_068_021_b2_j2.jpg",
  "has_page": true,
  "section": "valuation",
  "message": "Pro forma UGI share price and accretion vary with P/E multiple and equity financing share of the buy-in",
  "exhibit": "Accretion / (dilution) to current price $54.02",
  "data_type": "matrix",
  "about": "accretion by multiple and financing",
  "content": [
   "2019E 65% equity: 3%, (1%), (7%)",
   "75%: 9%, (2%), (7%)",
   "85%: (2%), (8%)",
   "2020E 65% equity: 7%, 3%, (5%), (11%)",
   "75%: 6%, 3%, (6%), (12%)",
   "85%: 6%, 2%, (6%), (12%)"
  ],
  "same_page": [
   {
    "row": "rp_068_021_b1",
    "exhibit": "Pro forma share price 2019E and 2020E EPS multiples",
    "content": [
     "2019E P/E 20.0x 18.8x 18.0x 17.0x by 65%, 75%, 85% equity",
     "65% equity: $59.23, $55.68, $53.20, $50.84",
     "85% equity: $57.07, $55.33, $50.73, $47.56"
    ]
   }
  ],
  "candidates": [
   "bk32",
   "bk20",
   "bk24",
   "bk19",
   "bk44",
   "heatmap",
   "table"
  ]
 },
 {
  "row": "rp_084_007_b2",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_084_007_b2_j2.jpg",
  "has_page": true,
  "section": "company",
  "message": "Empire's Board moved from gaming collaboration to hiring Moelis and forming a Special Committee in 2019",
  "exhibit": "Background on advisor role",
  "data_type": "text",
  "about": "Moelis advisory note",
  "content": [
   "Moelis was financial advisor to Empire on the bet365 agreement"
  ],
  "same_page": [
   {
    "row": "rp_084_007_b1",
    "exhibit": "Key dates for Project Bald Eagle",
    "content": [
     "Nov 14, 2018: sportsbook and digital gaming collaboration with bet365 affiliate",
     "Mar 12, 2019: Board discussed industry trends, projections, capital structure options",
     "Mar 12, 2019: Board discussed illustrative OPCO / PropCo structure"
    ]
   }
  ],
  "candidates": [
   "table",
   "bullets",
   "ig157",
   "timeline",
   "takeaway",
   "bk47"
  ]
 },
 {
  "row": "rp_115_010_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_115_010_b1_j2.jpg",
  "has_page": true,
  "section": "valuation",
  "message": "Software peers trade at median 3.5x to 8.6x revenue depending on SaaS, application or infrastructure model",
  "exhibit": "Enterprise value ($MM)",
  "data_type": "comparison",
  "about": "EV by software company",
  "content": [
   "VMW 37,845",
   "CRM 17,495",
   "ADBE 16,977",
   "CTXS 11,359",
   "BMC 7,940",
   "RHT 7,317",
   "TDC 7,251",
   "Autonomy 5,728",
   "INFA 4,502",
   "Software AG 4,312",
   "TIBX 4,001",
   "OTEX 2,648",
   "CNQR 2,454",
   "SFSF 2,180",
   "QLIK 1,886",
   "PRGS 1,743"
  ],
  "same_page": [
   {
    "row": "rp_115_010_b2",
    "exhibit": "EV / Revenue (CY11E)",
    "content": [
     "VMW 11.1x",
     "CRM 8.6x",
     "SFSF 8.6x"
    ]
   }
  ],
  "candidates": [
   "table",
   "line",
   "logo_row",
   "bk33",
   "bk22",
   "heatmap",
   "bar"
  ]
 },
 {
  "row": "rp_107_004_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_107_004_b1_j2.jpg",
  "has_page": true,
  "section": "process",
  "message": "Pacific ran a strategic alternatives process after suspending its drug program, but private bidders dropped out",
  "exhibit": "Pacific process chronology",
  "data_type": "process",
  "about": "steps April-June 2023",
  "content": [
   "Apr 3, 2023: suspended pomotrelvir, cut headcount ~85%, explored alternatives",
   "Apr 7, 2023: Foresite raised ownership to 27.2%",
   "Apr 20, 2023: Foresite letter on potential acquisition",
   "May 2, 2023: Special Committee formed; Leerink engaged",
   "Considered 133 strategic candidates and five financial buyers",
   "Nine private companies and three financial buyers included",
   "8 submitted non-binding IOIs by May 23, 2023",
   "Three held management presentations Jun 1-3",
   "Two of three dropped out when asked to return $100M capital; last also dropped out"
  ],
  "same_page": [],
  "candidates": [
   "bk51",
   "timeline",
   "ig113",
   "ig028",
   "table",
   "bullets"
  ]
 },
 {
  "row": "rp_082_023_b2",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_082_023_b2_j2.jpg",
  "has_page": true,
  "section": "valuation",
  "message": "DCF implies enterprise value of roughly $19-23bn across terminal multiple and growth assumptions",
  "exhibit": "Implied enterprise value sensitivity",
  "data_type": "matrix",
  "about": "EV by terminal EBITDA multiple and discount rate",
  "content": [
   "10.50x: 20,984 / 20,378 / 19,789 / 19,216",
   "10.75x: 21,473 / 20,854 / 20,252 / 19,667",
   "11.00x: 21,962 / 21,329 / 20,715 / 20,118",
   "11.25x: 22,451 / 21,805 / 21,178 / 20,569",
   "11.50x: 22,940 / 22,281 / 21,641 / 21,019",
   "Discount rates 6.25% to 7.00%",
   "Implied perpetuity growth 1.6% to 2.6%"
  ],
  "same_page": [
   {
    "row": "rp_082_023_b1",
    "exhibit": "Projected unlevered free cash flow",
    "content": [
     "EBITDA 2024E 949",
     "2025E 2,119",
     "2026E 2,354"
    ]
   }
  ],
  "candidates": [
   "bk44",
   "bk13",
   "bk24",
   "bk19",
   "heatmap",
   "table",
   "bk21",
   "bk20"
  ]
 },
 {
  "row": "ig_t_funnel_sourcing",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\ig_t_funnel_sourcing_j2.jpg",
  "has_page": false,
  "section": "process",
  "message": "Four channels narrow to one platform deal",
  "exhibit": "Deal sourcing funnel",
  "data_type": "process",
  "about": "many sources feed one platform deal",
  "content": [
   "Proprietary outreach",
   "Broker auctions",
   "Corporate carve-outs",
   "Founder-led businesses",
   "One platform deal"
  ],
  "same_page": [],
  "candidates": [
   "bk52",
   "chevrons",
   "bk49",
   "ig116",
   "ig026",
   "ig107",
   "bk51"
  ]
 },
 {
  "row": "ig_t_venn_synergy",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\ig_t_venn_synergy_j2.jpg",
  "has_page": false,
  "section": "thesis",
  "message": "The overlap is where the revenue synergies come from",
  "exhibit": "Where the two businesses overlap",
  "data_type": "relationship",
  "about": "shared and unique capabilities of acquirer and target",
  "content": [
   "Acquirer: distribution in 40 countries",
   "Target: proprietary software",
   "Overlap: shared enterprise clients"
  ],
  "same_page": [],
  "candidates": [
   "ig036",
   "ig084",
   "ig009",
   "ig030",
   "ig193",
   "ig032",
   "ig074"
  ]
 },
 {
  "row": "ig_t_rings_quality",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\ig_t_rings_quality_j2.jpg",
  "has_page": false,
  "section": "company",
  "message": "High-quality, sticky revenue",
  "exhibit": "Quality of revenue",
  "data_type": "kpi_set",
  "about": "three percentages",
  "content": [
   "Recurring revenue 85%",
   "Net revenue retention 112%",
   "Gross margin 78%"
  ],
  "same_page": [],
  "candidates": [
   "stat_strip",
   "ig181",
   "stat_icons",
   "bk37",
   "ig064",
   "table",
   "stat_rings"
  ]
 },
 {
  "row": "ig_t_map_uk",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\ig_t_map_uk_j2.jpg",
  "has_page": false,
  "section": "company",
  "message": "12 depots covering every UK region",
  "exhibit": "UK depots",
  "data_type": "geography",
  "about": "sites across UK regions",
  "content": [
   "Scotland 2",
   "North West 3",
   "Midlands 4",
   "London 2",
   "South West 1"
  ],
  "same_page": [],
  "candidates": [
   "ig138",
   "map_pins",
   "ig136",
   "ig137",
   "ig134",
   "ig155"
  ]
 },
 {
  "row": "ig_t_riskmap_move",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\ig_t_riskmap_move_j2.jpg",
  "has_page": false,
  "section": "risks",
  "message": "Power cost is the risk moving the wrong way",
  "exhibit": "Risk map: change since last quarter",
  "data_type": "matrix",
  "about": "risks plotted by likelihood and impact with movement",
  "content": [
   "Power cost: up",
   "Customer churn: down",
   "Key staff: flat",
   "FX: up",
   "Regulation: down"
  ],
  "same_page": [],
  "candidates": [
   "ig059",
   "ig196",
   "harvey",
   "risk_matrix",
   "bk35"
  ]
 },
 {
  "row": "ig_t_jigsaw_fit",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\ig_t_jigsaw_fit_j2.jpg",
  "has_page": false,
  "section": "thesis",
  "message": "The target fills four gaps at once",
  "exhibit": "Strategic fit",
  "data_type": "relationship",
  "about": "how the target fills gaps",
  "content": [
   "Missing product line",
   "New geography",
   "Engineering talent",
   "Customer base"
  ],
  "same_page": [],
  "candidates": [
   "ig084",
   "ig074",
   "ig082",
   "ig081",
   "ig032"
  ]
 },
 {
  "row": "ig_t_history",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\ig_t_history_j2.jpg",
  "has_page": false,
  "section": "company",
  "message": "From start-up to platform in 27 years",
  "exhibit": "Company history",
  "data_type": "time_series",
  "about": "dated milestones since founding",
  "content": [
   "1998 founded",
   "2004 first export",
   "2009 IPO",
   "2013 Asia entry",
   "2017 acquired rival",
   "2020 SaaS launch",
   "2023 taken private",
   "2025 bolt-on"
  ],
  "same_page": [],
  "candidates": [
   "ig128",
   "timeline",
   "ig123",
   "ig125",
   "ig130"
  ]
 },
 {
  "row": "ig_t_quotes",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\ig_t_quotes_j2.jpg",
  "has_page": false,
  "section": "company",
  "message": "Customers see high switching costs",
  "exhibit": "What customers say",
  "data_type": "list",
  "about": "customer interview quotes",
  "content": [
   "\"Switching would take us a year\"",
   "\"Best support in the market\"",
   "\"Pricing is fair\"",
   "\"Roadmap matches our needs\"",
   "\"We plan to add modules\"",
   "\"Onboarding was quick\""
  ],
  "same_page": [],
  "candidates": [
   "bullets",
   "ig174",
   "bk58",
   "ig042",
   "ig075",
   "ig157",
   "pill_rows"
  ]
 },
 {
  "row": "ig_t_speedo_avg",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\ig_t_speedo_avg_j2.jpg",
  "has_page": false,
  "section": "financials",
  "message": "13pts above the industry average",
  "exhibit": "Utilisation vs industry average",
  "data_type": "kpi_set",
  "about": "one big dial with average marker",
  "content": [
   "Utilisation 78%",
   "Industry average 65%"
  ],
  "same_page": [],
  "candidates": [
   "ig058",
   "table",
   "hero_number",
   "stacked",
   "ig057",
   "ig181"
  ]
 }
]
```
