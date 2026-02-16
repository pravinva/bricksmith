# YWS SparkML Migration to Unity Catalog

## Customer Context

The customer has a workload called **YWS** (Yellow Warning System) that currently runs on
**Databricks Runtime 9.1** (deprecated). The workload involves:

- **Model Training**: A LogisticRegression model trained using SparkML
- **Model Scoring/Inference**: Batch scoring using the trained model
- **Orchestration**: Triggered externally from **RageMaker** (external orchestration tool)
- **Data Access**: Currently uses ODBC from R to interact with Databricks

A prior migration effort (**AAAI**) already completed a **SparkR to DBSQL** migration,
providing a foundation. The SparkML component follows a different pattern — it requires
triggering a job to train/score, then retrieving predictions via SQL.

## Current Architecture (Challenges)

The existing architecture spans on-prem, two Azure Databricks environments, and RageMaker:

### On-Premises
- **Oracle Exadata / BIW** — source of truth, data is replicated out to Azure

### Azure — Insights EDP (Workspace 1)
- **ADF** (Azure Data Factory) for orchestration
- **Databricks Jobs** for processing
- **ADLS Gen 2 / Delta Lake** for storage
- Users access data here
- **Challenge**: UC Governance is NOT set up

### Azure — AA EDP (Workspace 2)
- **DBSQL Classic** — bespoke orchestration, wasting compute (sitting idle)
- **ADLS Gen 2 / Delta Lake** for storage
- Data is copied BACK to Databricks to be shared with other teams
- **Challenges**: Bespoke orchestration, wasting compute on DBSQL Classic

### RageMaker (External — Azure Infrastructure)
- **Feature Store / AADemand** — feature data
- **Azure NFS** — data copied to expensive NFS storage
- **Azure Batch** — batch compute for ML
- **Azure VMs** — 100s of VMs for model training/scoring (inefficient)
- **ML Train/Score** — SparkML LogisticRegression
- **R-Studio** — R-based analytics and ODBC access
- **Challenge**: Inefficient model training/scoring across 100s of VMs

### Key Pain Points (Numbered)
1. **Excessive data movement** — data replicated from BIW, copied to Azure NFS, copied back to Databricks
2. **Bespoke orchestration** — custom orchestration in AA EDP
3. **No UC governance** — neither workspace has Unity Catalog set up
4. **Wasting compute** — DBSQL Classic cluster running without full utilisation
5. **Inefficient ML** — model training/scoring spread across 100s of Azure VMs via RageMaker

## Interim State Architecture (Target for Phase 1)

The interim state consolidates the sprawling current architecture while allowing RageMaker
to continue orchestrating (but in a reduced role):

### On-Premises (unchanged)
- **Oracle Exadata / BIW** — still the source of truth

### Azure — Insights EDP (Workspace 1, simplified)
- **Workflows** replace ADF (Serverless Job Workflows)
- **Databricks Serverless Jobs** for processing
- **ADLS Gen 2 / Delta Lake** for storage
- Reads BIW data **directly via UC** from AA EDP (no more separate copies)
- Users access data here

### Azure — AA EDP (Workspace 2, consolidated ML hub)
- **Workflows** containing:
  - **Model Training Jobs** — SparkML LogisticRegression runs here
  - **Model Scoring Jobs** — batch inference runs here
- **DBSQL Serverless** (replaces Classic) — automatic cost optimization
- **ADLS Gen 2 / Delta Lake** — centralised storage, less data movement
- Batch inference and training now run as **Workflow Jobs** inside Databricks

### RageMaker* (reduced role, dashed border — being phased)
- **Feature Store / AADemand** — still holds feature definitions
- **R-Studio** — R analytics continue
- **ML Train/Score** — eventually moves fully into Databricks
- RageMaker **continues to orchestrate** but now by **triggering Databricks Workflows**
  via the Jobs API, rather than running ML on 100s of Azure VMs

### UC Model Registry (new, centralised)
- **Python Models** — registered and governed
- **R Models** — registered and governed
- Models are **centrally governed and tracked**

### Key Improvements (Numbered)
1. **Less data moves around** — centralised Delta Lake, no Azure NFS copying
2. **RageMaker triggers workflows** — orchestration continues but compute is Databricks-native
3. **UC governance** — cross-workspace data access via Unity Catalog; model registry for lineage
4. **Serverless everything** — ADF → Serverless Workflows; DBSQL Classic → DBSQL Serverless (auto cost optimisation)
5. **ML inside Databricks** — training and scoring as Workflow Jobs, not on Azure Batch/VMs

## Recommended Architecture — Option #2: Serverless Job Clusters

This is the recommended starting point before moving to the full Mosaic AI stack (Option #1).

### Workflow

1. **RageMaker** triggers a Databricks Job via the Jobs API
2. **Job Cluster 1 (Train)**: Trains the LogisticRegression model using SparkML,
   logs the model to **Unity Catalog** via **MLflow**
3. **Job Cluster 2 (Score)**: Loads the registered model from UC, performs batch
   inference on input data, writes predictions back to UC tables
4. **RageMaker** retrieves results via SQL/ODBC from the predictions table

### Key Components

- **Databricks Jobs** (Serverless): Ephemeral compute — spins up, does the work, shuts down
- **MLflow Model Registry** (Unity Catalog): Model versioning, lineage, governance
- **Unity Catalog Tables**: Input features, predictions output, model artifacts
- **Jobs API**: REST endpoint for RageMaker to trigger training and scoring jobs
- **SparkML**: Existing LogisticRegression code can be reused on updated runtime

### Advantages

- Removes DBSQL out of the equation for ML workloads
- Easily maintainable and simple
- Cost-efficient (compute comes up, does the work, then turns off)
- UC Feature Store tables provide automatic lineage
- MLflow Model Tracking included
- Does the work where the data is (no data movement)
- Existing SparkML code can be reused with minimal changes

### Disadvantages

- Need to right-size a jobs cluster (not painful)
- Won't reuse the DBSQL Warehouse running for other workloads
- Need to deploy training and scoring scripts to Databricks

## Other Options Considered

### Option #1: Full Mosaic AI Stack (future target)

- Train via Brickster, log model to UC, deploy to Model Serving Endpoint
- Score via `AI_QUERY()` DBSQL function — can integrate with existing ODBC/R workflow
- Best practice but larger scope of change

### Option #3: Python UDFs in DBSQL (least preferable)

- Use scikit-learn inside a UC SQL Function
- Minimal change but unsupported pattern, no model tracking, version pinning issues

## Migration Strategy

1. **Phase 1 (Now)**: Option #2 — Serverless Jobs for train + score, get off DBR 9.1
2. **Phase 2 (Later)**: Option #1 — Model Serving + AI_QUERY for real-time/SQL-native scoring

## Diagram Requirements

- Show **RageMaker** as an external orchestrator on the left
- Show **Databricks** as the main platform zone containing:
  - **Jobs API** as the entry point from RageMaker
  - **Serverless Job Cluster** (Training) running SparkML LogisticRegression
  - **Serverless Job Cluster** (Scoring) running batch inference
  - **MLflow** tracking and model registry
  - **Unity Catalog** as the governance layer containing:
    - Feature tables (input)
    - Model artifacts (registered models)
    - Predictions table (output)
  - **DBSQL Warehouse** for downstream SQL access
- Show **R/ODBC Client** retrieving predictions from the DBSQL Warehouse
- Show data flow arrows: RageMaker → Jobs API → Train → MLflow/UC → Score → UC Tables → DBSQL → R
- Use the **Databricks logo** prominently
- Use the **Unity Catalog logo** near the governance layer
- Use the **MLflow logo** near model tracking
- The diagram should convey: **simple migration path — reuse existing SparkML code,
  gain UC governance, MLflow tracking, and serverless efficiency**
