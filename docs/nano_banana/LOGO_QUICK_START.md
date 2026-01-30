# Logo Setup - Quick Start 🎨

**TL;DR**: Add 7 logo files → Run `./check-logos.sh` → Use logo **names** (not filenames) in diagram specs

## 🎯 The Key Concept

**Filenames are NEVER sent to the AI model. Only descriptions!**

```
Logo File              Logo Name            Description in Prompt
─────────────          ─────────            ─────────────────────
databricks-logo.jpg → "databricks"      → "red icon"
delta-lake-logo.jpg → "delta-lake"     → "teal icon"
uc-logo.jpg         → "uc"             → "pink squares, yellow triangles..."
```

This is **critical** to prevent filenames from appearing in generated diagrams.

## ✅ 3-Step Setup

### Step 1: Add Logo Files

Add these 7 files to `logos/default/`:

```
logos/default/
├── databricks-logo.jpg        ← Red icon
├── delta-lake-logo.jpg        ← Teal icon
├── uc-logo.jpg                ← Unity Catalog (pink/yellow/hexagon)
├── kaluza_logo_black.jpg      ← Three hexagons stacked
├── AGL_Energy_logo.svg.jpg    ← AGL Energy logo
├── aws-logo.jpg               ← AWS (grey text + orange smile)
└── azure-logo.jpg             ← Azure (blue symbol)
```

**Requirements**:
- Format: `.jpg`, `.jpeg`, or `.png`
- Size: < 5MB each
- Quality: High resolution recommended

### Step 2: Validate

```bash
source .venv/bin/activate

# Quick validation
./check-logos.sh

# Or detailed validation
nano-banana validate-logos --logo-dir logos/default
```

### Step 3: Use in Diagram Specs

Use **logo names**, NOT filenames:

```yaml
components:
  - id: "databricks"
    label: "Databricks Workspace"
    type: "service"
    logo_name: "databricks"  # ✅ Correct - logo name

  # NOT THIS:
  # logo_name: "databricks-logo.jpg"  # ❌ Wrong - filename!
```

## 📋 Logo Name Reference

| Logo File | Use This Name in YAML |
|-----------|-----------------------|
| `databricks-logo.jpg` | `logo_name: "databricks"` |
| `delta-lake-logo.jpg` | `logo_name: "delta-lake"` |
| `uc-logo.jpg` | `logo_name: "uc"` |
| `kaluza_logo_black.jpg` | `logo_name: "kaluza"` |
| `AGL_Energy_logo.svg.jpg` | `logo_name: "agl"` |
| `aws-logo.jpg` | `logo_name: "aws"` |
| `azure-logo.jpg` | `logo_name: "azure"` |

## 🧪 Test It

Generate a test diagram with all logos:

```bash
source .venv/bin/activate
source .env  # If using Databricks MLflow

nano-banana generate \
    --diagram-spec prompts/diagram_specs/all_logos_example.yaml \
    --template baseline \
    --run-name "logo-test"

# Check output
open outputs/output_*.png
```

## 🤖 What the AI Model Sees

When you generate a diagram, the prompt includes:

```
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
```

**Note**: No mention of `.jpg` files - only descriptions!

## 🎨 Customizing Descriptions

If your logos don't match the default descriptions, edit `src/nano_banana/logos.py`:

```python
DEFAULT_LOGO_DESCRIPTIONS = {
    "databricks": "your custom description here",
    "databricks-logo": "your custom description here",
    # ... etc
}
```

See **[LOGO_SETUP.md](LOGO_SETUP.md)** for detailed instructions.

## 📚 Complete Documentation

- **[LOGO_REFERENCE.md](logos/default/LOGO_REFERENCE.md)** - Quick reference card with copy-paste examples
- **[LOGO_SETUP.md](LOGO_SETUP.md)** - Complete logo configuration guide
- **[logos/default/README.md](logos/default/README.md)** - Logo directory documentation
- **[all_logos_example.yaml](prompts/diagram_specs/all_logos_example.yaml)** - Example using all 7 logos

## ⚡ Quick Commands

```bash
# Check logo setup
./check-logos.sh

# Validate logos
nano-banana validate-logos --logo-dir logos/default

# Generate test diagram
nano-banana generate \
    --diagram-spec prompts/diagram_specs/all_logos_example.yaml \
    --template baseline

# View all available prompt templates
ls prompts/prompt_templates/
```

## 🚨 Common Mistakes

❌ **Using filenames in diagram specs**:
```yaml
logo_name: "databricks-logo.jpg"  # WRONG!
```

✅ **Using logo names**:
```yaml
logo_name: "databricks"  # CORRECT!
```

---

❌ **Expecting filenames in prompts**:
The AI model never sees "databricks-logo.jpg"

✅ **Understanding descriptions are used**:
The AI model sees "red icon" (the description)

---

❌ **Forgetting to validate**:
Logos might not load correctly

✅ **Always validate after adding**:
```bash
./check-logos.sh
```

## 🎯 Next Steps

1. ✅ Add your 7 logo files to `logos/default/`
2. ✅ Run `./check-logos.sh` to validate
3. ✅ Review `logos/default/LOGO_REFERENCE.md` for copy-paste examples
4. ✅ Generate test diagram with `all_logos_example.yaml`
5. ✅ Create your own diagram specs using logo names
6. ✅ Evaluate logo fidelity in generated diagrams

---

**Remember**: The AI sees **descriptions**, not filenames. This is how we ensure no filenames leak into your diagrams! 🎨✨
