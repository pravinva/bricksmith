# AGL Energy: Azure Synapse to Databricks Migration
## Technical Architecture Brief

---

## **Subject Line (For Decision-Makers)**
**Zero-Downtime Synapse Migration via Databricks Lakebridge: A Phased, Safety-Critical Energy Platform Approach**

---

## **Executive Context**
AGL is already leveraging Databricks' raw → Parquet ingestion layer (Bronze layer) within the existing Synapse environment. This migration architecture demonstrates how to operationalize that foundational work while migrating to a unified Databricks Data Intelligence Platform. The approach employs Databricks Lakebridge for automated SQL/ETL assessment, conversion, and post-migration reconciliation—enabling zero-downtime migration of safety-critical SCADA, telemetry, and financial workloads across four production waves.

---

## **Core Migration Architecture Overview**

### **Three-Stage Lifecycle with Shadow-Mode Parallel Operation**

The migration follows a structured three-stage model, with a critical 8–12 week parallel operation period where Synapse and Databricks run simultaneously, validated via shadow-mode comparison before full cutover.

**Visual Layout: Left-to-Right Timeline with Three Discrete Sections**

1. **STAGE 1: CURRENT STATE (Synapse Environment)**
   - **Operational Stack**: Azure Synapse Analytics (Dedicated SQL Pool + Pipelines + Notebooks)
   - **Data Architecture**: 
     - Domain-specific pools (Customer Markets, Energy Assets, Energy Markets)
     - Synapse Pipeline orchestration → ADLS Gen2 staging → existing Bronze/Silver/Gold medallion
   - **Critical Data Flows**:
     - SAP S/4HANA → Synapse (financial/operational)
     - Ignition Gateway → Synapse (real-time SCADA: Liddell/Tomago Battery, Bayswater SCADA)
     - Spot Price APIs → Synapse (energy market data)
   - **Performance Baseline**: Query latency, cost-per-query, concurrent user limits
   - **Governance**: Synapse RBAC + Azure Purview integration

2. **STAGE 2: TRANSITION STATE (Parallel Operation via Shadow Mode)**
   - **Parallel Period Duration**: 8–12 weeks
   - **Data Migration Pipeline (Track A)**:
     - Step 1: Lakebridge Analyzer → assess all SQL workloads, complexity, effort estimates
     - Step 2: Schema mapping & ADLS Gen2 Bronze layer creation (leveraging existing infrastructure)
     - Step 3: Lakebridge Converter → transpile Synapse SQL/ETL to Databricks Spark SQL
     - Step 4: Delta Lake conversion with ACID validation + schema enforcement
     - Step 5: Lakeflow Connect ingestion setup (managed connectors for SAP, Ignition Gateway; standard connectors for APIs)
   - **Application Migration Pipeline (Track B)**:
     - Synapse Notebooks → Databricks Notebooks (via Lakebridge)
     - Synapse Pipelines → Lakeflow Spark Declarative Pipelines (serverless, auto-orchestrated)
     - Power BI connection string updates (Synapse DBSQL → Databricks DBSQL)
     - User Acceptance Testing (UAT) phase
   - **Shadow-Mode Validation Framework**:
     - Both systems run in parallel; legacy Synapse continues serving users
     - Databricks computes identical queries in the background (shadow)
     - Lakebridge Reconcile (row-level, schema-level, column-level diffing) validates 99.99%+ data parity
     - Automated checksum validation every ETL cycle
   - **Migration Control Tower Dashboard**:
     - Real-time validation metrics (data match rate, row counts, performance deltas)
     - Automated rollback procedures (point-in-time Delta Lake recovery)
     - Validation gates at three critical checkpoints:
       * **Gate 1**: PoC complete (single domain: Customer Markets)
       * **Gate 2**: Production pilot validated (Energy Markets)
       * **Gate 3**: Full cutover approved (Energy Assets safety-critical systems)
   - **Critical Safety Pattern**: For safety-critical SCADA and telemetry systems (Wave 3), maintain Reverse Shadow Mode where Databricks serves results while legacy Synapse validates in background—ensuring zero tolerance for downtime.

3. **STAGE 3: TARGET STATE (Databricks Data Intelligence Platform)**
   - **Operational Stack**:
     - **Lakeflow Connect**: Managed connectors (SAP S/4HANA, Ignition Gateway), standard connectors (Spot Price APIs, cloud storage)
     - **Delta Live Tables (DLT)**: Serverless, auto-orchestrated medallion pipelines (Bronze → Silver → Gold)
     - **Databricks SQL (DBSQL)**: Modern warehouse with 4× query performance vs. Synapse baseline
     - **Databricks AI**: Real-time ML model serving, GenAI integration via Agent Bricks
   - **Governance Layer**:
     - **Unity Catalog**: Centralized access control, data lineage, audit trails (replaces Synapse RBAC + Purview)
     - **Regulatory Alignment**: Proactive audit integration for NEM/NERL/NERR compliance, Security of Critical Infrastructure Act 2018, State-level electricity/gas acts (VIC, etc.)
   - **Storage & Format**:
     - **Delta Lake** with Iceberg support for multi-cloud transactional workloads
     - Medallion structure maintained (Bronze → Silver → Gold)
     - Multi-cloud ready (AWS + Azure capabilities preserved)
   - **Business Value Metrics**:
     - Query performance: 4× faster vs. Synapse baseline
     - Cost reduction: 30% lower TCO
     - Real-time analytics & ML enablement
     - Reduced governance overhead (Unity Catalog self-service)

---

## **Lakebridge-Driven Workflow (Pre- to Post-Migration)**

### **Pre-Migration Assessment (Lakebridge Analyzer)**
- Profiler scans entire Synapse SQL environment (workloads, complexity, data volumes)
- Complexity scoring per workload (high/medium/low) to prioritize conversion effort
- Effort & cost estimates for each domain (Customer Markets, Energy Markets, Energy Assets)
- Output: Detailed migration roadmap with wave prioritization

### **Conversion (Lakebridge Converter)**
- Automated transpilation of T-SQL → Spark SQL (with configuration-driven BladeBridge engine)
- Synapse Notebook conversion to Databricks Notebooks (magic command remapping)
- Pipeline orchestration rules → Lakeflow Spark Declarative Pipeline definitions
- Output: Databricks-native workload artifacts, ready for deployment

### **Post-Migration Reconciliation (Lakebridge Reconcile)**
- **Row-level diffing**: Hash-based row comparison (exact match mode)
- **Schema-level validation**: Column presence, datatype alignment
- **Column-level diffing**: Supports aggregate mode for incremental validation
- **Automated gates**: Reconciliation pass-rate thresholds trigger promotion to next wave
- Output: Audit trail, mismatch reports, data certification

---

## **Migration Wave Strategy (4 Waves with Hard Gates)**

| Wave | Domain | Criticality | Duration | Key Systems | Gate Criteria |
|------|--------|-------------|----------|-------------|---------------|
| **Wave 1** | Customer Markets | Non-Critical | Weeks 1–3 | Marketing segment tables, Customer 360 views | 99.99% reconciliation match, UAT sign-off |
| **Wave 2** | Energy Markets | Medium | Weeks 4–7 | NEM price feeds, spot market analytics | Performance parity (+/- 10% vs. baseline), business user sign-off |
| **Wave 3** | Energy Assets | Safety-Critical | Weeks 8–12 | SCADA telemetry (Liddell, Tomago, Bayswater), asset health monitoring | Zero data loss validation, safety review board approval |
| **Wave 4** | Decommission | N/A | Week 13+ | Archive Synapse, retire legacy pipelines | All workloads validated on Databricks, cost savings baseline achieved |

---

## **Data Source Integration via Lakeflow (Synapse → Databricks)**

| Data Source | Current Flow | Databricks Flow | Lakeflow Pattern |
|-------------|--------------|-----------------|------------------|
| **SAP S/4HANA** | Synapse via JDBC/ADF | Databricks Lakeflow SAP connector | Managed connector (incremental ingestion) |
| **Ignition Gateway (SCADA)** | Real-time to Synapse tables | Streaming tables via Lakeflow | Standard connector + Structured Streaming (real-time) |
| **Spot Price APIs** | Custom ETL pipeline | Lakeflow custom connector | Standard connector with auto-retry |
| **ADLS Gen2** | Direct mount (Bronze layer) | Auto Loader + Delta Live Tables | Streaming table ingestion with schema evolution |

---

## **Governance & Compliance Framework**

### **Unity Catalog Replaces Synapse RBAC + Purview**
- **Three-level namespace**: `catalog.schema.table` (vs. Synapse's flat object store)
- **Role-based access control (RBAC)**: Fine-grained permissions per table/column
- **Data lineage tracking**: Automatic lineage capture from Lakeflow → DLT → DBSQL
- **Audit logging**: Query history, data access events, compliance exports

### **Regulatory Alignment**
- **Electricity Market Compliance**: NEM, NERL, NERR rules embedded in data classification
- **Critical Infrastructure**: Security of Critical Infrastructure Act 2018 (SOCI) controls via Unity Catalog encryption + audit
- **State-Level Regulation**: Electricity Industry Act 2000 (VIC), Gas Industry Act 2001 (VIC), mapped to data governance policies
- **ESG Reporting**: Continuous data lineage validation for sustainability metrics

---

## **Risk Mitigation & Safety Mechanisms**

| Risk Category | Mitigation Strategy | Tool/Framework |
|---------------|-------------------|-----------------|
| **Data Loss** | Point-in-time Delta Lake recovery (time travel) | Delta Lake ACID semantics |
| **Query Correctness** | Row/schema/column-level reconciliation pre-cutover | Lakebridge Reconcile |
| **Performance Regression** | Baseline comparison + 10% tolerance gate | Migration Control Tower dashboard |
| **Downtime (Safety-Critical)** | Reverse Shadow Mode (Databricks serves, Synapse validates) | Dual-pipeline execution |
| **Regulatory Non-Compliance** | Unity Catalog audit trails + lineage validation | Automated compliance checks |
| **Schema Mismatch** | Automatic schema enforcement + mergeSchema option for evolution | Delta Lake schema enforcement |

---

## **Peer Knowledge Sharing (Industry Alignment)**

Engage existing Databricks customer base in energy/utilities for lessons learned:
- **Alinta Energy**: Migration sequencing for multi-asset portfolios
- **EnergyAustralia**: Real-time telemetry optimization (SCADA streaming tables)
- **Origin Energy**: Safety-critical system cutover procedures
- **Australian Energy Market Operator (AEMO)**: NEM compliance patterns

---

## **Success Metrics (Migration Control Tower)**

| KPI | Target | Measurement |
|-----|--------|-------------|
| Migration Completion | 100% workloads migrated to Databricks | Wave 4 gates closed |
| Data Parity | 99.99% row-match reconciliation | Lakebridge Reconcile audit |
| Performance Improvement | 4× query latency reduction | DBSQL vs. Synapse baseline |
| Cost Reduction | 30% TCO savings | Infrastructure cost delta |
| User Adoption | 95% user acceptance rate | UAT feedback by wave |
| Governance Overhead | 50% reduction in access request time | Unity Catalog vs. Synapse RBAC |

---

## **Timeline & Resourcing**

- **Weeks 1–2**: Lakebridge Analyzer (scope assessment, complexity scoring)
- **Weeks 3–4**: Strategic planning (wave sequencing, resource allocation, regulatory mapping)
- **Weeks 5–7**: Design (Databricks architecture, Lakeflow connector setup, DLT pipeline design)
- **Weeks 8–20**: Parallel operation + migration (Lakebridge Converter, shadow-mode validation, wave rollout)
- **Weeks 21–24**: Optimization (cost tuning, performance profiling, Synapse decommission)

**Resource Model**: Pair AGL engineers with Databricks Professional Services (side-by-side) + Databricks Data & AI Academy training plan (ongoing upskilling).

---

## **Key Technical Differentiators (vs. Lift-and-Shift)**

1. **Lakebridge Automation**: 80% of SQL/ETL conversion automated (vs. manual recoding)
2. **Zero-Downtime Shadow Mode**: Parallel validation without user impact (vs. maintenance windows)
3. **Serverless Medallion Pipelines**: DLT auto-orchestration reduces operational overhead (vs. manual Synapse Pipeline tuning)
4. **Safety-Critical Integration**: Reverse Shadow Mode for SCADA ensures continuous SCADA feed integrity
5. **Unified Governance**: Unity Catalog single source of truth for compliance (vs. Synapse RBAC + Purview fragmentation)

---

## **Visual Architecture (High-Level Schematic)**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ASSESS (Weeks 1–2)  │  PLAN (Weeks 3–4)  │  DESIGN (Weeks 5–7)  │ EXECUTE (8–20)  │ OPTIMIZE (21–24) │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────┐      ┌──────────────────────────────────────┐
│  CURRENT STATE: SYNAPSE              │      │  TRANSITION: PARALLEL OPERATION      │
│  ────────────────────────────────────│      │  ────────────────────────────────────│
│  • Dedicated SQL Pool                │      │  • Lakebridge Analyzer               │
│  • Domain pools (3)                  │      │  • Track A: Data migration (5 steps) │
│  • Synapse Pipelines + Notebooks     │      │  • Track B: App migration (4 steps)  │
│  • SAP / Ignition / APIs             │      │  • Shadow-mode validation            │
│  • ADLS Gen2 Bronze layer            │      │  • Migration Control Tower           │
│  • Performance baseline              │  ──→ │  • Gates 1,2,3 (wave checkpoints)    │
│                                      │      │  • 8–12 week parallel period         │
└──────────────────────────────────────┘      └──────────────────────────────────────┘
                                                           │
                                                           ↓
                                              ┌──────────────────────────────────────┐
                                              │  TARGET STATE: DATABRICKS            │
                                              │  ────────────────────────────────────│
                                              │  • Lakeflow (SAP, Ignition, APIs)    │
                                              │  • Delta Live Tables (DLT)           │
                                              │  • Databricks SQL (DBSQL)            │
                                              │  • Unity Catalog governance          │
                                              │  • 4× perf, 30% cost, ML-enabled     │
                                              │  • Multi-cloud (AWS + Azure)         │
                                              └──────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  WAVE ROADMAP: 1 (Weeks 1–3) | 2 (Weeks 4–7) | 3 (Weeks 8–12) | 4 (Week 13+) │
│  Customer Markets  → Energy Markets → Energy Assets (Safety-Critical) → Retire Synapse  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## **Next Steps for Technical Stakeholders**

1. **Run Lakebridge Analyzer**: Scan Synapse SQL workloads for complexity & effort estimates (execute in next 2 weeks)
2. **Validate Wave 1 Scope**: Finalize Customer Markets domain workload inventory for PoC
3. **Establish Governance Council**: Map Unity Catalog RBAC to current Synapse role matrix + regulatory requirements
4. **Engage Industry Peers**: Schedule knowledge-sharing sessions with Alinta Energy, EnergyAustralia, Origin
5. **Allocate Lakebridge Licenses & Resources**: Professional Services pairing + Databricks Academy enrollment for AGL data teams

---

## **Appendix: Lakebridge Capabilities Summary**

| Phase | Capability | Input | Output | Time Estimate |
|-------|-----------|-------|--------|----------------|
| **Assess** | Analyzer | SQL codebase + metadata | Complexity report, effort estimates, workload profiling | ~9–15 min (3,500+ SQL files) |
| **Convert** | Converter (BladeBridge) | T-SQL scripts, Synapse Pipelines, Notebooks | Databricks Spark SQL, DLT definitions, Notebooks | ~80% automation (manual validation ~20%) |
| **Reconcile** | Reconcile | Source (Synapse) + Target (Databricks) connections | Row-hash diffs, schema comparison, audit logs | Continuous (per pipeline run) |

---

**Document Classification**: Technical Architecture Brief (AGL Energy Stakeholders)  
**Next Review**: Post-Lakebridge Analyzer (Week 2)  
**Version**: 1.0 – January 2026
