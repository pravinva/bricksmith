# AGL Energy - Synapse Decommission & Direct Databricks Consumption
## Migration Architecture: Eliminating the Middle Layer

---

## Executive Brief

Create a migration architecture diagram showing AGL's journey from a hybrid Databricks–Synapse architecture to a unified Databricks platform. The critical insight: Synapse is currently downstream of Databricks, serving only as a SQL read layer. Databricks already processes raw data into Parquet, which Synapse PolyBase ingests into Dedicated SQL Warehouse. This migration simplifies the architecture by eliminating Synapse entirely and redirecting consumers (Power BI, apps) directly to Databricks SQL, using Databricks Lakebridge and Agent Bricks coding assistants to accelerate conversion and validation.

---

## Visual Style & Brand Identity

### Design Language
- Style: Enterprise migration journey diagram with left-to-right timeline.
- Aesthetic: Clean, professional, transformation-focused.
- Background: Clean white (#FFFFFF).
- Orientation: Landscape 16:9.

### Color Palette

Primary:
- AGL Deep Blue: #001CB0 – structural elements and headers.
- Databricks Orange: #FF3621 – target state and Databricks components.
- Synapse Purple: #7B42BC – current Synapse components (fading out).
- Transition Grey: #95A5A6 – parallel operation period.
- Success Green: #00A651 – validation checkpoints and improvements.

Accent:
- Warning Orange: #F39C12 – complexity indicators being removed.
- Light Grey: #E5E5E5 – decommissioned components.

### Typography
- Headers: Bold sans-serif in AGL Deep Blue (#001CB0).
- Subheaders: Semibold sans-serif.
- Body: Regular sans-serif, 10–12pt, high contrast.

---

## Composition & Layout

Overall: Left-to-right journey with three major sections (Current State, Transition State, Target State), plus:
- Top migration-phase chevron bar.
- Bottom risk-mitigation layer.
- Right-side vertical constraints panel.

---

## Top Header Bar: Migration Phases (Chevron Style)

Horizontal chevron progression spanning full width:

ASSESS (Weeks 1–2) → PLAN (Weeks 3–4) → DESIGN (Weeks 5–6) → EXECUTE (Weeks 7–16) → OPTIMIZE (Weeks 17–20)

Styling:
- Background: AGL Deep Blue gradient.
- Text: White, bold.
- Chevron arrows pointing right.
- Optional progress indicator marker.

---

## Section 1: Current State – “The Unnecessary Intermediate Layer”

Large container on the far left.

### Header
- Label: “CURRENT STATE: Hybrid Architecture (Databricks → Synapse)”.
- Background: Light Grey (#E5E5E5).

### Vertical Stack (Top to Bottom)

1) Data Sources  
- Box label: “Data Sources”.  
- Icons: SAP S/4HANA, Ignition Gateway (SCADA), ADLS Gen2, Spot Price APIs.  
- Subtext: “Liddell/Tomago Battery, Bayswater SCADA Telemetry, Spot Prices”.

Arrow down labeled “Ingestion”.

2) Databricks Processing (Databricks orange box)  
- Label: “Databricks Platform”.  
- Sub-components:
  - Raw layer ingestion (Bronze).
  - Data processing with Spark (transformations).
  - Parquet conversion.
  - Write Parquet to ADLS Gen2.
- Border: 2px Databricks Orange (#FF3621).

Arrow down labeled “PolyBase Hydration”.

3) Synapse Read Layer (purple box with warning)  
- Label: “Azure Synapse Dedicated SQL Warehouse”.
- Icon: Synapse logo with warning triangle.
- Subtext: “Read-only layer, no transformation; hydrated from Databricks Parquet via PolyBase”.
- Components:
  - PolyBase external tables from Parquet.
  - Dedicated SQL Pool.
  - Views and stored procedures.
- Border: 2px Synapse Purple (#7B42BC).
- Background: Light purple with a subtle fade to suggest decommission.

Arrow down labeled “SQL Queries”.

4) Consumers  
Three boxes side-by-side:
- “Power BI Dashboards”.
- “Custom Applications”.
- “Business Analysts”.
All connect to the Synapse SQL endpoint.

### Critical Insight Callout

Floating annotation box near the Databricks → Synapse arrow:
- Border: 3px Warning Orange (#F39C12), background light yellow.
- Icon: Lightbulb.
- Text:
  - “Synapse adds no transformation value. Databricks already prepares Parquet. Synapse is only a SQL read layer over Databricks-managed data. Removing Synapse simplifies architecture and reduces cost.”

### Pain-Points Bar (Far Left)

Vertical bar labeled “Why Eliminate Synapse?” listing pain points with red X icons:
- “Redundant read layer”.
- “Dual security / RBAC models”.
- “PolyBase hydration latency”.
- “Synapse licensing and operational overhead”.
- “Limited ML/AI capabilities compared to Databricks”.

---

## Section 2: Transition State – “Parallel Operation & Consumer Redirection”

Large central container representing the 8–12 week bridge period.

### Header
- Label: “TRANSITION STATE: Parallel Operation & Consumer Redirection”.
- Subtext: “Duration: 8–12 weeks”.
- Background: Transition Grey (#95A5A6).

Two horizontal swim lanes plus a migration accelerators bar.

### Swim Lane A (Top): Consumer Migration Track

Four steps (boxes left to right with arrows):

1) Power BI Connection Assessment  
- Inventory all reports/datasets currently pointed at Synapse.  
- Document SQL dependencies and data sources.  
- Icon: Checklist.

2) DBSQL Endpoint Configuration  
- Create Databricks SQL Warehouses with appropriate sizing.  
- Configure catalogs/schemas mirroring the Synapse presentation layer.  
- Icon: Database configuration.

3) Connection String Updates  
- Update Power BI and application connection strings from Synapse endpoint to DBSQL endpoint.  
- Parameterize dev/test/prod environments.  
- Icon: Plug/cable.

4) User Acceptance Testing  
- Compare visuals and metrics between Synapse-backed and DBSQL-backed reports.  
- Target: 99.99% parity.  
- Icon: Shield with checkmark.

### Swim Lane B (Bottom): Technical Validation Track

Four steps:

1) SQL Compatibility Analysis  
- Catalogue Synapse views, stored procedures, and T‑SQL patterns.  
- Identify incompatible constructs and migration complexity.  
- Icon: Code comparison.

2) Performance Benchmarking  
- Baseline query latency on Synapse.  
- Benchmark equivalent workloads on DBSQL.  
- Goal: Match or exceed Synapse performance.  
- Icon: Speedometer.

3) Security & Governance Mapping  
- Map Synapse RBAC and database roles to Unity Catalog privileges.  
- Ensure row-level and object-level security parity.  
- Icon: Shield + key.

4) Parallel Validation Period  
- Run both Synapse and Databricks in parallel.  
- Monitor query performance, correctness, and user adoption.  
- Ensure documented rollback procedures.  
- Icon: Parallel arrows.

### Migration Control Tower (Center)

A central box bridging the two swim lanes:
- Label: “Migration Command Center”.
- Icon: Control tower.
- Internal bullets:
  - Monitoring dashboard (performance, correctness, usage).
  - Validation gates and approvals.
  - Rollback plan.
  - Stakeholder communications.

### Migration Accelerators: Lakebridge and Agent Bricks

Horizontal box directly under the two swim lanes labeled:  
“Databricks Migration Accelerators”.

Split into two equal segments:

1) Lakebridge (SQL and ETL Migration)  
- Label: “Databricks Lakebridge – Automated Code and Data Migration”.  
- Bullet points:
  - Profiles existing Synapse SQL views, stored procedures, and ETL jobs.
  - Automatically converts approximately 70–80% of T‑SQL and ETL logic to Databricks SQL / Spark-compatible code.
  - Generates schema and data parity reports (row-count and aggregate checks) to validate that Databricks results match Synapse.
- Visual details:
  - Icon: Gear + SQL document.
  - Small tag on any SQL migration arrow: “Lakebridge-generated SQL”.

2) Agent Bricks Coding Assistant  
- Label: “Agent Bricks Coding Assistant – Assisted Conversion & Refactoring”.
- Bullet points:
  - Gen‑AI agent, built with Agent Bricks, trained on AGL’s Synapse SQL patterns to propose equivalent Databricks SQL and PySpark code snippets for complex objects.
  - Helps engineers refactor complex stored procedures, UDFs, and orchestration logic into modern lakehouse patterns (e.g., MERGE INTO Delta, incremental upserts).
  - Suggests performance optimizations and best practices during interactive migration sessions.
- Visual details:
  - Icon: Chat bubble + code brackets.
  - Dotted helper arrows from complex SQL icons in the Current State to Databricks columns in the Target State labeled “AI-assisted refactor”.

Styling for the accelerators box:
- Background: Very light Databricks Orange tint.
- Border: 1–2px AGL Navy (#1C355E).

### Validation Gates

Three vertical gate markers along the timeline:

- Gate 1: “PoC Complete – Customer Markets domain”.
- Gate 2: “Pilot Validated – Energy Markets domain”.
- Gate 3: “Production Cutover Approved – Energy Assets (safety-critical)”.

Each gate:
- Background: Success Green (#00A651).
- Icon: Checkmark.
- Gate 3 additionally includes a safety shield icon.

### Migration Waves Panel (Right of Section 2)

Vertical panel listing waves:

- Wave 1: Customer Markets (non-critical analytics).
- Wave 2: Energy Markets (trading, hedging).
- Wave 3: Energy Assets (SCADA, operational telemetry – safety critical).

Note on Wave 3:
- “Zero downtime; extended validation and rollback readiness.”

---

## Section 3: Target State – “Unified Databricks Platform”

Large container on the far right showing the simplified target architecture.

### Header
- Label: “TARGET STATE: Direct Databricks Consumption”.
- Background: Databricks Orange gradient.
- Small Databricks logo.

### Vertical Stack (Top to Bottom)

1) Data Sources  
- Same systems as current state: SAP S/4HANA, Ignition Gateway, ADLS Gen2, Spot Price APIs.  
- Arrow down labeled “Lakeflow Connect Ingestion”.

2) Databricks Data Intelligence Platform (Hero Container)  
- Label: “Databricks Platform – Single Source of Truth”.
- Four vertical columns inside:
  - Lakeflow – “Ingest, ETL & Streaming”.
  - Databricks AI – “Data Science & Agent Bricks”.
  - DBSQL – “Data Warehousing & BI”.
  - Lakebase – “Serverless Postgres – Transactional Workloads”.
- Medallion overlay in Lakeflow column:
  - Bronze → Silver → Gold with Delta/Parquet icons.
- Unity Catalog bar across the bottom:
  - Text: “Unity Catalog – Unified Governance, Security & Lineage”.

3) Consumers (Now Directly Connected to Databricks)  
Three boxes side-by-side:
- “Power BI Dashboards” (direct to DBSQL).
- “Custom Applications” (direct to DBSQL and Lakebase).
- “AI Agents & Copilots” (via Agent Bricks / Agent Bricks).
All arrows are solid Databricks Orange and labeled “Direct SQL Access”.

### Benefits Callout

Floating box near the target architecture:
- Border: Success Green, background light green.
- Bullets:
  - “Synapse removed: license and operations cost eliminated.”
  - “Single governance model via Unity Catalog.”
  - “No PolyBase hydration latency.”
  - “Real-time analytics and AI-ready lakehouse.”
  - “Less complexity, fewer moving parts.”

### Performance Metrics Panel

Three metric tiles:
- “Query performance: target 2–4× faster vs. Synapse.”
- “Total cost of ownership: 30–40% reduction.”
- “Operational overhead: ≥50% reduction in platform surface area.”

---

## Bottom Footer: Risk Mitigation & Success Metrics

Full-width bar at the bottom.

### Label
- “Risk Mitigation Strategy & Success Metrics”.

### Styling
- Background: AGL Deep Blue at 10% opacity.

### Five Connected Boxes

1) Zero Downtime Strategy  
- Parallel run period for each domain.  
- Phased cutover by domain.  
- Icon: Uptime graph.

2) Data Integrity Validation  
- Automated row-count and aggregate checks between Synapse and Databricks results.  
- Target: 99.99% match rate.  
- Icon: Magnifying glass.

3) Rollback Procedures  
- Documented rollback per wave.  
- Synapse kept warm until each domain is signed off.  
- Icon: Circular arrow.

4) Security & Compliance  
- Synapse permissions remapped to Unity Catalog.  
- ESG and regulatory reporting verified end-to-end.  
- Audit logs maintained.  
- Icon: Shield with checkmark.

5) Change Management  
- Training for BI developers and analysts on DBSQL and Unity Catalog.  
- Documentation updates and handover.  
- Icon: People with graduation cap.

Each box:
- Background: White.
- Border: 1px Success Green.
- Dotted connector lines between boxes.

---

## Right-Side Vertical Panel: Critical Constraints

Vertical column spanning Sections 2–3.

### Header
- “Critical Constraints”.

### Boxes

1) Safety-Critical Systems  
- “Energy Assets domain – zero tolerance for downtime.”  
- “Additional validation and approval gates required.”  
- Icon: Shield + warning.

2) Regulatory Continuity  
- “ESG and market reporting must remain uninterrupted.”  
- Icon: Document with tick.

3) Multi-Cloud Maintained  
- AWS (Customer/Retail) and Azure (Operational/Assets) remain as-is.  
- Icon: Two clouds.

4) Performance SLA  
- “DBSQL performance must meet or exceed Synapse baselines for key workloads.”  
- Icon: Stopwatch.

Styling:
- Background: White.
- Border: 2px AGL Navy.

---

## Critical Data Flow Arrows

### Current State
- Data Sources → Databricks: Solid blue arrow labeled “Ingestion”.
- Databricks → Synapse: Solid purple arrow labeled “PolyBase hydration from Parquet”.
- Synapse → Consumers: Solid purple arrow labeled “SQL queries”.

### Transition State
- Dotted green arrows showing validation comparisons (Synapse vs DBSQL results).
- Dashed orange arrows showing consumers moving from Synapse endpoint to DBSQL endpoint (connection cutover).

### Target State
- Data Sources → Databricks via solid orange arrow labeled “Lakeflow Connect”.
- Databricks DBSQL / Lakebase → Consumers via solid orange arrows labeled “Direct SQL access”.

Arrow styling:
- Width: 3–4px for primary flows.
- Colors: Match platform (blue, purple, orange).
- Solid for active flows, dashed for migration actions, dotted for validation.

---

## Special Annotations

1) Parquet Flow (Current State)  
- “Databricks writes Parquet to ADLS Gen2. Synapse PolyBase uses these Parquet files to hydrate the Dedicated SQL Pool.”

2) Lakebridge Annotation  
- “Lakebridge automates discovery, conversion, and validation of Synapse SQL and ETL to Databricks SQL/Spark, significantly reducing manual migration effort.”

3) Agent Bricks Annotation  
- “Agent Bricks coding assistant helps engineers translate and modernize complex T‑SQL patterns into Databricks SQL and PySpark using a gen‑AI agent tailored to AGL’s codebase.”

4) Unity Catalog Advantage  
- “Unity Catalog becomes the single governance spine replacing Synapse RBAC and separate security models.”

---

## Technical Accuracy Checklist

Ensure the diagram:

- Shows Databricks as the current processing engine producing Parquet that hydrates Synapse via PolyBase.
- Depicts Synapse as a read-only SQL layer, not the primary compute engine.
- Shows migration as:
  - Parallel operation.
  - Consumer redirection.
  - SQL compatibility and performance validation.
- Includes Lakebridge for automated profiling, conversion, and parity validation.
- Includes Agent Bricks for AI-assisted conversion of complex T‑SQL and UDFs.
- Presents the target state as a simplified Databricks-only consumption pattern with DBSQL and Lakebase.
- Shows Unity Catalog providing unified governance.
- Maintains multi-cloud and AGL’s energy context (SCADA, batteries, markets).
- Respects safety-critical and regulatory constraints.

---

## Output Specifications

- Format: PNG or SVG (vector preferred).
- Resolution: Minimum 1920×1080, ideally 2560×1440 (2K).
- Aspect ratio: 16:9 landscape.
- Filename: `AGL_Synapse_Decommission_Lakebridge_AgentBricks_2026.png`.

---

## Success Criteria

The diagram is successful if:

1. Stakeholders clearly see that Synapse is a redundant read layer on top of Databricks.
2. The migration is framed as simplification and cost reduction, not a risky re-platform.
3. Lakebridge and Agent Bricks are visible as key accelerators reducing manual conversion effort.
4. Risk mitigation (parallel run, rollback, safety-critical constraints) is clear and credible.
5. Executives can understand the story in under one minute.
6. Engineers can use the diagram as a blueprint for execution.
