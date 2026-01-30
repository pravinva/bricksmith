# GCP Logo Kit

Databricks + Google Cloud Platform logos.

## Included Logos

| File | Description | Use Case |
|------|-------------|----------|
| `Google_cloud.png` | GCP logo (multi-color) | Cloud provider branding |

**Note:** Add Databricks logos from `logos/default/` as needed:
- Copy `databricks-full.png`, `delta.png`, `unity-catalog.png` from default kit
- Add GCP service logos (Cloud Storage, BigQuery, Dataflow, etc.) as needed

## When to Use This Kit

Use this kit for:
- ✅ GCP customer engagements
- ✅ Lakehouse on GCP architectures
- ✅ GCP service integration diagrams
- ✅ Migration from BigQuery to Databricks

## Getting GCP Logos

Download official GCP Architecture Icons:
- **URL:** https://cloud.google.com/icons
- **License:** Free for architecture diagrams
- **Format:** SVG, PNG (convert to JPG if needed)

## Example Diagram Spec

```yaml
name: "gcp-lakehouse"
description: "Databricks lakehouse on GCP with Cloud Storage"

components:
  - id: "gcp"
    label: "Google Cloud"
    logo_name: "google_cloud"

  - id: "databricks"
    label: "Databricks"
    logo_name: "databricks-full"

  - id: "delta"
    label: "Delta Lake"
    logo_name: "delta"

connections:
  - from_id: "gcs"
    to_id: "databricks"
    label: "Ingest"

  - from_id: "databricks"
    to_id: "bigquery"
    label: "Export"
```

## Logo Descriptions

| Logo | Description in Prompt |
|------|----------------------|
| `google_cloud` | "multi-color Google Cloud logo" |

**When you add more GCP service logos, update this table accordingly.**

## Related Kits

- `logos/default/` - Core Databricks logos only
- `logos/aws/` - Databricks + AWS
- `logos/azure/` - Databricks + Azure
