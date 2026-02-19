# Logo Kits

This directory contains organized sets of logos for generating architecture diagrams.

## Structure

Each subdirectory is a **logo kit** - a collection of logos for a specific use case:

```
logos/
├── default/          # Default Databricks-focused logos
├── aws/             # AWS + Databricks logos
├── azure/           # Azure + Databricks logos
├── gcp/             # GCP + Databricks logos
└── custom/          # Your custom logo collections
```

## Using Logo Kits

### In Configuration

Edit `configs/default.yaml`:
```yaml
logo_kit:
  logo_dir: "./logos/default"  # or ./logos/aws, ./logos/azure, etc.
```

### Via CLI (when supported)

```bash
bricksmith generate \
    --diagram-spec spec.yaml \
    --template baseline \
    --logo-kit aws  # Use logos/aws/ directory
```

### Via Environment Variable

```bash
export BRICKSMITH_LOGO_KIT=./logos/azure
bricksmith generate --diagram-spec spec.yaml --template baseline
```

## Creating a New Logo Kit

1. **Create directory:**
   ```bash
   mkdir -p logos/my-customer
   ```

2. **Add logo files:**
   ```bash
   cp /path/to/logos/*.jpg logos/my-customer/
   ```

3. **Create README:**
   ```bash
   nano logos/my-customer/README.md
   ```

4. **Use it:**
   ```yaml
   # In configs/custom.yaml
   logo_kit:
     logo_dir: "./logos/my-customer"
   ```

## Logo File Requirements

- **Format:** `.jpg`, `.jpeg`, or `.png`
- **Size:** Maximum 5MB per file
- **Naming:** Lowercase with hyphens (e.g., `databricks-logo.jpg`)
- **Quality:** High resolution recommended (but will be resized for diagrams)

## Standard Logo Names

The system recognizes these logo names (filename without extension):

| Logo Name | Description | Typical Files |
|-----------|-------------|---------------|
| `databricks` | Databricks logo | `databricks-logo.jpg` |
| `delta-lake` | Delta Lake logo | `delta-lake-logo.jpg` |
| `uc` | Unity Catalog logo | `uc-logo.jpg` |
| `aws` | AWS logo | `aws-logo.jpg` |
| `azure` | Azure logo | `azure-logo.jpg` |
| `gcp` | GCP logo | `gcp-logo.jpg` |
| `s3` | AWS S3 | `s3-logo.jpg` |
| `glue` | AWS Glue | `glue-logo.jpg` |
| `redshift` | AWS Redshift | `redshift-logo.jpg` |
| `synapse` | Azure Synapse | `synapse-logo.jpg` |
| `blob-storage` | Azure Blob Storage | `blob-storage-logo.jpg` |
| `bigquery` | GCP BigQuery | `bigquery-logo.jpg` |
| `cloud-storage` | GCP Cloud Storage | `cloud-storage-logo.jpg` |

## Logo Kit Examples

### Default Kit (Databricks Core)

```
logos/default/
├── databricks-logo.jpg       # Red Databricks icon
├── delta-lake-logo.jpg       # Teal Delta Lake triangle
├── uc-logo.jpg               # Unity Catalog (pink/yellow/hexagon)
└── mlflow-logo.jpg           # MLflow logo
```

### AWS Kit

```
logos/aws/
├── databricks-logo.jpg       # Databricks
├── aws-logo.jpg              # AWS logo
├── s3-logo.jpg               # S3 bucket
├── glue-logo.jpg             # AWS Glue
├── redshift-logo.jpg         # Redshift
└── ec2-logo.jpg              # EC2
```

### Azure Kit

```
logos/azure/
├── databricks-logo.jpg       # Databricks
├── azure-logo.jpg            # Azure logo
├── blob-storage-logo.jpg     # Blob Storage
├── synapse-logo.jpg          # Synapse Analytics
├── data-factory-logo.jpg     # Data Factory
└── eventhub-logo.jpg         # Event Hub
```

### Customer-Specific Kit

```
logos/acme-corp/
├── databricks-logo.jpg       # Databricks
├── acme-logo.jpg             # Customer logo
├── internal-tool-logo.jpg    # Custom internal tools
└── partner-logo.jpg          # Partner systems
```

## Best Practices

### 1. Keep Kits Focused

Each kit should serve a specific use case:
- ✅ `aws/` - AWS cloud provider logos
- ✅ `acme-corp/` - Specific customer engagement
- ❌ `random-logos/` - Unfocused collection

### 2. Include Core Databricks Logos

Every kit should include:
- `databricks-logo.jpg`
- `delta-lake-logo.jpg`
- `uc-logo.jpg`

### 3. Document Your Logos

Create a README.md in each kit explaining:
- What logos are included
- When to use this kit
- Logo sources/licenses

### 4. Version Control

- ✅ Commit logo files to git (they're assets)
- ✅ Track changes to logo kits
- ✅ Document logo updates in commit messages

### 5. Logo Quality

- Use official logos from vendor sites
- Maintain consistent resolution
- Prefer square aspect ratios
- Use transparent backgrounds when possible

## Logo Sources

### Official Vendor Sites

- **Databricks:** https://databricks.com/company/brand
- **AWS:** https://aws.amazon.com/architecture/icons/
- **Azure:** https://learn.microsoft.com/en-us/azure/architecture/icons/
- **GCP:** https://cloud.google.com/icons

### Copyright & Licensing

- Only use logos you have permission to use
- Respect trademark guidelines
- Document logo sources in your kit's README

## Troubleshooting

### "Logo not found"

```bash
# Verify logo exists
ls logos/default/databricks-logo.jpg

# Check config points to correct directory
cat configs/default.yaml | grep logo_dir
```

### "Invalid logo format"

```bash
# Check file extension
file logos/default/my-logo.jpg

# Convert if needed
convert my-logo.png my-logo.jpg
```

### "Logo too large"

```bash
# Check file size
du -h logos/default/*.jpg

# Resize if needed (max 5MB)
convert large-logo.jpg -resize 2000x2000 -quality 85 resized-logo.jpg
```

## Related Documentation

- [LOGO_SETUP.md](../docs/bricksmith/LOGO_SETUP.md) - Detailed logo configuration
- [AUTHENTICATION.md](../docs/bricksmith/AUTHENTICATION.md) - Setup guide
- [README.md](../README.md) - Main project documentation

---

**Need help?** See the main README or create an issue.
