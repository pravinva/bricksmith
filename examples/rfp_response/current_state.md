Current Platform Challenges
AGL's existing data platform architecture, based on legacy Microsoft Synapse environments and SAP HANA hosted within Azure, faces critical challenges that impede the organisation's ability to execute its strategic transformation to connect 4.56 million customers to a sustainable future and transition to 12 GW renewable capacity by 2035.
Capacity Management and Inability to Scale: Critical Operational Constraints
Capacity saturation and fragile deployments represent the most immediate operational risk to AGL's data platform. The Customer Markets environment operates at an average utilisation of 92%, with peak loads exceeding 3,000 queries per 10-minute period, leaving no headroom for growth or demand spikes.
Business stakeholders have reported that "access is unstable, or pipelines fail" regularly, creating operational fragility that undermines confidence in the platform.
Manual capacity management requiring production downtime for scaling operations prevents AGL from responding to dynamic business needs, while the inability to elastically scale compute independently of storage forces over-provisioning and creates unnecessary cost, while still failing to meet peak demand.
Platform Performance and Reliability Constraints
Resource contention between data loads, modelling, and queries competing on shared clusters creates unpredictable query performance, with business users experiencing extended processing times that critically impact decision velocity. 
Schema evolution requires complete table rebuilds with associated downtime, while manual, offline processes for routine operations create operational friction incompatible with AGL's strategic requirement for real-time analytics.
The legacy Synapse architecture is unable to deliver the real-time insights required for operational excellence, forcing business units to rely on stale data and preventing the use of predictive analytics.
Data Fragmentation, Report Sprawl and Eroded Trust
Multi-cloud fragmentation between Azure and AWS prevents the realisation of platform benefits from AGL's strategic investments, including the Kaluza acquisition (AWS) and Salesforce deployment, which remain siloed from corporate systems hosted on Azure.
With over 15,200 database objects spanning Customer Markets, Energy Markets and Development, and Corporate systems—including a Data Vault 2.0 design with thousands of granular tables—the platform lacks a single source of truth for enterprise analytics.
This fragmentation has created massive report sprawl with duplicated and inconsistent reporting artefacts across siloed platforms. Business stakeholders consistently raise concerns: "Is the data I'm looking at the most current/accurate?" and "Being able to link data back to source and know its lineage can be challenging."
The proliferation of "multiple non-enterprise systems used across Customer Markets" compounds this challenge, while the lack of automated data lineage tracking prevents tracing data provenance, validating transformations, or reconciling discrepancies.
This has fundamentally eroded business confidence in data quality and accuracy, with different teams producing conflicting metrics from the same underlying business processes.
Data Discovery and Metadata Capability Gaps
Business users struggle with fundamental data discovery questions: "I don't know where data is, how do I access it?", "It's hard to get access to the data I need", and "How can I understand the data I'm looking at?"
The lack of intelligent metadata management, automated cataloguing, and self-service discovery capabilities forces users to rely on tribal knowledge and manual processes, significantly slowing time to insight and creating barriers to data democratisation across the enterprise. Point solutions for the energy sector like Lacima proliferate across AGL
Governance Fragmentation and Regulatory Risk
Fragmented governance across Synapse, SAP HANA, and multicloud environments creates compliance risk, particularly for FY26 mandatory climate reporting under AASB S2, which requires auditable lineage for 79 climate metrics across Australia's largest corporate emitter (30.7 MtCO₂e).
The absence of unified RBAC/ABAC capabilities, coupled with manual access management, increases security exposure, while the closed Synapse architecture creates vendor lock-in, limiting tool choice and requiring payment to extract data for use with other systems.
AI/ML Capability Limitations
Current platforms prevent AGL from executing critical energy sector AI capabilities, including algorithmic battery dispatch and optimisation, renewable energy forecasting, and VPP orchestration across 1,487 MW of decentralised assets. Business stakeholders ask: "Is there a means to profile or experiment?" and "I want to develop a model to create a new data set - how do I do this?"—questions that reveal fundamental gaps in AI/ML enablement.
The fragmented technology stack limits AI/ML operationalisation at enterprise scale, preventing the "technology, digitisation and AI at the core" strategic pillar that underpins AGL's energy transition strategy.
Real-Time Processing & Data Ingestion Challenges
Business units explicitly require near-real-time capabilities: "For some use cases, such as Collections, they require more frequent data and an overnight Batch. So real-time data is a key requirement."
Current multi-hop architecture (SAP HANA → ADF → Databricks → Parquet → Synapse Polybase) introduces latency and complexity incompatible with real-time requirements, while users report "High Costs/Timelines for Data Ingestion" that slow innovation and business responsiveness. 

