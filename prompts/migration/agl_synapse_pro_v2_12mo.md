# AGL Energy: Synapse to Databricks Migration
## 12-Month Enterprise Transformation

---

## **Executive Summary**
**Zero-Downtime Synapse Migration via Databricks Lakebridge: A 12-Month Phased Enterprise Transformation**

AGL's existing Databricks Bronze layer foundation enables a comprehensive 12-month migration from Azure Synapse to the Databricks Data Intelligence Platform. This architecture employs a **governance-first approach** with Unity Catalog deployed in Phase 1, followed by metadata-driven ingestion frameworks, Lakebridge-powered migration execution, and ultimately AI at scale integration. The approach delivers zero-downtime migration of safety-critical SCADA, telemetry, and financial workloads while establishing an AI Center of Excellence and achieving 100% Synapse decommission.

---

## **12-Month Migration Architecture**

### **Timeline Overview: 9 Integrated Phases**

The migration follows a structured 12-month model divided into 9 phases, with governance and platform foundations established before migration execution begins.

```
Month 1-2  | Month 3-4   | Month 5-6      | Month 7-9        | Month 10    | Month 11     | Month 12
Foundation | Platform    | Migration      | Migration        | Enablement  | Enterprise   | AI Scale +
Governance | Data        | Planning       | Execution        | at Scale    | Handover     | Complete
           | Products    |                |                  |             |              | Migration
```

---

## **Phase-by-Phase Architecture**

### **PHASE 1: Foundation & Governance (Months 1-2)**

**Objective**: Establish production-ready Databricks lakehouse with enterprise governance

**Key Deliverables**:
- Databricks lakehouse architecture design with AGL sign-off
- Unity Catalog deployment across all workspaces
- Line of Business (LOB) governance structure with clear roles and responsibilities
- Three-level namespace design (`catalog.schema.table`)
- Initial RBAC model mapped from Synapse + Purview

**Architecture Components**:
- **Unity Catalog Metastore**: Regional metastore creation in Azure Australia East
- **Catalog Structure**: 
  - `agl_customer_markets` (Customer domain)
  - `agl_energy_markets` (Trading & NEM data)
  - `agl_energy_assets` (SCADA, telemetry, asset health)
  - `agl_integration` (Cross-domain projects)
  - `agl_users` (Individual user workspaces)
- **Governance Framework**: Role definitions, access request workflows, audit integration
- **Regulatory Mapping**: NEM, NERL, NERR, SOCI Act 2018, State regulations (VIC Electricity/Gas Acts)

**Success Criteria**: Unity Catalog operational, LOB governance approved, baseline security posture established

---

### **PHASE 2: Platform & Data Products (Months 2-4)**

**Objective**: Deploy production-grade platform with monitoring and metadata-driven ingestion

**Key Deliverables**:
- Production Databricks Data Intelligence Platform deployment
- Unity Catalog access control implementation (fine-grained RBAC)
- Monitoring and cost observability frameworks (Databricks System Tables + Azure Monitor)
- **Metadata-driven ingestion framework** for automated, consistent data onboarding

**Metadata-Driven Ingestion Framework**:
- **Control Table Architecture**: Centralized metadata repository for source-to-target mappings
  - Source system details (SAP, Ignition Gateway, APIs, ADLS Gen2)
  - Ingestion frequency (real-time streaming, micro-batch, daily batch)
  - Schema evolution rules (mergeSchema, enforceSchema)
  - Data quality checks (row counts, null checks, duplicate detection)
- **Automated Lakeflow Pipelines**: Template-based ingestion using metadata
  - Managed connectors for SAP S/4HANA (incremental CDC)
  - Standard connectors for SCADA via Ignition Gateway (streaming tables)
  - Auto Loader for ADLS Gen2 Bronze layer files
  - API connectors for Spot Price feeds with retry logic
- **Medallion Architecture Blueprint**: Bronze → Silver → Gold with Delta Live Tables (DLT)
  - Bronze: Raw ingestion with schema-on-read
  - Silver: Cleansed, joined, validated datasets
  - Gold: Business-ready aggregates for reporting and analytics

**Observability Components**:
- Cost tracking via Databricks System Tables (`system.billing.usage`)
- Query performance monitoring (query history, execution plans)
- Data quality metrics dashboard (validation pass rates, SLA adherence)
- Lineage visualization (Unity Catalog automatic lineage)

**Success Criteria**: Metadata framework operational, cost observability live, LOB teams onboarded to Unity Catalog

---

### **PHASE 3: Migration Planning (Months 4-6)**

**Objective**: Complete comprehensive Synapse assessment and develop phased migration roadmap

**Key Deliverables**:
- Comprehensive Synapse environment assessment
- **LakeBridge Profiler & Analyser** deployment and execution
- Phased migration plan with wave sequencing
- Medallion architecture blueprint (alignment with existing Bronze layer)
- Risk mitigation strategy

**LakeBridge Assessment Workflow**:
1. **Profiling Phase**:
   - Scan all Synapse Dedicated SQL Pools (Customer Markets, Energy Markets, Energy Assets)
   - Extract T-SQL stored procedures, views, pipelines, notebooks
   - Log analysis (query history, performance baselines, user access patterns)
   - Complexity scoring (high/medium/low conversion effort)
2. **Analysis Phase**:
   - Identify SQL dialect compatibility issues (T-SQL → Spark SQL)
   - Map Synapse Pipelines → Lakeflow/Workflows
   - Assess Synapse Notebooks → Databricks Notebooks conversion
   - Estimate effort per workload (person-days, complexity rating)
3. **Migration Strategy Development**:
   - Wave prioritization (non-critical → medium → safety-critical)
   - Federation requirements (identify systems requiring live access during migration)
   - Data reconciliation plan (schema, row-level, column-level validation)

**Wave Sequencing Plan**:
- **Wave 1**: Customer Markets (non-critical marketing segments, Customer 360 views)
- **Wave 2**: Energy Markets (NEM price feeds, spot market analytics, trading data)
- **Wave 3**: Energy Assets (safety-critical SCADA telemetry, asset health monitoring)
- **Wave 4**: Decommission Synapse (archive, retire legacy pipelines)

**Success Criteria**: LakeBridge Analyzer report complete, wave plan approved by technical steering committee

---

### **PHASE 4: Enablement (Early) (Months 5-6)**

**Objective**: Map personas and design targeted enablement for early adoption

**Key Deliverables**:
- Persona mapping (data engineers, data scientists, BI analysts, business users)
- Targeted enablement plan per persona
- Early engagement sessions (lunch-and-learns, office hours)
- Capability uplift roadmap

**Persona-Based Enablement**:
| Persona | Key Skills to Build | Training Format | Success Metric |
|---------|-------------------|-----------------|----------------|
| Data Engineers | Delta Live Tables, Lakeflow, Unity Catalog | Hands-on workshops (3 days) | Build 1 DLT pipeline independently |
| Data Scientists | Databricks ML, Feature Store, MLflow | Lab-based training (2 days) | Deploy 1 model to production |
| BI Analysts | Databricks SQL, Power BI integration | Self-paced + office hours | Create 3 dashboards in DBSQL |
| Business Users | Unity Catalog data discovery, SQL basics | Video tutorials + Q&A | Run basic queries independently |

**Success Criteria**: 30% of target users (30/100) trained, early adopters identified

---

### **PHASE 5: Migration Execution (Months 7-9)**

**Objective**: Migrate Synapse workloads using LakeBridge and enable federation for live access

**Key Deliverables**:
- Wave 1-3 migration completion
- Federation layer for live access to remaining Synapse systems
- Data reconciliation validation (99.99%+ match rate)
- UAT sign-off per wave

**Migration Execution Sub-Phases**:

#### **5.1 Profiling & Code Analysis (Months 7)**
- Collection and analysis of Synapse query logs
- Extraction and analysis of T-SQL code, stored procedures, pipelines
- Development of migration strategy per wave
- **Output**: Detailed code inventory, conversion roadmap

#### **5.2 Code Conversion (Months 7-8)**
- **LakeBridge Converter** (automated transpilation):
  - T-SQL → Spark SQL (DDL, DML, stored procedures)
  - Synapse Pipelines → Databricks Lakeflow Spark Declarative Pipelines
  - Synapse Notebooks → Databricks Notebooks (magic command remapping)
- **Gen-AI Tools** for complex conversion:
  - Code explanation and optimization suggestions
  - Documentation generation for converted workflows
  - Edge case handling (vendor-specific SQL features)
- **Detailed Documentation**: Conversion logs, before/after comparison, technical debt notes

**Conversion Coverage**:
- Target: 80% automated via LakeBridge Converter
- Manual effort: 20% for complex business logic, custom UDFs, vendor-specific features

#### **5.3 Validation (Months 8-9)**
- **Code Syntax Testing**: Spark SQL syntax validation, notebook execution tests
- **Code Validation**: Logic correctness, business rule preservation
- **Data Validation** (LakeBridge Reconcile):
  - **Schema-level**: Column presence, datatype alignment, constraint validation
  - **Row-level**: Hash-based row comparison (exact match mode)
  - **Column-level**: Aggregate mode for incremental validation (sum, count, min/max)
- **Environment Promotion**: Development → UAT → Production
- **UAT Cycle**: Business users validate outputs against Synapse baseline

**Validation Gates**:
| Wave | Gate Criteria | Approval Authority |
|------|--------------|-------------------|
| Wave 1 | 99.99% reconciliation match + UAT sign-off | Customer Markets LOB Lead |
| Wave 2 | Performance parity (±10% vs. Synapse) + business sign-off | Energy Markets LOB Lead |
| Wave 3 | Zero data loss validation + safety review | Safety Review Board + Energy Assets LOB Lead |

#### **5.4 Deployment (Months 9)**
- **UAT Cycle**: Key business users validate migrated workloads in UAT environment
- **Production Deployment**: Phased cutover per wave
  - Blue-green deployment pattern (instant cutover capability)
  - Reverse shadow mode for Wave 3 (Databricks serves, Synapse validates)
- **Post-Deployment Monitoring**: 
  - Real-time performance tracking (query latency, job success rates)
  - Data quality monitoring (automated checksums per ETL cycle)
  - User feedback collection (issue tracking, support tickets)
- **Rollback Procedures**: Delta Lake time travel (point-in-time recovery)

**Federation Layer**:
- **Purpose**: Enable live access to remaining Synapse systems during migration
- **Technology**: Databricks Lakehouse Federation (query federation via JDBC)
- **Use Cases**:
  - Cross-query Synapse and Databricks tables during Wave 2-3 transition
  - Provide business continuity for unmigrated workloads
  - Support parallel operation validation (shadow mode queries)
- **Federated Connections**:
  - Synapse Dedicated SQL Pool (read-only foreign catalog)
  - SQL Server operational databases (live transactional data)
  - Third-party APIs (Spot Price feeds during migration window)

**Success Criteria**: Wave 1-3 migrated and validated, federation layer operational, Wave 4 decommission plan finalized

---

### **PHASE 6: Enablement at Scale (Month 10)**

**Objective**: Train 100 users across engineering, science, and analytics roles

**Key Deliverables**:
- 100 users trained (70 engineers/scientists, 30 analysts/business users)
- Foundational skills certification (Databricks Academy)
- Self-service enablement materials (documentation, video library, FAQ)
- Internal champions network (10 power users)

**Training Program**:
- **Data Engineers**: Advanced Delta Live Tables, Unity Catalog administration, performance tuning
- **Data Scientists**: MLflow, Databricks ML, AutoML, Feature Store
- **BI Analysts**: Databricks SQL, dashboard building, Power BI integration
- **Business Users**: Data discovery, basic SQL, Unity Catalog search

**Success Criteria**: 100 users certified, 90%+ satisfaction rating, self-service adoption >50%

---

### **PHASE 7: Enterprise-Grade Platform & Handover (Month 11)**

**Objective**: Transition operating procedures to AGL teams and establish AI CoE

**Key Deliverables**:
- Operating procedures documentation (runbooks, incident response, escalation paths)
- **AI Center of Excellence (CoE)** establishment:
  - Governance model (AI use case prioritization, ethical AI guidelines)
  - MLOps framework (model lifecycle management, monitoring, retraining)
  - Innovation pipeline (quarterly AI pilot projects)
- Enterprise-grade platform validation:
  - Governance: Unity Catalog audit trails, lineage validation, compliance certification
  - Security: Encryption at rest/in transit, network isolation, identity federation
  - Observability: Cost management dashboards, performance SLAs, data quality KPIs
- Knowledge transfer sessions (shadow AGL teams for 2 weeks)

**AI CoE Structure**:
| Role | Responsibility | Headcount |
|------|---------------|-----------|
| AI CoE Lead | Strategy, prioritization, stakeholder alignment | 1 |
| MLOps Engineers | Model deployment, monitoring, infrastructure | 2 |
| Data Scientists | Model development, experimentation, feature engineering | 3 |
| Business Translators | Use case identification, requirements gathering | 2 |

**Success Criteria**: AGL teams operating platform independently, AI CoE launched, enterprise validation complete

---

### **PHASE 8: AI at Scale (Month 12)**

**Objective**: Operate AI use cases in production and embed AI into core business processes

**Key Deliverables**:
- 3-5 AI use cases in production (e.g., demand forecasting, predictive maintenance, customer churn)
- Automated decision-making agents (GenAI-powered chatbots, recommendation engines)
- AI integration into core processes (customer service, energy trading, asset management)
- Real-time ML model serving (Databricks Model Serving)

**AI Use Case Examples**:
1. **Demand Forecasting**: Predict energy demand by region using historical consumption + weather data
2. **Predictive Maintenance**: SCADA telemetry → anomaly detection → maintenance scheduling
3. **Customer Churn Prediction**: Customer 360 data → churn probability → retention campaigns
4. **Spot Price Optimization**: NEM price feeds → trading strategy recommendations
5. **GenAI Customer Support**: Agent Bricks-powered chatbot for billing inquiries

**Success Criteria**: 3+ AI use cases live, measurable business impact (cost savings, revenue lift, efficiency gains)

---

### **PHASE 9: Complete Migration & Simplification (Month 12)**

**Objective**: Achieve 100% Synapse migration, simplify data estate, realize TCO reduction

**Key Deliverables**:
- 100% Synapse workloads migrated to Databricks
- Synapse Dedicated SQL Pools decommissioned
- Data estate simplified (single lakehouse platform vs. fragmented Synapse + Databricks)
- TCO reduction achieved (30% infrastructure cost savings)
- Final migration report (lessons learned, metrics, recommendations)

**Decommissioning Plan**:
- Archive Synapse historical data (cold storage in ADLS Gen2)
- Retire Synapse Pipelines (replace with Lakeflow/Workflows)
- Migrate Power BI connections to Databricks SQL
- Sunset Synapse licensing (cost savings realized)

**Success Criteria**: Synapse fully decommissioned, TCO target achieved, migration complete

---

## **Detailed Technology Stack**

### **Data Ingestion Layer**
| Component | Technology | Use Case |
|-----------|-----------|----------|
| SAP S/4HANA | Lakeflow Managed Connector | Incremental CDC ingestion (financial, operational data) |
| Ignition Gateway (SCADA) | Lakeflow Standard Connector + Streaming Tables | Real-time telemetry (Liddell, Tomago, Bayswater SCADA) |
| Spot Price APIs | Lakeflow Custom Connector | NEM spot price feeds with retry logic |
| ADLS Gen2 Bronze | Auto Loader + Delta Live Tables | Existing Bronze layer files (Parquet, CSV, JSON) |
| Metadata Control Table | Delta table in Unity Catalog | Source-to-target mappings, ingestion frequency, schema rules |

### **Data Transformation Layer**
| Component | Technology | Use Case |
|-----------|-----------|----------|
| Medallion Architecture | Delta Live Tables (DLT) | Bronze → Silver → Gold pipelines (serverless, auto-orchestrated) |
| Schema Enforcement | Delta Lake | ACID semantics, schema validation, time travel |
| Change Data Capture | Lakeflow + DLT `APPLY CHANGES INTO` | Incremental updates from SAP, operational DBs |
| Data Quality | DLT expectations | Automated validation (null checks, duplicate detection, SLA monitoring) |

### **Data Serving Layer**
| Component | Technology | Use Case |
|-----------|-----------|----------|
| Analytics Warehouse | Databricks SQL (DBSQL) | Power BI dashboards, ad-hoc queries, reporting |
| Real-Time ML | Databricks Model Serving | Low-latency model inference (demand forecasting, churn prediction) |
| GenAI Applications | Databricks AI (Agent Bricks) | Customer support chatbots, document summarization |
| Federation | Lakehouse Federation (Query Federation) | Live queries to Synapse during migration (Waves 2-3) |

### **Governance & Security**
| Component | Technology | Use Case |
|-----------|-----------|----------|
| Unified Catalog | Unity Catalog | Centralized metadata, RBAC, audit logs, lineage tracking |
| Fine-Grained Access | Row filters + column masking | Sensitive data protection (PII, financial data) |
| Audit & Compliance | Unity Catalog audit logs + System Tables | NEM/NERL/NERR compliance, SOCI Act adherence, GDPR |
| Data Lineage | Unity Catalog automatic lineage | Impact analysis, regulatory reporting, troubleshooting |

---

## **Migration Control Tower Dashboard**

### **Real-Time KPIs (Tracked Throughout Phases 5-9)**

| KPI | Target | Measurement Method | Current Status (Example) |
|-----|--------|-------------------|--------------------------|
| Migration Completion | 100% workloads | Wave progress tracker | Wave 1: ✓, Wave 2: 70%, Wave 3: 25%, Wave 4: 0% |
| Data Parity | 99.99% match rate | LakeBridge Reconcile (row-hash comparison) | 99.97% (within tolerance) |
| Query Performance | 4× faster vs. Synapse | DBSQL query history vs. Synapse baseline | 3.8× (on track) |
| Cost Reduction | 30% TCO | Infrastructure cost delta (Synapse vs. Databricks) | 22% (projected to hit 30% by Month 12) |
| User Adoption | 95% acceptance | UAT feedback per wave | Wave 1: 97%, Wave 2: 93% |
| Training Completion | 100 users certified | Databricks Academy completion tracking | 85/100 (85%) |
| Governance Overhead | 50% reduction | Access request time (Unity Catalog vs. Synapse RBAC) | 42% reduction |
| AI Use Cases Live | 3+ in production | MLflow deployment tracking | 2 live, 3 in UAT |

---

## **Risk Mitigation Strategy**

| Risk Category | Mitigation Strategy | Technology/Process |
|---------------|--------------------|--------------------|
| **Data Loss** | Point-in-time recovery (7-day retention) | Delta Lake time travel |
| **Query Correctness** | Automated reconciliation pre-cutover | LakeBridge Reconcile (schema, row, column validation) |
| **Performance Regression** | Baseline comparison + 10% tolerance gate | Migration Control Tower performance tracking |
| **Downtime (Safety-Critical)** | Reverse shadow mode (Databricks serves, Synapse validates) | Wave 3 dual-pipeline execution pattern |
| **Regulatory Non-Compliance** | Continuous audit trails + lineage validation | Unity Catalog audit logs + compliance dashboards |
| **Schema Drift** | Automatic schema enforcement + evolution rules | Delta Lake `enforceSchema` + `mergeSchema` options |
| **Cost Overrun** | Real-time cost monitoring + budget alerts | Databricks System Tables + Azure Cost Management |
| **User Resistance** | Early engagement + persona-based training | Phase 4 + Phase 6 enablement programs |
| **Federation Performance** | Query pushdown optimization + caching | Lakehouse Federation performance tuning |

---

## **Peer Benchmarking & Knowledge Sharing**

Engage existing Databricks customers in energy/utilities for lessons learned and best practices:

| Peer Company | Focus Area | Key Takeaway |
|--------------|-----------|--------------|
| **Alinta Energy** | Migration sequencing for multi-asset portfolios | Wave-based approach reduces risk, prioritize non-critical first |
| **EnergyAustralia** | Real-time telemetry optimization (SCADA) | Streaming tables + DLT for low-latency SCADA ingestion |
| **Origin Energy** | Safety-critical system cutover procedures | Reverse shadow mode + extensive UAT for zero-downtime |
| **AEMO** | NEM compliance patterns | Unity Catalog lineage tracking simplifies regulatory reporting |

**Engagement Plan**: Quarterly peer-to-peer sessions (virtual roundtables, site visits, case study sharing)

---

## **Success Metrics by Phase**

| Phase | Success Metric | Target | Actual (Example) |
|-------|---------------|--------|------------------|
| 1: Foundation | Unity Catalog operational | Month 2 | ✓ Month 2 |
| 2: Platform | Metadata framework live | Month 4 | ✓ Month 4 |
| 3: Planning | LakeBridge Analyzer complete | Month 6 | ✓ Month 6 |
| 4: Enablement (Early) | 30 users trained | Month 6 | 32 users (107%) |
| 5: Migration Execution | Wave 1-3 migrated | Month 9 | Wave 1-2 complete, Wave 3 in progress |
| 6: Enablement (Scale) | 100 users certified | Month 10 | 85 users (85%, on track) |
| 7: Enterprise Handover | AI CoE launched | Month 11 | On track |
| 8: AI at Scale | 3 AI use cases live | Month 12 | 2 live, 3 in UAT |
| 9: Complete Migration | 100% Synapse migrated | Month 12 | 75% (Wave 4 in progress) |

---

## **Timeline Visualization**

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                         AGL 12-MONTH MIGRATION TIMELINE                              │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                       │
│  Month 1-2          Month 3-4          Month 5-6           Month 7-9                 │
│  ┌─────────┐       ┌─────────┐       ┌─────────┐         ┌─────────┐               │
│  │Foundation│  ───> │Platform │  ───> │Migration│   ───>  │Migration│               │
│  │Governance│       │  Data   │       │Planning │         │Execution│               │
│  └─────────┘       │Products │       └─────────┘         │ (Waves) │               │
│                    └─────────┘                           └─────────┘               │
│                                      ┌─────────┐                                     │
│                                      │Enable-  │                                     │
│                                      │ment(1)  │                                     │
│                                      └─────────┘                                     │
│                                                                                       │
│  Month 10           Month 11          Month 12                                       │
│  ┌─────────┐       ┌─────────┐       ┌─────────────┐                               │
│  │Enable-  │  ───> │Enterprise│  ───> │AI Scale +   │                               │
│  │ment(100)│       │Handover │       │Complete     │                               │
│  └─────────┘       │AI CoE   │       │Migration    │                               │
│                    └─────────┘       └─────────────┘                               │
│                                                                                       │
└─────────────────────────────────────────────────────────────────────────────────────┘

Wave Rollout (Months 7-12):
├── Wave 1: Customer Markets (Month 7-8) ────────────────────── ✓ Complete
├── Wave 2: Energy Markets (Month 8-9) ──────────────────────── ✓ Complete  
├── Wave 3: Energy Assets (Month 9-11) ──────────────────────── → In Progress
└── Wave 4: Decommission Synapse (Month 12) ─────────────────── ○ Planned
```

---

## **Key Differentiators (vs. Lift-and-Shift)**

1. **Governance-First Approach**: Unity Catalog deployed before migration (not after)
2. **Metadata-Driven Automation**: Reusable ingestion framework reduces manual configuration
3. **LakeBridge Acceleration**: 80% automated SQL/ETL conversion (vs. manual recoding)
4. **Federation for Business Continuity**: Live access to Synapse during migration (zero disruption)
5. **Gen-AI for Code Conversion**: Accelerates complex logic migration + auto-documentation
6. **AI CoE as Outcome**: Migration unlocks AI capabilities, not just data warehouse replacement
7. **Reverse Shadow Mode**: Safety-critical SCADA systems (Wave 3) run on Databricks while Synapse validates
8. **100-User Enablement**: Capability uplift ensures self-sufficiency post-migration

---

## **Next Steps for AGL Technical Stakeholders**

1. **Validate Phase 1 Deliverables**: Review Unity Catalog design (catalog structure, RBAC model, regulatory mapping)
2. **Kick Off Phase 2**: Deploy metadata-driven ingestion framework control table
3. **Schedule LakeBridge Analyzer**: Execute profiling in non-production Synapse environment (Phase 3 entry)
4. **Finalize Wave Sequencing**: Confirm Customer Markets → Energy Markets → Energy Assets prioritization
5. **Establish Migration Control Tower**: Set up real-time KPI dashboard (data parity, performance, cost)
6. **Engage Peer Network**: Schedule knowledge-sharing sessions with Alinta Energy, EnergyAustralia, Origin
7. **Allocate Resources**: Confirm Databricks Professional Services pairing + internal team availability

---

**Document Classification**: Technical Architecture Brief (12-Month Migration)  
**Version**: 2.0 – January 2026  
**Next Review**: Post-Phase 1 (Month 2 governance sign-off)
