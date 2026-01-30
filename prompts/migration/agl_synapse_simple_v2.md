# AGL Energy: Synapse to Databricks Migration
## 12-Month Journey

---

## **Executive Summary**
**AGL's Path from Synapse to Databricks: 12-Month Zero-Downtime Enterprise Transformation**

---

## **Visual Style**
- Clean, executive-friendly architecture diagram
- Left-to-right timeline showing 12-month journey
- Minimal text, maximum visual clarity
- Color Palette:
  - **Synapse Purple** (#7B42BC) - Current state
  - **Transition Grey** (#95A5A6) - Migration phase
  - **Databricks Orange** (#FF3621) - Target state
  - **AGL Deep Blue** (#001CB0) - Governance & structure
  - **Success Green** (#00A651) - Validation checkpoints

---

## **12-Month Timeline Header Bar**

Simple chevron-style phases spanning the entire diagram top:

```
Foundation     Platform     Migration     Migration     Enablement     Enterprise     AI Scale
Governance  →  Data      →  Planning   →  Execution  →  at Scale   →  Handover   →  Complete
(Month 1-2)    (Month 3-4)  (Month 5-6)   (Month 7-9)   (Month 10)     (Month 11)     (Month 12)
```

---

## **Main Layout: Three-Section Timeline (Current → Transition → Future)**

### **SECTION 1: TODAY (Left Side)**
**Header**: "Current: Azure Synapse Analytics"

**Components** (simple boxes, vertical stack):
1. **Azure Synapse SQL Pool**
   - Customer Markets
   - Energy Markets  
   - Energy Assets

2. **Data Sources** (arrow feeding into Synapse)
   - SAP S/4HANA
   - Spot Price APIs
   - ADLS Gen2 Bronze Layer
   - Ignition Gateway (SCADA)

3. **Power BI Dashboards**

**Bottom callout**: "Already using Databricks for Bronze layer processing"

---

### **SECTION 2: TRANSITION (Center - The 12-Month Journey)**
**Header**: "12-Month Migration Journey"

**Three Horizontal Swim Lanes** (color-coded by phase):

#### **Lane 1: Foundation (Months 1-4)** [Deep Blue]
- **Month 1-2**: Unity Catalog Deployment (Governance First)
- **Month 3-4**: Metadata-Driven Ingestion Framework

#### **Lane 2: Migration (Months 5-9)** [Transition Grey]
- **Month 5-6**: LakeBridge Assessment & Planning
- **Month 7-9**: Migration Execution (4 Waves)
  - Wave 1: Customer Markets ✓
  - Wave 2: Energy Markets ✓
  - Wave 3: Energy Assets → (SCADA - Safety-Critical)
  - Wave 4: Decommission Synapse (Planned)

#### **Lane 3: AI & Scale (Months 10-12)** [Databricks Orange]
- **Month 10**: Train 100 Users
- **Month 11**: AI Center of Excellence Launch
- **Month 12**: AI at Scale + Complete Migration

**Center Element**: "Migration Control Tower"
- Real-time data validation
- Performance monitoring
- Cost tracking
- Rollback capability

**Key Pattern Callout** (floating badge):
- "Zero-Downtime: Federation enables live access during migration"

---

### **SECTION 3: FUTURE (Right Side)**
**Header**: "Target: Databricks Data Intelligence Platform"

**Components** (simple boxes, vertical stack):
1. **Unity Catalog** (Governance Layer)
   - Single access control
   - Automated audit trails
   - Data lineage tracking

2. **Lakeflow Connect** (Data Ingestion)
   - SAP, SCADA, APIs auto-connected
   - Metadata-driven pipelines

3. **Spark Declarative Pipelines** (Data Pipelines)
   - Bronze → Silver → Gold
   - Same medallion structure

4. **Databricks SQL** (Analytics)
   - Power BI connected
   - 4× faster queries

5. **AI Center of Excellence** (NEW)
   - Demand forecasting
   - Predictive maintenance
   - Customer insights

**Performance Badges** (floating):
- 4× Query Speed
- 43% Cost Savings
- AI-Powered Decisions

**Bottom callout**: "Multi-Cloud Ready (AWS + Azure) + AI at Scale"

---

## **Wave Progress Indicator (Right-Side Vertical Panel)**

Clean progress bars showing migration waves:

```
┌───────────────────────────────────┐
│ Migration Waves Progress          │
├───────────────────────────────────┤
│ Wave 1: Enery Markets          │
│ ████████████████████ 100%        │
│                                   │
│ Wave 2: Customer Markets            │
│ ████████████████████ 100%        │
│                                   │
│ Wave 3: Energy Assets (SCADA)     │
│ ████████░░░░░░░░░░░░  40%        │
│                                   │
│ Wave 4: Decommission Synapse      │
│ ░░░░░░░░░░░░░░░░░░░░   0%        │
└───────────────────────────────────┘
```

---

## **Key Data Flows (Simplified Arrows)**

1. **Synapse → ADLS Gen2** (thick blue arrow)
   - Label: "Existing Bronze Layer"

2. **ADLS Gen2 → Databricks** (thick orange arrow)
   - Label: "Metadata-Driven Ingestion"

3. **Parallel validation** (dotted green line)
   - Between Synapse and Databricks
   - Label: "Continuous Validation (99.99% match)"

4. **Power BI reconnection** (dashed line)
   - From Synapse to Databricks SQL
   - Label: "Connection Update (Wave 4)"

5. **Federation layer** (bidirectional dotted grey arrow)
   - Between Synapse and Databricks during Months 7-9
   - Label: "Live Access via Federation"

---

## **Bottom Footer: Key Benefits (Icon-Based)**

Five simple benefit badges:

1. **Zero Downtime** 
   - Icon: ✓ checkmark
   - "Federation ensures business continuity"

2. **Governance First**
   - Icon: 🛡️ shield
   - "Unity Catalog from Month 1"

3. **Safety-Critical Ready**
   - Icon: ⚠️ warning
   - "SCADA migrated with extra validation (Wave 3)"

4. **AI-Powered**
   - Icon: 🤖 robot
   - "AI CoE + 3 use cases in production"

5. **Cost Efficient**
   - Icon: 💰 money
   - "30% savings + 4× performance"

---

## **Success Metrics Scorecard (Bottom Right)**

Simple dashboard showing current status:

```
┌─────────────────────────────────┐
│ Migration Status (Month 9)      │
├─────────────────────────────────┤
│ Overall Progress      │   75%   │
│ Data Validation Match │ 99.97%  │
│ Waves Completed       │  2/4    │
│ Users Trained         │  85/100 │
│ Cost Reduction        │   22%   │
│ AI Use Cases Live     │   2/5   │
└─────────────────────────────────┘
```

---

## **Callout Boxes (Minimal - Only 4 Essential)**

**On Foundation Phase (Month 1-4)**:
- "Unity Catalog governance deployed BEFORE migration starts"

**On Migration Phase (Month 7-9)**:
- "LakeBridge automates 80% of SQL conversion work"
- "Federation enables live access to Synapse during migration"

**On Target State**:
- "AI Center of Excellence unlocks predictive analytics + GenAI"

---

## **Key Milestones (Timeline Markers)**

Vertical milestone markers at key months:

- **Month 2**: Unity Catalog Live ✓
- **Month 4**: Metadata Framework Deployed ✓
- **Month 6**: LakeBridge Assessment Complete ✓
- **Month 8**: Wave 1-2 Migrated ✓
- **Month 10**: 100 Users Trained (target)
- **Month 11**: AI CoE Launched (target)
- **Month 12**: 100% Synapse Migration (target)

---

## **Optional: Executive Summary Box (Top Center)**

If space allows, include floating summary:

```
┌────────────────────────────────────────────────────────────────┐
│  AGL SYNAPSE MIGRATION: 12-MONTH TRANSFORMATION                │
│  ────────────────────────────────────────────────────────────  │
│  Duration: 12 months (9 phases)                                │
│  Approach: Governance-first, zero-downtime federation          │
│  Method: LakeBridge (automated) + metadata-driven framework    │
│  Outcome: 4× performance, 30% cost savings, AI at scale        │
│  Training: 100 users across engineering, science, analytics    │
└────────────────────────────────────────────────────────────────┘
```

---

## **What's Different from 6-Month Version**

| Aspect | 6-Month Version | 12-Month Version |
|--------|----------------|------------------|
| **Timeline** | 8-12 week parallel operation | 12-month phased transformation |
| **Governance** | Mentioned in transition | Deployed FIRST (Months 1-2) |
| **Metadata Framework** | Brief mention | Dedicated phase (Months 3-4) |
| **Migration Waves** | 4 waves in 12 weeks | 4 waves spread across Months 7-12 |
| **Training** | Side-by-side pairing | 100 users formally certified (Month 10) |
| **AI Focus** | "ML-enabled" callout | AI CoE + AI at Scale (Months 11-12) |
| **Federation** | Not emphasized | Central to business continuity (Months 7-9) |
| **Decommission** | Wave 4 brief | Final phase (Month 12) with TCO validation |

---

## **Visual Emphasis**

1. **Left (Synapse)**: Show current complexity (multiple data sources, domain-specific pools)
2. **Center (Journey)**: Show structured 12-month roadmap with governance → migration → AI progression
3. **Right (Databricks)**: Show unified platform with AI capabilities (not just data warehouse replacement)

**Color Progression**: 
- Purple (legacy Synapse) 
- Deep Blue (governance foundation) 
- Grey (migration execution) 
- Orange (modern Databricks + AI)

---

## **Annotation Style**

- **Phase headers**: Bold, 18pt, AGL Deep Blue
- **Component boxes**: Rounded corners, simple icons, 14pt labels
- **Arrows**: 
  - Solid = data flow
  - Dashed = connection updates
  - Dotted = validation/federation
- **Progress bars**: Gradient fill (light to dark green based on completion)
- **Milestone markers**: Small circular badges on timeline with checkmarks

---

## **Exclusions (Removed for Executive Simplicity)**

Remove these technical details from PRO version:
- LakeBridge Analyzer/Converter/Reconcile technical workflow
- Detailed row/schema/column-level reconciliation specs
- Specific regulatory law citations (NEM, NERL, NERR, SOCI Act)
- Lakeflow connector mapping table (managed vs. standard)
- Unity Catalog three-level namespace explanation
- Detailed persona-based training matrix
- Risk mitigation matrix
- Peer company engagement specifics
- Week-by-week execution timeline
- Code conversion Gen-AI tool details

Keep focus on:
- 12-month phased journey (governance → migration → AI)
- Zero-downtime federation pattern
- 4 migration waves with progress visualization
- Key outcomes (4× performance, 30% cost, AI CoE)
- User enablement (100 trained)
- Unity Catalog as governance foundation

---

## **Use Cases for This Simplified Version**

**When to use**:
- Executive steering committee quarterly updates
- Board-level migration status presentations
- Customer success story (post-migration)
- Quick-reference poster for project war room
- Non-technical stakeholder alignment (finance, HR, legal)
- Change management communications

**When to use PRO version instead**:
- Technical architecture deep-dives
- LakeBridge scoping workshops
- Wave execution planning sessions
- Professional Services engagement planning
- Compliance/audit stakeholder briefings

---

## **Companion Assets**

This simplified version pairs with:
1. **agl_synapse_pro_v2_12mo.md** - Full technical depth (12-month plan)
2. **version_comparison.md** - Guidance on which version to use when
3. **agl_12month_migration_plan.md** - Phase breakdown from AGL's actual plan

---

**Document Classification**: Executive Visual Specification (12-Month Migration)  
**Version**: 2.0 Simplified – January 2026  
**Target Audience**: C-suite, board members, business stakeholders, change management teams
