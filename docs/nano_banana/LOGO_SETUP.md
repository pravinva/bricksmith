# Logo Setup Guide for Nano Banana Pro

This guide explains how to configure your logo kit for diagram generation.

## 🎯 Critical Concept: Logo Descriptions vs Filenames

**IMPORTANT**: The AI model receives **descriptions** of logos, NOT filenames. This ensures no filenames appear in generated diagrams.

### How It Works

1. **Physical Files**: Actual logo image files in `examples/logo_kit/`
2. **Logo Names**: Internal identifiers (derived from filename without extension)
3. **Descriptions**: Human-readable descriptions sent to the AI model

```
databricks-logo.jpg  →  logo name: "databricks-logo"  →  description: "red icon"
                                                          ↓
                                              Sent to AI model in prompt
```

## 📁 Your Logo Files

Place these files in `examples/logo_kit/`:

```
examples/logo_kit/
├── databricks-logo.jpg        # Databricks logo (red icon)
├── delta-lake-logo.jpg        # Delta Lake logo (teal icon)
├── uc-logo.jpg                # Unity Catalog (pink squares, yellow triangles, hexagon)
├── kaluza_logo_black.jpg      # Kaluza logo (three hexagons stacked)
├── AGL_Energy_logo.svg.jpg    # AGL Energy logo
├── aws-logo.jpg               # AWS logo (grey text with orange smile)
└── azure-logo.jpg             # Azure logo (blue symbol)
```

### File Requirements

- **Format**: `.jpg`, `.jpeg`, or `.png`
- **Size**: Maximum 5MB per file
- **Naming**: Lowercase with hyphens or underscores (e.g., `databricks-logo.jpg`)
- **Quality**: High resolution works best

## 🏷️ Current Logo Descriptions

The system currently has these logo descriptions configured:

| Logo File | Logo Name(s) | Description in Prompt |
|-----------|--------------|----------------------|
| `databricks-logo.jpg` | `databricks`, `databricks-logo` | "red icon" |
| `delta-lake-logo.jpg` | `delta-lake`, `delta-lake-logo` | "teal icon" |
| `uc-logo.jpg` | `uc`, `uc-logo`, `unity-catalog` | "pink squares, yellow triangles, hexagon in middle" |
| `kaluza_logo_black.jpg` | `kaluza`, `kaluza_logo_black` | "three hexagons stacked" |
| `AGL_Energy_logo.svg.jpg` | `agl`, `agl_energy` | "AGL Energy logo" |
| `aws-logo.jpg` | `aws`, `aws-logo` | "grey text with orange smile" |
| `azure-logo.jpg` | `azure`, `azure-logo` | "blue symbol" |

These descriptions are what the AI model sees in the prompt.

## 🔧 Customizing Logo Descriptions

If your logos don't match the default descriptions, you can customize them.

### Option 1: Edit the Code (Permanent)

Edit `src/nano_banana/logos.py`:

```python
DEFAULT_LOGO_DESCRIPTIONS = {
    "databricks": "your custom description",
    "databricks-logo": "your custom description",
    # ... add more
}
```

### Option 2: Create a Custom Logo Config File

Create `configs/my-logos.py`:

```python
# Custom logo descriptions
LOGO_DESCRIPTIONS = {
    "databricks": "red square with white DB letters",
    "databricks-logo": "red square with white DB letters",
    "delta-lake": "teal triangle with delta symbol",
    "delta-lake-logo": "teal triangle with delta symbol",
    # ... continue for all logos
}
```

Then modify the code to load from this file (advanced).

### Best Practices for Descriptions

✅ **Good descriptions** (visual, specific):
- "red icon" ✓
- "grey text with orange smile" ✓
- "three hexagons stacked vertically" ✓
- "teal triangle with delta symbol inside" ✓

❌ **Bad descriptions** (include filenames or paths):
- "databricks-logo.jpg" ✗
- "the file databricks.png" ✗
- "logo_databricks" ✗

## 🎨 Using Logos in Diagram Specs

In your YAML diagram specs, reference logos by their **logo name**:

```yaml
components:
  - id: "databricks"
    label: "Databricks Workspace"
    type: "service"
    logo_name: "databricks"  # ← Logo name (not filename!)

  - id: "delta"
    label: "Delta Lake"
    type: "storage"
    logo_name: "delta-lake"  # ← Logo name

  - id: "uc"
    label: "Unity Catalog"
    type: "service"
    logo_name: "uc"  # ← Can use short form
```

### Logo Name Matching

The system is **flexible** with logo names:

- `databricks` → matches `databricks-logo.jpg`
- `databricks-logo` → matches `databricks-logo.jpg`
- `delta-lake` → matches `delta-lake-logo.jpg`
- `uc` → matches `uc-logo.jpg`
- `unity-catalog` → matches `uc-logo.jpg`

All the underscores/hyphens variations are handled automatically.

## 📝 Example: How Descriptions Appear in Prompts

When you generate a diagram, the system builds a prompt like this:

```
You are generating a clean architecture diagram.

Logo kit provided as image references:
- Databricks (red icon)
- Delta Lake (teal icon)
- Unity Catalog (pink squares, yellow triangles, hexagon in middle)
- Kaluza (three hexagons stacked)
- Agl Energy (AGL Energy logo)
- Aws (grey text with orange smile)
- Azure (blue symbol)

CRITICAL CONSTRAINTS:
- Reuse uploaded logos EXACTLY as provided
- Scale all logos uniformly
- NO filenames or file labels may appear in the output

[... rest of prompt with diagram spec ...]
```

Note: **No filenames** - only descriptions!

## ✅ Validation

After adding your logo files, validate them:

```bash
source .venv/bin/activate

# Validate logo kit
nano-banana validate-logos --logo-dir examples/logo_kit
```

This shows:
- Logo names discovered
- Descriptions assigned
- File sizes
- SHA256 hashes (for tracking)

### Expected Output

```
Logo Kit (7 logos)
┌──────────────────┬────────────────────────────────────┬──────────┬──────────────┐
│ Name             │ Description                         │ Size     │ Hash (first) │
├──────────────────┼────────────────────────────────────┼──────────┼──────────────┤
│ agl_energy       │ AGL Energy logo                     │ 45.2 KB  │ a1b2c3d4     │
│ aws              │ grey text with orange smile         │ 23.1 KB  │ e5f6g7h8     │
│ azure            │ blue symbol                          │ 18.9 KB  │ i9j0k1l2     │
│ databricks       │ red icon                             │ 32.4 KB  │ m3n4o5p6     │
│ delta-lake       │ teal icon                            │ 28.7 KB  │ q7r8s9t0     │
│ kaluza_logo_black│ three hexagons stacked              │ 41.3 KB  │ u1v2w3x4     │
│ uc               │ pink squares, yellow triangles, ... │ 52.8 KB  │ y5z6a7b8     │
└──────────────────┴────────────────────────────────────┴──────────┴──────────────┘

✓ All logos valid!
```

## 🚨 Troubleshooting

### Logo Not Found

**Error**: `KeyError: Logo 'databricks' not found in cache`

**Solutions**:
1. Check logo file exists in `examples/logo_kit/`
2. Verify filename matches expected pattern
3. Run `validate-logos` to see what was loaded
4. Check logo name in diagram spec matches loaded names

### Wrong Description

**Problem**: AI model uses wrong logo or doesn't match well

**Solutions**:
1. Make description more specific and visual
2. Edit `DEFAULT_LOGO_DESCRIPTIONS` in `src/nano_banana/logos.py`
3. Regenerate diagram after updating descriptions

### Filename Appears in Output

**Problem**: Generated diagram shows "databricks-logo.jpg" text

**Solutions**:
1. This is a **critical violation** - score Logo Fidelity as 0
2. Strengthen prompt template constraints
3. Use `detailed` template which has stronger constraints
4. Add more explicit "NO FILENAMES" instruction to custom template

### Logo Not Matching Diagram

**Problem**: AI generates new logo instead of using provided one

**Solutions**:
1. Ensure logo image quality is high
2. Make description match logo visually
3. Use `detailed` template for stronger enforcement
4. Try lowering temperature for more consistency

## 🎯 Quick Setup Checklist

1. ✅ Add all 7 logo files to `examples/logo_kit/`
2. ✅ Run `nano-banana validate-logos --logo-dir examples/logo_kit`
3. ✅ Verify descriptions match your actual logos
4. ✅ (Optional) Customize descriptions if needed
5. ✅ Use logo names in diagram specs (not filenames!)
6. ✅ Generate test diagram
7. ✅ Evaluate for logo fidelity

## 📚 Related Documentation

- **examples/logo_kit/README.md** - Logo requirements
- **examples/diagram_specs/example_basic.yaml** - Example using logos
- **docs/usage.md** - Complete usage guide
- **QUICKSTART.md** - Quick reference

---

**Remember**: The AI model sees **descriptions**, not filenames. This is how we ensure no filenames leak into generated diagrams! 🎨
