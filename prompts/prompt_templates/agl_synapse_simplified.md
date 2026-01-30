# AGL Energy: Synapse to Databricks Migration
## Executive Overview Diagram

---

## **Subject Line**
**AGL's Path from Synapse to Databricks: Zero-Downtime Migration in 4 Waves**

---

## **Visual Style**
- Clean, executive-friendly architecture diagram
- Left-to-right timeline (3 sections)
- Minimal text, maximum visual clarity
- Color Palette:
  - **Synapse Purple** (#7B42BC) - Current state
  - **Transition Grey** (#95A5A6) - Migration phase
  - **Databricks Orange** (#FF3621) - Target state
  - **AGL Deep Blue** (#001CB0) - Structural elements
  - **Success Green** (#00A651) - Validation checkpoints

---

## **Layout: Three-Section Timeline**

### **SECTION 1: TODAY (Left Side)**
**Header**: "Current: Azure Synapse Analytics"

**Components** (simple boxes, top to bottom):
- Azure Synapse SQL Pool
- Data Sources → Synapse
  - SAP S/4HANA
  - SCADA (Liddell, Tomago, Bayswater)
  - Energy Market APIs
- ADLS Gen2 Storage (Bronze Layer)
- Power BI Dashboards

**Bottom callout**: "Already using Databricks for raw → parquet processing"

---

### **SECTION 2: TRANSITION (Center - The Bridge)**
**Header**: "8-12 Week Parallel Operation"

**Two Parallel Tracks** (horizontal lanes):

**Track 1: Data Migration**
- Step 1: Lakebridge Assessment
- Step 2: Convert SQL to Databricks
- Step 3: Validate Data (99.99% match)

**Track 2: Application Migration**
- Step 1: Update Pipelines
- Step 2: Reconnect Power BI
- Step 3: User Testing

**Center Element**: "Migration Control Tower"
- Real-time monitoring
- Automated validation
- Rollback capability

**Bottom: 4 Migration Waves** (colored progress bars):
- Wave 1: Customer Markets ✓ (Non-Critical)
- Wave 2: Energy Markets ✓ (Medium)
- Wave 3: Energy Assets → (Safety-Critical SCADA)
- Wave 4: Retire Synapse (Planned)

**Three Vertical Gates** (checkpoints between waves):
- Gate 1: PoC Validated
- Gate 2: Pilot Complete
- Gate 3: Production Approved

---

### **SECTION 3: FUTURE (Right Side)**
**Header**: "Target: Databricks Data Intelligence Platform"

**Components** (simple boxes, top to bottom):
- Lakeflow Connect (Data Ingestion)
  - SAP, SCADA, APIs automatically connected
- Delta Live Tables (Data Pipelines)
  - Bronze → Silver → Gold (same structure)
- Databricks SQL (Analytics)
  - Power BI connected here
- Unity Catalog (Governance)
  - Single access control + audit system

**Performance Callouts** (floating badges):
- 4× Faster Queries
- 30% Lower Cost
- Real-Time ML Ready

**Bottom callout**: "Multi-Cloud Ready (AWS + Azure)"

---

## **Top Header Bar: Timeline**
Simple chevron-style phases:
```
ASSESS (2 weeks) → PLAN (2 weeks) → DESIGN (3 weeks) → EXECUTE (12 weeks) → OPTIMIZE (4 weeks)
```

---

## **Bottom Footer: Key Benefits**
Five icon-based callouts:
1. **Zero Downtime**: Parallel operation = no service interruption
2. **Data Integrity**: Automated validation before cutover
3. **Safety-First**: SCADA systems migrate last with extra validation
4. **Regulatory Compliant**: Unity Catalog meets NEM/NERL requirements
5. **Cost Efficient**: 30% savings + 4× performance

---

## **Visual Flow Arrows (Key Connections Only)**

1. **Synapse → ADLS Gen2** (thick blue arrow)
   - Label: "Existing Bronze Layer"

2. **ADLS Gen2 → Databricks Delta Lake** (thick orange arrow)
   - Label: "Lakeflow Migration"

3. **Parallel validation arrows** (dotted green lines)
   - Between Synapse output and Databricks output
   - Label: "Continuous Validation"

4. **Power BI reconnection** (dashed line)
   - From Synapse to Databricks SQL
   - Label: "Connection Update"

---

## **Right-Side Panel: Migration Waves (Simplified)**

Vertical progress indicator:
```
┌─────────────────────────────┐
│ Wave 1: Customer Markets    │ ████████████ 100%
│ Wave 2: Energy Markets      │ ████████░░░░  70%
│ Wave 3: Energy Assets       │ ███░░░░░░░░░  25%
│ Wave 4: Decommission        │ ░░░░░░░░░░░░   0%
└─────────────────────────────┘
```

---

## **Left-Side Annotation: Core Principles**

Three key points:
- ✓ Leverage existing Databricks investment
- ✓ Zero downtime for safety-critical systems
- ✓ Automated validation via Lakebridge

---

## **Callout Boxes (Minimal)**

**On Transition Section**:
- "Lakebridge automates 80% of migration work"
- "Shadow-mode testing ensures safety"

**On Target Section**:
- "Unity Catalog = single governance layer"
- "Same medallion structure (Bronze→Silver→Gold)"

---

## **Success Metrics Dashboard (Bottom Right)**

Simple scorecard:
```
┌─────────────────────────────────┐
│ Migration Progress      │  65%  │
│ Data Validation Match   │ 99.9% │
│ Apps Migrated          │ 45/67 │
│ Users Trained          │  120  │
└─────────────────────────────────┘
```

---

## **Key Differences from Detailed Version**

| Aspect | Detailed Version | Simplified Version |
|--------|-----------------|-------------------|
| **Components** | 15+ technical elements per section | 4-5 high-level boxes per section |
| **Text Density** | Detailed technical specs | Key terms only |
| **Arrows** | 10+ data flow connections | 4 primary connections |
| **Callouts** | 12+ floating annotations | 6 essential callouts |
| **Wave Detail** | Full table with gate criteria | Simple progress bars |
| **Target Audience** | Technical architects + engineers | C-suite + business stakeholders |
| **Purpose** | Deep technical understanding | Strategic alignment + confidence |

---

## **Visual Emphasis Points**

1. **Left (Synapse)**: Show complexity (multiple systems feeding in)
2. **Center (Transition)**: Show control and safety (Migration Control Tower + waves)
3. **Right (Databricks)**: Show simplicity (unified platform) + performance gains

**Color Progression**: Purple (complex) → Grey (controlled transition) → Orange (modern, performant)

---

## **Optional: Top Executive Summary Box**

If space allows, include a floating summary box:

```
┌──────────────────────────────────────────────────────────────┐
│  AGL SYNAPSE MIGRATION AT A GLANCE                           │
│  ─────────────────────────────────────────────────────────── │
│  Duration: 24 weeks total (12 weeks parallel operation)      │
│  Approach: Zero-downtime shadow-mode migration               │
│  Method: Databricks Lakebridge (automated assessment +       │
│          conversion + validation)                            │
│  Outcome: 4× faster queries, 30% cost reduction, ML-ready    │
└──────────────────────────────────────────────────────────────┘
```

---

## **Annotation Style Guide**

- **Headers**: Bold, 18pt, AGL Deep Blue
- **Component boxes**: Rounded corners, subtle shadow, 14pt labels
- **Arrows**: Solid for data flow, dashed for control flow, dotted for validation
- **Callouts**: Small floating badges with icon + 2-4 word description
- **Progress bars**: Gradient fill (light to dark based on completion)
- **Gates**: Vertical colored lines with checkpoint labels

---

## **Exclusions from Detailed Version**

Remove these elements for simplicity:
- Detailed Lakebridge workflow steps (Analyzer/Converter/Reconcile specifics)
- Row/schema/column-level reconciliation details
- Specific regulatory law citations (NEM/NERL/NERR details)
- Synapse Pipeline → Lakeflow technical conversion steps
- Ignition Gateway technical integration details
- Unity Catalog three-level namespace explanation
- Detailed KPI metrics table
- Peer company engagement specifics
- Week-by-week timeline breakdown
- Resource allocation model

Keep focus on:
- High-level journey (where we are → transition → where we're going)
- Wave structure (4 waves with visual progress)
- Key value props (4× performance, 30% cost, zero downtime)
- Core safety message (SCADA handled carefully in Wave 3)
- Single governance layer (Unity Catalog replaces multiple tools)

---

## **Use Case**

**When to use this simplified version**:
- Executive steering committee updates
- Board-level presentations
- Customer success story decks
- Quick-reference poster for war room
- Non-technical stakeholder alignment

**When to use detailed version**:
- Technical architecture review
- Implementation planning sessions
- Lakebridge Analyzer follow-up workshops
- Professional Services scoping
- Wave execution playbooks

---

**Document Classification**: Executive Visual Specification  
**Companion Document**: agl_synapse_prompt_pro.md (detailed version)  
**Version**: 1.0 Simplified – January 2026
