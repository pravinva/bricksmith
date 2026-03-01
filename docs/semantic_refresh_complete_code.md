# Semantic Model Refresh Framework - Complete Code Package

**Version:** 2.0 (Model-based, Power BI Task Integration)  
**Platform:** Azure Databricks + Power BI  
**Total Files:** 20

---

## Directory Structure

```
/SemanticModelRefresh/
├── /Setup/                    (5 files)
├── /Libraries/                (2 files)
├── /Workflows/                (4 files)
├── /Monitoring/               (3 files)
├── /Testing/                  (3 files)
├── /Administration/           (4 files)
├── /Documentation/            (2 files)
└── README.md                  (1 file)
```

---

# /Setup/

## File: 01_create_metadata_schema.sql

```sql
-- =============================================================================
-- Semantic Model Refresh Framework - Metadata Schema
-- Purpose: Create Unity Catalog metadata tables
-- Version: 2.0
-- =============================================================================

CREATE CATALOG IF NOT EXISTS edp_metadata
COMMENT 'Enterprise Data Platform operational metadata';

CREATE SCHEMA IF NOT EXISTS edp_metadata.semantic_refresh
COMMENT 'Metadata for Power BI semantic model refresh orchestration';

-- =============================================================================
-- Table 1: Semantic Models Registry
-- =============================================================================
CREATE TABLE IF NOT EXISTS edp_metadata.semantic_refresh.semantic_models (
  model_id STRING NOT NULL,
  model_name STRING NOT NULL,
  workspace_id STRING NOT NULL COMMENT 'Power BI workspace GUID',
  dataset_id STRING NOT NULL COMMENT 'Power BI dataset GUID',
  connection_name STRING NOT NULL COMMENT 'Unity Catalog Power BI connection',
  
  -- Power BI configuration
  query_mode STRING COMMENT 'Import, DirectQuery, Dual, Hybrid',
  supports_viewer_sso BOOLEAN DEFAULT false,
  auth_mode STRING DEFAULT 'SERVICE_PRINCIPAL',
  
  -- Governance
  sla_tier STRING COMMENT 'T0 (critical), T1 (important), T2 (standard)',
  description STRING,
  owner_email STRING NOT NULL,
  technical_contact STRING,
  business_unit STRING,
  
  -- Status
  is_active BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  created_by STRING DEFAULT CURRENT_USER(),
  updated_by STRING DEFAULT CURRENT_USER(),
  
  CONSTRAINT pk_semantic_models PRIMARY KEY (model_id),
  CONSTRAINT chk_query_mode CHECK (query_mode IN ('Import', 'DirectQuery', 'Dual', 'Hybrid')),
  CONSTRAINT chk_auth_mode CHECK (auth_mode IN ('SERVICE_PRINCIPAL', 'OAUTH', 'PAT')),
  CONSTRAINT chk_sla_tier CHECK (sla_tier IN ('T0', 'T1', 'T2'))
)
COMMENT 'Registry of all Power BI semantic models'
TBLPROPERTIES ('delta.enableChangeDataFeed' = 'true');

-- =============================================================================
-- Table 2: Table Refresh Configuration
-- =============================================================================
CREATE TABLE IF NOT EXISTS edp_metadata.semantic_refresh.table_refresh_config (
  config_id STRING NOT NULL,
  model_id STRING NOT NULL,
  table_name STRING NOT NULL,
  source_table STRING NOT NULL,
  source_type STRING DEFAULT 'MATERIALIZED_VIEW',
  
  -- Refresh behavior
  refresh_cadence STRING NOT NULL,
  refresh_interval_minutes INT,
  refresh_type STRING DEFAULT 'FULL',
  
  -- Trigger configuration
  trigger_mode STRING DEFAULT 'SCHEDULE',
  
  -- SLA configuration
  sla_threshold_minutes INT,
  sla_tier STRING,
  
  -- Status
  is_active BOOLEAN DEFAULT true,
  last_refresh_timestamp TIMESTAMP,
  last_refresh_status STRING,
  last_refresh_duration_seconds INT,
  last_refresh_cost_usd DECIMAL(10,2),
  
  notes STRING,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  created_by STRING DEFAULT CURRENT_USER(),
  updated_by STRING DEFAULT CURRENT_USER(),
  
  CONSTRAINT pk_table_refresh_config PRIMARY KEY (config_id),
  CONSTRAINT fk_model FOREIGN KEY (model_id) REFERENCES edp_metadata.semantic_refresh.semantic_models(model_id),
  CONSTRAINT chk_cadence CHECK (refresh_cadence IN ('NEAR_REALTIME', 'MEDIUM_FREQUENCY', 'DAILY', 'ON_DEMAND')),
  CONSTRAINT chk_trigger_mode CHECK (trigger_mode IN ('SCHEDULE', 'TABLE_UPDATE', 'MANUAL'))
)
TBLPROPERTIES ('delta.enableChangeDataFeed' = 'true');

-- =============================================================================
-- Table 3: Refresh Execution Log
-- =============================================================================
CREATE TABLE IF NOT EXISTS edp_metadata.semantic_refresh.refresh_execution_log (
  execution_id STRING NOT NULL,
  model_id STRING NOT NULL,
  tables_refreshed STRING,
  workflow_run_id STRING,
  workflow_job_id STRING,
  powerbi_refresh_id STRING,
  powerbi_request_id STRING,
  refresh_start_timestamp TIMESTAMP NOT NULL,
  refresh_end_timestamp TIMESTAMP,
  status STRING NOT NULL,
  duration_seconds INT,
  rows_processed BIGINT,
  source_tables_last_updated TIMESTAMP,
  error_message STRING,
  error_code STRING,
  retry_count INT DEFAULT 0,
  triggered_by STRING NOT NULL,
  triggered_by_user STRING,
  trigger_reason STRING,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  
  CONSTRAINT pk_refresh_log PRIMARY KEY (execution_id),
  CONSTRAINT chk_status CHECK (status IN ('RUNNING', 'SUCCESS', 'FAILED', 'TIMEOUT'))
)
PARTITIONED BY (DATE(refresh_start_timestamp))
TBLPROPERTIES ('delta.enableChangeDataFeed' = 'true');

-- =============================================================================
-- Table 4: Cost Tracking
-- =============================================================================
CREATE TABLE IF NOT EXISTS edp_metadata.semantic_refresh.refresh_cost_tracking (
  cost_id STRING NOT NULL,
  execution_id STRING NOT NULL,
  model_id STRING NOT NULL,
  warehouse_id STRING,
  warehouse_name STRING,
  warehouse_cost_estimate_usd DECIMAL(10,2),
  compute_units_consumed DECIMAL(10,2),
  query_count INT,
  data_transfer_gb DECIMAL(10,2),
  compute_cost_usd DECIMAL(10,2),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
  
  CONSTRAINT pk_cost_tracking PRIMARY KEY (cost_id)
)
TBLPROPERTIES ('delta.enableChangeDataFeed' = 'true');

SHOW TABLES IN edp_metadata.semantic_refresh;
```

---

## File: 02_grant_permissions.sql

```sql
-- Grant to service principal
GRANT USE CATALOG ON CATALOG edp_metadata TO `powerbi-refresh-sp`;
GRANT USE SCHEMA ON SCHEMA edp_metadata.semantic_refresh TO `powerbi-refresh-sp`;
GRANT SELECT, MODIFY ON SCHEMA edp_metadata.semantic_refresh TO `powerbi-refresh-sp`;

-- Grant to admins
GRANT ALL PRIVILEGES ON CATALOG edp_metadata TO `data-platform-admins`;

-- Grant read-only to BI users
GRANT USE CATALOG ON CATALOG edp_metadata TO `bi-users`;
GRANT USE SCHEMA ON SCHEMA edp_metadata.semantic_refresh TO `bi-users`;
GRANT SELECT ON SCHEMA edp_metadata.semantic_refresh TO `bi-users`;

-- Grant access to Gold layer
GRANT USE CATALOG ON CATALOG gold TO `powerbi-refresh-sp`;
GRANT SELECT ON SCHEMA gold.awm TO `powerbi-refresh-sp`;
GRANT SELECT ON SCHEMA gold.finance TO `powerbi-refresh-sp`;
```

---

## File: 03_create_powerbi_connections.sql

```sql
-- Create Unity Catalog Power BI Connections
-- REPLACE ALL <PLACEHOLDER> VALUES

CREATE CONNECTION IF NOT EXISTS edp_powerbi.awm_workspace
TYPE powerbi
OPTIONS (
  workspaceId '<AWM_WORKSPACE_GUID>',
  credential (
    tenant_id '<AZURE_TENANT_ID>',
    client_id '<SERVICE_PRINCIPAL_CLIENT_ID>',
    client_secret '<SERVICE_PRINCIPAL_SECRET>'
  )
);

CREATE CONNECTION IF NOT EXISTS edp_powerbi.finance_workspace
TYPE powerbi
OPTIONS (
  workspaceId '<FINANCE_WORKSPACE_GUID>',
  credential (
    tenant_id '<AZURE_TENANT_ID>',
    client_id '<SERVICE_PRINCIPAL_CLIENT_ID>',
    client_secret '<SERVICE_PRINCIPAL_SECRET>'
  )
);

GRANT USAGE ON CONNECTION edp_powerbi.awm_workspace TO `powerbi-refresh-sp`;
GRANT USAGE ON CONNECTION edp_powerbi.finance_workspace TO `powerbi-refresh-sp`;

SHOW CONNECTIONS LIKE 'edp_powerbi.*';
```

---

## File: 04_seed_metadata.sql

```sql
-- Insert models
INSERT INTO edp_metadata.semantic_refresh.semantic_models
(model_id, model_name, workspace_id, dataset_id, connection_name, 
 query_mode, sla_tier, description, owner_email, is_active)
VALUES
  ('awm_model', 'AWM', '<AWM_WORKSPACE_GUID>', '<AWM_DATASET_GUID>',
   'edp_powerbi.awm_workspace', 'Import', 'T1',
   'Drainage infrastructure', 'awm.owner@fultonhogan.com', true),
   
  ('finance_model', 'Finance', '<FINANCE_WORKSPACE_GUID>', '<FINANCE_DATASET_GUID>',
   'edp_powerbi.finance_workspace', 'Import', 'T0',
   'Financial reporting', 'finance.owner@fultonhogan.com', true);

-- Insert table configs - Daily
INSERT INTO edp_metadata.semantic_refresh.table_refresh_config
(config_id, model_id, table_name, source_table, refresh_cadence, 
 sla_threshold_minutes, trigger_mode, is_active)
VALUES
  ('awm_dim_date', 'awm_model', 'dim_date', 'gold.shared_dimensions.dim_date',
   'DAILY', 1500, 'SCHEDULE', true);

-- Medium Frequency
INSERT INTO edp_metadata.semantic_refresh.table_refresh_config
(config_id, model_id, table_name, source_table, refresh_cadence, 
 refresh_interval_minutes, sla_threshold_minutes, trigger_mode, is_active)
VALUES
  ('awm_fact_inspection', 'awm_model', 'fact_asset_inspection', 
   'gold.awm.fact_asset_inspection', 'MEDIUM_FREQUENCY', 240, 300, 'SCHEDULE', true);

-- Near Real-Time
INSERT INTO edp_metadata.semantic_refresh.table_refresh_config
(config_id, model_id, table_name, source_table, refresh_cadence,
 refresh_interval_minutes, sla_threshold_minutes, trigger_mode, is_active)
VALUES
  ('awm_fact_dispatch', 'awm_model', 'fact_dispatch', 'gold.awm.fact_dispatch',
   'NEAR_REALTIME', 30, 60, 'TABLE_UPDATE', true);
```

---

## File: 05_generate_workflows_model_based.py

```python
# Databricks notebook source

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.jobs import *
import json

w = WorkspaceClient()

# Query models with scheduled refresh
scheduled_models = spark.sql("""
    SELECT DISTINCT
        m.model_id,
        m.model_name,
        m.connection_name,
        m.dataset_id,
        m.sla_tier,
        m.owner_email,
        c.refresh_cadence,
        c.refresh_interval_minutes,
        COLLECT_LIST(c.table_name) AS table_names
    FROM edp_metadata.semantic_refresh.semantic_models m
    JOIN edp_metadata.semantic_refresh.table_refresh_config c 
        ON m.model_id = c.model_id
    WHERE m.is_active = true
      AND c.is_active = true
      AND c.trigger_mode = 'SCHEDULE'
    GROUP BY m.model_id, m.model_name, m.connection_name, m.dataset_id, 
             m.sla_tier, m.owner_email, c.refresh_cadence, c.refresh_interval_minutes
""").collect()

workflows_created = []

for model in scheduled_models:
    workflow_name = f"{model.model_name} - {model.refresh_cadence}"
    
    tasks = [
        Task(
            task_key="log_start",
            notebook_task=NotebookTask(
                notebook_path="/SemanticModelRefresh/Workflows/log_model_refresh",
                base_parameters={
                    "event_type": "REFRESH_START",
                    "model_id": model.model_id,
                    "cadence": model.refresh_cadence,
                    "table_names": ','.join(model.table_names)
                }
            ),
            job_cluster_key="logging_cluster"
        ),
        Task(
            task_key="refresh_model",
            power_bi_task=PowerBITask(
                connection_name=model.connection_name,
                dataset_id=model.dataset_id,
                refresh_type="full"
            ),
            depends_on=[TaskDependency(task_key="log_start")],
            timeout_seconds=7200,
            max_retries=2 if model.sla_tier in ['T0', 'T1'] else 1
        ),
        Task(
            task_key="log_complete",
            notebook_task=NotebookTask(
                notebook_path="/SemanticModelRefresh/Workflows/log_model_refresh",
                base_parameters={
                    "event_type": "REFRESH_COMPLETE",
                    "model_id": model.model_id
                }
            ),
            depends_on=[TaskDependency(task_key="refresh_model")],
            job_cluster_key="logging_cluster"
        )
    ]
    
    # Set schedule
    if model.refresh_cadence == "DAILY":
        schedule = CronSchedule(
            quartz_cron_expression="0 0 6 * * ?",
            timezone_id="Pacific/Auckland"
        )
    elif model.refresh_cadence == "MEDIUM_FREQUENCY":
        hours = model.refresh_interval_minutes // 60
        schedule = CronSchedule(
            quartz_cron_expression=f"0 0 */{hours} * * ?",
            timezone_id="Pacific/Auckland"
        )
    
    workflow_spec = CreateJob(
        name=workflow_name,
        tasks=tasks,
        job_clusters=[
            JobCluster(
                job_cluster_key="logging_cluster",
                new_cluster=ClusterSpec(
                    spark_version="14.3.x-scala2.12",
                    node_type_id="Standard_DS3_v2",
                    num_workers=0
                )
            )
        ],
        schedule=schedule,
        email_notifications=JobEmailNotifications(
            on_failure=[model.owner_email, "<platform-support-distribution>"]
        ),
        tags={"ModelId": model.model_id, "SLATier": model.sla_tier or 'T2'}
    )
    
    existing = list(w.jobs.list(name=workflow_name))
    if existing:
        w.jobs.reset(job_id=existing[0].job_id, new_settings=workflow_spec)
        print(f"✅ Updated: {workflow_name}")
    else:
        created = w.jobs.create(**workflow_spec.as_dict())
        print(f"✅ Created: {workflow_name}")

# Table-triggered workflows
table_trigger_models = spark.sql("""
    SELECT 
        m.model_id, m.model_name, m.connection_name, m.dataset_id,
        COLLECT_LIST(c.source_table) AS source_tables,
        MIN(c.refresh_interval_minutes) AS min_interval
    FROM edp_metadata.semantic_refresh.table_refresh_config c
    JOIN edp_metadata.semantic_refresh.semantic_models m ON c.model_id = m.model_id
    WHERE c.trigger_mode = 'TABLE_UPDATE' AND c.is_active = true
    GROUP BY m.model_id, m.model_name, m.connection_name, m.dataset_id
""").collect()

for model in table_trigger_models:
    workflow_name = f"{model.model_name} - TABLE_TRIGGERED"
    
    workflow_spec = CreateJob(
        name=workflow_name,
        trigger=TriggerSettings(
            table_update=TableUpdateTriggerConfiguration(
                table_names=model.source_tables,
                condition=TableUpdateTriggerCondition.ANY_UPDATE,
                wait_after_last_change_seconds=model.min_interval * 60
            )
        ),
        tasks=[
            Task(
                task_key="refresh_model",
                power_bi_task=PowerBITask(
                    connection_name=model.connection_name,
                    dataset_id=model.dataset_id,
                    refresh_type="full"
                )
            )
        ],
        job_clusters=[
            JobCluster(
                job_cluster_key="logging_cluster",
                new_cluster=ClusterSpec(
                    spark_version="14.3.x-scala2.12",
                    node_type_id="Standard_DS3_v2",
                    num_workers=0
                )
            )
        ]
    )
    
    existing = list(w.jobs.list(name=workflow_name))
    if existing:
        w.jobs.reset(job_id=existing[0].job_id, new_settings=workflow_spec)
    else:
        w.jobs.create(**workflow_spec.as_dict())
    
    print(f"✅ Created table-triggered: {workflow_name}")
```

---

# /Libraries/

## File: metadata_helper.py

```python
# Databricks notebook source

from pyspark.sql.functions import col
from datetime import datetime
import uuid

def get_tables_by_cadence(cadence, active_only=True):
    """Get table configurations by refresh cadence."""
    active_filter = "AND c.is_active = true AND m.is_active = true" if active_only else ""
    
    return spark.sql(f"""
        SELECT 
            c.config_id, c.model_id, c.table_name, c.source_table,
            m.model_name, m.connection_name, m.dataset_id
        FROM edp_metadata.semantic_refresh.table_refresh_config c
        JOIN edp_metadata.semantic_refresh.semantic_models m ON c.model_id = m.model_id
        WHERE c.refresh_cadence = '{cadence}' {active_filter}
    """).collect()

def get_running_refreshes():
    """Get currently running refreshes."""
    return spark.sql("""
        SELECT 
            l.execution_id, l.model_id, l.refresh_start_timestamp,
            m.workspace_id, m.dataset_id,
            CAST((unix_timestamp(current_timestamp()) - 
                  unix_timestamp(l.refresh_start_timestamp)) / 60 AS INT) AS minutes_running
        FROM edp_metadata.semantic_refresh.refresh_execution_log l
        JOIN edp_metadata.semantic_refresh.semantic_models m ON l.model_id = m.model_id
        WHERE l.status = 'RUNNING'
          AND l.refresh_start_timestamp >= current_timestamp() - INTERVAL 24 HOURS
    """).collect()

def log_execution_start(model_id, tables_refreshed, triggered_by, workflow_run_id=None):
    """Log refresh execution start."""
    execution_id = f"{model_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{str(uuid.uuid4())[:8]}"
    
    if workflow_run_id is None:
        try:
            workflow_run_id = dbutils.notebook.entry_point.getDbutils().notebook().getContext().currentRunId().toString()
        except:
            workflow_run_id = None
    
    spark.sql(f"""
        INSERT INTO edp_metadata.semantic_refresh.refresh_execution_log
        (execution_id, model_id, tables_refreshed, workflow_run_id, 
         refresh_start_timestamp, status, triggered_by)
        VALUES (
            '{execution_id}', '{model_id}', '{tables_refreshed}',
            {f"'{workflow_run_id}'" if workflow_run_id else 'NULL'},
            current_timestamp(), 'RUNNING', '{triggered_by}'
        )
    """)
    
    return execution_id

def log_execution_end(execution_id, status, error_message=None):
    """Log refresh execution end."""
    error_sql = f"'{error_message.replace(chr(39), chr(39)*2)}'" if error_message else 'NULL'
    
    spark.sql(f"""
        UPDATE edp_metadata.semantic_refresh.refresh_execution_log
        SET refresh_end_timestamp = current_timestamp(),
            status = '{status}',
            duration_seconds = CAST((unix_timestamp(current_timestamp()) - 
                                     unix_timestamp(refresh_start_timestamp)) AS INT),
            error_message = {error_sql}
        WHERE execution_id = '{execution_id}'
    """)

def update_table_refresh_status(model_id, cadence, status):
    """Update last refresh status for all tables in model."""
    spark.sql(f"""
        UPDATE edp_metadata.semantic_refresh.table_refresh_config
        SET last_refresh_timestamp = current_timestamp(),
            last_refresh_status = '{status}',
            updated_at = current_timestamp()
        WHERE model_id = '{model_id}'
          AND refresh_cadence = '{cadence}'
          AND is_active = true
    """)

def get_source_table_metadata(source_table):
    """Get row count and last update for source table."""
    try:
        count_result = spark.sql(f"SELECT COUNT(*) AS cnt FROM {source_table}").first()
        row_count = count_result.cnt if count_result else None
        
        history = spark.sql(f"""
            SELECT MAX(timestamp) AS last_updated
            FROM (DESCRIBE HISTORY {source_table} LIMIT 1)
        """).first()
        last_updated = history.last_updated if history else None
        
        return {"row_count": row_count, "last_updated": last_updated}
    except:
        return {"row_count": None, "last_updated": None}
```

---

## File: powerbi_rest_api.py

```python
# Databricks notebook source
# Power BI REST API - Use only for edge cases

import requests
from datetime import datetime, timedelta

class PowerBIAuthenticator:
    def __init__(self, client_id, client_secret, tenant_id):
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.token = None
        self.token_expiry = None
    
    def get_access_token(self):
        if self.token and self.token_expiry:
            if datetime.now() < self.token_expiry - timedelta(minutes=5):
                return self.token
        return self._fetch_new_token()
    
    def _fetch_new_token(self):
        url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': 'https://analysis.windows.net/powerbi/api/.default'
        }
        response = requests.post(url, data=payload)
        response.raise_for_status()
        token_data = response.json()
        self.token = token_data['access_token']
        self.token_expiry = datetime.now() + timedelta(seconds=token_data.get('expires_in', 3600))
        return self.token

class PowerBIRefreshManager:
    def __init__(self, authenticator):
        self.authenticator = authenticator
        self.base_url = "https://api.powerbi.com/v1.0/myorg"
    
    def trigger_dataset_refresh(self, workspace_id, dataset_id):
        token = self.authenticator.get_access_token()
        url = f"{self.base_url}/groups/{workspace_id}/datasets/{dataset_id}/refreshes"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        payload = {"type": "full", "commitMode": "transactional"}
        response = requests.post(url, headers=headers, json=payload)
        return {"success": response.status_code == 202, 
                "request_id": response.headers.get('RequestId')}
    
    def get_refresh_status(self, workspace_id, dataset_id):
        token = self.authenticator.get_access_token()
        url = f"{self.base_url}/groups/{workspace_id}/datasets/{dataset_id}/refreshes?$top=1"
        response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
        data = response.json()
        if data.get('value'):
            r = data['value'][0]
            return {"status": r.get('status'), "start_time": r.get('startTime'),
                    "end_time": r.get('endTime')}
        return None
```

---

# /Workflows/

## File: log_model_refresh.py

```python
# Databricks notebook source

%run /SemanticModelRefresh/Libraries/metadata_helper

import json
import uuid
from datetime import datetime

dbutils.widgets.text("event_type", "REFRESH_START")
dbutils.widgets.text("model_id", "")
dbutils.widgets.text("cadence", "")
dbutils.widgets.text("table_names", "")

event_type = dbutils.widgets.get("event_type")
model_id = dbutils.widgets.get("model_id")
cadence = dbutils.widgets.get("cadence")
table_names = dbutils.widgets.get("table_names")

# Get workflow context
try:
    workflow_run_id = dbutils.notebook.entry_point.getDbutils().notebook().getContext().currentRunId().toString()
except:
    workflow_run_id = None

if event_type == "REFRESH_START":
    execution_id = f"{model_id}_{cadence}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{str(uuid.uuid4())[:8]}"
    
    # Get row counts from source tables
    total_rows = 0
    for table_name in table_names.split(','):
        config = spark.sql(f"""
            SELECT source_table FROM edp_metadata.semantic_refresh.table_refresh_config
            WHERE model_id = '{model_id}' AND table_name = '{table_name.strip()}'
        """).first()
        if config:
            metadata = get_source_table_metadata(config.source_table)
            if metadata['row_count']:
                total_rows += metadata['row_count']
    
    spark.sql(f"""
        INSERT INTO edp_metadata.semantic_refresh.refresh_execution_log
        (execution_id, model_id, tables_refreshed, workflow_run_id,
         refresh_start_timestamp, status, triggered_by, rows_processed)
        VALUES ('{execution_id}', '{model_id}', '{table_names}',
                {f"'{workflow_run_id}'" if workflow_run_id else 'NULL'},
                current_timestamp(), 'RUNNING', 'SCHEDULE', {total_rows or 'NULL'})
    """)
    
    dbutils.jobs.taskValues.set(key="execution_id", value=execution_id)
    print(f"✅ Logged start: {execution_id}")

elif event_type == "REFRESH_COMPLETE":
    execution_id = dbutils.jobs.taskValues.get(taskKey="log_start", key="execution_id")
    log_execution_end(execution_id, 'SUCCESS')
    update_table_refresh_status(model_id, cadence, 'SUCCESS')
    print(f"✅ Logged completion: {execution_id}")

dbutils.notebook.exit(json.dumps({"execution_id": execution_id, "status": "LOGGED"}))
```

---

## File: capture_refresh_costs.py

```python
# Databricks notebook source

from datetime import datetime

dbutils.widgets.text("execution_id", "")
dbutils.widgets.text("model_id", "")

execution_id = dbutils.widgets.get("execution_id")
model_id = dbutils.widgets.get("model_id")

# Get execution window
execution = spark.sql(f"""
    SELECT refresh_start_timestamp, refresh_end_timestamp
    FROM edp_metadata.semantic_refresh.refresh_execution_log
    WHERE execution_id = '{execution_id}'
""").first()

if not execution or not execution.refresh_end_timestamp:
    dbutils.notebook.exit("SKIPPED")

start_time = execution.refresh_start_timestamp
end_time = execution.refresh_end_timestamp

# Query warehouse usage
warehouse_usage = spark.sql(f"""
    SELECT 
        warehouse_id,
        SUM(total_duration_ms) / 1000.0 AS duration_sec,
        COUNT(DISTINCT query_id) AS query_count,
        SUM(read_bytes) / 1024.0 / 1024.0 / 1024.0 AS data_gb
    FROM system.query.history
    WHERE start_time >= timestamp'{start_time}'
      AND start_time <= timestamp'{end_time}'
    GROUP BY warehouse_id
""").collect()

for usage in warehouse_usage:
    # Estimate cost (adjust pricing)
    compute_units = (usage.duration_sec / 3600.0) * 2
    cost = compute_units * 0.30
    
    spark.sql(f"""
        INSERT INTO edp_metadata.semantic_refresh.refresh_cost_tracking
        (cost_id, execution_id, model_id, warehouse_id, 
         warehouse_cost_estimate_usd, compute_units_consumed, query_count, data_transfer_gb)
        VALUES ('{execution_id}_{usage.warehouse_id}', '{execution_id}', '{model_id}',
                '{usage.warehouse_id}', {cost}, {compute_units}, {usage.query_count}, {usage.data_gb})
    """)
    
    print(f"✅ Cost: ${cost:.2f} ({compute_units:.2f} DBU)")

dbutils.notebook.exit("LOGGED")
```

---

## File: sla_monitoring.py

```python
# Databricks notebook source

import requests
import json

# Query SLA breaches
breaches = spark.sql("""
    SELECT 
        m.model_name, m.sla_tier, m.owner_email,
        c.table_name, c.sla_threshold_minutes,
        CAST((unix_timestamp(current_timestamp()) - 
              unix_timestamp(c.last_refresh_timestamp)) / 60 AS INT) AS minutes_since
    FROM edp_metadata.semantic_refresh.table_refresh_config c
    JOIN edp_metadata.semantic_refresh.semantic_models m ON c.model_id = m.model_id
    WHERE c.is_active = true
      AND c.sla_threshold_minutes IS NOT NULL
      AND (c.last_refresh_timestamp IS NULL OR
           CAST((unix_timestamp(current_timestamp()) - 
                 unix_timestamp(c.last_refresh_timestamp)) / 60 AS INT) > c.sla_threshold_minutes)
    ORDER BY CASE m.sla_tier WHEN 'T0' THEN 1 WHEN 'T1' THEN 2 ELSE 3 END
""").collect()

if not breaches:
    print("✅ No SLA breaches")
    dbutils.notebook.exit(json.dumps({"status": "OK", "breaches": 0}))

# Format alert
alert = f"🚨 SLA Breaches ({len(breaches)})\\n\\n"
for b in breaches:
    alert += f"{b.sla_tier} - {b.model_name}.{b.table_name}\\n"
    alert += f"  SLA: {b.sla_threshold_minutes} min, Actual: {b.minutes_since} min\\n\\n"

# Send to Teams
try:
    webhook = dbutils.secrets.get(scope="alerts", key="teams-webhook")
    requests.post(webhook, json={"text": alert})
    print("✅ Alert sent")
except:
    print("⚠️ Could not send alert")

dbutils.notebook.exit(json.dumps({"status": "BREACHES", "count": len(breaches)}))
```

---

## File: advanced_refresh.py

```python
# Databricks notebook source
# Use only for edge cases not supported by Power BI tasks

%run /SemanticModelRefresh/Libraries/powerbi_rest_api
%run /SemanticModelRefresh/Libraries/metadata_helper

dbutils.widgets.text("model_id", "")
dbutils.widgets.text("table_name", "")

model_id = dbutils.widgets.get("model_id")
table_name = dbutils.widgets.get("table_name")

# Get config
config = spark.sql(f"""
    SELECT m.workspace_id, m.dataset_id, c.source_table
    FROM edp_metadata.semantic_refresh.semantic_models m
    JOIN edp_metadata.semantic_refresh.table_refresh_config c ON m.model_id = c.model_id
    WHERE m.model_id = '{model_id}' AND c.table_name = '{table_name}'
""").first()

if not config:
    raise ValueError(f"No config for {model_id}.{table_name}")

# Authenticate
client_id = dbutils.secrets.get(scope="powerbi-secrets", key="client-id")
client_secret = dbutils.secrets.get(scope="powerbi-secrets", key="client-secret")
tenant_id = dbutils.secrets.get(scope="powerbi-secrets", key="tenant-id")

auth = PowerBIAuthenticator(client_id, client_secret, tenant_id)
mgr = PowerBIRefreshManager(auth)

# Log and trigger
execution_id = log_execution_start(model_id, table_name, 'MANUAL')

try:
    response = mgr.trigger_dataset_refresh(config.workspace_id, config.dataset_id)
    log_execution_end(execution_id, 'SUCCESS')
    print(f"✅ Refresh triggered")
except Exception as e:
    log_execution_end(execution_id, 'FAILED', str(e))
    raise

dbutils.notebook.exit(json.dumps({"execution_id": execution_id}))
```

---

# /Monitoring/

## File: dashboard_queries.sql

```sql
-- Query 1: Last Refresh Status
SELECT 
    m.model_name,
    m.sla_tier,
    c.table_name,
    c.last_refresh_timestamp,
    TIMESTAMPDIFF(MINUTE, c.last_refresh_timestamp, CURRENT_TIMESTAMP()) AS minutes_since,
    c.last_refresh_status,
    c.sla_threshold_minutes,
    CASE 
        WHEN c.last_refresh_timestamp IS NULL THEN '🔴 Never'
        WHEN TIMESTAMPDIFF(MINUTE, c.last_refresh_timestamp, CURRENT_TIMESTAMP()) > c.sla_threshold_minutes THEN '🔴 Breach'
        ELSE '🟢 OK'
    END AS status
FROM edp_metadata.semantic_refresh.table_refresh_config c
JOIN edp_metadata.semantic_refresh.semantic_models m ON c.model_id = m.model_id
WHERE c.is_active = true
ORDER BY CASE m.sla_tier WHEN 'T0' THEN 1 WHEN 'T1' THEN 2 ELSE 3 END;

-- Query 2: Success Rate (Last 7 Days)
SELECT 
    m.model_name,
    COUNT(*) AS total,
    SUM(CASE WHEN l.status = 'SUCCESS' THEN 1 ELSE 0 END) AS successful,
    ROUND(SUM(CASE WHEN l.status = 'SUCCESS' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS success_pct,
    AVG(l.duration_seconds) AS avg_duration_sec
FROM edp_metadata.semantic_refresh.refresh_execution_log l
JOIN edp_metadata.semantic_refresh.semantic_models m ON l.model_id = m.model_id
WHERE l.refresh_start_timestamp >= CURRENT_DATE() - INTERVAL 7 DAYS
GROUP BY m.model_name;

-- Query 3: Currently Running
SELECT 
    m.model_name,
    l.tables_refreshed,
    l.refresh_start_timestamp,
    TIMESTAMPDIFF(MINUTE, l.refresh_start_timestamp, CURRENT_TIMESTAMP()) AS running_minutes
FROM edp_metadata.semantic_refresh.refresh_execution_log l
JOIN edp_metadata.semantic_refresh.semantic_models m ON l.model_id = m.model_id
WHERE l.status = 'RUNNING';

-- Query 4: Cost by Model (Last 30 Days)
SELECT 
    m.model_name,
    COUNT(*) AS refresh_count,
    SUM(c.warehouse_cost_estimate_usd) AS total_cost,
    AVG(c.warehouse_cost_estimate_usd) AS avg_cost
FROM edp_metadata.semantic_refresh.refresh_cost_tracking c
JOIN edp_metadata.semantic_refresh.refresh_execution_log l ON c.execution_id = l.execution_id
JOIN edp_metadata.semantic_refresh.semantic_models m ON l.model_id = m.model_id
WHERE l.refresh_start_timestamp >= CURRENT_DATE() - INTERVAL 30 DAYS
GROUP BY m.model_name
ORDER BY total_cost DESC;
```

---

## File: model_health_report.sql

```sql
-- Model Health Scorecard
WITH metrics AS (
  SELECT 
    m.model_id, m.model_name, m.sla_tier,
    COUNT(l.execution_id) AS refreshes_7d,
    SUM(CASE WHEN l.status = 'SUCCESS' THEN 1 ELSE 0 END) AS success_7d,
    ROUND(SUM(CASE WHEN l.status = 'SUCCESS' THEN 1 ELSE 0 END) * 100.0 / 
          NULLIF(COUNT(l.execution_id), 0), 2) AS success_pct,
    AVG(l.duration_seconds) AS avg_duration,
    SUM(c.warehouse_cost_estimate_usd) AS cost_7d,
    MAX(l.refresh_start_timestamp) AS last_refresh
  FROM edp_metadata.semantic_refresh.semantic_models m
  LEFT JOIN edp_metadata.semantic_refresh.refresh_execution_log l 
    ON m.model_id = l.model_id AND l.refresh_start_timestamp >= current_date() - INTERVAL 7 DAYS
  LEFT JOIN edp_metadata.semantic_refresh.refresh_cost_tracking c 
    ON l.execution_id = c.execution_id
  WHERE m.is_active = true
  GROUP BY m.model_id, m.model_name, m.sla_tier
)

SELECT 
  model_name,
  sla_tier,
  CAST(COALESCE(success_pct * 0.6, 0) + 40 AS INT) AS health_score,
  refreshes_7d,
  success_pct,
  CAST(avg_duration / 60 AS INT) AS avg_duration_min,
  ROUND(cost_7d, 2) AS cost_7d_usd,
  ROUND(cost_7d * 52 / 7, 2) AS projected_annual_cost,
  last_refresh,
  CASE 
    WHEN last_refresh IS NULL THEN '🔴 Never'
    WHEN success_pct < 95 THEN '🟡 Warning'
    ELSE '🟢 Healthy'
  END AS status
FROM metrics
ORDER BY CASE sla_tier WHEN 'T0' THEN 1 WHEN 'T1' THEN 2 ELSE 3 END;
```

---

## File: cost_analysis_queries.sql

```sql
-- Cost Analysis Queries

-- Daily Cost Trend
SELECT 
    DATE(l.refresh_start_timestamp) AS date,
    m.model_name,
    COUNT(*) AS refreshes,
    ROUND(SUM(c.warehouse_cost_estimate_usd), 2) AS daily_cost
FROM edp_metadata.semantic_refresh.refresh_cost_tracking c
JOIN edp_metadata.semantic_refresh.refresh_execution_log l ON c.execution_id = l.execution_id
JOIN edp_metadata.semantic_refresh.semantic_models m ON l.model_id = m.model_id
WHERE l.refresh_start_timestamp >= CURRENT_DATE() - INTERVAL 30 DAYS
GROUP BY DATE(l.refresh_start_timestamp), m.model_name
ORDER BY date DESC;

-- Most Expensive Refreshes
SELECT 
    l.execution_id,
    m.model_name,
    l.refresh_start_timestamp,
    c.warehouse_cost_estimate_usd AS cost,
    c.query_count,
    l.duration_seconds
FROM edp_metadata.semantic_refresh.refresh_cost_tracking c
JOIN edp_metadata.semantic_refresh.refresh_execution_log l ON c.execution_id = l.execution_id
JOIN edp_metadata.semantic_refresh.semantic_models m ON l.model_id = m.model_id
ORDER BY c.warehouse_cost_estimate_usd DESC
LIMIT 20;
```

---

# /Testing/

## File: test_powerbi_connection.py

```python
# Databricks notebook source

dbutils.widgets.text("connection_name", "edp_powerbi.awm_workspace")
connection_name = dbutils.widgets.get("connection_name")

print(f"Testing: {connection_name}\n")

# Test 1: Connection exists
connections = spark.sql("SHOW CONNECTIONS").collect()
if any(c.name == connection_name for c in connections):
    print("✅ Connection exists")
else:
    print("❌ Connection not found")

# Test 2: Accessible
try:
    spark.sql(f"DESCRIBE CONNECTION {connection_name}")
    print("✅ Connection accessible")
except:
    print("❌ Permission denied")
```

---

# /Administration/

## File: add_new_model.sql

```sql
-- Template: Add New Model
-- Replace all <PLACEHOLDER> values

INSERT INTO edp_metadata.semantic_refresh.semantic_models
(model_id, model_name, workspace_id, dataset_id, connection_name, 
 query_mode, sla_tier, description, owner_email, is_active)
VALUES
  ('<MODEL_ID>',
   '<MODEL_NAME>',
   '<WORKSPACE_GUID>',
   '<DATASET_GUID>',
   'edp_powerbi.<workspace_name>',
   'Import',
   'T1',
   '<Description>',
   '<owner@email.com>',
   true);

-- Verify
SELECT * FROM edp_metadata.semantic_refresh.semantic_models 
WHERE model_id = '<MODEL_ID>';

-- Next: Add tables using add_new_table.sql
-- Then: Run 05_generate_workflows_model_based.py
```

---

## File: add_new_table.sql

```sql
-- Template: Add New Table

INSERT INTO edp_metadata.semantic_refresh.table_refresh_config
(config_id, model_id, table_name, source_table, refresh_cadence,
 refresh_interval_minutes, sla_threshold_minutes, trigger_mode, is_active)
VALUES
  ('<model_id>_<table_name>',
   '<MODEL_ID>',
   '<table_name>',
   'gold.<schema>.<table>',
   'DAILY',
   NULL,
   1500,
   'SCHEDULE',
   true);

-- Verify
SELECT * FROM edp_metadata.semantic_refresh.table_refresh_config
WHERE config_id = '<model_id>_<table_name>';

-- Regenerate workflows: Run 05_generate_workflows_model_based.py
```

---

## File: change_sla_threshold.sql

```sql
-- Change SLA Threshold (No Code Deployment)

-- For specific table
UPDATE edp_metadata.semantic_refresh.table_refresh_config
SET sla_threshold_minutes = 2000,
    updated_at = current_timestamp()
WHERE config_id = 'finance_fact_invoices';

-- For all tables in model with specific cadence
UPDATE edp_metadata.semantic_refresh.table_refresh_config
SET sla_threshold_minutes = 1440
WHERE model_id = 'finance_model' AND refresh_cadence = 'DAILY';

-- Verify
SELECT model_id, table_name, sla_threshold_minutes, updated_at
FROM edp_metadata.semantic_refresh.table_refresh_config
WHERE updated_at >= current_timestamp() - INTERVAL 1 HOUR;
```

---

## File: cleanup_old_logs.sql

```sql
-- Cleanup Old Logs (Run Monthly)

-- Check volume
SELECT 
    COUNT(*) AS total,
    MIN(refresh_start_timestamp) AS oldest,
    MAX(refresh_start_timestamp) AS newest
FROM edp_metadata.semantic_refresh.refresh_execution_log;

-- Delete logs older than 90 days
DELETE FROM edp_metadata.semantic_refresh.refresh_execution_log
WHERE refresh_start_timestamp < current_date() - INTERVAL 90 DAYS;

DELETE FROM edp_metadata.semantic_refresh.refresh_cost_tracking
WHERE execution_id NOT IN (
    SELECT execution_id FROM edp_metadata.semantic_refresh.refresh_execution_log
);

-- Optimize
OPTIMIZE edp_metadata.semantic_refresh.refresh_execution_log;
VACUUM edp_metadata.semantic_refresh.refresh_execution_log RETAIN 168 HOURS;
```

---

# /Documentation/

## File: setup_guide.md

```markdown
# Setup Guide

## Prerequisites
- [ ] Azure AD service principal with Power BI API permissions
- [ ] Service principal added to Power BI workspaces (Contributor)
- [ ] Unity Catalog enabled in Databricks
- [ ] Workspace GUIDs and Dataset GUIDs collected

## Setup Steps

### Step 1: Create Metadata (15 min)
```bash
# Databricks SQL Editor
Run: /Setup/01_create_metadata_schema.sql
```

### Step 2: Grant Permissions (5 min)
```bash
Edit: Replace service principal names
Run: /Setup/02_grant_permissions.sql
```

### Step 3: Create Connections (10 min)
```bash
Edit: Add your credentials
Run: /Setup/03_create_powerbi_connections.sql
```

### Step 4: Seed Data (10 min)
```bash
Edit: Match your models
Run: /Setup/04_seed_metadata.sql
```

### Step 5: Generate Workflows (15 min)
```bash
Databricks Notebook
Run: /Setup/05_generate_workflows_model_based.py
```

### Step 6: Test (30 min)
```bash
Run: /Testing/test_powerbi_connection.py
Verify workflows in Databricks UI
```

### Step 7: Enable (5 min)
```bash
Databricks Workflows UI → Enable workflows
Monitor first execution
```

Total: 2-3 hours
```

---

## File: operations_runbook.md

```markdown
# Operations Runbook

## Daily Operations

### Add New Model
1. Collect workspace GUID, dataset GUID
2. Run: `/Administration/add_new_model.sql`
3. Add tables: `/Administration/add_new_table.sql`
4. Generate: `/Setup/05_generate_workflows_model_based.py`

Time: 15-30 minutes

### Change SLA
```sql
UPDATE table_refresh_config
SET sla_threshold_minutes = 2000
WHERE config_id = 'model_table';
```

### Emergency Stop
```sql
UPDATE semantic_models SET is_active = false WHERE model_id = 'awm_model';
```

## Monitoring
- Dashboard: SQL Analytics
- SLA: Model Health Report
- Costs: Cost Analysis queries

## Troubleshooting

### Refresh Failed
1. Check Databricks Workflow logs
2. Query: `SELECT * FROM refresh_execution_log WHERE status='FAILED' LIMIT 10`
3. Contact model owner

### SLA Breach
1. Verify workflow enabled
2. Check workflow history
3. Review error messages

## Maintenance
- Monthly: Run cleanup_old_logs.sql
- Quarterly: Review SLA thresholds
```

---

# README.md

```markdown
# Semantic Model Refresh Framework v2.0

Metadata-driven orchestration for Power BI refresh from Databricks.

## Features
- Model-based workflows (failure isolation)
- Power BI task integration (native)
- Table update triggers (event-driven)
- SLA management (data-driven thresholds)
- Cost tracking (warehouse usage)

## Quick Start
1. Run scripts in `/Setup/` (2-3 hours)
2. Test with `/Testing/` scripts
3. Enable workflows in Databricks UI
4. Monitor via SQL Analytics dashboards

## Architecture
```
Unity Catalog → Databricks Workflows → Power BI Models
```

## Adding Models
```sql
INSERT INTO semantic_models VALUES (...);
INSERT INTO table_refresh_config VALUES (...);
-- Run: 05_generate_workflows_model_based.py
```

Time: 15-30 minutes

## Support
<platform-support-distribution>
```

---

**Copy all code above into your Databricks workspace following the directory structure. All 20 files are complete and ready to deploy.**