# Logo Kits - Organizing Multiple Logo Sets

## Overview

Nano Banana Pro supports **multiple logo kits** - organized collections of logos for different use cases. This allows you to maintain separate logo sets for different cloud providers, customers, or scenarios.

## Directory Structure

```
logos/
├── README.md           # Master documentation
├── default/           # Core Databricks logos
│   ├── README.md
│   ├── INSTRUCTIONS.md
│   ├── databricks-logo.jpg
│   ├── delta-lake-logo.jpg
│   └── uc-logo.jpg
├── aws/              # AWS + Databricks
│   ├── README.md
│   ├── databricks-logo.jpg
│   ├── s3-logo.jpg
│   ├── glue-logo.jpg
│   └── redshift-logo.jpg
├── azure/            # Azure + Databricks
│   ├── README.md
│   ├── databricks-logo.jpg
│   ├── blob-storage-logo.jpg
│   └── synapse-logo.jpg
└── gcp/              # GCP + Databricks
    ├── README.md
    ├── databricks-logo.jpg
    ├── cloud-storage-logo.jpg
    └── bigquery-logo.jpg
```

## Using Logo Kits

### Method 1: Configuration File (Recommended)

Edit your config file to point to the desired logo kit:

**configs/default.yaml:**
```yaml
logo_kit:
  logo_dir: "./logos/default"
```

**configs/aws.yaml:**
```yaml
logo_kit:
  logo_dir: "./logos/aws"
```

**Usage:**
```bash
# Use default config (logos/default/)
nano-banana generate --diagram-spec spec.yaml --template baseline

# Use AWS config (logos/aws/)
nano-banana generate --config configs/aws.yaml --diagram-spec spec.yaml --template baseline
```

### Method 2: Environment Variable

```bash
# Set logo kit
export NANO_BANANA_LOGO_KIT__LOGO_DIR="./logos/azure"

# Generate diagram
nano-banana generate --diagram-spec spec.yaml --template baseline
```

### Method 3: CLI Flag (Future)

When implemented:
```bash
nano-banana generate \
    --diagram-spec spec.yaml \
    --template baseline \
    --logo-kit aws  # Uses logos/aws/
```

## Creating Custom Logo Kits

### Step 1: Create Directory

```bash
mkdir -p logos/acme-corp
```

### Step 2: Add README

```bash
cat > logos/acme-corp/README.md << 'EOF'
# ACME Corp Logo Kit

Logos for ACME Corp engagement.

## Included Logos

- databricks-logo.jpg
- acme-logo.jpg
- internal-system-logo.jpg

## When to Use

Use this kit for ACME Corp architecture diagrams and presentations.
EOF
```

### Step 3: Add Logo Files

```bash
# Copy logos
cp ~/Downloads/databricks-logo.jpg logos/acme-corp/
cp ~/Downloads/acme-logo.jpg logos/acme-corp/
cp ~/Downloads/internal-system.jpg logos/acme-corp/internal-system-logo.jpg
```

### Step 4: Create Config

```bash
cat > configs/acme-corp.yaml << 'EOF'
vertex:
  project_id: "fe-dev-sandbox"
  location: "us-central1"
  model_id: "gemini-3-pro-image-preview"
  temperature: 0.4

mlflow:
  tracking_uri: "databricks"
  experiment_name: "/Users/${DATABRICKS_USER}/acme-corp-diagrams"

logo_kit:
  logo_dir: "./logos/acme-corp"
  max_logo_size_mb: 5.0
  allowed_extensions: [".jpg", ".jpeg", ".png"]
EOF
```

### Step 5: Use It

```bash
nano-banana generate \
    --config configs/acme-corp.yaml \
    --diagram-spec prompts/diagram_specs/acme-architecture.yaml \
    --template baseline
```

## Pre-Built Logo Kits

### Default Kit

**Use case:** Generic Databricks architectures, cloud-agnostic diagrams

**Logos:**
- databricks-logo.jpg
- delta-lake-logo.jpg
- uc-logo.jpg
- mlflow-logo.jpg

**Config:**
```yaml
logo_kit:
  logo_dir: "./logos/default"
```

### AWS Kit

**Use case:** AWS customer engagements, lakehouse on AWS

**Logos:**
- Core Databricks logos
- aws-logo.jpg
- s3-logo.jpg
- glue-logo.jpg
- redshift-logo.jpg
- ec2-logo.jpg
- kinesis-logo.jpg
- lambda-logo.jpg

**Config:**
```yaml
logo_kit:
  logo_dir: "./logos/aws"
```

### Azure Kit

**Use case:** Azure customer engagements, lakehouse on Azure

**Logos:**
- Core Databricks logos
- azure-logo.jpg
- blob-storage-logo.jpg
- synapse-logo.jpg
- data-factory-logo.jpg
- eventhub-logo.jpg

**Config:**
```yaml
logo_kit:
  logo_dir: "./logos/azure"
```

### GCP Kit

**Use case:** GCP customer engagements, lakehouse on GCP

**Logos:**
- Core Databricks logos
- gcp-logo.jpg
- cloud-storage-logo.jpg
- bigquery-logo.jpg
- dataflow-logo.jpg
- pubsub-logo.jpg

**Config:**
```yaml
logo_kit:
  logo_dir: "./logos/gcp"
```

## Logo Kit Management

### Listing Available Kits

```bash
ls -1 logos/
# default
# aws
# azure
# gcp
# acme-corp
```

### Validating a Kit

```bash
nano-banana validate-logos --logo-dir logos/aws
```

### Syncing Kits

Keep core Databricks logos consistent across all kits:

```bash
# Update databricks logo in all kits
for kit in logos/*/; do
    cp logos/default/databricks-logo.jpg "$kit"
done
```

## Best Practices

### 1. Keep Core Logos Consistent

Every kit should have the same versions of:
- databricks-logo.jpg
- delta-lake-logo.jpg
- uc-logo.jpg

This ensures brand consistency across all diagrams.

### 2. Document Each Kit

Every kit should have:
- `README.md` - Overview and usage
- `INSTRUCTIONS.md` or similar - Setup instructions

### 3. Organize by Use Case

Create kits based on **scenarios**, not just technology:

✅ **Good organization:**
- `logos/aws/` - AWS cloud provider
- `logos/retail/` - Retail industry logos
- `logos/healthcare/` - Healthcare industry logos
- `logos/customer-x/` - Specific customer

❌ **Poor organization:**
- `logos/all-logos/` - Everything mixed together
- `logos/misc/` - Unclear purpose

### 4. Version Control

Commit logo files to git:
```bash
git add logos/
git commit -m "Add AWS logo kit"
```

### 5. Share Kits Across Team

```bash
# Package a kit
tar -czf aws-logo-kit.tar.gz logos/aws/

# Share with team
# Team member extracts to their logos/ directory
tar -xzf aws-logo-kit.tar.gz
```

## Troubleshooting

### "Logo not found" Error

```bash
# Check which kit is configured
cat configs/default.yaml | grep logo_dir

# List logos in that kit
ls logos/default/

# Verify logo exists
ls logos/default/databricks-logo.jpg
```

### Wrong Kit Being Used

```bash
# Check environment variable
echo $NANO_BANANA_LOGO_KIT__LOGO_DIR

# Unset if incorrect
unset NANO_BANANA_LOGO_KIT__LOGO_DIR

# Explicitly specify config
nano-banana generate --config configs/aws.yaml ...
```

### Kit Has Old Logos

```bash
# Update from default kit
cp logos/default/databricks-logo.jpg logos/aws/
cp logos/default/delta-lake-logo.jpg logos/aws/

# Or sync all core logos
for logo in databricks-logo.jpg delta-lake-logo.jpg uc-logo.jpg; do
    cp logos/default/$logo logos/aws/
done
```

## Advanced: Dynamic Kit Selection

For advanced users, you can create wrapper scripts:

```bash
#!/bin/bash
# generate-aws.sh - Always use AWS kit

export NANO_BANANA_LOGO_KIT__LOGO_DIR="./logos/aws"
nano-banana generate "$@"
```

Usage:
```bash
./generate-aws.sh --diagram-spec spec.yaml --template baseline
```

## Related Documentation

- [logos/README.md](../../logos/README.md) - Logo kit overview
- [LOGO_SETUP.md](LOGO_SETUP.md) - Logo configuration details
- [AUTHENTICATION.md](AUTHENTICATION.md) - Setup guide

---

**Questions?** See the main README or create an issue.
