Subject:
AGL Energy - Azure Synapse to Databricks Migration Architecture
Multi-Phase Journey Diagram with Parallel Operation Strategy

Style:
Enterprise migration roadmap. Left-to-right timeline with swim lanes.
Clean white background with progress indicators.
Color Palette: 
- Synapse Purple (#7B42BC) for current state (left)
- Transition Grey (#95A5A6) for parallel operation (middle)
- Databricks Orange (#FF3621) for target state (right)
- AGL Deep Blue (#001CB0) for structural elements
- Success Green (#00A651) for validation checkpoints

Layout (Left-to-Right Timeline with 3 Major Sections):

SECTION 1: CURRENT STATE (Synapse Environment)
- Top box: "Azure Synapse Analytics - Current Operational Environment"
- Four vertical pillars showing:
  1. Dedicated SQL Pool (with AGL domains: Customer Markets, Energy Assets, Energy Markets)
  2. Synapse Pipelines (ETL orchestration)
  3. Synapse Notebooks (transformation logic)
  4. Data Sources (SAP S/4HANA, Ignition Gateway, ADLS Gen2, Spot Price APIs)
- Bottom annotation: "Asset Telemetry: Liddell/Tomago Battery, Bayswater SCADA"
- Performance metrics box: Query performance baseline, Cost baseline

SECTION 2: TRANSITION STATE (Parallel Operation - THE BRIDGE)
- Large central container labeled "Parallel Operation Period (8-12 weeks)"
- Two parallel horizontal tracks:

  TRACK A (Top): Data Migration Pipeline
  - Step 1: Schema Assessment & Mapping
  - Step 2: ADLS Gen2 Staging (Bronze layer creation)
  - Step 3: Delta Lake Conversion (with ACID validation)
  - Step 4: Data Quality Validation (compare Synapse vs Databricks output)
  
  TRACK B (Bottom): Application Migration Pipeline
  - Step 1: Notebook Conversion (Synapse → Databricks notebooks)
  - Step 2: Pipeline Refactoring (Synapse Pipelines → Lakeflow/Workflows)
  - Step 3: Power BI Re-pointing (connection string updates)
  - Step 4: User Acceptance Testing

- Central hub icon: "Migration Control Tower"
  - Monitoring dashboard
  - Rollback procedures
  - Validation gates

- Three vertical colored gates between stages:
  Gate 1: "PoC Complete (Single Domain)"
  Gate 2: "Production Pilot (Customer Markets)"
  Gate 3: "Full Cutover Approved"

SECTION 3: TARGET STATE (Databricks Platform)
- Top box: "Databricks Data Intelligence Platform - Target Architecture"
- Recreate simplified AGL Databricks architecture:
  - Lakeflow (ingestion)
  - Databricks AI (with Agent Bricks)
  - DBSQL (data warehousing)
  - Lakebase (transactional)
- Unity Catalog bar (governance layer)
- Delta Lake storage (with Iceberg support)
- Multi-cloud foundations (AWS + Azure maintained)

- Performance improvement callouts:
  "4x Query Performance"
  "30% Cost Reduction"
  "Real-Time ML Enabled"

TOP HEADER BAR (Process Phases - Chevron Style):
ASSESS (Weeks 1-2) → PLAN (Weeks 3-4) → DESIGN (Weeks 5-7) → EXECUTE (Weeks 8-20) → OPTIMIZE (Weeks 21-24)

BOTTOM FOOTER (Risk Mitigation Layer):
- Five connected boxes:
  1. Zero Downtime Strategy (parallel operation)
  2. Data Integrity Validation (automated checksums)
  3. Rollback Procedures (point-in-time recovery)
  4. Security & Compliance (Unity Catalog RBAC)
  5. Change Management (training & documentation)

RIGHT-SIDE VERTICAL PANEL: Migration Waves
- Wave 1: PoC (Customer Markets - Non-Critical)
- Wave 2: Pilot (Energy Markets - Medium Criticality)
- Wave 3: Production (Energy Assets - SAFETY CRITICAL)
- Wave 4: Decommission Synapse

LEFT-SIDE ANNOTATION: Key Constraints
- "Safety-Critical Systems: Zero Tolerance for Downtime"
- "Regulatory: ESG Reporting Continuity Required"
- "Multi-Cloud: AWS + Azure Maintained"

CRITICAL DATA FLOW ARROWS:
1. Synapse → ADLS Gen2 Staging (thick blue arrow)
2. ADLS Gen2 → Delta Lake (thick orange arrow with "Lakeflow Connect" label)
3. Parallel validation arrows (dotted green) between Synapse and Databricks outputs
4. Power BI reconnection arrows (from Synapse to Databricks DBSQL)
5. Ignition Gateway direct connection to both Synapse (during transition) and Databricks (post-cutover)

CALLOUT BOXES (Floating annotations):
- "SAP S/4HANA Integration: Lakeflow Connectors"
- "Real-Time SCADA Data: Streaming Tables"
- "Medallion Architecture: Bronze → Silver → Gold maintained"
- "Unity Catalog: Replaces Synapse RBAC + Purview"

SUCCESS METRICS DASHBOARD (Bottom Right):
- Migration completion: X% (progress bar)
- Data validation: 99.99% match rate
- Application compatibility: Y/Z apps migrated
- User training: N users certified
