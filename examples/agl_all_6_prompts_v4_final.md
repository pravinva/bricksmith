# AGL DATABRICKS RFP – Complete Nano Banana Prompt Suite (v4)
## Six Standalone Prompts – Dual‑Cloud (AWS + Azure), AIBI, Agent Bricks, DBSQL, Metric Views

All prompts follow Nano Banana Pro best practices:
- ✅ Logo Kit embedded at the top of each prompt
- ✅ AWS and Azure logos as explicit cloud markers
- ✅ No filenames shown in diagrams
- ✅ AIBI Dashboards, AIBI Genie, Unity Catalog Metric Views (semantic layer)
- ✅ Agent Bricks mentioned in AI/ML sections
- ✅ Modern data infrastructure inspired (a16z, Azure Databricks reference)
- ✅ RFP-ready language and clarity

---

# PROMPT 1 – Dual‑Cloud Platform Layers (Vertical Stack)

```text
===== LOGO KIT – CRITICAL INSTRUCTIONS (APPLY TO THIS DIAGRAM) =====

You have six uploaded reference images. Treat these as a fixed logo kit and reuse them EXACTLY.

1) "databricks-logo.jpg"        → Databricks brand mark
   - Red three-layer stacked-box icon (no text).

2) "databricks-full.jpg"        → Databricks wordmark
   - Same red brand mark plus the word "databricks" in black.

3) "delta-lake-logo.jpg"        → Delta Lake logo
   - Cyan/teal triangular mark plus the words "Delta Lake".

4) "uc-logo.jpg"                → Unity Catalog logo
   - Pink and yellow ring around a dark blue hexagon, with the words "Unity Catalog".

5) "kaluza_logo_black.jpg"      → Kaluza logo
   - Black three-hexagon mark plus the word "kaluza" in black.

6) "AGL_Energy_logo.svg.jpg"    → AGL logo
   - Cyan/blue radial fan above the word "agl" in black.

CLOUD LOGOS (drawn, not file‑based):

7) AWS logo
   - Standard "aws" wordmark in dark grey with orange curved smile underline.

8) Azure logo
   - Modern flat Azure symbol: blue angular "A" next to "Azure" in dark blue.

CRITICAL RULES:

- ALWAYS reuse uploaded images directly. Do NOT redraw, trace, or approximate any logo.
- Scale logos uniformly only; do NOT change aspect ratio, recolour, crop or add effects.
- NEVER substitute generic icons where a logo is requested.
- Do NOT print file names, extensions or paths in the diagram.
- If you show a label near a logo, use ONLY the brand name: "Databricks", "Delta Lake", "Unity Catalog", "kaluza", "AGL", "AWS", "Azure".
- If unsure, LEAVE THE SPOT BLANK.

===== PROMPT BODY =====

You are a Lead Databricks Solutions Architect with decades of experience designing
compelling reference architectures for RFPs.

Design a VERTICAL, STACKED LAYERED reference architecture diagram showing AGL's Databricks
Data Intelligence Platform (Lakehouse) running on BOTH AWS and Azure.

The diagram should feel like a modern, layered a16z / Azure Databricks architecture:
clean bands, clear separation of concerns, and explicit governance. It will be used
in an RFP response to explain how AGL consolidates data, analytics and AI across
customer, markets, generation and finance.

===== LAYERS & COLUMNS =====

Create FIVE horizontal layers from bottom to top:

1. Cloud Infrastructure
2. Storage & Governance
3. Processing & Intelligence
4. Data Products & Applications
5. Business Outcomes

Across layers 1–4, divide into THREE vertical columns:

- LEFT: AWS
- CENTRE: Databricks Unified Platform
- RIGHT: Azure

Use subtle vertical separators, with colour accents:
- AWS: orange (#FF9900)
- Azure: blue (#0078D4)
- Databricks: slate/red (#1E212D / #EC1C24)

===== HEADER =====

Top header bar (AGL branded):

- Background: AGL cyan→blue gradient.
- Left: Place the AGL logo from the Logo Kit (no text label).
- Right: Title in white, bold:
  "AGL Unified Data & AI Platform – Databricks Lakehouse Across AWS and Azure"
- Subtitle in white:
  "Modern, governed Data Intelligence Platform spanning AWS and Azure for retail, markets,
   generation and finance."
- Optional: On the right side of the header, show small AWS and Azure logos side‑by‑side
  to reinforce dual‑cloud support.

===== LAYER 1 – CLOUD INFRASTRUCTURE =====

AWS column:

- Place the AWS logo at the top of this column as a column header.
- Icons below logo: VPC, EC2, S3, MSK/Kinesis.
- Caption: "Customer‑facing and call‑centre workloads on AWS."

Azure column:

- Place the Azure logo at the top of this column as a column header.
- Icons below logo: Virtual Network, VMs, ADLS Gen2, Event Hubs, IoT Hub.
- Caption: "SAP, enterprise systems and OT/IoT telemetry on Azure."

Databricks centre:

- Place the Databricks brand‑mark logo from the Logo Kit.
- Label: "Databricks Workspaces and Control Plane".
- Subtitle: "Unified workspace experience across AWS and Azure."

===== LAYER 2 – STORAGE & GOVERNANCE =====

AWS column:

- Box: "Delta Lake on S3 – Bronze / Silver / Gold".
- Place the Delta Lake logo from the Logo Kit on the left of the box.
- Text: "Customer, interaction and call‑centre events from kaluza, Salesforce and Amazon Connect."

Azure column:

- Box: "Delta Lake on ADLS Gen2 – Bronze / Silver / Gold".
- Place the same Delta Lake logo on the left.
- Text: "SAP finance and billing, markets data, OT/generation telemetry, enterprise data."

Databricks centre band (spanning both):

- Place the Unity Catalog logo from the Logo Kit on the left.
- Main label: "Unity Catalog – Cross‑Cloud Governance & Semantic Layer".
- Sub‑labels:
  - "Central catalogue and fine‑grained access control"
  - "Lineage, quality, PII detection"
  - "Unity Catalog Metric Views – shared semantic model for AI/BI"
- Arrows upward from both Delta Lake boxes into this band.

===== LAYER 3 – PROCESSING & INTELLIGENCE =====

In the Databricks centre column, three stacked capability boxes:

1) "Data Engineering & Ingestion"
   - "Lakeflow (ingest, ETL, streaming), LDP (Lakeflow Declarative Pipelines),
      Auto Loader, Structured Streaming"
   - Caption: "Batch and streaming pipelines from AWS (kaluza, Salesforce, Amazon Connect)
      and Azure (SAP, OT/IoT, enterprise apps)."

2) "Analytics & AI/BI"
   - "DBSQL, AI/BI Dashboards, AIBI Genie"
   - "Unity Catalog Metric Views as the governed semantic layer"
   - Caption: "Enterprise reporting and agentic business intelligence across AGL."

3) "Agentic AI & Machine Learning"
   - "Agent Bricks – agentic AI and ML"
   - "MLflow, Feature Store, Model Registry, Model Serving"
   - Caption: "Forecasting (demand, price, load), churn and credit risk, contact‑centre
      analytics, asset and outage analytics."

Small badge near this layer: "Same developer experience and governance on AWS and Azure."

===== LAYER 4 – DATA PRODUCTS & APPLICATIONS =====

AWS column (Customer & Operations):

- Group title: "Customer & Call‑Centre Apps on AWS".
- Place the AWS logo as a small badge at the top of this section.
- Place the Kaluza logo next to the label "kaluza – retail energy platform".
- Additional apps:
  - "Salesforce – CRM & sales"
  - "Amazon Connect – cloud contact‑centre and IVR"
- Text: "Customer interactions, billing events, usage data, tickets, service orders."
- Arrows:
  - Down to "Delta Lake on S3".
  - Across to "Data Engineering & Ingestion".
  - Upwards to "AI/BI Dashboards and AIBI Genie" for agentic insights.

Databricks centre column (domain data products):

- Boxes representing logical products:
  - "Customer 360 & Interaction Hub"
  - "Energy Demand & Load Forecasting Layer"
  - "Operational & Asset Insight Layer"
- Caption: "Domain‑aligned, governed data products consumed by apps, AI/BI and Agent Bricks."

Azure column (Enterprise & SAP):

- Group title: "Enterprise and SAP on Azure".
- Place the Azure logo as a small badge at the top of this section.
- Items:
  - "SAP – ERP, billing, market settlement"
  - "Finance and commercial systems"
  - "HR, asset and work management, risk"
  - "OT / generation systems (SCADA, historian, IoT)"
- Text: "Enterprise and financial data, markets data, OT telemetry."
- Arrows:
  - Down to "Delta Lake on ADLS Gen2".
  - Across to "Data Engineering & Ingestion".
  - Upwards to AI/BI and Agent Bricks workloads.

===== LAYER 5 – BUSINESS OUTCOMES =====

Single band at the top with icon + label pairs:

- "Customer experience and NPS uplift"
- "Revenue and margin optimisation"
- "Energy demand and load forecasting accuracy"
- "Regulatory and compliance confidence"
- "Operational efficiency and asset performance"

Each outcome has thin arrows back to relevant data products and AI/BI / Agent Bricks layers.

===== VISUAL STYLE =====

- Aspect ratio: 16:9 landscape.
- Clean, flat vector; subtle layer shadows only.
- Information density similar to modern a16z / Databricks diagrams.
- No filenames; only real logos and business labels.
```

---

# PROMPT 2 – Data Journey with AIBI, Metric Views and Agent Bricks

```text
===== LOGO KIT – CRITICAL INSTRUCTIONS (APPLY TO THIS DIAGRAM) =====

[Use the same Logo Kit block from Prompt 1 – paste it here]

===== PROMPT BODY =====

You are a Lead Databricks Solutions Architect responding to an RFP.

Create a HORIZONTAL LEFT‑TO‑RIGHT DATA JOURNEY diagram that shows how AGL moves data from
AWS and Azure into a governed Databricks Lakehouse, and then into AI/BI Dashboards, AIBI Genie
and Agent Bricks‑powered AI.

The style should resemble modern "Emerging Architectures for Modern Data Infrastructure"
flows and the Azure Databricks reference: five phases, three swim lanes.

===== STRUCTURE =====

Three swim lanes:

- Top lane: "AWS (with AWS logo) – sources and sinks"
  Place the AWS logo at the left of the lane title as a lane badge.

- Middle lane: "Databricks Data Intelligence Platform"

- Bottom lane: "Azure (with Azure logo) – sources and sinks"
  Place the Azure logo at the left of the lane title as a lane badge.

Five vertical phases:

1. Ingest
2. Transform
3. Govern
4. Analyse (AI/BI)
5. Activate (Agentic AI & Operations)

Alternate phase shading (light grey / white).

===== LOGO USE =====

- Databricks wordmark lightly in the background of the middle lane.
- Delta Lake logo in the Transform phase.
- Unity Catalog logo in the Govern phase.

===== PHASE 1 – INGEST =====

AWS lane:
- "kaluza events", "Salesforce records", "Amazon Connect interactions".
- Services: Kinesis/MSK, DMS, S3.

Azure lane:
- "SAP transactions", "OT / SCADA telemetry", "enterprise systems".
- Services: Event Hubs, Data Factory, Synapse Link, ADLS.

Databricks lane:
- Box: "Ingest with Lakeflow, Auto Loader & LDP".
- Converging arrows from AWS and Azure lanes.

===== PHASE 2 – TRANSFORM =====

Databricks lane:

- Wide box:
  - Place the Delta Lake logo on the left.
  - Labels:
    - "Delta Lake Medallion Architecture (Bronze → Silver → Gold)"
    - "Apache Spark & Photon – batch and streaming"
    - "Lakeflow Declarative Pipelines (LDP), Jobs, Structured Streaming"

Data flows left‑to‑right through Bronze, Silver, Gold.

===== PHASE 3 – GOVERN =====

Databricks lane:

- Wide box:
  - Place the Unity Catalog logo on the left.
  - Main text: "Unity Catalog – Single Governance & Semantic Layer".
  - Subtext:
    - "Central catalogue and access control"
    - "Lineage and quality checks"
    - "Unity Catalog Metric Views – governed semantic model for AI/BI".

Small arrows from AWS and Azure lanes into this box showing both clouds' data governed together.

===== PHASE 4 – ANALYSE (AI/BI) =====

Databricks lane:

- Box: "AI/BI Dashboards and AIBI Genie".
- Inside:
  - "DBSQL queries over Delta Lake"
  - "Unity Catalog Metric Views providing the semantic layer"
  - "AI‑assisted analysis via AIBI Genie"
- Outputs to:
  - "Executive dashboards"
  - "Operational AI/BI dashboards for call‑centre and operations"
  - "Self‑service business users".

AWS and Azure lanes can show small "Embedded dashboards / reports" fed from the middle lane.

===== PHASE 5 – ACTIVATE (AGENTIC AI & OPERATIONS) =====

Databricks lane:

- Box: "Agent Bricks, MLflow, Feature Store & Model Serving".
- Inside:
  - "Agent Bricks orchestrating agentic AI workflows"
  - "MLflow experiments & Model Registry"
  - "Feature Store"
  - "Real‑time and batch Model Serving"

Outbound arrows:

- To AWS lane:
  - "kaluza – personalised offers and tariff recommendations"
  - "Salesforce – next‑best‑action, lead scoring"
  - "Amazon Connect – agent assist, routing, sentiment alerts"

- To Azure lane:
  - "SAP – financial forecasts, revenue assurance"
  - "OT systems – predictive maintenance"
  - "Regulatory marts – pre‑populated reports".

Right margin: outcome list:
- "Better decisions via AI/BI and Genie"
- "Agentic automation with Agent Bricks"
- "Cross‑cloud governance and trust."

===== STYLE =====

- 16:9 landscape, rounded Databricks components, sharper cloud services.
- AWS orange / Azure blue / Databricks slate+red palette.
- No filenames, only product names and flows.
```

---

# PROMPT 3 – Concentric Ecosystem (Dual‑Cloud Rings)

```text
===== LOGO KIT – CRITICAL INSTRUCTIONS (APPLY TO THIS DIAGRAM) =====

[Use the same Logo Kit block from Prompt 1 – paste it here]

===== PROMPT BODY =====

You are a Lead Databricks Solutions Architect.

Design a CONCENTRIC CIRCLE / TARGET diagram showing AGL's Databricks Lakehouse at the
centre, shared platform services around it, then AWS/Azure systems split left/right,
and finally business domains around the outside.

The diagram should follow modern platform ecosystem patterns: clean rings, clear segmentation,
balanced labels. Do NOT write "Ring 1 / Ring 2 / Ring 3 / Ring 4" in the diagram; use only
business and technical labels.

===== HIGH‑LEVEL RING STRUCTURE =====

From inside to outside:

- Inner core: "AGL Unified Energy Data Platform"
- Ring 2: "Shared Databricks Platform Services"
- Ring 3: "Cloud Systems – AWS (left) vs Azure (right)"
- Outer ring: "Business Domains & Data Products"

===== LOGO PLACEMENT =====

- Place the Databricks brand mark logo from the Logo Kit in the centre of the inner core.
- Place the Delta Lake logo from the Logo Kit on the storage slice of the core.
- Place the Unity Catalog logo from the Logo Kit on the governance slice of the core.
- Place the Kaluza logo from the Logo Kit inside the "Retail Energy and Customer" outer segment.
- Place the AGL logo from the Logo Kit in the top‑left header area, outside the rings.
- Place the AWS logo as a badge in the outer perimeter of the AWS half of Ring 3.
- Place the Azure logo as a badge in the outer perimeter of the Azure half of Ring 3.

Never show logo filenames as text.

===== INNER CORE =====

Solid circle with:
- Main text: "AGL Unified Energy Data Platform"
- Subtitle: "Databricks Lakehouse on AWS and Azure"

Slice the inner core into three radial segments (120 degrees each):

1) Storage:
   - Next to the Delta Lake logo.
   - Label: "Delta Lake – S3 (AWS) and ADLS Gen2 (Azure)"

2) Processing:
   - Label: "Apache Spark, Photon, SQL Warehouses"

3) Governance:
   - Next to the Unity Catalog logo.
   - Label: "Unity Catalog – Cross‑cloud governance, lineage, security"
   - Sub‑text: "Metric Views provide the unified semantic layer"

===== RING 2 – SHARED PLATFORM SERVICES =====

Complete ring divided into three equal sectors (120 degrees each):

Sector 1 – "Data Engineering & Ingestion" (top‑left):
- "Lakeflow, LDP, Auto Loader, Structured Streaming"
- "Batch and streaming pipelines from AWS and Azure"

Sector 2 – "Analytics & AI/BI" (bottom):
- "DBSQL, AI/BI Dashboards, AIBI Genie"
- "Unity Catalog Metric Views as governed semantic layer"
- "Enterprise reporting and self‑service AI/BI"

Sector 3 – "Agentic AI & ML for Energy" (top‑right):
- "Agent Bricks"
- "MLflow, Feature Store, Model Registry, Serving"
- "Forecasting, churn, credit, outage and asset‑health agents"

===== RING 3 – CLOUD SYSTEMS (AWS LEFT, AZURE RIGHT) =====

Split this ring vertically into left and right halves with a subtle vertical divider at
12 o'clock and 6 o'clock.

Left half (AWS – orange accents):

- Place the AWS logo as a small badge near the outer edge of the AWS half, roughly at the mid‑angle.
- Title: "Customer and Call‑Centre Apps (AWS)"
- Inside:
  - Place the Kaluza logo from the Logo Kit near or in the AWS section (but reserve the main
    Kaluza placement for the outer ring).
  - "Salesforce"
  - "Amazon Connect"
- Text: "Customer interactions, billing events, usage data, tickets, service orders"
- Icons around perimeter: S3, Kinesis, MSK pointing inward to Ring 2.

Right half (Azure – blue accents):

- Place the Azure logo as a small badge near the outer edge of the Azure half, roughly at the mid‑angle.
  Do NOT use the SAP logo here; SAP remains an application box inside the Azure half.
- Title: "Enterprise and SAP (Azure)"
- Inside:
  - "SAP – ERP, Billing, Market Settlement"
  - "Finance and commercial systems"
  - "HR, asset and work management, risk"
  - "Enterprise SaaS (Workday and HRIS)"
- Text: "Financials, contracts, pricing, market data, enterprise HR and OT telemetry"
- Icons: ADLS, Event Hubs, Data Factory, Azure IoT Hub/Edge (for OT/IoT from generation sites).

===== OUTER RING – BUSINESS DOMAINS =====

Five evenly spaced segments around the circle (72 degrees each).
Do NOT show the text "Ring 4" anywhere; use only business domain names.

Distribute clockwise from top:

Segment 1 – "Retail Energy and Customer" (top or top‑right):

- Colour: Light blue‑green pastel.
- Place the Kaluza logo here (if not already prominently used in Ring 3).
- Text: "Tariff optimisation, churn prediction, customer 360, campaign analytics"
- Small AWS‑orange chip to show AWS‑anchored apps.
- Arrow curves inward toward inner core.

Segment 2 – "Customer Operations and Contact Centre" (right or lower‑right):

- Colour: Light orange pastel.
- Text: "NPS and complaints analytics, agent performance, call reason analysis"
- AWS‑orange chip.
- Arrow curves inward.

Segment 3 – "Markets, Trading and Risk" (bottom or bottom‑right):

- Colour: Light purple pastel.
- Text: "Price forecasting, risk analytics, hedging performance, AEMO and market data"
- Neutral / dual‑cloud chip.
- Arrow curves inward.

Segment 4 – "Generation and Asset Operations" (bottom‑left or left):

- Colour: Light amber pastel.
- Text: "Plant performance, outage analytics, predictive maintenance, IoT and SCADA telemetry"
- Azure‑blue chip to show OT/IoT telemetry lands in Azure.
- Small IoT icon (sensor symbol) coloured with Azure accents.
- Arrow curves inward.

Segment 5 – "Finance and Regulatory Reporting" (left or upper‑left):

- Colour: Light slate/grey pastel.
- Text: "Financial reporting, regulatory packs, audit and compliance analytics"
- Azure‑blue chip.
- Arrow curves inward.

===== LEGEND =====

Small legend bottom‑right:

- [Dark slate/red swatch] "Databricks core platform"
- [Orange dot] "AWS‑anchored workloads"
- [Blue dot] "Azure‑anchored workloads"
- [Grey dot] "Cross‑cloud / neutral domains"
- [AWS logo] "AWS infrastructure and apps"
- [Azure logo] "Azure infrastructure and apps"
- [Small IoT icon with blue accent] "OT/IoT telemetry landing on Azure"

===== HEADER =====

- Place the AGL logo from the Logo Kit in the top‑left, outside the rings (10–15% width).
- Centre title in white, bold: "AGL Unified Data & AI Platform – Databricks Lakehouse Across AWS and Azure"
- Subtitle in white: "Customer and call‑centre workloads on AWS; SAP, enterprise systems, and OT/IoT
  on Azure, all governed by a single Databricks Lakehouse with AI/BI and Agent Bricks."

===== STYLE =====

- 16:9 landscape.
- White background, soft drop shadow on inner two rings.
- AWS orange / Azure blue accents on their respective halves of Ring 3.
- Balanced information density similar to modern data‑infra platform diagrams.
- No filenames; logos appear only as graphics with minimal brand text.
```

---

# PROMPT 4 – Three Workload Pillars (Analytics, Real‑Time, Agentic AI)

```text
===== LOGO KIT – CRITICAL INSTRUCTIONS (APPLY TO THIS DIAGRAM) =====

[Use the same Logo Kit block from Prompt 1 – paste it here]

===== PROMPT BODY =====

You are a Lead Databricks Solutions Architect.

Design a THREE‑COLUMN workload pattern diagram showing how the dual‑cloud Databricks
Lakehouse supports:

1. Analytics & AI/BI
2. Real‑Time Operations
3. Agentic AI & Machine Learning

Each column has three layers: Ingestion → Lakehouse Core → Consumption.

At the top‑right of each column, show a small AWS logo and Azure logo side‑by‑side with text
"Runs on AWS and Azure".

===== STRUCTURE =====

Divide canvas into THREE equal vertical columns with consistent layout.

===== COLUMN 1 – ANALYTICS & AI/BI =====

Ingestion:
- "Batch sources: operational DBs, data warehouses, SaaS."

Lakehouse Core:
- Place the Delta Lake logo from the Logo Kit prominently.
- Labels:
  - "Clean Delta tables (Bronze / Silver / Gold)"
  - "Unity Catalog Metric Views as enterprise semantic model"

Consumption:
- "DBSQL, AI/BI Dashboards, AIBI Genie"
- "Power BI, Tableau, Looker"
- Caption: "Governed AI/BI for executives and analysts."

===== COLUMN 2 – REAL‑TIME OPERATIONS =====

Ingestion:
- "Streaming from Kafka/MSK, Event Hubs, APIs, IoT."
- "Amazon Connect, kaluza and Salesforce events."

Lakehouse Core:
- Place the Delta Lake logo from the Logo Kit prominently.
- Labels:
  - "Delta Lake with streaming and ACID transactions"
  - "Fresh Gold tables with real‑time operational facts"

Consumption:
- "Operational dashboards fed by AI/BI"
- "Real‑time APIs and reverse ETL into SaaS"
- Caption: "Always‑on operational decisions."

===== COLUMN 3 – AGENTIC AI & MACHINE LEARNING =====

Ingestion:
- "Training data and features from Lakehouse"
- "Logs and telemetry"

Lakehouse Core:
- Place the Delta Lake logo from the Logo Kit prominently.
- Labels:
  - "Feature Store and ML‑ready tables"
  - "Governed by Unity Catalog"

Consumption:
- "Agent Bricks for agentic AI & ML"
- "MLflow experiments & Model Registry"
- "Model Serving for real‑time and batch inference"
- Caption: "Production‑ready agents and models."

===== BOTTOM GOVERNANCE BAR =====

Full‑width bar spanning all columns:

- Place the Unity Catalog logo from the Logo Kit on the left.
- Main text: "Unity Catalog – Single Governance & Semantic Layer".
- Subtext: "Consistent policies, lineage and Metric Views across Analytics, Real‑Time and
  Agentic AI/ML workloads."

===== AWS/AZURE INDICATORS =====

At the top‑right of each column, show:
- Small AWS logo and Azure logo side‑by‑side
- Text: "Runs on AWS and Azure"

This reinforces that each workload pattern operates identically on both clouds.

===== STYLE =====

- 16:9 landscape, three equal columns.
- Light column background tints (blue, green, purple) with neutral core.
- Flat, minimalistic; information density on par with modern platform comparison diagrams.
- No filenames, only brand names and workloads.
```

---

# PROMPT 5 – Federated Data Mesh on Dual‑Cloud Lakehouse

```text
===== LOGO KIT – CRITICAL INSTRUCTIONS (APPLY TO THIS DIAGRAM) =====

[Use the same Logo Kit block from Prompt 1 – paste it here]

===== PROMPT BODY =====

You are a Lead Databricks Solutions Architect.

Create a FEDERATED DATA MESH diagram showing multiple AGL business domains owning
their data products, all built on a central Databricks Lakehouse spanning AWS and Azure.

The look should echo modern "data mesh on lakehouse" visuals: central platform, surrounding
domain nodes, clear dual‑cloud governance story.

===== CENTRAL PLATFORM =====

At the centre, draw a layered hexagon or circle with the label:
"Databricks Lakehouse Platform (AWS + Azure)"

Inside, three nested layers:

1) Inner layer – "Unity Catalog":
   - Place the Unity Catalog logo from the Logo Kit.
   - Text: "Central governance, lineage, access control, PII, quality"
   - "Unity Catalog Metric Views – unified semantic model"

2) Middle layer – "Delta Lake":
   - Place the Delta Lake logo from the Logo Kit.
   - Text: "Domain‑partitioned Delta tables on S3 and ADLS Gen2"

3) Outer layer – "Shared Compute":
   - Icons: Spark, DBSQL, Feature Store, Agent Bricks.
   - Text: "Shared compute plane and agentic AI orchestration"

Below the central platform, place the AWS logo and Azure logo side‑by‑side with text:
"Deployed on AWS and Azure infrastructure"

===== DOMAIN NODES =====

Around the centre, place 5–6 domain circles/hexagons connected by lines. Each domain
represents a major AGL business function owning and operating its own data product.

For each domain node, show three layers:

- Top: "Sources owned by domain" (icons and labels)
- Middle: "[Domain] Data Product" (Delta tables with a small Unity Catalog icon)
- Bottom: "Consumers" (dashboards, AI/BI, Agent Bricks, APIs, reports)

===== DOMAIN DETAILS =====

Domain 1 – Retail Energy & Customer:

- Colour: Light blue‑green pastel.
- Place the Kaluza logo from the Logo Kit in this node.
- Sources: "kaluza platform, CRM, web and app telemetry"
- Data product: "Customer 360 & product eligibility"
- Consumers: "AI/BI Dashboards, churn prediction agents (Agent Bricks), campaign analytics"

Domain 2 – Customer Operations & Contact Centre:

- Colour: Light orange pastel.
- Sources: "Amazon Connect, Salesforce service cloud"
- Data product: "Contact‑centre performance & NPS"
- Consumers: "Ops dashboards, AIBI Genie analysis, workforce planning, agent assist agents"

Domain 3 – Markets, Trading & Risk:

- Colour: Light purple pastel.
- Sources: "Market data feeds, SAP, external pricing"
- Data product: "Market & risk analytics hub"
- Consumers: "Trading desk dashboards, VaR and stress test models, market forecast agents"

Domain 4 – Generation & Asset Operations:

- Colour: Light amber pastel.
- Sources: "SCADA, historian, IoT sensors, asset databases"
- Data product: "Asset health & generation performance"
- Consumers: "Predictive maintenance models (Agent Bricks), outage analytics, plant dashboards"

Domain 5 – Finance & Regulatory Reporting:

- Colour: Light slate/grey pastel.
- Sources: "SAP finance, GL, billing, regulatory inputs"
- Data product: "Finance and compliance data mart"
- Consumers: "Regulatory packs, CFO dashboards, AI‑generated audit insights (Agent Bricks)"

Domain 6 (Optional) – Enterprise Shared Services:

- Colour: Light grey pastel.
- Sources: "HR systems, shared service data"
- Data product: "Shared enterprise reference data"
- Consumers: "HR analytics, shared metrics for all domains via AI/BI"

===== CONNECTIONS =====

- Lines from each domain's middle "data product" layer back to the Delta Lake layer in
  the central platform.
- Small Unity Catalog icons on those lines indicate central governance flowing outward.
- Selected cross‑domain arrows (e.g., Retail → Markets for pricing, Generation → Finance for
  revenue assurance) show data sharing through the Lakehouse, not point‑to‑point.

===== MESSAGE LABEL =====

At bottom:

- Title: "Decentralised domain ownership, centralised governance."
- Subtitle: "Domains own data products and operate independently; Databricks Lakehouse on AWS
  and Azure provides the shared, governed backbone for analytics, AI/BI and agentic AI."

===== STYLE =====

- 16:9 landscape, network‑like layout.
- Clean vector style, domain nodes in soft pastels; central platform slightly darker.
- AWS and Azure indicated only in the central platform label (not repeated on every node).
- No filenames; branding appears only via provided logos and domain names.
```

---

# PROMPT 6 – Before/After: Legacy vs Dual‑Cloud Databricks Lakehouse

```text
===== LOGO KIT – CRITICAL INSTRUCTIONS (APPLY TO THIS DIAGRAM) =====

[Use the same Logo Kit block from Prompt 1 – paste it here]

===== PROMPT BODY =====

You are a Lead Databricks Solutions Architect.

Create a SPLIT‑SCREEN "BEFORE/AFTER" comparison diagram showing AGL's transformation from a
fragmented, legacy data stack to a modern, unified Databricks Data Intelligence Platform on
AWS and Azure.

The goal: clearly communicate RFP value – consolidation, governance, multi‑cloud flexibility
and AI/ML readiness.

===== LAYOUT =====

- Left half: "BEFORE – Fragmented, single‑cloud and siloed"
- Right half: "AFTER – Unified Databricks Lakehouse on AWS & Azure"
- Bold vertical divider or thick arrow in the middle labelled "Databricks Transformation"

===== LOGOS =====

- Logos appear ONLY on the AFTER side:
  - Databricks wordmark logo near the new platform core
  - Delta Lake logo on the unified storage layer
  - Unity Catalog logo on the governance layer
  - AWS logo and Azure logo as cloud headers in their respective zones
- No logos on the BEFORE side
- No filenames anywhere in the diagram

===== BEFORE SIDE – FRAGMENTED LEGACY STACK (GREY, MUTED, CHAOTIC) =====

STORAGE (scattered, disconnected):

- Separate boxes for "Legacy DWH 1", "Legacy DWH 2 (cloud)", "Hadoop cluster"
- "Siloed S3 buckets", "Isolated ADLS accounts"
- Fragmented arrows, no central hub

GOVERNANCE (chaotic, inconsistent):

- Multiple small catalogue/lock icons:
  - "Per‑system metadata"
  - "Inconsistent access controls"
  - "No end‑to‑end lineage"

PROCESSING (fragmented, brittle):

- Separate stacks: "Spark cluster for ETL", "SQL engine A", "SQL engine B"
- Home‑grown pipelines, cron jobs, brittle dependencies

CONSUMPTION (isolated, no unified view):

- Siloed BI tools:
  - "Power BI (Finance only)"
  - "Tableau (Operations only)"
  - "Custom dashboards"
- No single source of truth
- Limited analytics / no AI/BI capabilities

ML (unmanaged, scattered):

- "Ad‑hoc notebooks", "Scripts on VMs"
- "No feature store", "No model registry", "No agentic AI"

PAIN POINTS (RED MARKERS):

Use red crosses or red labels to highlight:
- "Data duplication"
- "High cost & lock‑in"
- "Slow change, brittle pipelines"
- "Tool sprawl"
- "Siloed teams and inconsistent metrics"
- "No AI/BI or agentic capabilities"

Overall styling: muted greys with red accents for problems; tangled, messy connectors.

===== CENTRE DIVIDER =====

Bold vertical line or thick arrow running top to bottom, labelled:
"Databricks Transformation"

Optional: Add small phase labels:
- "Phase 1: Assessment"
- "Phase 2: Migration"
- "Phase 3: Optimisation"

===== AFTER SIDE – UNIFIED DATABRICKS LAKEHOUSE (VIBRANT, ORGANISED, CLEAN) =====

CORE PLATFORM:

- Central box titled: "Databricks Data Intelligence Platform (AWS + Azure)"
- Place the Databricks wordmark logo near this title

CLOUD INFRASTRUCTURE:

Left zone (AWS):

- Place the AWS logo as a header.
- Show: "kaluza, Salesforce, Amazon Connect, S3, MSK/Kinesis"
- Arrows flowing into the central Lakehouse

Right zone (Azure):

- Place the Azure logo as a header.
- Show: "SAP, Finance systems, OT/SCADA via Event Hubs, ADLS, Data Factory"
- Arrows flowing into the central Lakehouse

STORAGE:

- Single large storage band: "Unified Delta Lake – S3 (AWS) and ADLS Gen2 (Azure)"
- Place the Delta Lake logo from the Logo Kit
- Show Bronze / Silver / Gold zones inside the band

GOVERNANCE:

- Band across the platform:
  - Place the Unity Catalog logo from the Logo Kit
  - Label: "Unity Catalog – single governance plane across AWS and Azure"
  - Subtext: "Central catalogue, fine‑grained access, lineage, quality, PII controls"
  - "Unity Catalog Metric Views – unified semantic layer"

PROCESSING & INTELLIGENCE:

- "Data Engineering & Streaming"
  - "Lakeflow, LDP, Auto Loader, Structured Streaming"
- "Analytics & AI/BI"
  - "DBSQL, AI/BI Dashboards, AIBI Genie"
- "Agentic AI & ML"
  - "Agent Bricks, MLflow, Feature Store, Model Registry, Model Serving"

CONSUMPTION:

- "Trusted data products" band feeding:
  - "Customer & product analytics"
  - "Markets & risk tools"
  - "Generation & asset insights"
  - "Finance & regulatory reporting"
  - "AI‑driven apps and agentic agents"

BENEFITS (GREEN CHECKMARKS):

- "One governed Lakehouse across AWS and Azure"
- "Reduced TCO and tool sprawl"
- "Faster time‑to‑insight and AI/ML time‑to‑value"
- "Re‑usable features, semantic models and agents"
- "Consistent metrics and AI/BI across retail, markets, generation and finance"
- "Agentic AI and Agent Bricks automation"

Overall styling: vibrant Databricks / AGL palette, clear flows towards a central Lakehouse,
green success markers, AWS/Azure logos clearly positioned.

===== STYLE =====

- 16:9 landscape, crisp split down the middle.
- BEFORE: grey tones, messy connectors, red problem markers, chaotic.
- AFTER: vibrant Databricks / AGL palette, clean flows, green benefit markers, organised.
- Designed to feel like a transformation slide a senior architect would use in an RFP
  defence meeting – clear, compelling, RFP‑grade visuals.
```

---

## Summary

Six complete, production‑ready prompts for Nano Banana Pro:

1. ✅ **Prompt 1** – Vertical Platform Stack (5 layers, AWS/Databricks/Azure columns)
2. ✅ **Prompt 2** – Horizontal Data Journey (5 phases, 3 swim lanes)
3. ✅ **Prompt 3** – Concentric Ecosystem (4 rings, dual‑cloud split in Ring 3)
4. ✅ **Prompt 4** – Three Workload Pillars (Analytics, Real‑Time, Agentic AI)
5. ✅ **Prompt 5** – Federated Data Mesh (central Lakehouse, 6 domain nodes)
6. ✅ **Prompt 6** – Before/After (legacy vs modern dual‑cloud)

**All prompts include:**
- ✅ Logo Kit (Databricks, Delta Lake, Unity Catalog, kaluza, AGL, AWS, Azure)
- ✅ AIBI Dashboards, AIBI Genie, DBSQL
- ✅ Unity Catalog Metric Views (semantic layer)
- ✅ Agent Bricks (agentic AI/ML)
- ✅ AWS and Azure logos as explicit cloud markers
- ✅ No filenames in diagrams
- ✅ Modern reference architecture patterns
- ✅ RFP‑ready language and clarity

