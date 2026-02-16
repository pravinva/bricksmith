# AGL Energy — Zerobus High-Level Architecture

## Customer Context

AGL Energy operates 2M+ historian tags across coal, gas, hydro, wind, and battery assets.
Their current stack is anchored on AVEVA PI — proprietary formats, expensive per-tag licensing,
and heavy operational overhead for every new site onboarding.

The Zerobus solution replaces this with an open lakehouse architecture: a single Ignition
module at the edge streams data directly into Databricks Delta Lake, enabling real-time
analytics without proprietary lock-in.

## Architecture Overview (High Level)

This diagram should show the **big picture** — the end-to-end data journey from industrial
assets to business decisions, without exposing implementation internals.

### Left: Industrial Assets (Data Sources)
AGL's physical asset fleet generates operational telemetry:
- **Power Generation Assets**: Coal (Bayswater, Loy Yang), Gas (Torrens Island), Hydro (Kiewa)
- **Renewable Assets**: Wind farms (Macarthur, Hallett), Solar, Battery storage (Liddell, Tomago)
- **SCADA/PLC/OPC-UA**: Industrial control systems producing real-time sensor data
- **2M+ historian tags** flowing from these assets

### Center-Left: Ignition Gateway (Edge/On-Premises)
A single box representing the on-premises Ignition SCADA platform:
- **Zerobus Connector**: Single module that compresses, buffers, and streams data to the cloud
- Key message: "One module replaces entire AVEVA PI infrastructure"
- Guaranteed delivery with store-and-forward
- SDT compression at the edge (same algorithm as AVEVA PI)

### Center: Network Boundary
- **gRPC/TLS** encrypted stream from edge to cloud
- Simple, secure, single connection

### Center-Right: Databricks Lakehouse
The cloud platform processing and serving data:
- **Streaming Ingestion**: Real-time data landing via Zerobus Endpoint
- **Medallion Architecture**: Bronze (raw) → Silver (enriched) → Gold (analytics)
- **All data in Delta Lake**: Open format, ACID, time travel
- **Unity Catalog**: Governance, lineage, access control across all data
- **Lakeflow Pipelines**: Automated data processing from raw to analytics-ready

### Right: Analytics & Business Outcomes
What the platform delivers to AGL:
- **Databricks App**: Operational dashboard for asset operators and energy traders
- **Asset Health Monitoring**: Z-score anomaly detection per asset
- **NEM Market Integration**: Price forecasting and revenue risk assessment
- **Actionable Recommendations**: Automated severity ladder from "Monitor" to "Critical shutdown"
- **Revenue Risk Quantification**: capacity × hours × price × failure probability

## Key Messages (What the Diagram Should Convey)

1. **Simplicity**: One Zerobus module replaces the entire AVEVA PI infrastructure stack
   (collectors, buffer nodes, relay nodes, archive servers)
2. **Open Standards**: All data in Delta Lake — no vendor lock-in, open formats
3. **Edge to Insight**: Continuous flow from physical assets to business decisions
4. **Real-Time**: Streaming architecture — not batch ETL, continuous data flow
5. **Business Value**: Not just data storage — actionable analytics, revenue protection,
   predictive maintenance recommendations

## What to Abstract Away (DO NOT show)

- Internal Zerobus module stages (OtEventMapper, StoreAndForwardBuffer, ZerobusEventSink)
- Protobuf message formats
- Buffer tier details (Memory Buffer, DiskSpool)
- Watermark/backpressure mechanisms
- REST API endpoints
- Table names (agl_demo.ot.raw_tags etc.)
- Code file references (bronze_silver.py etc.)
- Individual materialized view details

## Diagram Requirements

- Show **industrial assets** on the far left as the data origin
- Show the **Ignition Gateway + Zerobus** as a single clean box at the edge
- Show **Databricks Lakehouse** as the main platform with medallion layers
- Show **analytics/business outcomes** on the far right as the value delivery
- Use the **AGL Energy logo** prominently (top-left or header)
- Use the **Kaluza logo** (technology partner) — positioned near the Zerobus/edge component
- The diagram should read left-to-right: Assets → Edge → Cloud → Insights
- Keep it to **5-7 major components** maximum — this is a boardroom diagram, not a technical spec
- Emphasise the contrast: "Before (complex AVEVA PI stack)" vs "After (single module + lakehouse)"
