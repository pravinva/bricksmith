Create a **future-state companion diagram** to the “Coles Group: Logical Semantic Fragmentation – From Hub Data Model to Tool-Specific Silos” slide.

This new slide should show the **target logical architecture** where Coles introduces a **central, governed semantic layer** (implemented on Databricks Lakehouse with Unity Catalog and Delta Lake) that publishes **enterprise semantic data products** to downstream tools (Power BI, Palantir, Fabric) in a consistent, governed way.

Maintain the same Databricks brand style, logo rules, colors, and flat design constraints as the previous prompt (no gradients, no numbered circles, white background, professional executive style).

---

# SUBJECT

Title:

> “Coles Group: Future-State Logical Architecture – Governed Semantic Layer Feeding All Analytics”

Sub-title (under the title, smaller):

> “From tool-specific models to a single governed semantic backbone”

This is a **positive**, clean architecture: the visual should clearly contrast with the earlier fragmentation slide. It should communicate **coherence, reuse, and governance**, not chaos.

---

# NARRATIVE INTENT

The future-state diagram must make these points visually:

- Coles **introduces a central semantic layer** on the Lakehouse (Unity Catalog + Delta Lake) that expresses the **enterprise logical model** (Customer, Product, Store, Order, Promotion, metrics).
- That semantic layer is **governed and shared**: one set of definitions, reused everywhere.
- Downstream tools (Power BI, Palantir, Fabric) **consume**, not reinvent, the semantic model.
- This is aligned with **data mesh** and **federated computational governance**: domains publish semantic data products; platform provides the semantic backbone and catalog.

---

# HIGH-LEVEL STRUCTURE (FOUR HORIZONTAL BANDS)

## BAND 1 – Source Systems (Same as Before)

- Keep the **same** top band as the current-state slide for direct comparison:

  - Light-gray boxes in a row:
    - “SAP”
    - “Legacy Systems”
    - “Third-Party Data”
    - “Operational Sources”
  - Downward neutral arrows into the Lakehouse ingestion zone.
  - Small label below: “Raw operational data (system-of-record schemas)”.

- Style:
  - Background boxes: #F5F5F5, text #1B3139.
  - Arrows: thin gray #CCCCCC, straight, clean.

## BAND 2 – Lakehouse & Central Semantic Layer (Target Hub)

This band replaces “Snowflake-only hub” with a **Databricks Lakehouse + Unity Catalog** semantic hub that still interoperates with Snowflake if needed, but **centralizes semantics**.

### 2A. Lakehouse Storage

- Left/center, show a **Databricks Lakehouse zone**:
  - Databricks logo (top-left of the zone).
  - Delta Lake logo inside this zone.
  - Box title: “Databricks Lakehouse (Delta Lake)”.
  - Subtitle: “Curated & conformed data products”.

- Optional: To acknowledge Snowflake still exists as a hub:
  - To the right, a smaller Snowflake box:
    - Title: “Snowflake Data Warehouse”.
    - Subtitle: “Additional analytical storage (optional)”.
  - Draw a thin, bi-directional connector between Lakehouse and Snowflake labeled:
    - “Synced / mirrored datasets” (small text).

### 2B. Central Semantic Layer (Logical Model, Governed)

Directly over or integrated into the Lakehouse zone, draw a **prominent semantic layer band**:

- Use the **Unity Catalog logo** plus a clear label:

  - Title: “Unity Catalog Semantic Layer”.
  - Subtitle: “Governed enterprise logical model & metrics”.
  - Small note: “Federated computational governance, reusable across domains”.

- Inside this semantic layer band:

  1. **Entity strip** (similar to the current-state slide, but more formal and clean):
     - Rectangles labeled:
       - “Customer”
       - “Product”
       - “Store”
       - “Order”
       - “Promotion”
     - Clean relationship lines:
       - Customer → Order
       - Order → Product
       - Order → Store
       - Promotion → Order
     - Style:
       - White boxes, navy text, navy borders.
       - Lines in gray #A0ACBE, straight and neat.

  2. **Metrics cluster**:
     - A white box titled “Enterprise Metrics (Governed)” with navy border and a Databricks-orange heading bar.
     - Inside, list:
       - Gross Sales
       - Net Sales
       - Units Sold
       - Like-for-Like Sales
       - Basket Size
       - Profit / Margin
     - Note at bottom in small italic text:
       - “Defined once, reused everywhere”.

  3. **Data products callout** (right side of the semantic layer band):
     - Small labeled list:
       - “Sales Domain Data Products”
       - “Customer Domain Data Products”
       - “Product Domain Data Products”
     - Note: “Published with contracts in Unity Catalog”.

- The entire semantic band should feel like a **calm, authoritative backbone**:
  - Background: light blue strip (#E8F4F8) behind entities/metrics.
  - Border: thin navy frame around the semantic band.

---

## BAND 3 – Consuming Tools (Spokes, Now Aligned)

Below the semantic layer, show **three primary consumer/tool lanes** (Power BI, Palantir, Microsoft Fabric). Each lane should now clearly show **CONSUMPTION**, not reinvention.

### Shared visual rules

- All arrows from the semantic layer to tools:
  - Color: Databricks-orange (#FF3621) or navy.
  - Style: Straight, aligned, same thickness (2–3px).
  - Direction: Vertical downward from semantic layer to each tool.
  - Label on each arrow: “Semantic model consumption (read-only)”.

- No red borders here; these are **good** patterns.

### Lane 1 – Power BI (BI Consumption)

- Box with Power BI logo on the left.
- Title: “Power BI – Thin Semantic Models”.
- Subtitle: “Reusing enterprise semantic layer”.
- Inside the box:
  - Small stylized table icons labeled “Imported semantic model”.
  - A short measures list:
    - [M] Gross Sales (from UC)
    - [M] Net Sales (from UC)
    - [M] LFL Sales (from UC)
  - Small note at bottom:
    - “No re-definition of core entities or metrics”.

### Lane 2 – Palantir (Exploratory UX on Shared Semantics)

- Box with Palantir branding.
- Title: “Palantir Ontology – UX on Shared Entities”.
- Subtitle: “Visual exploration on governed model”.
- Inside:
  - Node-link mini-graph labeled with:
    - “Customer (from UC)”
    - “Order (from UC)”
    - “Product (from UC)”
  - Note:
    - “Ontology built over central semantic layer, not separate truth”.

### Lane 3 – Microsoft Fabric (Governed Experimentation)

- Box with Microsoft Fabric logo.
- Title: “Microsoft Fabric – Governed Workloads”.
- Subtitle: “Aligned to central semantic layer”.
- Inside:
  - Lakehouse/dataset icon labeled “Semantic-aligned datasets”.
  - Mini “Semantic model” icon labeled “Inherits definitions from UC”.
  - Note:
    - “Experiments reuse governed entities and metrics”.

---

## BAND 4 – Data Mesh & Governance Outcomes (Positive)

At the bottom, show a **green/teal (or navy) impact band** that contrasts the red one on the current-state slide.

- Background: navy (#1B3139) or a strong, non-red accent.
- Text color: white (#FFFFFF).
- Title: “Outcomes with a Central Semantic Layer & Federated Governance”.
- Bullets:
  - “Customer, Product, Store, O
