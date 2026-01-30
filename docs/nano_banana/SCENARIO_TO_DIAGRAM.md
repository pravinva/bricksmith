# Scenario to Diagram Generation

Generate architecture diagrams from natural language descriptions using AI.

## Overview

Instead of manually writing YAML diagram specifications, you can describe your architecture scenario in plain English and let Nano Banana generate the specification for you.

**Two workflows available:**

1. **Two-step**: Generate spec → Review/edit → Generate diagram
2. **One-step**: Generate spec AND diagram immediately

## Quick Start

### One-Step Generation (Fastest)

```bash
nano-banana generate-from-scenario \
    --scenario "Build a lakehouse on AWS with Databricks processing data from S3 to Redshift"
```

This will:
1. Generate a YAML diagram spec from your scenario
2. Immediately create the diagram using the baseline template
3. Track everything in MLflow

### Two-Step Generation (More Control)

```bash
# Step 1: Generate the spec
nano-banana scenario-to-spec \
    --scenario "Real-time streaming pipeline with Kafka, Spark, and Delta Lake" \
    --output prompts/diagram_specs/streaming.yaml

# Step 2: Review and edit the spec if needed
nano prompts/diagram_specs/streaming.yaml

# Step 3: Generate the diagram
nano-banana generate \
    --diagram-spec prompts/diagram_specs/streaming.yaml \
    --template baseline
```

## Writing Good Scenarios

### What Makes a Good Scenario

Good scenarios are:
- **Specific**: Mention actual technologies (Databricks, S3, Kafka, etc.)
- **Structured**: Describe data flow from source to destination
- **Purposeful**: Explain what the architecture does
- **Complete**: Include all major components

### Examples

#### ✅ Good Scenarios

```bash
# Good: Specific technologies, clear flow
nano-banana generate-from-scenario \
    --scenario "Build a medallion architecture on Azure with Databricks.
    Ingest raw data from Blob Storage into Bronze tables, transform to Silver
    using Delta Lake, and serve Gold tables to Power BI for analytics."

# Good: Real-time use case with clear components
nano-banana generate-from-scenario \
    --scenario "Real-time fraud detection pipeline. Kafka streams transaction
    events to Databricks Structured Streaming, enriches with customer data from
    Unity Catalog, scores with MLflow models, and writes alerts to MongoDB."

# Good: Migration scenario
nano-banana generate-from-scenario \
    --scenario "Migrate from Teradata to Databricks lakehouse on GCP.
    Use Google Cloud Storage for data lake, Unity Catalog for governance,
    and Delta Lake for ACID transactions. Connect to existing BigQuery data warehouse."
```

#### ❌ Bad Scenarios

```bash
# Too vague
nano-banana generate-from-scenario \
    --scenario "Data pipeline with some databases"

# No data flow
nano-banana generate-from-scenario \
    --scenario "Databricks and S3"

# Missing key components
nano-banana generate-from-scenario \
    --scenario "Build a lakehouse"
```

## Command Reference

### `scenario-to-spec`

Generate YAML diagram specification from scenario.

**Options:**
- `--scenario` (required): Natural language architecture description
- `--output`: Path to save the spec (default: `prompts/diagram_specs/generated-<timestamp>.yaml`)

**Example:**
```bash
nano-banana scenario-to-spec \
    --scenario "IoT data pipeline with AWS IoT Core, Kinesis, Databricks, and S3" \
    --output prompts/diagram_specs/iot-pipeline.yaml
```

**Output:**
- YAML diagram specification file
- Console display of generated spec
- Component and connection counts

### `generate-from-scenario`

Generate spec AND diagram in one command.

**Options:**
- `--scenario` (required): Natural language architecture description
- `--template`: Prompt template (default: `baseline`)
- `--save-spec`: Optional path to save the generated spec
- `--run-name`: Optional MLflow run name

**Example:**
```bash
nano-banana generate-from-scenario \
    --scenario "Customer 360 on Databricks with Salesforce, Snowflake, and Tableau" \
    --template detailed \
    --save-spec prompts/diagram_specs/customer-360.yaml \
    --run-name "customer-360-demo"
```

**Output:**
- Generated diagram image in `outputs/`
- MLflow run with metrics and artifacts
- Optional: Saved diagram spec YAML

## How It Works

### Step 1: Scenario Analysis

The AI analyzes your scenario and identifies:
- **Components**: Services, databases, storage, compute, etc.
- **Data flow**: How data moves between components
- **Relationships**: Governance, metadata, optional connections

### Step 2: Logo Matching

Available logos are automatically matched to components:
- Checks your configured logo kit (default: `logos/default/`)
- Uses exact logo names from your logo collection
- Sets `logo_name: null` for components without logos

### Step 3: Structure Generation

Generates valid YAML with:
- **Component IDs**: snake-case identifiers (`databricks-workspace`)
- **Labels**: Sentence case display names (`Databricks Workspace`)
- **Types**: Appropriate component types (`service`, `storage`, `external`)
- **Connections**: Logical data flow with labels
- **Constraints**: Sensible layout and styling defaults

### Step 4: Validation

The generated YAML is:
- Parsed and validated for correct syntax
- Checked for required fields (name, description, components, connections)
- Converted to a `DiagramSpec` object
- Displayed for review

## Advanced Usage

### Custom Logo Kits

Use specific logo collections for different scenarios:

```bash
# AWS-specific scenario
export NANO_BANANA_LOGO_KIT__LOGO_DIR="./logos/aws"
nano-banana generate-from-scenario \
    --scenario "Databricks on AWS with S3, Glue, and Redshift"

# Azure-specific scenario
export NANO_BANANA_LOGO_KIT__LOGO_DIR="./logos/azure"
nano-banana generate-from-scenario \
    --scenario "Databricks on Azure with ADLS, Data Factory, and Synapse"
```

### Iterative Refinement

Generate, evaluate, and refine:

```bash
# 1. Generate initial diagram
nano-banana generate-from-scenario \
    --scenario "Your scenario here" \
    --save-spec prompts/diagram_specs/v1.yaml

# 2. Get the run ID from output, then evaluate
nano-banana evaluate <run-id>

# 3. Refine the diagram spec manually
nano prompts/diagram_specs/v1.yaml

# 4. Regenerate with refined spec
nano-banana generate --diagram-spec prompts/diagram_specs/v1.yaml --template baseline
```

### Template Selection

Choose templates based on complexity:

```bash
# Simple architectures
nano-banana generate-from-scenario \
    --scenario "Basic lakehouse with S3 and Databricks" \
    --template minimal

# Standard architectures
nano-banana generate-from-scenario \
    --scenario "Medallion architecture with governance" \
    --template baseline

# Complex architectures
nano-banana generate-from-scenario \
    --scenario "Multi-cloud data mesh with 15+ components" \
    --template detailed
```

## Example Scenarios by Use Case

### Lakehouse Architecture

```bash
nano-banana generate-from-scenario \
    --scenario "Modern lakehouse on AWS. Raw data from various sources lands in S3,
    Databricks processes it into Bronze, Silver, and Gold layers using Delta Lake,
    Unity Catalog provides governance, and BI tools query the Gold layer."
```

### Real-Time Streaming

```bash
nano-banana generate-from-scenario \
    --scenario "Real-time clickstream analytics. Kafka receives events from web apps,
    Databricks Structured Streaming processes in real-time, enriches with user profiles
    from Unity Catalog, and writes metrics to Delta Lake for dashboards."
```

### ML Pipeline

```bash
nano-banana generate-from-scenario \
    --scenario "MLOps pipeline on Databricks. Feature engineering in Delta Live Tables,
    model training with AutoML, model registry in MLflow, inference serving via
    Model Serving, and monitoring with Lakehouse Monitoring."
```

### Migration

```bash
nano-banana generate-from-scenario \
    --scenario "Migrate from on-prem Hadoop to Databricks on Azure. Lift data from HDFS
    to ADLS Gen2, replatform Hive tables to Delta Lake, modernize Spark jobs to notebooks,
    and integrate with existing Synapse Analytics."
```

### Data Mesh

```bash
nano-banana generate-from-scenario \
    --scenario "Data mesh architecture. Each domain team owns their data products in Unity
    Catalog. Central governance team manages policies and lineage. Consumers discover and
    access data products through Marketplace. Databricks Workflows orchestrate pipelines."
```

## Troubleshooting

### Generated Spec Has Wrong Logos

**Problem:** Component uses wrong logo or `null` when logo exists

**Solution:** Check logo names with `validate-logos`:
```bash
nano-banana validate-logos --logo-dir logos/default
```

Make sure your scenario mentions technologies that match your logo collection.

### Too Many/Few Components

**Problem:** Generated spec is too simple or too complex

**Solution:** Be more specific in your scenario:
- **Too few components**: Add more detail about data sources, processing steps, and destinations
- **Too many components**: Simplify scenario to focus on key architecture elements

### Wrong Connection Types

**Problem:** Connections use wrong style (solid/dashed/dotted)

**Solution:** Edit the generated YAML before generating diagram:
- `solid`: Data flow
- `dashed`: Governance, metadata, configuration
- `dotted`: Optional or conditional flow

### AI Generated Invalid YAML

**Problem:** YAML parsing error

**Solution:** Check the console output for the generated YAML. The error message will indicate what's wrong. Common issues:
- Missing required fields
- Invalid component IDs (must be snake-case)
- Incorrect indentation

Try regenerating with a more structured scenario description.

## Best Practices

1. **Start simple**: Test with simple scenarios first
2. **Be specific**: Mention actual technologies by name
3. **Review before generating**: Use two-step workflow for important diagrams
4. **Save specs**: Always use `--save-spec` to keep generated specifications
5. **Iterate**: Use MLflow to track iterations and improvements
6. **Match logo kits**: Configure appropriate logo kit for your cloud/tech stack

## Related Documentation

- [QUICKSTART.md](QUICKSTART.md) - Getting started with manual specs
- [PROMPT_REFINEMENT.md](PROMPT_REFINEMENT.md) - Refining generated diagrams
- [LOGO_KITS.md](LOGO_KITS.md) - Managing logo collections
- [AUTHENTICATION.md](AUTHENTICATION.md) - Setting up API keys

---

**New to Nano Banana?** Start with the [QUICKSTART.md](QUICKSTART.md) guide.
