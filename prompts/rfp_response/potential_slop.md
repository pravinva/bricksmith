Product Road Map / Technology Strategy
Product Roadmap
Our Vision: The AGL Energy Unified Intelligence Platform
Our roadmap is not a schedule of features—it is a strategic transformation pathway that directly addresses AGL's critical operational constraints whilst positioning you to lead Australia's energy transition. We are moving AGL from a fragmented, capacity-saturated legacy environment operating at 92% utilisation with fragile deployments to a Unified Intelligence Platform that shifts your technology from passive reporting to active decision-making.

This transformation addresses AGL's most urgent question: "Is the data I'm looking at the most current/accurate?"—and replaces it with a new capability: "What actions should we take based on real-time intelligence?"

Phase 1: Immediate Stabilisation & Foundation (Q1–Q2 2026)
Mission: Eliminate capacity crisis, restore platform stability, and unify multi-cloud governance without costly data migration.

1.1 Eliminating Capacity Saturation & Manual Scaling (Q1 2026)
AGL's Critical Constraint:
"Customer Markets environment operates at 92% average utilisation with peak loads exceeding 3,000 queries per 10-minute period, leaving no headroom for growth. Manual capacity management requires production downtime for scaling operations."

Databricks Solution:

Serverless Compute Auto-Scaling (GA): Elastic infrastructure scales from zero to thousands of concurrent users in under 60 seconds with automatic scale-to-zero during idle periods—eliminating the 92% utilisation ceiling and manual capacity management entirely
Compute-Storage Separation: Independent scaling enables AGL to handle peak query loads 10-100x higher (3,000 queries → 30,000+ queries per 10 minutes) without storage constraints or production downtime
Intelligent Workload Management: ML-powered query routing and prioritisation eliminates resource contention, ensuring business-critical Collections queries receive priority over exploratory analytics
Quantified Transformation:

From: 92% utilisation, manual scaling, production downtime
To: Elastic 0-100% utilisation, automatic scaling, zero downtime
Business Impact: Eliminates "access is unstable, or pipelines fail regularly" operational fragility
AGL-Specific Use Case: Collections team can run real-time payment risk queries during peak demand periods without impacting Energy Markets trading analytics—impossible on current shared Synapse infrastructure.

1.2 Unifying Multi-Cloud Governance Without Migration (Q1 2026)
AGL's Critical Constraint:
"Multi-cloud fragmentation between Azure and AWS prevents realisation of platform benefits from strategic investments including Kaluza acquisition (AWS) and Salesforce deployment, which remain siloed from corporate systems on Azure."

Databricks Solution:

Unity Catalog Cross-Cloud Governance (GA): Single governance layer across AWS (Kaluza, Salesforce) and Azure (operational assets) enabling unified RBAC/ABAC, lineage, and audit logging—without physical data migration
Lakehouse Federation: Direct queries from Azure Databricks to AWS S3 Kaluza billing data and Salesforce CRM without ETL pipelines or data duplication, eliminating costly cross-cloud egress fees
Delta Sharing Protocol: Zero-copy data exchange between AWS and Azure environments maintains single source of truth whilst enabling governed collaboration
Quantified Transformation:

From: Siloed AWS (Kaluza) + Azure (Corporate) with duplicate ETL pipelines
To: Unified governance across clouds with direct federated queries
Cost Impact: Eliminates cross-cloud data replication costs estimated at 15-30% of current cloud spend
AGL-Specific Use Case: Customer 360 analytics combining Kaluza billing data (AWS), Salesforce service interactions (AWS), and Azure operational data in a single governed query—answering "How can I link data back to source?" across cloud boundaries.

1.3 Building the Single Source of Truth (Q1–Q2 2026)
AGL's Critical Constraint:
"With over 15,200 database objects spanning Customer Markets, Energy Markets, and Corporate systems, the platform lacks a single source of truth. This fragmentation has created massive report sprawl with duplicated and inconsistent reporting artefacts, fundamentally eroding business confidence."

Databricks Solution:

Medallion Architecture Migration: Transform 15,200+ fragmented objects into streamlined Bronze → Silver → Gold layers with automated data lineage tracking provenance from source systems through every transformation
Unity Catalog Automated Lineage: Every query, transformation, and report automatically tracked at table and column level, answering "Being able to link data back to source and know its lineage can be challenging" through visual lineage graphs and SQL-queryable metadata
Lakebridge Automated Migration: Assessment and conversion tool analyses 3,742 simple objects, 2,650 medium objects, and 60 complex/very complex objects from Synapse, generating automated migration plans with reconciliation validation ensuring data integrity
Quantified Transformation:

From: 15,200+ fragmented objects, no automated lineage, conflicting metrics
To: Governed medallion layers with end-to-end lineage, certified golden datasets
Time Impact: Reduces data discovery from hours to seconds, lineage tracing from manual investigation to instant visual navigation
AGL-Specific Use Case: When business stakeholders ask "Is this the most current/accurate data?", data stewards provide instant lineage proof showing exactly which source systems, transformation logic, and refresh timestamps produced the metric—restoring business confidence in data quality.

1.4 Enabling Real-Time Analytics (Q2 2026)
AGL's Critical Constraint:
"Business units require near-real-time capabilities: 'For Collections, they require more frequent data than overnight batch. Real-time data is a key requirement.' Current multi-hop architecture (SAP HANA → ADF → Databricks → Parquet → Synapse) introduces latency incompatible with real-time requirements."

Databricks Solution:

Real-Time Streaming Mode (Public Preview → GA Q2): Replace 4-hop batch architecture with direct streaming ingestion achieving sub-second latency (40-300ms p99) for operational workloads
Lakebase OLTP (Public Preview → GA Q2 2026): Managed PostgreSQL-compatible database with single-digit millisecond query latency for customer-facing applications requiring transactional consistency
Managed Synced Tables: Continuous synchronisation from analytical Delta Lake to operational Lakebase, enabling real-time dashboards whilst maintaining historical context for compliance reporting
Quantified Transformation:

From: Overnight batch (8-12 hour latency), 4-hop architecture
To: Sub-second streaming (<1 second latency), direct ingestion
Business Impact: Collections team identifies at-risk customers in real-time rather than acting on stale overnight data, improving recovery rates and customer outcomes
AGL-Specific Use Case: Collections Optimizer App (Databricks App with Lakebase backend) provides Collections agents with real-time payment risk scores, recommended actions, and customer vulnerability indicators updated continuously as payment events occur—impossible with current overnight batch architecture.

Phase 2: Intelligence Activation & Self-Service (Q3–Q4 2026)
Mission: Transform from passive reporting to active intelligence, democratise data access, and deploy production AI applications.

2.1 Moving Beyond Dashboards: The Application Layer (Q3 2026)
AGL's Strategic Requirement:
"We aren't just building a data warehouse for passive reporting; we are enabling an App Layer that deploys intelligent applications directly within business processes."

Databricks Solution:

Agent Bricks Agent Bricks (Beta → GA Q2 2026): Pre-built agent patterns enabling rapid deployment of intelligent applications including:

Knowledge Assistant: RAG-powered chatbot answering operational questions from technical manuals, regulatory documents, and historical incident reports
Multi-Agent Supervisor: Orchestrates complex workflows across multiple data domains (customer + asset + market data) with automated decision-making
Databricks Apps (GA): Deploy custom Python/Node.js applications with Streamlit, Gradio, or React UIs on serverless compute with built-in OAuth, enabling business-specific applications such as:

VPP Dispatch Optimizer: Real-time orchestration of 1,487 MW decentralised assets based on wholesale prices, grid constraints, and battery state-of-charge
Outage Impact Predictor: Correlates SCADA telemetry from Liddell/Bayswater with customer location data to proactively notify affected customers before outages occur
Vulnerable Customer Protector: Automated detection and routing of customers experiencing vulnerability indicators to specialist support teams
Quantified Transformation:

From: Static Power BI dashboards with overnight refresh
To: Live applications embedded in business workflows with second-level latency
Strategic Impact: Technology shifts from reporter to actor, directly supporting "technology, digitisation and AI at the core" strategic pillar
Game-Changer Moment:
Anthropic Claude 3.5 Sonnet In-Region Australia (GA January 21, 2026) enables world-class AI for sensitive customer interactions—automating risk hedging analysis, personalising offers for vulnerable customers, and interpreting complex regulatory documents—whilst ensuring data never leaves Australian shores. This provides legal certainty and customer trust essential for regulated energy operations.

2.2 Solving Data Discovery & Metadata Challenges (Q3 2026)
AGL's Critical Constraint:
"Business users struggle with fundamental questions: 'I don't know where data is, how do I access it?', 'It's hard to get access to the data I need', and 'How can I understand the data I'm looking at?'"

Databricks Solution:

AI-Powered Semantic Search (GA Q3): Natural language data discovery through Databricks Assistant—business users ask "Show me customer vulnerability data" and receive instant results with automatic governance enforcement ensuring only authorised datasets appear
Unity Catalog Discover Experience (GA Q3): Curated marketplace of certified data products organised by business domain (Customer Analytics, Generation Forecasting, Retail Operations) with AI-generated recommendations surfacing high-value assets
Automated Data Classification: Agentic AI scans and tags PII, customer identifiers, and sensitive fields within 24 hours of table creation, enabling self-service access with automatic privacy protection
Quantified Transformation:

From: Tribal knowledge, manual access requests, hours/days to find data
To: AI-powered discovery, self-service access requests, seconds to find data
Productivity Impact: Estimated 60-80% reduction in time-to-first-insight for business analysts
AGL-Specific Use Case: Marketing analyst searching for "customers likely to adopt solar" receives instant discovery of relevant datasets from Customer Markets (engagement history), Energy Markets (consumption patterns), and Corporate (demographic data)—with automatic access request workflow to asset owners, eliminating manual IT tickets.

Phase 3: Autonomous Operations & AI-Native Business (2027+)
Mission: Deploy autonomous AI agents for operational excellence, enable algorithmic asset dispatch, and transform customer experience through personalisation at scale.

3.1 Algorithmic Battery Dispatch & VPP Orchestration (Q1 2027)
AGL's Strategic Requirement:
"Current platforms prevent algorithmic battery dispatch and optimisation, renewable energy forecasting, and VPP orchestration across 1,487 MW of decentralised assets—blocking operational AI capabilities essential for 12 GW renewable capacity transition by 2035."

Databricks Solution:

Multi-Agent Supervisor for VPP Dispatch (GA Q1 2027): Autonomous AI agents coordinating dispatch decisions across distributed solar, battery, and EV charging assets based on:

Real-time wholesale NEM pricing signals (5-minute intervals)
Grid frequency regulation requirements from AEMO
Weather forecasts and renewable generation predictions
Customer preferences and contractual obligations
Digital Twin Architecture: Real-time asset state serving via Lakebase (sub-10ms latency) maintains virtual representations of 1,487 MW portfolio, enabling simulation and optimisation before executing dispatch commands

Closed-Loop Control: Databricks Apps write optimised dispatch schedules directly to SCADA systems and battery management platforms, creating edge-to-cloud-to-edge control loops

Quantified Transformation:

From: Manual dispatch decisions, batch optimisation (overnight)
To: Autonomous AI dispatch, real-time optimisation (5-minute cycles)
Financial Impact: Estimated 15-25% improvement in VPP revenue through optimal market participation and ancillary services bidding
AGL-Specific Use Case: VPP Dispatch Agent receives AEMO frequency regulation signal indicating grid instability → autonomously queries 1,487 MW asset portfolio availability → calculates optimal dispatch schedule across batteries, demand response, and peaker plants → executes bid into FCAS market within 5-minute window—all without human intervention.

3.2 Customer Experience & Personalisation at Scale (Q2–Q3 2027)
AGL's Strategic Requirement:
"Support NPS +20 targets whilst serving 4.56 million customers experiencing electrification transition, managing vulnerable customer obligations, and maintaining regulatory compliance."

Databricks Solution:

Churn Prediction with Fairness Checks (GA Q2 2027): ML models identifying at-risk customers whilst ensuring equitable treatment across demographic groups—supporting both commercial objectives and vulnerable customer protection obligations
Dynamic Pricing Optimisation Engine: Real-time price elasticity models integrated with 15-minute smart meter intervals and renewable generation forecasts, enabling time-of-use tariffs that balance customer value with grid stability
Federated Learning for Privacy-Preserving Personalisation (Beta Q3 2027): Train models on customer energy usage patterns without centralising sensitive data—enabling personalisation whilst maintaining Australian Privacy Principles compliance
Quantified Transformation:

From: Segment-based batch campaigns, overnight targeting
To: Individual-level personalisation, real-time engagement
Customer Impact: Estimated 20-30% improvement in offer relevance, directly supporting NPS +20 targets
AGL-Specific Use Case: Customer receives personalised solar + battery offer automatically generated by AI agent considering their actual consumption patterns, roof orientation (GIS data), financial capacity indicators, and grid capacity constraints—delivered via preferred channel (email/app) at optimal engagement time predicted by behavioural models.

3.3 Compliance Automation & Climate Transparency (Ongoing 2026–2027)
AGL's Critical Constraint:
"FY26 mandatory climate reporting under AASB S2 requires auditable lineage for 79 climate metrics across Australia's largest corporate emitter (30.7 MtCO₂e). Fragmented governance creates compliance risk."

Databricks Solution:

Automated ESG Reporting Framework (Q3 2026): Pre-built templates for TCFD, SASB, GRI, and AASB S2 with Unity Catalog lineage ensuring every metric traces to source operational systems through complete transformation pipeline
SAP Green Ledger Integration (Q4 2026): Double-entry carbon accounting integrated with financial systems, linking emissions to business activities with full auditability
Scope 3 Data Collaboration via Delta Sharing (Q2 2027): Secure emissions data exchange with suppliers and customers without data replication, building stakeholder trust through transparency
Quantified Transformation:

From: Manual compliance aggregation, 6-8 weeks to produce reports, high audit risk
To: Automated ESG reporting, 48 hours to produce auditable reports, lineage-backed compliance
Risk Reduction: Transforms high-risk manual compliance exercise into automated, auditable process with complete data provenance
AGL-Specific Use Case: FY26 AASB S2 annual report generation: Unity Catalog automatically aggregates 79 climate metrics from 30+ operational source systems (generation assets, retail operations, supply chain) → applies transformation logic with version-controlled calculations → produces audit-ready report with complete lineage documentation showing exactly which Liddell/Bayswater emissions measurements, renewable generation data, and Scope 3 estimates contributed to each metric.

Phase 4: Continuous Evolution & Platform Intelligence (2027–2028)
Mission: Self-optimising platform reducing operational overhead whilst continuously improving performance and cost efficiency.

4.1 AI-Driven Platform Optimisation (Continuous)
AGL's Operational Requirement:
"Platform becomes more efficient over time without manual tuning, freeing teams to focus on business insights rather than infrastructure management."

Databricks Solution:

Predictive Optimisation (GA, Enabled by Default): AI automatically manages table maintenance (OPTIMIZE, VACUUM, ANALYZE) based on usage patterns—70% faster queries over 3 years without manual intervention
Adaptive Query Execution: Runtime query re-optimisation delivering 31% faster ETL workloads year-over-year and 73% faster BI queries over 2 years through automatic join strategy switching and partition coalescing
Photon Engine Enhancements: Vectorised query execution improvements delivering 25% additional performance gains (June 2025 release) automatically applied to existing workloads without version upgrades
Quantified Transformation:

From: Manual performance tuning, degrading query performance over time
To: Self-optimising platform, automatically improving performance (70% faster over 3 years)
Operational Impact: Eliminates manual tuning overhead, redirects 2-3 FTE from infrastructure management to business value delivery
Roadmap Summary: Phased Value Delivery
Phase	Timeline	Core Objective	AGL Business Impact
1: Stabilisation	Q1–Q2 2026	Eliminate capacity crisis, unify governance, build SSOT	Platform stability restored, multi-cloud unified, data trust rebuilt
2: Intelligence	Q3–Q4 2026	Enable self-service, deploy real-time analytics, activate AI/ML	"Where is my data?" → instant discovery; overnight batch → real-time insights
3: Automation	2027	Deploy autonomous agents, algorithmic dispatch, personalisation	Reporter → Actor; VPP orchestration; NPS +20 enablement
4: Evolution	2027–2028	Self-optimising platform, continuous improvement	Reducing operational overhead whilst improving performance (70% faster)



Artificial Intelligence (AI) Strategy
Current Capability: AI Embedded at Three Operational Layers
Unlike legacy platforms where AI is an add-on, Databricks embeds AI natively across data operations, analytics, and custom applications—directly addressing AGL's question: "Is there a means to profile or experiment?"

Layer 1: AI for Data Operations (Operational AI)
Solving: "Manual, offline processes for routine operations create friction incompatible with real-time requirements."

Current Capabilities:

Predictive Optimisation: AI manages table maintenance automatically—running OPTIMIZE, VACUUM, and ANALYZE based on usage patterns. Over 2,400 customers achieved up to 20x query performance improvements and 2x storage cost reductions without manual tuning
Intelligent Workload Management: ML predicts query resource requirements, dynamically scales compute, and prioritises short-running queries—eliminating the resource contention between data loads, modelling, and queries currently degrading performance
Automated Data Classification: Agentic AI scans and tags PII across lakehouse within 24 hours, enabling automatic policy enforcement—solving "I don't know where data is" through intelligent metadata management
AGL Value: Eliminates manual infrastructure management overhead, freeing 2-3 data engineers to focus on business value rather than performance tuning.

Layer 2: AI for Analytics & Insights (Embedded AI)
Solving: "How can I understand the data I'm looking at?" and democratising access for 100+ monthly active users across Data Analysts, Engineers, and Data Scientists.

Current Capabilities:

AI/BI Genie (GA): Natural language to SQL conversion—business users ask "Show me customers at risk of churn in Melbourne metro" and receive instant visualisations without technical knowledge
Databricks Assistant: Context-aware code generation leveraging Unity Catalog metadata, query history, and AGL-specific terminology—accelerating data engineer productivity by 40-60% through automated code suggestions
ai_forecast() SQL Function: Multivariate time-series forecasting directly in SQL for demand prediction, renewable generation variability, and grid balancing—enabling predictive analytics for business analysts without Python/data science expertise
AGL Value: Democratises AI/ML capabilities beyond data science team to 100+ business analysts and domain experts, accelerating time-to-insight from weeks to hours.

Layer 3: AI for Custom Applications (Generative AI)
Solving: "Current platforms prevent algorithmic battery dispatch, renewable forecasting, and VPP orchestration—blocking 'technology, digitisation and AI at the core' strategic pillar."

Current Capabilities:

Agent Bricks Agent Framework (GA): Production-quality RAG applications and multi-agent systems with unified governance—enabling:

Battery dispatch algorithms autonomously optimising charge/discharge cycles based on wholesale prices and grid signals
Customer service automation handling billing enquiries and outage notifications with contextual awareness
Regulatory compliance extraction from technical documents and legislation for AEMO reporting
Foundation Model APIs with Provisioned Throughput: Sub-50ms inference for customer-facing applications with guaranteed performance SLAs—supporting real-time Collections use cases and operational decision-making

MLflow 3 with GenAI Tracing: Complete lineage from prompts to responses with automated evaluation—ensuring AI applications meet regulatory compliance and customer trust standards required for vulnerable customer interactions

AGL Value: Enables production AI applications previously impossible on legacy platforms, directly supporting renewable transition and customer experience transformation.

AI Features in Development: Strategic Capabilities for Energy Operations
Q2 2026: Multi-Modal AI for Operational Intelligence
Business Challenge Addressed:
"How do we extract operational intelligence from drone imagery, field inspection photos, and regulatory PDF documents currently trapped in unstructured formats?"

Databricks Capability:

Vision AI for Asset Inspection: Process drone imagery and field photos to detect equipment degradation across Liddell/Bayswater generation assets—enabling predictive maintenance that reduces unplanned outages
Document AI for Regulatory Compliance (ai_parse_document): Automated extraction of structured data from AEMO regulatory filings, AASB S2 reporting templates, and NEM rule changes—reducing manual effort for 79 climate metrics tracking
Value to AGL: Transforms unstructured operational data (images, documents) representing 60-70% of total enterprise data into actionable insights, accelerating compliance reporting and asset reliability.

Q3 2026: Autonomous AI Agents for Energy Operations
Business Challenge Addressed:
"I want to develop a model to create a new data set - how do I do this?" Current platforms lack AI/ML experimentation capabilities accessible to business users.

Databricks Capability:

Data Science Agent (Beta → GA Q3 2026): Multi-step workflow automation from a single natural language prompt—users request "Perform exploratory analysis on smart meter data and identify anomalous consumption patterns" and agent:

Plans analysis steps (data profiling, outlier detection, statistical testing)
Generates executable code (Python/SQL)
Executes transformations on serverless compute
Interprets results with business context
Fixes errors automatically through iterative refinement
Enhanced Agent Evaluation with RLHF: Subject matter expert feedback loops for VPP orchestration agents—continuously improving dispatch algorithms based on actual grid performance and market outcomes

Value to AGL: Democratises AI/ML capabilities to 100+ business users, enabling "Is there a means to profile or experiment?" through natural language instruction rather than requiring Python/data science expertise.

AGL-Specific Use Case: Energy Markets analyst prompts: "Build a model predicting wholesale price spikes based on renewable generation forecasts and grid constraints" → Data Science Agent automatically generates feature engineering pipeline, trains multiple models (AutoML), evaluates performance, and deploys best model to production—compressing 6-week data science project to 6 hours.

Q4 2026: Real-Time Anomaly Detection & Predictive Analytics
Business Challenge Addressed:
"Resource contention creates unpredictable query performance and data quality issues that undermine business confidence. How do we shift from reactive firefighting to proactive operational excellence?"

Databricks Capability:

Lakehouse Monitoring Anomaly Detection (GA Q4 2026): Automated ML models detecting data quality issues, sensor drift, and operational anomalies across smart meter streams and SCADA telemetry—preventing data quality erosion before impacting business stakeholders
Streaming Anomaly Detection: Real-time pattern recognition on energy consumption, grid frequency, and voltage events—enabling proactive grid management and outage prevention
Explainable AI for Forecasting: SHAP value integration for renewable generation and demand forecasts—providing transparency required for operational trust when automated decisions impact grid stability
Value to AGL: Shifts from reactive issue resolution (mean time to detect: hours/days) to proactive prevention (mean time to detect: seconds/minutes), improving platform reliability and business confidence.

AGL-Specific Use Case: Grid Frequency Anomaly Detector monitors SCADA telemetry from Liddell/Bayswater in real-time → detects abnormal frequency deviation pattern (ML model trained on historical grid events) → automatically triggers alert to control room with predicted fault location and recommended corrective action → prevents cascading failure that would have caused widespread customer outages.

2027: Privacy-Preserving Customer Analytics & Electrification
Business Challenge Addressed:
"How do we drive electrification adoption (heat pumps, EVs, solar+battery) across 4.56 million customers whilst maintaining privacy obligations and vulnerable customer protections?"

Databricks Capability:

Federated Learning for Privacy-Preserving Analytics (Beta 2027): Train models on customer energy usage patterns without centralising sensitive data—enabling personalisation whilst maintaining Australian Privacy Principles compliance
Real-Time Pricing Engines with Fairness Constraints: Sub-second price optimisation integrating wholesale market signals, grid constraints, and customer preferences whilst ensuring equitable treatment across protected demographic groups
Behavioural AI for Demand Response: Predictive models identifying price-responsive customers and optimal engagement timing for load-shifting programs supporting grid stability during renewable intermittency
Value to AGL: Enables data-driven customer engagement that balances commercial objectives (retention, upsell) with regulatory obligations (privacy, vulnerability protection), supporting NPS +20 targets whilst maintaining customer trust across 4.56 million relationships.

AGL-Specific Use Case: Electrification Advisor Agent analyses customer's historical consumption, roof orientation, financial capacity, and grid capacity constraints → recommends personalised solar+battery+EV package → simulates bill savings under time-of-use tariffs → generates pre-approved financing offer → delivers via preferred channel—all automated whilst respecting privacy and vulnerability indicators.

Adaptability to Industry Changes
Proven Track Record: Three Strategic Pivots Mirroring AGL's Transformation
Our technology and organisation have demonstrably adapted to energy sector evolution through strategic investments directly aligned with AGL's current transformation journey.

Adaptation 1: Renewable Integration & Operational Intelligence (2023–2025)
Industry Change:
Transition from centralised fossil generation (predictable baseload) to distributed renewable energy (intermittent, requiring real-time orchestration and forecasting).

Databricks Organisational Response:

Zerobus Ingest Launch (Public Preview 2025): Direct SCADA and IoT telemetry ingestion with sub-5-second latency—purpose-built for real-time grid monitoring as utilities transition to distributed generation
AVEVA CONNECT Partnership: Native OSI PI historian integration via Delta Sharing—enabling 50+ global utilities to unify OT/IT analytics without replacing operational systems
Digital Twin Solution Accelerator (2025): RDF-based asset modelling with real-time state serving for VPP orchestration and battery dispatch optimisation—validated through deployments with major utilities managing distributed energy resources
Technology Evolution:

From: Batch-oriented data warehouse architectures assuming stable generation profiles
To: Real-time streaming platforms handling intermittent renewable generation and bidirectional grid flows from customer-sited assets
AGL Relevance:
These capabilities directly enable AGL's transition to 12 GW renewable capacity by 2035, providing the real-time operational intelligence required for grid balancing, VPP orchestration across 1,487 MW, and renewable generation forecasting that optimises NEM market participation.

Customer Validation:

Hydro-Québec: Analyses 4.5 million meters with 1 trillion+ data points for demand forecasting
DTE Energy: Real-time grid reliability analytics for 2.3 million customers
Octopus Energy: Smart meter analytics enabling dynamic pricing and behavioural programs
Adaptation 2: Data Sovereignty & Regulatory Compliance (2024–2026)
Industry Change:
Escalating regulatory requirements including mandatory climate reporting (AASB S2), Australian Privacy Principles enforcement, SOCI Act critical infrastructure protection, and customer demand for data sovereignty.

Databricks Organisational Response:

Anthropic Claude Australia Region Launch (January 21, 2026): Strategic partnership ensuring world-class LLM capabilities available in-region with data sovereignty guarantees—directly responding to utilities' need for sovereign AI
IRAP PROTECTED Certification (Public Preview Azure, GA AWS Sydney): ACSC-validated security controls meeting government and critical infrastructure standards—demonstrating commitment to Australian regulatory landscape
Automated Data Classification with ABAC (Public Preview 2025): AI-powered PII detection and policy-based protection within 24 hours—enabling Australian Privacy Principles compliance at scale across millions of customer records
Technology Evolution:

From: Generic global cloud platforms with limited sovereignty guarantees
To: Region-specific deployments with in-country AI processing, IRAP certification, and automated privacy controls
AGL Relevance:
Directly addresses FY26 mandatory climate reporting with auditable lineage for 79 metrics, whilst enabling sovereign AI capabilities that maintain customer trust and regulatory compliance for sensitive use cases (vulnerable customer interactions, payment risk assessment, personalised offers).

Regulatory Validation:

AEMO publicly endorses Databricks as pivotal in their data strategic roadmap, with Unity Catalog facilitating Data Centre of Excellence
Alinta Energy, Energy Australia, Essential Energy, AusNet Services trust Databricks for compliance-sensitive workloads
Adaptation 3: AI/ML Democratisation & Operational Excellence (2024–2026)
Industry Change:
Energy sector shift from descriptive analytics (what happened?) to predictive/prescriptive AI (what will happen? what should we do?) for asset optimisation, customer engagement, and market participation.

Databricks Organisational Response:

Agent Bricks Agent Framework (GA 2025): Production-quality AI agents with unified governance—transforming from "Is there a means to experiment?" to one-click deployment of governed AI applications
AI/BI Genie (GA 2025): Natural language analytics democratising insights for non-technical business users—addressing "How can I understand the data I'm looking at?" across decentralised teams
MLflow 3 with GenAI (2025): End-to-end AI lifecycle management from experimentation to production monitoring—enabling responsible AI deployment at enterprise scale with complete auditability
Technology Evolution:

From: AI/ML as specialist data science tools requiring dedicated teams and infrastructure
To: AI embedded throughout platform, accessible via natural language, governed through unified framework
AGL Relevance:
Enables AGL's "technology, digitisation and AI at the core" strategic pillar by democratising AI/ML capabilities across 100+ business users, accelerating time-to-value for battery dispatch, customer personalisation, and operational optimisation.

Enterprise Validation:

Over 10,000 enterprises using Databricks for production AI/ML workloads
600+ customers deploying Agent Bricks Agent Framework in production
Fortune 500 utilities achieving 40% reduction in time-to-business-outcomes through AI democratisation
Future Industry Alignment
Strategic Foresight: Four Energy Sector Transformations Shaping Our Roadmap
Our product strategy anticipates four major energy sector transformations directly aligned with AGL's 2035 renewable transition roadmap and regulatory environment.

Transformation 1: Distributed Energy Resource (DER) Orchestration (2026–2028)
Market Driver:
Australian Energy Market Commission mandates real-time consumer energy data access from January 1, 2028, whilst behind-the-meter solar, batteries, and EVs create bidirectional grid complexity requiring millisecond-level coordination across millions of endpoints.

Databricks Strategic Investment:

Enhanced Time-Series Analytics (Q3 2026): Sub-second streaming analytics for real-time DER dispatch optimisation across millions of customer-sited assets
Federated Learning Roadmap (2027): Privacy-preserving ML enabling VPP coordination without centralising sensitive customer data—balancing optimisation with privacy obligations
Edge-to-Cloud Integration (Continuous): Lightweight forwarding agents streaming telemetry from substations, inverters, and batteries with closed-loop control where cloud-computed insights flow back to field devices
AGL Strategic Alignment:
Enables orchestration of 1,487 MW+ decentralised assets as virtual power plants, optimising dispatch across solar, battery, and EV charging whilst maintaining customer privacy and grid stability—directly supporting renewable capacity growth and firming strategy under CTAP.

Competitive Differentiation:
Unlike competitors requiring separate IoT platforms and analytics stacks, Databricks provides unified governance from edge sensors through AI models to automated dispatch commands—eliminating integration complexity whilst maintaining compliance.

Transformation 2: Climate Transparency & Emissions Accountability (2026–2030)
Market Driver:
Mandatory AASB S2 reporting (FY26), Scope 3 emissions accountability expanding across value chains, and investor/customer demand for transparent decarbonisation pathways validated through auditable data.

Databricks Strategic Investment:

SAP Green Ledger Integration (Q4 2026): Double-entry carbon accounting integrated with financial systems—linking emissions to business activities with auditability meeting external audit standards
Automated ESG Reporting Templates (Q3 2026): Pre-built TCFD, SASB, GRI, and AASB S2 frameworks with Unity Catalog lineage ensuring data provenance for regulatory scrutiny
Scope 3 Data Collaboration (Q2 2027): Delta Sharing enabling secure emissions data exchange with suppliers and customers without data replication—building trust through transparency whilst protecting commercial sensitivity
AGL Strategic Alignment:
De-risks FY26 compliance for 79 climate metrics across 30.7 MtCO₂e emissions portfolio, whilst building stakeholder trust through transparent, auditable decarbonisation progress tracking aligned to Climate Transition Action Plan targets and investor commitments.

Operational Impact:

From: Manual compliance aggregation (6-8 weeks, high audit risk)
To: Automated auditable reporting (48 hours, lineage-backed compliance)
Cost Avoidance: Eliminates estimated $2-5M annual compliance overhead through automation
Transformation 3: Customer Energy Management & Electrification (2027–2030)
Market Driver:
Residential and commercial electrification driving 2-3x electricity demand growth by 2035, requiring sophisticated demand response, dynamic pricing, and customer engagement platforms balancing grid stability with customer value.

Databricks Strategic Investment:

Behavioural AI for Demand Response (Q2 2027): Predictive models identifying price-responsive customers and optimal engagement timing for load-shifting programs
Real-Time Pricing Engines (Q3 2027): Sub-second price optimisation integrating wholesale market signals, grid constraints, and customer preferences—enabling time-of-use tariffs that help customers manage costs whilst maintaining grid stability
Personalisation at Scale with Fairness (2027): AI-driven customer segmentation and offer optimisation across millions of households—supporting NPS +20 targets whilst ensuring equitable treatment
AGL Strategic Alignment:
Transforms 4.56 million customer relationships from transactional to collaborative, enabling electrification adoption (heat pumps, EVs, solar+battery) whilst maintaining grid stability and customer satisfaction during energy transition.

Customer Experience Impact:

Personalised solar offers based on actual consumption, roof orientation, financial capacity
Proactive outage notifications correlating grid events with customer locations
Automated vulnerability detection routing at-risk customers to specialist support
Transformation 4: Grid Resilience & Cyber-Physical Security (Ongoing)
Market Driver:
SOCI Act expanding critical infrastructure obligations, increasing cyber threats to OT/IT converged environments, and extreme weather events requiring resilient operations during grid disturbances.

Databricks Strategic Investment:

Enhanced Security Monitoring (GA): CIS Level 1 hardened images, behaviour-based malware detection, and file integrity monitoring—protecting OT/IT converged environments from cyber threats
Multi-Region Disaster Recovery (Continuous Enhancement): Active-passive DR across Azure australiasoutheast/australiaeast with automated failover achieving <1-hour RTO for critical trading and customer systems
Anomaly Detection for Cyber-Physical Threats (Q4 2026): ML models detecting unusual SCADA access patterns, sensor manipulation, and coordinated attacks across grid infrastructure
AGL Strategic Alignment:
Protects critical generation and distribution infrastructure whilst maintaining operational continuity during cyber incidents or natural disasters—essential for reliable service delivery across Australia's largest electricity generation portfolio.

SOCI Act Compliance:
Unity Catalog audit logs provide 365-day retention of all access events with 15-minute streaming to SIEM platforms, meeting critical infrastructure incident reporting obligations whilst enabling forensic investigation.

Industrial Data Strategy
Unified OT/IT Architecture: From Multi-Hop Latency to Direct Streaming
Our industrial data strategy directly addresses AGL's SCADA, IoT, and time-series challenges by eliminating the current 4-hop architecture complexity that introduces unacceptable latency and prevents real-time operational excellence.

The Transformation: From Complex to Simple
Current AGL Architecture (Legacy):

SCADA/Historian → SAP HANA → ADF → Databricks → Parquet → Synapse Polybase
└─ Overnight batch processing
└─ Hours of latency
└─ Multiple failure points
└─ High operational overhead

Databricks Unified Architecture:

SCADA/Historian → Databricks Unity Catalog (Streaming Ingestion)
└─ Sub-second latency
└─ Single governance layer
└─ Automatic failure recovery
└─ Zero operational overhead

Quantified Impact:

From: 4-hop architecture, 8-12 hour latency, manual failure recovery
To: Direct ingestion, sub-second latency, automatic recovery
Cost Reduction: Estimated 40-60% reduction in data engineering overhead through architectural simplification
Ingestion: Direct OT-to-Lakehouse Connectivity
Capability 1: Native Historian Integration
AGL Challenge: "How do we access high-fidelity operational data from OSI PI, IP21, and PHD historians currently trapped in proprietary formats?"

Databricks Approach:

AVEVA CONNECT Integration: Native OSI PI System access via Delta Sharing with 5-minute refresh (AVEVA Connect limitation), preserving asset hierarchy metadata from PI AF for contextual analysis across Liddell, Bayswater, and renewable assets
AVEVA Adapters: Collect data from third-party historians including Honeywell IP21, AspenTech PHD via OPC UA servers—supporting heterogeneous OT environments without vendor lock-in
Seeq Industrial Analytics Integration: Bi-directional connectivity enabling process engineers to perform contextual analysis in Seeq whilst maintaining Databricks as system of record
Technical Advantage:
Maintains operational tool continuity (engineers keep using Seeq/PI Vision) whilst unifying data governance and enabling AI/ML workloads impossible on historian platforms alone.

Capability 2: Real-Time SCADA Streaming
AGL Challenge: "Overnight batch processing prevents real-time grid monitoring, operational decision-making, and proactive customer communication during outages."

Databricks Approach:

Zerobus Ingest (Public Preview): Direct gRPC streaming from SCADA systems, HiveMQ, Ignition, and RabbitMQ into Delta Lake with sub-5-second end-to-end latency—eliminating middleware complexity
Azure Event Hubs/Kafka Native Integration: Structured Streaming ingestion from industrial message buses with exactly-once semantics and automatic schema evolution—handling smart meter telemetry at 15-minute intervals for 4.56 million customers
Auto Loader for Batch Historian Exports: Incremental processing of historian exports (CSV, Parquet, JSON) with automatic schema detection and rescued data columns preventing data loss during format changes
Architectural Simplification:
Replaces 4-hop complexity with direct connectivity, reducing latency from hours/overnight to sub-minute streaming—enabling real-time Collections, grid monitoring, and operational decision-making.

Capability 3: Smart Meter Analytics at Scale
AGL Challenge: "Processing 4.56 million smart meters with 15-minute interval reads requires elastic scalability and real-time availability impossible on current capacity-constrained infrastructure."

Databricks Approach:

Serverless Streaming Pipelines: Auto-scaling infrastructure processes 100+ million meter reads per day with consistent sub-minute latency regardless of volume spikes
Delta Lake ACID Transactions: Enables simultaneous streaming writes (real-time ingestion) and analytical reads (BI dashboards) on same dataset without conflicts—critical for billing accuracy and customer analytics running concurrently
Lakeflow Spark Declarative Pipelines: Unified batch/streaming processing applying identical quality logic (validation rules, anomaly detection) across both overnight reconciliation and real-time monitoring
Scale Validation:

Hydro-Québec: 4.5M meters, 1 trillion+ data points
DTE Energy: 2.3M customers, real-time grid reliability
Octopus Energy: Large-scale smart meter analytics for dynamic pricing
Processing: Unified Batch & Streaming for Industrial Workloads
Challenge: Manual Processes & Schema Evolution Downtime
AGL's Pain Point:
"Schema evolution requires complete table rebuilds with associated downtime, while manual, offline processes for routine operations create friction incompatible with real-time analytics requirements."

Databricks Differentiation:

1. Declarative Pipeline Simplification

Lakeflow Spark Declarative Pipelines: Single pipeline definition handles both overnight batch meter reconciliation and streaming voltage event monitoring—eliminating dual-stack complexity and code duplication
Automatic Schema Evolution: New telemetry fields from renewable asset types (battery state-of-charge, EV charging rates) automatically added to schemas without pipeline failures or rebuilds
Rescued Data Columns: Unexpected SCADA payload variations captured as JSON for downstream inspection rather than dropped data or failed pipelines
2. Real-Time Streaming Mode (Public Preview → GA Q2 2026)

Sub-second latency (40-300ms p99) for operational workloads like battery dispatch decisions and grid balancing—10-100x faster than traditional micro-batch processing
Exactly-once semantics ensuring billing accuracy and regulatory compliance across concurrent streaming and batch settlement processes
3. Medallion Architecture for Industrial Data

Layer	Purpose	AGL Example	Quality Controls
Bronze	Raw ingestion with full fidelity	SCADA telemetry, smart meter reads (15-min intervals), asset historian data	Schema evolution, rescued data, time-travel audit
Silver	Cleansed, contextual	De-duplicated sensor readings, asset hierarchy enrichment, quality flags	Expectations (warn/drop/fail), anomaly detection
Gold	Business-ready aggregations	Customer consumption profiles, asset performance KPIs, regulatory reports	Certified datasets, automated lineage, access control



Operational Transformation:

From: Manual ETL processes, schema rebuild downtime (hours), separate batch/streaming stacks
To: Automated pipelines, zero-downtime evolution, unified processing
Developer Productivity: Estimated 50-70% reduction in pipeline development time through declarative approach
Analytics: Purpose-Built for Industrial Intelligence
Capability 1: Time-Series Optimisation at Scale
AGL Challenge: "Analysing years of SCADA telemetry and smart meter history for predictive maintenance and demand forecasting requires sub-second query performance on terabyte-scale datasets."

Databricks Optimisation:

Z-Ordering on Timestamp Columns: Physically clusters related time ranges—delivering 10-100x faster queries on historical sensor data (e.g., "Show me all voltage events at Liddell last quarter")
Bloom Filters: Accelerated lookup of specific sensors/assets across billions of time-series events—enabling instant root cause analysis during incidents
Photon Engine: Vectorised execution delivering 3-8x faster aggregations on high-cardinality industrial datasets (millions of unique sensor IDs)
Predictive Optimisation: AI automatically maintains time-series tables—70% faster queries over 3 years without manual index tuning or partition maintenance
Performance Proof:
Production deployments demonstrate ETL workloads 31% faster year-over-year and BI queries 73% faster over 2 years—automatically applied improvements without re-architecture.

Capability 2: Industrial AI/ML Patterns
AGL Challenge: "Platform prevents algorithmic battery dispatch, renewable forecasting, and VPP orchestration—blocking operational AI required for 12 GW transition."

Databricks AI for Industrial Operations:

1. ai_forecast() SQL Function (GA)

Multivariate forecasting for renewable generation, demand prediction, and grid balancing directly in SQL—no Python/data science expertise required
Supports grouped forecasting across multiple assets (wind farms, battery systems, customer segments) in a single query
Integrates weather data, grid conditions, and market signals as covariates for accurate predictions
AGL Application: Energy Markets analyst runs SQL query: SELECT ai_forecast(generation_mw, weather_conditions, grid_constraints) FROM renewable_assets GROUP BY asset_id → receives hourly generation forecasts for every renewable asset → optimises day-ahead AEMO market offers—all without writing Python code.

2. Agent Bricks AutoML Forecasting (Public Preview)

Automatic algorithm selection (Prophet, Auto-ARIMA, DeepAR) on serverless compute—testing multiple approaches and selecting optimal model based on accuracy metrics
Generates production-ready notebooks and registers models to Unity Catalog for governance
Supports batch inference and real-time serving—enabling both strategic planning and operational dispatch
AGL Application: Data scientist initiates AutoML forecasting on wholesale NEM price data → platform automatically tests 10+ algorithms → selects optimal ensemble model → deploys to Model Serving endpoint → Collections team receives hourly price predictions informing payment plan recommendations.

3. Predictive Maintenance Models

Anomaly detection on SCADA telemetry identifying equipment degradation before failure—reducing unplanned outages across generation portfolio
Condition-based maintenance scheduling optimising asset availability whilst minimising maintenance costs
Integration with CMMS systems (Maximo, SAP PM) via REST APIs for automated work order creation
AGL Application: Liddell Turbine Health Monitor analyses vibration sensors, temperature readings, and pressure telemetry → detects abnormal bearing wear pattern → predicts failure in 72-96 hours → automatically creates maintenance work order → optimises unit shutdown timing to minimise market impact—preventing forced outage and wholesale price exposure.

Capability 3: Digital Twin & Real-Time Simulation
AGL Challenge: "How do we simulate VPP dispatch scenarios, test grid stability under high renewable penetration, and optimise battery charge/discharge cycles without impacting live operations?"

Databricks Digital Twin Architecture:

Lakebase (Managed Postgres): Low-latency operational state serving (<10ms query latency) for real-time digital twin applications representing:

VPP asset states: Current battery SOC, solar generation, customer demand
Grid topology: Substation capacity, transformer loading, voltage profiles
Market conditions: Wholesale prices, FCAS signals, demand forecasts
Synced Tables: Continuous synchronisation from analytical Delta Lake to operational Postgres—enabling:

Real-time operational dashboards (<10ms query response) for control room displays
Historical context for ML training (years of operational data in Delta Lake)
Simulation workloads testing dispatch scenarios without impacting live state
RDF-Based Twin Modelling: Graph relationships capturing asset hierarchies, grid topologies, and system dependencies for holistic operational intelligence

Transformation Impact:

From: Static asset management, reactive operations, limited simulation capability
To: Dynamic digital twins, proactive optimisation, comprehensive scenario testing
Operational Excellence: Enables "what-if" scenario analysis for VPP dispatch before executing commands, reducing operational risk
AGL-Specific Use Case:
VPP Scenario Simulator models impact of dispatching 1,487 MW battery portfolio during evening peak → tests grid stability under various renewable generation scenarios → identifies optimal dispatch schedule maximising FCAS revenue whilst maintaining reliability obligations → executes validated strategy automatically—shifting from manual reactive dispatch to autonomous optimised operations.

Integration: Cloud-Native & Multi-Cloud Industrial Architecture
Solving Multi-Cloud Fragmentation Without Forced Migration
AGL's Reality:
"Kaluza customer platform (AWS) + Corporate operational assets (Azure) creates governance fragmentation and prevents unified industrial analytics. Current approach forces costly cross-cloud data replication."

Databricks Integration Strategy:

1. Unity Catalog Cross-Cloud Governance

Single governance layer across AWS and Azure industrial data—SCADA telemetry from Azure coexists with Kaluza customer data from AWS under unified RBAC/ABAC controls
Consistent audit logging across clouds with 365-day retention—simplifying SOCI Act compliance reporting
Centralised metadata management—one catalog for Customer Markets (AWS), Energy Markets (Azure), Corporate (Azure) platforms
2. Lakehouse Federation (No Data Movement)

Direct queries to operational databases (SQL Server, Oracle, PostgreSQL) without data replication—accessing SCADA historians and EMS systems in-place whilst maintaining Unity Catalog governance
Query pushdown optimisation: Filters and aggregations execute at source systems using native database engines, minimising network transfer
Materialised views: Cache frequently-accessed federated data as Delta tables with incremental refresh—balancing performance with cost
3. Delta Sharing for Governed Collaboration

Zero-copy data sharing enabling:
AEMO Market Data Integration: Secure sharing of wholesale pricing, demand forecasts, and regulatory signals without replication
Partner Collaboration: Sharing anonymised grid performance data with distribution partners and technology vendors under governed contracts
Cross-Business Unit Analytics: Energy Markets accessing Customer Markets smart meter data for demand forecasting whilst respecting privacy boundaries
4. Cloud-Native Integration Without Lock-In

Azure Synapse Migration Path: Lakebridge automated assessment and conversion with reconciliation validation ensuring data integrity during transition from current environment
Private Link Connectivity: Ignition Gateway, Event Hubs, and storage accessed via Microsoft backbone ensuring industrial telemetry never traverses public internet
AWS Services Access: Direct S3 querying from Azure Databricks for Kaluza/Salesforce data without costly cross-cloud egress fees
Architectural Benefit:
Eliminates forced data migration and cross-cloud duplication, enabling unified industrial analytics across AWS customer data and Azure operational assets whilst optimising cloud costs and maintaining security boundaries.

Cost Impact:
Estimated 30-50% reduction in cross-cloud data transfer costs through selective replication and federated queries replacing wholesale data movement.

Industrial Data Capabilities: Specific Applications for AGL's Energy Operations
Application 1: Smart Meter Analytics (4.56M Customers)
Business Objective: Enable dynamic pricing, demand response programs, and customer behaviour analytics whilst supporting Collections and billing accuracy.

Data Flow:

Ingestion: Azure Event Hubs streaming 15-minute interval reads with Auto Loader for batch reconciliation (overnight settlement files)
Processing: Lakeflow pipelines detecting anomalies, estimating missing reads, and calculating consumption patterns with declarative quality rules
Analytics: Customer segmentation, demand forecasting, and dynamic pricing optimisation using ai_forecast() SQL function and AutoML models
Real-Time Application: Collections Prioritisation App using Lakebase backend providing second-level latency payment risk scores based on live consumption patterns and payment behaviour
Transformation Metric:

From: Overnight batch, 8-12 hour latency, manual Collections prioritisation
To: Real-time streaming, <1 minute latency, AI-driven Collections optimisation
Business Value: Estimated 15-20% improvement in payment recovery rates through timely intervention
Application 2: Generation Asset Monitoring (Liddell, Bayswater, Renewables)
Business Objective: Maximise asset availability, minimise unplanned outages, optimise maintenance schedules, and ensure compliance with AEMO obligations.

Data Flow:

Ingestion: AVEVA CONNECT for OSI PI historian data with 5-minute refresh; Zerobus for direct SCADA streaming (real-time alarms, frequency events)
Processing: Asset hierarchy preservation from PI AF, contextual enrichment with operational metadata (unit status, maintenance history, environmental conditions)
Analytics:
Predictive maintenance models detecting bearing wear, boiler tube degradation, turbine efficiency loss
Efficiency optimisation identifying heat rate improvements and fuel consumption reduction opportunities
Emissions tracking for AASB S2 Scope 1 reporting with automated lineage to source measurements
Real-Time Application: Asset Health Dashboard (Databricks App) providing control room operators with sub-second updates on unit status, predicted failures, and automated dispatch recommendations
Operational Excellence:

From: Reactive maintenance, unplanned outages, manual efficiency analysis
To: Predictive maintenance, proactive intervention, AI-optimised operations
Reliability Impact: Estimated 10-15% reduction in unplanned outages through early fault detection
Application 3: VPP Orchestration (1,487 MW Decentralised Assets)
Business Objective: Orchestrate distributed solar, battery, and EV charging assets as virtual power plant, maximising revenue through NEM market participation whilst maintaining grid stability and customer service obligations.

Data Flow:

Ingestion:

Solar inverter telemetry (generation output, voltage profiles) via IoT protocols (MQTT)
Battery state-of-charge streaming from distributed battery management systems
EV charging load data from smart chargers deployed across AGL customer sites
Processing:

Digital twin state synchronisation to Lakebase for sub-10ms operational queries
Real-time aggregation of available capacity across 1,487 MW portfolio
Grid constraint evaluation (thermal limits, voltage stability) based on AEMO network data
Analytics:

Multi-agent AI orchestration optimising dispatch across distributed assets based on:
Wholesale NEM prices (5-minute intervals)
FCAS market opportunities (frequency regulation, load following)
Grid constraints and reliability obligations
Customer preferences and contractual terms
Scenario simulation testing dispatch strategies before execution
Closed-Loop Control: Custom PySpark Sinks writing optimised dispatch commands back to battery management systems and demand response platforms—creating autonomous operations

Autonomous Operation:
VPP Dispatch Agent receives AEMO price spike signal (wholesale > $300/MWh) → queries 1,487 MW asset availability in real-time → calculates optimal dispatch maximising revenue whilst respecting grid constraints → executes automated bidding into 5-minute NEM market → sends discharge commands to distributed batteries → monitors performance and adjusts in real-time—all without human intervention.

Financial Impact:
Estimated $15-25M annual revenue uplift through optimal market participation and ancillary services bidding enabled by autonomous dispatch impossible with overnight batch architecture.

Application 4: Grid Reliability & Proactive Outage Management
Business Objective: Minimise customer impact from grid disturbances, enable proactive communication, and improve NPS through transparency during outages.

Data Flow:

Ingestion:

Voltage event streaming (sags, swells, interruptions) via SCADA
Breaker status changes indicating fault conditions
Transformer load monitoring detecting thermal overload risks
Processing:

Complex event processing detecting cascading failures and abnormal patterns
Spatial correlation using Mosaic H3 geospatial indexing linking grid events to customer locations
Analytics:

Outage prediction models forecasting fault probability 4-72 hours in advance
Optimal switching strategies minimising customer impact during restoration
Customer impact assessment identifying affected households and vulnerability indicators
Proactive Customer Communication: Outage Notification Agent automatically sends personalised alerts via preferred channel (SMS/email/app) with estimated restoration time

Cross-Domain Integration (The Game-Changer):
By unifying Azure (Operational SCADA) and AWS (Customer) estates, we enable use cases previously impossible—such as correlating real-time asset failure data (OT) with customer impact data (IT) to proactively communicate outages with personalised context (e.g., "Your area experiencing outage due to Liddell substation fault, estimated restoration 14:30, vulnerable customer support available at 1800-XXX-XXX"), directly improving NPS metrics crucial to AGL's strategy.

Customer Experience Transformation:

From: Reactive outage communication, generic messages, customer frustration
To: Proactive personalised notifications, estimated restoration times, vulnerable customer routing
NPS Impact: Estimated +5-8 NPS points through transparency and proactive communication during outages
Integration Summary: The Edge-to-Cloud Continuum
The Strategic Shift:
We treat industrial data as a first-class citizen, not an afterthought requiring custom integration. Our platform provides bidirectional edge-to-cloud integration supporting AGL's grid modernisation requirements:

Edge → Cloud (Telemetry Ingestion):

Lightweight forwarding agents at grid edge locations (substations, renewable sites, battery installations)
Batch and stream operational data (voltage readings, breaker status, generation output) with low latency
Real-time visibility across AGL's generation, transmission, and distribution assets
Cloud → Edge (Action Execution):

Unity Catalog syncs curated lakehouse data (ML predictions, load forecasts, equipment health scores) into operational systems via managed synced tables
Custom PySpark Sinks write analytics results back to SCADA systems and battery management platforms
Closed-loop control where cloud-computed insights flow back to field devices and control room displays
Autonomous Grid Operations:
This architecture supports AGL's autonomous grid operations, enabling faster response to network events (seconds vs. minutes) whilst reducing infrastructure complexity and operational costs—directly supporting the transition to 12 GW renewable capacity with reliable, resilient operations.