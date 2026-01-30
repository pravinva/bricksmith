**Executive Summary: Databricks Roadmap and Energy-Sector Capabilities for AGL**

AGL Energy operates Australia's most complex energy data environment: 4.56 million customers, 15,200+ database objects across fragmented Azure/AWS infrastructure, and 92% capacity utilisation causing operational instability. Your strategic transformation to 12 GW renewable capacity by 2035 requires a platform purpose-built for energy operations, not generic cloud warehousing.

**Product Roadmap: Delivery Timeline**

**Q1 2025 (Now Available)**
- Unity Catalog cross-cloud external locations (GA): Query Kaluza billing data in AWS S3 directly from Azure Databricks without replication
- Automated data classification (Public Preview): AI-driven PII detection and tagging across customer data estate
- Agent Bricks Agent Framework (GA): Production-grade AI agents with governance, evaluation, and observability
- AI/BI Genie (GA): Natural language analytics for business users

**Q2 2025**
- Serverless compute intelligent workload management: Predictive autoscaling for 3,000+ queries per 10-minute peaks
- Unity Catalog Metric Views (GA): Semantic layer eliminating report sprawl—define customer churn rate, renewable generation capacity, emissions intensity once
- Lakeflow enhanced CDC: Sub-minute latency for SAP HANA and Salesforce sources
- Agent Bricks Gateway enhancements: 60% latency reduction, 40% cost reduction through automatic prompt caching

**Q3 2025**
- Serverless streaming: Sub-second latency for real-time meter data processing
- Automated data classification (GA): Production-ready PII governance
- Lakeflow Connect: 150+ SaaS connectors including AEMO market data feeds and SCADA historians
- Compound AI systems: Multi-step reasoning for renewable forecasting combining weather APIs, SCADA telemetry, NEM price signals

**Q4 2025**
- Serverless ML training: Automatic GPU provisioning for renewable forecasting models
- Enhanced column-level lineage: Impact analysis dashboards for schema change management
- Intelligent pipeline recommendations: AI-suggested partition strategies, Z-ordering, liquid clustering
- MLflow 3.0: GenAI-specific tracing, LLM judge evaluations, automated A/B testing

**Q1 2026**
- Unity Catalog automated data quality scoring: Freshness, completeness, accuracy metrics in Catalog Explorer
- Lakeflow automated data quality remediation: Self-healing pipelines quarantine invalid interval meter data

**Energy-Sector Differentiators: Why Databricks for Utilities**

**SCADA and OT/IT Integration**
Databricks Zerobus eliminates Kafka complexity for SCADA ingestion. Ignition Gateway, HiveMQ MQTT brokers, and RabbitMQ messages flow directly to Azure Event Hubs, then into Delta Lake with exactly-once processing guarantees. This native OT/IT bridge is unavailable in Snowflake or traditional warehouses—they require separate message buses, introducing latency and operational complexity. For AGL's battery storage and VPP orchestration across 1,487 MW of decentralised assets, Zerobus delivers sub-second telemetry processing enabling real-time state estimation and algorithmic dispatch.

**NEM 5-Minute Settlement and Real-Time Streaming**
Structured Streaming with Real-Time Mode delivers 40-300ms p99 latency—critical for Australia's transition to 5-minute settlement intervals. Snowflake's Snowpipe Streaming cannot match this latency for grid operations requiring sub-second response times (frequency regulation, voltage control, fault detection). Stateful stream processing handles de-duplication, anomaly detection, and smoothing of noisy SCADA telemetry, whilst watermarking manages late-arriving data from distributed generation assets.

**Battery Dispatch Optimisation and VPP Orchestration**
Agent Bricks Agent Framework enables autonomous dispatch algorithms coordinating battery storage, solar generation, and demand response. Streaming ML inference applies trained models to real-time NEM price signals and asset telemetry, generating dispatch instructions within seconds. MLflow Model Serving provides sub-100ms inference latency with automatic scaling—supporting FCAS market participation and frequency regulation services. Snowflake lacks native ML serving; their external function approach introduces 500ms+ latency, disqualifying it for real-time trading operations.

**Renewable Forecasting with Weather API Integration**
AutoML forecasting capabilities support Prophet, Auto-ARIMA, and DeepAR algorithms optimised for solar and wind generation prediction. Pre-built Energy Forecasting Solution Accelerator incorporates weather API integrations (Bureau of Meteorology, Solcast) and historical generation data. Unity Catalog tracks lineage from raw weather data through feature engineering to deployed models—ensuring explainability for trading operations and regulatory compliance.

**Digital Twin Capabilities for Generation Assets**
Digital Twin Solution Accelerator combines Zerobus Ingest with Structured Streaming and Delta Lake for sub-second telemetry processing. This enables real-time state estimation, predictive maintenance, and algorithmic dispatch across distributed energy resources. Delta Lake's time travel provides point-in-time queries supporting incident investigation and regulatory audits—maintaining 365-day audit retention for NEM settlement processes.

**Competitive Differentiation**

**Unified Batch + Streaming on Single Engine**
Databricks Spark processes historical, microbatch, and real-time data in declarative Lakeflow pipelines. Snowflake requires separate architectures: batch queries in warehouses, streaming via Snowpipe, forcing data duplication and operational complexity. For AGL's interval meter data, unified processing eliminates multi-hop architectures causing stale data.

**Open Formats Preventing Lock-In**
Delta Lake, Iceberg, and Parquet on ADLS Gen2 ensure data portability. Compute separates from storage—AGL retains ownership even if switching vendors. Snowflake's proprietary format locks data inside their platform; migration requires full export/import. Unity Catalog's open APIs enable federated queries from Power BI, Tableau, and Python without replication.

**AI Agents for Trading and Grid Operations**
Agent Bricks enables production GenAI applications: customer service chatbots, trading assistants analysing market signals for battery dispatch, predictive maintenance for generation assets. Multi-AI Indemnity covering OpenAI, Anthropic, Meta, Google provides legal protection for IP claims—eliminating procurement barriers. Snowflake's Cortex AI lacks governance frameworks for regulated industries; no indemnity protection for customer-facing applications.

**Measurable Outcomes**

Databricks delivers: 10x faster time-to-insight through serverless compute eliminating 92% utilisation constraints; 80% reduction in governance overhead via Unity Catalog automation across 15,200+ database objects; 70% query performance improvement from Predictive Optimisation; sub-100ms latency for grid operations supporting FCAS market participation; production-ready GenAI capabilities enabling AGL's "Technology, Digitisation and AI at the Core" strategic pillar.