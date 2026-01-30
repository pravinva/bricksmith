Proposed Architecture for AGL Energy
This architecture represents the AGL Energy Unified Intelligence Platform. Its primary goal is to bring order and security to your data landscape whilst unlocking a new tier of operational value.

The Secure Foundation
Currently, our source data sits across two distinct worlds: our Customer Cloud on AWS and our Operational Assets on Azure. This platform unifies those worlds into a single, secure foundation.
The most critical component here is the Governance Layer (Unity Catalog). It ensures that whether data is being used by a Data Scientist or a Business Analyst, it is strictly governed, auditable, and secure. We are moving from fragmented silos to a unified Medallion Architecture—standardizing our data quality from Raw to Gold so decision-making is based on trusted facts and a single copy of data, not guesswork.
Moving Beyond Dashboards (The App Layer)
Databricks' true differentiation in 2026 lies in enabling an Application Layer, not merely a data warehouse for passive reporting. By leveraging Agent Bricks and Databricks Apps, AGL can deploy intelligent applications that sit directly within business processes—automating risk hedging, personalising customer offers, and optimising grid operations.
This capability is essential for Agentic AI. Critically for AGL, Anthropic's Claude models became available in-region in Australia on 21 January 2026. Combined with Lakebase (Serverless PostgreSQL for transactional workloads), AGL now operates an enterprise-grade agentic platform where world-class AI processes sensitive data without leaving Australian shores.
Coding Agents unlock a fundamentally new paradigm for analytics. Tools like Claude Code enable AI agents to autonomously write, debug, and execute analytical code directly against AGL's lakehouse. Rather than pre-defined dashboards limited to known questions, coding agents dynamically generate bespoke applications in response to natural language requests—accelerating insights from days to minutes whilst maintaining Unity Catalog governance and full auditability.
This transforms data from a passive asset into active, sovereign business logic. AGL's energy market data, customer insights, and operational telemetry become the foundation for autonomous decision-making systems that remain fully governed within Australian regulatory boundaries, directly supporting your CTAP objectives.
These capabilities are not theoretical—they directly address the operational challenges you face today. Having carefully reviewed your questionnaire, we recognise that AGL is undertaking a strategic platform transformation that goes far beyond technology selection - you are architecting the data foundation that will power your energy business for the next decade.
Throughout our engagement, five critical challenges have emerged:
Operational Fragility: "Access is unstable, or pipelines fail" - driven by 92% utilisation constraints and manual capacity management on Synapse.
Data Discovery & Governance: "I don't know where data is, how do I access it?" - spanning 15,200+ database objects across fragmented systems. There are over 22K PowerBI reports
Data Trust: "Is the data I'm looking at the most current/accurate?" - requiring automated quality validation and lineage.
Semantic Understanding: "How can I understand the data I'm looking at?" - needing consistent business definitions. Data model sprawl across Synapse and PBI has led to multiple versions of the truth.
AI/ML Accessibility: "I want to develop a model - how do I do this?" - democratising advanced analytics beyond specialist teams. Dedicated ML team operates in a silo on a separate technology stack.
Our product roadmap, AI strategy, and industry adaptations directly address each challenge through three strategic pillars, visualized in the architecture below:

1. Enterprise Governance at Scale
Addressing Challenges #2 (Discovery) and #4 (Semantic Understanding)
Unity Catalog is the central nervous system of the platform, providing the "define once, secure everywhere" model you require.
Unified Discovery: Unity Catalog spans the entire estate, replacing the "tribal knowledge" problem with a searchable, intelligent Data Catalogue and Metadata Management layer shown in the Supervision Plane.
Semantic Consistency: By enabling a Semantic Layer within the Intelligence Engine, business definitions are standardized. When a user asks "How can I understand the data?", the platform provides context, not just raw tables.
Security without Friction: The integration with AGL myIdentity (Entra ID) ensures that while data is discoverable, access is strictly governed via RBAC/SSO, ensuring security never becomes a bottleneck.
2. Mitigation of Migration Risk & Operational Stability
Addressing Challenges #1 (Fragility) and #3 (Trust)
To eliminate the "access is unstable" experience, the architecture replaces fragile legacy pipelines with a robust, automated factory.
Elastic Scalability: The Databricks SQL layer utilizes Serverless SQL Warehouses and Separation of Storage/Compute. This eliminates the "92% utilisation" constraint by allowing compute to scale instantly to meet demand without affecting storage or other workloads.
Structured Trust: The diagram explicitly maps the Medallion Architecture (Raw  Refined Curated). This automated curation ensures that by the time data reaches the "Consumption Zone," it is trusted and validated—answering the "Is this accurate?" question.
Automated Orchestration: Lakeflow Jobs and Lakeflow Connect handle the heavy lifting of ingestion and orchestration, replacing brittle manual processes with managed, resilient pipelines.
3. Future-Proofing for the Energy Transition
Addressing Challenge #5 (AI Accessibility)
This architecture is built to democratise innovation, bridging the gap between specialist teams and business users.
Bridging OT and IT: The bottom layer unifies Customer Cloud (AWS) and Operational Cloud (Azure). This allows AGL to harness industrial data streams (Ignition/SCADA) alongside customer data (Kaluza) for holistic predictive operations.
Democratising AI: For the user asking "How do I develop a model?", the platform offers tiered access: Data Scientists use notebooks, while Business Analysts leverage AI Agents & Copilots and Dashboards & AI/BI.
The Intelligence Engine: The core Intelligence Engine, powered by Agent Bricks and Foundation Model Serving, allows AGL to deploy generative AI agents that can actively assist in grid optimization and customer service, rather than just passively reporting on them.