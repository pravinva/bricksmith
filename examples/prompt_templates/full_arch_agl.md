# AGL Energy Unified Data Intelligence Platform
## Powering AGL's Strategic Priorities

---

## Executive Brief

Create a high-fidelity, enterprise-grade technical reference architecture diagram for AGL Energy's Unified Data Intelligence Platform built on Databricks Data Intelligence Platform (2026). This diagram is designed for executive stakeholder communication and technical enablement, combining the governance-first medallion architecture framework with AGL's multi-cloud, multi-domain business reality. The visual must reflect AGL's 180+ year heritage as Australia's trusted energy provider while showcasing cutting-edge 2026 Databricks capabilities including Agent Bricks, Lakeflow, and Unity Catalog.

---

## Visual Style & Brand Identity

### Design Language
- Style: Conservative enterprise engineering blueprint with modern flat 2D vector graphics
- Aesthetic: Professional, high-contrast, technical precision—evokes trust, reliability, and innovation
- Background: Clean white or very light grey (#F8F8F8)
- Layout orientation: Landscape (16:9 or similar) optimized for presentation decks

### AGL Brand Color Palette (Strict Compliance Required)

Primary Colors:
- AGL Deep Blue: #001CB0 (International Klein Blue) — Primary structural elements, headers, key containers
- AGL Navy: #1C355E (RGB: 28, 53, 94) — Secondary structural elements, text, borders
- White: #FFFFFF — Background, negative space, contrast areas

Accent Colors:
- Databricks Red: #FF3621 — Core Databricks platform engine/components only
- Energetic Orange: #F18A00 — AWS cloud elements, energy/action indicators
- Azure Blue: #0078D4 — Azure cloud elements
- Success Green: #00A651 — Governance checkpoints, data quality indicators
- Warm Grey: #B2B2B2 — Supporting infrastructure, dividers

Typography:
- Headers: Bold sans-serif (e.g., Helvetica Bold, Arial Black) in AGL Deep Blue (#001CB0)
- Subheaders: Semibold sans-serif in AGL Navy (#1C355E)
- Body text: Regular sans-serif, 10-12pt, high contrast
- Labels: Clean, legible, never cluttered

---

## Composition & Hierarchical Layout

The diagram uses a stacked layer architecture (top-to-bottom) with horizontal swim lanes and vertical domain columns. Think of it as a wedding cake structure where each layer represents a stage in the data lifecycle and platform capability.

---

### HEADER: Business Context Bar (Top)
Visual treatment: Thin horizontal bar spanning full width, divided into 4 equal segments

Content:
Customer Markets | Energy Assets | Energy Markets | Strategy & Sustainability

- Use subtle vertical dividers
- Each segment: Icon (small, simple) + Label
- Background: Light AGL Navy (#1C355E at 10% opacity)
- Text: AGL Navy (#1C355E)

---

### LAYER 1: Persona Interface — "Who Uses the Platform"
Visual treatment: Row of 5 user persona cards with icons + labels

Personas (left to right):
1. Data Engineer (icon: database + wrench)
2. ML Engineer (icon: brain + code)
3. Data Scientist (icon: chart + microscope)
4. Business Analyst (icon: dashboard + magnifying glass)
5. App Developer (icon: code brackets + mobile)

- Small downward arrows from each persona to Layer 2
- Icons: Simple line art, AGL Navy (#1C355E)
- Background per persona card: White with AGL Deep Blue (#001CB0) border (2px)

---

### LAYER 2: Tools & Access Layer — "How They Connect"
Visual treatment: Horizontal container divided into 3 rounded boxes

Box 1: Development Tools
- Label: "ETL & Data Science Tools"
- Content: Databricks Notebooks | VS Code | Python/SQL | Spark
- Icon: Code editor symbol

Box 2: Analytics & BI Tools
- Label: "BI & Visualization"
- Content: AIBI | Power BI | Databricks SQL
- Icon: Chart/dashboard symbol

Box 3: AI Applications
- Label: "Data & AI Apps"
- Content: Agent Bricks Gateway | Custom Apps | REST APIs
- Icon: App window + AI sparkle

- Container background: White
- Border: AGL Navy (#1C355E), 2px
- Header bar for each box: AGL Deep Blue (#001CB0) at 20% opacity

---

### LAYER 3: Databricks Data Intelligence Platform — THE CORE ENGINE (PRIMARY FOCUS)
Visual treatment: Large central container—this is the hero of the diagram

Container Header:
- Text: "Databricks Data Intelligence Platform"
- Background: Databricks Red (#FF3621) gradient bar
- Databricks logo (small) on left side

Sub-layer 3A: Orchestration (Top bar inside container)
- Full-width horizontal strip
- Label: "Lakeflow Jobs (Orchestration)"
- Background: Light grey (#E5E5E5)
- Icons: Clock + workflow diagram
- Border: Subtle dashed line

Sub-layer 3B: Four Vertical Pillars (The Product Quartet)

Create 3 equal-width vertical columns inside the main container:

Column 1: Lakeflow
- Icon: Flowing streams
- Label: "Lakeflow"
- Subtitle: "Ingest, ETL & Real-time Analytics"
- Components (stacked vertically):
  - Lakeflow Connect (Ingestion)
  - Spark Declarative Pipelines (ETL)
  - Lakeflow Designer (No Code)
  - Zerobus (Real-time Events)

Column 2: Databricks AI
- Icon: AI brain/agent
- Label: "Databricks AI"
- Subtitle: "Data Science & AI"
- Components (stacked vertically):
  - Agent Bricks
  - Foundation Model Serving
  - Vector Search

Column 3: Databricks Serving
- Icon: Database + query
- Label: "Databricks SQL"
- Subtitle: "Data Warehousing"
- Components (stacked vertically):
  - Serverless SQL Warehouses
  - SQL Editor + AI Assistant
  - Dashboards & AI/BI
  - Query Optimization

Column 4: Lakebase
- Icon: PostgreSQL
- Label: "Lakebase"
- Subtitle: "Serverless Postgres"
- Components (stacked vertically):
  - Open Source
  - Separation of Storage/Compute
  - Designed for AI
  - Pay for what you use 

- Background per column: Very light tint of respective color (Lakeflow: light orange, AI: light red, SQL: light blue)
- Border per column: 1px solid AGL Navy (#1C355E)
- Agent Bricks 

Sub-layer 3C: Intelligence Engine (Bottom bar inside container)
- Full-width horizontal strip below the 4 pillars
- Label: "Intelligence Engine (Generative AI, Semantic Layer, Agentic Workflow)"
- Background: Databricks Red (#FF3621) at 15% opacity
- Icons: AI sparkle + network nodes
- Text: "Powered by Agent Bricks & Agent Bricks"

---

### LAYER 4: Unified Governance — "The Security & Trust Layer"
Visual treatment: Full-width horizontal bar with right-side connection

Main bar:
- Label: "Unity Catalog — Unified Security, Governance, Data Lineage & Auditing"
- Unity Catalog logo (use uc-logo.png) on left side
- Background: AGL Deep Blue (#001CB0) at 25% opacity
- Border: 2px solid AGL Deep Blue (#001CB0)
- Icons: Shield + lock + lineage tree

Right-side connected box:
- Label: "AGL myIdentity (Entra ID)"
- Connected with arrow labeled "SSO & RBAC"
- Background: White
- Border: AGL Navy (#1C355E)
- Icon: User badge + key

---

### LAYER 5: Unified Storage — "The Data Lake Foundation"
Visual treatment: Full-width horizontal bar

- Label: "Delta Lake — Unified Open Data Storage (ACID, Time Travel, Versioning)"
- Background: Light grey (#E5E5E5)
- Border: 1px solid AGL Navy (#1C355E)
- Icons: Database layers + delta symbol
- Optional sub-text: "+ Apache Iceberg | Postgres (Lakebase)"

---

### LAYER 6: Multi-Cloud Foundations — "Infrastructure Layer"
Visual treatment: Two large side-by-side containers at the bottom

Container A: Customer Cloud (AWS) — Left side
- Header background: Energetic Orange (#F18A00)
- Header text: "Customer Cloud (AWS) — Retail & Digital"
- Content (icon grid):
  - Salesforce (CRM icon)
  - Kaluza (use kaluza-logo.png) — Energy flexibility platform
  - Amazon Connect (phone icon)
  - Amazon Kinesis (streaming icon)
  - Amazon S3 (bucket icon)
- Border: 2px Energetic Orange

Container B: Operational Cloud (Azure) — Right side
- Header background: Azure Blue (#0078D4)
- Header text: "Operational Cloud (Azure) — Energy Assets"
- Content (icon grid):
  - SAP S/4HANA (ERP icon)
  - Azure Data Lake Storage Gen2 (folder icon)
  - Ignition Gateway
  - Corporate Systems 
- Border: 2px Azure Blue

Connecting arrows:
- Upward arrows from both containers to Layer 5 (Delta Lake)
- Label arrows: "Data Ingestion via Lakeflow Connect"

---

### FOOTER: Data Operations & Supervision Plane — "The Control Tower"
Visual treatment: Wide horizontal bar at very bottom with connected mini-boxes

Label (left side): "Data Operations & Supervision Plane"
- Background: AGL Navy (#1C355E) at 10% opacity
- Border: 1px solid AGL Navy

Mini-boxes (horizontal left to right, not connected):
1. Data Quality (Expectations)
2. Observability (Lakehouse Monitoring)
3. FinOps (System Tables)
4. Policy & Controls Management
5. Access Control (RBAC/ABAC)
6. Model Governance
7. Data Lineage & Audit
8. Data Catalogue (Unity Catalog Search)
9. Test Data Management
10. Metadata Management

- Each box: Small icon + 2-3 word label
- Background per box: White
- Border: 1px solid Success Green (#00A651)
- Connecting lines: Dotted lines in grey

---

### RIGHT-SIDE PANEL: Consumption Zone (Vertical) - CRITICAL COMPONENT
Visual treatment: Vertical column spanning Layers 2–5 on the far right

Panel header:
- Label: "Consumption Zone"
- Background: AGL Deep Blue (#001CB0) gradient vertical bar
- Text orientation: Vertical or angled

Stacked content boxes (top to bottom):
1. Power BI Dashboards
   - Icon: Power BI logo
   - Connection arrow from Layer 3 (DBSQL)

2. Custom Applications
   - Icon: Mobile + web app
   - Connection arrow from Layer 3 (Lakeflow/AI)

3. AI Agents & Copilots
   - Icon: Robot + chat bubble
   - Connection arrow from Layer 3 (Agent Bricks)
   - Callout: "100% from Databricks"

4. Data Sharing (Delta Sharing)
   - Icon: Share symbol + external arrow
   - Connection arrow from Layer 4 (Unity Catalog)
   - Sub-text: "Secure external sharing"

- Background per box: White
- Border: AGL Navy (#1C355E), 1px

---

### LEFT-SIDE ANNOTATION: Data Flow Chevron (Process Phases)
Visual treatment: Top-left chevron-style process flow

Chevrons (left to right):
CAPTURE | PRODUCE | SHARE | CONSUME

- Background: AGL Navy (#1C355E) gradient
- Text: White, bold
- Chevron arrows pointing right
- Optional: Overarching label above: "GOVERN" spanning all 4 chevrons

---

### MEDALLION ARCHITECTURE OVERLAY (Inside Layer 3 — Lakeflow Column)
Visual treatment: Small horizontal mini-diagram inside the Lakeflow pillar

Flow (left to right):
Landing Zone → Raw (Bronze) → Refined (Silver) → Curated (Gold)

- Use small circles or hexagons for each zone
- Color progression:
  - Landing: Light grey
  - Bronze: #CD7F32 (bronze color)
  - Silver: #C0C0C0 (silver color)
  - Gold: #FFD700 (gold color)
- Arrows between zones
- Label above: "Medallion Architecture"

Domain Containers (below medallion):
- 3 small vertical bars labeled: EMD | CM | CORP
- Background: Light AGL Navy (#1C355E at 5%)
- Represents AGL's data domains

---

## Key Visual Design Principles

1. Hierarchy & Flow: Eyes should move top-to-bottom and left-to-right naturally
2. Balance: The Databricks Platform (Layer 3) is the largest visual element—it is the hero
3. Color discipline: Use AGL brand colors for structure; reserve Databricks Red for platform components only
4. Whitespace: Do not cram—allow breathing room between layers
5. Iconography: Simple, consistent line-art icons (2-color max: AGL Navy + accent color)
6. Arrows: Use directional arrows to show data flow and dependencies (not decorative)
7. Callouts: Try highlight 2026 innovations:
   - Agent Bricks 
   - Lakebase 
   - Lakeflow Connect
   - Lakeflow Designer 
   - Zerobus 
8. Legibility: All text must be readable at 1920x1080 resolution when projected

---

## Technical Annotations & Labels

### Key Terminology to Include:
- "Lakehouse Architecture" (near Delta Lake layer)
- "Serverless Compute" (near Lakeflow Jobs)
- "Zero-Copy Data Sharing" (near Delta Sharing)
- "Unified Governance" (near Unity Catalog)
- "Agentic AI" (near Agent Bricks)
- "Multi-Cloud Data Mesh" (near AWS/Azure containers)
- "ACID Transactions" (near Delta Lake)
- "Real-Time Streaming" (near Lakeflow)

### Personas Placement:
- Data Engineers → Lakeflow column
- ML Engineers + Data Scientists → Databricks AI column
- Business Analysts → DBSQL column
- App Developers → Agent Bricks Gateway + Consumption Zone

---

## Optional Enhancements (If Space Permits)

1. Top-right corner: Small AGL logo + "Powered by Databricks Data Intelligence Platform" text
2. Bottom-right corner: Version/date stamp (e.g., "v2.0 | January 2026")
3. Data flow arrows: Visual indicators showing data moving from clouds → storage → platform → consumption
4. Governance checkpoints: Small green checkmarks or shields at Unity Catalog integration points
5. Compliance badges: Small icons for SOC2, ISO 27001, GDPR (in footer near Supervision Plane)

---

## Content Accuracy Checklist

- Agent Bricks featured prominently as 2026 innovation
- Lakeflow (GA December 2025) with Connect, Pipelines, Jobs
- Unity Catalog as central governance spine
- Agent Bricks Gateway for model access
- Delta Sharing for external data sharing
- DBSQL with serverless warehouses and AI Assistant
- Medallion Architecture (Bronze → Silver → Gold)
- Multi-cloud (AWS for customer, Azure for operations)
- AGL business domains (Customer Markets, Energy Assets, Energy Markets, Strategy & Sustainability)
- AGL brand colors (#001CB0 primary, #1C355E secondary)
- 2026-current features (no deprecated terminology)

---

## Final Output Specifications

- Format: PNG or SVG (vector preferred for scalability)
- Resolution: Minimum 1920x1080 (Full HD), ideally 3840x2160 (4K)
- Aspect ratio: 16:9 landscape
- File naming: AGL_Databricks_Reference_Architecture_2026_v2.0.png
- Delivery: Single-page diagram suitable for PowerPoint, PDF export, and large-format printing

---

## Success Criteria

This diagram succeeds if:
1. An AGL executive can understand the platform's business value in 30 seconds
2. A solutions architect can use it to explain technical architecture in a sales meeting
3. It feels unmistakably "AGL" (brand colors, energy sector context)
4. It accurately represents 2026 Databricks capabilities (Agent Bricks, Lakeflow, Unity Catalog)
5. Data flow is intuitive: Sources → Platform → Governance → Consumption
6. All stakeholders (engineers, analysts, data scientists, developers) see "where they fit"

---

This prompt synthesizes the medallion architecture governance framework (Prompt 1), the layered technical stack (Prompt 2), AGL's brand identity, and 2026 Databricks innovations into a single, production-ready reference architecture diagram for Nano Banana Pro.
