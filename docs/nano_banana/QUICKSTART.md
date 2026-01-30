# Quick Start Guide

Your Nano Banana Pro system is configured and ready to use!

## Configuration

✅ **GCP Project**: `fe-dev-sandbox`
✅ **Model**: `gemini-3-pro-image-preview`
✅ **Vertex AI Authentication**: Working (verified)
✅ **MLflow**: Configured for **Databricks** (centralized tracking)

## 🔗 Databricks MLflow Setup

Your system is configured to send **all MLflow traces to Databricks**. To complete the setup:

### Quick Setup

```bash
# Run the Databricks setup script
./setup-databricks.sh
```

### Manual Setup

1. **Create `.env` file**:
   ```bash
   cp .env.example .env
   ```

2. **Add your Databricks credentials** to `.env`:
   ```bash
   DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
   DATABRICKS_TOKEN=dapi...
   DATABRICKS_USER=your.email@company.com
   GCP_PROJECT_ID=fe-dev-sandbox
   ```

3. **Load environment variables**:
   ```bash
   source .env
   ```

4. **Verify connection**:
   ```bash
   source .venv/bin/activate
   python -c "import mlflow; mlflow.set_tracking_uri('databricks'); print('✓ Connected')"
   ```

### Getting Your Databricks Token

1. Log in to your Databricks workspace
2. Click your username → **User Settings**
3. Go to **Access Tokens** tab
4. Click **Generate New Token**
5. Copy and save the token securely

See **[DATABRICKS_SETUP.md](DATABRICKS_SETUP.md)** for detailed instructions.

## Immediate Next Steps

### 1. Add Your Logo Files

Place your logo files in `examples/logo_kit/`:

```bash
# Required logos (see examples/logo_kit/README.md for details):
examples/logo_kit/
├── databricks-logo.jpg
├── delta-lake-logo.jpg
├── uc-logo.jpg
├── kaluza_logo_black.jpg
├── AGL_Energy_logo.svg.jpg
├── aws-logo.jpg
└── azure-logo.jpg
```

### 2. Validate Logo Kit

```bash
source .venv/bin/activate
nano-banana validate-logos --logo-dir examples/logo_kit
```

### 3. Generate Your First Diagram

```bash
# Activate environment
source .venv/bin/activate

# Load Databricks credentials
source .env

# Generate diagram (will track in Databricks MLflow)
nano-banana generate \
    --diagram-spec examples/diagram_specs/example_basic.yaml \
    --template baseline \
    --run-name "my-first-diagram"

# Output will be saved to: outputs/output_<run-id>.png
```

### 4. Evaluate the Diagram

```bash
# Interactive evaluation (you'll be prompted for scores)
nano-banana evaluate <run-id>
```

### 5. View in Databricks MLflow UI

Your runs are tracked in **Databricks MLflow**:

1. Open your Databricks workspace
2. Navigate to: **Machine Learning → Experiments**
3. Find: `/Users/your.email@company.com/vertexai-nanobanana-arch-diagrams`
4. View runs with all parameters, metrics, and artifacts

**Alternative**: Use local MLflow UI (if not using Databricks):
```bash
# Override to use local tracking
export NANO_BANANA_MLFLOW__TRACKING_URI="file:./mlruns"
mlflow ui
# Open http://localhost:5000
```

## Quick Commands Reference

```bash
# List all CLI commands
nano-banana --help

# Check authentication
nano-banana check-auth

# Verify complete setup
nano-banana verify-setup

# List recent runs
nano-banana list-runs --max-results 10

# Show run details
nano-banana show-run <run-id>

# Generate with tags
nano-banana generate \
    --diagram-spec examples/diagram_specs/example_basic.yaml \
    --template baseline \
    --run-name "test-run" \
    --tag "experiment=baseline" \
    --tag "version=1"
```

## Example Workflow

1. **Create a diagram spec** (YAML):
   ```yaml
   name: "my-architecture"
   description: "My system architecture"
   components:
     - id: "db"
       label: "Databricks"
       type: "service"
       logo_name: "databricks"
   connections:
     - from_id: "source"
       to_id: "db"
   constraints:
     layout: "left-to-right"
   ```

2. **Generate**:
   ```bash
   nano-banana generate --diagram-spec my-spec.yaml --template baseline
   ```

3. **Evaluate**:
   ```bash
   nano-banana evaluate <run-id>
   ```

4. **Iterate**: Modify prompt template or diagram spec and regenerate

5. **Compare**: View all runs in MLflow UI to compare results

## Available Prompt Templates

- **baseline** - Clean, professional diagrams
- **detailed** - Highly detailed with emphasis on clarity
- **minimal** - Simple, minimal style

Templates are in `examples/prompt_templates/` - edit or create new ones!

## Example Diagram Specs

- **example_basic.yaml** - Simple lakehouse architecture
- **example_complex.yaml** - Multi-cloud lakehouse

Specs are in `examples/diagram_specs/` - create your own!

## Troubleshooting

### Authentication Issues

```bash
# Re-authenticate
gcloud auth application-default login

# Verify
nano-banana check-auth
```

### Enable Vertex AI API

If you get "API not enabled" errors:

```bash
gcloud services enable aiplatform.googleapis.com --project fe-dev-sandbox
```

### Logo Issues

```bash
# Validate logos
nano-banana validate-logos --logo-dir examples/logo_kit

# Check requirements:
# - Format: .jpg, .jpeg, .png
# - Size: < 5MB
# - Must be valid images
```

## Documentation

- **README.md** - Full overview
- **docs/setup.md** - Detailed setup instructions
- **docs/usage.md** - Complete usage guide
- **CLAUDE.md** - Architecture and development guide

## Key Constraints to Remember

⚠️ **Critical Requirements**:
- Logos must be reused EXACTLY as provided
- NO filenames may appear in generated diagrams
- All logos must be scaled uniformly
- OAuth-only authentication (no API keys)

## Support

For issues:
1. Check the documentation in `docs/`
2. Review the PRD: `# PRD: MLflow-Tracked Prompt Engineering.md`
3. Run `nano-banana verify-setup` to diagnose issues

---

**Ready to generate architecture diagrams!** 🎨

Start by adding your logos to `examples/logo_kit/`, then run:

```bash
./setup.sh  # Or follow steps above manually
```
