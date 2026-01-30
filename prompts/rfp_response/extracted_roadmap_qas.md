# Extracted Q&As for Product Roadmap / Technology Strategy

## AI Governance

### RES.070: Explain your policy-driven governance framework for AI models....

**Response:** Databricks delivers policy-driven AI governance through Unity Catalog, applying consistent access controls, audit trails, and compliance frameworks across all AI assets, data, and analytics.  Three core capabilities enable this:  1. Centralised policy enforcement: MLflow AI Gateway governs all LLM endpoints (external models like OpenAI/Anthropic and Databricks-hosted models) with configurable guardrails for PII detection, safety filtering, role-based permissions, and token-level rate limiting pe...

---

### RES.071: How do you enforce ethical AI guidelines and bias checks?...

**Response:** Databricks enforces ethical AI guidelines through three integrated layers critical for AGL's customer-facing and operational AI systems.  Detection and Assessment: Agent Bricks Agent Evaluation provides built-in LLM judges assessing safety, bias, groundedness, and correctness with plain-language rationales. Custom LLM Judges can also be configured to align with your requirements. Lakehouse Monitoring delivers automated fairness metrics for classification models, including predictive parity and equa...

---

### RES.072: Describe your audit trail capabilities for AI model lifecycle events....

**Response:** Databricks delivers comprehensive audit trails for AI model lifecycle events, supporting AGL's governance requirements across energy operations and regulatory compliance.  MLflow Tracking automatically captures all training events: parameters, metrics, code versions, training datasets, user identity, and timestamps. This metadata flows to Unity Catalog for cross-workspace visibility and centralised governance.  Unity Catalog audit logs record all model registry events including version updates, ...

---

## BI / Reporting

### RES.093: What differentiates your approach to AI-driven insights in reporting?...

**Response:** Databricks delivers AI-driven insights through compound AI architecture, not generic LLMs added to traditional BI tools. AI/BI Genie employs specialised agents for planning, SQL generation, and visualisation that learn from your complete data lifecycle including ETL pipelines, Unity Catalog lineage, and query history. This contextual understanding produces more accurate insights than standalone language models.  For AGL's governance requirements, trusted assets provide certified answers marked a...

---

## Data Audit & Monitoring

### RES.055: Explain your real-time audit logging architecture for all data operations....

**Response:** Databricks delivers comprehensive real-time audit logging through Unity Catalog system tables and diagnostic log delivery, supporting AGL's data governance and compliance requirements.  Unity Catalog automatically captures all data operations including table access, metadata queries, permission changes, and data sharing activities. These logs are accessible via SQL queries across all workspaces. This provides AGL's data governance team with visibility for compliance monitoring and forensic analy...

---

### RES.057: Describe your anomaly detection approach for access and usage patterns....

**Response:** With configuration, Databricks can detect anomalies in access and usage patterns through the system.access.audit table, which captures all user activities and data access operations. Security teams build SQL-based detection queries to identify suspicious patterns including repeated failed logins, unusual access times, simultaneous remote sessions, privilege escalation attempts, high-volume data operations, and unauthorised permission changes. These queries integrate with Databricks SQL alerts fo...

---

## Data Catalog

### RES.043: Explain your approach for automated data discovery and cataloging across multi-cloud environments....

**Response:** Unity Catalog provides automated data discovery across AWS, Azure, and GCP through a centralised metadata layer. The system maintains one metastore per region, capturing metadata, lineage, and audit logs automatically as data assets are created or modified.  AGL's existing Data Publishing and Unity Catalog design naturally supports hub-and-spoke discovery where each of the three data platforms (Customer Markets, Energy Markets and Development, Corporate) publishes certified data products to cent...

---

### RES.045: What differentiates your catalog in terms of AI-driven recommendations?...

**Response:** Unity Catalog differentiates through platform-native AI capabilities requiring no additional licensing. AI/BI Genie enables business users to ask natural language questions and receive intelligent follow-up suggestions based on Unity Catalog metadata, usage patterns, and certified metrics. Databricks Assistant provides context-aware recommendations including /findTables for discovering relevant datasets and automated code optimisation. You also have the ability to prompt and add skills to the Da...

---

## Data Classification

### RES.047: Describe your integration strategy with DLP and compliance tools....

**Response:** Databricks integrates with enterprise DLP programmes through three complementary layers that support AGL's data governance requirements across customer, operational, and environmental datasets.  Unity Catalog provides the governance foundation. Automated Data Classification (Public Preview) detects PII across tables, Attribute-Based Access Control enables dynamic row filtering and column masking, and comprehensive audit logs stream to SIEM platforms for centralised monitoring. System tables expo...

---

## Data Cleansing / Enrichment

### RES.086: Describe your ML-driven enrichment capabilities....

**Response:** Databricks delivers ML-driven enrichment through Feature Store and automated change data capture workflows that support AGL's customer analytics and operational intelligence requirements.  Feature Store provides automatic feature lookups with point-in-time correct joins for time-series data, eliminating training-serving skew critical for customer behaviour models and demand forecasting. Stream-static joins enrich incremental data with current slowly-changing dimension values, ensuring customer p...

---

## Data Governance Workflow

### RES.100: Explain your policy-driven governance workflow architecture....

**Response:** Unity Catalog implements policy-driven governance through a hierarchical three-level namespace (catalog.schema.table) where policies cascade automatically from parent to child objects. This inheritance model ensures consistent controls across AGL's expanding data estate without repetitive configuration as renewable energy operations, customer analytics, and grid optimisation workloads scale.  Unity Catalog attribute-based access control (ABAC) enables tag-driven policies that dynamically enforce...

---

## Data Lifecycle Management

### RES.049: Explain your policy-driven approach for data retention and archival....

**Response:** Databricks delivers policy-driven data retention and archival through Delta Lake table properties integrated with Azure storage lifecycle management.  Delta Lake table properties control retention at the table level. The delta.deletedFileRetentionDuration property (default 7 days) determines how long deleted files remain available for time travel queries, supporting audit requirements and operational recovery. The delta.logRetentionDuration property independently controls metadata retention, all...

---

## Data Lineage

### RES.037: Describe your approach for end-to-end lineage tracking across datasets, transformations, and ML mode...

**Response:** Databricks delivers comprehensive end-to-end lineage tracking through Unity Catalog, which automatically captures runtime data lineage across all datasets, transformations, and ML models without additional configuration.  Unity Catalog tracks lineage at both table and column levels across all languages (SQL, Python, R, Scala). It captures relationships between data assets and the notebooks, Lakeflow Jobs, and dashboards that created or consume them. This automated tracking supports AGL's regulat...

---

## Data Observability

### RES.065: Describe your anomaly detection and alerting mechanisms for data pipelines....

**Response:** Databricks provides integrated anomaly detection and alerting for data pipelines, supporting AGL's operational reliability requirements for energy data systems.  Unity Catalog includes automatic data quality monitoring that detects freshness and completeness anomalies by analysing historical commit patterns and row volumes. Deviations from expected patterns trigger alerts, with results logged to queryable system tables for root cause analysis. Lakeflow Jobs can be configured with thresholds with...

---

## Data Orchestration

### RES.034: How do you enable orchestration for cross-domain workflows (data + ML + LLM) seamlessly?...

**Response:** Databricks Lakeflow Jobs provides native orchestration across data engineering, ML, and LLM workloads through a unified control plane with 99.95% uptime SLA. The platform supports diverse task types within a single DAG: Lakeflow Spark Declarative Pipelines for ETL, MLflow for model training and deployment, Agent Bricks for LLM fine-tuning and evaluation, DBSQL for analytics, and AI/BI tasks for semantic model publishing to Power BI. This eliminates the need for separate orchestrators across domains...

---

### RES.035: What capabilities do you have for near-real-time orchestration capabilities & digital-twins?...

**Response:** Databricks provides three integrated capabilities for near-real-time orchestration and digital twins.  Structured Streaming with Real-Time Mode delivers 40-300ms p99 latency for event processing. Lakeflow Spark Declarative Pipelines enable event-driven data flows with stateful stream processing for de-duplication, anomaly detection, and smoothing. The Digital Twin Solution Accelerator combines Zerobus Ingest for direct telemetry ingestion, RDF-based twin modelling, and Lakebase (managed Postgres...

---

### RES.036: How do you enable federated queries across OT systems (SCADA, historian databases) and IT systems fo...

**Response:** Databricks enables federated queries across AGL's OT and IT systems through three complementary patterns that support real-time grid operations while maintaining unified governance.  Lakehouse Federation provides read-only federated queries to operational databases including SQL Server, Oracle, PostgreSQL, and MySQL. Unity Catalog connections push queries down to source systems via JDBC, avoiding data duplication while maintaining unified governance and lineage across OT and IT sources. This sup...

---

## Data Privacy

### RES.016: How do you support privacy-by-design in AI/ML workflows?...

**Response:** Databricks embeds privacy-by-design through Unity Catalog's hierarchical access controls, which enforce governance at catalog, schema, and table levels with row filters, column masks, and attribute-based policies. Data lineage tracks privacy-sensitive fields end-to-end across Delta Lake and Iceberg tables, supporting compliance reporting for AGL's customer and operational data across Retail, Markets, and Corporate domains.  Identity management integrates Microsoft Entra ID for SSO and least-priv...

---

### RES.017: How do you enforce compliance with Australian Privacy Principles (APPs) for customer energy data?...

**Response:** Databricks enforces Australian Privacy Principles compliance through Unity Catalog's centralised governance framework, mapping directly to APP requirements across AGL's customer energy data estate.  For APP 6, 10 and 11 (use, quality and security), Unity Catalog provides fine-grained table, row and column-level policies with attribute-based access controls. These policies define once and secure everywhere, ensuring permissible use of customer energy data and evidencing quality controls. This is ...

---

### RES.018: Do you provide accelerators for secure handling of Personally Identifiable Information in Australian...

**Response:** Yes. Databricks provides Automatic Data Classification in Unity Catalog as a purpose-built accelerator for secure PII handling in Australian utilities.  This capability uses agentic AI to automatically discover, classify and tag PII across your lakehouse, then enforces policy-based protection through attribute-based access controls. Classification runs incrementally as data changes, triggering governance workflows and remediation where needed. The outputs integrate directly with Unity Catalog's ...

---

## Data Protection

### RES.052: How do you implement encryption at rest and in transit using industry standards?...

**Response:** Databricks implements AES-256 encryption for all data at rest across notebooks, workspace storage, managed disks, and query results. Customer-managed keys from Azure Key Vault provide workspace-level control over three encryption layers: managed services including notebooks and queries, DBFS root storage, and temporary compute storage. This envelope encryption approach gives AGL complete key lifecycle control through Azure Key Vault while maintaining dual-layer protection.  All data in transit u...

---

## Data Quality & Profiling

### RES.006: Does your solution offer rule-based and ML-driven data quality checks at scale?...

**Response:** Yes. Databricks provides both rule-based and ML-driven data quality checks at scale.  Rule-based checks use Lakeflow Spark Declarative Pipelines with SQL-based EXPECT constraints. You define quality gates with configurable actions (warn, drop, or fail) on invalid records. Expectation metrics are queryable from pipeline event logs and version-controlled for consistent promotion across environments. This ensures repeatable quality standards as data products move from development to production.  ML...

---

### RES.007: How do you handle real-time data quality checks for streaming pipelines?...

**Response:** Databricks handles real-time data quality through Lakeflow Spark Declarative Pipelines with integrated expectations that validate data as it streams. Quality rules are defined declaratively in SQL or Python within table definitions, checking schema, nullability, referential integrity, and business logic inline with data flow.  Configurable violation actions (fail, drop, or alert) provide flexible handling based on criticality. All validation metrics are automatically captured in queryable event ...

---

### RES.009: Explain how your solution applies ML-driven anomaly detection to improve data quality....

**Response:** Databricks delivers ML-driven anomaly detection through a two-layer approach that strengthens AGL's Business Intelligence value driver by catching quality issues before they impact downstream analytics and reporting.  The first layer is automated ML monitoring at the schema level. Databricks builds per-table models of freshness and completeness patterns across Unity Catalog tables, surfacing health indicators to data consumers and logging detection results for alerting. This runs as a background...

---

### RES.011: What pre-built rules exist for validating NEM wholesale market data and SCADA telemetry?...

**Response:** Databricks does not provide pre-packaged NEM or SCADA validation templates. Instead, it offers configurable frameworks that allow AGL to define domain-specific data quality rules tailored to wholesale market data and telemetry requirements.  Lakeflow SDP expectations enable inline quality rules in SQL or Python to validate value ranges, timestamp integrity, and mandatory fields. Expectations can warn, drop, or fail records on violations and support reusable patterns stored in Delta tables for co...

---

## Data Reconciliation

### RES.080: Describe your anomaly detection approach during reconciliation....

**Response:** Databricks detects anomalies during reconciliation through three core mechanisms that ensure data integrity across AGL's energy systems.  Delta Lake's change data feed tracks row-level changes between source and target tables, creating an audit trail that identifies unexpected data patterns in inserts, updates, and deletes. This provides precise reconciliation at the transaction level.  Data Quality Monitoring uses ML forecasting models trained on historical table metrics such as commit times, r...

---

## Data Transformation

### RES.082: Explain your support for declarative and code-based transformations....

**Response:** Databricks supports both declarative and code-based transformations, enabling AGL's teams to select the optimal approach for their requirements and skill sets.  Declarative Transformations: Lakeflow Spark Declarative Pipelines (SDP) provides a SQL-first framework where you declare desired transformations and the platform handles execution. SQL analysts and data engineers define streaming tables and materialised views using standard CREATE statements without managing infrastructure. The framework...

---

### RES.084: Describe your rollback mechanisms for transformation failures....

**Response:** Databricks provides three-tier rollback mechanisms for transformation failures, ensuring data reliability for AGL's CTAP reporting and operational analytics.  Table-level rollback uses Delta Lake RESTORE commands to revert tables to any previous version by timestamp or version number within the retention period (7 days default, configurable). DESCRIBE HISTORY provides complete audit metadata for identifying the correct recovery point, supporting compliance requirements.  Pipeline-level recovery ...

---

## Data Warehouse

### RES.088: Explain your elastic scaling strategy for compute and storage....

**Response:** Databricks delivers elastic scaling that aligns with AGL's variable energy data workloads and cost optimisation objectives.  For compute, serverless capabilities provide sub-60-second startup times with automatic infrastructure scaling. The platform intelligently scales resources based on real-time demand across notebooks, Lakeflow Jobs, SQL warehouses, and Lakeflow Spark Declarative Pipelines. This eliminates manual capacity planning whilst supporting fluctuating analytical workloads during pea...

---

## Data Wrangling

### RES.104: Describe your version control and reusability features for wrangling steps....

**Response:** Databricks provides version control and reusability for data wrangling through three core capabilities that align with AGL's governance and change management requirements.  1. Databricks Asset Bundles enable infrastructure-as-code where transformation logic, pipelines, and dependencies are defined as version-controlled YAML configurations. Teams write wrangling steps once and deploy across dev-staging-prod environments using parameterised variables for environment-specific settings like catalogs...

---

### RES.105: What ML-driven wrangling suggestions do you offer?...

**Response:** Databricks delivers four ML-driven wrangling capabilities that accelerate AGL's data transformation work.  Databricks Assistant (GA) generates SQL and Python code from natural language. Data engineers describe tasks like "flatten nested JSON meter readings and aggregate by customer" and receive executable code leveraging Unity Catalog schemas. In Edit mode, the Assistant proposes notebook‑wide refactors and updates across multiple cells from a single prompt; you can review and accept or reject e...

---

## DataOps

### RES.061: Explain your approach for automated deployment and version control of data pipelines....

**Response:** Databricks provides a three-layer approach to pipeline deployment and version control, addressing AGL's regulatory compliance and operational excellence requirements.  Version Control Foundation: Databricks Asset Bundles define pipelines as infrastructure-as-code in YAML, stored in Git repositories. This includes Lakeflow Spark Declarative Pipelines definitions, notebooks, job configurations, and cluster specifications. Git integration through Databricks Repos enables standard branch management,...

---

### RES.063: Describe your automated testing and validation strategy for data pipelines....

**Response:** Databricks delivers automated testing across three layers for production pipeline reliability.  Unit and integration testing uses native pytest integration within notebooks and CI/CD pipelines. The workspace testing interface (Public Preview) provides automated test discovery and execution through a dedicated sidebar, validating transformation logic before deployment.  Data quality validation is embedded in Lakeflow Spark Declarative Pipelines through declarative EXPECT clauses. These SQL-based ...

---

## Feature Store

### RES.112: Explain your centralized feature store architecture for ML models....

**Response:** Databricks centralises feature management through Unity Catalog integration. Any Delta table with a primary key can be treated as a feature table, unifying data and feature governance under a single platform. This supports AGL's ML operations across energy forecasting, customer analytics, and operational models with consistent governance.  The Feature Engineering Client enables batch and streaming feature computation using standard Spark pipelines. For real-time applications like demand forecast...

---

### RES.113: How do you ensure versioning and reuse of features across models?...

**Response:** Databricks ensures feature versioning and reuse through Unity Catalog's integration with Delta Lake's native versioning capabilities.  Feature tables are Delta tables that automatically create immutable versions for each modification. Time-travel queries retrieve historical feature values for model reproducibility and compliance auditing. Models logged using FeatureEngineeringClient automatically retain references to exact feature table versions used during training, eliminating version drift be...

---

### RES.114: Describe your support for real-time feature updates....

**Response:** Databricks supports real-time feature updates through streaming pipelines that continuously synchronise features from offline Delta tables to Online Feature Stores, enabling low-latency access for production inference workloads.  Feature tables stored as Delta tables in Unity Catalog leverage Change Data Feed to track row-level changes. When publish_table is called with streaming=True, a continuous pipeline propagates changes from offline storage to the Online Feature Store, typically achieving ...

---

## General Architecture & Strategy

### RES.003: Explain your disaster recovery architecture and RPO/RTO guarantees....

**Response:** Databricks supports active-passive disaster recovery across AGL's multi-region, multicloud topology (Azure australiasoutheast/australiaeast and AWS ap-southeast-2).  Architecture: Deploy paired workspaces using Infrastructure-as-Code (Terraform/CI-CD) to replicate workspace assets. Data replication uses Delta Lake Deep Clone between ADLS Gen2 and S3 for transactional consistency. Unity Catalog provides centralised governance with scripted metadata replication to maintain permissions and lineage ...

---

### RES.004: What differentiates your platform for supporting generative AI and LLM workloads?...

**Response:** Databricks differentiates through enterprise-grade governance and legal protection that eliminates the fragmentation of multi-vendor AI stacks.  Our Multi-AI Indemnity covers all major frontier models (OpenAI, Anthropic, Meta, Google) deployed through Model Serving, protecting AGL from IP claims including judgements, settlements and legal fees. This provides legal certainty for production AI deployments without vendor lock-in.  Unity Catalog delivers centralised governance across all AI assets: ...

---

### RES.005: How do you incorporate automation and AI-driven optimisation in your platform roadmap?...

**Response:** Databricks embeds AI-driven optimisation throughout our platform roadmap, automatically improving performance without increasing operational overhead for AGL's data teams.  Our Predictive Optimisation uses AI to maintain Unity Catalog tables automatically - running OPTIMIZE, VACUUM, and ANALYZE based on usage patterns. Enabled by default since November 2024, production deployments show 70% faster queries over three years through automatic liquid clustering, Bloom filters, and Native IO optimisat...

---

## Identity & Access Management

### RES.020: How do you implement fine-grained, context-aware access control for large-scale data platforms?...

**Response:** Databricks implements fine-grained, context-aware access control through Unity Catalog's hierarchical governance model, integrated with Azure-native identity and networking controls.  Unity Catalog enforces privileges at catalog, schema, table, and column levels, with dynamic row filters and column masks applied at query time. Attribute-based access control (ABAC) policies centralise filter logic across multiple catalogs, reducing administrative overhead while maintaining granular control over s...

---

### RES.023: What innovations do you offer for adaptive authentication based on risk scoring?...

**Response:** Databricks leverages Microsoft Entra ID Protection for adaptive authentication, providing continuous risk scoring against billions of global threat signals. Every sign-in is evaluated in real time for compromised credentials, impossible travel patterns, malicious IP addresses, and anomalous user behaviour.  Based on calculated risk levels, Entra ID Protection dynamically enforces appropriate controls: step-up MFA challenges, mandatory password resets, or access blocks. These policies integrate s...

---

## Industry Differentiators

### RES.132: What industry-specific accelerators do you provide for Australian utilities (e.g., NEM bidding, AEMO...

**Response:** Databricks provides utilities accelerators customisable for NEM market participation and AEMO compliance, validated through Australian deployments.  NEM/AEMO Data Accelerator (in development): We are building an OpenElectricity API integration with enterprise Python SDK for automated NEM market data ingestion. This delivers facility generation and network demand at 5-minute intervals with pre-built ETL functions, Unity Catalog governance, and optimised PySpark schemas aligned to AEMO settlement ...

---

### RES.133: How do you support OT/IT convergence for distributed energy resources and smart grid operations?...

**Response:** Databricks enables OT/IT convergence for distributed energy resources and smart grid operations through unified streaming ingestion, real-time processing, and governed analytics across operational and enterprise domains.  Zerobus Ingest (part of Lakeflow Connect, Public Preview) streams telemetry directly from SCADA systems, smart meters, solar inverters, battery storage, and EV chargers into Unity Catalog Delta tables. It supports industrial protocols including MQTT and OPC-UA, eliminating trad...

---

### RES.134: Do you offer pre-built connectors for SCADA, historian systems, and AEMO APIs?...

**Response:** Databricks does not provide pre-built managed connectors for SCADA, historian systems, or AEMO APIs in Lakeflow Connect. However, proven integration patterns exist for these industrial data sources.  For historian systems, AVEVA CONNECT aggregates AVEVA PI System and OSIsoft PI historian data with native Delta Sharing integration. AVEVA Adapters collect data from third-party historians including Honeywell IP21 and AspenTech PHD via OPC UA servers. Seeq industrial analytics platform offers bi-dir...

---

### RES.135: What compliance certifications and frameworks do you support for Australian energy regulations?...

**Response:** Databricks holds IRAP PROTECTED certification (generally available on AWS Sydney, public preview on Azure), validated by ACSC-accredited assessors. This enables processing of Australian government data at PROTECTED classification level per ISM controls, supporting critical infrastructure operators with government contracts.  For energy data handling, Databricks maintains ISO 27001/27017/27018/27701 for information security and cloud privacy, SOC 2 Type II attestation, PCI-DSS Level 1, and GDPR/C...

---

### RES.136: How do you enable edge-to-cloud integration for real-time grid operations?...

**Response:** Databricks enables bidirectional edge-to-cloud integration supporting AGL's grid modernisation and distributed energy resource orchestration requirements.  Edge-to-cloud ingestion: Lakeflow Connect streams telemetry from substations, smart meters, solar inverters and battery systems directly into Unity Catalog Delta tables. Lightweight forwarding agents deployed at grid edge locations batch and stream operational data including voltage readings, breaker status and generation output with low late...

---

### RES.137: Do you provide accelerators for retail billing analytics and customer churn prediction in the Austra...

**Response:** Yes. Databricks provides configurable Solution Accelerator frameworks for retail billing analytics and customer churn prediction that can be adapted to Australian energy market requirements.  For churn prediction, the platform supports ML frameworks that analyse customer behaviour, consumption patterns, and engagement metrics. These can incorporate NEM pricing dynamics, smart meter interval data, and AER regulatory requirements specific to Australian energy retail.  Billing analytics capabilitie...

---

### RES.139: What capabilities exist for integrating generation asset telemetry with AEMO dispatch and bidding sy...

**Response:** Databricks provides the core capabilities for generation asset telemetry integration with AEMO dispatch and bidding systems, though custom development is required for direct AEMO connectivity.  Real-time telemetry processing: Lakeflow Spark Declarative Pipelines and Structured Streaming ingest generation data from wind, solar, battery storage, and conventional assets via Azure Event Hubs, Kafka, or Zerobus Ingest. This continuous monitoring supports AGL's growing renewable generation and firming...

---

### RES.141: How do you support carbon accounting and renewable energy certificate tracking in compliance with Au...

**Response:** Databricks provides the data governance and analytical foundation to build custom carbon accounting and renewable energy certificate tracking solutions aligned to Australian standards including the NGER Act, AASB S2, and LGC/STC (and VEEC where applicable) schemes. Pre-built compliance templates are not currently available.  Three core capabilities support AGL's decarbonisation reporting requirements. First, Unity Catalog delivers automated data lineage at table and column level, comprehensive a...

---

### RES.142: Do you offer AI-driven forecasting for renewable generation variability and grid balancing?...

**Response:** Yes. Databricks delivers AI-driven forecasting capabilities specifically designed for renewable generation variability and grid balancing, supporting AGL's transition to a lower-emissions future.  The platform provides three core capabilities for managing renewable intermittency:  1. Agent Bricks AutoML Forecasting (Public Preview) serverless time series forecasting with automatic algorithm selection. It supports multivariate forecasting with covariates, enabling you to incorporate weather data, gr...

---

## LLM Application

### RES.124: Explain your support for building custom applications powered by LLMs....

**Response:** Databricks provides end-to-end native capabilities for building, deploying, and governing custom LLM applications across AWS and Azure environments.  For development, Agent Bricks Agent Framework (GA) enables production-quality AI agents in Python using any library including LangChain, LangGraph, LlamaIndex, or custom code, with MLflow 3 integration for lifecycle management and Unity Catalog governance. AI Playground offers no-code prototyping to test models and build tool-calling agents with expor...

---

### RES.126: Describe your deployment strategy for LLM applications across environments....

**Response:** Databricks provides enterprise-grade LLM deployment through three integrated capabilities supporting AGL's governance and operational requirements.  Databricks Asset Bundles enable infrastructure-as-code deployment where LLM agents, model serving endpoints, and pipelines are defined in declarative YAML files with environment-specific configurations. This supports automated promotion across development, staging, and production via CI/CD pipelines, ensuring consistent deployments aligned with AGL'...

---

### RES.127: What pre-trained LLM models or accelerators do you offer for utilities-specific use cases (e.g., out...

**Response:** Databricks does not offer pre-trained LLM models specifically for utilities use cases. Instead, we provide foundation models and tooling that AGL can customise with your operational data.  We provide solution accelerator code templates that demonstrate utilities patterns for dispatch optimisation and grid analytics. These are starting-point frameworks you adapt with AGL's data, not pre-trained models.  Through Agent Bricks, you can access foundation models like Meta Llama 3.3 70B Instruct via Found...

---

## LLM Model Services

### RES.118: Explain your APIs for hosting and serving LLMs securely....

**Response:** Databricks provides secure LLM hosting through Agent Bricks Model Serving with unified REST APIs, MLflow Deployment APIs, and OpenAI-compatible endpoints for real-time and batch inference.  Three deployment options support different use cases: Foundation Model APIs offer pay-per-token pricing for experimentation with preconfigured endpoints for Meta Llama, DBRX, Anthropic Claude, OpenAI GPT, and Google Gemini. Provisioned Throughput delivers production-grade performance guarantees and supports fine...

---

## MLOps

### RES.024: Does your platform provide CI/CD pipelines for ML model deployment and monitoring?...

**Response:** Yes. Databricks provides complete CI/CD pipelines for ML model deployment and monitoring, unified under Unity Catalog governance across your AWS and Azure environments.  MLflow Model Registry enables automated model versioning and promotion across development, staging, and production using Champion/Challenger aliases. Webhook-triggered pipelines integrate with Azure DevOps and GitHub Actions on model registration or stage transitions.  Databricks Asset Bundles define ML pipelines, training jobs,...

---

### RES.025: How do you ensure reproducibility and governance of ML pipelines across environments?...

**Response:** Databricks ensures ML pipeline reproducibility and governance through Unity Catalog's unified lineage framework, tracking complete relationships from source Delta tables through feature engineering, model training, and production deployments in a single auditable system.  Delta Lake time travel provides point-in-time reproducibility by versioning training datasets alongside models. You can recreate exact training conditions from any historical state and audit which data produced specific predict...

---

### RES.026: Describe your automated model drift detection and retraining strategy....

**Response:** Databricks provides automated model drift detection and retraining through Lakehouse Monitoring, MLflow, and Unity Catalog working as an integrated MLOps platform.  Lakehouse Monitoring continuously tracks statistical properties of inference tables, detecting data drift using KS-test, PSI, Chi-square, and other statistical methods. It computes drift scores comparing current distributions against training baselines and generates configurable alerts when thresholds are exceeded.  Automated retrain...

---

### RES.027: How do you integrate explainability and fairness checks into production workflows?...

**Response:** Databricks embeds explainability and fairness checks directly into production ML workflows through three integrated layers.  During development, MLflow automatically logs explainability artifacts including SHAP values and feature importance alongside model versions. Unity Catalog packages these artifacts with models, ensuring reproducible explanations across environments.  Pre-deployment validation gates enforce fairness checks using Fairlearn integration. Models must pass bias assessments befor...

---

### RES.028: What differentiates your approach to scaling MLOps for generative AI models?...

**Response:** Databricks scales GenAI MLOps through unified governance and continuous improvement loops connecting AI systems directly to enterprise data. For AGL, this delivers faster time-to-value for customer-facing AI whilst maintaining rigorous controls for regulated energy operations.  Our differentiation centres on three capabilities. MLflow 3.0 provides GenAI-specific tracing, LLM judge evaluations with human review, and deployment guardrails through Inference Tables and AI Gateway. Daily quality trac...

---

### RES.029: Do you provide pre-built ML pipelines for energy load forecasting and wholesale price prediction?...

**Response:** Yes. Databricks provides AutoML forecasting and solution accelerators purpose-built for energy load and price prediction, deployable on both AWS and Azure.  AutoML forecasting automatically selects optimal algorithms including Prophet, Auto-ARIMA and DeepAR on serverless compute. It generates production-ready notebooks, registers models to Unity Catalog for governance, and provides batch inference and real-time serving options. Solution accelerators deliver ready-to-use blueprints that compress ...

---

### RES.030: How do you support predictive maintenance for generation assets using IoT data?...

**Response:** Databricks enables predictive maintenance for AGL's generation and battery assets by unifying operational technology and IT data streams into a governed lakehouse architecture, reducing unplanned downtime and optimising maintenance schedules across your portfolio.  For AGL's SCADA environment, we support direct integration from Ignition and HiveMQ through Zerobus Ingest patterns, forwarding RabbitMQ messages into Delta Lake tables. Alternatively, high-fidelity historian data from AVEVA CONNECT (...

---

## Master Data Management

### RES.144: What master domains are natively supported (Customer, Asset, Meter/Device, Premise/Site, Product/Tar...

**Response:** Databricks does not provide native master domain models for Customer, Asset, Meter/Device, Premise/Site, Product/Tariff, Supplier, or Employee entities. Instead, the platform enables building custom domain models through Delta Lake tables with fully customisable schemas tailored to AGL’s specific business requirements.  Solution Accelerators provide reference implementations for common patterns including Customer Entity Resolution and Customer 360, reducing development time whilst requiring cust...

---

### RES.145: How do you create and manage the golden record (survivorship, match/merge, trust scores)? Describe y...

**Response:** Databricks creates golden records through Delta Lake MERGE operations with configurable survivorship logic, supporting deterministic, probabilistic, and ML-assisted matching. This is a platform-based approach requiring data engineering rather than packaged MDM tooling.  Golden Record Creation: Delta Lake MERGE INTO operations consolidate duplicates into authoritative records using SQL‑based survivorship rules. CASE WHEN statements and window functions (ROW_NUMBER() OVER (PARTITION BY … ORDER BY ...

---

### RES.149: What embedded DQ capabilities exist (profiling, rules, thresholds, anomaly detection)? Can we write ...

**Response:** Yes, Databricks provides comprehensive embedded data quality capabilities with full support for custom rules reusable across all domains through Unity Catalog governance.  Data Profiling delivers automated statistical analysis with 20+ metrics including nulls, distinct values, quantiles, and distributions. Drift detection uses Chi-squared, Wasserstein distance, PSI, and KS tests. Results are stored in queryable Delta tables with auto-generated Lakeview dashboards for monitoring.  Declarative Qua...

---

### RES.150: Describe stewardship workflows (task routing, bulk edits, approvals, audit trail). Do you support ro...

**Response:** Databricks provides robust building blocks for data stewardship workflows through configuration rather than pre-built stewardship UI, enabling AGL to integrate with existing enterprise systems.  Task Routing and Orchestration: Lakeflow Jobs orchestrates workflows with up to 1,000 tasks per job, supporting conditional logic, task dependencies, and programmatic creation via REST API, CLI, and Terraform. This enables custom stewardship workflows integrated with AGL's approval systems.  Bulk Edit Op...

---

### RES.152: Detail security: RBAC/ABAC, attribute-based masking, consent flags, PII handling, Right‑to‑be‑Forgot...

**Response:** Databricks Unity Catalog delivers enterprise-grade security controls for master data management, supporting Australian Privacy Act and GDPR compliance requirements critical to AGL's customer data governance.  RBAC and ABAC: Unity Catalog implements role-based access control through granular privilege grants at catalog, schema, table, and column levels. Attribute-Based Access Control uses governed tags and policies to dynamically enforce access based on data sensitivity, classification, or busine...

---

### RES.155: How do you handle multi-region deployments, high availability, disaster recovery (RPO/RTO), and sche...

**Response:** Databricks supports multi-region deployments through Unity Catalog's regional metastore architecture, providing data isolation per region. Cross-region access uses Delta Sharing for near real-time, zero-copy data access without replication overhead. For replication requirements, Deep Clone with scheduled jobs enables incremental synchronisation, or Change Data Feed supports streaming updates to regional replicas.  High availability within regions leverages zone-redundant control plane architectu...

---

### RES.156: Do you provide ML-assisted matching and anomaly detection? Can models be trained on our data and gov...

**Response:** Yes. Databricks provides comprehensive ML-assisted anomaly detection and full MLOps governance for models trained on your data.  Anomaly detection is built-in through data profiling. The system analyses historical patterns to automatically assess data freshness and completeness across schemas. Per-table predictive models learn expected commit times and row volumes, flagging tables as unhealthy when commits are late or row counts fall below predicted ranges. Automated root cause analysis identifi...

---

### RES.160: Licensing model (per domain, per record, per environment)?...

**Response:** Databricks uses a consumption-based licensing model, not per domain, record, or environment. You pay only for compute resources used, measured in Databricks Units (DBUs) and billed per-second.  The model operates on three principles:  1. Pay-as-you-go consumption: No per-user fees or upfront costs. Multiple teams, business units, and environments (dev/test/prod) share a unified DBU pool without artificial constraints.  2. Workload-differentiated pricing: Different compute types (Jobs, All-Purpos...

---

### RES.161: Estimated TCO for a 3‑year period for ~20M customer devices and multi-domain governance...

**Response:** TCO estimation for 20 million customer devices with multi-domain governance requires detailed workload profiling aligned to AGL's architecture and CTAP objectives. A comprehensive Enterprise tier deployment would encompass several key cost drivers.  Platform components include streaming data ingestion from smart metres and DER assets using Lakeflow Spark Declarative Pipelines with Delta Lake optimisation. Unity Catalog manages separate business domain catalogs for customer markets, energy market...

---

## Metadata Management

### RES.178: Which source types are supported for automated metadata harvesting (data lakes, Delta/Parquet, wareh...

**Response:** Yes. Unity Catalog supports automated metadata harvesting across all requested source types through runtime-based capture during normal query execution.  Data lakes and Delta/Parquet: Native metadata capture for Delta Lake tables (managed and external), Parquet, CSV, JSON, Avro, ORC, and text files in ADLS Gen2 and S3. Automatic partition discovery supported for external tables.  Warehouses and databases: Lakehouse Federation enables metadata discovery via query federation for MySQL, PostgreSQL,...

---

### RES.179: Do you support Unity Catalog, Azure Fabric, Azure Data Factory, Azure AI Services, Delta Lake, Icebe...

**Response:** Yes. Databricks natively supports all listed capabilities through Unity Catalog, our centralised governance layer managing data and AI assets across Azure and AWS. Databricks is the creator of Unity Catalog, Spark, Delta Lake, MLflow, and is the primary contributor to Iceberg via the Tabular acquisition. We pioneered the Lakehouse category and continue to make significant contributions to the open source community.  Unity Catalog provides the three-level namespace (catalog.schema.table), access ...

---

### RES.180: How do you model business glossary, data products, domains, ownership, criticality, SLAs?...

**Response:** Unity Catalog provides native metadata management for ownership, lineage, and classification, while business glossary and SLA concepts require organisational conventions.  Ownership: Every object (catalogs, schemas, tables, views, volumes, models, functions) has a designated owner with full privileges. Ownership is transferable, with best practice assigning production objects to groups for continuity.  Business semantics: AI-generated and manual documentation on all objects and columns. Automate...

---

### RES.185: Do you store DQ metrics (freshness, completeness, accuracy, anomaly scores) as metadata and tie them...

**Response:** Yes. Databricks stores data quality metrics as metadata in Unity Catalog system tables and links them directly to data assets through catalog, schema, and table identifiers.  Data quality metrics include freshness, completeness, accuracy, and anomaly scores. Anomaly detection automatically monitors tables and stores results in Unity Catalog system tables with documented retention windows (for example, up to 365 days). Quality metrics can be joined with lineage to enable downstream impact analysi...

---

### RES.187: How do users discover assets (faceted search, domains, ratings, endorsements)? Do you provide APIs/S...

**Response:** Yes. Unity Catalog provides comprehensive discovery and programmatic access for AGL's data governance and self-service requirements.  Discovery capabilities:  Unity Catalog Discover delivers faceted search filtering by catalog, schema, owner, modification date, tags, object type, and certification status. Popularity signals rank assets by user interaction frequency. AI-generated comments incorporate organisation-specific terminology into search results, improving discoverability of AGL's energy ...

---

### RES.188: Connectors to developer tools (dbt, Airflow, ADF, Fabric pipelines), BI (Power BI, Tableau), and ML ...

**Response:** Yes. Databricks provides native connectors and validated integrations across developer tools, BI platforms, and ML ecosystems, all governed through Unity Catalog.  Developer tools: Native dbt adapter runs as Lakeflow Jobs tasks with full Unity Catalog integration. Apache Airflow provider package orchestrates jobs via REST API. Azure Data Factory integrates directly via Web activity for notebook and script execution. Microsoft Fabric reads Unity Catalog tables via OneLake shortcuts with credentia...

---

### RES.191: Do you provide automated classification, PII detection, and semantic tagging using AI/ML? Can AI ass...

**Response:** Yes, with configuration required. Databricks provides AI and ML-powered data governance capabilities through Unity Catalog's Data Classification system, supporting AGL's Business Intelligence value driver with automated metadata management.  Automated PII detection and classification: Data Classification (Public Preview) uses an agentic AI system combining pattern recognition, metadata analysis, and LLMs to automatically identify and tag 15+ sensitive data types at the column level. This include...

---

### RES.192: Typical rollout approach, training, adoption KPIs, and stewardship operating model. Migration strate...

**Response:** Databricks Unity Catalog enables a phased, federation-first migration maintaining backwards compatibility whilst establishing centralised governance across AGL's data estate supporting CTAP objectives and AI/BI value drivers.  Migration Strategy: Unity Catalog's Hive Metastore Federation creates a foreign catalog mirroring existing metadata, enabling soft migration where workloads access HMS tables through Unity Catalog's three-level namespace without immediate code changes. This maintains backw...

---

### RES.194: Security & Compliance Addendum: ISO 27001, SOC 2, IRAP/ASD Essential Eight (for AU), data residency,...

**Response:** Databricks meets AGL's regulatory and operational requirements for the Australian energy sector across security, deployment, and support dimensions.  Security and Compliance: Databricks maintains ISO 27001, SOC 2 Type II, and IRAP certifications for Australian regions. Customer-managed keys (CMK) and bring-your-own-key (BYOK) integrate with Azure Key Vault, covering managed services, DBFS root storage, and managed disks. Data residency is enforced through Australian Geos (australiaeast, australi...

---

## Model Execution / Hosting

### RES.110: Describe your deployment strategy for multi-cloud and hybrid environments....

**Response:** Databricks delivers portable, governance-first deployment across cloud and hybrid environments, preventing vendor lock-in while maintaining consistent security and compliance.  Three core capabilities enable this. First, open standards through MLflow packaging. Models deploy unchanged across AWS, Azure, GCP, on-premises Kubernetes, or edge devices. Your models trained on AWS today serve from Azure or hybrid infrastructure tomorrow without refactoring.  Second, unified governance via Unity Catalo...

---

## Model Marketplace

### RES.067: Describe your curated marketplace for pre-trained models and its governance....

**Response:** Databricks Marketplace provides a curated platform for pre-trained AI models with comprehensive Unity Catalog governance. The marketplace offers over 75 models including foundation models from Meta, Mistral, and Google, plus industry-specific models from providers like John Snow Labs, all accessible through a single governed platform.  Unity Catalog delivers unified governance across all models with centralised access control, auditing, lineage tracking, and usage monitoring. This ensures securi...

---

## Model Training

### RES.106: Explain your architecture for distributed training of large-scale models....

**Response:** Databricks distributed training architecture separates orchestration, compute, and data concerns for scalability and flexibility.  For orchestration, TorchDistributor and DeepSpeed integrate with PySpark to support Data Parallel, Fully Sharded Data Parallel, and ZeRO optimisation across single-node multi-GPU and multi-node configurations. Ray on Databricks provides specialised parallel compute for complex workflows, supporting PyTorch, TensorFlow, and HuggingFace with Ray Tune for hyperparameter...

---

### RES.107: How do you monitor and optimize training jobs automatically?...

**Response:** Databricks automates training job monitoring through integrated tooling that reduces manual overhead for AGL's data science teams.  MLflow Autologging captures parameters, metrics, and artefacts automatically from scikit-learn, PyTorch, TensorFlow, XGBoost, and LightGBM without code changes. Every training session becomes an auditable MLflow run, creating complete lineage for model development.  Hyperparameter optimisation runs automatically via Optuna, Ray Tune, and Hyperopt. These frameworks p...

---

## Prompt Engineering / RAG

### RES.128: How do you implement retrieval-augmented generation for enterprise data?...

**Response:** Databricks implements retrieval-augmented generation through a unified architecture where vector indexes, agents, and enterprise data operate under single governance without data duplication.  Vector Search operates directly on Delta tables in Unity Catalog, maintaining your lakehouse as the single source of truth. Delta Sync monitors source tables and incrementally updates vector indexes in real-time as documents change. One-click configuration handles embedding generation and failure recovery,...

---

## Real-Time Data Management

### RES.076: Explain your architecture for real-time ingestion and processing of streaming data....

**Response:** Databricks delivers enterprise streaming architecture built on Apache Spark Structured Streaming with Delta Lake enabling unified batch and streaming operations through ACID transaction guarantees.  Spark Real-Time mode in Public Preview delivers ultra-low latency processing with p99 end-to-end latency as low as 5ms for operational workloads.  The architecture comprises three integrated layers. The ingestion layer uses Auto Loader for incremental file processing from cloud storage with exactly-o...

---

### RES.078: Describe your approach to schema evolution in real-time pipelines....

**Response:** Databricks manages schema evolution in real-time pipelines through three integrated layers that maintain data continuity without pipeline interruptions.  Auto Loader detects schema changes automatically at ingestion. The addNewColumns mode adds new fields, while rescued data columns capture unexpected variations in JSON format for later reconciliation rather than dropping data or failing streams.  Delta Lake enforces schema at write time with explicit evolution controls. The mergeSchema option e...

---

## Reference Data Management

### RES.172: Support for multilingual labels, localization, and industry dictionaries (AEMO/NEM terminology, NAES...

**Response:** Yes, through configuration. Unity Catalog provides the metadata framework to implement multilingual labels and industry-specific terminology, requiring setup rather than pre-loaded dictionaries.  For industry terminology (AEMO/NEM, NAESB, GS1), configure governed tags with industry-specific keys and controlled vocabularies. Tags like nemparticipanttype or gs1gtinlevel enforce standard classifications across data assets, supporting up to 1,000 characters at catalog, schema, table, and column leve...

---

### RES.175: Planned features (rule expressions, policy ties to reference changes, auto-sync to catalogs)....

**Response:** Unity Catalog provides centralised reference data management today through metadata governance, fine-grained access controls, and lineage tracking. SQL-based row and column filters enable policy enforcement through attribute-based access control using data classification tags.  Regarding the three planned features:  Rule expressions: Unity Catalog currently supports SQL-based validation rules. More sophisticated rule expression engines for reference data validation are under evaluation by produc...

---

## Self-service / Ad-hoc Analysis

### RES.094: Explain your support for self-service data exploration with role-based access....

**Response:** Databricks delivers governed self-service data exploration through Unity Catalog, which centralises role-based and attribute-based access controls across all data and AI assets on AWS and Azure.  Users discover data through Catalog Explorer, which surfaces assets they have permissions to access with AI-generated insights and usage patterns. Business users query data using natural language via AI/BI Genie, while technical users leverage SQL Editor and notebooks with integrated Databricks Assistan...

---

