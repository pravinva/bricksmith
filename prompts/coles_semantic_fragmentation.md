# Coles Group: Semantic Fragmentation Under Data Democratization
## Enterprise Architecture Diagram – Nano Banana Pro Prompt

---

## EXECUTIVE INTENT

**Objective:** Visualize why Coles' source-aligned data product strategy, while operationally sound for ingestion and raw data distribution, creates unsustainable semantic fragmentation downstream. Demonstrate that without a governed, centralized semantic layer, democratized modeling devolves into tool-specific silos, violating core data mesh and enterprise data governance principles.

**Audience:** C-suite, Chief Data Officer, enterprise architects, data governance stakeholders.

**Core Message:** *Coles has optimized for data democratization at the expense of semantic coherence. Semantic logic has fragmented across four competing platforms with no unified source of truth, creating redundancy, inconsistency, and governance debt.*

---

## ARCHITECTURAL CONTEXT

### Data Mesh Principles Violated

This diagram illustrates three critical failures against data mesh and modern enterprise data architecture best practices:

1. **No Federated Governance Over Semantic Layer**: Data mesh requires federated governance with agreed contracts. Coles has democratic modeling without semantic contracts, creating divergent business logic.

2. **Product Thinking Stops at Raw Data**: Source-aligned data products deliver raw/conformed data only. Semantic products (business metrics, dimensions, facts) are built downstream in tool-specific silos instead of being published as discoverable, reusable data products.

3. **Semantic Layer Fragmentation**: Instead of a single, governed semantic layer (Unity Catalog + Lakehouse semantic tables, or equivalent), semantic logic lives in:
   - Snowflake SQL transformation scripts (imperative, code-based, hard to discover)
   - Power BI semantic models (BI-specific, non-reusable, locked to tool)
   - Palantir ontology (isolated discovery layer, good UX but separate truth)
   - Microsoft Fabric (emerging, unvetted, adds another source of truth)

---

## DESIGN SPECIFICATIONS

### Visual Style

**Brand Framework:** Databricks-aligned enterprise aesthetic  
**Background:** Clean white (#FFFFFF)  
**Typography:** Modern sans-serif (Inter, Lato, Open Sans), no serifs  
**Hierarchy:** Bold navy (#1B3139) for titles, regular grey for descriptions  
**Font Sizes:** 40px (title), 32px (section headers), 24px (box titles), 20px (subtitles), 16px (body)

### Color Palette

| Element | Color | Hex | Purpose |
|---------|-------|-----|---------|
| Primary Accent | Databricks Orange | #FF3621 | Highlights, accents |
| Headers & Primary Text | Navy | #1B3139 | Authority, readability |
| Secondary Text | Warm Gray | #A0ACBE | Descriptions, subtle info |
| Warning/Fragmentation | Red | #DC3545 | Risk indicators, problems |
| Neutral Backgrounds | Light Gray | #F5F5F5 | Source systems, neutral zones |
| Action/Error | Deep Red | #B71C1C | Consequence layer, critical messaging |

### Logo Treatment

**Uploaded Logos (Use Exactly):**
- Databricks: Red/orange stacked bars with text
- Delta Lake: Teal triangle
- Unity Catalog: Pink squares, yellow triangles, navy hexagon

**Generated Logos (Official Styles):**
- Snowflake: Blue snowflake icon with white background
- Power BI: Dark blue square with yellow accent
- Palantir: Geometric gotham-style mark
- Microsoft Fabric: Purple/blue gradient fabric weave icon

**Logo Rules:**
- No redrawing or substitution
- Uniform scaling (approximately 32px × 32px)
- No numbered labels, circles, or badges
- No filenames or annotations
- Place logos at left-edge of respective box titles

---

## LAYOUT ARCHITECTURE

### Section 1: Ingestion Layer (Clean, Orderly)
**Goal:** Show that raw data flow works correctly. This part is not the problem.

**Visual Structure:**
```
Four light-gray boxes in horizontal row, evenly spaced, neutral appearance:
   [SAP]  [Legacy Systems]  [Third-Party Data]  [Operational Sources]
```

**Content:**
- Box label color: #F5F5F5 background, #1B3139 text
- Title font: 20px bold
- Sub-label below row: "Raw data from enterprise systems" (14px, #A0ACBE)
- Arrows: Simple, neutral gray (#CCCCCC), pointing downward, thickness 2px
- Arrow labels: None (implicit clean flow)

**Message:** "Ingestion is solved. The problem lies downstream."

---

### Section 2: Central Hub (Snowflake Warehouse)
**Goal:** Position Snowflake as source-of-truth for raw data. Highlight that it serves only as a hub, not as semantic authority.

**Visual Structure:**
```
Large rectangular box, centered, Snowflake brand blue background
```

**Content:**
- **Logo:** Snowflake official logo (left side, 40px × 40px)
- **Title:** "Snowflake Data Warehouse" (32px bold, navy)
- **Subtitle:** "Hub-and-Spoke Model • Source-Aligned Data Products" (20px regular, navy)
- **Description:** "Enterprise Data Team creates raw data products, democratizes modeling to business units" (16px regular, warm gray, max 2 lines)
- **Background Color:** Snowflake light blue (#E8F4F8) with darker blue border (#0066CC, 2px)
- **Border Weight:** 2px solid #0066CC
- **Padding:** 24px internal spacing

**Visual Cue:** Downward arrow from source systems to Snowflake is thick, green-tinted to suggest "healthy so far."

**Message:** "Snowflake is the hub. Semantic decisions happen downstream—and that's the problem."

---

### Section 3: Fragmentation Layer (Chaos Zone)
**Goal:** Make the fragmentation viscerally obvious. Boxes should feel disconnected, arrows should diverge in competing colors, red borders signal risk.

**Visual Structure:**
```
Four boxes placed in loose, deliberately non-aligned horizontal row below Snowflake.
Each box positioned at slightly different vertical offsets (first at -8px, second at +4px, third at -12px, fourth at +6px)
to suggest instability and lack of cohesion.
```

**Diverging Arrows from Snowflake Hub:**
- Four separate arrows, each a different color: red, orange, yellow, purple
- Arrow thickness: 3px (more prominent than ingestion layer)
- Arrow labels: Placed above/beside each arrow: "Business Team A", "Business Team B", "Business Team C", "Business Team D"
- Label font: 14px italic, #1B3139
- Divergence point labeled: "Semantic logic fragments here" (16px bold, #DC3545, positioned at center between Snowflake and fragmentation layer)

**Chaos Indicators Between Boxes:**
- Dotted lines (2px dashed, gray #CCCCCC) connecting adjacent boxes
- Label on dotted lines: "Inconsistent definitions" (12px italic, #A0ACBE)
- Small red warning triangles (⚠️ style, not emoji—use SVG outline) placed above 2–3 of the dotted lines
- Placement of question marks "?" (14px, #DC3545) between boxes to signal ambiguity

---

### Box 1: Snowflake SQL Scripts

**Content:**
- **Icon:** Red warning triangle (top-right corner, 24px)
- **Title:** "Snowflake SQL Scripts" (24px bold, navy, with no logo—SQL is not a product brand)
- **Subtitle:** "Transformation Logic" (16px regular, navy)
- **Description:** "Business analysts write custom SQL • Hundreds of scattered scripts • Logic lives in code • Hard to discover, hard to reuse" (14px regular, warm gray, left-aligned, bullet-separated)
- **Background:** White with red border
- **Border:** 3px solid #DC3545
- **Size:** Approximately 220px wide × 140px tall
- **Padding:** 16px
- **Text Color:** Navy for titles, warm gray for description

**Subtle Note:** Optional small text at bottom: "Governance: None. Discoverability: Low. Reusability: Minimal." (11px italic, #A0ACBE)

---

### Box 2: Power BI Semantic Models

**Content:**
- **Logo:** Power BI official logo (left side, 32px × 32px)
- **Icon:** Red warning triangle (top-right corner, 24px)
- **Title:** "Power BI Semantic Models" (24px bold, navy)
- **Subtitle:** "BI Logic Layer" (16px regular, navy)
- **Description:** "Semantic models define business metrics • Logic locked in BI • Not reusable outside Power BI • Vendor-specific semantics" (14px regular, warm gray, left-aligned, bullet-separated)
- **Background:** White with red border
- **Border:** 3px solid #DC3545
- **Size:** ~220px × 140px
- **Padding:** 16px

**Subtle Note:** "Governance: Team-level. Discoverability: Within Power BI only. Reusability: Requires re-modeling." (11px italic, #A0ACBE)

---

### Box 3: Palantir Ontology

**Content:**
- **Icon:** Red warning triangle (top-right corner, 24px)
- **Title:** "Palantir Ontology" (24px bold, navy)
- **Subtitle:** "Data Discovery & Relationships" (16px regular, navy)
- **Description:** "Interactive canvas for exploration • Table relationships mapped • Good UX, isolated silo • Another source of truth" (14px regular, warm gray, left-aligned, bullet-separated)
- **Highlight Box:** Small inset, light orange background: "Best feature: Visual exploration canvas. Problem: Logic not reused elsewhere." (12px italic, navy, in smaller box within the main box, top-left, light background)
- **Background:** White with red border
- **Border:** 3px solid #DC3545
- **Size:** ~220px × 140px
- **Padding:** 16px

**Subtle Note:** "Governance: Discovery-focused, not metric-focused. Discoverability: High within Palantir. Reusability: Low." (11px italic, #A0ACBE)

---

### Box 4: Microsoft Fabric IQ

**Content:**
- **Logo:** Microsoft Fabric official logo (left side, 32px × 32px)
- **Icon:** Red warning triangle (top-right corner, 24px)
- **Title:** "Microsoft Fabric IQ" (24px bold, navy)
- **Subtitle:** "Experimental Workloads" (16px regular, navy)
- **Description:** "Positioned as silver bullet • Still playing catch-up on governance • Adds another competing silo • Emerging, not yet proven at scale" (14px regular, warm gray, left-aligned, bullet-separated)
- **Background:** White with red border
- **Border:** 3px solid #DC3545
- **Size:** ~220px × 140px
- **Padding:** 16px

**Subtle Note:** "Governance: Unclear. Discoverability: Unknown. Reusability: Unproven. Risk: Vendor lock-in." (11px italic, #A0ACBE)

---

### Section 4: Consequence Layer (Impact Zone)
**Goal:** Make the cost tangible and undeniable. High visual weight, red background, white text, clear messaging.

**Visual Structure:**
```
Full-width box spanning all four fragmentation boxes above, positioned below with 16px gap.
```

**Content:**
- **Background Color:** Deep red #B71C1C with slight opacity (95%) to allow subtle white grid pattern or texture
- **Text Color:** White (#FFFFFF)
- **Border:** None (solid background carries weight)
- **Padding:** 32px
- **Height:** ~160px

**Header:**
- **Icon:** Warning symbol (⚠️ rendered as SVG outline, not emoji, 40px × 40px, white, left-aligned)
- **Title:** "MULTIPLE SOURCES OF TRUTH" (32px bold, white, positioned right of icon)
- **Spacing:** 16px between icon and title

**Content Grid (Two Columns):**

| Left Column | Right Column |
|---|---|
| • Same metric calculated 4 different ways | • No enterprise data model |
| • Inconsistent business logic | • Semantic layer is uncontrolled |

Font: 16px regular, white, bullet-separated, line-height 1.6

**Sub-message (Below Grid):**
"The cautionary tale: democratized modeling without federated governance = fragmentation at scale" (14px italic, white, #F0F0F0 color, margin-top 12px)

**Alternative Layout (if space permits):**
- Display as four bullet points in a 2×2 grid instead of 2-column layout
- Centered, bold bullet text

---

## VISUAL FLOW ARCHITECTURE

### Primary Data Flow (Top to Fragmentation)

1. **Ingestion Flow** (Green accent, 3px):
   - Source systems → Snowflake: Straight down, aligned, professional
   - Label: "Clean ingestion" (implicit, no label needed)

2. **Divergence Point** (Orange accent, transition zone):
   - At Snowflake bottom edge, add a small zone label: "Semantic decisions democratized here ➜"
   - Introduce first red accent at divergence point

3. **Fragmentation Flow** (Multi-colored, chaotic):
   - Snowflake → Four boxes: Four separate arrows in red, orange, yellow, purple
   - Each arrow bends slightly differently (subtle curves, not straight) to suggest organic drift rather than intentional design
   - Arrow heads: Standard triangle, colored to match arrow
   - Central label: "Semantic logic fragments here" (16px bold, #DC3545, positioned between Snowflake and top of fragmentation boxes)

4. **Interconnected Chaos** (Dotted red/gray):
   - Dotted lines (2px dashed) between fragmentation boxes
   - Labels: "Inconsistent definitions", "Version conflicts?", "No reconciliation"
   - Question marks (?) scattered between boxes in red

---

## ANNOTATION LAYER (Overlay Text)

### Fragmentation Zone Callout

Position at top-center of fragmentation layer (overlaid on or just above):

```
"What Palantir does well:
 • Interactive visual canvas
 • Good UX for exploration

What's missing across all systems:
 • Unified semantic contracts
 • Federated governance
 • Reusable metric definitions
 • Enterprise data model"
```

Font: 13px regular, navy, inset white background box with light gray border, positioned center-top, ~300px wide

---

## VISUAL EMPHASIS RULES (DO / DO NOT)

### ✅ DO Emphasize

- Fragmentation: Use red borders, multiple arrow colors, dotted chaos lines
- Divergence: Show arrows splitting in four directions at different angles
- Redundancy: Use question marks, warning triangles, "Which is right?" messaging
- Risk: Deep red background on consequence box, warning icons, italic cautionary text
- Contrast: Clean top (ingestion) vs. messy middle (fragmentation) vs. red bottom (cost)

### ❌ DO NOT

- Make fragmentation look organized, aligned, or intentional
- Use green checkmarks or positive framing anywhere
- Add badges, numbers, or ranked lists suggesting priority
- Use orderly grid layouts for the fragmentation zone
- Include success metrics or positive KPIs
- Use gradients, drop shadows, 3D effects, or excessive transparency
- Add decorative elements unrelated to the architecture
- Use serif fonts anywhere
- Include Databricks logo in the "problem" section (only on title/branding if needed)

---

## GOVERNANCE & ARCHITECTURE CALLOUTS

### Implicit Design Critique

The diagram, by structure alone, should communicate:

1. **Scalability Illusion:** Coles scaled data distribution (hub-and-spoke) without scaling semantic governance. Result: governance debt.

2. **Tool Proliferation ≠ Data Democracy:** Four platforms don't equal democracy; they equal fragmentation.

3. **Semantic Layer as Missing Infrastructure:** The diagram has no representation of a centralized, governed semantic layer. This absence is intentional and visual.

4. **Data Mesh Incomplete:** Data products are defined only at raw/conformed level. Semantic products (metrics, dimensions) are not published, discovered, or governed.

---

## TECHNICAL SPECIFICATIONS FOR IMAGE GENERATION

### Canvas

- **Resolution:** 1920px × 1440px (16:9 landscape, executive slide-ready)
- **DPI:** 96 (screen optimized)
- **Background:** Solid white #FFFFFF, no texture

### Typography Rendering

- Font family: Inter or Lato (sans-serif, modern)
- Anti-aliasing: On (smooth rendering)
- Font rendering: Screen-optimized (not print)

### Spacing & Layout

- **Horizontal margins:** 60px left/right
- **Vertical spacing:** 
  - Source systems to Snowflake hub: 80px gap
  - Snowflake hub to fragmentation layer: 60px gap
  - Fragmentation layer to consequence box: 40px gap
- **Grid alignment:** Left-align all text within boxes (flush-left)

### Box Styling

- **Border radius:** 0px (sharp corners, corporate)
- **Box shadow:** None (flat design)
- **Border weight:** 2px (Snowflake/hubs), 3px (fragmentation boxes)

---

## MESSAGING HIERARCHY

### Primary Message (Visual, not text)

"Coles' source-aligned data product approach is sound for raw data but creates semantic chaos downstream."

### Secondary Message (Fragmentation callout)

"Four competing semantic platforms, four competing truths, no enterprise data model, no source of truth."

### Tertiary Message (Consequence box)

"Democratized modeling without federated governance = unsustainable fragmentation."

---

## SUCCESS CRITERIA

The diagram is successful if, when shown to a Chief Data Officer:

- ✅ They immediately see the contrast between "clean ingestion" and "messy semantic layer"
- ✅ They understand Snowflake is not the problem; the downstream silos are
- ✅ They feel urgency about the lack of a governed semantic layer
- ✅ They recognize that Palantir's good UX doesn't solve the fragmentation problem
- ✅ They understand this violates data mesh principles (federated governance, semantic reusability)
- ✅ They see the warning as actionable, not alarmist

---

## ANTI-PATTERNS (Avoid These)

- ❌ Making all sections look equally chaotic (top should feel orderly)
- ❌ Suggesting the solution (e.g., adding a "Unified Semantic Layer" box—this prompt only diagnoses)
- ❌ Using soft pastels or light colors for warning elements (use bold red)
- ❌ Positioning Power BI and Palantir as "solutions" (they're silos)
- ❌ Adding positive framing about tool capabilities (this is a problem diagram)
- ❌ Using flowchart symbols or process diagrams (static architecture, not workflow)

---

## FINAL INTENT

This diagram tells a single, architecturally sound story: **Coles optimized for data distribution but created semantic fragmentation. To scale further, they need a governed semantic layer as enterprise infrastructure, not tool-specific implementations.**

The visual language reinforces this without text: chaos in the middle, red warning at the bottom, clean top that's working but insufficient. This is a cautionary tale about the limits of democratization without governance.

