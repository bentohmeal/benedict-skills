# Layout judge
You are setting the answer key for a slide-layout test. Work alone: use only this file and the sheet images it names.
Do not open golden.jsonl, scores.md, examples.md, swaps.md or any other file in the eval folder.

For each of the 54 rows below, open its `sheet` image with the Read tool. The left side is a real bank page (or, when
`has_page` is false, there is no page: judge from the written block). The right side shows candidate layouts from the
deck builder's library, lettered A, B, C... with their ids.

The question for every row: **which layout id would rebuild this exhibit (the `exhibit` / `content` fields: one chart,
table or list on the page, not the whole page) the way the bank actually drew it?** For rows without a page: which
layout would a top bank analyst choose for this content and message?
- Look at the shape of what the bank drew: chart type and orientation, table with or without bars / heat colours,
  number of panels, text boxes vs bullets, map, logos. Match that, not just the topic.
- You may name any id from the catalogue below, not only the candidates on the sheet, if it fits better.
- `ok`: other ids a demanding banker would also accept for this exhibit (0-3). Leave it empty if only one fits.
- `why`: one line naming what you saw (e.g. "horizontal bars ranked, 6 items, values at bar end").
- `doubt`: true if the row looks broken (garbled text, the block does not match the page, not a real exhibit).

Write `C:\Users\user\benedict-skills\plugins\benedict-skills\skills\deal-desk\scripts\..\assets\eval\runs\judge\ans_b4_j1.json` as
{"<row id>": {"best": "<id>", "ok": ["<id>", ...], "why": "...", "doubt": false}, ...}
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
- `table` table (layout, comparison, 2-15 items): Comparison tables, sources & uses, comps, precedent transactions, deal terms, requirements with detail | Don't: A trend or one number per item (use a chart)
- `fin_table` fin table (layout, time_series, 4-20 items): Income statement / cash flow line items in bank format (A / E periods, % rows) | Don't: A one-metric trend (use fin_chart)
- `fin_chart` fin chart (layout, time_series, 4-12 items): One metric's trend with CAGR, actual / estimate split and a % margin strip | Don't: Several unrelated metrics (use fin_table)
- `column` column (layout, time_series, 3-12 items): Market size or volumes over time, or a few series side by side | Don't: Shares of a whole (use stacked / rings)
- `bar` bar (layout, comparison, 3-15 items): Ranking players by one metric (target navy, the rest grey) | Don't: A time series (use column)
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
- `bk11` Plan vs street chart grid (layout, comparison, 2-4 items): Comparing two forecast cases visually | Don't: Only one forecast case
- `bk13` DCF page (page, time_series, 4-8 items): Any DCF output page | Don't: No cash-flow forecast; summary valuation page (use a football field)
- `bk14` WACC build (layout, list, 5-12 items): Discount rate support page | Don't: Main valuation summary; when WACC is just an input line
- `bk15` Football field + commentary panel (layout, range, 3-7 items): Valuation summary that needs the why behind each bar | Don't: A single method; more than 8 methods
- `bk17` Methodology overview (layout, list, 2-6 items): Explaining which methods were used and why | Don't: Showing the numbers themselves (use a football field)
- `bk18` EV bridge waterfall (layout, bridge, 3-8 items): Showing how value builds up | Don't: No adjustments between EV and equity
- `bk19` Multiples table with mean/median band (layout, matrix, 3-15 items): Trading comps or precedent transactions | Don't: Fewer than 3 peers; when one multiple is the point (use bk21/bk22)
- `bk20` Comps + implied value range (layout, matrix, 3-10 items): Linking multiples to an implied valuation | Don't: No implied value to show
- `bk21` Precedent table with inline bars (layout, matrix, 4-12 items): Precedents where the multiple is the point | Don't: Deals with no disclosed multiple
- `bk22` Ranked columns with median line (layout, comparison, 4-12 items): Operational or valuation benchmarking on one metric | Don't: Many metrics at once (use bk32/bk33)
- `bk23` Logo bars + side stats (layout, comparison, 4-10 items): Precedent multiples with who-bought-whom | Don't: No acquirer/target names to show
- `bk24` Column chart + deal table (layout, matrix, 4-10 items): Precedents where the chart and details are both needed | Don't: More than 10 deals (use bk19/bk21)
- `bk25` Premiums paid (layout, range, 2-5 items): Premium analysis | Don't: Private target (no share price)
- `bk26` Price chart with lettered events (layout, time_series, 3-8 items): Share price history with what moved it | Don't: Private target; no events worth flagging
- `bk27` Price chart with callout boxes (layout, time_series, 2-5 items): Trading during a process, reaction to news | Don't: Private target; more than 5 callouts
- `bk28` Price chart + stats side table (layout, time_series, 3-7 items): Share price context for an offer | Don't: Private target
- `bk29` Indexed performance + table (layout, time_series, 2-5 items): Relative share price performance vs peers / index | Don't: Absolute price levels matter more than relative moves
- `bk30` Volume at price (layout, composition, 5-12 items): Shareholder cost base / where stock traded | Don't: Private target; no volume data
- `bk31` Public market overview (page, kpi_set, 4-10 items): Public company snapshot | Don't: Private target
- `bk32` Benchmarking bar matrix (layout, matrix, 3-6 items): Comparing peers on 4-6 metrics at once | Don't: One metric (use bk22); more than 8 peers
- `bk33` Peer small multiples (layout, comparison, 2-4 items): Full peer benchmarking page | Don't: One metric (use bk22)
- `bk35` Company comparison matrix (layout, matrix, 3-5 items): Comparing 3-5 entities or precedent deals on attributes | Don't: More than 5 entities; purely numeric comparison (use bk19)
- `bk36` 2x2 chart dashboard (layout, time_series, 3-4 items): Historical / projected financial summary, market data | Don't: Only one chart worth showing
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
  "row": "sg_dc_s01_b4",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\sg_dc_s01_b4_j1.jpg",
  "has_page": true,
  "section": "market",
  "message": "Asia's premium data centre hub, running at over 95% occupancy",
  "exhibit": "What sets Singapore apart",
  "data_type": "text",
  "about": "connectivity, hyperscaler base, capital depth, barriers to entry",
  "content": [
   "28 subsea cables, 13 more planned",
   "AWS S$12bn more to 2028",
   "Listed DC REITs plus platform buyers",
   "US$14.5/W build cost"
  ],
  "candidates": [
   "pill_rows",
   "table",
   "stacked",
   "ig176",
   "bullets",
   "column",
   "side_tabs"
  ]
 },
 {
  "row": "sg_dc_s02_b4",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\sg_dc_s02_b4_j1.jpg",
  "has_page": true,
  "section": "market",
  "message": "Cloud and AI demand far outruns what Singapore can add",
  "exhibit": "Recent commitments to Singapore",
  "data_type": "list",
  "about": "who committed what capital and when: operators, tender awards",
  "content": [
   "AWS S$12bn to 2028",
   "Digital Realty S$4.3bn Apr 2026",
   "DC-CFA2 200MW Aug 2026",
   "Equinix SG6 US$260m 20MW",
   "Keppel 25MW floating DC 2028",
   "DC-CFA1 80MW Jul 2023"
  ],
  "candidates": [
   "timeline",
   "ig174",
   "pill_rows",
   "bk17",
   "table",
   "bk14"
  ]
 },
 {
  "row": "sg_dc_s03_b4",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\sg_dc_s03_b4_j1.jpg",
  "has_page": true,
  "section": "market",
  "message": "Power and land, not demand, cap new supply",
  "exhibit": "Why supply stays tight",
  "data_type": "text",
  "about": "power, land, time constraints",
  "content": [
   "Power: ~7% of electricity, grid upgrades",
   "Land: steered to Jurong Island",
   "Time: tranches take years"
  ],
  "candidates": [
   "stacked",
   "bk41",
   "table",
   "column",
   "bullets",
   "pill_rows",
   "ig075"
  ]
 },
 {
  "row": "sg_dc_s05_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\sg_dc_s05_b1_j1.jpg",
  "has_page": true,
  "section": "market",
  "message": "A concentrated field of global operators and hyperscalers",
  "exhibit": "Colocation operators",
  "data_type": "comparison",
  "about": "players named with logos, one of three groups",
  "content": [
   "Equinix",
   "Digital Realty",
   "STT GDC",
   "AirTrunk",
   "Keppel",
   "Nxera",
   "NTT",
   "Global Switch",
   "GDS",
   "Princeton Digital"
  ],
  "candidates": [
   "harvey",
   "logo_row",
   "bar",
   "ig060",
   "page_landscape",
   "table"
  ]
 },
 {
  "row": "sg_dc_s05_b5",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\sg_dc_s05_b5_j1.jpg",
  "has_page": true,
  "section": "market",
  "message": "A concentrated field of global operators and hyperscalers",
  "exhibit": "How competition works",
  "data_type": "text",
  "about": "landlord's market, legacy sites, allocation, global capital",
  "content": [],
  "candidates": [
   "photo",
   "pill_rows",
   "bk47",
   "bullets",
   "takeaway",
   "ig157"
  ]
 },
 {
  "row": "sg_dc_s06_b4",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\sg_dc_s06_b4_j1.jpg",
  "has_page": true,
  "section": "market",
  "message": "Scarcity gives Singapore the highest rents in the region",
  "exhibit": "What it means for owners",
  "data_type": "text",
  "about": "rents holding, tenants compete, replacement cost, AI retrofit, arbitrage, so what",
  "content": [],
  "candidates": [
   "side_tabs",
   "bullets",
   "ig157",
   "bk47",
   "photo",
   "takeaway"
  ]
 },
 {
  "row": "sg_dc_s08_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\sg_dc_s08_b1_j1.jpg",
  "has_page": true,
  "section": "valuation",
  "message": "What Singapore data centre assets are worth today",
  "exhibit": "Hyperscale cap rates by market (%)",
  "data_type": "range",
  "about": "low-high cap rate range per market, Singapore highlighted",
  "content": [],
  "candidates": [
   "football_field",
   "table",
   "bar",
   "ig132",
   "bk25",
   "takeaway"
  ]
 },
 {
  "row": "sg_dc_s09_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\sg_dc_s09_b1_j1.jpg",
  "has_page": true,
  "section": "thesis",
  "message": "Own scarce, powered capacity; grow through the corridor",
  "exhibit": "Investment thesis pillars",
  "data_type": "list",
  "about": "four thesis pillars, each a bold claim with evidence, so what and for returns",
  "content": [],
  "candidates": [
   "ig157",
   "page_thesis",
   "takeaway",
   "ig006",
   "pill_rows",
   "side_tabs",
   "bk47"
  ]
 },
 {
  "row": "sg_dc_s10_b2",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\sg_dc_s10_b2_j1.jpg",
  "has_page": true,
  "section": "risks",
  "message": "Each key risk has a clear mitigant",
  "exhibit": "Risk numbers",
  "data_type": "kpi_set",
  "about": "headline risk numbers in a row",
  "content": [
   "~7% electricity",
   "45% largest client",
   "US$14.5/W build",
   "2,500MW+ Johor",
   "-19% value hit"
  ],
  "candidates": [
   "ig177",
   "bk37",
   "stat_icons",
   "stat_strip",
   "bk31"
  ]
 },
 {
  "row": "rp_004_015_b2",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_004_015_b2_j1.jpg",
  "has_page": true,
  "section": "valuation",
  "message": "Premiums paid in US deals vary by consideration type",
  "exhibit": "1-day and 30-day bid premia",
  "data_type": "time_series",
  "about": "premia by consideration 2014-2019 YTD",
  "content": [
   "2014 36%",
   "2015 20%",
   "2016 35%",
   "2017 23%",
   "2018 33%",
   "2019 YTD 23%"
  ],
  "candidates": [
   "bk26",
   "bk13",
   "bar",
   "bk28",
   "bk25",
   "fin_table",
   "bk08",
   "column"
  ]
 },
 {
  "row": "rp_013_025_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_013_025_b1_j1.jpg",
  "has_page": true,
  "section": "company",
  "message": "Three alternatives weighed on benefits and considerations",
  "exhibit": "Alternatives comparison",
  "data_type": "matrix",
  "about": "benefits and considerations per alternative",
  "content": [
   "I. Sale to Shepherd: realizable value; Shepherd assumes obligations; eliminates key risks",
   "II. Sale of Spectrum to Dalmatian: net proceeds address funding gap; likely permits refinancing",
   "III. Chapter 11 Restructuring: addresses capital structure; highly uncertain outcome; equity recovery uncertain"
  ],
  "candidates": [
   "harvey",
   "pros_cons",
   "bk35",
   "table",
   "bk19",
   "bk32"
  ]
 },
 {
  "row": "rp_108_004_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_108_004_b1_j1.jpg",
  "has_page": true,
  "section": "company",
  "message": "Revised proposal offers $13.25 per share with committed financing",
  "exhibit": "Price",
  "data_type": "kpi_set",
  "about": "offer price and premiums",
  "content": [
   "$13.25 per share",
   "30.3% premium to closing price of $10.17 on Jan 25, 2024",
   "31.6% premium to 30-day VWAP of $10.07",
   "29.1% premium to 30-day VWAP of $10.26"
  ],
  "candidates": [
   "side_tabs",
   "bk31",
   "stat_strip",
   "bk37",
   "bk01",
   "table",
   "stat_icons",
   "ig177"
  ]
 },
 {
  "row": "rp_069_006_b2",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_069_006_b2_j1.jpg",
  "has_page": true,
  "section": "company",
  "message": "Valuation uses six methodologies on management projections",
  "exhibit": "Methodology overview",
  "data_type": "list",
  "about": "six valuation approaches",
  "content": [
   "Financial projections",
   "Trading multiples",
   "Sum-of-the-parts",
   "Transaction multiples",
   "Intrinsic valuation",
   "Synergy analysis"
  ],
  "candidates": [
   "pill_rows",
   "bk58",
   "side_tabs",
   "bk17",
   "ig191",
   "ig042"
  ]
 },
 {
  "row": "rp_067_007_b2",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_067_007_b2_j1.jpg",
  "has_page": true,
  "section": "market",
  "message": "Macro backdrop and FttH/FWA competition compressed cable multiples",
  "exhibit": "Multiple change since pre-COVID",
  "data_type": "comparison",
  "about": "percent change in multiples",
  "content": [
   "Charter (87.7%)",
   "Cable One (38.5%)",
   "Comcast (63.4%)",
   "Lumen (79.7%)",
   "Median (37.0%)"
  ],
  "candidates": [
   "bk21",
   "column",
   "bar",
   "table",
   "logo_row",
   "bk22"
  ]
 },
 {
  "row": "rp_052_028_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_052_028_b1_j1.jpg",
  "has_page": true,
  "section": "process",
  "message": "Sale process runs about five months from March to August",
  "exhibit": "Process timeline",
  "data_type": "process",
  "about": "workstreams by week",
  "content": [
   "Marketing document preparation",
   "Outbound calls / NDAs",
   "Initial buyer management meetings / due diligence",
   "First round bids due",
   "Detailed / confirmatory diligence, buyers secure financing",
   "Contract markup due",
   "Final bids / negotiate and sign definitive agreement"
  ],
  "candidates": [
   "ig111",
   "ig121",
   "timeline",
   "bk51",
   "ig126",
   "ig026"
  ]
 },
 {
  "row": "rp_032_007_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_032_007_b1_j1.jpg",
  "has_page": true,
  "section": "financials",
  "message": "Two management cases differ on growth, margins and returns",
  "exhibit": "Case 1 projections",
  "data_type": "text",
  "about": "January 24, 2017 management case",
  "content": [
   "Service and fee revenue grows 8.5% in 2018E then 5%",
   "Underwriting margin improves 79.1% to 66.6%",
   "Investment yield 2.47% to 2.60% in 2018E",
   "Operating income $244mm 2018E to $441mm 2022E",
   "Operating ROE rises to 11.5% by 2022E"
  ],
  "candidates": [
   "bullets",
   "side_tabs",
   "bk09",
   "bk57",
   "bk06",
   "pill_rows",
   "column"
  ]
 },
 {
  "row": "rp_001_016_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_001_016_b1_j1.jpg",
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
  "candidates": [
   "bk06",
   "stacked",
   "column",
   "bk36",
   "line",
   "fin_table",
   "bk08"
  ]
 },
 {
  "row": "rp_006_003_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_006_003_b1_j1.jpg",
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
  "candidates": [
   "bk26",
   "bk27",
   "bk28",
   "bk29",
   "column",
   "bk33",
   "line"
  ]
 },
 {
  "row": "rp_106_002_b2",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_106_002_b2_j1.jpg",
  "has_page": true,
  "section": "process",
  "message": "Broad outreach narrowed to two revised financial buyer proposals",
  "exhibit": "Process narrative",
  "data_type": "text",
  "about": "key events",
  "content": [
   "Pacific suspended pomotrelvir development and engaged SVB Securities",
   "Three private companies selected for diligence",
   "Return of capital of at least $100M required",
   "Two private companies withdrew",
   "Financial buyers revised proposals June 9-12, 2023"
  ],
  "candidates": [
   "takeaway",
   "pill_rows",
   "timeline",
   "table",
   "ig006",
   "bullets",
   "bk49"
  ]
 },
 {
  "row": "rp_000_007_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_000_007_b1_j1.jpg",
  "has_page": true,
  "section": "financials",
  "message": "Margins expand to about 12.5% by FY2028 on stable growth",
  "exhibit": "Projections summary",
  "data_type": "time_series",
  "about": "revenue, EBITDA, capex across years",
  "content": [
   "Years FY22A to FY34E",
   "Gross margin 55.5% FY24 to 54.3% FY28",
   "EBITDA margin about 12.5% by FY2028",
   "Capex in line with historical levels",
   "Net working capital use of cash"
  ],
  "candidates": [
   "column",
   "bk08",
   "fin_table",
   "bk06",
   "bk46"
  ]
 },
 {
  "row": "rp_028_006_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_028_006_b1_j1.jpg",
  "has_page": true,
  "section": "valuation",
  "message": "Selling now at $35-36 beats holding or spinning off unless revenue and EPS grow at high required rates",
  "exhibit": "Alternatives compared",
  "data_type": "comparison",
  "about": "sell vs hold vs spin-off value per share",
  "content": [
   "Sell (pre-spin) $35.00 present value",
   "Spin-off Downside $23.96 / Base $28 / Upside $33",
   "Hold Downside $22.25 / Base $25.77 / Upside $30",
   "Sell A&I (post-spin) $35-37",
   "EPS CAGR Downside 6.4% / Base 9.3% / Upside 11.3%",
   "EPS CAGR required for sell value 14.4%-15.1%"
  ],
  "candidates": [
   "bk22",
   "bar",
   "bk48",
   "bk23",
   "table",
   "bk09",
   "ig104"
  ]
 },
 {
  "row": "rp_115_008_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_115_008_b1_j1.jpg",
  "has_page": true,
  "section": "company",
  "message": "400+ partners and 20,000+ customers span multiple verticals",
  "exhibit": "Partners",
  "data_type": "icons",
  "about": "partner logos",
  "content": [
   "400+ partners"
  ],
  "candidates": [
   "ig094",
   "page_landscape",
   "ig181",
   "hero_number",
   "ig057",
   "logo_row",
   "ig058"
  ]
 },
 {
  "row": "rp_113_013_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_113_013_b1_j1.jpg",
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
  "candidates": [
   "table",
   "bk49",
   "bk51",
   "bk52",
   "chevrons",
   "numbered_steps",
   "harvey"
  ]
 },
 {
  "row": "rp_104_028_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_104_028_b1_j1.jpg",
  "has_page": true,
  "section": "structure",
  "message": "Lunar financing package provides $3,720mm funded debt and $4,570mm commitments at 4.79% base cost",
  "exhibit": "Financing facility terms",
  "data_type": "matrix",
  "about": "size, tenor, pricing by facility",
  "content": [
   "Revolver $1,000mm, 5 years, L+250",
   "Term Loan A $1,000mm, 5 years, L+250",
   "Term Loan B $1,900mm, 7 years, L+375, floor 0.75%, OID 99",
   "Bridge $1,50mm funded + $520mm unsecured, 8 years, L+650",
   "Financial covenants: net first lien leverage and interest coverage"
  ],
  "candidates": [
   "table",
   "bk55",
   "bk19",
   "bk45",
   "side_tabs",
   "bk20",
   "bk47"
  ]
 },
 {
  "row": "rp_115_004_b3",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_115_004_b3_j1.jpg",
  "has_page": true,
  "section": "market",
  "message": "Unstructured data growing twice as fast as structured creates a large data management opportunity",
  "exhibit": "Behaviourally targeted online ad spend",
  "data_type": "time_series",
  "about": "US spend 2007-2012",
  "content": [
   "2007 525",
   "2008 775",
   "2009 1,100",
   "2010 1,700",
   "2011 2,700",
   "2012 4,400"
  ],
  "candidates": [
   "bar",
   "bk41",
   "line",
   "column",
   "timeline",
   "ig097",
   "fin_table"
  ]
 },
 {
  "row": "rp_070_017_b2",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_070_017_b2_j1.jpg",
  "has_page": true,
  "section": "valuation",
  "message": "Take-privates of US-listed Chinese companies saw median premiums of 23-44% across measures",
  "exhibit": "Revised offer",
  "data_type": "text",
  "about": "offer reference",
  "content": [
   "Revised offer at $27.50"
  ],
  "candidates": [
   "bk23",
   "bullets",
   "hero_number",
   "table",
   "bk47",
   "takeaway"
  ]
 },
 {
  "row": "rp_001_023_b2",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_001_023_b2_j1.jpg",
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
  "candidates": [
   "ig131",
   "bk17",
   "ig006",
   "bk47",
   "table",
   "bk50"
  ]
 },
 {
  "row": "rp_028_007_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_028_007_b1_j1.jpg",
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
  "candidates": [
   "table",
   "football_field",
   "bk15",
   "bk22",
   "column",
   "bk25"
  ]
 },
 {
  "row": "rp_039_052_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_039_052_b1_j1.jpg",
  "has_page": true,
  "section": "process",
  "message": "PE buyers paid take-private multiples of about 11-18x TEV / EBITDA in chemicals",
  "exhibit": "Chemicals P2P deals",
  "data_type": "matrix",
  "about": "target, buyer, date, price, multiple",
  "content": [
   "Ferro / Lydall / TPC Group / Innophos / AMLREAN deals",
   "Buyers: First Reserve, SK Capital, Apollo, One Rock",
   "Dates 11/8/2012, 6/1/2015, 10/21/2019, 5/11/2021, 6/21/2021",
   "Price $1,019mm for one deal",
   "TEV / FY1 EBITDA 11.6x, 11.1x, 17.9x"
  ],
  "candidates": [
   "bk55",
   "bk33",
   "bk19",
   "harvey",
   "bk35",
   "bk21",
   "table"
  ]
 },
 {
  "row": "rp_082_053_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_082_053_b1_j1.jpg",
  "has_page": true,
  "section": "valuation",
  "message": "Indicative offer of $34.25 sits about 7% above the unaffected price after volatile trading history",
  "exhibit": "Share price performance",
  "data_type": "time_series",
  "about": "price since NYSE listing and YTD",
  "content": [
   "Listing Dec-15 at $38.75",
   "High $56.57 (May-17)",
   "Low $28.86 (Oct-18)",
   "High $41.12 / Low $28.36 (Mar-20)",
   "Indicative offers $37.55 / $35.75 / $34.25",
   "Unaffected price $32.08 (3/6/2024)"
  ],
  "candidates": [
   "line",
   "bk13",
   "bk27",
   "fin_table",
   "bk28",
   "timeline",
   "bk26"
  ]
 },
 {
  "row": "rp_117_014_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_117_014_b1_j1.jpg",
  "has_page": true,
  "section": "valuation",
  "message": "DCF sensitivities are anchored on median WACC of about 10% and comparable multiples",
  "exhibit": "DCF sensitivity tables",
  "data_type": "matrix",
  "about": "value by discount rate and terminal assumptions",
  "content": [
   "Based on management forecasts",
   "Discount rate range around 10.13% median comparable WACC",
   "9.76% median WACC with Jaguar capital structure",
   "Terminal multiples and growth rates linked to comparables"
  ],
  "candidates": [
   "bk44",
   "bk20",
   "bk19",
   "heatmap",
   "bk21",
   "bk24",
   "table"
  ]
 },
 {
  "row": "rp_082_009_b3",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_082_009_b3_j1.jpg",
  "has_page": true,
  "section": "financials",
  "message": "Management forecast shows capex shifting to Renewables with EBITDA and EPS growth to 2035",
  "exhibit": "Adj. EPS",
  "data_type": "time_series",
  "about": "earnings per share 2024E-2035E",
  "content": [
   "2024E $2.28",
   "2025E $2.47",
   "2026E $2.60",
   "2027E $2.74",
   "2028E $2.96",
   "2029E $3.22",
   "2030E $3.13",
   "2031E $3.47",
   "2032E $3.93",
   "2033E $4.24",
   "2034E $4.54",
   "2035E $4.85"
  ],
  "candidates": [
   "line",
   "bk08",
   "column",
   "bk36",
   "fin_chart",
   "fin_table"
  ]
 },
 {
  "row": "rp_011_015_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_011_015_b1_j1.jpg",
  "has_page": true,
  "section": "financials",
  "message": "Events segment revenue and EBITDA swing with the Olympic cycle, peaking in 2028E",
  "exhibit": "Segment financials",
  "data_type": "matrix",
  "about": "revenue, adj. EBITDA and UFCF by year",
  "content": [
   "EE&R revenue 2023A $1,999, 2024E $3,038, 2025E $2,008, 2026E $2,455, 2027E $2,327, 2028E $4,128",
   "Adj. EBITDA 2024E $325, 2025E $251, 2026E $334, 2027E $326, 2028E $631",
   "Pre-tax UFCF 2024E $246, 2026E $452, 2027E $658, 2028E $314",
   "Split IMG Media, On Location, Other"
  ],
  "candidates": [
   "bk20",
   "table",
   "bk09",
   "bk06",
   "bk07",
   "bk55",
   "bk19",
   "fin_table"
  ]
 },
 {
  "row": "rp_039_030_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_039_030_b1_j1.jpg",
  "has_page": true,
  "section": "financials",
  "message": "Section covers management forecast 2023E-2027E and observations on its drivers and assumptions",
  "exhibit": "Section contents",
  "data_type": "list",
  "about": "topics covered in forecast section",
  "content": [
   "Business Background & Drivers",
   "Historic and Forecast Financial Development",
   "Net Sales & Gross Profit Bridge Observations",
   "Performance vs Various Company Management Forecast",
   "Company Management Forecast FX Assumptions",
   "Preliminary Observations"
  ],
  "candidates": [
   "bk58",
   "bk17",
   "pill_rows",
   "ig042",
   "side_tabs",
   "ig006",
   "numbered_steps"
  ]
 },
 {
  "row": "rp_071_008_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_071_008_b1_j1.jpg",
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
  "candidates": [
   "chevrons",
   "numbered_steps",
   "bk51",
   "ig121",
   "ig111",
   "bk52"
  ]
 },
 {
  "row": "rp_114_004_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_114_004_b1_j1.jpg",
  "has_page": true,
  "section": "process",
  "message": "Buyers like product and management but worry about user trends, market size and exit",
  "exhibit": "Positive feedback",
  "data_type": "list",
  "about": "buyer positives",
  "content": [
   "Product leadership and pipeline of product improvements",
   "Positive on Archives, DNA and potential TLC agreement",
   "Potential for international market penetration",
   "Opportunity to partner with Family Search on content",
   "Strong management team"
  ],
  "candidates": [
   "pill_rows",
   "bullets",
   "pros_cons",
   "ig006",
   "table",
   "ig119",
   "bk57",
   "bk17"
  ]
 },
 {
  "row": "rp_085_023_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_085_023_b1_j1.jpg",
  "has_page": true,
  "section": "market",
  "message": "Cloud delivery expands the ERP addressable market beyond on-premise models",
  "exhibit": "Illustrative ERP total addressable market",
  "data_type": "composition",
  "about": "on-premise vs cloud addressable market by firm size",
  "content": [
   "Large: ~9,000 firms",
   "Mid-Market 100-1,000 employees: ~116,000 firms",
   "Small under 100 employees: ~6,000,000 firms",
   "On-Premise ERP Addressable Market",
   "Cloud ERP Addressable Market"
  ],
  "candidates": [
   "ig178",
   "stacked",
   "ig071",
   "bk41",
   "bk39",
   "bk30",
   "stat_rings"
  ]
 },
 {
  "row": "rp_066_015_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_066_015_b1_j1.jpg",
  "has_page": true,
  "section": "valuation",
  "message": "Precedent deals priced at a median 13.5x LTM EBITDA with 25-49% premiums",
  "exhibit": "Enterprise value / LTM EBITDA by deal",
  "data_type": "comparison",
  "about": "precedent transaction multiples",
  "content": [
   "Mar-19 7.9x",
   "Apr-18 18.0x",
   "Apr-17 17.3x",
   "Oct-15 16.8x",
   "Nov-19 13.5x",
   "Dec-20 6.6x",
   "Oct-20 9.9x",
   "Feb-20 11.1x",
   "Median 13.5x",
   "Median 9.9x"
  ],
  "candidates": [
   "bk21",
   "bk22",
   "bk23",
   "bk19",
   "table",
   "heatmap",
   "bar"
  ]
 },
 {
  "row": "rp_083_029_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_083_029_b1_j1.jpg",
  "has_page": true,
  "section": "process",
  "message": "Sale process runs from August to November with approvals and financing dates in parallel",
  "exhibit": "M&A process timeline",
  "data_type": "process",
  "about": "key actions by week",
  "content": [
   "Discuss Joint Offer and liquidity alternatives with lenders",
   "Finalize company forecast model and marketing materials",
   "Contact other potential acquirers and gauge interest",
   "Sign confidentiality agreements and distribute marketing materials",
   "Finalize electronic data room and give buyer access",
   "Negotiate and execute definitive agreement",
   "Majority-of-the-minority stockholder approval",
   "SEC materials review and approval",
   "Receive regulatory approvals"
  ],
  "candidates": [
   "ig126",
   "ig113",
   "bk51",
   "ig028",
   "ig089",
   "ig107",
   "timeline"
  ]
 },
 {
  "row": "rp_070_010_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_070_010_b1_j1.jpg",
  "has_page": true,
  "section": "valuation",
  "message": "All methods place Focus Media below or around the $27.50 revised offer",
  "exhibit": "Implied share price by methodology (US$/ADS)",
  "data_type": "range",
  "about": "valuation ranges by method",
  "content": [
   "DCF management case WACC 18.3%: 22.35 to 31.17",
   "DCF WACC 18.9%: 22.64 to 26.01",
   "DCF WACC 20.8%: 22.07 to 20.23",
   "Trading multiples 2013E P/E 9.0-12.0x: 26.01 to 34.59",
   "2013E EV/EBITDA 6.0-9.0x: 17.58 to 25.85",
   "2013E EV/Sales 1.5-2.5x: 23.67 to 29.81",
   "Transaction multiples LTM EV/EBITDA 6.0-8.0x: 27.35 to 31.33",
   "52-week range $21.84 to $29.90",
   "Initial offer $27.00, Revised offer $27.50"
  ],
  "candidates": [
   "football_field",
   "bk15",
   "heatmap",
   "bk22",
   "table"
  ]
 },
 {
  "row": "rp_115_010_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_115_010_b1_j1.jpg",
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
  "candidates": [
   "logo_row",
   "bk32",
   "heatmap",
   "bar",
   "table",
   "line",
   "column",
   "bk22"
  ]
 },
 {
  "row": "rp_109_004_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_109_004_b1_j1.jpg",
  "has_page": true,
  "section": "company",
  "message": "Rover's share price reacted to successive takeover proposals from February to July 2024",
  "exhibit": "Rover daily share price and volume with key events",
  "data_type": "time_series",
  "about": "price and events Jan-Jul 2024",
  "content": [
   "Jan 26, 2024: private request for waiver of Investor Rights Agreement",
   "Feb 22, 2024: UnitedHealth suspected cybersecurity breach",
   "Feb 26, 2024: NMC public draft proposal $13.75 / share, 1-day +25%",
   "Mar 11, 2024: Special committee formed",
   "Mar 19, 2024: waiver request rejected",
   "May 7-8, 2024: standstill waiver, Q1 earnings",
   "Jun 13, 2024: TCP-ASC requests standstill waiver",
   "Jul 1, 2024: NMC draft proposal $13.25",
   "Jul 19, 2024: TCP-ASC with CD&R proposal $14.30; NMC proposal $14.05; Rover $12.90"
  ],
  "candidates": [
   "line",
   "bk27",
   "ig123",
   "bk26",
   "timeline",
   "bk38",
   "table"
  ]
 },
 {
  "row": "rp_121_022_b1",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_121_022_b1_j1.jpg",
  "has_page": true,
  "section": "company",
  "message": "Owner bears expenses under Keppel leases and colocation; triple-net leases shift costs to clients",
  "exhibit": "Contractual arrangements by property",
  "data_type": "matrix",
  "about": "lease type and owner responsibilities",
  "content": [
   "Keppel DC Singapore 1-5, 7, 8: Keppel lease / colocation; client pays rent; owner bears all expenses",
   "DC1: triple-net lease; client pays rent and outgoings except shell insurance",
   "Gore Hill Data Centre: triple-net lease; client pays rent and all outgoings",
   "Gore Hill Data Centre (one client): colocation; owner bears all expenses",
   "Guangdong Data Centres 1, 2 & 3: triple-net lease; client pays except real estate tax threshold",
   "Tokyo Data Centre 1: triple-net lease; client pays rent and all outgoings",
   "Basis Bay Data Centre: colocation; owner bears agreed facilities management amount, insurance, property tax"
  ],
  "candidates": [
   "bk35",
   "bk19",
   "bk21",
   "bk20",
   "table",
   "side_tabs",
   "harvey"
  ]
 },
 {
  "row": "rp_082_023_b2",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\rp_082_023_b2_j1.jpg",
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
  "candidates": [
   "heatmap",
   "bk21",
   "bk13",
   "bk24",
   "table",
   "bk19",
   "bk44",
   "bk20"
  ]
 },
 {
  "row": "ig_t_cycle_deal",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\ig_t_cycle_deal_j1.jpg",
  "has_page": false,
  "section": "process",
  "message": "A seven-stage sale from prep to close",
  "exhibit": "M&A deal cycle",
  "data_type": "process",
  "about": "the stages a sale goes through",
  "content": [
   "Prepare",
   "Market",
   "First-round bids",
   "Due diligence",
   "Final bids",
   "Sign",
   "Close"
  ],
  "candidates": [
   "bk51",
   "ig107",
   "numbered_steps",
   "ig026",
   "ig113",
   "timeline",
   "chevrons"
  ]
 },
 {
  "row": "ig_t_tam_rings",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\ig_t_tam_rings_j1.jpg",
  "has_page": false,
  "section": "market",
  "message": "A US$1.5bn near-term prize inside a US$48bn market",
  "exhibit": "TAM / SAM / SOM",
  "data_type": "hierarchy",
  "about": "nested market size",
  "content": [
   "TAM US$48bn",
   "SAM US$12bn",
   "SOM US$1.5bn"
  ],
  "candidates": [
   "ig011",
   "column",
   "tam_sam_som",
   "table",
   "ig071"
  ]
 },
 {
  "row": "ig_t_thermo_fund",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\ig_t_thermo_fund_j1.jpg",
  "has_page": false,
  "section": "process",
  "message": "80% of the fund is raised",
  "exhibit": "Fundraising progress",
  "data_type": "kpi_set",
  "about": "money raised vs target",
  "content": [
   "Raised US$1.6bn",
   "Target US$2.0bn"
  ],
  "candidates": [
   "hero_number",
   "ig181",
   "table",
   "ig057",
   "ig094",
   "stat_icons"
  ]
 },
 {
  "row": "ig_t_map_world",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\ig_t_map_world_j1.jpg",
  "has_page": false,
  "section": "company",
  "message": "Seven offices across three continents",
  "exhibit": "Global office network",
  "data_type": "geography",
  "about": "offices worldwide",
  "content": [
   "New York",
   "London",
   "Frankfurt",
   "Dubai",
   "Singapore",
   "Tokyo",
   "Sydney"
  ],
  "candidates": [
   "ig143",
   "ig146",
   "ig147",
   "ig144",
   "ig135",
   "ig136",
   "ig145",
   "map_pins"
  ]
 },
 {
  "row": "ig_t_bullbear_mkt",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\ig_t_bullbear_mkt_j1.jpg",
  "has_page": false,
  "section": "market",
  "message": "Demand drivers outweigh supply limits",
  "exhibit": "Market direction",
  "data_type": "comparison",
  "about": "drivers pushing up vs down",
  "content": [
   "Up: AI demand, cloud migration",
   "Down: power limits, rate rises"
  ],
  "candidates": [
   "ig132",
   "logo_row",
   "bk57",
   "ig102",
   "table",
   "pros_cons"
  ]
 },
 {
  "row": "ig_t_radar_peers",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\ig_t_radar_peers_j1.jpg",
  "has_page": false,
  "section": "market",
  "message": "Wins on product, service and tech; trails on reach",
  "exhibit": "Capability vs peers",
  "data_type": "comparison",
  "about": "target vs peer average on six dimensions",
  "content": [
   "Product 8 vs 6",
   "Price 5 vs 7",
   "Service 9 vs 6",
   "Reach 4 vs 7",
   "Brand 7 vs 7",
   "Tech 8 vs 5"
  ],
  "candidates": [
   "bar",
   "ig066",
   "table",
   "ig079",
   "ig080",
   "logo_row",
   "bk32",
   "bk22"
  ]
 },
 {
  "row": "ig_t_cogs_ops",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\ig_t_cogs_ops_j1.jpg",
  "has_page": false,
  "section": "thesis",
  "message": "Scale meets reach",
  "exhibit": "Two businesses that mesh",
  "data_type": "relationship",
  "about": "manufacturing plus distribution",
  "content": [
   "Acquirer: manufacturing scale",
   "Target: distribution network"
  ],
  "candidates": [
   "ig084",
   "ig092",
   "ig090",
   "ig009",
   "ig115"
  ]
 },
 {
  "row": "ig_t_year_ring",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\ig_t_year_ring_j1.jpg",
  "has_page": false,
  "section": "process",
  "message": "Six fixed reporting moments a year",
  "exhibit": "Annual reporting calendar",
  "data_type": "time_series",
  "about": "events across 12 months",
  "content": [
   "Jan budget",
   "Mar Q4 results",
   "Apr AGM",
   "May Q1 results",
   "Aug half-year",
   "Nov Q3 results"
  ],
  "candidates": [
   "ig128",
   "ig131",
   "timeline",
   "logo_row",
   "ig130",
   "ig126"
  ]
 },
 {
  "row": "ig_t_team",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\ig_t_team_j1.jpg",
  "has_page": false,
  "section": "company",
  "message": "A proven team that stays post-deal",
  "exhibit": "Management team",
  "data_type": "list",
  "about": "people with roles",
  "content": [
   "CEO, 20 yrs",
   "CFO, ex-Big 4",
   "COO, ex-Amazon",
   "CTO, founder",
   "CRO, ex-Salesforce"
  ],
  "candidates": [
   "ig175",
   "table",
   "side_tabs",
   "ig157",
   "bk58",
   "pill_rows",
   "ig042"
  ]
 },
 {
  "row": "ig_t_speedo_avg",
  "sheet": "C:\\Users\\user\\benedict-skills\\plugins\\benedict-skills\\skills\\deal-desk\\scripts\\..\\assets\\eval\\runs\\judge\\sheets\\ig_t_speedo_avg_j1.jpg",
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
  "candidates": [
   "ig057",
   "ig058",
   "hero_number",
   "table",
   "ig181",
   "stacked"
  ]
 }
]
```
