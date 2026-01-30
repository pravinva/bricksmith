# Azure Logo Kit

Databricks + Azure cloud provider logos.

## Included Logos

| File | Description | Use Case |
|------|-------------|----------|
| `Microsoft_Azure.png` | Azure logo (blue symbol) | Cloud provider branding |

**Note:** Add Databricks logos from `logos/default/` as needed:
- Copy `databricks-full.png`, `delta.png`, `unity-catalog.png` from default kit
- Add Azure service logos (Blob Storage, Synapse, Data Factory, etc.) as needed

## When to Use This Kit

Use this kit for:
- ✅ Azure customer engagements
- ✅ Lakehouse on Azure architectures
- ✅ Azure service integration diagrams
- ✅ Migration from Synapse to Databricks

## Getting Azure Logos

Download official Azure Architecture Icons:
- **URL:** https://learn.microsoft.com/en-us/azure/architecture/icons/
- **License:** Free for architecture diagrams
- **Format:** SVG (convert to JPG if needed)

## Example Diagram Spec

```yaml
name: "azure-lakehouse"
description: "Databricks lakehouse on Azure with ADLS"

components:
  - id: "azure"
    label: "Microsoft Azure"
    logo_name: "microsoft_azure"

  - id: "databricks"
    label: "Databricks"
    logo_name: "databricks-full"

  - id: "delta"
    label: "Delta Lake"
    logo_name: "delta"

connections:
  - from_id: "blob"
    to_id: "databricks"
    label: "Ingest"

  - from_id: "databricks"
    to_id: "synapse"
    label: "Export"
```

## Logo Descriptions

| Logo | Description in Prompt |
|------|----------------------|
| `microsoft_azure` | "blue Microsoft Azure symbol" |

**When you add more Azure service logos, update this table accordingly.**

## Related Kits

- `logos/default/` - Core Databricks logos only
- `logos/aws/` - Databricks + AWS
- `logos/gcp/` - Databricks + GCP
