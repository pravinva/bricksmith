Technology Response
AGL seeks greater details on your data platform technology from questions listed within the excel file titled Data Platform RFP Questionnaire - Response for Item 3.3.
Please respond each question within Data Platform RFP Questionnaire - Response for Item 3.3.
Product Road Map / Technology Strategy
Please provide detailed responses to the following:
Product Roadmap
Provide your product roadmap.
Highlight any future features or capabilities that may be particularly beneficial to AGL.
Artificial Intelligence (AI) Strategy
Describe how AI is currently utilized in your product.
Detail any AI features in development and explain how these features would deliver value to AGL (e.g., predictive analytics, anomaly detection, automation).
Adaptability to Industry Changes
Provide examples of how your technology and organization have previously adapted to changes in the energy/utilities industry market.
Future Industry Alignment
Explain how your organization plans to incorporate upcoming changes in the energy/utilities market into your technology strategy.
Industrial Data Strategy
What are your technology plans and strategy for managing industrial system data sources such as SCADA, IoT sensor streams, and time-series data?
Include details on ingestion, processing, analytics, and integration with cloud platforms and data lakes.
Implementation / Migration of Workloads and Datasets
Please provide detailed responses to the following:
Foundational Approach
Describe your proposed approach to establish the foundations for successful use of your technology (e.g., environment setup, governance, security, architecture design).
Reference architecture and best practices based on the medallion architecture and well‑architected Lakehouse to inform network, identity, storage, security requirements
e.g. compute and serverless budget policies, network connectivity configuration, fine-grained or attribute-based access control, serverless egress control, network policies.
Databricks Unity Catalog ensures consolidated Data Governance of all your data and AI assets. Define once, secure everywhere. Govern multiple workspaces under a single Databricks account and attach them to a shared Unity Catalog metastore to centralize governance, auditing, lineage, discovery, and fine‑grained access control across data and AI assets
Security Best Pratices: Define, Deploy, and Monitor
Automation:
Terraform to define infrastructure-as-code for components underpinning Databricks cloud infrastructure foundation (e.g. VNet / VPC, subnet ranges, IP address / CIDR ranges, private / VPC endpoints, PrivateLink etc)
DABs for promoting assets (notebooks etc.)
Databricks CLI with your preferred DevOps provider (e.g. Azure DevOps, Github Actions, GitLab). We also have a unified template for deploying AI workloads through MLOps / LLMOps
Migration Strategy
Outline your recommended approach for migrating existing workloads and datasets from other data platforms to your technology.
Databricks recommended a phased approach to migrate workloads from legacy systems to databricks. Organize data using the bronze–silver–gold medallion design pattern to progressively improve data quality and structure as it flows through the platform; consolidated data and AI assets are governed, secured, monitored with data quality and discovery to accelerate incremental processing, business analytics, compliance reporting and decision making. 
Databricks’ Lakebridge is capable of automatic assessment for code complexity, object dependencies and supports phased and incremental migration based on the automatic code assessment and object dependency. 
Synapse is well supported by both automatic conversion and reconciliation to Databricks, which greatly reduces migration complexity and protects the data integrity and quality with detailed data reconciliation. Data reconciliation helps for parallel runs during migration cutoff, ensure trusted data quality for end user consumption and analytics. 
Include considerations for minimizing downtime, ensuring data integrity, and handling complex transformations.
Minimizing downtime: run dual‑write/dual‑read windows (source and Databricks side), use Delta ACID and time travel for controlled cutover, and apply insert‑only MERGE/foreachBatch patterns for micro‑batch deduplication where appropriate.
Orchestration and cost: use Lakeflow Jobs to schedule Auto Loader/CDC pipelines (AvailableNow triggers/file arrival) and DBSQL alerts/dashboards for SLO monitoring; enable event‑driven refresh where possible. 
Complex transformations: standardize on Lakeflow Spark Declarative Pipelines/Delta Live Tables for declarative pipelines, dependency management, autoscaling, and built‑in event logs; use expectations (constraints) to quarantine/drop/fail bad records and to codify contract checks across hops. 
Data integrity and validation: codify rules as expectations (retain/drop/fail) supported by Lakeflow Spark Declarative Pipelines/Delta Live Tables, add count/shape checks, and leverage Lakehouse Monitoring for broad anomaly detection and slice‑based quality metrics; record violations and trends for operational follow‑up.
Change Management
Describe your recommended approach for change management to embed the use of your technology within an organization of AGL’s size and complexity.
Stakeholder engagement: align executive sponsors and business owners on migration roadmaps, value levers (cost, time‑to‑insight, risk reduction), and platform KPIs; socialize progress via QBRs and data product scorecards tied to Lakehouse Monitoring outputs and Unity Catalog system tables. 
Governance operating model: stand up a cross‑functional Lakehouse SME council (platform, data owners, risk/compliance, domain teams) to define catalogs/schemas ownership, data contracts, tagging, and stewardship processes in Unity Catalog. 
Include strategies for stakeholder engagement, training, and adoption.
Databricks provides role‑based enablement: deliver Databricks Academy training and subscription services (DSA/RSA/CoE) for platform admins, data engineers, analysts, and ML engineers to accelerate skills and standardize best practices
Customer Responsibilities
What key resources, responsibilities, and organizational drivers will AGL need to provide to effectively use and maximize value from your technology?
Resources: Executive sponsorship, a Lakehouse platform team (UC admins, architects, security/FinOps), and domain data owners/stewards to publish and maintain governed datasets and contracts across catalogs/schemas.
Responsibilities: Establish unified governance with Unity Catalog (shared metastore, catalogs/schemas, storage credentials/external locations), manage identities and access via UC (not direct cloud paths), and enforce fine‑grained policies plus lineage/auditing/discovery across all workspaces.
Resource Model Benefits
Describe the benefits of using your direct resources or resources from one of your partners instead of internal resources.
Accelerated outcomes with lower risk: prescriptive Professional Services offerings (e.g., Jumpstart, Migration Assurance, Lakehouse Build‑out) use proven methods and structured risk mitigation to deliver faster timelines and seamless migrations.
Access to Databricks experts and ecosystem: resident/delivery solution architects, program governance, and co‑delivery with partners, plus direct alignment with Product/Engineering (roadmap, private previews), to unblock issues and scale impact.
Enablement and operating‑model uplift: role‑based training/certifications via Databricks Academy and subscription services (DSA/RSA/CoE) to embed best practices, standardize patterns, and sustain enterprise adoption. 

Include scenarios where partner involvement accelerates implementation or adds specialized expertise.
Complex migrations (legacy EDW/Hadoop/multicloud): partners bring repeatable migration accelerators, code‑conversion tooling, and additional delivery capacity to compress timelines and de‑risk cutovers.
Industry/regulatory use cases (e.g., energy/utilities patterns, SAP integration, compliance): partners provide domain solutions, specialized connectors, and regulatory know‑how, co‑delivering with Databricks to unblock complex requirements.
Scale enablement and operating model (CoE, MLOps/streaming): partner‑led subscriptions and role‑based training help stand up Centers of Excellence, standardize best practices, and accelerate enterprise‑wide adoption and production readiness.
Optimisation and Continuous improvement
Please provide detailed responses to the following:
Maximising Value
Describe the steps and activities customers should undertake to maximise the value of your technology (e.g., governance practices, performance tuning, feature adoption strategies)
Ongoing Investment
Provide your recommendations for ongoing investment required by AGL (e.g., skills development, resource allocation, training programs) to ensure optimal use and value from your technology.
Optimisation
Explain how you will help AGL optimise cost-effective use of your technology over the next 18–24 months.
Include strategies such as licensing models, resource utilisation, automation, and performance optimisation.
