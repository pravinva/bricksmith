# AGL DATABRICKS RFP – Complete Nano Banana Prompt Suite (v5 – AGL Annual Report Context)
## Six Standalone Prompts – Dual‑Cloud (AWS + Azure), AIBI, Agent Bricks, DBSQL, Metric Views + AGL Context

All prompts follow Nano Banana Pro best practices and are now enriched with context from AGL Energy Limited FY25 Annual Report:
- ✅ Logo Kit embedded at the top of each prompt
- ✅ AWS and Azure logos as explicit cloud markers
- ✅ No filenames shown in diagrams
- ✅ AIBI Dashboards, AIBI Genie, Unity Catalog Metric Views (semantic layer)
- ✅ Agent Bricks mentioned in AI/ML sections
- ✅ **AGL business context**: Customer Markets, Integrated Energy, renewable transition, generation portfolio, retail operations, regulatory compliance
- ✅ Modern data infrastructure inspired (a16z, Azure Databricks reference)
- ✅ RFP-ready language and clarity

---

## AGL BUSINESS CONTEXT (from FY25 Annual Report)

**Three Operating Segments:**
1. **Customer Markets**: Retail electricity, gas, broadband, mobile, solar, energy efficiency to residential and business customers. Includes kaluza platform, Salesforce CRM, Amazon Connect call centre, customer contact operations.
2. **Integrated Energy**: Power generation portfolio (coal, gas, wind, hydro, batteries), trading and origination, gas storage and sourcing, dispatch of generation assets.
3. **Investments**: ActewAGL Retail Partnership, Tilt Renewables, Energy Impact Partners Europe.

**Key Strategic Priorities (FY27 Targets):**
- Customer NPS leadership (target: 20)
- Digital-only customers growth (target: 60%)
- Speed to market improvement
- Green revenue expansion
- 2.1 GW new renewable and firming capacity contracted/in delivery
- 1.5 GW grid-scale batteries
- 1.6 GW decentralised assets under orchestration
- Financial reporting, regulatory compliance, energy market data

**Critical Data & AI Opportunities:**
- Customer 360 and churn prediction (NPS, loyalty)
- Load and demand forecasting (for 4.1M customer services)
- Energy cost optimisation (wholesale electricity price volatility)
- Renewable and firming asset performance (Liddell Battery, Wandoan Battery, etc.)
- Regulatory reporting (ASIC, AEMO, NEM compliance)
- Risk and hedging analytics (wholesale market price exposure)
- Call centre NPS and agent performance analytics
- OT/IoT from generation assets and grid-scale batteries (SAP integration for maintenance)

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

You are a Lead Databricks Solutions Architect preparing an RFP response for AGL Energy Limited,
Australia's leading integrated energy company with 4.1+ million customer services across electricity,
gas, broadband and mobile.

Design a VERTICAL, STACKED LAYERED reference architecture diagram showing how AGL's Databricks
Data Intelligence Platform (Lakehouse) runs on BOTH AWS and Azure to support AGL's three
operating segments: Customer Markets, Integrated Energy, and Investments.

The diagram should feel like a modern, layered a16z / Azure Databricks architecture: clean bands,
clear separation of concerns, and explicit governance. It will be used in an RFP response to explain
how AGL consolidates data across customer, markets, generation portfolio and regulatory reporting.

===== AGL CONTEXT =====

AGL operates in three key segments:

- CUSTOMER MARKETS: 4.1M customer services (electricity, gas, broadband, mobile, solar).
  Includes kaluza platform (retail energy), Salesforce (CRM), Amazon Connect (call centre).
  Critical data: Customer 360, churn prediction, NPS analytics, billing events.

- INTEGRATED ENERGY: Power generation portfolio (coal, gas, renewables, batteries).
  Gen assets: Liddell Battery, Bayswater, Loy Yang A, Torrens Island, wind/hydro.
  Trading and origination; dispatch; gas storage and sourcing.
  Critical data: Generation performance, wholesale electricity prices, fuel costs, hedging.

- INVESTMENTS: ActewAGL, Tilt Renewables, Energy Impact Partners.

Strategic FY27 targets: NPS leadership, digital customers, 2.1 GW new renewables,
1.5 GW grid-scale batteries, 1.6 GW decentralised assets orchestration.

===== LAYERS & COLUMNS =====

Create FIVE horizontal layers from bottom to top:

1. Cloud Infrastructure (AWS and Azure foundations)
2. Storage & Governance (Delta Lake + Unity Catalog)
3. Processing & Intelligence (Databricks engines)
4. Data Products & Applications (AGL domains)
5. Business Outcomes (Strategic value)

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
  "Integrated energy company unifying Customer Markets (4.1M services), Integrated Energy (generation,
   trading) and Investments across AWS (customer/call centre) and Azure (SAP, generation OT/IoT)."

===== LAYER 1 – CLOUD INFRASTRUCTURE =====

AWS column:

- Place the AWS logo at the top of this column as a column header.
- Icons: VPC, EC2, S3, MSK/Kinesis.
- Caption: "Customer-facing and call‑centre workloads. kaluza, Salesforce, Amazon Connect, billing systems."

Azure column:

- Place the Azure logo at the top of this column as a column header.
- Icons: Virtual Network, VMs, ADLS Gen2, Event Hubs, IoT Hub.
- Caption: "SAP ERP, generation asset operations, OT/IoT from generation portfolio and grid-scale batteries."

Databricks centre:

- Place the Databricks brand‑mark logo.
- Label: "Databricks Workspaces and Control Plane".
- Subtitle: "Unified workspace experience across AWS and Azure with central governance."

===== LAYER 2 – STORAGE & GOVERNANCE =====

AWS column:

- Box: "Delta Lake on S3 – Bronze / Silver / Gold".
- Place the Delta Lake logo on the left.
- Text: "Customer 360 data, interaction events from kaluza, Salesforce, Amazon Connect, billing, NPS data."

Azure column:

- Box: "Delta Lake on ADLS Gen2 – Bronze / Silver / Gold".
- Place the same Delta Lake logo on the left.
- Text: "SAP finance and billing, generation performance data, wholesale market data, OT/generation telemetry,
   energy hedging, regulatory reporting data."

Databricks centre band (spanning both):

- Place the Unity Catalog logo on the left.
- Main label: "Unity Catalog – Cross‑Cloud Governance & Semantic Layer".
- Sub‑labels:
  - "Central catalogue and fine‑grained access control"
  - "Lineage, quality, PII detection for regulatory compliance (ASIC, AEMO)"
  - "Unity Catalog Metric Views – shared semantic model for AI/BI and reporting"
- Arrows upward from both Delta Lake boxes into this band.

===== LAYER 3 – PROCESSING & INTELLIGENCE =====

In Databricks centre column, three stacked capability boxes:

1) "Data Engineering & Ingestion"
   - "Lakeflow (ingest, ETL, streaming), LDP (Lakeflow Declarative Pipelines), Auto Loader,
      Structured Streaming"
   - Caption: "Batch and streaming pipelines from AWS (kaluza events, Salesforce, call centre),
      and Azure (SAP transactions, generation OT/IoT, market data)."

2) "Analytics & AI/BI"
   - "DBSQL, AI/BI Dashboards, AIBI Genie"
   - "Unity Catalog Metric Views for semantic layer (customer, financial, generation metrics)"
   - Caption: "Enterprise reporting, AI/BI for NPS, churn, load forecasting, asset performance across AGL."

3) "Agentic AI & Machine Learning"
   - "Agent Bricks – agentic AI and ML"
   - "MLflow, Feature Store, Model Registry, Model Serving"
   - Caption: "Demand forecasting, churn prediction, credit risk, load forecasting, call‑centre analytics,
      predictive maintenance (generation assets)."

Small badge: "Same developer experience and governance on AWS and Azure."

===== LAYER 4 – DATA PRODUCTS & APPLICATIONS =====

AWS column (Customer Markets):

- Group title: "Customer & Call‑Centre Apps on AWS".
- Place the AWS logo as a small badge.
- Place the Kaluza logo next to label "kaluza – retail energy platform (electricity, gas, solar offers)".
- Additional apps: "Salesforce (CRM, sales, lead scoring)", "Amazon Connect (contact centre, IVR)".
- Text: "Customer interactions, billing events, usage data, NPS, call centre tickets, service orders (4.1M services)."
- Arrows: Down to "Delta Lake on S3", Across to "Data Engineering", Upwards to "AI/BI and AIBI Genie".

Databricks centre column (AGL domain data products):

- Boxes:
  - "Customer 360, Churn & NPS Hub" → feeds kaluza targeting and Amazon Connect agent assist
  - "Energy Demand & Load Forecasting Layer" → feeds wholesale trading, battery dispatch
  - "Generation & Asset Insight Layer" → feeds maintenance scheduling, Liddell/Wandoan battery performance
  - "Financial & Regulatory Reporting Layer" → feeds SAP, ASIC/AEMO compliance
- Caption: "Domain‑aligned, governed data products consumed by apps, AI/BI, Agent Bricks and executive dashboards."

Azure column (Integrated Energy & SAP):

- Group title: "Enterprise and SAP on Azure".
- Place the Azure logo as a small badge.
- Items:
  - "SAP (ERP, billing, market settlement, finance)"
  - "Finance and commercial systems (revenue assurance)"
  - "HR, asset and work management, risk"
  - "OT / generation systems (SCADA, historian, IoT from Bayswater, Loy Yang, Torrens Island, batteries)"
- Text: "Financials, contracts, generation asset data, market data, maintenance records, OT telemetry."
- Arrows: Down to "Delta Lake on ADLS", Across to "Data Engineering", Upwards to AI/BI and Agent Bricks.

===== LAYER 5 – BUSINESS OUTCOMES =====

Single band at top with icon + label pairs aligned to AGL's FY27 strategic targets:

- "Customer NPS Leadership (FY27 target: 20 NPS)"
  ← arrows to Customer 360 Hub and Amazon Connect agent assist
- "Digital Customer Growth (FY27 target: 60% digital-only)"
  ← arrows to churn prediction and demand forecasting
- "Load & Demand Forecasting Accuracy"
  ← arrows to forecasting layer and renewable dispatch
- "Renewable & Battery Asset Performance"
  ← arrows to generation asset insights and predictive maintenance
- "Regulatory & Financial Reporting Confidence (ASIC, AEMO, NEM compliance)"
  ← arrows to financial and regulatory data layer

===== VISUAL STYLE =====

- 16:9 landscape, flat vector, subtle layer shadows.
- Information density similar to modern a16z / Databricks diagrams.
- No filenames; only real logos and AGL business labels as described.
```

---

# PROMPT 2 – Data Journey with AIBI, Metric Views and Agent Bricks (AGL Context)

```text
===== LOGO KIT – CRITICAL INSTRUCTIONS (APPLY TO THIS DIAGRAM) =====

[Use the same Logo Kit block from Prompt 1 – paste it here]

===== PROMPT BODY =====

You are a Lead Databricks Solutions Architect responding to an RFP for AGL Energy Limited.

Create a HORIZONTAL LEFT‑TO‑RIGHT DATA JOURNEY diagram that shows how AGL moves data from
AWS and Azure into a governed Databricks Lakehouse, and then into AI/BI Dashboards, AIBI Genie
and Agent Bricks‑powered AI for AGL's three operating segments.

The style should resemble modern "Emerging Architectures for Modern Data Infrastructure"
flows and the Azure Databricks reference: five phases, three swim lanes, with AGL-specific data flows.

===== AGL CONTEXT =====

AGL operates:

- AWS: kaluza platform (retail energy, 4.1M customers), Salesforce CRM, Amazon Connect call centre,
  customer billing and interaction data.

- Azure: SAP ERP (finance, billing, market settlement), generation asset OT/IoT (SCADA from Bayswater,
  Loy Yang, Torrens Island, Liddell Battery, etc.), market data, regulatory compliance data.

Critical data flows:
- Customer 360: kaluza → churn prediction → NPS improvement
- Load forecasting: market data + customer demand → wholesale trading decisions
- Generation performance: SCADA + historian → predictive maintenance, battery dispatch
- Financial compliance: SAP → regulatory reporting (ASIC, AEMO, NEM data)

===== STRUCTURE =====

Three swim lanes:

- Top lane: "AWS (with AWS logo) – kaluza, Salesforce, Amazon Connect, billing events"
- Middle lane: "Databricks Data Intelligence Platform"
- Bottom lane: "Azure (with Azure logo) – SAP, generation OT/IoT, market data, compliance"

Five vertical phases:

1. Ingest
2. Transform
3. Govern
4. Analyse (AI/BI)
5. Activate (Agentic AI & Operations)

===== PHASE 1 – INGEST =====

AWS lane:

- "kaluza events" (tariffs, offers, customer interactions)
- "Salesforce records" (leads, customers, service orders)
- "Amazon Connect interactions" (call centre logs, agent performance)
- "Billing events" (customer payments, usage)
- Services: Kinesis/MSK, DMS, S3

Azure lane:

- "SAP transactions" (finance, billing, market settlement)
- "OT / SCADA telemetry" (Bayswater, Loy Yang, Torrens Island, batteries – EAF, fuel costs, outages)
- "Market data feeds" (AEMO, wholesale prices, hedging)
- "Enterprise systems" (HR, asset management, compliance data)
- Services: Event Hubs, Data Factory, Synapse Link, ADLS, IoT Hub

Databricks lane:

- Box: "Ingest with Lakeflow, Auto Loader & LDP".
- Converging arrows from AWS and Azure lanes.

===== PHASE 2 – TRANSFORM =====

Databricks lane:

- Wide box:
  - Place the Delta Lake logo.
  - Labels:
    - "Delta Lake Medallion Architecture (Bronze → Silver → Gold)"
    - "Apache Spark & Photon – batch and streaming"
    - "Lakeflow Declarative Pipelines (LDP), Jobs, Structured Streaming"
    - "Aggregations for NPS, churn, load forecasts, asset health"

Data flows left‑to‑right: Bronze (raw kaluza events, SCADA, SAP) → Silver (cleaned, deduplicated)
→ Gold (business-ready: Customer 360, Load Forecast, Asset Performance tables).

===== PHASE 3 – GOVERN =====

Databricks lane:

- Wide box:
  - Place the Unity Catalog logo.
  - Main text: "Unity Catalog – Single Governance & Semantic Layer for AGL".
  - Subtext:
    - "Central catalogue and access control (customer data, generation OT/IoT, finance)"
    - "Lineage and quality checks (NPS data integrity, load forecast accuracy, SAP compliance)"
    - "PII detection for regulatory compliance (ASIC, AEMO customer and market data)"
    - "Unity Catalog Metric Views – shared semantic model: Customer Metrics, Energy Metrics, Financial Metrics"

Small arrows from AWS and Azure lanes showing both clouds' data governed together.

===== PHASE 4 – ANALYSE (AI/BI) =====

Databricks lane:

- Box: "AI/BI Dashboards and AIBI Genie".
- Inside:
  - "DBSQL queries over Delta Lake Gold tables"
  - "Unity Catalog Metric Views providing the semantic layer"
  - "AIBI Genie for AI-assisted analysis: 'What drives NPS?', 'Forecast load for tomorrow?',
     'Asset health risk?'"
- Outputs to:
  - "Executive dashboards" (CEO, CFO: NPS trends, financial performance, generation margins)
  - "Operational AI/BI dashboards" (call‑centre NPS, customer churn, renewable dispatch, compliance)
  - "Self‑service business users" (product teams, traders, asset managers)

===== PHASE 5 – ACTIVATE (AGENTIC AI & OPERATIONS) =====

Databricks lane:

- Box: "Agent Bricks, MLflow, Feature Store & Model Serving".
- Inside:
  - "Agent Bricks orchestrating agentic AI workflows"
  - "MLflow experiments & Model Registry"
  - "Feature Store (shared: Customer Features, Market Features, Asset Health Features)"
  - "Real‑time and batch Model Serving"

Outbound arrows:

- To AWS lane (Customer Markets):
  - "kaluza – personalised tariff offers, solar/battery recommendations (churn prediction agents)"
  - "Salesforce – next‑best‑action, lead scoring, customer 360 enrichment"
  - "Amazon Connect – agent assist, sentiment alerts, routing (NPS agents)"

- To Azure lane (Integrated Energy & SAP):
  - "SAP – financial forecasts, revenue assurance, market settlement optimization"
  - "Generation systems – predictive maintenance alerts, battery dispatch optimization (load forecast agents)"
  - "Regulatory marts – pre‑populated ASIC/AEMO compliance reports (regulatory agents)"

Right margin: outcome list:
- "Better decisions via AI/BI and AIBI Genie"
- "Agentic automation with Agent Bricks (churn, NPS, forecasting, maintenance)"
- "Cross‑cloud data trust and governance"
- "FY27 strategic targets achieved: NPS 20, digital growth, asset performance"

===== STYLE =====

- 16:9 landscape, rounded Databricks components, sharper cloud services.
- AWS orange / Azure blue / Databricks slate+red palette.
- No filenames, only product names, AGL business terms and flows.
```

---

# PROMPT 3 – Concentric Ecosystem (Dual‑Cloud Rings, AGL Context)

```text
===== LOGO KIT – CRITICAL INSTRUCTIONS (APPLY TO THIS DIAGRAM) =====

[Use the same Logo Kit block from Prompt 1 – paste it here]

===== PROMPT BODY =====

You are a Lead Databricks Solutions Architect.

Design a CONCENTRIC CIRCLE / TARGET diagram showing AGL's Databricks Lakehouse at the
centre, shared platform services around it, then AWS/Azure systems split left/right,
and finally AGL's five business domains around the outside.

The diagram maps directly to AGL's operating model: Customer Markets (AWS), Integrated Energy
(Azure with OT/IoT), and investment in renewable and firming assets.

Follow the same ring structure as a modern platform ecosystem: clean rings, clear segmentation,
balanced labels. Do NOT write "Ring 1 / Ring 2 / Ring 3 / Ring 4" in the diagram; use only
business and technical labels.

===== HIGH‑LEVEL RING STRUCTURE =====

From inside to outside:

- Inner core: "AGL Unified Energy Data Platform"
- Ring 2: "Shared Databricks Platform Services"
- Ring 3: "Cloud Systems – AWS (left) vs Azure (right)"
- Outer ring: "AGL Business Domains & Data Products" (5 domains)

===== LOGO PLACEMENT =====

- Place Databricks brand mark logo in the centre of the inner core
- Place Delta Lake logo on the storage slice of the core
- Place Unity Catalog logo on the governance slice of the core
- Place Kaluza logo in the "Retail Energy & Customer" outer segment
- Place AGL logo in the top‑left header area, outside the rings
- Place AWS logo as a badge in the outer perimeter of the AWS half of Ring 3
- Place Azure logo as a badge in the outer perimeter of the Azure half of Ring 3

Never show logo filenames as text.

===== INNER CORE =====

Solid circle with:
- Main text: "AGL Unified Energy Data Platform"
- Subtitle: "Databricks Lakehouse on AWS and Azure"

Slice the inner core into three radial segments (120 degrees each):

1) Storage:
   - Next to the Delta Lake logo
   - Label: "Delta Lake – S3 (AWS) and ADLS Gen2 (Azure)"
   - Include: Customer 360, load forecasts, generation performance, SAP financial data

2) Processing:
   - Label: "Apache Spark, Photon, SQL Warehouses"
   - Includes: DBSQL, AI/BI Dashboards, AIBI Genie, Agent Bricks orchestration

3) Governance:
   - Next to the Unity Catalog logo
   - Label: "Unity Catalog – Cross‑cloud governance, lineage, security"
   - Sub‑text: "Metric Views provide the unified semantic layer"
   - Includes: Regulatory compliance (ASIC, AEMO), PII detection

===== RING 2 – SHARED PLATFORM SERVICES =====

Complete ring divided into three equal sectors (120 degrees each):

Sector 1 – "Data Engineering & Ingestion" (top‑left):
- "Lakeflow, LDP, Auto Loader, Structured Streaming"
- "Batch and streaming pipelines from AWS (kaluza, Salesforce, Amazon Connect) and Azure
   (SAP, OT/SCADA, market data)"

Sector 2 – "Analytics & AI/BI" (bottom):
- "DBSQL, AI/BI Dashboards, AIBI Genie"
- "Unity Catalog Metric Views as governed semantic layer"
- "Enterprise reporting and self‑service AI/BI for AGL executives and traders"

Sector 3 – "Agentic AI & ML for Energy" (top‑right):
- "Agent Bricks"
- "MLflow, Feature Store, Model Registry, Serving"
- "Churn, NPS, load forecasting, predictive maintenance agents"

===== RING 3 – CLOUD SYSTEMS (AWS LEFT, AZURE RIGHT) =====

Split this ring vertically into left and right halves with a subtle vertical divider at
12 o'clock and 6 o'clock.

Left half (AWS – orange accents):

- Place AWS logo as a small badge near the outer edge
- Title: "Customer Markets on AWS"
- Inside:
  - Place Kaluza logo near this section (or prominently in outer ring)
  - "kaluza – retail energy platform (electricity, gas, solar, batteries)"
  - "Salesforce – CRM, sales, customer data"
  - "Amazon Connect – contact centre, agent performance, NPS"
- Text: "Customer interactions, billing events, 4.1M services, NPS data, churn indicators"
- Icons: S3, Kinesis, MSK pointing inward to Ring 2
- Arrows inward

Right half (Azure – blue accents):

- Place Azure logo as a small badge near the outer edge
- Title: "Integrated Energy on Azure"
- Inside: (Do NOT use SAP logo as cloud logo; SAP remains an application inside)
  - "SAP – ERP, billing, market settlement, financial data"
  - "Finance and commercial systems"
  - "OT / generation systems" (SCADA, historian, IoT from Liddell, Bayswater, Loy Yang,
     Torrens Island, Wandoan batteries, etc.)
- Text: "Generation asset data, wholesale market data, hedging, maintenance records, financials"
- Icons: ADLS, Event Hubs, Data Factory, Azure IoT Hub/Edge
- Arrows inward

===== OUTER RING – AGL BUSINESS DOMAINS =====

Five evenly spaced segments around the circle (72 degrees each).
Do NOT show the text "Ring 4" anywhere; use only AGL domain names.

Distribute clockwise from top:

Domain 1 – "Retail Energy and Customer" (top or top‑right):

- Colour: Light blue‑green pastel
- Place Kaluza logo here (if prominent)
- Text: "kaluza platform, customer tariffs, solar/battery offers, NPS, churn prediction"
- Data products: Customer 360, churn propensity, product recommendations
- Small AWS‑orange chip
- Arrow curves inward

Domain 2 – "Call Centre & Customer Operations" (right or lower‑right):

- Colour: Light orange pastel
- Text: "Amazon Connect call analytics, agent performance, NPS, customer satisfaction"
- Data products: Agent assist, sentiment analysis, routing optimization
- AWS‑orange chip
- Arrow curves inward

Domain 3 – "Markets, Trading and Risk" (bottom):

- Colour: Light purple pastel
- Text: "Wholesale electricity prices, AEMO data, hedging performance, revenue assurance"
- Data products: Price forecasting, hedging analytics, market risk dashboards
- Neutral/dual‑cloud chip
- Arrow curves inward

Domain 4 – "Generation and Asset Operations" (bottom‑left or left):

- Colour: Light amber pastel
- Text: "Bayswater, Loy Yang, Torrens Island, Liddell Battery, Wandoan Battery performance.
   SCADA data, outage analytics, predictive maintenance, load optimization"
- Data products: Asset health, maintenance alerts, generation dispatch
- Azure‑blue chip (OT/IoT telemetry lands on Azure)
- Small IoT icon (sensor symbol) coloured with Azure accents
- Arrow curves inward

Domain 5 – "Finance and Regulatory Reporting" (left or upper‑left):

- Colour: Light slate/grey pastel
- Text: "SAP financials, revenue recognition, regulatory packs (ASIC, AEMO, NEM).
   Audit compliance, cost analytics"
- Data products: Financial metrics, regulatory dashboards, audit packs
- Azure‑blue chip (SAP on Azure)
- Arrow curves inward

===== LEGEND =====

Small legend bottom‑right:

- [Dark slate/red swatch] "Databricks core platform"
- [Orange dot] "AWS‑anchored workloads"
- [Blue dot] "Azure‑anchored workloads"
- [Grey dot] "Cross‑cloud / neutral domains"
- [AWS logo] "AWS infrastructure and apps (kaluza, Salesforce, Amazon Connect)"
- [Azure logo] "Azure infrastructure and apps (SAP, generation OT/IoT)"
- [Small IoT icon with blue accent] "OT/IoT telemetry from generation assets landing on Azure"

===== HEADER =====

- Place AGL logo in the top‑left, outside the rings (10–15% width)
- Centre title in white, bold: "AGL Unified Data & AI Platform – Databricks Lakehouse Across AWS and Azure"
- Subtitle in white: "Integrated energy company: Customer Markets (4.1M on AWS), Integrated Energy
   (generation, trading on Azure), powered by unified Databricks with AI/BI and Agent Bricks."

===== STYLE =====

- 16:9 landscape
- White background, soft drop shadow on inner two rings
- AWS orange / Azure blue accents on their respective halves of Ring 3
- Balanced information density similar to modern data‑infra platform diagrams
- No filenames; logos appear only as graphics with minimal brand text
```

---

# PROMPT 4 – Three Workload Pillars (Analytics, Real‑Time, Agentic AI, AGL Context)

```text
===== LOGO KIT – CRITICAL INSTRUCTIONS (APPLY TO THIS DIAGRAM) =====

[Use the same Logo Kit block from Prompt 1 – paste it here]

===== PROMPT BODY =====

You are a Lead Databricks Solutions Architect.

Design a THREE‑COLUMN workload pattern diagram showing how AGL's dual‑cloud Databricks
Lakehouse supports:

1. Analytics & AI/BI (NPS dashboards, financial reporting, trader dashboards)
2. Real‑Time Operations (agent performance, battery dispatch, load forecasting)
3. Agentic AI & Machine Learning (churn prediction agents, maintenance agents, trading agents)

Each column has three layers: Ingestion → Lakehouse Core → Consumption.

At the top‑right of each column, show AWS and Azure logos side‑by‑side with text
"Runs on AWS and Azure".

===== COLUMN 1 – ANALYTICS & AI/BI (Executive Dashboards & Reporting) =====

Ingestion:
- "Batch sources: SAP finance, kaluza customer data, SCADA logs, NEM/AEMO market data"
- Tools: dbt, Fivetran

Lakehouse Core:
- Place Delta Lake logo prominently
- Labels:
  - "Clean Delta tables (Bronze / Silver / Gold)"
  - "AGL domains: Customer Metrics, Financial Metrics, Generation Metrics"
  - "Unity Catalog Metric Views as enterprise semantic model"

Consumption:
- "DBSQL, AI/BI Dashboards, AIBI Genie"
- "Executive dashboards: CEO NPS trends, CFO financial performance, COO generation margins"
- "Trader dashboards: wholesale prices, hedging performance, market risk"
- Caption: "Governed AI/BI for executives, traders and analysts."

===== COLUMN 2 – REAL‑TIME OPERATIONS (Agent Performance, Battery Dispatch, Load Control) =====

Ingestion:
- "Streaming from Kafka/MSK, Event Hubs, APIs, IoT"
- "kaluza events" (customer interactions, tariff enquiries)
- "Salesforce events" (lead activity)
- "Amazon Connect events" (call centre interactions, IVR)
- "SCADA/historian streams" (Bayswater, Loy Yang, Torrens Island, batteries – EAF, fuel costs)"
- "AEMO dispatch signals, load data"

Lakehouse Core:
- Place Delta Lake logo prominently
- Labels:
  - "Delta Lake with streaming and ACID transactions"
  - "Fresh Gold tables: Real-time Customer Facts, Generation Facts, Market Facts"
  - "Sub-second latency for agent assist and dispatch optimization"

Consumption:
- "Operational dashboards fed by AI/BI" (agent performance, NPS sentiment, battery SoC)
- "Real‑time APIs and reverse ETL into kaluza, Amazon Connect, SCADA systems"
- "Agent assist: customer service suggestions, offer recommendations (real‑time)"
- Caption: "Always‑on operational decisions for 4.1M customer services and generation assets."

===== COLUMN 3 – AGENTIC AI & MACHINE LEARNING =====

Ingestion:
- "Training data and features from Lakehouse Gold tables"
- "Historical: 4+ years customer behaviour, generation asset logs, market data"
- "Telemetry: call centre interactions, SCADA performance, hedging outcomes"

Lakehouse Core:
- Place Delta Lake logo prominently
- Labels:
  - "Feature Store and ML‑ready tables (customer features, asset health features, market features)"
  - "Governed by Unity Catalog for reproducible ML"
  - "Versioned data for agent training, retraining, monitoring"

Consumption:
- "Agent Bricks for agentic AI orchestration"
- "Agents: Churn prediction (kaluza), NPS sentiment (Amazon Connect), Load forecasting,
   Predictive maintenance (generation assets), Trading optimization (markets)"
- "MLflow experiments & Model Registry"
- "Model Serving for real‑time and batch inference"
- Caption: "Production‑ready agents and models enabling AGL's FY27 strategic targets."

===== BOTTOM GOVERNANCE BAR =====

Full‑width bar spanning all columns:

- Place Unity Catalog logo
- Main text: "Unity Catalog – Single Governance & Semantic Layer"
- Subtext: "Consistent policies, Metric Views and lineage across Analytics, Real‑Time and
   Agentic AI/ML workloads. Regulatory compliance (ASIC, AEMO) built in."

===== AWS/AZURE INDICATORS =====

At the top‑right of each column, show:
- Small AWS logo and Azure logo side‑by‑side
- Text: "Runs on AWS and Azure"

This reinforces that each workload pattern operates identically on both clouds.

===== STYLE =====

- 16:9 landscape, three equal columns
- Light column background tints (blue, green, purple) with neutral core
- Flat, minimalistic; information density on par with modern platform comparison diagrams
- No filenames, only brand names and AGL workloads
```

---

# PROMPT 5 – Federated Data Mesh on Dual‑Cloud Lakehouse (AGL Context)

```text
===== LOGO KIT – CRITICAL INSTRUCTIONS (APPLY TO THIS DIAGRAM) =====

[Use the same Logo Kit block from Prompt 1 – paste it here]

===== PROMPT BODY =====

You are a Lead Databricks Solutions Architect.

Create a FEDERATED DATA MESH diagram showing how AGL's five business domains own
their data products, all built on a central Databricks Lakehouse spanning AWS and Azure.

The look should echo modern "data mesh on lakehouse" visuals: central platform, surrounding
domain nodes, clear dual‑cloud governance story, with AGL's specific domain structure.

===== CENTRAL PLATFORM =====

At the centre, draw a layered hexagon or circle with the label:
"Databricks Lakehouse Platform (AWS + Azure)"

Inside, three nested layers:

1) Inner layer – "Unity Catalog":
   - Place Unity Catalog logo
   - Text: "Central governance, lineage, access control, PII, quality"
   - "Unity Catalog Metric Views – unified semantic model (Customer, Financial, Generation metrics)"

2) Middle layer – "Delta Lake":
   - Place Delta Lake logo
   - Text: "Domain‑partitioned Delta tables on S3 (AWS) and ADLS Gen2 (Azure)"

3) Outer layer – "Shared Compute":
   - Icons: Spark, DBSQL, Feature Store, Agent Bricks
   - Text: "Shared compute plane and agentic AI orchestration"

Below the central platform, place AWS logo and Azure logo side‑by‑side with text:
"Deployed on AWS and Azure infrastructure"

===== DOMAIN NODES =====

Around the centre, place 5 domain circles/hexagons connected by lines. Each domain
represents a major AGL business function owning and operating its own data product.

For each domain node, show three layers:

- Top: "Sources owned by domain" (icons and labels)
- Middle: "[Domain] Data Product" (Delta tables with a small Unity Catalog icon)
- Bottom: "Consumers" (dashboards, AI/BI, Agent Bricks, APIs, reports)

===== DOMAIN DETAILS =====

Domain 1 – Retail Energy & Customer:

- Colour: Light blue‑green pastel
- Place Kaluza logo in this node
- Sources: "kaluza platform, CRM data, web and app telemetry, customer billing"
- Data product: "Customer 360 & product eligibility (governed Delta tables)"
- Consumers: "AI/BI Dashboards (NPS, churn), Agents (tariff recommendations, churn prevention),
   kaluza platform (real‑time offers)"

Domain 2 – Call Centre & Customer Operations:

- Colour: Light orange pastel
- Sources: "Amazon Connect call logs, agent scripts, customer service tickets"
- Data product: "Contact‑centre performance & NPS (governed Delta tables)"
- Consumers: "Ops dashboards (AIBI Genie), agent assist agents (real‑time sentiment),
   workforce planning tools"

Domain 3 – Markets, Trading & Risk:

- Colour: Light purple pastel
- Sources: "Market data feeds (AEMO, wholesale prices), hedging transactions"
- Data product: "Market & risk analytics hub (governed Delta tables)"
- Consumers: "Trader dashboards (price forecasts), Agent Bricks (trading optimization),
   VaR and stress test models"

Domain 4 – Generation & Asset Operations:

- Colour: Light amber pastel
- Sources: "SCADA systems (Bayswater, Loy Yang, Torrens Island, Liddell Battery),
   historian data, asset databases"
- Data product: "Asset health & generation performance (governed Delta tables)"
- Consumers: "Predictive maintenance models (Agent Bricks), outage analytics dashboards,
   dispatch optimization, plant dashboards"

Domain 5 – Finance & Regulatory Reporting:

- Colour: Light slate/grey pastel
- Sources: "SAP finance, GL systems, billing data, regulatory inputs"
- Data product: "Finance and compliance data mart (governed Delta tables)"
- Consumers: "Regulatory reporting packs (ASIC, AEMO), CFO dashboards, AI‑generated audit
   insights (Agent Bricks), tax planning tools"

===== CONNECTIONS =====

- Lines from each domain's middle "data product" layer back to the Delta Lake layer in
  the central platform
- Small Unity Catalog icons on those lines indicate central governance flowing outward
- Selected cross‑domain arrows (e.g., Retail → Markets for pricing, Generation → Finance for
  revenue assurance) show data sharing through the Lakehouse, not point‑to‑point

===== MESSAGE LABEL =====

At bottom:

- Title: "Decentralised domain ownership, centralised governance."
- Subtitle: "AGL domains own data products and operate independently; Databricks Lakehouse on AWS
   and Azure provides the shared, governed backbone for analytics, AI/BI and agentic AI.
   FY27 targets delivered through unified data."

===== STYLE =====

- 16:9 landscape, network‑like layout
- Clean vector style, domain nodes in soft pastels; central platform slightly darker
- AWS and Azure indicated only in the central platform label
- No filenames; branding appears only via provided logos and AGL domain names
```

---

# PROMPT 6 – Before/After: Legacy vs Dual‑Cloud Databricks Lakehouse

```text
===== LOGO KIT – CRITICAL INSTRUCTIONS (APPLY TO THIS DIAGRAM) =====

[Use the same Logo Kit block from Prompt 1 – paste it here]

===== PROMPT BODY =====

You are a Lead Databricks Solutions Architect.

Create a SPLIT‑SCREEN "BEFORE/AFTER" comparison diagram showing AGL's transformation from
a fragmented, legacy, single‑cloud data stack to a modern, unified Databricks Data Intelligence
Platform on AWS and Azure.

The goal: clearly communicate RFP value – consolidation, governance, multi‑cloud flexibility
and AI/ML readiness for AGL's three operating segments.

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

===== BEFORE SIDE – FRAGMENTED LEGACY (GREY, MUTED, CHAOTIC) =====

STORAGE (scattered, disconnected):

- Separate boxes for "Data Warehouse (Redshift or Netezza)", "Legacy kaluza systems", "SAP silos"
- "Isolated S3 buckets (aws)", "Isolated ADLS instances (Azure)" – no integration
- "File shares, CSVs, spreadsheets for reporting"
- Fragmented arrows, no central hub

GOVERNANCE (chaotic, inconsistent):

- Multiple metadata catalogues: "kaluza metadata", "SAP metadata", "custom data dictionary"
- Different access control models per system (Finance team access ≠ Operations team access)
- No lineage shown; no audit trail
- No PII protection; compliance risk

PROCESSING (fragmented, brittle):

- Separate Apache Spark clusters: "one for kaluza ETL", "one for SAP", "one for ad‑hoc analytics"
- Multiple SQL engines (Hive, Presto, custom)
- Manual cron jobs, brittle dependencies; 3‑day batch cycles for reporting
- No real‑time capabilities

CONSUMPTION (isolated, no unified view):

- Siloed BI tools: "Tableau (Finance only)", "Power BI (Operations only)", "custom dashboards (IT)"
- No single customer view; no unified NPS tracking
- No load forecasting capability; manual trading decisions
- Limited analytics / no AI/BI capabilities

ML (unmanaged, scattered):

- "Ad‑hoc notebooks on VMs", "Scripts on laptops"
- "No feature store", "No model registry", "No agentic AI"
- No churn prediction, no load forecasting agents

PAIN POINTS (RED MARKERS):

- "Data duplication across systems"
- "High cost: multiple warehouses, multiple cloud subscriptions"
- "Slow change; 3‑day batch reporting cycles"
- "Tool sprawl; training overhead"
- "Siloed teams; no shared metrics"
- "No AI/BI or agentic capabilities"
- "Regulatory risk: no audit trail, compliance inconsistency"
- "Customer experience gap: 4.1M customers, no unified 360 view"

Overall styling: muted greys with red accents for problems; tangled, messy connectors;
arrows pointing in different directions (chaotic).

===== CENTRE DIVIDER =====

Bold vertical line or thick arrow running top to bottom, labelled:
"Databricks Transformation"

Optional: Add small phase labels:
- "Phase 1: Assessment & Business Case"
- "Phase 2: AWS & Azure Deployment"
- "Phase 3: Migration & Enablement"

===== AFTER SIDE – UNIFIED DATABRICKS LAKEHOUSE (VIBRANT, ORGANISED, CLEAN) =====

CORE PLATFORM:

- Central box titled: "Databricks Data Intelligence Platform (AWS + Azure)"
- Place Databricks wordmark logo near this title

CLOUD INFRASTRUCTURE:

Left zone (AWS):

- Place AWS logo as a header
- Show: "kaluza platform, Salesforce CRM, Amazon Connect (4.1M customer services)"
- Show: "S3, Kinesis/MSK" for ingestion
- Arrows flowing into central Lakehouse

Right zone (Azure):

- Place Azure logo as a header
- Show: "SAP ERP, generation asset OT/IoT (Bayswater, Loy Yang, Torrens Island, Liddell Battery),
   market data feeds"
- Show: "ADLS Gen2, Event Hubs, Data Factory, IoT Hub" for ingestion
- Arrows flowing into central Lakehouse

STORAGE:

- Single large storage band: "Unified Delta Lakehouse – S3 (AWS) and ADLS Gen2 (Azure)"
- Place Delta Lake logo
- Show Bronze / Silver / Gold zones
- Show: "Customer 360", "Load Forecasts", "Generation Insights", "Financial Data"

GOVERNANCE:

- Band across the platform:
  - Place Unity Catalog logo
  - Label: "Unity Catalog – single governance plane across AWS and Azure"
  - Subtext: "Central catalogue, fine‑grained access, lineage, quality, PII controls"
  - "Unity Catalog Metric Views – unified semantic layer (Customer, Financial, Generation metrics)"
  - "Regulatory compliance built in (ASIC, AEMO, NEM data)"

PROCESSING & INTELLIGENCE:

- "Data Engineering & Streaming" – Lakeflow, LDP, Auto Loader
- "Analytics & AI/BI" – DBSQL, AI/BI Dashboards, AIBI Genie
- "Agentic AI & ML" – Agent Bricks, MLflow, Feature Store, Model Registry

CONSUMPTION:

- "Trusted data products" band feeding:
  - "Customer Experience" (kaluza offers, Amazon Connect agent assist, NPS tracking)
  - "Markets & Trading" (price forecasting, hedging optimization, risk dashboards)
  - "Generation & Assets" (predictive maintenance, dispatch optimization, asset dashboards)
  - "Finance & Compliance" (regulatory packs, CFO dashboards, audit intelligence)
  - "AI-driven decision agents" (churn prevention, tariff optimization, maintenance scheduling)

BENEFITS (GREEN CHECKMARKS):

- "One unified Lakehouse on AWS and Azure"
- "Unified Customer 360 for 4.1M services"
- "Real‑time AI/BI dashboards and AIBI Genie"
- "Agentic AI: churn, NPS, forecasting, maintenance agents"
- "Reduced cost: single platform, single governance, single tool"
- "Faster decision-making: 1-hour dashboards vs 3-day batches"
- "Regulatory confidence (ASIC, AEMO, NEM compliance)"
- "FY27 strategic targets enabled: NPS 20, digital growth, 2.1 GW renewable integration"

Overall styling: vibrant Databricks / AGL palette, clear flows towards central Lakehouse,
green success markers, AWS/Azure logos clearly positioned.

===== STYLE =====

- 16:9 landscape, crisp split down the middle
- BEFORE: grey tones, messy connectors, red problem markers, chaotic
- AFTER: vibrant Databricks / AGL palette, clean flows, green benefit markers, organised
- Designed to feel like a transformation slide a senior architect would use in an RFP
  defence meeting – clear, compelling, RFP‑grade visuals
```

---

## Summary

Six complete, production‑ready, AGL-contextualized prompts for Nano Banana Pro:

1. ✅ **Prompt 1** – Vertical Platform Stack (5 layers, AWS/Databricks/Azure columns, AGL domains)
2. ✅ **Prompt 2** – Horizontal Data Journey (5 phases, 3 swim lanes, AGL data flows)
3. ✅ **Prompt 3** – Concentric Ecosystem (4 rings, AWS/Azure split, 5 AGL domains)
4. ✅ **Prompt 4** – Three Workload Pillars (Analytics, Real‑Time Ops, Agentic AI for AGL)
5. ✅ **Prompt 5** – Federated Data Mesh (central Lakehouse, 5 AGL domain nodes)
6. ✅ **Prompt 6** – Before/After (legacy fragmentation vs unified AGL Databricks platform)

**All prompts include:**
- ✅ Logo Kit (Databricks, Delta Lake, Unity Catalog, kaluza, AGL, AWS, Azure)
- ✅ AIBI Dashboards, AIBI Genie, DBSQL
- ✅ Unity Catalog Metric Views (semantic layer)
- ✅ Agent Bricks (agentic AI/ML)
- ✅ AWS and Azure logos as explicit cloud markers
- ✅ **AGL Annual Report context**:
  - 3 operating segments: Customer Markets, Integrated Energy, Investments
  - 4.1M customer services across electricity, gas, broadband, mobile
  - kaluza (retail energy), Salesforce (CRM), Amazon Connect (call centre)
  - Generation assets: Bayswater, Loy Yang, Torrens Island, Liddell Battery, etc.
  - SAP ERP, financial systems, regulatory compliance (ASIC, AEMO)
  - OT/IoT from generation portfolio and grid-scale batteries
  - FY27 strategic targets: NPS, digital growth, renewable capacity, batteries
  - Key use cases: Customer 360, churn prediction, load forecasting, asset health, financial reporting
- ✅ No filenames in diagrams
- ✅ Modern reference architecture patterns
- ✅ RFP-ready language and clarity

