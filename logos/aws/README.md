# AWS Logo Kit

Databricks + AWS cloud provider logos.

## Included Logos

| File | Description | Use Case |
|------|-------------|----------|
| `Amazon_Web_Services_Logo.png` | AWS logo (orange/black) | Cloud provider branding |

**Note:** Add Databricks logos from `logos/default/` as needed:
- Copy `databricks-full.png`, `delta.png`, `unity-catalog.png` from default kit
- Add AWS service logos (S3, Glue, Redshift, etc.) as needed

## When to Use This Kit

Use this kit for:
- ✅ AWS customer engagements
- ✅ Lakehouse on AWS architectures
- ✅ AWS service integration diagrams
- ✅ Cloud migration (to/from AWS)

## Getting AWS Logos

Download official AWS Architecture Icons:
- **URL:** https://aws.amazon.com/architecture/icons/
- **License:** Free for architecture diagrams
- **Format:** SVG, PNG (convert to JPG if needed)

## Example Diagram Spec

```yaml
name: "aws-lakehouse"
description: "Databricks lakehouse on AWS with S3"

components:
  - id: "aws"
    label: "AWS"
    logo_name: "amazon_web_services_logo"

  - id: "databricks"
    label: "Databricks"
    logo_name: "databricks-full"

  - id: "delta"
    label: "Delta Lake"
    logo_name: "delta"

connections:
  - from_id: "s3"
    to_id: "databricks"
    label: "Ingest"

  - from_id: "databricks"
    to_id: "redshift"
    label: "Export"
```

## Logo Descriptions

| Logo | Description in Prompt |
|------|----------------------|
| `amazon_web_services_logo` | "orange and black AWS logo" |

**When you add more AWS service logos, update this table accordingly.**

## Related Kits

- `logos/default/` - Core Databricks logos only
- `logos/azure/` - Databricks + Azure
- `logos/gcp/` - Databricks + GCP
