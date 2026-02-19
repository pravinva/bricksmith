# Databricks Multi-Cloud Solution Design Architecture - Image Generation Prompts

## Overview

This document provides **7 optimized Bricksmith prompts** for generating professional solution design architecture diagrams for Databricks deployed on both AWS and Azure. These prompts are specifically designed for Lead Data Engineers and Data Architects, balancing detail and clarity.

---

## Prompt 1: Core Multi-Cloud Lakehouse Architecture Overview

**Purpose**: Main overview diagram showing Databricks deployed across AWS and Azure with key architectural layers

**Prompt**:
```
Create a clean, professional technical architecture diagram for a multi-cloud Databricks lakehouse platform deployed on both AWS and Azure. The diagram should use a horizontal swim-lane layout with the following seven layers from left to right: Source, Ingest, Transform, Query/Process, Serve, Analysis, and Storage.

At the top, show a split representation indicating AWS (left half) and Azure (right half) with their respective logos. 

In the Source layer, display various data sources including: AWS S3 and Azure Data Lake Storage Gen2 for cloud object storage, AWS RDS and Azure SQL Database for transactional databases, Amazon Kinesis and Azure Event Hubs for streaming data, Salesforce and SAP for enterprise applications, and REST APIs for external integrations.

In the Ingest layer, show: Databricks Auto Loader for incremental file ingestion, Delta Live Tables for declarative ETL, Kafka/Confluent for event streaming, Fivetran and Airbyte for SaaS connectors, and custom Spark Structured Streaming jobs.

In the Transform layer, prominently feature: Unity Catalog spanning across both clouds as the governance layer, Delta Lake as the storage format foundation, and the Medallion Architecture with three distinct zones labeled Bronze (raw ingestion), Silver (cleansed and conformed), and Gold (business-level aggregates). Show Databricks Workflows orchestrating the transformations.

In the Query/Process layer, display: Databricks SQL for analytics workloads, Spark notebooks for data engineering, MLflow for machine learning experimentation, and Photon Engine for accelerated query performance.

In the Serve layer, show: Delta Sharing for secure data sharing, Databricks SQL Warehouses (both serverless and classic), Feature Store for ML features, and Model Registry for ML model versioning.

In the Analysis layer, include: Databricks SQL Dashboards, Power BI and Tableau for business intelligence, Jupyter notebooks for data science, and custom applications via REST API.

The Storage layer at the bottom should span the full width showing: AWS S3 buckets on the left with Delta Lake tables, Azure Data Lake Storage Gen2 on the right with Delta Lake tables, and Unity Catalog Metastore in the center managing metadata across both clouds.

Add two additional horizontal layers overlaying the entire diagram: at the very top, a Control Plane bar labeled "Databricks Control Plane (Databricks-Managed)" showing workspace management, cluster lifecycle, job scheduling, and authentication; just below it, a Compute Plane bar labeled "Compute Plane (Customer Cloud Account)" showing serverless compute, job clusters, and all-purpose clusters.

Use a modern color palette with Databricks orange/red (#FF3621) for Databricks-specific components, AWS orange (#FF9900) for AWS services, Azure blue (#0078D4) for Azure services, and neutral grays for generic components. Include subtle connecting lines showing data flow from left to right through the layers. Ensure all text is clearly legible with a clean sans-serif font. The overall aesthetic should be enterprise-grade, technically accurate, and suitable for architect-level presentations.
```

**File Name**: `databricks-multi-cloud-overview.png`

**Caption**: Multi-cloud Databricks lakehouse architecture showing deployment across AWS and Azure with unified governance

---

## Prompt 2: Medallion Architecture Data Flow Detail

**Purpose**: Detailed view of the Bronze-Silver-Gold medallion pattern with data transformations

**Prompt**:
```
Create a detailed technical diagram illustrating the Databricks Medallion Architecture pattern across Bronze, Silver, and Gold layers. Organize the diagram into three distinct vertical zones from left to right.

The Bronze Layer zone on the left should show: multiple data source icons at the top (S3/ADLS cloud storage, Kafka streams, JDBC databases, REST APIs), flowing into raw data ingestion represented by delta tables with schema "bronze.raw_customers", "bronze.raw_orders", "bronze.raw_events". Include annotations showing "Append-only writes", "Raw format preservation", "Schema on read", and "Full historical audit trail". Show Auto Loader and Delta Live Tables as ingestion mechanisms. Indicate both batch and streaming ingestion paths with distinct arrow styles.

The Silver Layer zone in the center should display: data flowing from Bronze with transformation operations clearly labeled including "Deduplication", "Null handling", "Data type casting", "Business rule validation", and "Join operations". Show delta tables with schema "silver.customers_cleaned", "silver.orders_validated", "silver.customer_transactions". Include a quarantine table path labeled "silver.quarantine" for invalid records. Add annotations for "SCD Type 2 for history", "Data quality checks", and "Standardized schemas". Show Change Data Feed (CDF) enabled on tables.

The Gold Layer zone on the right should show: business-ready dimensional models with schemas like "gold.dim_customer", "gold.fact_sales", "gold.customer_360", "gold.daily_revenue_summary". Include annotations for "Star schema modeling", "Business-level aggregations", "Pre-joined for consumption", and "Optimized for query performance". Show liquid clustering optimization indicators on tables.

Between each layer, display transformation logic boxes showing: Bronze to Silver uses "Structured Streaming with watermarking", "MERGE operations for upserts", "Expectation constraints for quality"; Silver to Gold uses "Dimensional modeling", "Time-based aggregations", "Slowly Changing Dimensions".

At the bottom, show a timeline indicating data latency: Bronze (minutes), Silver (near real-time to hourly), Gold (hourly to daily). Include Unity Catalog lineage connectors showing metadata tracking across all layers.

Add persona indicators showing: Bronze layer accessed by "Data Engineers" and "Compliance teams", Silver layer by "Data Engineers", "Data Scientists", and "Analysts", Gold layer by "Business Analysts", "BI Developers", and "Executives".

Use color coding: bronze/copper tone (#CD7F32) for Bronze layer, silver/gray (#C0C0C0) for Silver layer, and gold/yellow (#FFD700) for Gold layer. Include Delta Lake logo watermarks in each zone. Show Databricks Workflows orchestration bars at the top connecting the layers. The diagram should be highly detailed but remain clean and readable with clear typography and logical flow arrows.
```

**File Name**: `databricks-medallion-detail.png`

**Caption**: Detailed medallion architecture showing progressive data refinement from raw ingestion through business-ready analytics

---

## Prompt 3: Control Plane vs Compute Plane Architecture

**Purpose**: Detailed breakdown of Databricks architectural separation across AWS and Azure

**Prompt**:
```
Create a detailed technical diagram showing the architectural separation between Databricks Control Plane and Compute Plane for both AWS and Azure deployments. Organize the diagram into two horizontal sections.

The top section labeled "Control Plane - Databricks Managed (Multi-Cloud SaaS)" should show: Databricks cloud infrastructure with components including Workspace UI and Notebooks, REST APIs and CLI interfaces, Cluster Manager for lifecycle orchestration, Job Scheduler and Workflow engine, Unity Catalog Metastore (showing it spans both clouds), Authentication and Identity Management (integrating with Azure AD and AWS IAM), DBFS root storage, Web Application backend, Secrets Manager, and Audit Logs. Use a purple/violet background (#6C3483) to indicate Databricks-managed infrastructure. Show this as a single unified control plane serving both cloud environments.

The bottom section should be split vertically into two zones: left side for AWS, right side for Azure.

AWS Compute Plane zone should display: Customer AWS Account containing VPC with private subnets, EC2 instances running Databricks Runtime (showing driver and worker nodes), Serverless Compute pools, Job Clusters (auto-terminating), All-Purpose Clusters (persistent for development), Instance Pools for fast cluster startup, S3 buckets for Unity Catalog managed storage and external locations, AWS Secrets Manager integration, CloudWatch for monitoring and logs, IAM roles for cross-account access, Security Groups and NACLs, and PrivateLink endpoints for secure connectivity back to Control Plane. Use AWS orange (#FF9900) color scheme.

Azure Compute Plane zone should display: Customer Azure Subscription containing Virtual Network with private subnets, VM instances running Databricks Runtime (showing driver and worker nodes), Serverless Compute pools, Job Clusters (auto-terminating), All-Purpose Clusters (persistent for development), Instance Pools for fast cluster startup, Azure Data Lake Storage Gen2 for Unity Catalog managed storage and external locations, Azure Key Vault integration, Azure Monitor for monitoring and logs, Managed Identities for authentication, Network Security Groups, and Private Endpoints for secure connectivity back to Control Plane. Use Azure blue (#0078D4) color scheme.

Show clear bidirectional communication arrows between Control Plane and both Compute Planes labeled with: "Cluster commands and configuration", "Job execution instructions", "Notebook code and results", "Metrics and logs", "Authentication tokens". Indicate these connections can use either Public Internet or Private Connectivity (PrivateLink/Private Endpoints).

Add annotations explaining: "Control Plane: manages orchestration, metadata, and user interface", "Compute Plane: executes workloads and stores data in customer environment", "Data never transits through Control Plane". Include security indicators showing encryption in transit (TLS) and encryption at rest.

Add a small inset diagram showing the network flow: User → Control Plane → Compute Plane → Data Storage, with return path for results.

Use clear, enterprise-grade styling with distinct color coding for each cloud provider and Databricks components. Include cloud provider logos and Databricks logo. Ensure all connection lines are clear with directional arrows and labels.
```

**File Name**: `databricks-control-compute-plane.png`

**Caption**: Control plane and compute plane architectural separation showing Databricks management layer and customer cloud execution environments

---

## Prompt 4: Unity Catalog Multi-Cloud Governance Architecture

**Purpose**: Detailed view of Unity Catalog governance spanning AWS and Azure

**Prompt**:
```
Create a comprehensive technical diagram illustrating Unity Catalog's multi-cloud governance architecture across AWS and Azure. Use a layered three-tier approach.

The top tier labeled "Unity Catalog Metastore - Central Governance Layer" should show: a single Unity Catalog metastore icon at the center, with the three-level namespace hierarchy clearly displayed as "Metastore → Catalogs → Schemas → Tables/Volumes". Show multiple catalogs including "prod_catalog", "dev_catalog", "analytics_catalog", and "ml_catalog". Include governance capabilities radiating from the metastore: Fine-grained Access Control (showing table/row/column level permissions), Data Lineage tracking (with visual lineage graph), Audit Logging, Data Discovery and Search, and Attribute-based Access Control (ABAC) tags.

The middle tier should show security and identity integration: on the left, AWS IAM roles and policies connecting to Unity Catalog; on the right, Azure Active Directory and Managed Identities connecting to Unity Catalog; in the center, external identity providers (Okta, Azure AD) for user authentication. Show SCIM provisioning for user/group sync.

The bottom tier should be split into two cloud zones.

AWS zone on the left showing: S3 buckets designated as External Locations (for external tables) and Managed Locations (for managed tables), with storage credentials using IAM roles. Display external tables pointing to S3 paths, managed tables in Unity Catalog-managed S3 locations, and external volumes for unstructured data. Show cross-account IAM role trust relationships. Include Unity Catalog external locations configuration with path permissions.

Azure zone on the right showing: Azure Data Lake Storage Gen2 containers designated as External Locations and Managed Locations, with storage credentials using Azure Managed Identities and Service Principals. Display external tables pointing to ADLS paths, managed tables in Unity Catalog-managed ADLS locations, and external volumes for unstructured data. Show ABAC integration with Azure tags. Include Unity Catalog external locations configuration with path permissions.

In the center between clouds, show Delta Sharing capabilities: external recipients accessing shared data, share objects, and recipients, with secure token-based authentication. Show that Delta Sharing works across both clouds.

Add a workspace assignment section showing: multiple Databricks workspaces (workspace_prod, workspace_dev, workspace_analytics) across both AWS and Azure, all connected to the single central Unity Catalog metastore. Show that workspaces can be in different regions and clouds but share the same governance.

Include permission grant flow diagrams showing: Principal (User/Service Principal/Group) → Privilege (SELECT/MODIFY/CREATE) → Securable Object (Catalog/Schema/Table/Volume). Show inheritance hierarchy where schema permissions inherit from catalog, and table permissions inherit from schema.

Add cross-cloud access pattern showing: Azure Databricks workspace accessing AWS S3 data through Unity Catalog with proper storage credentials and external locations configured for cross-cloud access (highlight this as a key capability).

Use a color scheme with: deep purple (#5B2C6F) for Unity Catalog components, AWS orange for AWS elements, Azure blue for Azure elements, and green (#27AE60) for security/permissions elements. Include icons for tables, volumes, catalogs, and schemas. Show clear connection lines with permission flows and data access paths. Add Unity Catalog logo prominently.
```

**File Name**: `databricks-unity-catalog.png`

**Caption**: Unity Catalog multi-cloud governance architecture showing centralized metadata, access control, and lineage across AWS and Azure

---

## Prompt 5: Compute Options and Cluster Architecture

**Purpose**: Detailed breakdown of compute options including serverless, job clusters, and all-purpose clusters

**Prompt**:
```
Create a detailed technical diagram comparing and showing Databricks compute options and cluster architecture. Organize into four main sections.

Top section labeled "Compute Options Overview" should show three distinct compute types side by side: Serverless Compute (left), Job Clusters (center), and All-Purpose Clusters (right). For each, include a visual representation and key characteristics.

Serverless Compute panel should show: Databricks-managed compute infrastructure icon, characteristics listed as "Instant startup (seconds)", "Auto-scaling", "Fully managed by Databricks", "No cluster configuration needed", "Pay per query/task", "Isolated per job". Show use cases: "Databricks SQL queries", "Delta Live Tables", "Notebooks execution", "Scheduled jobs". Indicate availability: "AWS and Azure". Use a glowing effect to indicate instant-on capability.

Job Clusters panel should show: cluster lifecycle diagram with "Created → Running → Terminated" flow, characteristics listed as "Created for specific job", "Auto-terminates after completion", "Isolated per job", "Cost-optimized", "5-minute startup", "Configured via job definition". Show use cases: "Production ETL pipelines", "Scheduled batch processing", "Automated workflows", "CI/CD deployments". Display instance pool connection for faster startup.

All-Purpose Clusters panel should show: persistent cluster icon with restart capability, characteristics listed as "Manually created", "Shared by multiple users", "Persists until manually terminated", "Auto-pause after inactivity", "Development-focused", "Higher cost per DBU". Show use cases: "Interactive development", "Notebook experimentation", "Ad-hoc analysis", "Collaborative work". Show multiple user icons connected to the cluster.

Middle section labeled "Cluster Architecture Detail" should show: a detailed cluster composition with one Driver Node (larger box) connected to multiple Worker Nodes (smaller boxes in a grid). Driver Node should contain: "SparkContext", "Notebook execution", "Task coordination", "Results aggregation". Worker Nodes should contain: "Task execution", "Data processing", "Distributed storage". Show Databricks Runtime layer with "Spark", "Delta Lake", "MLflow", "Photon Engine" components. Include cluster configuration panel showing: "Worker type: m5.2xlarge (AWS) / D8s_v3 (Azure)", "Driver type: m5.xlarge", "Workers: 2-8 (auto-scale)", "Databricks Runtime: 13.3 LTS ML", "Spot instances: enabled".

Bottom left section labeled "Instance Pools" should show: a pool of pre-warmed idle instances ready for allocation, with arrows showing fast cluster creation from pool. Include characteristics: "Reduces cluster start time to ~2 minutes", "Idle instances stay warm", "Shared across job clusters", "Cost-effective for frequent jobs".

Bottom right section labeled "Cluster Policies and Governance" should show: policy templates restricting cluster configurations with examples: "Limit instance types", "Enforce tags", "Set autoscaling ranges", "Restrict runtime versions", "Control library installation". Show how policies enforce compliance and cost control.

Add comparison table at bottom showing Total Cost of Ownership: Serverless (lowest for sporadic use), Job Clusters (optimal for production), All-Purpose Clusters (highest for always-on). Startup Time: Serverless (seconds), Job Clusters (5 min or 2 min with pools), All-Purpose (5 min or instant if running). Best Use Case clearly differentiated for each type.

Use color coding: cyan/blue (#17A2B8) for Serverless, green (#28A745) for Job Clusters, orange (#FD7E14) for All-Purpose Clusters. Include Databricks and Apache Spark logos. Show cost indicators with dollar signs. Include arrows showing data flow through cluster components. Use modern technical diagram styling with clear typography.
```

**File Name**: `databricks-compute-options.png`

**Caption**: Databricks compute options architecture showing serverless, job clusters, and all-purpose clusters with detailed cluster composition

---

## Prompt 6: End-to-End Data Pipeline Reference Architecture

**Purpose**: Complete data pipeline showing ingestion through consumption with all components

**Prompt**:
```
Create a comprehensive end-to-end data pipeline architecture diagram for Databricks lakehouse showing realistic enterprise data flow. Use a left-to-right horizontal flow organized into clear stages.

Stage 1 "Data Sources" (far left) should show diverse source systems: AWS S3 buckets containing JSON/Parquet/CSV files with file arrival triggers, Azure Event Hubs streaming IoT sensor data in real-time, Salesforce CRM via Fivetran connector, PostgreSQL transactional database via JDBC, REST APIs from third-party services, Snowflake data warehouse via Lakehouse Federation.

Stage 2 "Ingestion Layer" should show: Databricks Auto Loader monitoring S3/ADLS with incremental file processing and schema inference, Structured Streaming consuming from Event Hubs/Kafka with exactly-once semantics, Fivetran CDC connectors syncing Salesforce changes, JDBC batch reads with partitioning and predicate pushdown, Delta Live Tables declarative ingestion pipelines. Show data landing in Bronze layer Delta tables with append-only semantics.

Stage 3 "Bronze Layer - Raw Zone" should display: Delta tables in "bronze" schema preserving raw data formats, tables named "bronze.raw_events", "bronze.salesforce_accounts", "bronze.postgres_orders". Show characteristics: "Schema on read", "Full audit trail", "Immutable append", "External volumes for unstructured". Include retention policy annotation: "7 year retention for compliance".

Stage 4 "Transformation Layer" should show: Delta Live Tables pipeline with expectations (data quality rules), Spark Structured Streaming with stateful operations and watermarking, Databricks Workflows orchestrating multiple notebook tasks in parallel DAG, Python/SQL transformations with UDFs and window functions. Show error handling with quarantine tables.

Stage 5 "Silver Layer - Cleansed Zone" should display: Delta tables in "silver" schema with validated and joined data, tables named "silver.customers", "silver.orders_enriched", "silver.events_sessionized". Show operations: "Deduplication", "Type 2 SCD", "Business rule validation", "Join dimension tables", "Column-level encryption for PII". Include Change Data Feed enabled for downstream incremental processing.

Stage 6 "Gold Layer - Business Zone" should display: Delta tables in "gold" schema with dimensional models, fact tables "gold.fact_sales", "gold.fact_web_events", dimension tables "gold.dim_customer", "gold.dim_product", aggregate tables "gold.agg_daily_revenue", "gold.customer_360". Show optimizations: "Liquid clustering on query predicates", "Z-order indexing", "Bloom filters", "Partitioned by date".

Stage 7 "Serving Layer" should show: Databricks SQL Warehouse (serverless) for BI workloads with query federation, Feature Store serving features for ML models with online/offline stores, Model Serving endpoints exposing ML models via REST API, Delta Sharing sharing datasets with external partners, Materialized views for frequently accessed aggregations.

Stage 8 "Consumption Layer" (far right) should show diverse consumers: Power BI dashboards connecting via SQL endpoint with DirectQuery, Tableau workbooks using Databricks connector, Custom Python applications using Databricks SQL Connector, Jupyter notebooks for data science, Databricks SQL dashboards for embedded analytics, Real-time applications consuming from Model Serving APIs, External partners accessing via Delta Sharing.

Overlaying the entire pipeline, show cross-cutting concerns: Unity Catalog governance spanning all layers with lineage tracking from source to consumption, Databricks Workflows orchestrating the pipeline with task dependencies and retries, Delta Lake providing ACID transactions and time travel across all layers, Monitoring and alerting with Databricks SQL alerts and custom metrics.

At the bottom, show infrastructure details: compute allocation showing "Bronze ingestion: Serverless", "Silver transformation: Job clusters with photon", "Gold aggregation: Job clusters", "Serving: SQL Warehouses and Model Serving". Storage showing AWS S3/Azure ADLS with lifecycle policies and cost optimization tiers.

Add performance metrics: "Bronze latency: < 5 minutes from source", "Silver latency: 15-30 minutes", "Gold latency: hourly refreshes", "Query performance: sub-second on gold layer". Include cost optimization annotations: "Spot instances for batch jobs", "Serverless for variable loads", "Cluster autoscaling".

Use visual flow arrows showing data movement, transformation arrows between layers, and bidirectional governance arrows for Unity Catalog lineage. Color code by layer using medallion colors (bronze, silver, gold). Include Databricks, Delta Lake, and Unity Catalog logos at relevant points. Add subtle icons representing data quality checks, security, and monitoring. Use modern enterprise architecture styling with clean lines and clear typography.
```

**File Name**: `databricks-e2e-pipeline.png`

**Caption**: End-to-end Databricks lakehouse data pipeline from ingestion through consumption showing medallion architecture and governance

---

## Prompt 7: Security and Networking Architecture

**Purpose**: Detailed security architecture showing network isolation, authentication, and encryption

**Prompt**:
```
Create a detailed security and networking architecture diagram for Databricks deployed in AWS and Azure showing enterprise security controls and network isolation. Organize into layered security zones with clear boundaries.

Top section labeled "Identity and Access Management" should show: centralized identity provider (Azure Active Directory or Okta) with SAML/OIDC SSO integration to Databricks, user and service principal authentication flows, group-based access control synced via SCIM, multi-factor authentication (MFA) requirement, conditional access policies, and token-based API authentication. Show Unity Catalog RBAC integration with principals, privileges, and securables hierarchy. Include service-to-service authentication using AWS IAM roles and Azure Managed Identities.

Middle section split into AWS and Azure zones showing network architecture.

AWS zone should display: customer VPC with private subnets in multiple availability zones for high availability, Databricks workspace deployed in VPC with no public IPs on cluster nodes, AWS PrivateLink establishing secure connection from VPC to Databricks Control Plane (bypassing public internet), VPC endpoints for S3, Secrets Manager, CloudWatch, and STS services, Security Groups with strict ingress rules (only port 443 from specific CIDRs, inter-cluster communication ports), Network ACLs providing subnet-level filtering, NAT Gateway for outbound internet access (optional), AWS Transit Gateway for connectivity to on-premises networks via VPN/Direct Connect, Web Application Firewall (WAF) protecting endpoints, Network packet inspection using VPC Flow Logs. Show cluster nodes in private subnets with no public IP addresses.

Azure zone should display: customer Virtual Network (VNet) with private subnets across availability zones, Databricks workspace in VNet injection mode with delegated subnets, Azure Private Link connecting VNet to Databricks Control Plane, Private Endpoints for ADLS, Key Vault, and Azure Monitor, Network Security Groups (NSGs) with restrictive rules, Azure Firewall for egress filtering, User-Defined Routes (UDR) controlling traffic flow, ExpressRoute or VPN Gateway for hybrid connectivity to on-premises, Application Gateway with WAF for web application protection, NSG Flow Logs for network monitoring. Show secure cluster deployment topology.

Bottom section labeled "Data Security and Encryption" should show multiple security layers:

Encryption at rest: customer-managed keys (CMK) in AWS KMS and Azure Key Vault for encrypting S3/ADLS data, EBS/managed disk encryption for cluster volumes, Delta Lake supporting encryption at column level for PII data, encrypted DBFS root storage, encrypted notebook and job output.

Encryption in transit: TLS 1.2+ for all communications between control plane and compute plane, TLS for data movement between clusters and storage, TLS for user access to workspace UI and APIs, internal cluster communication encryption.

Secrets management: integration with AWS Secrets Manager and Azure Key Vault, Databricks secret scopes (AWS-backed and Azure-backed), secure credential passthrough for accessing storage without exposing credentials, service principal rotation policies.

Data protection: Unity Catalog managing table and column-level access control, dynamic view functions for row-level security, attribute-based access control (ABAC) using tags, data masking and redaction for sensitive fields, PII detection and classification, audit logs capturing all data access with query text and user identity.

Right side panel labeled "Compliance and Monitoring" should show: audit logs streamed to CloudWatch Logs (AWS) or Azure Monitor (Azure), SIEM integration with Splunk or Azure Sentinel, compliance framework badges (SOC 2, HIPAA, GDPR, PCI-DSS), data residency controls ensuring data stays in specific regions, diagnostic logging for all Databricks operations, alerting on anomalous access patterns, Unity Catalog audit log queries for governance reporting.

Add threat model diagram in corner showing: defense in depth layers preventing data exfiltration, network isolation preventing lateral movement, credential protection preventing unauthorized access, monitoring detecting anomalies.

Use color coding: red (#DC3545) for security boundaries and firewalls, green (#28A745) for encrypted connections, blue (#007BFF) for identity/authentication, yellow (#FFC107) for monitoring/alerting. Include padlock icons for encryption, shield icons for security controls, and eye icons for monitoring. Show clear network boundaries with firewall symbols. Use professional enterprise security diagram styling with clear annotations and data flow arrows.
```

**File Name**: `databricks-security-arch.png`

**Caption**: Enterprise security and networking architecture for Databricks showing network isolation, encryption, identity management, and compliance controls

---

## Usage Instructions

### For Bricksmith Image Generation:

1. Copy the prompt text exactly as written (including all technical details)
2. Use the suggested file name for consistency
3. Generate at high resolution (recommend 1920x1080 or higher)
4. Landscape orientation (16:9 aspect ratio) works best for these technical diagrams

### Customization Tips:

- **Single Cloud**: Remove AWS or Azure sections for single-cloud deployments
- **Specific Industries**: Add compliance frameworks (HIPAA, PCI-DSS, etc.) to Prompt 7
- **ML Focus**: Enhance ML components (MLflow, Feature Store, Model Serving) in relevant prompts
- **Cost Optimization**: Emphasize serverless and job cluster sections in Prompt 5

### Recommended Presentation Flow:

- **Executive Overview**: Start with Prompt 1
- **Technical Deep Dive**: Use Prompts 2-5 sequentially
- **Security Review**: Lead with Prompt 7, reference Prompt 4 for governance
- **Implementation Planning**: Use Prompt 6 as the comprehensive reference

---

## Document Information

**Created**: January 2026  
**Version**: 1.0  
**Intended Audience**: Lead Data Engineers, Data Architects, Solutions Architects  
**Target Platform**: Databricks on AWS and Azure  
**Architecture Pattern**: Lakehouse with Medallion Architecture  
**Governance Model**: Unity Catalog Multi-Cloud

---

## Additional Resources

- Full Implementation Guide: See accompanying `implementation_guide.md`
- Databricks Documentation: https://docs.databricks.com
- Unity Catalog Guide: https://docs.databricks.com/data-governance/unity-catalog/
- a16z Modern Data Infrastructure: https://a16z.com/emerging-architectures-for-modern-data-infrastructure/
