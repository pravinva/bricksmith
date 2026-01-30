# Logo Reference Card

Quick reference for using logos in your diagram specifications.

## 📋 Your Logo Kit

| # | File Name | Use in YAML | Description Sent to AI |
|---|-----------|-------------|------------------------|
| 1 | `databricks-logo.jpg` | `logo_name: "databricks"` | "red icon" |
| 2 | `delta-lake-logo.jpg` | `logo_name: "delta-lake"` | "teal icon" |
| 3 | `uc-logo.jpg` | `logo_name: "uc"` | "pink squares, yellow triangles, hexagon in middle" |
| 4 | `kaluza_logo_black.jpg` | `logo_name: "kaluza"` | "three hexagons stacked" |
| 5 | `AGL_Energy_logo.svg.jpg` | `logo_name: "agl"` | "AGL Energy logo" |
| 6 | `aws-logo.jpg` | `logo_name: "aws"` | "grey text with orange smile" |
| 7 | `azure-logo.jpg` | `logo_name: "azure"` | "blue symbol" |

## 🎯 Quick Copy-Paste for Diagram Specs

### Databricks Component
```yaml
- id: "databricks"
  label: "Databricks Workspace"
  type: "service"
  logo_name: "databricks"
```

### Delta Lake Component
```yaml
- id: "delta-lake"
  label: "Delta Lake"
  type: "storage"
  logo_name: "delta-lake"
```

### Unity Catalog Component
```yaml
- id: "unity-catalog"
  label: "Unity Catalog"
  type: "service"
  logo_name: "uc"
```

### Kaluza Component
```yaml
- id: "kaluza"
  label: "Kaluza Analytics"
  type: "service"
  logo_name: "kaluza"
```

### AGL Energy Component
```yaml
- id: "agl"
  label: "AGL Energy"
  type: "consumer"
  logo_name: "agl"
```

### AWS Component
```yaml
- id: "aws-s3"
  label: "AWS S3"
  type: "storage"
  logo_name: "aws"
```

### Azure Component
```yaml
- id: "azure-storage"
  label: "Azure Storage"
  type: "storage"
  logo_name: "azure"
```

## ⚡ Important Notes

### ✅ DO:
- Use logo names from the "Use in YAML" column
- Descriptions are automatically added to prompts
- System handles variations (e.g., "databricks" or "databricks-logo" both work)

### ❌ DON'T:
- Don't use filenames: ~~`logo_name: "databricks-logo.jpg"`~~ ✗
- Don't include paths: ~~`logo_name: "./logos/databricks.jpg"`~~ ✗
- Don't worry about case: System converts to lowercase automatically

## 🔍 Validation Command

After adding logos, validate:

```bash
nano-banana validate-logos --logo-dir examples/logo_kit
```

## 📝 Example Diagram with All Logos

```yaml
name: "complete-architecture"
description: "Example using all available logos"

components:
  - id: "aws"
    label: "AWS S3"
    type: "storage"
    logo_name: "aws"

  - id: "azure"
    label: "Azure Blob"
    type: "storage"
    logo_name: "azure"

  - id: "databricks"
    label: "Databricks"
    type: "service"
    logo_name: "databricks"

  - id: "delta"
    label: "Delta Lake"
    type: "storage"
    logo_name: "delta-lake"

  - id: "uc"
    label: "Unity Catalog"
    type: "service"
    logo_name: "uc"

  - id: "kaluza"
    label: "Kaluza"
    type: "service"
    logo_name: "kaluza"

  - id: "agl"
    label: "AGL Energy"
    type: "consumer"
    logo_name: "agl"

connections:
  - from_id: "aws"
    to_id: "databricks"
  - from_id: "azure"
    to_id: "databricks"
  - from_id: "databricks"
    to_id: "delta"
  - from_id: "delta"
    to_id: "uc"
  - from_id: "uc"
    to_id: "kaluza"
  - from_id: "kaluza"
    to_id: "agl"

constraints:
  layout: "top-to-bottom"
  background: "white"
  spacing: "comfortable"
```

Save as `examples/diagram_specs/complete.yaml` and generate with:

```bash
nano-banana generate \
    --diagram-spec examples/diagram_specs/complete.yaml \
    --template baseline \
    --run-name "all-logos-test"
```
