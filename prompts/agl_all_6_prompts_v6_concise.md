# AGL DATABRICKS RFP – Bricksmith Prompt Suite (v6 – Concise)
## Six Prompts – Dual‑Cloud (AWS + Azure), AIBI, Agent Bricks, Metric Views + AGL Context (Less Verbose)

Simplified, cleaner prompts that produce less text on diagrams while maintaining strategic intent.

---

# PROMPT 1 – Vertical Stack (5 Layers, 3 Columns)


===== PROMPT BODY =====

You are a Databricks Solutions Architect designing AGL Energy's unified data platform.

Create a VERTICAL STACKED ARCHITECTURE with 5 layers and 3 columns (AWS | Databricks | Azure).
Style: Modern, minimal, clean like a16z / Databricks reference architectures.
Purpose: Show how AGL unifies Customer Markets (AWS), Integrated Energy (Azure) and Investments
via a central Databricks Lakehouse.

===== STRUCTURE =====

LAYERS (bottom to top):
1. Cloud Infrastructure
2. Storage & Governance
3. Processing & Intelligence
4. Data Products
5. Business Outcomes

COLUMNS:
- LEFT: AWS (orange accents)
- CENTRE: Databricks (slate/red)
- RIGHT: Azure (blue accents)

===== LAYER 1 – CLOUD INFRASTRUCTURE =====

AWS:
- [AWS logo] Small badge at top
- Icons: S3, Kinesis, EC2
- Label: "kaluza, Salesforce, Amazon Connect"

Databricks:
- [Databricks logo]
- "Workspaces & Control Plane"

Azure:
- [Azure logo] Small badge at top
- Icons: ADLS, Event Hubs, Data Factory
- Label: "SAP, OT/SCADA, Market Data"

===== LAYER 2 – STORAGE & GOVERNANCE =====

AWS:
- [Delta Lake logo] Small
- "Delta Lake on S3 (Bronze/Silver/Gold)"
- "Customer Data"

Databricks (full width, two sub-bands):
- Top: [Delta Lake logo] "Unified Delta Lakehouse"
- Bottom: [Unity Catalog logo] "Unity Catalog + Metric Views (Governance, PII, Lineage)"

Azure:
- [Delta Lake logo] Small
- "Delta Lake on ADLS (Bronze/Silver/Gold)"
- "SAP, OT/IoT, Markets"

===== LAYER 3 – PROCESSING & INTELLIGENCE =====

Centre only (single box with 3 sub-sections):
- "Data Eng: Lakeflow, LDP, Auto Loader"
- "Analytics: DBSQL, AI/BI Dashboards, AIBI Genie"
- "AI/ML: Agent Bricks, MLflow, Feature Store"

===== LAYER 4 – DATA PRODUCTS =====

AWS:
- "Customer 360"
- "NPS & Churn"
- "Tariff Offers"

Centre (connecting):
- Arrows pointing up and down

Azure:
- "Generation Insights"
- "Load Forecasting"
- "Financial Metrics"

===== LAYER 5 – BUSINESS OUTCOMES =====

Single band, left to right:
- "NPS Leadership (20)"
- "Digital Growth (60%)"
- "Asset Performance"
- "Regulatory Confidence"

===== VISUAL STYLE =====

16:9 landscape. Minimal text. Large white space. No filenames.
AWS orange, Azure blue, Databricks red accents only.
```

---

# PROMPT 2 – Data Journey (5 Phases, 3 Lanes)

```text
===== LOGO KIT – CRITICAL INSTRUCTIONS =====

[Same as Prompt 1]

===== PROMPT BODY =====

You are a Databricks Solutions Architect.

Create a HORIZONTAL DATA JOURNEY diagram (left to right) with 5 phases and 3 swim lanes.
Style: Modern data-flow, like emerging architectures diagrams.
Purpose: Show AGL's data flowing from AWS/Azure → Lakehouse → Decisions/Agents.

===== STRUCTURE =====

3 SWIM LANES:
- Top: AWS (orange) – kaluza, Salesforce, Amazon Connect
- Middle: Databricks Platform (slate/red)
- Bottom: Azure (blue) – SAP, SCADA, Markets

5 PHASES (left to right):
1. Ingest
2. Transform
3. Govern
4. Analyse (AI/BI)
5. Activate (Agents)

===== PHASE 1 – INGEST =====

AWS lane: Events, records, call logs
Azure lane: Transactions, SCADA, market feeds
Middle: Lakeflow, Auto Loader icon

===== PHASE 2 – TRANSFORM =====

Middle (full width):
- [Delta Lake logo]
- "Bronze → Silver → Gold"
- "Spark, Photon, Streaming"

===== PHASE 3 – GOVERN =====

Middle (full width):
- [Unity Catalog logo]
- "Single Governance Plane"
- "Metric Views (Semantic Layer)"

===== PHASE 4 – ANALYSE =====

Middle:
- "DBSQL, AI/BI Dashboards, AIBI Genie"

AWS lane: Executive dashboards
Azure lane: Trader dashboards

===== PHASE 5 – ACTIVATE =====

Middle:
- "Agent Bricks, MLflow, Model Serving"

AWS lane: Churn agents, tariff agents, assist
Azure lane: Maintenance agents, trading agents, forecast agents

===== VISUAL STYLE =====

16:9 landscape. Converging arrows from clouds into centre, then fanning out.
Minimal text. No filenames. Clean flows.
```

---

# PROMPT 3 – Concentric Rings (4 Rings, Dual-Cloud Split)

```text
===== LOGO KIT – CRITICAL INSTRUCTIONS =====

[Same as Prompt 1]

===== PROMPT BODY =====

You are a Databricks Solutions Architect.

Create a CONCENTRIC RING diagram (target/bullseye) showing AGL's platform ecosystem.
Style: Balanced, clean rings like modern platform architecture diagrams.
Purpose: Show Databricks core, shared services, cloud systems (AWS left / Azure right),
and 5 business domains around the outside.

DO NOT label rings as "Ring 1 / Ring 2" etc. Use only business and technical labels.

===== RING STRUCTURE =====

INNER CORE:
- [Databricks logo]
- "AGL Unified Energy Data Platform"
- Sub-rings: [Delta Lake logo] Storage | Processing | [Unity Catalog logo] Governance

RING 2 (Shared Services):
- Divide into 3 sectors (120° each):
  - "Data Eng" (Lakeflow, LDP, Auto Loader)
  - "Analytics" (DBSQL, AI/BI, AIBI Genie)
  - "AI/ML" (Agent Bricks, MLflow)

RING 3 (Cloud Systems):
- Split LEFT (AWS, orange) | RIGHT (Azure, blue)

LEFT (AWS):
- [AWS logo] Badge
- "kaluza, Salesforce, Amazon Connect"
- "4.1M Customer Services"

RIGHT (Azure):
- [Azure logo] Badge
- "SAP, SCADA, Markets"
- "Generation & Finance"

RING 4 (Domains):
- 5 segments (72° each):
  1. "Retail Energy" [Kaluza logo] – AWS chip
  2. "Call Centre" – AWS chip
  3. "Markets & Trading" – Neutral chip
  4. "Generation & Assets" – Azure chip
  5. "Finance & Compliance" – Azure chip

===== VISUAL STYLE =====

16:9 landscape. Soft drop shadows on inner rings. AWS orange / Azure blue accents on Ring 3.
Minimal text labels. No filenames. Clean, balanced layout.
```

---

# PROMPT 4 – Three Workload Pillars

```text
===== LOGO KIT – CRITICAL INSTRUCTIONS =====

[Same as Prompt 1]

===== PROMPT BODY =====

You are a Databricks Solutions Architect.

Create a THREE-COLUMN WORKLOAD PATTERN diagram showing how AGL's Lakehouse supports
three distinct data workload patterns on AWS and Azure.

Style: Clean, three equal columns, modern data-platform style.
Purpose: Show that Analytics, Real-Time Ops, and Agentic AI all run identically on both clouds.

===== COLUMNS =====

Each column has 3 layers: INGEST | LAKEHOUSE CORE | CONSUMPTION

===== COLUMN 1 – ANALYTICS & AI/BI =====

Ingest:
- "Batch: SAP, kaluza, SCADA"

Lakehouse Core:
- [Delta Lake logo]
- "Gold tables: Customer, Financial, Generation Metrics"
- [Unity Catalog logo] "Metric Views"

Consumption:
- "DBSQL, AI/BI Dashboards, AIBI Genie"
- "Executive & trader dashboards"

AWS/Azure badges (top-right): "Runs on AWS and Azure"

===== COLUMN 2 – REAL-TIME OPERATIONS =====

Ingest:
- "Streaming: Kinesis, Event Hubs, IoT"

Lakehouse Core:
- [Delta Lake logo]
- "Fresh Gold tables (sub-second latency)"
- "Real-time facts: Customer, Generation, Market"

Consumption:
- "Operational dashboards"
- "Real-time APIs, reverse ETL"
- "Agent assist (in-call, dispatch)"

AWS/Azure badges: "Runs on AWS and Azure"

===== COLUMN 3 – AGENTIC AI & ML =====

Ingest:
- "Features: Gold tables, telemetry"

Lakehouse Core:
- [Delta Lake logo]
- "Feature Store, ML tables"
- [Unity Catalog logo] "Versioned, governed"

Consumption:
- "Agent Bricks orchestration"
- "Agents: Churn, NPS, Load, Maintenance"
- "MLflow, Model Serving"

AWS/Azure badges: "Runs on AWS and Azure"

===== BOTTOM GOVERNANCE BAR =====

Full-width:
- [Unity Catalog logo]
- "Unity Catalog – Consistent governance across all workloads"

===== VISUAL STYLE =====

16:9 landscape. Three equal columns, light tints (blue/green/purple).
Minimal text. No filenames. Modern, clean.
```

---

# PROMPT 5 – Federated Data Mesh

```text
===== LOGO KIT – CRITICAL INSTRUCTIONS =====

[Same as Prompt 1]

===== PROMPT BODY =====

You are a Databricks Solutions Architect.

Create a FEDERATED DATA MESH diagram showing AGL's 5 business domains owning data products
on a central Databricks Lakehouse.

Style: Network diagram with central hub and 5 surrounding nodes.
Purpose: Show decentralised domain ownership + centralised governance on dual-cloud Lakehouse.

===== CENTRAL PLATFORM =====

Hexagon or circle in centre:
- [Databricks logo]
- "Databricks Lakehouse (AWS + Azure)"
- Sub-layers (3 rings):
  - [Delta Lake logo] "Delta Lake (S3 + ADLS)"
  - "Compute: Spark, DBSQL, Feature Store, Agent Bricks"
  - [Unity Catalog logo] "Governance & Metric Views"

Bottom: [AWS logo] [Azure logo] "Deployed on AWS and Azure"

===== DOMAIN NODES (5) =====

Arranged in circle around centre. Each node has 3 layers:
- Top: Sources (icons, minimal text)
- Middle: Data Product name (Delta tables + UC icon)
- Bottom: Consumers (tools, brief labels)

DOMAIN 1 – Retail Energy:
- Sources: kaluza, CRM, web
- Product: "Customer 360"
- [Kaluza logo] (optional, prominently placed)
- Consumers: kaluza offers, churn agents
- AWS chip

DOMAIN 2 – Call Centre:
- Sources: Amazon Connect
- Product: "Contact Performance"
- Consumers: Agent assist, NPS dashboards
- AWS chip

DOMAIN 3 – Markets & Trading:
- Sources: Market feeds, hedging
- Product: "Market Analytics"
- Consumers: Trader dashboards, agents
- Neutral chip

DOMAIN 4 – Generation & Assets:
- Sources: SCADA, historian
- Product: "Asset Health"
- Consumers: Maintenance agents, dispatch
- Azure chip (IoT icon)

DOMAIN 5 – Finance & Compliance:
- Sources: SAP, GL
- Product: "Financial Data"
- Consumers: CFO dashboards, regulatory agents
- Azure chip

===== CONNECTIONS =====

Lines from each domain's product layer back to Delta Lake in centre.
Small UC icons on lines show governance flowing outward.
Selected cross-domain arrows (Retail ↔ Markets, Gen ↔ Finance) show data sharing.

===== MESSAGE =====

Bottom: "Decentralised ownership, centralised governance"

===== VISUAL STYLE =====

16:9 landscape. Network layout. Soft pastels on domain nodes. Central platform darker.
Minimal text. No filenames. Clean, balanced.
```

---

# PROMPT 6 – Before/After Transformation

```text
===== LOGO KIT – CRITICAL INSTRUCTIONS =====

[Same as Prompt 1]

===== PROMPT BODY =====

You are a Databricks Solutions Architect.

Create a BEFORE/AFTER SPLIT-SCREEN diagram showing AGL's transformation from
fragmented, single-cloud legacy to unified dual-cloud Databricks platform.

Style: Left (grey, chaotic) vs Right (vibrant, clean).
Purpose: RFP-compelling transformation narrative.

===== STRUCTURE =====

LEFT HALF: "BEFORE – Fragmented Legacy"
RIGHT HALF: "AFTER – Unified Databricks Lakehouse"
CENTRE: Bold divider labelled "Databricks Transformation"

===== BEFORE SIDE (Grey, Muted, Chaotic) =====

STORAGE:
- Scattered boxes: "Data Warehouse", "kaluza silos", "SAP systems"
- "S3 buckets", "ADLS buckets" – disconnected
- "Spreadsheets, CSVs"
- Red X: "No central hub"

GOVERNANCE:
- Multiple metadata catalogues (kaluza, SAP, custom)
- Red X: "No lineage, no PII controls"
- Red X: "Inconsistent policies"

PROCESSING:
- Separate Spark clusters (one per system)
- Multiple SQL engines (Hive, Presto, custom)
- Red X: "3-day batch cycles"
- Red X: "No real-time"

CONSUMPTION:
- Siloed BI: "Tableau (Finance only)", "Power BI (Ops only)"
- Red X: "No unified customer view"
- Red X: "No AI/BI, no agents"

PAIN POINTS (Red text):
- "Data duplication"
- "High cost (multiple warehouses)"
- "Slow reporting cycles"
- "Tool sprawl"
- "Siloed teams"
- "Compliance risk"

===== AFTER SIDE (Vibrant, Organised, Clean) =====

CORE PLATFORM:
- Central box: "Databricks Data Intelligence Platform"
- [Databricks logo]

CLOUD ZONES:

Left zone:
- [AWS logo] header
- "kaluza, Salesforce, Amazon Connect"
- S3, Kinesis icons
- Arrows flowing → centre

Right zone:
- [Azure logo] header
- "SAP, SCADA, Markets"
- ADLS, Event Hubs icons
- Arrows flowing → centre

STORAGE:
- [Delta Lake logo]
- "Unified Delta Lakehouse (S3 + ADLS)"
- Show: Bronze/Silver/Gold zones
- Show: "Customer 360", "Forecasts", "Insights", "Finance"

GOVERNANCE:
- [Unity Catalog logo]
- "Unity Catalog: Single governance"
- "Metric Views, lineage, PII, compliance"

PROCESSING:
- "Data Eng: Lakeflow, LDP"
- "Analytics: DBSQL, AI/BI, AIBI Genie"
- "AI/ML: Agent Bricks, MLflow"

CONSUMPTION:
- "Customer insights"
- "Market dashboards"
- "Asset performance"
- "Finance + compliance"
- "Agentic AI decisions"

BENEFITS (Green checkmarks):
- "Unified platform on AWS + Azure"
- "Unified customer view (4.1M)"
- "Real-time dashboards + AI/BI"
- "Agentic automation"
- "Reduced cost"
- "Faster decisions"
- "Regulatory confidence"
- "FY27 targets enabled"

===== VISUAL STYLE =====

16:9 landscape. BEFORE: grey, tangled arrows, red X's (chaotic).
AFTER: vibrant (Databricks + AGL palette), clean flows, green checks (organised).
RFP-grade transformation narrative.
```

---

## Summary

Six streamlined, less-verbose prompts for Bricksmith Pro:

| Prompt | Focus | Key Feature |
|--------|-------|---|
| **1. Vertical Stack** | 5 layers, 3 columns | AWS/Databricks/Azure split |
| **2. Horizontal Journey** | 5 phases, data flow | Ingest→Transform→Govern→Analyse→Activate |
| **3. Concentric Rings** | Ecosystem, 4 rings | Central Lakehouse + 5 domains |
| **4. Three Pillars** | Workloads | Analytics, Real-Time, Agents |
| **5. Data Mesh** | Domains | Decentralised ownership + central governance |
| **6. Before/After** | Transformation | Chaotic legacy vs unified platform |

**All include:**
- ✅ Logo Kit (Databricks, Delta Lake, Unity Catalog, kaluza, AGL, AWS, Azure)
- ✅ AIBI, DBSQL, Agent Bricks, Metric Views
- ✅ AGL context (3 segments, 4.1M customers, generation assets, SAP, SCADA)
- ✅ **Minimal text** – cleaner diagrams
- ✅ No filenames
- ✅ RFP-ready

