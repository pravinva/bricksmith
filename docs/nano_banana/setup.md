# Setup Guide

Complete setup instructions for Nano Banana Pro.

## Prerequisites

### 1. Python 3.11+

```bash
python --version  # Should be 3.11 or higher
```

### 2. uv Package Manager

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify installation
uv --version
```

### 3. Google Cloud SDK

```bash
# Install gcloud CLI
# See: https://cloud.google.com/sdk/docs/install

# Verify installation
gcloud --version
```

### 4. GCP Project

- Create or use existing GCP project
- Enable Vertex AI API
- Set up billing

## Installation

### 1. Clone Repository

```bash
cd nano_banana
```

### 2. Create Virtual Environment

```bash
# Create venv with uv
uv venv

# Activate venv
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate     # Windows
```

### 3. Install Dependencies

```bash
# Install package in editable mode
uv pip install -e .

# Install dev dependencies (optional)
uv pip install -e ".[dev]"
```

### 4. Verify Installation

```bash
nano-banana --version
```

## Authentication

### OAuth Setup (Required)

Nano Banana Pro uses **OAuth-only** authentication. No API keys are supported.

```bash
# Log in with your Google Cloud account
gcloud auth application-default login

# Set your project
gcloud config set project YOUR_PROJECT_ID

# Verify authentication
nano-banana check-auth
```

### Environment Variables

```bash
# Required: Set your GCP project ID
export GCP_PROJECT_ID="your-gcp-project-id"

# Optional: Override other settings
export NANO_BANANA_VERTEX__LOCATION="us-central1"
export NANO_BANANA_VERTEX__MODEL_ID="gemini-3-pro-image-preview"
```

Add to `~/.bashrc` or `~/.zshrc` for persistence.

## Configuration

### 1. Default Configuration

The default config is at `configs/default.yaml`:

```yaml
vertex:
  project_id: "${GCP_PROJECT_ID}"
  location: "us-central1"
  model_id: "gemini-3-pro-image-preview"
  temperature: 0.4
  top_p: 0.95
  max_output_tokens: 8192
  image_size: "1024x1024"
  seed: 42

mlflow:
  tracking_uri: "file:./mlruns"
  experiment_name: "vertexai-nanobanana-arch-diagrams"

logo_kit:
  logo_dir: "./examples/logo_kit"
  max_logo_size_mb: 5.0
  allowed_extensions: [".jpg", ".jpeg", ".png"]
```

### 2. Custom Configuration

Create a custom config file:

```bash
cp configs/default.yaml configs/my-config.yaml
# Edit as needed
```

Use with CLI:

```bash
nano-banana --config configs/my-config.yaml generate ...
```

### 3. Environment Variable Overrides

Override any setting:

```bash
export NANO_BANANA_VERTEX__TEMPERATURE="0.6"
export NANO_BANANA_VERTEX__TOP_P="0.9"
export NANO_BANANA_MLFLOW__TRACKING_URI="http://localhost:5000"
```

Format: `NANO_BANANA_<section>__<key>=<value>`

## Logo Kit Setup

### 1. Obtain Logo Files

Acquire the required logo files:

- databricks-logo.jpg (Red Icon)
- delta-lake-logo.jpg (Teal Icon)
- uc-logo.jpg (Pink Squares, Yellow Triangles, Hexagon)
- kaluza_logo_black.jpg (Three hexagons stacked)
- AGL_Energy_logo.svg.jpg
- aws-logo.jpg (Grey text + Orange smile)
- azure-logo.jpg (Blue symbol)

### 2. Add to Logo Directory

```bash
# Copy logos to the logo kit directory
cp /path/to/your/logos/*.jpg examples/logo_kit/

# Verify logos
nano-banana validate-logos --logo-dir examples/logo_kit
```

### 3. Logo Requirements

- **Format**: .jpg, .jpeg, or .png
- **Size**: Maximum 5MB per logo
- **Quality**: Clear, high-resolution images work best
- **Naming**: Lowercase filenames (e.g., `databricks-logo.jpg`)

## MLflow Setup

### Local File-Based Tracking (Default)

No setup required. Runs are tracked in `./mlruns/`.

```bash
# View runs in MLflow UI
mlflow ui

# Open http://localhost:5000
```

### Remote MLflow Server

```bash
# Start MLflow server
mlflow server \
    --backend-store-uri sqlite:///mlflow.db \
    --default-artifact-root ./mlartifacts \
    --host 0.0.0.0 \
    --port 5000

# Configure client
export NANO_BANANA_MLFLOW__TRACKING_URI="http://localhost:5000"
```

### Databricks MLflow

```bash
export NANO_BANANA_MLFLOW__TRACKING_URI="databricks"
export DATABRICKS_HOST="https://your-workspace.cloud.databricks.com"
export DATABRICKS_TOKEN="your-token"
```

## Verification

### Complete Setup Check

```bash
nano-banana verify-setup
```

This checks:
- ✓ Vertex AI authentication
- ✓ MLflow configuration
- ✓ Logo directory exists
- ✓ Template directory exists

### Manual Checks

```bash
# Check auth
nano-banana check-auth

# Validate logos
nano-banana validate-logos --logo-dir examples/logo_kit

# List templates
ls examples/prompt_templates/

# List diagram specs
ls examples/diagram_specs/
```

## Troubleshooting

### Authentication Errors

**Error**: `DefaultCredentialsError`

**Solution**:
```bash
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

### API Not Enabled

**Error**: `Vertex AI API has not been used in project`

**Solution**:
```bash
gcloud services enable aiplatform.googleapis.com --project YOUR_PROJECT_ID
```

### Logo Validation Fails

**Error**: `Logo {name} is too large`

**Solution**: Resize image to < 5MB

**Error**: `Logo {name} is not a valid image`

**Solution**: Verify file is a valid image (not corrupted)

### MLflow Connection Issues

**Error**: `Connection refused`

**Solution**: Check tracking URI:
```bash
echo $NANO_BANANA_MLFLOW__TRACKING_URI
mlflow server --help
```

### Permission Denied

**Error**: `Permission denied` when writing outputs

**Solution**:
```bash
# Ensure write permissions
chmod 755 outputs/
mkdir -p outputs
```

## Next Steps

After setup is complete:

1. Read [Usage Guide](usage.md) for detailed usage instructions
2. Try generating your first diagram
3. Explore prompt templates
4. Review evaluation rubric

## Support

For additional help:
- Check the [README](../README.md)
- Review the [PRD document](../# PRD: MLflow-Tracked Prompt Engineering.md)
- Consult [CLAUDE.md](../CLAUDE.md) for architecture details
