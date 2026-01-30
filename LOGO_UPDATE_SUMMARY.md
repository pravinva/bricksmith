# Logo Files Update Summary

## What Was Updated

The application has been updated to work with your refactored logo files.

## Your Logo Structure

```
logos/
├── default/           # Core Databricks logos (7 files)
│   ├── databricks-full.png
│   ├── delta.png
│   ├── iceberg.png
│   ├── MLflow-logo-final-black.png
│   ├── postgres-logo.png
│   ├── unity-catalog-solo.png
│   └── unity-catalog.png
│
├── aws/              # AWS cloud (1 file)
│   └── Amazon_Web_Services_Logo.png
│
├── azure/            # Azure cloud (1 file)
│   └── Microsoft_Azure.png
│
├── gcp/              # GCP cloud (1 file)
│   └── Google_cloud.png
│
├── agl/              # AGL Energy customer (2 files)
│   ├── AGL_Energy_logo.png
│   └── kaluza_logo_black.png
│
└── other/            # AI/ML tools (5 files)
    ├── Claude_AI_symbol.png
    ├── Model_Context_Protocol_logo.png
    ├── plotly.png
    ├── Python_logo_and_wordmark.png
    └── Python-logo-notext.svg.png
```

## Changes Made

### 1. Updated Logo Descriptions (logos.py)

✅ Added descriptions for all your logo files:

| Logo File | Logo Name | Description |
|-----------|-----------|-------------|
| `databricks-full.png` | `databricks-full` | "red/orange stacked bars icon with 'databricks' text" |
| `delta.png` | `delta` | "teal/cyan triangle icon" |
| `iceberg.png` | `iceberg` | "blue iceberg icon" |
| `unity-catalog.png` | `unity-catalog` | "pink squares, yellow triangles, navy hexagon in center" |
| `unity-catalog-solo.png` | `unity-catalog-solo` | "pink squares, yellow triangles, navy hexagon icon" |
| `MLflow-logo-final-black.png` | `mlflow-logo-final-black` | "black MLflow logo with text" |
| `postgres-logo.png` | `postgres-logo` | "blue elephant icon" |
| `Amazon_Web_Services_Logo.png` | `amazon_web_services_logo` | "orange and black AWS logo" |
| `Microsoft_Azure.png` | `microsoft_azure` | "blue Microsoft Azure symbol" |
| `Google_cloud.png` | `google_cloud` | "multi-color Google Cloud logo" |
| `AGL_Energy_logo.png` | `agl_energy_logo` | "cyan/teal AGL Energy logo with rays" |
| `kaluza_logo_black.png` | `kaluza_logo_black` | "three black hexagons in triangular pattern" |
| `Claude_AI_symbol.png` | `claude_ai_symbol` | "orange/coral Claude AI symbol" |
| `Model_Context_Protocol_logo.png` | `model_context_protocol_logo` | "purple Model Context Protocol logo" |
| `plotly.png` | `plotly` | "blue Plotly logo" |
| `Python_logo_and_wordmark.png` | `python_logo_and_wordmark` | "blue and yellow Python logo with text" |
| `Python-logo-notext.svg.png` | `python-logo-notext.svg` | "blue and yellow Python logo without text" |

### 2. Updated Logo Kit READMEs

✅ `logos/default/README.md` - Updated to show actual logos
✅ `logos/aws/README.md` - Updated for AWS kit
✅ `logos/azure/README.md` - Updated for Azure kit
✅ `logos/gcp/README.md` - Updated for GCP kit
✅ `logos/agl/README.md` - NEW for AGL Energy
✅ `logos/other/README.md` - NEW for AI/ML tools

### 3. Updated Example Files

✅ `examples/diagram_specs/example_basic.yaml` - Uses correct logo names

## How to Use Your Logos

### Default Kit (Core Databricks)

```yaml
# examples/diagram_specs/my-diagram.yaml
name: "databricks-lakehouse"
description: "Core lakehouse architecture"

components:
  - id: "databricks"
    label: "Databricks"
    logo_name: "databricks-full"

  - id: "delta"
    label: "Delta Lake"
    logo_name: "delta"

  - id: "uc"
    label: "Unity Catalog"
    logo_name: "unity-catalog"

  - id: "mlflow"
    label: "MLflow"
    logo_name: "mlflow-logo-final-black"

  - id: "postgres"
    label: "PostgreSQL"
    logo_name: "postgres-logo"
```

### AGL Energy Kit

```bash
# Create config for AGL
cat > configs/agl.yaml << 'YAML'
logo_kit:
  logo_dir: "./logos/agl"
YAML

# Use in diagram
nano-banana generate \
    --config configs/agl.yaml \
    --diagram-spec my-agl-diagram.yaml \
    --template baseline
```

```yaml
# Diagram with AGL logos
components:
  - id: "agl"
    label: "AGL Energy"
    logo_name: "agl_energy_logo"

  - id: "kaluza"
    label: "Kaluza Platform"
    logo_name: "kaluza_logo_black"
```

### AI/ML Tools Kit

```bash
# Set environment variable
export NANO_BANANA_LOGO_KIT__LOGO_DIR="./logos/other"

# Generate diagram
nano-banana generate --diagram-spec ai-pipeline.yaml --template baseline
```

```yaml
# Diagram with AI tools
components:
  - id: "python"
    label: "Python App"
    logo_name: "python_logo_and_wordmark"

  - id: "claude"
    label: "Claude AI"
    logo_name: "claude_ai_symbol"

  - id: "mcp"
    label: "MCP Server"
    logo_name: "model_context_protocol_logo"

  - id: "plotly"
    label: "Visualizations"
    logo_name: "plotly"
```

### Cloud Provider Logos

```yaml
# AWS diagram
components:
  - id: "aws"
    label: "AWS Cloud"
    logo_name: "amazon_web_services_logo"

# Azure diagram
components:
  - id: "azure"
    label: "Azure Cloud"
    logo_name: "microsoft_azure"

# GCP diagram
components:
  - id: "gcp"
    label: "Google Cloud"
    logo_name: "google_cloud"
```

## Testing Your Setup

```bash
# 1. Verify logos are detected
nano-banana validate-logos --logo-dir logos/default

# 2. List available logo names
ls logos/default/*.png | xargs -n1 basename | sed 's/.png$//'

# 3. Generate test diagram
nano-banana generate \
    --diagram-spec examples/diagram_specs/example_basic.yaml \
    --template baseline \
    --run-name "test-logos"

# 4. Check output
ls outputs/
```

## Logo Name Mapping

The system automatically converts filenames to logo names:

| Filename | Logo Name (use in YAML) |
|----------|------------------------|
| `databricks-full.png` | `databricks-full` |
| `delta.png` | `delta` |
| `unity-catalog.png` | `unity-catalog` |
| `MLflow-logo-final-black.png` | `mlflow-logo-final-black` |
| `Amazon_Web_Services_Logo.png` | `amazon_web_services_logo` |
| `Microsoft_Azure.png` | `microsoft_azure` |
| `Google_cloud.png` | `google_cloud` |
| `AGL_Energy_logo.png` | `agl_energy_logo` |
| `kaluza_logo_black.png` | `kaluza_logo_black` |
| `Claude_AI_symbol.png` | `claude_ai_symbol` |
| `Python_logo_and_wordmark.png` | `python_logo_and_wordmark` |

**Rules:**
- Filename without extension → logo name
- Converted to lowercase
- Underscores and hyphens preserved
- Use exact logo name in diagram specs

## Configuration Examples

### Default Kit (Already Configured)
```yaml
# configs/default.yaml
logo_kit:
  logo_dir: "./logos/default"
```

### AGL Kit
```yaml
# configs/agl.yaml
logo_kit:
  logo_dir: "./logos/agl"
```

### AI Tools Kit
```yaml
# configs/ai-tools.yaml
logo_kit:
  logo_dir: "./logos/other"
```

### Multi-Cloud Kit
```bash
# Copy logos from multiple kits
mkdir -p logos/multi-cloud
cp logos/default/*.png logos/multi-cloud/
cp logos/aws/*.png logos/multi-cloud/
cp logos/azure/*.png logos/multi-cloud/
cp logos/gcp/*.png logos/multi-cloud/

# Use it
logo_kit:
  logo_dir: "./logos/multi-cloud"
```

## Next Steps

1. **Generate your first diagram:**
   ```bash
   nano-banana generate \
       --diagram-spec examples/diagram_specs/example_basic.yaml \
       --template baseline
   ```

2. **Try the new visual refinement feature:**
   ```bash
   nano-banana refine-prompt \
       --run-id <run-id> \
       --feedback "logos look great!"
   ```

3. **Create custom diagram specs:**
   - Use logo names from tables above
   - Reference `examples/diagram_specs/example_basic.yaml`
   - See `logos/*/README.md` for examples

## Troubleshooting

### "Logo not found" Error

```bash
# Check which logos are loaded
nano-banana validate-logos --logo-dir logos/default

# Verify logo name matches filename
ls logos/default/databricks-full.png
# Use logo_name: "databricks-full" in YAML
```

### Wrong Logo Appears

Check logo description in `src/nano_banana/logos.py`:
- Line 16-87: DEFAULT_LOGO_DESCRIPTIONS
- Logo descriptions are used instead of filenames to prevent leakage

### Need to Add More Logos

```bash
# 1. Download logo
# 2. Convert to PNG if needed
# 3. Copy to appropriate kit
cp new-logo.png logos/default/

# 4. Add description to logos.py if needed
# 5. Regenerate
```

---

**Status:** ✅ Application updated and ready to use your logos!
