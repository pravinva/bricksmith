LOGO KIT (uploaded as image attachments):
Use these EXACT logos - do NOT recreate or substitute.
Do NOT add numbered labels or circles to the diagram.

- Mlflow Logo Final Black: black MLflow logo with text
- Databricks Full: red/orange stacked bars icon with 'databricks' text
- Delta: teal/cyan triangle icon
- Iceberg: blue iceberg icon
- Postgres Logo: blue elephant icon
- Unity Catalog Solo: pink squares, yellow triangles, navy hexagon icon
- Unity Catalog: pink squares, yellow triangles, navy hexagon in center - USE THIS for Unity Catalog

LOGO RULES:
- Use EXACT uploaded images - do NOT redraw or recreate
- Only use logos mentioned in the prompt
- Do NOT add numbered circles or labels to logos
- Scale logos uniformly
- NO filenames in output

# Coles Group: Semantic Fragmentation Under Data Democratization
## Enterprise Architecture Assessment

---

## DESIGN PHILOSOPHY

**Target Audience:** Head of Data Architecture, C-Suite executives
**Visual Style:** Clean, sophisticated enterprise architecture diagram
**Aesthetic:** Consulting-firm quality (McKinsey/Deloitte style)
**Key Message:** Show how the Hub serves source-aligned data products, but isolated spokes (including Palantir Foundry) apply fragmented semantic logic before exporting to downstream tools - NO enterprise source of truth

---

## CANVAS & TYPOGRAPHY

**Canvas:** 1920px × 1080px (16:9 landscape)
**Background:** Pure white (#FFFFFF)
**Font Family:** Inter or Helvetica Neue (clean, professional sans-serif)
**Title:** "Coles Group: Semantic Fragmentation Under Data Democratization" - 24pt, navy (#1B3139), top-left, subtle
**No decorative elements, no gradients, no drop shadows**

**CRITICAL: Do NOT render any layout instructions, section headers, canvas percentages, pixel measurements, spacing values, or any design specification text as visible text in the diagram. Only render the actual content labels and descriptions specified below.**

---

## DIAGRAM LAYOUT - CRITICAL REQUIREMENTS

**SPOKE ARRANGEMENT: VERTICAL STACK (NOT HORIZONTAL)**
- The three spokes must be STACKED VERTICALLY (one on top of the other)
- Spoke A at top, Spoke B in middle, Spoke C at bottom
- Each spoke is a separate, independent container
- NO arrows connecting spokes to each other - they are completely isolated

**DATA FLOW:**
- Hub sends data to each spoke independently (three separate arrows from Hub)
- Each spoke sends data to its downstream tool independently
- Spokes do NOT connect to each other in any way

---

## DIAGRAM CONTENT (LEFT TO RIGHT)

**SOURCE SYSTEMS (Left edge)**
Two stacked gray boxes, vertically aligned:
- "SAP ERP" - medium weight, navy
- "POS Systems" - medium weight, navy
Box styling: Light gray (#F0F0F0), 1px solid #D0D0D0 border, 4px corner radius
Arrow: Single clean arrow (muted green #4CAF50) pointing right toward Hub

**SNOWFLAKE HUB (Left-center) - CONTAINS SOURCE-ALIGNED DATA PRODUCTS**
Container with light blue background (#F8FBFD), 2px solid #0066CC border, 6px corner radius
- Label above container: "HUB" - caps, gray
- Snowflake logo (official) left-aligned
- Title: "Snowflake Data Warehouse" - bold, navy
- Subtitle: "Centralized Ingestion & Source-Aligned Products" - gray

Internal structure (top to bottom):

**Raw Data Layer section:**
- Section label: "Raw Data Layer" - gray
- Two stacked boxes:
  - "Sales Raw Data" - small gray box
  - "Inventory Raw Data" - small gray box

**Source-Aligned Data Products section (served from Hub):**
- Section label: "Source-Aligned Data Products" - bold, navy
- Green dot + "Governed" label - muted green
- Two boxes side by side, PERFECTLY ALIGNED:
  - Left box: "Sales Data Product" - bold, "Conformed sales tables" - gray, light green border (#4CAF50)
  - Right box: "Inventory Data Product" - bold, "Stock levels • Warehouse data" - gray, light green border (#4CAF50)
- Footer: "Enterprise-governed, source-aligned" - italic, muted green

**THREE SEPARATE ARROWS from Hub:** One arrow to each spoke (Spoke A, Spoke B, Spoke C) - arrows do NOT connect to each other

**ISOLATED SPOKES (Center - VERTICALLY STACKED)**
Section label: "SNOWFLAKE SPOKES - ISOLATED BUSINESS UNIT MODELING" - navy

**CRITICAL: Stack these three spokes VERTICALLY (top to bottom), NOT horizontally. Each spoke is completely separate with NO arrows connecting them to each other.**

**SPOKE A: Sales Team Environment (TOP position)**
- Container: White background, 2px solid #0066CC border, 6px corner radius
- Label: "SPOKE A" - caps, gray
- Title: "Sales Team" - bold, navy
- Incoming arrow from Hub (labeled: "Receives Sales Data Product")

**Semantic Logic section (ONLY content inside spoke):**
- Section Label: "Semantic Logic (Applied in Spoke)" - #B71C1C
- Two boxes side by side, PERFECTLY ALIGNED:
  - Left box: Snowflake logo, "SQL Scripts" - bold, "Transformation logic" - gray, red border 1px solid #DC3545
  - Right box: "Custom Metrics" - bold, "Team-specific definitions" - gray, red border 1px solid #DC3545
- Footer: "Own semantic definitions - no shared standards" - italic, #B71C1C
- Output arrow: Points right to Microsoft Fabric

**SPOKE B: Supply Chain Environment (MIDDLE position)**
- Container: White background, 2px solid #0066CC border, 6px corner radius (SAME dimensions as Spoke A)
- Label: "SPOKE B" - caps, gray
- Title: "Supply Chain Team" - bold, navy
- Incoming arrow from Hub (labeled: "Receives Inventory Data Product")

**Semantic Logic section (ONLY content inside spoke):**
- Section Label: "Semantic Logic (Applied in Spoke)" - #B71C1C
- Two boxes side by side, PERFECTLY ALIGNED (matching Spoke A layout exactly):
  - Left box: Snowflake logo, "SQL Scripts" - bold, "Different transformations" - gray, red border 1px solid #DC3545
  - Right box: "Custom Metrics" - bold, "Conflicting definitions" - gray, red border 1px solid #DC3545
- Footer: "Own semantic definitions - no shared standards" - italic, #B71C1C
- Output arrow: Points right to Microsoft Fabric

**SPOKE C: Palantir Foundry Environment (BOTTOM position)**
- Container: White background, 2px solid #0066CC border, 6px corner radius (SAME dimensions as Spoke A and B)
- Label: "SPOKE C" - caps, gray
- Palantir logo (official)
- Title: "Palantir Foundry" - bold, navy
- Incoming arrow from Hub (labeled: "Receives Data Products")

**Semantic Logic section (ONLY content inside spoke):**
- Section Label: "Foundry Modeling (Applied in Spoke)" - #B71C1C
- Two boxes side by side, PERFECTLY ALIGNED (matching other spokes):
  - Left box: "Foundry Transforms" - bold, "Pipeline logic" - gray, red border 1px solid #DC3545
  - Right box: "Custom Objects" - bold, "Foundry-specific definitions" - gray, red border 1px solid #DC3545
- Footer: "Own semantic definitions - no shared standards" - italic, #B71C1C
- Output arrow: Points right to Palantir Ontology

**ISOLATION INDICATOR (positioned to the side of the stacked spokes, NOT between them):**
- Broken chain icon
- Text: "No shared semantics" - #DC3545
- This is a label/annotation, NOT an arrow connecting the spokes

**MISSING LAYER (below all three stacked spokes):**
- Dashed border box (2px dashed #DC3545), light red tint background (#FEF2F2)
- "Consumer-Aligned Products" - bold, #B71C1C
- "Enterprise Semantic Layer" - gray
- "NOT IMPLEMENTED" - bold, #DC3545
- Warning icon (⚠)

**DOWNSTREAM CONSUMPTION (Right side)**
Section label: "Downstream Consumption" - navy

Two tool boxes, vertically aligned:

Box A: Microsoft Fabric (receives from Spokes A & B)
- 2px solid #DC3545 border, white background
- Microsoft Fabric logo (official)
- "Microsoft Fabric" - bold, navy
- Nested inside: Power BI logo + "Power BI Semantic Models"
- "Receives inconsistent definitions" - gray
- Incoming arrows from Spoke A and Spoke B

Box B: Palantir Ontology (receives from Spoke C only)
- 2px solid #DC3545 border, white background
- Palantir logo (official)
- "Palantir Ontology" - bold, navy
- "Discovery layer" - gray
- "Receives Foundry-modeled data" - gray
- Incoming arrow from Spoke C (Palantir Foundry) only

**"Same Question, Different Answers" section below tool boxes:**
- "Q: What is Total Revenue?" - navy, centered
- Three answer boxes horizontally aligned, subtle red border:
  - "$142M" (Spoke A)
  - "$147M" (Spoke B)
  - "$139M" (Palantir)

**CONSEQUENCE SECTION (Full width, bottom)**
Light gray background (#F5F5F5) with 4px red left border accent (#DC3545)

Left side:
- "NO ENTERPRISE SOURCE OF TRUTH" - bold, #B71C1C
- "Hub serves source-aligned products → Spokes (incl. Foundry) apply fragmented semantics → Inconsistent exports" - navy

Right side:
- "Business Impact" - bold caps, gray
- Three bullet points (navy):
  • "Conflicting executive reports"
  • "No trusted metrics for decisions"
  • "Governance debt accumulating"

---

## VISUAL RULES

✅ DO:
- STACK the three spokes VERTICALLY (Spoke A top, Spoke B middle, Spoke C bottom)
- Keep each spoke completely ISOLATED - no arrows connecting spokes to each other
- Show Source-Aligned Data Products INSIDE the Hub (served from Hub)
- Show ONLY Semantic Logic/Modeling INSIDE each spoke
- Show Palantir Foundry as a spoke that feeds into Palantir Ontology
- Include Snowflake logo with SQL Scripts boxes inside Spokes A and B
- Include Palantir logo in both Spoke C (Foundry) and Palantir Ontology box
- Include Microsoft Fabric logo in the Fabric box
- Show Power BI as nested WITHIN Microsoft Fabric
- PERFECTLY ALIGN all boxes
- Use consistent spacing throughout
- Show clear data flow: Hub serves products → Each spoke independently receives and applies semantics → Each spoke independently exports to its downstream tool

❌ DO NOT:
- Arrange spokes horizontally (they must be VERTICALLY STACKED)
- Draw any arrows connecting spokes to each other
- Place Data Products inside the Spokes (they come FROM the Hub)
- Render any section headers, layout instructions, or design specifications as visible text
- Display any measurements or spacing values as visible text
- Have jumbled or overlapping boxes inside the spokes
- Have any boxes slightly misaligned
- Show Palantir Ontology receiving directly from the Hub (it receives from Foundry spoke)