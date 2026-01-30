# AGL Energy Unified Data Intelligence Platform
## Powering AGL's Strategic Priorities

---

## Executive Brief

Create a high-fidelity, enterprise technical reference architecture diagram for AGL Energy's Unified Data Intelligence Platform built on Databricks. This is an intermediate-complexity diagram that balances technical depth with executive readability. It shows the complete data platform architecture including personas, tools, core platform capabilities, governance, storage, and multi-cloud foundations, while maintaining visual clarity for stakeholder presentations.

---

## Visual Style & Brand Identity

### Design Language
- Style: Professional enterprise engineering schematic with modern flat 2D vector graphics
- Aesthetic: Clean, high-contrast, corporate technical diagram
- Background: Clean white (#FFFFFF)
- Layout orientation: Landscape 16:9 optimized for presentations

### AGL Brand Color Palette

Primary Colors:
- AGL Deep Blue: #001CB0 - Primary headers and structural elements
- AGL Navy: #1C355E - Secondary borders and text
- White: #FFFFFF - Background and card backgrounds

Accent Colors:
- Databricks Orange: #FF3621 - Core platform components
- AWS Orange: #F18A00 - AWS cloud section
- Azure Blue: #0078D4 - Azure cloud section
- Success Green: #00A651 - Governance indicators
- Light Grey: #E5E5E5 - Supporting infrastructure

Typography:
- Headers: Bold sans-serif in AGL Deep Blue (#001CB0)
- Subheaders: Semibold sans-serif in AGL Navy (#1C355E)
- Body text: Regular sans-serif, high contrast, 10-12pt

---

## Composition & Hierarchical Layout

The diagram uses a stacked layer architecture (top-to-bottom) with 8 distinct horizontal layers. Each layer is clearly separated with subtle borders and whitespace.

---

### LAYER 0: Title & Logo Bar (Top)
Visual treatment: Thin bar spanning full width

Left side:
- AGL logo (small, proportional)
- Text: "AGL Energy Unified Data Intelligence Platform"
- Font: Bold, AGL Deep Blue (#001CB0)

Right side:
- Text: "Powered by Databricks"
- Databricks logo (small)
- Font: Regular, AGL Navy (#1C355E)

Background: White with subtle bottom border in Light Grey

---

### LAYER 1: Business Context Bar
Visual treatment: Horizontal bar divided into 4 equal segments

Content (left to right):
1. Customer Markets
   - Subtext: "NPS +20 Target"
2. Energy Assets
   - Subtext: "Safety & Reliability"
3. Energy Markets
   - Subtext: "Risk Hedging"
4. Strategy & Sustainability
   - Subtext: "ESG Reporting"

Visual styling:
- Background: AGL Deep Blue (#001CB0) at 20% opacity
- Text: AGL Navy (#1C355E), bold headers with regular subtext
- Vertical dividers: Light grey between segments
- Small relevant icons per segment (optional)

---

### LAYER 2: Persona Layer
Visual treatment: Horizontal row of 5 persona cards

Personas (left to right):
1. Data Engineer
2. ML Engineer
3. Data Scientist
4. Business Analyst
5. App Developer

Visual styling per card:
- Simple icon above label (line art style)
- Icon color: AGL Navy (#1C355E)
- Background: White
- Border: 1px solid AGL Navy (#1C355E)
- Small downward arrow below each card pointing to Layer 3

---

### LAYER 3: Tools & Access Layer
Visual treatment: Single horizontal container divided into 3 sections

Section 1: Development Tools
- Label: "ETL & Data Science"
- Content: Databricks Notebooks, VS Code, Python/SQL
- Icon: Code symbol

Section 2: Analytics Tools
- Label: "BI & Visualization"
- Content: Power BI, Tableau, Databricks SQL
- Icon: Chart symbol

Section 3: AI Applications
- Label: "Data & AI Apps"
- Content: Agent Bricks Gateway, Custom Apps
- Icon: App symbol

Visual styling:
- Container background: White
- Border: 2px solid AGL Navy (#1C355E)
- Section dividers: Vertical light grey lines
- Section headers: AGL Deep Blue (#001CB0)

---

### LAYER 4: Databricks Platform Core (THE HERO ELEMENT)
Visual treatment: Large central container with prominent header

Container Header:
- Text: "Databricks Data Intelligence Platform"
- Background: Databricks Orange (#FF3621) gradient bar
- Databricks logo on left side
- Text color: White

Orchestration Bar (inside container, top):
- Label: "Lakeflow Jobs & Workflows"
- Background: Light Grey (#E5E5E5)
- Spans full width of container
- Icon: Workflow diagram

Four Vertical Columns (inside container, main area):

Column 1: Lakeflow
- Icon: Flowing streams symbol
- Label: "Lakeflow"
- Subtext: "Ingest, ETL & Streaming"
- Key components listed:
  - Lakeflow Connect
  - Declarative Pipelines
  - Streaming Tables
- Background: Light orange tint
- Border: 1px solid AGL Navy

Column 2: Databricks AI
- Icon: AI brain symbol
- Label: "Databricks AI"
- Subtext: "Data Science & AI"
- Key components listed:
  - Agent Bricks (with small star indicator)
  - Model Training
  - Vector Search
- Background: Light red tint
- Border: 1px solid AGL Navy

Column 3: Databricks SQL
- Icon: Database symbol
- Label: "Databricks SQL"
- Subtext: "Data Warehousing"
- Key components listed:
  - Serverless SQL
  - AI Assistant
  - Dashboards
- Background: Light blue tint
- Border: 1px solid AGL Navy

Column 4: Lakebase
- Icon: Postgres/database layers symbol
- Label: "Lakebase"
- Subtext: "Serverless Postgres"
- Key components listed:
  - Transactional Workloads
  - PostgreSQL Compatible
  - Low Latency
- Background: Light purple tint
- Border: 1px solid AGL Navy

Intelligence Bar (inside container, bottom):
- Label: "Intelligence Engine - Generative AI & Agentic Workflow"
- Background: Databricks Orange (#FF3621) at 15% opacity
- Spans full width of container

Visual styling:
- Main container border: 3px solid Databricks Orange (#FF3621)
- Internal spacing: Generous padding between elements
- This is the largest visual element in the diagram
- Four equal-width columns with consistent spacing

---

### LAYER 5: Unified Governance Layer
Visual treatment: Full-width horizontal bar with right-side extension

Main bar:
- Label: "Unity Catalog - Unified Security, Governance & Data Lineage"
- Unity Catalog logo (use uc-logo.png) on left side
- Background: AGL Deep Blue (#001CB0) at 25% opacity
- Border: 2px solid AGL Deep Blue (#001CB0)
- Icons: Shield, lock, and lineage tree symbols
- Text: AGL Navy (#1C355E)

Right-side connected box:
- Label: "AGL myIdentity (Entra ID)"
- Background: White
- Border: 1px solid AGL Navy (#1C355E)
- Connected arrow labeled "SSO & RBAC"
- Icon: User badge with key

---

### LAYER 6: Unified Storage Layer
Visual treatment: Full-width horizontal bar

Main content:
- Label: "Delta Lake - Unified Open Data Storage"
- Subtext: "ACID, Time Travel, Versioning"
- Background: Light Grey (#E5E5E5)
- Border: 1px solid AGL Navy (#1C355E)

Three inline storage format indicators:
- Delta Lake logo/icon (primary, larger)
- Iceberg logo/icon
- Postgres logo/icon (Lakebase)

Right side annotation box:
- Label: "Asset Telemetry"
- Content: "Liddell/Tomago Battery Data, Bayswater SCADA, Spot Prices"
- Background: White
- Border: 1px dashed AGL Navy (#1C355E)
- Font: Small, italicized

Visual styling:
- Delta symbol icon on left
- Storage format icons evenly spaced
- Clean horizontal layout
- Postgres icon connects conceptually to Lakebase in Layer 4

---

### LAYER 7: Multi-Cloud Infrastructure
Visual treatment: Two side-by-side containers of equal width

Container A: Customer Cloud (AWS) - Left side
- Header background: AWS Orange (#F18A00)
- Header text: "Customer Cloud (AWS) - Retail & Digital"
- Border: 2px solid AWS Orange
- Content (icon grid):
  - Salesforce (with logo/icon)
  - Kaluza (use kaluza-logo.png) - Energy flexibility platform
  - Amazon Connect (with logo/icon)
  - Amazon Kinesis (with logo/icon)
  - Amazon S3 (with logo/icon)
- Background: White
- Icons arranged in grid layout

Container B: Operational Cloud (Azure) - Right side
- Header background: Azure Blue (#0078D4)
- Header text: "Operational Cloud (Azure) - Energy Assets"
- Border: 2px solid Azure Blue
- Content (icon grid):
  - SAP S/4HANA (with logo/icon)
  - Azure Data Lake Storage Gen2 (with logo/icon)
  - Ignition Gateway (with logo/icon)
  - Ignition Gateway (with icon)
- Background: White
- Icons arranged in 2x2 grid

Connecting arrows:
- Upward arrows from both containers to Layer 6 (Storage)
- Label on arrows: "Data Ingestion"
- Arrow color: AGL Navy (#1C355E)

---

### LAYER 8: Data Operations Footer
Visual treatment: Horizontal bar with connected mini-boxes

Main bar:
- Label: "Data Operations & Supervision Plane"
- Background: AGL Navy (#1C355E) at 10% opacity
- Border: 1px solid AGL Navy

Connected boxes (left to right):
1. Data Quality
2. Observability
3. FinOps
4. Policy Management
5. Access Control
6. Model Governance
7. Data Lineage
8. Data Catalogue

Visual styling per box:
- Small icon + label (2-3 words)
- Background: White
- Border: 1px solid Success Green (#00A651)
- Boxes connected with dotted lines
- Even spacing across width

---

### RIGHT-SIDE PANEL: Consumption Zone (Vertical Panel)
Visual treatment: Vertical column spanning Layers 3-5 on far right

Panel header:
- Label: "Consumption Zone"
- Background: AGL Deep Blue (#001CB0) vertical gradient bar
- Text orientation: Vertical or angled 45 degrees

Stacked boxes (top to bottom):
1. Power BI Dashboards
   - Icon: Power BI logo
   - Arrow from DBSQL column

2. Custom Applications
   - Icon: Mobile + web symbol
   - Arrow from Lakeflow column

3. AI Agents
   - Icon: Robot symbol
   - Arrow from Agent Bricks
   - Note: "Built with Agent Bricks"

4. Delta Sharing
   - Icon: Share symbol
   - Arrow from Unity Catalog
   - Note: "Secure external sharing"

Visual styling per box:
- Background: White
- Border: 1px solid AGL Navy (#1C355E)
- Compact layout with icon + label + subtext

---

### LEFT-SIDE ANNOTATION: Process Flow Chevrons
Visual treatment: Top-left chevron-style process indicator

Chevrons (left to right):
CAPTURE | PRODUCE | SHARE | CONSUME

Visual styling:
- Background: AGL Navy (#1C355E)
- Text: White, bold
- Chevron arrows pointing right
- Overarching label above: "GOVERN" spanning all chevrons
- Font size: Medium, bold

---

## Key Visual Design Principles

1. Hierarchy: Layer 4 (Databricks Platform) is the largest element and visual focal point
2. Color discipline: Use AGL blue for structure, Databricks orange for platform core only
3. Whitespace: Minimum 20px padding between layers for clarity
4. Arrows: Only show critical data flow paths (Cloud → Storage → Platform → Consumption)
5. Icons: Simple line art, 2-color maximum, consistent style throughout
6. Legibility: All text readable at 1920x1080 resolution
7. Balance: Four-column platform layout with right-side Consumption Zone as accent
8. Simplicity: More detailed than simplified version but cleaner than comprehensive version

---

## Critical Data Flow Arrows

Include these specific directional arrows:
1. Upward arrows: Multi-Cloud Layer → Storage Layer (labeled "Data Ingestion via Lakeflow Connect")
2. Upward arrows: Storage Layer → Platform Core (labeled "Unified Access")
3. Horizontal arrows: Platform Core → Right-side Consumption Zone (per specific tool)
4. Downward arrows: Persona Layer → Tools Layer (labeled "Access via")
5. Vertical connector: Unity Catalog → Platform Core (labeled "Governance")
6. Subtle connector: Postgres storage icon (Layer 6) → Lakebase column (Layer 4) with dashed line

Arrow styling:
- Width: 2-3px
- Color: AGL Navy (#1C355E)
- Style: Solid lines for primary flows, dashed for governance/control
- Arrowheads: Simple triangle style

---

## Technical Annotations

Key terminology labels to include:
- "Lakehouse Architecture" (near Storage Layer)
- "Serverless Compute" (near Lakeflow Jobs)
- "Unified Governance" (near Unity Catalog)
- "Multi-Cloud Data Platform" (near Infrastructure Layer)
- "Zero-Copy Sharing" (near Delta Sharing)
- "Agentic AI" (near Agent Bricks)
- "Transactional & Analytical" (near Lakebase)

Placement: Small labels in light grey, positioned near relevant components

---

## Content Accuracy Checklist

- Agent Bricks prominently featured in Databricks AI column
- Lakeflow with Connect, Pipelines, and Jobs components
- Unity Catalog as governance spine
- Agent Bricks Gateway in Tools layer
- Delta Sharing in Consumption Zone
- DBSQL with serverless capabilities
- Lakebase as fourth platform pillar for transactional PostgreSQL workloads
- Delta Lake, Iceberg, and Postgres (Lakebase) storage formats in Storage Layer
- Multi-cloud (AWS for customer, Azure for operations)
- AGL business context (Customer Markets, Energy Assets, Energy Markets, Strategy & Sustainability)
- AGL-specific telemetry data examples (Liddell, Tomago, Bayswater, SCADA)
- All 2026 Databricks features and current terminology

---

## Output Specifications

- Format: PNG or SVG (vector preferred)
- Resolution: Minimum 1920x1080 (Full HD), ideally 2560x1440 (2K)
- Aspect ratio: 16:9 landscape
- File naming: AGL_Databricks_Intermediate_Architecture_2026.png
- Optimization: Suitable for PowerPoint presentations and PDF export

---

## Success Criteria

This intermediate diagram succeeds if:
1. Contains more architectural detail than the simplified version (includes personas, tools, operations plane)
2. Remains cleaner and more scannable than the comprehensive version (fewer sub-components per layer)
3. Executive can understand platform value in 45-60 seconds
4. Solutions architect can use it for technical discussions
5. Clearly shows AGL brand identity and energy sector context
6. Accurately represents 2026 Databricks architecture including all four platform pillars (Lakeflow, AI, SQL, Lakebase)
7. Data flow is intuitive and clearly marked with arrows
8. All key stakeholders can identify their role and tools
9. Lakebase is clearly positioned as the transactional/operational database layer complementing analytical workloads

---

This prompt creates an intermediate-complexity reference architecture that bridges the gap between the simplified executive summary and the comprehensive technical blueprint, optimized for versatile stakeholder communication.
