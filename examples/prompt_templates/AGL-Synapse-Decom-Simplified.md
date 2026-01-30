# AGL Energy - Synapse Decommission Architecture

## Overview

Create a migration architecture diagram showing AGL's transition from a hybrid Databricks–Synapse architecture to a unified Databricks platform. Key insight: Synapse serves only as a SQL read layer over Databricks-managed Parquet data. This migration eliminates Synapse, redirecting consumers directly to Databricks SQL.

---

## Visual Style

| Element | Value |
|---------|-------|
| Layout | Landscape 16:9, left-to-right flow |
| Background | White (#FFFFFF) |
| AGL Blue | #001CB0 (headers, structure) |
| Databricks Orange | #FF3621 (target state) |
| Synapse Purple | #7B42BC (current state, fading) |
| Success Green | #00A651 (validation, benefits) |
| Warning Orange | #F39C12 (complexity indicators) |

---

## Structure

Three horizontal sections with a phase bar above and risk mitigation below:

```
┌─────────────────────────────────────────────────────────────────────┐
│  ASSESS → PLAN → DESIGN → EXECUTE → OPTIMIZE  (chevron timeline)    │
├───────────────────┬───────────────────┬─────────────────────────────┤
│   CURRENT STATE   │  TRANSITION STATE │        TARGET STATE         │
│   (Synapse layer) │  (parallel run)   │    (Databricks unified)     │
├───────────────────┴───────────────────┴─────────────────────────────┤
│               RISK MITIGATION & SUCCESS METRICS                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Section 1: Current State

**Header:** "CURRENT STATE: Hybrid Architecture"
**Background:** Light grey

**Data Flow (vertical stack):**

1. **Data Sources** - SAP S/4HANA, Ignition Gateway, ADLS Gen2, Spot Price APIs
   ↓ Ingestion
2. **Databricks Platform** - Bronze ingestion → Spark transforms → Parquet to ADLS
   ↓ PolyBase Hydration
3. **Synapse SQL Warehouse** - Read-only layer (no transformation)
   ↓ SQL Queries
4. **Consumers** - Power BI | Applications | Analysts

**Key Callout Box (Warning Orange border):**
> Synapse adds no transformation value—it's a redundant SQL read layer over Databricks-managed data.

**Pain Points (vertical list with ✗ icons):**
- Redundant read layer
- Dual security models
- PolyBase hydration latency
- Synapse licensing overhead

---

## Section 2: Transition State

**Header:** "TRANSITION STATE: Parallel Operation"
**Duration:** 8–12 weeks
**Background:** Grey

### Two Tracks

**Consumer Migration Track:**
1. Power BI Assessment → 2. DBSQL Configuration → 3. Connection Updates → 4. UAT (99.99% parity)

**Technical Validation Track:**
1. SQL Compatibility → 2. Performance Benchmarks → 3. Security Mapping → 4. Parallel Validation

### Migration Accelerators

| Lakebridge | Agent Bricks |
|------------|--------------|
| Auto-converts ~70-80% T-SQL to Databricks SQL | AI-assisted refactoring for complex procedures |
| Schema and data parity reports | Suggests performance optimizations |

### Validation Gates (Green checkmarks)
- Gate 1: PoC Complete (Customer Markets)
- Gate 2: Pilot Validated (Energy Markets)
- Gate 3: Production Cutover (Energy Assets - safety critical)

### Migration Waves
- Wave 1: Customer Markets
- Wave 2: Energy Markets
- Wave 3: Energy Assets (zero downtime required)

---

## Section 3: Target State

**Header:** "TARGET STATE: Unified Databricks Platform"
**Background:** Databricks Orange gradient

**Data Flow:**

1. **Data Sources** → Lakeflow Connect Ingestion
2. **Databricks Platform** (single source of truth)
   - Lakeflow (ETL & Streaming)
   - Databricks AI (Data Science)
   - DBSQL (Warehousing & BI)
   - Lakebase (Transactional)
   - Unity Catalog (Governance bar across bottom)
3. **Consumers** → Direct SQL Access
   - Power BI → DBSQL
   - Applications → DBSQL / Lakebase
   - AI Agents → Agent Bricks

**Benefits Box (Green border):**
- Synapse eliminated (cost savings)
- Single governance via Unity Catalog
- No PolyBase latency
- AI-ready lakehouse

**Metrics:**
- Query performance: 2–4× faster
- TCO: 30–40% reduction
- Platform surface area: ≥50% reduction

---

## Bottom Bar: Risk Mitigation

Five connected boxes:

| Zero Downtime | Data Integrity | Rollback | Security | Change Mgmt |
|---------------|----------------|----------|----------|-------------|
| Parallel run per domain | 99.99% match rate | Documented per wave | Unity Catalog mapping | Training & docs |

---

## Data Flow Arrows

| State | Arrow Style | Label |
|-------|-------------|-------|
| Current: Sources → Databricks | Solid blue | Ingestion |
| Current: Databricks → Synapse | Solid purple | PolyBase hydration |
| Transition | Dotted green | Validation comparisons |
| Transition | Dashed orange | Consumer cutover |
| Target: Sources → Databricks | Solid orange | Lakeflow Connect |
| Target: Databricks → Consumers | Solid orange | Direct SQL access |

---

## Constraints Panel (right side)

- **Safety-Critical:** Energy Assets domain - zero downtime tolerance
- **Regulatory:** ESG/market reporting must continue uninterrupted
- **Multi-Cloud:** AWS (Retail) + Azure (Operations) maintained
- **Performance SLA:** DBSQL must match or exceed Synapse baselines

---

## Output

- Format: PNG or SVG
- Resolution: 1920×1080 minimum
- Aspect: 16:9 landscape
