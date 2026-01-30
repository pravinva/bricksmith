# Databricks Multi-Cloud Solution Architecture Prompts - Technical Edition v2.0
## Updated with 2025-2026 Multi-Cloud Best Practices

*For technical audiences: Lead Data Engineers, Data Architects, Cloud Architects*

---

## Overview

This document provides **10 optimized prompts** for generating enterprise-grade Databricks solution design architecture diagrams. Version 2.0 incorporates latest multi-cloud best practices from 2025-2026 industry research, including:

- **Active-passive disaster recovery patterns** with 4-hour RTO
- **Unity Catalog per-region metastore** architecture with Delta Sharing
- **Cross-cloud private network connectivity** (PrivateLink, ExpressRoute)
- **FinOps cost optimization** strategies for multi-cloud
- **Event-driven cross-cloud integration** patterns
- **Data gravity and compute placement** principles
- **Infrastructure as Code** (Terraform) multi-cloud provisioning

---

## Prompt 1: Multi-Cloud Lakehouse Architecture with DR Topology

**Purpose**: Enterprise-grade overview showing Databricks across AWS and Azure with disaster recovery, network topology, and regional pairing

**Prompt**:
```
Create a comprehensive technical architecture diagram for an enterprise Databricks lakehouse platform deployed across AWS and Azure with disaster recovery capabilities and multi-region topology. Use a layered approach with clear regional boundaries.

At the top level, show two major cloud regions: AWS us-east-1 (Primary) on the left and Azure East US 2 (Secondary/DR) on the right. Indicate these are paired regions for disaster recovery with a 4-hour RTO. Show a third region below: AWS us-west-2 for geographic distribution.

For each region, display the architectural layers:

**Network Layer:** Show VPC (AWS) and VNet (Azure) with private subnets across multiple availability zones. Display AWS PrivateLink endpoints connecting to Databricks Control Plane, Azure Private Link endpoints for the same purpose. Show AWS Direct Connect and Azure ExpressRoute connections to on-premises data center (illustrated at bottom). Include AWS Transit Gateway and Azure Virtual WAN for hub-spoke network topology. Show VPC/VNet peering connections between regions with replication traffic flows.

**Data Sources Layer:** Display cloud-native sources: S3 buckets in AWS, ADLS Gen2 in Azure, AWS RDS and Azure SQL Database, Amazon Kinesis and Azure Event Hubs for streaming. Show Kafka cluster with Confluent cross-cloud private replication (highlight this as cross-cloud data integration). Include on-premises data sources connected via Direct Connect/ExpressRoute: Oracle databases, file servers, mainframe.

**Ingestion Layer:** Show Databricks Auto Loader with schema inference monitoring S3/ADLS for file arrivals, Spark Structured Streaming consuming from Kinesis/Event Hubs with exactly-once semantics, Delta Live Tables pipelines for declarative ETL, Fivetran connectors for SaaS data (Salesforce, SAP), Lakehouse Federation querying external databases in-place (PostgreSQL, Snowflake, BigQuery) without data movement.

**Unity Catalog Governance Layer** (spanning across diagram): Show three separate Unity Catalog metastores: one for AWS us-east-1, one for Azure East US 2, one for AWS us-west-2. Clearly label "One metastore per region" as architectural principle. Show Delta Sharing connections between metastores for cross-region and cross-cloud data access (read-only catalogs). Display SCIM provisioning from central Azure Active Directory syncing users/groups to all metastores. Show federated authentication with SSO spanning all workspaces.

**Medallion Data Layer:** For each region, show Bronze-Silver-Gold medallion architecture. In primary region (AWS us-east-1), show full medallion with all three layers actively processing data. In DR region (Azure East US 2), show medallion in passive standby mode with replication arrows from primary indicating: Delta table Deep Clone for data replication, metastore metadata sync, job/pipeline configuration sync. In tertiary region (AWS us-west-2), show active medallion for geographically distributed workloads.

**Compute Layer:** Display compute options per region: Serverless Compute pools for SQL warehouses and DLT pipelines (highlighted as cost-optimized for variable workloads), Job Clusters with auto-termination for production ETL (shown with instance pools for fast startup), All-Purpose Clusters (minimal, marked "dev only"), Photon Engine enabled on all compute for acceleration. Show spot instances indicator for non-critical batch jobs (40-70% cost savings). Add cost tags showing "Prod: Reserved capacity" for primary, "DR: Minimal always-on" for standby.

**Serving and Consumption Layer:** Show Databricks SQL Warehouses (serverless) serving Power BI and Tableau via JDBC/ODBC, Delta Sharing sharing curated gold datasets with external partners and customers (shown as external organizations), Model Serving endpoints exposing ML models via REST API for real-time inference, Feature Store with online and offline stores serving features to ML models and applications.

**Cross-Cutting Concerns Bar** (horizontal across top): Show Databricks Control Plane (multi-cloud SaaS) managing all workspaces across regions and clouds, Terraform/Infrastructure as Code provisioning all resources with policy enforcement, Unified Monitoring sending logs to centralized SIEM (Splunk or Azure Sentinel), consolidated cost management dashboard showing AWS Cost Explorer + Azure Cost Management data, Audit logs from all Unity Catalog metastores aggregated to central lake.

**Disaster Recovery Flow** (highlighted pathway): Show failover sequence from AWS us-east-1 to Azure East US 2 with numbered steps: (1) Outage detected in primary region, (2) DNS/load balancer redirects to DR region, (3) Passive clusters activated in Azure, (4) Jobs resume from last checkpoint using replicated data, (5) 4-hour RTO achieved. Show reverse failback flow after primary recovery.

**Data Gravity Annotations:** Add callouts showing "Compute placed near data storage to minimize egress costs" with arrows pointing to colocated compute and storage in same region. Show cross-region data transfer with cost indicator "$$$" to emphasize expense.

**Network Security Indicators:** Display encryption in transit (TLS 1.2+) on all connections, customer-managed keys (AWS KMS, Azure Key Vault) for encryption at rest, network security groups and firewalls at subnet boundaries, Zero Trust security model indicators at access points.

Use color coding: AWS orange (#FF9900), Azure blue (#0078D4), Databricks red-orange (#FF3621), Green (#27AE60) for active systems, Gray (#95A5A6) for passive/standby systems, Red (#E74C3C) for security boundaries. Include cloud provider logos, Databricks logo, Delta Lake logo. Use clear directional arrows for data flow, replication, and failover paths. Add latency indicators: "< 5ms" for intra-region, "~50ms" for cross-region, "~80ms" for cross-cloud.

Enterprise technical diagram style with detailed annotations, clear typography using modern sans-serif font, and professional color palette suitable for C-level and technical stakeholder presentations.
```

**File Name**: `databricks-multicloud-dr-topology.png`

**Caption**: Enterprise multi-cloud Databricks lakehouse architecture with active-passive disaster recovery, regional pairing, and cross-cloud Unity Catalog governance

---

## Prompt 2: Unity Catalog Multi-Region Cross-Cloud Architecture

**Purpose**: Detailed technical view of Unity Catalog metastore-per-region pattern with Delta Sharing and cross-cloud data access

**Prompt**:
```
Create a detailed technical diagram illustrating Unity Catalog's multi-region, cross-cloud architecture following the "one metastore per region" pattern with Delta Sharing for cross-metastore data access. Use a matrix layout with regions as rows and governance layers as columns.

**Top Section - Account and Identity Layer:**
Show Databricks Account at the apex managing multiple workspaces across clouds. Display centralized identity provider (Azure Active Directory or Okta) with SAML/OIDC federation to Databricks Account. Show SCIM API provisioning syncing users, groups, and service principals to all metastores. Display conditional access policies enforcing MFA and device compliance.

**Matrix Layout:**

Row 1: AWS us-east-1 Region
Row 2: Azure East US 2 Region  
Row 3: AWS eu-west-1 Region

For each region row, show:

**Column 1 - Metastore:**
Display Unity Catalog Metastore icon labeled "unity_catalog_aws_use1", "unity_catalog_azure_eus2", "unity_catalog_aws_euw1". Show three-level namespace: Metastore → Catalogs (prod_catalog, dev_catalog, analytics_catalog, ml_catalog) → Schemas (bronze, silver, gold) → Tables/Volumes. Clearly annotate "Metastore scoped to region and cloud" and "Workspace can only be assigned to ONE metastore".

**Column 2 - Storage Credentials:**
For AWS rows: Show IAM roles for cross-account access with trust relationships, storage credentials configuration in Unity Catalog pointing to IAM role ARN, external locations mapped to S3 bucket paths.

For Azure row: Show Azure Managed Identities and Service Principals, storage credentials configuration pointing to managed identity, external locations mapped to ADLS Gen2 container paths.

**Column 3 - Data Assets:**
Display managed tables stored in Unity Catalog-managed S3/ADLS locations (auto-created), external tables pointing to customer S3/ADLS paths with external locations, external volumes for unstructured data (PDFs, images, models), table access control indicators showing table, row, column, and attribute-level permissions.

**Column 4 - Workspaces:**
Show 2-3 Databricks workspaces per region, each assigned to the regional metastore. Label workspaces by purpose: prod_workspace, dev_workspace, ml_workspace. Show workspace isolation but shared metadata through metastore.

**Cross-Metastore Delta Sharing Connections:**
Between regions, show Delta Sharing links connecting metastores:

From AWS us-east-1 to Azure East US 2: Show "Share" object containing list of tables/views to share, "Recipient" object representing destination metastore ID, read-only catalog created in Azure metastore consuming shared AWS data, token-based secure authentication.

From Azure East US 2 to AWS eu-west-1: Show bidirectional sharing capability.

Annotate clearly: "Delta Sharing shares DATA, not ENTITLEMENTS" and "Permissions must be mirrored via Terraform/IaC in destination metastore".

**Cross-Cloud Access Pattern (Highlight This):**
Show detailed flow: Azure Databricks workspace → Unity Catalog metastore → Storage credential (AWS IAM role) → External location (S3 bucket in AWS) → Query execution returns data. Label "Cross-cloud data access without migration or duplication - GA 2025". Show read-only support indicator.

**Center Panel - Governance Capabilities:**
Display capabilities radiating from Unity Catalog:

Fine-Grained Access Control: Show GRANT/DENY matrix with principals (users, service principals, groups) and privileges (SELECT, MODIFY, CREATE, USAGE) on securables (catalogs, schemas, tables, volumes, functions, models). Display inheritance hierarchy: schema inherits from catalog, table inherits from schema.

Data Lineage: Show lineage graph tracking column-level lineage from source tables through transformations to downstream dashboards and ML models. Annotate "Lineage scoped to metastore - does not cross metastore boundaries".

Audit Logging: Display audit log entries capturing: user identity, query text, accessed objects, timestamp, source IP, result status. Show logs streaming to CloudWatch (AWS) and Azure Monitor.

Data Discovery: Show search interface finding tables across catalogs based on metadata, tags, and column names.

Attribute-Based Access Control (ABAC): Display tags (PII, Confidential, Public) applied to tables/columns with dynamic policies granting access based on user attributes.

**Bottom Section - Permission Grant Flow:**
Show detailed RBAC flow diagram:
1. Principal identified (user@company.com, service_principal_xyz, analytics_team group)
2. Privilege requested (SELECT on gold.customer_360 table)
3. Unity Catalog checks grants and inheritance
4. Access allowed/denied
5. Audit log entry created

**Right Panel - Delta Sharing Detail:**
Zoom into Delta Sharing architecture:
- Provider metastore: defines share, adds tables to share, creates recipient with metastore ID
- Recipient metastore: defines provider, creates read-only catalog from share
- Secure token exchange for authentication
- Incremental change propagation via Change Data Feed
- Works across Databricks accounts and with non-Databricks consumers (pandas, Spark)

**Cross-Cloud Data Sharing Use Case:**
Show example: "Financial data in AWS S3 (regulated region)" shared to "European analytics team in Azure workspace (local compliance)". Data stays in AWS, queried from Azure without replication.

**Terraform Integration Annotation:**
Show IaC workflow: Terraform modules define metastores, catalogs, schemas, grants. Same module reused across regions with region-specific variables. Policy as Code enforces naming conventions, access patterns, and cost controls.

Use color scheme: Deep purple (#5B2C6F) for Unity Catalog components, AWS orange for AWS elements, Azure blue for Azure elements, Green (#27AE60) for permission grants, Red (#E74C3C) for denials, Gold (#F39C12) for Delta Sharing. Include Unity Catalog logo prominently, Delta Sharing logo, and cloud provider icons. Clear connection lines with labeled data flows and permission inheritance arrows.

Add technical annotations explaining: "Metastore metadata stored in Databricks-managed infrastructure", "Data always stays in customer cloud account", "Cross-cloud access incurs cloud provider egress charges", "Unity Catalog metastore enables $1M+ cost savings by avoiding data duplication".

Professional enterprise architecture style with clear visual hierarchy, detailed labels, and suitable for deep technical review sessions.
```

**File Name**: `databricks-unity-catalog-multiregion.png`

**Caption**: Unity Catalog multi-region cross-cloud architecture showing per-region metastores, Delta Sharing, and cross-cloud data access patterns

---

## Prompt 3: Multi-Cloud Network Architecture and Private Connectivity

**Purpose**: Detailed network topology showing private connectivity, hub-spoke patterns, and cross-cloud networking

**Prompt**:
```
Create a detailed network architecture diagram for Databricks multi-cloud deployment showing enterprise-grade private connectivity, network segmentation, and cross-cloud networking patterns. Use a three-cloud layout (AWS, Azure, on-premises) with clear network topology.

**Top Section - Databricks Control Plane:**
Display Databricks Control Plane (multi-cloud SaaS) as purple cloud at top center. Show components: Workspace UI, REST APIs, Cluster Manager, Job Scheduler, Unity Catalog Metastore services, Web Application backend. Label "Managed by Databricks in AWS us-west-2 region".

**AWS Network Architecture (Left Section):**

Outer boundary: AWS Account with multiple VPCs.

Primary VPC (us-east-1): Display hub-spoke topology with Transit Gateway at center. Show three spoke VPCs: Databricks Production VPC, Databricks Development VPC, Shared Services VPC.

Databricks Production VPC detail:
- Three private subnets across availability zones (us-east-1a, us-east-1b, us-east-1c)
- Delegated subnet for Databricks compute (no public IPs on cluster nodes)
- Security Groups with strict ingress rules: Port 443 from specific CIDR ranges only, inter-cluster communication ports 8085-8087
- Network ACLs providing subnet-level filtering
- Route table with routes to Transit Gateway, PrivateLink endpoints, NAT Gateway
- NAT Gateway in public subnet for limited outbound internet (package downloads only)
- VPC Flow Logs enabled for network packet inspection

PrivateLink Architecture:
- AWS PrivateLink VPC endpoint connecting to Databricks Control Plane (bypassing public internet)
- VPC endpoints for AWS services: S3 (gateway endpoint), Secrets Manager, CloudWatch Logs, STS, Kinesis
- Interface endpoints in private subnets with DNS resolution
- Annotation: "All control plane communication via PrivateLink - zero public internet exposure"

S3 Storage:
- Multiple S3 buckets: unity-catalog-managed bucket, external data lake buckets, Delta Lake table storage
- S3 bucket policies restricting access to specific VPC endpoints
- Customer-managed KMS keys for encryption at rest
- Lifecycle policies moving data to Glacier for cost optimization
- Versioning enabled for compliance

Direct Connect:
- AWS Direct Connect connection (10 Gbps) to on-premises data center
- Virtual Private Gateway attached to VPC
- BGP routing for private IP connectivity
- Redundant connection for high availability

**Azure Network Architecture (Right Section):**

Outer boundary: Azure Subscription with Resource Groups.

Primary VNet (East US 2): Display hub-spoke topology with Azure Virtual WAN hub at center. Show three spoke VNets: Databricks Production VNet, Databricks Development VNet, Shared Services VNet.

Databricks Production VNet detail:
- VNet injection mode with two delegated subnets: private-subnet (cluster nodes), public-subnet (Databricks infrastructure - no actual public IPs)
- Network Security Groups (NSGs) with restrictive rules: Inbound 443 from Azure Firewall only, inter-cluster rules, deny all other inbound
- User-Defined Routes (UDR) forcing traffic through Azure Firewall for egress filtering
- Service endpoints for ADLS Gen2, Key Vault, Azure Monitor
- NSG Flow Logs enabled for monitoring

Private Link Architecture:
- Azure Private Link private endpoint connecting to Databricks Control Plane (backend and frontend)
- Private endpoints for Azure services: ADLS Gen2, Key Vault, Azure Monitor, Event Hubs
- Private DNS zones for name resolution within VNet
- Annotation: "Secure cluster connectivity via Private Link - all communication private"

ADLS Gen2 Storage:
- Storage accounts with hierarchical namespace enabled for Unity Catalog
- Network rules restricting access to specific VNets and private endpoints
- Customer-managed keys in Azure Key Vault for encryption
- Lifecycle management policies for cost optimization
- Soft delete and versioning for data protection

ExpressRoute:
- Azure ExpressRoute circuit (10 Gbps) to on-premises data center
- VNet Gateway in hub VNet
- Microsoft peering for private connectivity
- Redundant circuit for failover

**Cross-Cloud Networking (Center):**

Show cross-cloud connectivity options:

Option 1 - Internet-based with IPSec VPN: VPN gateway in each cloud connecting via internet, encrypted tunnels, lower performance but lower cost.

Option 2 - Confluent Private Backbone (Recommended): Show Confluent Cloud private network backbone connecting AWS VPC to Azure VNet, bypasses public internet entirely, used for Kafka cross-cloud replication, annotation "Enterprise clusters with PrivateLink on both ends".

Option 3 - Cloud Interconnect Services: AWS Direct Connect colocation facility connecting to Azure ExpressRoute via carrier, private Layer 2/3 connection, lowest latency option.

**On-Premises Data Center (Bottom):**

Show on-premises infrastructure: Oracle databases, file servers, Active Directory, existing applications. Display connections to both clouds via Direct Connect and ExpressRoute. Show BGP routing advertisements and private IP ranges. Include firewall and DMZ at edge.

**Security Zones:**

Color-code security zones:
- Red zone: Public internet (minimal exposure)
- Orange zone: DMZ and edge (firewalls)
- Yellow zone: Private subnets with outbound internet (NAT Gateway)
- Green zone: Fully private subnets (no internet)
- Blue zone: Databricks Control Plane (managed)

**Data Flow Paths:**

Show labeled data flow paths:

1. User to Workspace UI: User → Internet → Databricks Control Plane → PrivateLink/Private Link → Compute Plane (return path highlighted)

2. Cluster to S3/ADLS: Cluster in private subnet → VPC/Service endpoint → S3/ADLS (no internet traversal)

3. On-prem to Cloud: On-premises DB → Direct Connect/ExpressRoute → VPC/VNet → Databricks cluster

4. Cross-cloud replication: AWS cluster → S3 → Confluent Kafka → Azure Event Hubs → Azure cluster (all private network)

**Cost Optimization Annotations:**

Add cost callouts:
- "Local VPC endpoint: $0.01/GB" vs "Internet egress: $0.09/GB"
- "Direct Connect: Flat monthly fee + data transfer" vs "VPN: Free gateway + internet charges"
- "PrivateLink: $0.01/hour/endpoint + $0.01/GB processed"
- "Cross-region data transfer: $0.02/GB" vs "Cross-cloud: $0.09/GB"

**Monitoring and Observability:**

Show monitoring layer:
- VPC Flow Logs (AWS) → CloudWatch Logs → S3 → Athena for querying
- NSG Flow Logs (Azure) → Azure Monitor → Log Analytics
- Unified SIEM: All logs from both clouds aggregated to Splunk or Azure Sentinel
- Real-time alerting on anomalous network patterns

**Network Performance Metrics:**

Add performance indicators:
- Intra-AZ latency: < 1ms
- Inter-AZ latency: < 5ms
- Intra-region latency: < 10ms  
- Cross-region same cloud: ~50ms (us-east-1 to us-west-2)
- Cross-cloud: ~80ms (AWS us-east-1 to Azure East US 2)
- On-premises to cloud: ~30ms via Direct Connect

Use color coding: AWS orange for AWS networks, Azure blue for Azure networks, Purple (#6C3483) for Databricks Control Plane, Green (#27AE60) for private connections, Red (#E74C3C) for firewalls and security boundaries, Gray (#7F8C8D) for on-premises. Include network topology icons (routers, firewalls, gateways), cloud logos, Databricks logo, PrivateLink and ExpressRoute icons. Clear directional arrows for traffic flows with latency and cost labels.

Professional network architecture diagram style with detailed technical annotations, IP address space examples (10.0.0.0/16, 172.16.0.0/16), routing tables, and suitable for network engineering review.
```

**File Name**: `databricks-network-multicloud.png`

**Caption**: Multi-cloud network architecture for Databricks with private connectivity, hub-spoke topology, and cross-cloud networking options

---

## Prompt 4: Active-Passive Multi-Region Disaster Recovery Architecture

**Purpose**: Detailed DR architecture showing replication, failover, and failback mechanisms with 4-hour RTO

**Prompt**:
```
Create a comprehensive disaster recovery architecture diagram for Databricks showing active-passive multi-region deployment with detailed failover and failback mechanisms achieving 4-hour RTO. Use a side-by-side comparison layout with process flows.

**Left Side - Primary Region (Active): AWS us-east-1**

Show full active Databricks environment:

Workspace Layer:
- Production workspace with 50+ users actively developing and running jobs
- Multiple notebooks, SQL queries, and dashboards in active use
- Job scheduler running 200+ daily scheduled jobs
- Streaming pipelines continuously processing data

Unity Catalog Metastore:
- Primary metastore managing all catalogs: prod_catalog, analytics_catalog, ml_catalog
- Active users querying and accessing data
- Audit logs being generated in real-time
- Data lineage tracking all transformations

Compute Layer:
- 15 job clusters actively running production ETL workloads
- 5 all-purpose clusters for development (mark as "will not failover")
- 3 SQL warehouses (serverless) serving BI queries
- Delta Live Tables pipelines in continuous update mode

Data Layer:
- S3 buckets containing petabytes of Delta Lake tables
- Bronze layer: 10TB of raw data ingested daily
- Silver layer: 5TB of cleansed data
- Gold layer: 2TB of business-ready aggregates
- Change Data Feed enabled on all silver and gold tables

**Right Side - Secondary Region (Passive): Azure East US 2**

Show passive standby environment:

Workspace Layer:
- Standby workspace with identical configuration but minimal active usage
- Notebooks and code replicated but not executing
- Job definitions replicated but disabled
- Ready to activate within minutes

Unity Catalog Metastore:
- Secondary metastore with identical structure
- Catalogs and schemas mirrored from primary
- Permissions and grants synchronized
- Empty until failover (except replicated data)

Compute Layer:
- Minimal warm standby: 2 small clusters kept running for fast activation
- Pre-configured job cluster definitions ready to launch
- SQL warehouses in stopped state (can start in seconds with serverless)
- Instance pools pre-warmed with idle VMs for 2-minute cluster startup

Data Layer:
- ADLS Gen2 buckets receiving replicated Delta Lake tables
- Replication lag: < 15 minutes for silver/gold, 1 hour for bronze
- Incremental replication using Delta Lake Deep Clone
- Point-in-time consistency maintained

**Center - Replication Mechanisms:**

Show detailed replication flows with technologies:

1. Metastore Metadata Replication:
   - Custom scripts using Unity Catalog APIs
   - Sync frequency: Every 15 minutes
   - Items replicated: catalogs, schemas, tables, views, permissions
   - Technology: Python scripts + Databricks CLI
   - Annotation: "Metadata sync preserves governance structure"

2. Data Replication:
   - Delta Lake Deep Clone for incremental table replication
   - S3 → ADLS cross-cloud copy using AWS DataSync or Azure Data Factory
   - Replication modes: Full clone initially, incremental updates using Change Data Feed
   - Bandwidth: 10 Gbps dedicated for replication
   - Schedule: Silver/Gold every 15 minutes, Bronze every hour
   - Annotation: "Deep Clone provides point-in-time consistency and metadata preservation"

3. Workspace Configuration Replication:
   - Terraform state managing both regions
   - Git repositories (Azure DevOps/GitHub) storing all notebook code
   - Job definitions exported as JSON and version controlled
   - Cluster configurations as Terraform modules
   - Sync frequency: Real-time via Git commits
   - Technology: Terraform + Databricks Terraform provider

4. Secrets Replication:
   - AWS Secrets Manager → Azure Key Vault cross-cloud sync
   - Secret scopes created in both workspaces
   - Automated rotation synchronized
   - Technology: Custom Lambda/Function App

**Top - Failover Process (Numbered Steps):**

Show failover sequence with timeline:

T+0 (Detection): 
- Primary region outage detected by monitoring (AWS health dashboard, workspace unavailability)
- Automated alerts trigger incident response
- Decision to failover made by on-call architect

T+30 min (Activation):
- DNS/Global Load Balancer switched from primary to secondary endpoint
- Users redirected to Azure workspace (transparent to end users)
- Service principals credentials updated to use Azure workspace URL

T+60 min (Compute Activation):
- Warm standby clusters scaled up from 2 to 15 job clusters
- Instance pools provide rapid cluster launch (2-3 minutes per cluster)
- SQL warehouses started (serverless: instant start)

T+90 min (Job Resumption):
- Jobs resume from last successful checkpoint using replicated data
- Streaming jobs resume with Kafka offset preserved
- Delta Live Tables pipelines restarted from last update

T+240 min (Full Operation):
- All critical jobs running in DR region
- BI dashboards connected to DR SQL warehouses
- 4-hour RTO achieved
- Status: Fully operational on Azure

**Bottom - Failback Process (After Primary Recovery):**

Show failback sequence:

1. Primary Region Recovery Validated:
   - AWS region declares all-clear
   - Testing performed to confirm stability
   - Decision to failback made

2. Data Synchronization (Reverse):
   - Changes made in Azure during outage replicated back to AWS
   - Using same Deep Clone mechanism in reverse
   - Bi-directional sync ensures no data loss
   - Annotation: "Failback WITHOUT breaking governance or losing Azure-generated data"

3. Cutover Window:
   - Scheduled maintenance window announced to users
   - Brief pause in processing (15-30 minutes)
   - DNS switched back to AWS endpoint
   - Jobs migrated back to primary

4. Return to Normal State:
   - AWS primary region fully active
   - Azure returns to passive standby
   - Replication resumes primary → secondary direction
   - Post-incident review conducted

**Right Panel - DR Testing and Validation:**

Show testing cadence:

- Quarterly DR drills: Full failover and failback test (4-hour exercises)
- Monthly partial tests: Activate single job in DR region
- Weekly replication validation: Verify data consistency between regions
- Daily monitoring: Replication lag alerts if > 30 minutes

Results dashboard:
- Last DR test: Success, 3 hours 45 minutes to full operation
- Data loss: 12 minutes (acceptable within RPO)
- Issues identified: 2 job definitions not replicated, 1 secret missing (remediated)
- Confidence level: High

**Monitoring and Alerting:**

Show monitoring architecture:
- Primary and secondary regions monitored continuously
- Replication lag metrics: Target < 15 minutes, Alert at > 30 minutes
- AWS health API polled every 60 seconds
- Workspace availability checks every 5 minutes
- Automated failover triggers (optional): If primary unavailable > 20 minutes

**Cost Analysis Box:**

Show DR cost breakdown:
- Primary region (active): $50K/month (full production workload)
- Secondary region (passive standby):
  - Minimal compute: $2K/month (warm standby clusters)
  - Data storage (ADLS): $15K/month (replicated data)
  - Network egress (cross-cloud replication): $8K/month
  - Total DR cost: $25K/month (50% of primary)
- DR cost as % of primary: 50% (industry benchmark: 30-70%)
- Annotation: "Active-passive significantly cheaper than active-active (would be 100% duplicate)"

**RTO and RPO Metrics:**

Display targets and actuals:
- RTO (Recovery Time Objective): Target 4 hours, Actual 3h 45min
- RPO (Recovery Point Objective): Target 30 minutes, Actual 12 minutes
- Availability SLA: 99.95% (includes DR capability)

Use color coding: Green (#27AE60) for active systems, Amber (#F39C12) for warm standby, Gray (#95A5A6) for cold/disabled, Red (#E74C3C) for failure detection, Blue (#3498DB) for replication flows. Include AWS and Azure logos, Databricks logo, Delta Lake logo, Terraform logo. Clear timeline indicators, numbered process steps, and bidirectional replication arrows.

Add detailed technical annotations: "Deep Clone preserves Delta transaction log", "Terraform state stored in S3 with DynamoDB locking", "Cross-cloud replication uses TLS 1.3 encryption", "Metastore sync preserves column-level lineage".

Enterprise DR architecture style with detailed technical specifications, recovery procedures, and suitable for compliance documentation and disaster recovery planning.
```

**File Name**: `databricks-dr-active-passive.png`

**Caption**: Active-passive multi-region disaster recovery architecture for Databricks with 4-hour RTO, showing replication mechanisms and failover/failback procedures

---

## Prompt 5: Multi-Cloud FinOps Cost Optimization Architecture

**Purpose**: Cost optimization architecture showing workload placement, FinOps practices, and cost management across clouds

**Prompt**:
```
Create a detailed FinOps cost optimization architecture diagram for multi-cloud Databricks showing workload placement strategies, cost allocation, and optimization patterns. Use a matrix layout with workload types and cloud placement decisions.

**Top Section - Unified Cost Visibility Dashboard:**

Show consolidated FinOps dashboard displaying:
- Total Databricks spend across AWS and Azure: $180K/month
- Breakdown: AWS $120K (67%), Azure $60K (33%)
- Cost trend: 15% decrease month-over-month (optimization working)
- Budget vs. Actual: $200K budget, $180K actual (10% under budget)
- Top 5 cost drivers: Compute 65%, Storage 20%, Network egress 8%, Serverless SQL 5%, Other 2%

Integrated cost tools:
- AWS Cost Explorer feeding data via API
- Azure Cost Management feeding data via API
- Databricks System Tables (billing data) via SQL
- Unified in central dashboard (Grafana, Datadog, or CloudHealth)

**Matrix Layout - Workload Placement Decisions:**

Create matrix with workload types as rows, cloud placement as columns:

**Row 1: Production ETL Pipelines (Steady-State)**
- Placement: AWS us-east-1 (primary data lake location)
- Compute Strategy: Job Clusters with Reserved Instance backed (60% cost savings vs on-demand)
- Cluster Configuration: i3.2xlarge instances (cost-optimized for I/O)
- Instance Commitment: 1-year Reserved Instances + Savings Plan
- Actual Cost: $45K/month
- Optimization: Automated cluster termination, instance pools, spot instances for non-critical stages
- Rationale: "Data gravity - S3 data lake in AWS, minimize egress"

**Row 2: Real-Time Streaming Analytics**
- Placement: Azure East US 2 (near Azure Event Hubs source)
- Compute Strategy: Serverless Compute + Photon Engine
- Auto-scaling: 2-20 workers based on Event Hubs lag
- Actual Cost: $18K/month
- Optimization: Serverless eliminates idle time, pay-per-second billing
- Rationale: "Variable load - serverless optimal for unpredictable streaming volume"

**Row 3: ML Training and Experimentation**
- Placement: AWS us-west-2 (access to latest GPU instances)
- Compute Strategy: Spot Instances for training (70% cost savings)
- Cluster Configuration: p3.8xlarge (GPU) with spot bidding
- Fallback: On-demand if spot unavailable
- Actual Cost: $32K/month (would be $107K on-demand)
- Optimization: Checkpointing every 10 minutes, auto-restart on spot termination
- Rationale: "GPU availability and pricing better on AWS, spot acceptable for training"

**Row 4: BI and Analytics (SQL Workloads)**  
- Placement: Both AWS and Azure (multi-region for global access)
- Compute Strategy: Serverless SQL Warehouses  
- Warehouse sizing: Small (Europe), Medium (Americas), Large (Asia-Pacific) based on user load
- Auto-suspend: 10 minutes idle time
- Actual Cost: $22K/month
- Optimization: Serverless eliminates idle costs, rightsizing per region
- Rationale: "Serverless SQL provides instant start and pay-per-query model"

**Row 5: Development and Testing**
- Placement: Azure (cheaper compute for non-production)
- Compute Strategy: All-Purpose Clusters with auto-termination
- Scheduled shutdown: Non-business hours (weekends and nights)
- Cluster policy: Maximum 8 workers, auto-termination after 60 min idle
- Actual Cost: $8K/month (was $24K before optimization)
- Optimization: 70% cost reduction via scheduling and auto-termination
- Rationale: "Non-production - aggressive cost controls acceptable"

**Row 6: Data Science Notebooks (Ad-Hoc)**
- Placement: Both clouds (based on data location)
- Compute Strategy: Serverless Notebooks (GA 2025)
- On-demand small clusters with fast startup
- Actual Cost: $5K/month
- Optimization: No idle clusters, instant termination when notebook closed
- Rationale: "Unpredictable usage - serverless eliminates wasted spend"

**Right Panel - Cost Optimization Strategies:**

Show optimization techniques with impact:

1. Right-Sizing (Impact: 20% reduction)
   - AI-driven recommendations from Databricks System Tables
   - Before: i3.4xlarge clusters, After: i3.2xlarge (sufficient for 90% of jobs)
   - Monthly savings: $36K

2. Auto-Scaling (Impact: 15% reduction)
   - Dynamic worker allocation based on queue depth
   - Before: Fixed 20 workers, After: 5-20 workers auto-scale
   - Monthly savings: $27K

3. Spot Instances (Impact: 25% reduction for ML workloads)
   - 70% discount for interruptible compute
   - Checkpointing ensures fault tolerance
   - Monthly savings: $75K (on ML workloads specifically)

4. Serverless Adoption (Impact: 30% reduction for variable workloads)
   - Eliminated idle time for SQL and streaming
   - Pay-per-second granular billing
   - Monthly savings: $18K

5. Scheduled Cluster Termination (Impact: 70% reduction for dev/test)
   - Automated shutdown outside business hours (18:00-08:00, weekends)
   - Monthly savings: $16K (on dev/test environment)

6. Storage Lifecycle Management (Impact: 40% reduction in storage costs)
   - Bronze layer: Transition to S3 Intelligent-Tiering after 30 days
   - Archive old data to Glacier after 365 days
   - Monthly savings: $14K

7. Network Egress Optimization (Impact: 60% reduction in egress costs)
   - Minimize cross-cloud data transfers
   - Use local read pattern: replicate data to local cloud, read locally
   - Avoid cross-region BI queries (use local gold layer)
   - Monthly savings: $10K

**Bottom Section - Cost Allocation and Chargeback:**

Show cost allocation model:

Tagging Strategy (enforced via Terraform):
- Cost Center: Finance, Marketing, Product, Engineering
- Environment: prod, dev, test, staging
- Project: customer-360, fraud-detection, recommendation-engine
- Owner: email address of responsible team/person

Chargeback Model:
- Monthly cost reports per business unit
- Showback to teams for awareness
- Chargeback for production, showback for dev/test
- Shared costs (Unity Catalog, network) allocated by usage percentage

Cost Allocation Accuracy: 95% (5% untagged resources marked for deletion)

**Left Panel - FinOps Organizational Structure:**

Show cross-functional FinOps team:

- Finance Lead: Budget management, forecasting, variance analysis
- Engineering Lead: Technical optimization, cluster policies
- Business Lead: Prioritization, ROI analysis
- Cloud Architect (Databricks): Workload placement, architecture decisions

Meeting Cadence:
- Weekly: Review spend trends and anomalies
- Monthly: Cost allocation review and chargeback
- Quarterly: Budget planning and commitment purchases

**Center - Cost Anomaly Detection and Alerts:**

Show automated alerting:

Alert Types:
- Spend spike: > 20% increase day-over-day (triggers immediate investigation)
- Budget threshold: 80% of monthly budget consumed (early warning)
- Untagged resource: Any cluster/SQL warehouse without proper tags (auto-terminate after 24h)
- Idle resource: Cluster running with 0% utilization for > 1 hour (auto-terminate)
- Commitment under-utilization: Reserved capacity < 70% used (re-evaluate commitment)

Alerting Channels: Slack #finops-databricks, Email to cost center owners, PagerDuty for critical

**Top Right - Commitment Strategy:**

Show Reserved Instance/Savings Plan portfolio:

AWS Commitments:
- 1-year Reserved Instances: $50K/month commit (currently 85% utilized)
- 3-year Savings Plan: $25K/month commit (currently 92% utilized)
- On-demand buffer: $45K/month (for spikes and new workloads)

Azure Commitments:
- 1-year Reserved Instances: $30K/month commit (currently 78% utilized)
- On-demand buffer: $30K/month

Commitment Review: Quarterly reassessment based on usage trends

**Bottom Right - Cross-Cloud Cost Comparison:**

Show pricing comparison for identical workload:

Workload: 100-worker Databricks cluster running 8 hours/day

AWS Pricing:
- On-demand: $480/day = $14,400/month
- 1-yr Reserved: $192/day = $5,760/month (60% savings)
- Spot: $144/day = $4,320/month (70% savings)

Azure Pricing:
- On-demand: $460/day = $13,800/month (4% cheaper than AWS)
- 1-yr Reserved: $184/day = $5,520/month (4% cheaper than AWS)
- Spot: $138/day = $4,140/month (4% cheaper than AWS)

Decision: Place workload in AWS because data already in S3 (egress costs would negate Azure savings)

**Sustainability Metric (New in 2025):**

Show carbon footprint tracking:
- Total cloud carbon: 450 tons CO2/year
- Optimization reduced carbon by 15% (alongside cost reduction)
- Using AWS renewable energy regions where possible

Use color coding: Green (#27AE60) for optimized workloads, Amber (#F39C12) for partially optimized, Red (#E74C3C) for unoptimized/over-budget, Blue (#3498DB) for committed spend, Gray (#7F8C8D) for on-demand. Include Databricks logo, AWS and Azure logos, cost chart icons, dollar sign indicators. Clear cost flow diagrams and comparison tables.

Add financial annotations: "Reserved capacity delivers 60% ROI", "Spot instances require fault-tolerant design", "Serverless has 10% premium but eliminates idle waste", "Cross-cloud egress: $0.09/GB can exceed compute costs".

Enterprise FinOps architecture style with detailed cost breakdowns, optimization recommendations, and suitable for CFO and finance team presentations.
```

**File Name**: `databricks-finops-multicloud.png`

**Caption**: Multi-cloud FinOps cost optimization architecture showing workload placement, commitment strategies, and cost reduction techniques for Databricks

---

## Prompt 6: Cross-Cloud Event-Driven Integration Architecture

**Purpose**: Event-driven data integration across clouds using Kafka, Event Hubs, and Databricks Structured Streaming

**Prompt**:
```
Create a detailed event-driven architecture diagram for cross-cloud data integration showing Kafka/Confluent streaming across AWS and Azure consumed by Databricks. Use a horizontal event flow layout with clear event routing patterns.

**Left Section - Event Sources (Multi-Cloud):**

AWS Event Sources:
- Amazon Kinesis Data Streams: IoT sensor data from manufacturing devices (1M events/second)
- AWS S3 Event Notifications: File arrival events triggering processing
- AWS DynamoDB Streams: Change data capture from transactional databases
- Custom applications publishing to Kafka topics via producer API

Azure Event Sources:
- Azure Event Hubs: Web clickstream data from customer applications (500K events/second)
- Azure Service Bus: Order processing events from e-commerce platform
- Azure Blob Storage events: Data file uploads triggering workflows
- Power Apps publishing business events

On-Premises Sources:
- Legacy mainframe CDC (Change Data Capture) streamed via Kafka Connect
- Oracle GoldenGate streaming database changes
- File-based events from FTP servers

**Center - Confluent Cloud Event Backbone:**

Show Confluent Cloud as central event streaming platform spanning AWS and Azure:

AWS Enterprise Cluster (us-east-1):
- Kafka cluster with PrivateLink connectivity to AWS VPC
- 12 brokers across 3 availability zones
- Replication factor: 3 for durability
- Topics: iot-sensor-raw, s3-file-events, dynamodb-cdc, application-events
- Retention: 7 days (for reprocessing and replay)

Azure Enterprise Cluster (East US 2):
- Kafka cluster with Private Link connectivity to Azure VNet
- 12 brokers across 3 availability zones
- Topics: clickstream-raw, order-events, blob-storage-events, powerapp-events

Cross-Cloud Cluster Linking:
- Confluent Cluster Linking connecting AWS cluster to Azure cluster
- Private network replication via Confluent backbone (no public internet)
- Offset-preserving replication for exactly-once semantics
- Bi-directional mirroring: AWS topics mirrored to Azure, Azure topics mirrored to AWS
- Latency: 50-100ms cross-cloud replication lag
- Annotation: "First and only platform with private cross-cloud replication"

Schema Registry (Global):
- Centralized schema registry managing event schemas across both clouds
- Schema evolution with backward/forward compatibility
- Schema Linking keeping schemas synchronized across clusters
- Versioned schemas for iot-sensor-events v1, v2, v3

**Right Section - Databricks Consumption (Multi-Cloud):**

AWS Databricks Consumption (us-east-1):

Structured Streaming Jobs:
- Consuming iot-sensor-raw topic from local AWS Kafka cluster
- Exactly-once semantics with idempotent writes to Delta Lake
- Watermarking: 10-minute late event tolerance
- Checkpoint location in S3 for fault tolerance
- Microbatch processing: 30-second intervals

Processing Logic:
- Stateful aggregations: Session windows for sensor grouping
- Stream-stream joins: Enriching sensor data with device metadata
- Anomaly detection: ML model scoring in real-time
- Complex event processing: Detecting multi-event patterns

Output:
- Bronze layer: Raw events written to Delta tables (append-only)
- Silver layer: Aggregated and enriched data (merge operations for deduplication)
- Real-time dashboards: Databricks SQL serving live metrics
- Alerts: Publishing critical events back to Kafka topic for downstream consumers

Azure Databricks Consumption (East US 2):

Structured Streaming Jobs:
- Consuming clickstream-raw topic from local Azure Kafka cluster
- Also consuming mirrored iot-sensor-raw topic (cross-cloud) for unified analysis
- Auto Loader monitoring Azure Blob Storage for file-based events
- Delta Live Tables pipeline for declarative streaming ETL

Processing Logic:
- Session reconstruction: Stitching clickstream events into user sessions
- Real-time personalization: Scoring recommendation models on live clickstream
- Fraud detection: ML model identifying suspicious orders in real-time
- Data quality: Expectations enforcing schema and business rules

Output:
- Silver layer: Cleansed clickstream and order data
- Gold layer: Customer 360 view combining web activity and orders
- Feature Store: Real-time features for ML models (user behavior, purchase history)
- Delta Sharing: Sharing aggregated clickstream metrics with partner companies

**Top Section - Event-Driven Orchestration:**

Show event-driven workflow triggers:

Event-Triggered Databricks Jobs:
- S3 file arrival → Lambda function → Databricks Jobs API → Start processing job
- Kafka event threshold reached → Databricks Auto Loader → Incremental load
- Azure Function monitoring Event Hubs lag → Trigger scale-up of Databricks cluster

Event-Driven ML Pipeline:
1. New training data arrives in S3/ADLS (event published)
2. Databricks job triggered to retrain model
3. Model registered in MLflow Model Registry (event published)
4. Automated testing job triggered
5. If tests pass, model promoted to production (event published)
6. Model Serving endpoint updated (event published)
7. Monitoring job activated to track model performance

Annotation: "Fully event-driven - zero scheduled jobs, all triggered by events"

**Bottom Section - Event Streaming Patterns:**

Show streaming patterns implemented:

Pattern 1: Event Sourcing
- All state changes captured as immutable events
- Delta Lake as event store with time travel
- Replay capability for debugging and reprocessing
- Event log retention: 90 days

Pattern 2: CQRS (Command Query Responsibility Segregation)
- Write events to Kafka (command side)
- Read from materialized Delta Lake views (query side)
- Eventual consistency acceptable (5-minute lag typical)

Pattern 3: Saga Pattern (Distributed Transactions)
- Multi-step business process coordinated via events
- Example: Order placement → Inventory check → Payment → Fulfillment
- Compensation events for rollback on failure

Pattern 4: Event-Driven Microservices
- Databricks jobs as event-driven microservices
- Each job subscribes to relevant Kafka topics
- Publish processed results back to Kafka for downstream consumers
- Decoupled architecture enabling independent scaling

**Center Bottom - Event Quality and Governance:**

Schema Validation:
- All events validated against Schema Registry before processing
- Invalid events routed to dead-letter queue (DLQ) topic
- Schema evolution tracked with lineage in Unity Catalog

Event Lineage:
- Unity Catalog tracking event flow: Source → Topic → Databricks job → Delta table → Dashboard
- Column-level lineage showing event field transformations
- Bi-directional lineage: trace dashboards back to source events

Data Quality Metrics:
- Event arrival rate: 1.5M events/second total
- Processing lag: < 2 minutes (p99)
- Duplicate rate: 0.01% (filtered via deduplication)
- Schema violation rate: 0.5% (routed to DLQ)
- Data quality score: 99.5%

**Right Panel - Cross-Cloud Event Disaster Recovery:**

Disaster Recovery Pattern:
- Primary processing in AWS (active)
- Kafka topics mirrored to Azure via Cluster Linking
- Databricks jobs in Azure on standby (passive)
- On AWS outage: Azure jobs automatically activated via Kafka consumer group failover
- RTO: 15 minutes (jobs resume from last committed offset)
- RPO: 0 (no data loss due to offset preservation)

Failover Testing:
- Monthly DR drill: Simulate AWS outage, activate Azure processing
- Validate: Offset preservation, exactly-once semantics, zero data loss
- Last test: Success, 12-minute failover time

**Left Panel - Performance and Scalability:**

Kafka Cluster Sizing:
- Throughput: 150 MB/second per broker
- Total capacity: 1.8 GB/second across 12 brokers (sufficient for 1.5M events/sec)
- Auto-scaling: Confluent automatically adds brokers at 70% capacity

Databricks Auto-Scaling:
- Structured Streaming clusters auto-scale from 5-50 workers based on Kafka lag
- Trigger: If lag > 5 minutes, add 5 workers
- Scale down: If lag < 2 minutes for 10 minutes, remove 5 workers
- Cost optimization: Right-sized for actual event volume

Partitioning Strategy:
- Kafka topics partitioned by event key (user_id, device_id)
- 100 partitions per topic for parallelism
- Databricks Structured Streaming: 1 task per partition (100 tasks)
- Linear scalability proven up to 500 partitions

**Top Right - Cost Analysis:**

Event Streaming Costs:
- Confluent Cloud (AWS + Azure): $35K/month
- Cross-cloud Cluster Linking: $8K/month
- Network egress (cross-cloud): $12K/month
- Total Kafka infrastructure: $55K/month

Databricks Consumption Costs:
- Streaming job clusters: $40K/month (job clusters with auto-termination)
- Serverless DLT pipelines: $15K/month
- Total Databricks streaming: $55K/month

Combined Event Architecture: $110K/month
- Processing 1.5M events/sec = $0.000002 per event
- Cost-effective compared to batch processing alternative

Use color coding: Orange (#E67E22) for Kafka/event streams, Databricks red-orange (#FF3621), AWS orange, Azure blue, Green (#27AE60) for active processing, Gray (#95A5A6) for standby/passive. Include Confluent logo, Kafka logo, Databricks logo, Delta Lake logo, cloud provider logos. Clear event flow arrows with throughput labels, latency indicators, and data volume metrics.

Add technical annotations: "Exactly-once semantics via Kafka transactions + Delta ACID", "Watermarking handles late events up to 10 minutes", "Cluster Linking preserves offsets for seamless failover", "Structured Streaming microbatches provide near real-time processing with exactly-once guarantees".

Modern event-driven architecture style with detailed streaming patterns, technical specifications, and suitable for real-time data engineering presentations.
```

**File Name**: `databricks-event-driven-multicloud.png`

**Caption**: Cross-cloud event-driven integration architecture using Confluent Kafka with private network replication and Databricks Structured Streaming consumption

---

## Prompt 7: Infrastructure as Code (Terraform) Multi-Cloud Provisioning

**Purpose**: IaC architecture showing Terraform-based multi-cloud Databricks provisioning with policy enforcement

**Prompt**:
```
Create a detailed Infrastructure as Code architecture diagram showing Terraform-based multi-cloud Databricks provisioning with GitOps workflow and policy enforcement. Use a CI/CD pipeline layout with IaC components.

**Top Section - Source Control and Collaboration:**

GitHub Enterprise Repository:
- Mono-repo structure: databricks-infrastructure/
- Directories: aws/, azure/, modules/, policies/, environments/
- Branching strategy: main (production), develop (staging), feature branches
- Code owners: CODEOWNERS file requiring architect approval for changes
- Pull request workflow: Feature branch → PR → Reviews → Automated tests → Merge

Team Collaboration:
- 5 cloud architects committing IaC code
- 20 data engineers using Terraform modules
- Automated PR comments from Terraform Cloud showing plan previews
- Slack integration notifying #databricks-infra channel of changes

**Left Pipeline - AWS Provisioning Workflow:**

Stage 1 - Code Commit:
- Engineer commits Terraform code for new Databricks workspace
- Code: HCL defining workspace, clusters, Unity Catalog resources
- Example module:
  ```
  module "databricks_workspace" {
    source = "./modules/workspace"
    cloud_provider = "aws"
    region = "us-east-1"
    workspace_name = "prod-analytics"
  }
  ```

Stage 2 - CI Pipeline (GitHub Actions):
- Automated trigger on PR creation
- Terraform fmt check (code formatting)
- Terraform validate (syntax validation)
- TFLint static analysis (best practices)
- Checkov security scanning (misconfigurations)
- OPA (Open Policy Agent) policy validation
- KICS (Keeping Infrastructure as Code Secure) scanning

Policy Checks:
- Policy 1: Cluster cannot exceed 50 workers (cost control)
- Policy 2: All resources must have cost_center tag
- Policy 3: Public IPs on clusters denied (security)
- Policy 4: Only approved Databricks runtime versions (compliance)
- Policy 5: SQL warehouses must use serverless (cost optimization)
- Result: Pass/Fail with detailed violation report

Stage 3 - Terraform Plan:
- Terraform Cloud executes plan remotely
- Shows resources to be created, modified, destroyed
- Cost estimation: Infracost tool estimates monthly cost impact
- Plan output commented on PR for reviewer visibility
- Example output: "+15 to add, 2 to change, 0 to destroy, Est. cost: +$5K/month"

Stage 4 - Manual Approval:
- Cloud architect reviews plan and approves
- Cost impact reviewed against budget
- Security posture validated
- Merge approved if all checks pass

Stage 5 - Terraform Apply (Auto-triggered on Merge to Main):
- Terraform Cloud executes apply
- Resources provisioned in AWS:
  - Databricks workspace created
  - Unity Catalog metastore registered
  - Job clusters configured with policies
  - S3 buckets for Unity Catalog created
  - IAM roles and trust relationships established
  - PrivateLink VPC endpoints configured
- Apply duration: ~15 minutes
- State file stored in remote backend (S3 with DynamoDB locking)

Stage 6 - Post-Deployment:
- Automated testing: Terraform test executes validation scripts
- Workspace connectivity test: curl workspace URL
- Unity Catalog test: Query system tables
- Notification: Slack message with workspace URL and login instructions
- Documentation: Auto-generated README with Terraform outputs

**Right Pipeline - Azure Provisioning Workflow:**

Identical stages but Azure-specific resources:
- Azure Databricks workspace with VNet injection
- Private Link private endpoints
- Azure Key Vault for secrets
- ADLS Gen2 storage accounts
- Managed Identities for authentication
- Network security groups and rules

Same Terraform modules with cloud-specific providers:
```
module "databricks_workspace" {
  source = "./modules/workspace"
  cloud_provider = "azure"
  region = "eastus2"
  workspace_name = "prod-analytics"
}
```

Annotation: "Same module code, different provider - 95% code reuse across clouds"

**Center - Terraform Module Library:**

Show reusable module components:

Core Modules:
- workspace: Creates Databricks workspace with networking
- unity-catalog: Configures metastore, catalogs, schemas
- cluster-policy: Defines cluster policies enforcing governance
- job: Creates Databricks job with cluster configuration
- sql-warehouse: Creates serverless SQL warehouse
- secret-scope: Creates secret scope with AWS/Azure backing

Module Inputs (Standardized):
- cloud_provider: aws | azure
- environment: prod | dev | staging
- cost_center: finance | marketing | engineering
- workspace_name: string
- tags: map of key-value pairs

Module Outputs:
- workspace_id: used by dependent modules
- workspace_url: for user access
- metastore_id: for Unity Catalog resources

**Bottom Section - State Management and Collaboration:**

Remote State Backend:
- Terraform Cloud workspace per environment
- State locking prevents concurrent modifications
- Encrypted state storage
- State versioning for rollback capability
- Run history for audit trail

Cross-Cloud State Sharing:
- AWS workspace outputs consumed by Azure resources
- Example: Unity Catalog metastore ID from AWS used in Azure Delta Sharing config
- Remote state data sources enable cross-cloud dependencies

Workspace Organization:
- databricks-aws-prod: Production AWS resources
- databricks-azure-prod: Production Azure resources
- databricks-aws-dev: Development AWS resources
- databricks-azure-dev: Development Azure resources

**Left Bottom - Policy as Code (OPA):**

Show Open Policy Agent integration:

Policy File Example:
```
# Deny clusters without auto-termination
deny[msg] {
  input.resource_type == "databricks_cluster"
  not input.autotermination_minutes
  msg = "Clusters must have auto-termination configured"
}

# Enforce tagging
deny[msg] {
  input.resource_type == "databricks_workspace"
  not input.tags.cost_center
  msg = "All resources must have cost_center tag"
}
```

Policy Enforcement Results:
- Policies evaluated on every PR
- Violations block merge to main branch
- Exception process: Architect can override with justification
- Policy audit log tracks all evaluations

**Right Bottom - Multi-Cloud Resource Provisioning:**

Show resources being provisioned across clouds in single Terraform apply:

Resources Created (Single Plan):
AWS:
- 1x Databricks workspace (us-east-1)
- 1x Unity Catalog metastore
- 3x S3 buckets (managed, external, logs)
- 5x IAM roles
- 2x PrivateLink endpoints

Azure:
- 1x Databricks workspace (East US 2)
- 1x Unity Catalog metastore
- 2x ADLS Gen2 storage accounts
- 3x Managed Identities
- 2x Private endpoints

Unity Catalog Cross-Cloud:
- Delta Sharing share from AWS to Azure
- Recipient configuration in Azure metastore

Total: 20 resources across 2 clouds, provisioned in 18 minutes

Annotation: "Idempotent: Re-running apply makes no changes if no code changes"

**Top Right - Terraform Providers:**

Show provider configuration:

```
terraform {
  required_providers {
    databricks = {
      source = "databricks/databricks"
      version = "~> 1.30"
    }
    aws = {
      source = "hashicorp/aws"
      version = "~> 5.0"
    }
    azurerm = {
      source = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "databricks" {
  alias = "aws_workspace"
  host = "https://dbc-abc123.cloud.databricks.com"
  account_id = "xxxx-xxxx-xxxx"
}

provider "databricks" {
  alias = "azure_workspace"
  host = "https://adb-1234.azuredatabricks.net"
  account_id = "yyyy-yyyy-yyyy"
}
```

Multi-Provider Pattern: Provider aliases for multiple Databricks workspaces

**Center Top - Cost Estimation Integration:**

Infracost Output in PR Comment:
```
Monthly cost estimate: $12,450 → $17,680 (+$5,230/+42%)

Resource changes:
+ databricks_cluster.ml_cluster: +$4,200/month (20 i3.2xlarge instances)
+ databricks_sql_endpoint.analytics: +$1,030/month (Medium serverless)

Budget: $25,000/month
New total: $17,680 (71% of budget)
Status: ✅ Within budget
```

Approval Decision: Cost acceptable, architect approves

**Far Right - Disaster Recovery IaC:**

Terraform manages DR replication scripts:
- Provisioned Lambda functions (AWS) and Azure Functions for metastore sync
- S3-to-ADLS data replication jobs configured
- Scheduled based on Terraform-defined cron expressions
- All DR infrastructure versioned and reproducible

DR Testing Automation:
- Terraform module: dr-failover-test
- Creates temporary standby workspace, runs failover simulation, tears down
- Executed monthly as part of DR validation
- Results logged and reported

Use color coding: Purple (#8E44AD) for Terraform, Blue (#3498DB) for CI/CD pipeline, Green (#27AE60) for passed validations, Red (#E74C3C) for failed policies, AWS orange, Azure blue, Databricks red-orange. Include Terraform logo, GitHub logo, Databricks logo, OPA logo, cloud provider logos. Clear pipeline flow arrows, stage transitions, and automated decision points.

Add technical annotations: "HCL declarative syntax ensures idempotency", "Remote state backend prevents conflicts", "Policy as Code enforces governance at deployment time", "GitOps workflow provides full audit trail and rollback capability", "Same module provisions identically across clouds".

Professional DevOps architecture style with detailed CI/CD workflows, code samples, and suitable for platform engineering presentations.
```

**File Name**: `databricks-terraform-iac.png`

**Caption**: Infrastructure as Code architecture for multi-cloud Databricks provisioning using Terraform with GitOps workflow and policy enforcement

---

## Prompt 8: Unified Observability and Monitoring Architecture

**Purpose**: Cross-cloud monitoring, logging, and observability for Databricks with centralized SIEM

**Prompt**:
```
Create a comprehensive observability and monitoring architecture diagram for multi-cloud Databricks showing unified monitoring, centralized logging, and SIEM integration. Use a layered telemetry collection approach.

**Bottom Layer - Telemetry Sources (Multi-Cloud):**

AWS Databricks Telemetry:
- Databricks Audit Logs: Workspace access, job execution, table queries, notebook runs
- Cluster Metrics: CPU, memory, disk I/O, network throughput per node
- Job Metrics: Job duration, success/failure, data processed, cluster utilization
- SQL Warehouse Metrics: Query count, query duration, cache hit rate, concurrency
- Delta Lake Metrics: Table operations, compaction activity, Z-order operations
- Spark Metrics: Executor memory, shuffle read/write, stage completion times
- System Tables: Billing usage, compute usage, lineage, audit logs
- CloudWatch Logs: VPC Flow Logs, PrivateLink logs, Lambda logs
- AWS Cost Explorer: Resource-level cost data

Azure Databricks Telemetry:
- Identical Databricks telemetry categories
- Azure Monitor Logs: VNet NSG Flow Logs, Private Link logs, Function App logs
- Azure Cost Management: Resource-level cost data

On-Premises Sources:
- Network device logs, application logs, database logs

**Second Layer - Collection and Aggregation:**

AWS Collection:
- CloudWatch Logs receiving Databricks audit logs via streaming
- CloudWatch Metrics receiving cluster and job metrics
- S3 bucket storing raw log files (long-term retention)
- Kinesis Data Firehose streaming logs to centralized platform

Azure Collection:
- Azure Monitor receiving Databricks diagnostic logs
- Log Analytics Workspace aggregating all Azure telemetry
- ADLS Gen2 storing raw log files (long-term retention)
- Event Hubs streaming logs to centralized platform

Databricks System Tables:
- SQL queries extracting audit, lineage, and billing data
- Incremental Delta Live Tables pipelines processing system tables
- Gold layer aggregates: daily usage by workspace, monthly cost by cost center

**Third Layer - Centralized SIEM and Analytics Platform:**

Show SIEM platform (Splunk or Azure Sentinel) as central hub:

Splunk Enterprise:
- Universal Forwarders installed collecting from all sources
- Index: databricks_aws (AWS telemetry)
- Index: databricks_azure (Azure telemetry)
- Index: databricks_audit (unified audit logs)
- Index: databricks_cost (cost and billing data)

Data Ingestion Rate:
- 500 GB/day total log volume
- 10,000 events/second peak
- 90-day retention in hot storage, 2-year retention in cold (S3/ADLS)

Security Analytics:
- UEBA (User and Entity Behavior Analytics) detecting anomalies
- Threat intelligence feed correlation
- Alerts on suspicious activity: unusual data access, off-hours usage, privilege escalation

**Fourth Layer - Dashboards and Visualization:**

Show multiple dashboard categories:

Operational Dashboards (Grafana):

Dashboard 1: Cluster Health
- Metrics: Active clusters, CPU utilization heatmap, memory usage, disk I/O
- Per-cluster drill-down showing node-level metrics
- Alert indicators for unhealthy clusters (>90% CPU for >10 min)

Dashboard 2: Job Performance
- Job success rate: 98.5% (target >98%)
- Average job duration trend (weekly)
- Top 10 longest-running jobs
- Failed jobs in last 24 hours with error details

Dashboard 3: Data Pipeline Health
- Delta Live Tables pipeline status (green/amber/red)
- Data freshness: Time since last successful update per table
- Expectation violations: Data quality rule failures
- Row counts and data volume processed

Dashboard 4: SQL Warehouse Performance
- Query throughput: Queries per minute
- Query latency: p50, p90, p99 percentiles
- Cache hit ratio: 75% (target >70%)
- Warehouse utilization and auto-scaling activity

Cost Dashboards (Databricks SQL / Power BI):

Dashboard 5: Multi-Cloud Cost Overview
- Total spend trend: $180K/month current, 15% down from prior month
- Cost by cloud: AWS 67%, Azure 33%
- Cost by cost center: Finance 35%, Marketing 25%, Product 20%, Engineering 20%
- Budget variance: $20K under budget (10%)

Dashboard 6: Resource-Level Cost Breakdown
- Top 10 most expensive clusters (with utilization metrics)
- Idle resource waste: $12K/month identified
- Compute vs storage vs network cost split
- Spot instance savings realized: $75K/month

Security Dashboards (Splunk / Sentinel):

Dashboard 7: Access and Authentication
- Login attempts and failures
- MFA enrollment rate: 98% (target 100%)
- Service principal usage
- Unusual access patterns flagged

Dashboard 8: Data Access Audit
- Sensitive table access events (PII, confidential data)
- Large data exports (>1 million rows)
- Cross-account/cross-cloud data access
- Unity Catalog permission changes

Data Quality Dashboards (Monte Carlo / Great Expectations):

Dashboard 9: Data Quality Score
- Overall data quality: 99.2%
- Schema change detection: 3 unexpected changes in last week
- Freshness SLA: 99.5% of tables updated within SLA
- Volume anomalies: 2 tables with unexpected row count changes

**Fifth Layer - Alerting and Incident Response:**

Alert Rules and Channels:

Critical Alerts (PagerDuty):
- Workspace unavailable >5 minutes → Page on-call engineer
- Job failure rate >10% in 1 hour → Page data engineering lead
- Data quality score drop >5 points → Page data governance team
- Security breach detected → Page security ops

Warning Alerts (Slack #databricks-ops):
- Cluster CPU >85% for >15 minutes
- Storage cost increase >20% week-over-week
- Table not updated in expected timeframe (freshness SLA miss)
- Unexpected schema change detected

Informational Alerts (Email):
- Daily summary: Jobs run, success rate, data processed
- Weekly cost report by cost center
- Monthly capacity planning report

Incident Response Workflow:
1. Alert triggered and routed to appropriate channel
2. On-call engineer acknowledges and begins investigation
3. Runbook automatically attached to alert with common remediation steps
4. Incident logged in ServiceNow with severity classification
5. Root cause analysis performed using logs and metrics
6. Post-incident review and runbook updates

**Right Panel - AI-Driven Insights (2025 Emerging):**

Machine Learning on Observability Data:

Anomaly Detection:
- ML model trained on historical metrics detecting unusual patterns
- Anomaly types: Cost spikes, performance degradation, unusual access patterns
- Predictive alerting: Warn before problem becomes critical

Capacity Planning:
- Time series forecasting predicting future resource needs
- Recommendation: "Add 5 reserved instances in next quarter based on trend"

Performance Optimization:
- AIOps platform (Datadog, Dynatrace) analyzing metrics
- Recommendations: "Cluster XYZ underutilized, recommend downsizing from Large to Medium"

Cost Optimization:
- AI-driven cost anomaly detection
- Automated rightsizing recommendations with projected savings

**Left Panel - Unified Correlation and Investigation:**

Cross-Cloud Log Correlation:

Scenario: Slow query performance reported by users

Investigation Flow:
1. Query Databricks SQL warehouse metrics: High query latency detected
2. Correlate with cluster metrics: CPU at 95%, memory pressure
3. Check Unity Catalog audit logs: Identify user and query text
4. Examine Delta Lake metrics: Large table scan without optimization
5. Review network logs: No network issues detected
6. Root cause: Missing Z-order index on frequently queried column
7. Remediation: Run OPTIMIZE ZORDER command, query performance restored
8. Duration: 15 minutes from alert to resolution

Unified Investigation UI:
- Single pane of glass showing correlated data from all sources
- Timeline view of events leading to incident
- Automated correlation using common identifiers (cluster_id, job_id, user_id)

**Bottom Right - Compliance and Audit Reporting:**

Audit Reports (Automated):

SOC 2 Compliance Report:
- Monthly report showing: All administrative actions, data access to sensitive tables, permission changes, failed login attempts
- Evidence: Unity Catalog audit logs timestamped and immutable
- Distribution: Compliance team, external auditors

GDPR Data Access Report:
- User data access requests processed
- Data deletion requests completed
- Cross-border data transfer logs (cross-cloud access)
- Retention policy enforcement validation

Regulatory Reporting:
- Financial services: FINRA, SEC data retention compliance
- Healthcare: HIPAA audit logs for PHI access
- Automated report generation from Unity Catalog audit logs

**Center - SLA Monitoring:**

SLA Tracking:

Availability SLA:
- Target: 99.9% uptime
- Current: 99.95% (exceeding target)
- Downtime: 4.3 hours year-to-date (allowable: 8.76 hours/year)

Performance SLA:
- Job completion within 4 hours: 99.2% (target 98%)
- Query response <10 seconds: 97% (target 95%)
- Data freshness <1 hour: 99.5% (target 99%)

Data Quality SLA:
- Overall data quality >99%: Met
- Schema stability: 99.8% (3 unexpected changes)
- Completeness: 99.9% (null rate <0.1%)

Use color coding: Blue (#3498DB) for AWS metrics, Azure blue for Azure metrics, Purple (#8E44AD) for Databricks, Green (#27AE60) for healthy status, Amber (#F39C12) for warnings, Red (#E74C3C) for critical alerts. Include Splunk/Sentinel logo, Grafana logo, Databricks logo, cloud provider logos, monitoring tool logos (Datadog, Dynatrace). Clear telemetry flow arrows, dashboard mockups, and alert routing diagrams.

Add technical annotations: "CloudWatch Logs to Splunk via Kinesis Firehose", "Azure Monitor to Sentinel native integration", "Unity Catalog System Tables queried every 15 minutes", "UEBA detects anomalous behavior using ML baseline", "Cross-cloud correlation via shared event_id and timestamp".

Enterprise observability architecture style with detailed monitoring patterns, metrics definitions, and suitable for SRE and platform operations presentations.
```

**File Name**: `databricks-observability-multicloud.png`

**Caption**: Unified observability and monitoring architecture for multi-cloud Databricks with centralized SIEM, AI-driven insights, and comprehensive alerting

---

## Prompt 9: End-to-End Medallion Pipeline with Cross-Cloud Replication

**Purpose**: Detailed medallion architecture with cross-cloud data replication and consumption patterns

**Prompt**:
```
Create a detailed end-to-end medallion architecture diagram showing Bronze-Silver-Gold data flow with cross-cloud replication and diverse consumption patterns. Use horizontal layered approach with data flow from left to right.

**Far Left - Diverse Data Sources:**

Cloud Sources (AWS):
- S3 buckets: JSON files (web logs), Parquet files (historical data), CSV files (flat file feeds)
- RDS PostgreSQL: Transactional database with CDC via Debezium
- DynamoDB Streams: Real-time change capture
- Kinesis Data Streams: IoT sensor data (1M events/second)

Cloud Sources (Azure):
- ADLS Gen2: Compressed CSV files from partner systems
- Azure SQL Database: Operational data with change tracking
- Event Hubs: Clickstream data from web applications
- Blob Storage: Unstructured documents (PDFs, images)

SaaS Sources:
- Salesforce: CRM data via Fivetran connector
- SAP: ERP data via HANA Cloud connector
- Workday: HR data via REST API
- Google Analytics: Web analytics via API

On-Premises Sources:
- Oracle database: Legacy ERP via GoldenGate CDC
- File servers: Daily batch files via SFTP
- Mainframe: VSAM files converted to sequential

**Bronze Layer - Raw Ingestion (Immutable Append):**

AWS Bronze (us-east-1):

Ingestion Mechanisms:
- Auto Loader (Incremental File Processing): Monitors S3 paths, infers schema automatically, handles schema evolution
- Structured Streaming: Consumes from Kinesis with exactly-once semantics
- Fivetran: Syncs Salesforce data hourly with CDC
- JDBC Batch: Daily full refresh of reference tables

Bronze Tables:
- bronze.raw_web_logs: 100M rows/day, partitioned by date, 30-day retention then archive to Glacier
- bronze.raw_iot_sensors: 500M events/day, liquid clustering on device_id and timestamp
- bronze.raw_salesforce_accounts: 1M rows, SCD Type 1 full snapshot
- bronze.raw_postgres_orders: 10M rows/day, CDC with insert/update/delete operations

Characteristics:
- Schema on read (flexible schema)
- Append-only writes (no updates/deletes)
- Full historical audit trail
- External volumes for unstructured data (PDFs stored as files, metadata in tables)
- Retention: 7 years for compliance

Compute:
- Serverless compute for Auto Loader (pay-per-file-processed)
- Job clusters for streaming (auto-scaling 5-25 workers)
- Cost: $25K/month

Azure Bronze (East US 2):

Similar structure but Azure-native sources:
- bronze.raw_clickstream: 200M events/day from Event Hubs
- bronze.raw_documents: Metadata for unstructured files in Blob Storage
- bronze.raw_erp_data: SAP HANA data synced hourly

**Silver Layer - Cleansed and Conformed:**

AWS Silver (us-east-1):

Transformation Logic (Delta Live Tables):

Pipeline 1: Web Logs Cleansing
- Input: bronze.raw_web_logs
- Transformations:
  - Deduplication: Remove duplicate events using session_id + timestamp
  - Null handling: Fill missing user_agent with "Unknown"
  - Data type casting: Parse timestamp strings to timestamp type
  - Business rule validation: Expectation "page_load_time < 60 seconds"
  - Invalid rows routed to silver.quarantine_web_logs
- Output: silver.web_sessions (sessionized clickstream data)
- Freshness: 15-minute latency from bronze to silver

Pipeline 2: Order Processing
- Input: bronze.raw_postgres_orders + bronze.raw_salesforce_accounts
- Transformations:
  - Join operations: Enrich orders with account information
  - SCD Type 2: Track historical changes to customer records with valid_from/valid_to
  - Change Data Feed (CDF): Enable for downstream incremental processing
  - Standardized schemas: Convert all currency to USD, all dates to UTC
- Output: silver.orders_enriched, silver.customers_scd2
- Freshness: 30-minute latency

Data Quality Checks (Great Expectations):
- Expectation: orders.customer_id must exist in customers table (referential integrity)
- Expectation: orders.amount > 0 (business rule)
- Expectation: orders.order_date <= current_date (future dates invalid)
- Violation handling: Failed rows quarantined, alert sent to data engineering team

Silver Tables:
- silver.web_sessions: 50M rows/day (deduplicated from 100M bronze)
- silver.orders_enriched: 9.5M rows/day (98% pass quality checks)
- silver.customers_scd2: 5M rows with historical versions
- silver.iot_sensors_aggregated: 10M rows/day (aggregated from 500M events)

Characteristics:
- MERGE operations for upserts (slowly changing dimensions)
- Change Data Feed enabled for incremental downstream processing
- Data quality expectations enforced
- Standardized schemas and naming conventions
- Z-order indexing on frequently filtered columns

Compute:
- Delta Live Tables serverless pipelines (enhanced autoscaling)
- Cost: $35K/month

Azure Silver (East US 2):

Similar transformations on Azure data sources:
- silver.clickstream_sessions: Sessionized web activity
- silver.erp_transactions: Validated and standardized ERP data

**Gold Layer - Business-Ready Analytics:**

AWS Gold (us-east-1):

Dimensional Modeling:

Fact Tables:
- gold.fact_sales: Daily sales transactions with metrics (revenue, quantity, discount)
  - Partitioned by sale_date
  - Liquid clustering on customer_id, product_id
  - Pre-aggregated for fast query performance
  - Materialized view for last 90 days
  - 20M rows/month

- gold.fact_web_events: Web interaction events for analytics
  - Pre-joined with dimension tables
  - Optimized for BI tool consumption
  - Compressed with Zstd codec
  - 100M rows/month

Dimension Tables:
- gold.dim_customer: Customer master data (SCD Type 2 from silver)
  - 5M rows, includes historical versions
  - Surrogate keys for data warehouse best practices

- gold.dim_product: Product catalog with attributes
- gold.dim_date: Date dimension with fiscal calendar
- gold.dim_geography: Location hierarchy (country → region → city)

Aggregate Tables:
- gold.customer_360: Unified customer view combining CRM, transactions, web behavior
  - 1 row per customer with 150+ attributes
  - Refreshed daily via MERGE operation
  - Used by customer-facing applications

- gold.daily_revenue_summary: Daily revenue aggregates by product, region, channel
  - Pre-calculated for dashboard performance
  - 10-second query response vs 5-minute raw data query

Characteristics:
- Star schema modeling (facts + dimensions)
- Pre-joined for consumption (avoid complex joins in BI tools)
- Liquid clustering replacing static partitioning (30% query performance improvement)
- Bloom filters on high-cardinality columns (product_id)
- Optimized file sizes (128MB target) via OPTIMIZE command
- Statistics collected for query optimization

Compute:
- Job clusters for aggregation (nightly batch, 2-hour window)
- Photon Engine enabled (3x performance boost)
- Spot instances for cost optimization (70% savings)
- Cost: $20K/month

Azure Gold (East US 2):

Mirrored gold layer for geo-distributed access:
- Local consumption for European users (low latency)
- Replicated from AWS gold layer via Deep Clone
- Replication frequency: Daily for dimensional tables, hourly for fact tables
- Enables local queries avoiding cross-cloud egress costs

**Cross-Cloud Replication (Center):**

Show replication flows:

AWS → Azure Replication:
- Delta Lake Deep Clone: Incremental table replication preserving metadata
- Replication schedule: Gold tables every 6 hours, Silver tables every hour
- Bandwidth: 5 Gbps dedicated
- Technology: Databricks Jobs running Deep Clone commands
- Cost: $8K/month (network egress charges)

Replication Benefits:
- Geographic distribution: Low-latency access for global users
- Disaster recovery: Azure serves as failover if AWS unavailable
- Compliance: Keep European data in Azure for GDPR
- Cost optimization: Avoid expensive cross-cloud query egress

**Serving Layer - Consumption Patterns:**

Multiple consumption methods:

BI and Reporting:
- Power BI: DirectQuery to Databricks SQL Warehouse (serverless)
  - 500 users accessing gold.fact_sales via pre-built semantic model
  - Row-level security enforced via Unity Catalog dynamic views
  - Query response: < 3 seconds for standard reports

- Tableau: Live connection to gold layer
  - 200 users building ad-hoc analyses
  - Extracts refreshed nightly for performance

- Databricks SQL Dashboards: Embedded analytics for internal stakeholders
  - Real-time dashboards on silver layer (15-minute freshness)
  - Scheduled email delivery of reports

Data Science and ML:
- Feature Store: Serving features from gold.customer_360 for ML models
  - Online store (low-latency): Azure CosmosDB serving features to production apps
  - Offline store (training): Delta Lake gold tables for batch training

- Jupyter Notebooks: Data scientists querying silver/gold layers for exploration
  - Auto-complete and schema discovery via Unity Catalog integration

Operational Analytics:
- Real-time applications consuming silver layer via Databricks SQL Connector
  - Customer 360 API serving gold.customer_360 to CRM application
  - REST API with 50ms p99 latency

Data Sharing:
- Delta Sharing: Sharing gold.daily_revenue_summary with partner companies
  - Read-only access with token-based authentication
  - External recipients consume via pandas or Spark
  - Automatic propagation of updates via Change Data Feed

Reverse ETL:
- Hightouch/Census: Syncing gold.customer_360 back to Salesforce
  - Enriches CRM with aggregated data lake insights
  - Bi-directional data flow (operational → analytics → operational)

**Bottom - Data Governance and Quality:**

Unity Catalog Lineage:
- Column-level lineage tracked from source to consumption
- Visual graph: Salesforce Account.Name → bronze.raw_salesforce_accounts.name → silver.customers_scd2.customer_name → gold.dim_customer.customer_name → Power BI Report
- Impact analysis: If source column changes, downstream dependencies identified

Access Control:
- Bronze layer: Data engineers only (write), compliance teams (read for audit)
- Silver layer: Data engineers, data scientists, analysts (read)
- Gold layer: All users (read), business analysts can query freely
- Row-level security: Sales reps see only their region's data via Unity Catalog dynamic views

Data Quality Metrics:
- Overall data quality score: 99.5%
- Expectation pass rate: 98.5% (silver layer validations)
- Freshness SLA: 99.2% of tables updated within expected timeframe
- Completeness: 99.8% (null rate <0.2% on required fields)

**Right Panel - Performance Metrics:**

Latency Metrics:
- Source to Bronze: < 5 minutes (streaming), < 1 hour (batch)
- Bronze to Silver: 15-30 minutes
- Silver to Gold: Hourly refresh for fact tables, daily for dimensions
- End-to-end latency (source to gold): 2 hours typical, 4 hours p99

Throughput:
- Ingestion: 1TB/day raw data into bronze
- Processing: 500GB/day cleansed data in silver
- Aggregation: 100GB/day in gold layer
- Query: 10,000 queries/day on gold layer

Cost Breakdown:
- Bronze ingestion: $25K/month
- Silver transformation: $35K/month
- Gold aggregation: $20K/month
- Cross-cloud replication: $8K/month
- Storage (all layers): $30K/month
- Serving (SQL warehouses): $22K/month
- Total: $140K/month

Cost per GB processed: $4.67/GB (including storage and compute)

Use color coding: Bronze/copper (#CD7F32) for Bronze layer, Silver/gray (#C0C0C0) for Silver layer, Gold/yellow (#FFD700) for Gold layer, Databricks red-orange, AWS orange, Azure blue. Include Delta Lake logo, Unity Catalog logo, Databricks logo, BI tool logos (Power BI, Tableau), data quality tool logos (Great Expectations). Clear data flow arrows with transformation labels, latency indicators, and volume metrics.

Add technical annotations: "Auto Loader schema inference handles evolving schemas", "Delta Live Tables expectations enforce data quality", "Liquid clustering optimizes for diverse query patterns", "Deep Clone preserves transaction log and statistics", "Materialized views cache frequent aggregations".

Enterprise data engineering architecture style with detailed pipeline specifications, performance metrics, and suitable for data platform review sessions.
```

**File Name**: `databricks-medallion-e2e-multicloud.png`

**Caption**: End-to-end medallion architecture with Bronze-Silver-Gold data flow, cross-cloud replication, and diverse consumption patterns

---

## Prompt 10: Zero Trust Security Architecture for Multi-Cloud Databricks

**Purpose**: Comprehensive Zero Trust security model for Databricks across clouds with defense-in-depth

**Prompt**:
```
Create a detailed Zero Trust security architecture diagram for multi-cloud Databricks implementing defense-in-depth principles with identity-centric security. Use concentric security rings layout with Zero Trust principles.

**Core Principle (Center):** 
Display "Never Trust, Always Verify" as central tenant with three Zero Trust pillars:
1. Verify explicitly: Always authenticate and authorize based on all available data points
2. Use least privilege access: Limit user access with Just-In-Time and Just-Enough-Access (JIT/JEA)
3. Assume breach: Minimize blast radius and segment access

**Ring 1 - Identity and Access Management (Innermost):**

Centralized Identity Provider:
- Azure Active Directory (primary IdP)
- SAML 2.0 SSO to Databricks Account
- SCIM provisioning syncing users, groups, service principals
- Conditional Access Policies enforcing:
  - MFA required for all users (100% enrollment)
  - Device compliance check (managed devices only)
  - Location-based access (block from untrusted countries)
  - Risk-based authentication (adaptive MFA on unusual sign-in)

Multi-Factor Authentication:
- Primary: Microsoft Authenticator push notifications
- Backup: FIDO2 hardware security keys (YubiKey)
- SMS disabled (vulnerable to SIM swapping)
- MFA bypass: None (no exceptions)

Service Principal Security:
- Client certificate authentication (no password-based)
- Automatic rotation: Every 90 days via Azure Key Vault
- Secrets never in code: Retrieved from Key Vault at runtime
- Least privilege: Service principals granted only required permissions

User Lifecycle:
- Onboarding: Automated provisioning via SCIM (new hire → AD group → Databricks access within hours)
- Offboarding: Automated deprovisioning (termination → AD disabled → Databricks access revoked within minutes)
- Access review: Quarterly attestation by managers (recertify or revoke)

**Ring 2 - Unity Catalog RBAC (Second Ring):**

Fine-Grained Access Control:

Hierarchical Permission Model:
- Metastore level: Account admins only
- Catalog level: Data engineering leads (USAGE, CREATE SCHEMA)
- Schema level: Team leads (USAGE, CREATE TABLE)
- Table level: Analysts (SELECT), engineers (MODIFY)
- Column level: Sensitive columns (PII, PHI) restricted to compliance team
- Row level: Dynamic views filtering data by user attributes (sales rep sees only their region)

Permission Grants (Examples):
```
-- Grant read access to analytics catalog
GRANT USAGE ON CATALOG analytics TO `analytics_team`;

-- Grant write access to silver schema
GRANT MODIFY ON SCHEMA analytics.silver TO `data_engineers`;

-- Row-level security: Users see only their region
CREATE VIEW gold.sales_by_region_filtered AS
SELECT * FROM gold.sales_by_region
WHERE region = current_user_region();
```

Attribute-Based Access Control (ABAC):
- Tags applied to tables: PII, Confidential, Public, Restricted
- Policies grant access based on user attributes + data tags
- Example: Users with clearance_level=high can access Confidential tables

Permission Inheritance:
- Catalog permissions inherit to schemas
- Schema permissions inherit to tables
- Explicit denies override inheritance

Audit Trail:
- All permission grants/revokes logged to Unity Catalog audit log
- Immutable audit trail for compliance
- Queryable via System Tables for reporting

**Ring 3 - Network Security (Third Ring):**

Zero Trust Network Architecture:

AWS Network Security:
- VPC with no public subnets (100% private)
- Databricks cluster nodes: Private IPs only, no internet access
- PrivateLink: All communication to Databricks Control Plane via private endpoint
- VPC endpoints: S3, Secrets Manager, CloudWatch (no internet gateway)
- NAT Gateway: Only for software package downloads (egress allowlist: pypi.org, maven.org)
- Security Groups: Default deny all, explicit allow rules only
  - Inbound: Port 443 from VPC CIDR only
  - Inter-cluster: Ports 8085-8087 for Spark communication
  - Outbound: Specific VPC endpoints only
- Network ACLs: Subnet-level stateless filtering (defense in depth)
- VPC Flow Logs: All traffic logged for analysis

Azure Network Security:
- VNet injection: Databricks in delegated subnets
- No public IPs: All cluster nodes private
- Private Link: Frontend and backend private endpoints to Control Plane
- NSG (Network Security Groups): Restrictive inbound/outbound rules
  - Application Security Groups for logical grouping
- Azure Firewall: Centralized egress filtering
  - Deny all by default, explicit allowlist for package repositories
- User-Defined Routes (UDR): Force all traffic through firewall
- NSG Flow Logs: Traffic analysis and threat detection

Micro-Segmentation:
- Production workspaces in dedicated VPC/VNet (isolated)
- Development workspaces in separate VPC/VNet
- No direct network connectivity between prod and dev
- Cross-workspace communication via private service endpoints only

DDoS Protection:
- AWS Shield Standard (automatic)
- Azure DDoS Protection Standard (enhanced)
- Web Application Firewall (WAF) for workspace UI

**Ring 4 - Data Protection (Fourth Ring):**

Encryption Architecture:

Encryption at Rest:
- S3/ADLS: Customer-Managed Keys (CMK) in AWS KMS / Azure Key Vault
- Key rotation: Automatic annual rotation
- EBS/Managed Disks: Encrypted with CMK
- Delta Lake: Column-level encryption for PII columns using crypto functions
- DBFS root: Encrypted with Databricks-managed keys
- Notebook outputs: Encrypted

Encryption in Transit:
- TLS 1.3 minimum version (TLS 1.2 deprecated)
- Control Plane to Compute Plane: TLS over PrivateLink
- Cluster to S3/ADLS: TLS via VPC/service endpoints
- Inter-cluster communication: Encrypted
- User to Workspace UI: HTTPS with HSTS (HTTP Strict Transport Security)
- Certificate pinning for mobile/API clients

Data Loss Prevention (DLP):
- Sensitive data classification: PII, PHI, PCI automatically detected
- Data masking: Dynamic masking of SSN, credit cards in non-production
- Redaction: Audit logs redact sensitive query parameters
- Exfiltration prevention: 
  - Alerting on large data exports (>1M rows)
  - Unity Catalog audit log tracking all data access
  - Blocked: Unencrypted external shares

Secrets Management:
- AWS Secrets Manager / Azure Key Vault: Centralized secret storage
- Databricks Secret Scopes: Backend by cloud provider secrets managers
- Secure credential passthrough: Access S3/ADLS without exposing credentials
- No secrets in notebooks: Retrieved dynamically via dbutils.secrets
- Automatic rotation: Database passwords rotated every 90 days

**Ring 5 - Threat Detection and Response (Fifth Ring):**

SIEM and Security Analytics:

Centralized Logging:
- All sources: Unity Catalog audit logs, CloudWatch, Azure Monitor, VPC Flow Logs
- SIEM: Splunk Enterprise Security or Azure Sentinel
- Log retention: 2 years hot, 7 years cold (compliance requirement)

Threat Detection Use Cases:

1. Unusual Data Access:
   - UEBA baseline: Normal access patterns per user
   - Alert: User accessing 10x more data than usual (potential insider threat)
   - Alert: Access to sensitive table from unusual location/time

2. Privilege Escalation:
   - Alert: User granted admin permissions (requires approval workflow)
   - Alert: Service principal granted excessive permissions

3. Credential Compromise:
   - Alert: Login from impossible travel (New York → Tokyo in 2 hours)
   - Alert: Multiple failed login attempts (brute force attack)
   - Alert: Token usage from unexpected IP address

4. Data Exfiltration:
   - Alert: Large data export to external system
   - Alert: Unusual outbound network traffic volume
   - Alert: Delta Sharing used to share sensitive catalog

5. Malicious Queries:
   - Alert: SQL injection attempt detected in query text
   - Alert: Query accessing all tables in catalog (reconnaissance)

SOAR (Security Orchestration, Automation, Response):
- Automated response playbooks:
  - Credential compromise → Revoke session, reset MFA, notify user
  - Data exfiltration → Block export, disable user, alert security team
  - Privilege escalation → Revert permission grant, notify admin
- Integration: SIEM → SOAR → Ticketing (ServiceNow) → Notification (PagerDuty)

Threat Intelligence:
- IP reputation feeds: Block known malicious IPs at WAF
- Indicator of Compromise (IOC) matching in logs
- Automated threat hunting queries running daily

**Ring 6 - Compliance and Governance (Outermost):**

Regulatory Compliance:

SOC 2 Type II:
- Control evidence: Unity Catalog audit logs, access reviews, encryption verification
- Automated control testing: Daily scripts validating security controls
- Annual audit: External auditor reviews logs and controls

GDPR:
- Data subject rights: Automated data discovery and deletion workflows
- Cross-border transfers: Documented via Unity Catalog cross-cloud access logs
- Privacy by design: Default deny access, explicit consent required

HIPAA:
- PHI protection: Column-level encryption, row-level security, audit logging
- Business Associate Agreement (BAA): Databricks BAA executed
- Access controls: MFA, audit logs, encryption enforced

PCI-DSS:
- Cardholder data: Masked in non-production, encrypted at rest and in transit
- Network segmentation: Cardholder data environment (CDE) isolated VPC
- Quarterly vulnerability scans: Automated scanning via AWS Inspector / Azure Defender

Compliance Monitoring Dashboard:
- Control adherence: 98% (target 100%)
- Open findings: 3 (all low severity, remediation in progress)
- Audit readiness: Green (all evidence collected and available)

**Bottom Section - Defense in Depth Layers Summary:**

Show layered defense visualization:

Layer 1: Identity - "Who are you?" → MFA, SSO, SCIM
Layer 2: Authorization - "What can you access?" → Unity Catalog RBAC, least privilege
Layer 3: Network - "Where are you connecting from?" → PrivateLink, micro-segmentation
Layer 4: Data - "Is the data protected?" → Encryption, DLP, masking
Layer 5: Monitoring - "Are we under attack?" → SIEM, threat detection, UEBA
Layer 6: Response - "How do we respond?" → SOAR, incident response, forensics

Annotation: "Multiple layers ensure defense even if one layer fails"

**Right Panel - Security Metrics and KPIs:**

Security Posture Score:
- Overall: 92/100 (target >90)
- Identity: 95/100 (MFA 100%, SCIM provisioning automated)
- Network: 88/100 (VPC Flow Logs enabled, NAT gateway restricted)
- Data: 94/100 (Encryption 100%, DLP active)
- Monitoring: 90/100 (SIEM integrated, 95% alert response within SLA)

Mean Time to Detect (MTTD): 8 minutes (target <15 minutes)
Mean Time to Respond (MTTR): 45 minutes (target <1 hour)
False Positive Rate: 12% (target <15%)
Security Incidents (Last Quarter): 2 (both low severity, closed)

**Left Panel - Zero Trust Principles Applied:**

Verify Explicitly:
- Every access request authenticated with MFA
- Device health checked before access granted
- Continuous verification (not just at login)

Least Privilege Access:
- JIT (Just-In-Time): Temporary elevated access via PIM (Privileged Identity Management)
- JEA (Just-Enough-Access): Minimal permissions granted
- Time-bound access: Admin access auto-expires after 4 hours

Assume Breach:
- Micro-segmentation limits lateral movement
- Continuous monitoring detects anomalies
- Automated response playbooks contain breaches
- Regular penetration testing validates defenses

Use color coding: Red (#E74C3C) for security boundaries and threats, Green (#27AE60) for allowed access, Amber (#F39C12) for warnings and alerts, Blue (#3498DB) for identity and authentication, Purple (#8E44AD) for encryption. Include security icons: lock, shield, key, firewall, camera (monitoring). Cloud provider logos, Databricks logo, Azure AD logo, security tool logos (Splunk, Sentinel, CrowdStrike).

Add technical annotations: "Zero Trust eliminates implicit trust", "Identity is the new perimeter", "Encryption everywhere: data never in clear text", "Assume breach: monitoring and rapid response critical", "Least privilege: users get minimum access needed, nothing more".

Enterprise security architecture style with detailed security controls, threat models, and suitable for CISO and security team presentations.
```

**File Name**: `databricks-zero-trust-security.png`

**Caption**: Zero Trust security architecture for multi-cloud Databricks with identity-centric defense-in-depth, encryption, and continuous verification

---

## Summary and Usage Guidelines

### Technical Audience Focus

These updated prompts incorporate 2025-2026 multi-cloud best practices including:

✅ **Active-passive DR with 4-hour RTO** (Prompt 4) - industry-proven pattern  
✅ **Unity Catalog per-region metastores** with Delta Sharing (Prompts 2, 4, 9)  
✅ **Private network connectivity** via PrivateLink/Private Endpoints (Prompts 1, 3, 6)  
✅ **FinOps workload placement strategies** (Prompt 5) - data gravity principle  
✅ **Event-driven cross-cloud integration** with Confluent (Prompt 6)  
✅ **Infrastructure as Code multi-cloud provisioning** with Terraform (Prompt 7)  
✅ **Unified observability and SIEM** (Prompt 8)  
✅ **End-to-end medallion with cross-cloud replication** (Prompt 9)  
✅ **Zero Trust security model** (Prompt 10) - 2025 security standard  

### Recommended Usage:

**For DR Planning:** Use Prompts 1 + 4  
**For Cost Optimization:** Use Prompts 1 + 5  
**For Security Review:** Use Prompts 3 + 10  
**For Data Engineering:** Use Prompts 2 + 9  
**For Platform Engineering:** Use Prompts 7 + 8  
**For Real-Time Integration:** Use Prompt 6  

### Technical Depth:

These prompts are significantly more detailed and technical than v1.0, targeting:
- Cloud architects designing multi-cloud platforms
- Data architects planning lakehouse migrations
- Lead data engineers implementing production pipelines
- Platform engineers managing infrastructure
- Security architects implementing Zero Trust

All prompts include specific technologies, configurations, metrics, and real-world patterns validated by 2025-2026 industry research.

---

**Document Version:** 2.0 Technical Edition  
**Last Updated:** January 2026  
**Research Sources:** 75+ industry articles, Databricks documentation, multi-cloud best practices  
**Target Audience:** Technical practitioners (architects, lead engineers, platform teams)
