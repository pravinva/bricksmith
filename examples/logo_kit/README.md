# Logo Kit Directory

## 📁 Required Logo Files

Place these 7 logo files in this directory:

| # | Filename | Description | Notes |
|---|----------|-------------|-------|
| 1 | `databricks-logo.jpg` | Databricks (red icon) | Required |
| 2 | `delta-lake-logo.jpg` | Delta Lake (teal icon) | Required |
| 3 | `uc-logo.jpg` | Unity Catalog (pink/yellow/hexagon) | Required |
| 4 | `kaluza_logo_black.jpg` | Kaluza (three hexagons) | Required |
| 5 | `AGL_Energy_logo.svg.jpg` | AGL Energy logo | Required |
| 6 | `aws-logo.jpg` | AWS (grey text + orange smile) | Required |
| 7 | `azure-logo.jpg` | Azure (blue symbol) | Required |

## ✅ File Requirements

- **Format**: `.jpg`, `.jpeg`, or `.png` only
- **Size**: Maximum 5MB per logo file
- **Quality**: High resolution works best for AI generation
- **Naming**: Use exact filenames listed above

## 🔍 Validation

After adding logos, validate them:

```bash
# Quick check
./check-logos.sh

# Or detailed validation
nano-banana validate-logos --logo-dir examples/logo_kit
```

## 🎯 How to Use in Diagram Specs

**IMPORTANT**: Reference logos by **name**, NOT filename!

```yaml
components:
  - id: "databricks"
    label: "Databricks"
    type: "service"
    logo_name: "databricks"  # ← Use name, NOT "databricks-logo.jpg"!
```

### Logo Name Reference

| Logo File | Use This Name |
|-----------|---------------|
| `databricks-logo.jpg` | `logo_name: "databricks"` |
| `delta-lake-logo.jpg` | `logo_name: "delta-lake"` |
| `uc-logo.jpg` | `logo_name: "uc"` |
| `kaluza_logo_black.jpg` | `logo_name: "kaluza"` |
| `AGL_Energy_logo.svg.jpg` | `logo_name: "agl"` |
| `aws-logo.jpg` | `logo_name: "aws"` |
| `azure-logo.jpg` | `logo_name: "azure"` |

## 📚 Complete Documentation

- **[LOGO_REFERENCE.md](LOGO_REFERENCE.md)** - Quick reference card
- **[LOGO_SETUP.md](../../LOGO_SETUP.md)** - Complete logo setup guide
- **[Example diagram](../diagram_specs/all_logos_example.yaml)** - Using all logos

## 🤖 How It Works

The system uses **descriptions** (not filenames) to tell the AI about logos:

1. **Load**: System loads logo files from this directory
2. **Hash**: Computes SHA256 hash for each (for tracking/reproducibility)
3. **Convert**: Converts to format needed by Vertex AI
4. **Describe**: Injects descriptions into prompt (e.g., "red icon" not "databricks-logo.jpg")

This ensures **NO filenames appear in generated diagrams** (critical requirement!).

## 📋 Current Descriptions

These descriptions are sent to the AI model:

- **databricks**: "red icon"
- **delta-lake**: "teal icon"
- **uc**: "pink squares, yellow triangles, hexagon in middle"
- **kaluza**: "three hexagons stacked"
- **agl**: "AGL Energy logo"
- **aws**: "grey text with orange smile"
- **azure**: "blue symbol"

If your logos don't match these descriptions, see [LOGO_SETUP.md](../../LOGO_SETUP.md) for customization instructions.

## 🚨 Critical Requirements

✅ **DO**:
- Use exact filenames listed above
- Provide high-quality images
- Validate after adding files
- Reference by logo name in specs (not filename)

❌ **DON'T**:
- Don't commit logo files to git (they're in .gitignore)
- Don't use filenames in diagram specs
- Don't exceed 5MB per file
- Don't use unsupported formats (only .jpg, .jpeg, .png)

## 📝 Next Steps

1. Add all 7 logo files to this directory
2. Run `./check-logos.sh` to validate
3. Try the example: `examples/diagram_specs/all_logos_example.yaml`
4. Generate your first diagram!

## 🆘 Troubleshooting

### "Logo not found" error
- Check filename exactly matches expected name
- Ensure file is in `examples/logo_kit/` directory
- Run `./check-logos.sh` to see what's loaded

### "File too large" error
- Resize logo to < 5MB
- Use JPEG format for smaller size
- Compress image without losing quality

### Filename appears in diagram
- **Critical violation!** Score Logo Fidelity as 0
- This shouldn't happen if configured correctly
- Contact support if issue persists

---

**Note**: Logo files are NOT tracked in git (.gitignore). Add your own logos after cloning.
