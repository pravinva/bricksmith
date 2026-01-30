1.0.4a Product Roadmap
Databricks' product roadmap directly addresses AGL's operational fragility and capacity saturation challenges through three strategic investment pillars: intelligent automation, unified governance, and AI-native capabilities. Our development priorities align with AGL's transformation to connect 4.56 million customers whilst transitioning to 12 GW renewable capacity by 2035.
Serverless Compute Evolution (GA Now – Continuous Enhancement)
Serverless compute eliminates AGL's 92% utilisation constraint and manual capacity management. Currently in General Availability across all compute types including SQL, notebooks, model serving, and streaming workloads, delivering cold start times within seconds and automatic elastic scaling—directly resolving the "access is unstable, or pipelines fail" issues reported by AGL stakeholders.
Largely due to demand from AGL, we released our Serverless Capability into Azure Australia South East on 21st November 2025. It is currently pending security review and architecture endorsement.
Q4 FY26 (Nov 2025–Jan 2026) brings enhanced Intelligent Workload Management with predictive autoscaling that pre-provisions capacity ahead of AGL's 3,000+ queries per 10-minute peak loads. Serverless cost controls (Q4 FY26) introduce t-shirt size rate limits and entitlements, enabling workspace admins to control costs whilst maintaining elastic scaling.
Q1 FY27 (Feb–Apr 2026) delivers Serverless GPU Compute Public Preview for renewable forecasting models with automatic A10G and H100 provisioning, whilst Real-Time Streaming Mode (GA April FY27) provides sub-second latency for operational workloads including Collections and grid monitoring.

Unity Catalog: Unified Governance Maturity (GA Now – Q2 FY27)
Unity Catalog's roadmap directly tackles AGL's data fragmentation across Azure and AWS, eliminating silos between Kaluza (AWS), Salesforce (AWS), and Azure corporate systems whilst providing the single source of truth required to rebuild business confidence.
Q4 FY26 (Now – Jan 2026) delivers three crucial  governance capabilities:
ABAC, Governed Tags, and Data Classification (GA Jan FY26): Automated governance where agentic AI scans and tags PII within 24 hours, automatically applying attribute-based access control policies to mask sensitive customer data—reducing manual classification effort by 80% whilst helping ensure Australian Privacy Principles compliance
Unity Catalog Business Semantics (GA Dec FY26): Semantic layer capabilities enabling AGL to define metrics once (customer churn rate, renewable generation capacity, emissions intensity) and consume them consistently across AI/BI Genie, Dashboards and PBI SQL queries—directly resolving the "multiple non-enterprise systems creating conflicting metrics" challenge
Data Quality Monitoring (Public Preview Dec FY26): Automated ML-driven anomaly detection across freshness and completeness, answering "Is the data I'm looking at the most current/accurate?" through health indicators surfaced directly in Catalog Explorer
Q1 FY27 (Feb–Apr 2026) introduces:
Enhanced column-level lineage with impact analysis dashboards, enabling data stewards to visualise downstream dependencies before schema changes—preventing unintended breakage across 15,200+ database objects
Request for Access (GA): Self-service workflow where users discover datasets and request permissions with automated routing to asset owners via Slack/email/Teams—eliminating manual IT tickets
Discover Page (Public Preview Q1 FY27): Curated internal marketplace with AI-powered recommendations surfacing high-value certified datasets, dashboards, and AI agents—solving "I don't know where data is, how do I access it?"
Q2 FY27 (May–Jul 2026) we are aiming for a Global Unity Catalog across regions, clouds, and accounts whilst maintaining single source of truth without manual reconciliation—critical for AGL's multi-region disaster recovery requirements.

Lakeflow: Intelligent Data Engineering (GA Now – Q3 FY27)
Lakeflow replaces manual, offline ETL processes with declarative, self-healing pipelines whilst enabling low-risk Synapse migration through automated code conversion.
Lakebridge Migration Platform (Q4 FY26 – Q1 FY27)
Purpose-built for AGL's Synapse migration, Lakebridge combines three complementary conversion engines—BladeBridge (strategic acquisition), Morpheus (field-proven), and LLM-based converters—delivering unmatched accuracy:
/migrate Assistant Function (GA Q3 FY26): Code translation directly in SQL editor or notebooks, converting Synapse SQL to ANSI SQL with context-aware suggestions
Analyzer Results Dashboard (GA Q4 FY26): Automated assessment of AGL's 3,742 simple, 2,650 medium, and 60 complex/very complex objects with migration complexity scoring and dependency mapping
LLM Validator (Q4 FY26 – Q1 FY27): Validates syntax and business logic ensuring converted code runs correctly on Databricks—providing migration confidence through automated testing
Synapse Profiler & Reconciler (Q4 FY26 – Q1 FY27): Automated data reconciliation during parallel cutover runs, ensuring data integrity and quality for end-user consumption
Lakeflow Connect Expansion (Q4 FY26 – Q1 FY27)
Managed connectors reduce integration effort by 60-80%:
Database CDC Connectors (Q4 FY26 – Q1 FY27): MySQL, PostgreSQL, Oracle CDC with sub-minute latency for SAP BDC and Salesforce sources—eliminating multi-hop architecture causing stale data
Query-Based Connectors (Q4 FY26 – Q1 FY27): Azure Synapse Analytics connector enabling federated queries during migration, plus Teradata, BigQuery, Snowflake, Redshift for multi-platform integration
Unstructured Data for AI (Q4 FY26 – Q1 FY27): SharePoint, Google Drive, Jira, Confluence connectors with ACL preservation—enabling RAG applications grounded in AGL's technical documentation and operational knowledge
Zerobus Public Preview (Q4 FY26): Push records directly to Delta for IoT telemetry and clickstream data with sub-5-second latency, supporting SCADA integration and smart meter streaming for your new battery sites.
Lakeflow Spark Declarative Pipelines (GA Now – Q1 FY27)
Data Engineering Agent (Beta Q4 FY26): Autonomous pipeline generation from natural language—users prompt "Ingest Salesforce opportunities with CDC, validate required fields, enrich with customer data" and agent automatically generates complete SDP pipeline
Real-Time Mode (Public Preview July FY26, GA April FY27): Millisecond-latency streaming for operational applications including Collections and grid monitoring—transforming from overnight batch to sub-second intelligence
Polished IDE for Pipelines (GA Q4 FY26): Data engineering workspace with data previews, execution insights, git integration, and observability—accelerating development by 40-50%

Agent Bricks: Production GenAI for Energy Operations (GA Now – Q3 FY27)
Agent Bricks democratises production-grade AI across AGL's organisation whilst maintaining enterprise governance—directly enabling the "Technology, Digitisation and AI at the Core" strategic pillar.
Agent Bricks (Q4 FY26 – Q1 FY27)
Pre-built agent patterns compressing proof-of-concept from months to days:
Knowledge Assistant (GA Dec FY26): Production-quality RAG chatbots answering operational questions from technical manuals, regulatory documents, and incident reports—supporting customer service automation and compliance extraction
Multi-Agent Supervisor (GA Jan FY27): Orchestrates complex workflows across customer, asset, and market data domains with autonomous task delegation—enabling VPP dispatch optimization and cross-domain analytics
Information Extraction (Integration with AI Functions Q1 FY27): Extract structured data from AEMO regulatory filings, AASB S2 templates, and NEM rule changes—reducing manual compliance effort
AI/BI Intelligence Layer (GA Now – Q1 FY27)
Genie Research Agent (Beta Nov FY26, Public Preview Dec FY26): Deep research capabilities with multi-turn interactions and comprehensive report generation—enabling business users to perform complex analysis through conversation
Databricks One (Workspace GA Jan FY26): ChatGPT-like experience for business users with unified chat (PrPr Q4 FY26), domain-organised content, and simplified onboarding—democratising access for non-technical stakeholders
Data Science Agent (GA Q4 FY26 = Jan 2026): Autonomous data science workflows including EDA, data cleaning, feature engineering, and model training from single natural language prompt—answering "I want to develop a model... how do I do this?"
Foundation Model Serving (Q4 FY26 – Q1 FY27)
Anthropic Claude Provisioned Throughput (Q4 FY26): Production-grade performance guarantees for in-region Australian deployment—enabling sensitive customer interactions with data sovereignty
OpenAI GPT, Gemini 2.5, Qwen3 Provisioned Throughput (Q4 FY26): Guaranteed performance for high-throughput applications with sub-50ms latency.
AI Gateway IA Redesign (Beta Oct FY26, Public Preview Q1 FY27): Unified governance across all foundation models with custom guardrails, token-based rate limiting, and comprehensive audit trails
These roadmap investments are designed to deliver measurable operational shifts: accelerating time-to-insight through serverless compute, streamlining governance overhead via Unity Catalog automation, optimising query performance through Predictive Optimisation, and establishing the production-ready AI capabilities required for AGL's strategic transformation.

1.0.4b Artificial Intelligence (AI) Strategy
Databricks' AI strategy centres on democratising production-grade AI across AGL's organisation whilst maintaining enterprise governance—directly enabling the "Technology, Digitisation and AI at the Core" strategic pillar through platform-native capabilities that eliminate the fragmentation of multi-vendor AI stacks.
Current AI Utilisation: Platform-Native Intelligence
Databricks embeds AI throughout the platform today, delivering immediate value without additional licensing:
AI for Data Operations (Operational AI)
Predictive Optimisation (GA, Enabled by Default): AI manages table maintenance automatically—running OPTIMIZE, VACUUM, and ANALYZE based on usage patterns. Over 2,400 customers achieved up to 20x query performance improvements and 2x storage cost reductions without manual tuning, directly addressing AGL's resource contention and unpredictable query performance
Intelligent Workload Management: ML predicts query resource requirements, dynamically scales compute, and prioritises short-running queries—eliminating the 92% utilisation constraint whilst maintaining cost efficiency
Automated Data Classification (Public Preview → GA Jan FY26): Agentic AI scans and tags PII across 4.56 million customer records within 24 hours, enabling automatic policy enforcement—solving "I don't know where data is" through intelligent metadata management
AI for Analytics & Insights (Embedded AI)
AI/BI Genie (GA, 16K Weekly Active Users): Natural language to SQL conversion—business users ask "What's our customer churn rate in NSW for Q4 2024?" and receive instant visualisations without SQL expertise. 527% YoY growth demonstrates market-leading adoption
Databricks Assistant (GA): Context-aware code generation leveraging Unity Catalog metadata and AGL-specific terminology—accelerating developer productivity by 40%. The /findTables command discovers relevant datasets across 15,200+ objects using natural language
ai_forecast() SQL Function (GA): Multivariate time-series forecasting directly in SQL for demand prediction, renewable generation variability, and grid balancing—enabling predictive analytics for business analysts without Python expertise
ai_parse_document (Public Preview Q3 FY26): Extract structured data from PDFs, DOCX, and regulatory filings for automated compliance reporting—reducing manual effort for AASB S2 metrics tracking
AI for Custom Applications (Generative AI)
Agent Bricks Agent Framework (GA): Production-quality RAG applications and multi-agent systems with unified governance—enabling battery dispatch algorithms, customer service automation, and regulatory compliance extraction
Foundation Model APIs with Provisioned Throughput: Sub-50ms inference with performance guarantees for customer-facing applications—supporting real-time Collections use cases and operational decision-making
MLflow 3 with GenAI Tracing: Complete lineage from prompts to responses with automated LLM judge evaluations—ensuring AI applications meet regulatory compliance and customer trust standards

Features in Development: Strategic Capabilities for Energy Operations
Databricks continuously enhances the Data Intelligence Platform with capabilities designed to accelerate AI adoption, simplify data engineering, and strengthen governance across AGL's energy operations.
Q4 FY26 (November 2025 – January 2026): Intelligent Automation
Data Science Agent (GA January 2026)
Transforms AI/ML from specialist tools to natural language workflows. Users prompt "Build churn prediction model using consumption patterns and payment history" and the agent autonomously performs exploratory data analysis, feature engineering, model training, and deployment—enabling data scientists to accelerate model development whilst maintaining governance standards.
Additional Q4 Capabilities:
Data Engineering Agent (Beta): Automates Lakeflow pipeline creation from natural language prompts, accelerating ETL development through intelligent code generation for ingestion, transformation, and data quality rules.
Genie Research Agent (Beta November, Public Preview December): Enables deep research capabilities with multi-turn interactions, clarification questions, and comprehensive report generation—supporting complex analytical workflows through conversational interfaces.
ABAC + Data Classification (GA January 2026): Delivers automated governance at catalogue level where AI detects PII, tags columns, and applies masking policies automatically—transforming manual governance into intelligent automation whilst maintaining Australian Privacy Principles compliance.
Lakebridge Validator (Q4 FY26): Ensures Synapse-converted code runs correctly on Databricks through automated syntax and business logic validation—providing migration confidence through comprehensive testing and reconciliation.
Q1 FY27 (February–April 2026): Enterprise Self-Service & Discovery
Databricks One Workspace (GA January 2026)
ChatGPT-like interface for business users with unified chat experience, democratising platform access beyond technical teams to analysts, domain experts, and stakeholders across AGL's operations.
Knowledge Assistant & Multi-Agent Supervisor (GA December 2026 / January 2027)
Production-grade AI agents with inference APIs enabling customer service automation, operational advisors, and regulatory reporting assistants whilst maintaining comprehensive audit trails and governance controls required for regulated energy operations.
Discover Page (Public Preview Q1 FY27)
AI-curated internal marketplace surfacing certified datasets, dashboards, and AI agents with quality signals—solving data discovery challenges through intelligent recommendations whilst respecting Unity Catalogue access controls.

Value Delivery: Measurable Business Outcomes
Our AI strategy delivers value across AGL's strategic drivers through a platform uniquely designed to give enterprise context to your data securely—this is why Databricks is recognised as the Gartner Leader of Leaders for Data Science and Machine Learning platforms.
Business Intelligence
AI/BI Genie reduces time-to-insight from hours to seconds, enabling self-serve analytics. Automated data quality monitoring prevents the "Is this data current/accurate?" concerns eroding trust, whilst intelligent metadata management answers "How can I understand the data I'm looking at?" AI/BI Genie includes human-in-the-loop benchmarking and evaluation capabilities built in—ensuring continuous quality improvement through subject matter expert feedback.
Operational Excellence
Predictive Optimisation eliminates manual performance tuning (70% faster queries), Databricks Assistant accelerates pipeline development by 40%, and automated anomaly detection catches issues before impacting operations. Real-time streaming with ML-driven quality checks ensures interval meter data meets NEM settlement requirements.
Technology, Digitisation and AI at the Core
Agent Bricks enables production GenAI applications across customer service (billing enquiries), trading operations (market signal analysis for battery dispatch), and asset management (predictive maintenance). MLflow 3.8 provides comprehensive testing and evaluation with LLM-as-a-Judge assessments, complete trace logging to Unity Catalog Delta tables, and automated drift detection—ensuring AI applications deliver reliable, compliant outcomes. Our Multi-AI Indemnity covering OpenAI, Anthropic, Meta, and Google provides legal protection for IP claims, eliminating procurement barriers.
Governance and Responsible AI
Unity Catalog extends governance to AI assets, tracking lineage from training data through deployed models. This capability is unique to Unity Catalog. MLflow Model Registry provides versioning and approval workflows, whilst Lakehouse Monitoring detects model drift in production. Agent Bricks Gateway enforces responsible AI policies at inference layer—detecting and blocking PII in prompts, filtering toxic content, and maintaining comprehensive audit trails supporting regulatory compliance.
Our AI strategy positions AGL to lead the energy sector in AI adoption whilst maintaining rigorous governance required for regulated operations—delivering measurable productivity gains, operational improvements, and customer experience enhancements across the enterprise.

1.0.4c Adaptability to Industry Changes
Databricks demonstrates continuous adaptability to energy sector requirements through purpose-built capabilities, strategic partnerships, and rapid feature development responding to sector-specific challenges.
Energy Sector Adaptations: Operational Technology Integration
Databricks adapted platform architecture to support unique requirements of energy OT environments:
Direct SCADA Integration

Zerobus Ingest pattern (Public Preview Q4 FY26) enables direct integration with SCADA systems including Ignition and HiveMQ for real-time processing. We are currently in the process of publishing our Zerobus Connector officially in the Ignition Marketplace. This eliminates proprietary barriers between OT and IT systems, enabling unified analytics across generation assets, transmission networks, and customer operations.
Digital Twin Solution Accelerator

For AGL's battery storage and VPP orchestration, we developed accelerator combining Zerobus Ingest with Structured Streaming and Delta Lake for sub-5 second telemetry processing. This enables real-time state estimation, predictive maintenance, and algorithmic dispatch across distributed energy resources—directly supporting AGL's 1,487 MW decentralised assets and expansion to 12 GW renewable capacity.
Lakehouse Federation for Energy Data Sources

Adapted to support SQL Server historian databases, Oracle PI System integrations, and legacy SCADA repositories. Push-down query optimisation minimises data movement whilst Unity Catalog provides unified governance across OT and IT systems—enabling federated queries combining real-time SCADA telemetry with customer billing data and NEM market signals without replication.

Regulatory Compliance Adaptations: Australian Energy Market
Databricks rapidly adapted to Australian regulatory requirements:
Mandatory Climate Reporting (AASB S2)
Automated data lineage capabilities provide traceable data provenance required for 79 climate metrics across Scope 1, 2, and 3 emissions—critical for AGL as Australia's largest corporate emitter at 30.7 MtCO₂e.
Australian Privacy Principles & IRAP Certification
Unity Catalog fine-grained access controls and 365-day audit logging support APP compliance for customer energy data
IRAP PROTECTED certification (GA AWS Sydney, obtained Q3 FY26 for GCP, Public Preview Azure) validated by ACSC-accredited assessors—supporting critical infrastructure operators
Delta Lake ACID transactions and time travel ensure data integrity for NEM settlement processes
Interval Meter Data Validation

Lakehouse Monitoring adapted to support automated quality checks for 15-minute and 5-minute interval data required for NEM wholesale market settlement. Configurable expectation rules validate timestamp integrity, value ranges, and mandatory fields—preventing settlement errors and regulatory penalties.

Renewable Energy Forecasting & Real-Time Grid Operations
AutoML Forecasting for Energy (GA)
Purpose-built for renewable energy prediction supporting Prophet, Auto-ARIMA, and DeepAR algorithms optimised for time-series data with seasonal patterns and weather dependencies. Energy Forecasting Solution Accelerator provides pre-built notebooks for solar and wind generation forecasting with weather API integrations.
Structured Streaming with Real-Time Mode (Public Preview July FY26)
Delivers 40-300ms p99 latency for event processing—adapted for frequency regulation, voltage control, and fault detection where traditional batch processing introduces unacceptable delays. Stateful stream processing handles de-duplication, anomaly detection, and smoothing of SCADA telemetry. In combination with Lakebase, Databricks can serve as an effective Operational Data Store for your applications.

Multi-Cloud Adaptations for Energy Sector M&A
Unity Catalog adapted to support cross-cloud governance in response to energy sector consolidation trends. For AGL's Kaluza acquisition (AWS) and Salesforce deployment (AWS), cross-cloud external locations enable unified analytics without data migration—preserving existing investments whilst eliminating silos.
This adaptability proved critical as energy retailers increasingly operate hybrid architectures: customer platforms on AWS (Salesforce, Kaluza), corporate systems on Azure (ERP, finance), and edge computing for distributed assets. Our consistent governance model across clouds reduces integration complexity and accelerates innovation.
These adaptations demonstrate Databricks' commitment to energy sector requirements—positioning AGL to lead the industry's digital transformation with purpose-built capabilities addressing operational technology integration, regulatory compliance, renewable forecasting, real-time grid operations, and multi-cloud complexity.

1.0.4d Future Industry Alignment
Databricks aligns with energy market evolution through active customer collaboration and platform capabilities designed to flex with regulatory and technological transformation. Rather than predetermined roadmaps, we provide foundational capabilities that allow AGL to configure the platform to meet emerging requirements—ensuring you retain control as Australia's energy landscape transforms.
Australia's Energy Market Transformation
Australia's National Electricity Market (NEM) is experiencing unprecedented change. These are not distant possibilities, but imminent requirements demanding platform adaptability:
Renewable Explosion: AEMO forecasts a tripling of solar and wind capacity by 2030, with South Australia targeting 100% renewables within this decade (already at 85%).
Data Mandates: The AEMC has mandated real-time consumer energy data access from smart meters by 1 Jan 2028, fundamentally changing demand response and personalization.
Compliance Pressure: AASB S2 climate-related financial disclosures become mandatory for AGL in FY26, requiring auditable data flows from operations to investor reporting.

Strategic Capabilities for AGL
To address these shifts, Databricks offers specific technical advantages:
1. Distributed Energy Resources (DER) & Virtual Power Plants
The shift to behind-the-meter assets requires speed. Databricks Real-Time Mode (Public Preview) delivers 40-300ms p99 latency for operational workloads. This enables frequency regulation, battery dispatch optimization, and VPP coordination at grid-timescale speeds. Unity Catalog’s governance scales to millions of assets while maintaining privacy, supporting AGL’s orchestration of 1.49 GW of decentralized assets today and expansion toward 2.5 GW by FY27.
2. Climate Transition & Mandatory Reporting
Unity Catalog delivers the governance foundation needed for AASB S2 compliance—including automated lineage, audit logging, and fine-grained access controls. By tracing emissions data from the source, AGL can ensure auditability. Furthermore, our planned SAP Green Ledger integration (Q4 2025) will tie carbon accounting to financial dimensions, streamlining integrated climate and financial reporting.
3. Electrification & Transport Integration
Partner solutions, such as CKDelta ∆Power, provide AI-driven EV charging network optimization to maximize revenue and carbon offsets. Our unified platform supports real-time pricing and grid integration with governed customer data. This enables cross-sell opportunities while maintaining the necessary regulatory separation between electricity retail and charging infrastructure.
4. Autonomous Operations & Agentic AI
To accelerate the deployment of autonomous grid operations and predictive asset management with AI, Databricks provides a Multi-AI Indemnity. This covers OpenAI, Anthropic, Meta, and Google models, protecting AGL against IP claims (including judgments and legal fees). This removes procurement barriers, allowing AGL to safely deploy customer-facing AI and agentic workflows.


1.0.4e Industrial Data Strategy
Databricks provides a comprehensive industrial data platform purpose-built for energy operations, addressing SCADA systems, IoT sensor streams, and time-series data requirements across AGL's generation assets, transmission networks, and distributed energy resources.
SCADA Integration & Operational Technology Connectivity
Real-Time Streaming Ingestion
Zerobus Ingest enables real-time data flow from Ignition SCADA and HiveMQ MQTT brokers to Azure Event Hubs or AWS Kinesis for immediate processing. This eliminates the traditional air gap between operational technology and IT systems, enabling unified analytics across generation control, substation automation, and customer operations.
Historian Federation
Lakehouse Federation provides read-only federated queries to legacy SCADA historians including OSIsoft PI System, Wonderware, and GE Proficy via JDBC connections. AVEVA CONNECT delivers native Delta Sharing integration with five-minute refresh intervals. Push-down query optimisation executes filters and aggregations at source, minimising data movement whilst Unity Catalog enforces consistent access controls.
Real-Time Processing
Structured Streaming processes SCADA telemetry with exactly-once guarantees, handling deduplication, anomaly detection, smoothing algorithms, and watermarking for late-arriving data from distributed assets.
IoT Sensor Stream Processing at Scale
Databricks ingests IoT streams through native cloud integrations (Azure IoT Hub, AWS IoT Core) and Lakeflow Connect for MQTT brokers and Kafka clusters. Custom PySpark Data Sources enable reusable connectors for industrial protocols including Modbus and OPC-UA.
For AGL's battery storage and solar farms, Structured Streaming processes millions of sensor readings per second with sub-second latency. Delta Lake provides ACID transactions for concurrent writes from thousands of distributed sensors, ensuring data consistency despite network partitions and device failures.
Time-Series Data Optimisation
Delta Lake optimises time-series storage through partition pruning via timestamp hierarchies, Z-ordering for 10× faster queries on asset ID and sensor type, Predictive Optimisation automatically compacting small files whilst maintaining 70% faster queries, and time travel providing point-in-time queries for regulatory audits.
Real-Time Analytics & Operational Applications
Structured Streaming with Real-Time Mode delivers 40–300ms 99th percentile latency for frequency regulation, fault detection, and battery dispatch optimisation responding to NEM 5-minute market intervals. Streaming ML inference via MLflow Model Serving delivers sub-100ms latency with automatic scaling.
Databricks Apps enables custom operational applications including:
Asset Health Monitors with sub-second updates on unit status and predicted failures
Collections Optimiser providing real-time payment risk scores and recommended actions
VPP Dispatch Controller with scenario simulation and autonomous command execution
These industrial data capabilities eliminate the 6-hop architecture complexity (SAP HANA → ADF → Databricks → Parquet → Synapse → PBI) introducing unacceptable latency—replacing it with direct streaming ingestion achieving sub-second end-to-end latency whilst maintaining enterprise governance and regulatory compliance required for critical energy infrastructure.
Cloud Platform & Data Lake Integration
The platform integrates seamlessly with Azure (Event Hubs, IoT Hub, ADLS Gen2, Monitor) and AWS (Kinesis, IoT Core, S3, CloudWatch). Delta Lake serves as the unified lakehouse storage layer with ACID transactions, schema evolution, and time travel. Unity Catalog delivers centralised governance, lineage, and audit logging across OT and IT systems.

