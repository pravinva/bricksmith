# Guaranteed Logo Constraints ✅

## 🎯 The Answer: YES!

**Logo information and constraints are AUTOMATICALLY passed to ALL prompts**, regardless of which template you use.

## ✅ What's Guaranteed in EVERY Prompt

Every single prompt sent to the AI model includes:

### 1. Logo Descriptions (NOT Filenames!)

```
Logo kit provided as image references:
- Databricks (red icon)
- Delta Lake (teal icon)
- Unity Catalog (pink squares, yellow triangles, hexagon in middle)
- Kaluza (three hexagons stacked)
- Agl Energy (AGL Energy logo)
- Aws (grey text with orange smile)
- Azure (blue symbol)
```

### 2. Critical Logo Constraints

```
CRITICAL CONSTRAINTS:
- Reuse uploaded logos EXACTLY as provided
- Scale all logos uniformly
- NO filenames or file labels may appear in the output
```

### 3. Diagram Information

```
Diagram: your-diagram-name
Description: Your diagram description

Components:
- component-id: Component Label (type: service) [use logo-name logo]

Connections:
- from → to "Label" (style)

Layout Constraints:
- Layout: left-to-right
- Background: white
- etc.
```

## 🛡️ How It's Guaranteed

The system uses **3 levels of protection**:

### Level 1: Template Placeholders (Recommended)

If your template includes `{logo_section}` and `{diagram_section}`:

```
You are generating a diagram.

{logo_section}

{diagram_section}

Your custom instructions...
```

→ Constraints inserted via placeholders ✅

### Level 2: Auto-Injection

If your template is missing placeholders:

```
Create a simple diagram.

Your instructions...
```

→ System **automatically prepends** logo section and constraints ✅

### Level 3: Force-Injection

If somehow constraints are still missing (shouldn't happen):

```python
# System double-checks all critical constraints are present
if not all_constraints_present:
    # Force-inject at top of prompt
    prompt = constraint_block + prompt
```

→ Constraints **force-injected** ✅

## 🧪 Proof: Test Results

Run `./test-prompt-building.py` to verify:

```bash
source .venv/bin/activate
python test-prompt-building.py
```

**Results**:

```
Test 1: Template WITH {logo_section}
  ✅ has_logo_section: True
  ✅ has_reuse_constraint: True
  ✅ has_scale_constraint: True
  ✅ has_no_filename_constraint: True
  ✅ has_diagram_info: True

Test 2: Template WITHOUT {logo_section} (auto-inject)
  ✅ has_logo_section: True
  ✅ has_reuse_constraint: True
  ✅ has_scale_constraint: True
  ✅ has_no_filename_constraint: True
  ✅ has_diagram_info: True

Test 3: MINIMAL template (extreme test)
  ✅ has_logo_section: True
  ✅ has_reuse_constraint: True
  ✅ has_scale_constraint: True
  ✅ has_no_filename_constraint: True
  ✅ has_diagram_info: True

✅ SUCCESS: Logo constraints are ALWAYS included!
```

## 📝 Examples

### Example 1: Standard Template

**Your template** (`baseline.txt`):
```
You are generating a clean architecture diagram.

{logo_section}

{diagram_section}

Make it professional.
```

**Final prompt sent to AI**:
```
You are generating a clean architecture diagram.

Logo kit provided as image references:
- Databricks (red icon)
- Delta Lake (teal icon)
[... all logos ...]

CRITICAL CONSTRAINTS:
- Reuse uploaded logos EXACTLY as provided
- Scale all logos uniformly
- NO filenames or file labels may appear in the output

Diagram: my-diagram
Description: My architecture
[... diagram details ...]

Make it professional.
```

✅ Logo constraints included!

### Example 2: Minimal Template

**Your template** (`simple.txt`):
```
Generate a diagram.
```

**Final prompt sent to AI** (auto-injected):
```
Logo kit provided as image references:
- Databricks (red icon)
- Delta Lake (teal icon)
[... all logos ...]

CRITICAL CONSTRAINTS:
- Reuse uploaded logos EXACTLY as provided
- Scale all logos uniformly
- NO filenames or file labels may appear in the output

Generate a diagram.

Diagram: my-diagram
Description: My architecture
[... diagram details ...]
```

✅ Logo constraints auto-injected!

### Example 3: Custom Template

**Your template** (`custom.txt`):
```
Create a modern, sleek diagram for executives.

Use high contrast and professional colors.
Large, readable fonts.
Minimal clutter.
```

**Final prompt sent to AI** (auto-injected):
```
Logo kit provided as image references:
- Databricks (red icon)
- Delta Lake (teal icon)
[... all logos ...]

CRITICAL CONSTRAINTS:
- Reuse uploaded logos EXACTLY as provided
- Scale all logos uniformly
- NO filenames or file labels may appear in the output

Create a modern, sleek diagram for executives.

Use high contrast and professional colors.
Large, readable fonts.
Minimal clutter.

Diagram: my-diagram
Description: My architecture
[... diagram details ...]
```

✅ Logo constraints auto-injected!

## 🎨 What This Means for You

### You Can Focus On:

✅ Diagram style and aesthetics
✅ Layout preferences
✅ Color schemes
✅ Typography
✅ Audience-specific language
✅ Custom instructions

### You DON'T Need to Worry About:

❌ Remembering to include logo constraints
❌ Repeating "no filenames" instructions
❌ Logo descriptions
❌ Critical requirements

**The system handles all critical constraints automatically!**

## 🔍 Verification

After generating a diagram, you can verify constraints were included:

### Method 1: Check Logged Prompt

```bash
# Generate diagram
nano-banana generate --diagram-spec spec.yaml --template baseline

# View logged prompt artifact
cat mlruns/<experiment-id>/<run-id>/artifacts/prompts/prompt.txt
```

### Method 2: In Databricks MLflow

1. Navigate to your run
2. Click **Artifacts** tab
3. Open `prompts/prompt.txt`
4. Verify logo constraints are present

### Method 3: Programmatic Check

```python
from nano_banana.prompts import PromptBuilder

# After building prompt
validation = builder.validate_final_prompt(final_prompt)

# All should be True
assert validation["has_reuse_constraint"]
assert validation["has_scale_constraint"]
assert validation["has_no_filename_constraint"]
```

## 📚 Documentation

- **PROMPT_ENGINEERING.md** - Complete prompt engineering guide
- **LOGO_SETUP.md** - Logo configuration guide
- **test-prompt-building.py** - Test script (run to verify)
- **prompts/prompt_templates/** - Example templates

## 💡 Best Practices

### ✅ Recommended: Use Placeholders

```
{logo_section}
{diagram_section}
```

This gives you most control over where sections appear.

### ✅ Also Fine: Skip Placeholders

```
Your custom template without placeholders
```

System will auto-inject everything needed.

### ✅ Test Your Templates

```bash
python test-prompt-building.py
```

Verifies constraints are always included.

## 🚨 Critical Guarantee

**No matter what template you write, these constraints will ALWAYS be in your prompt:**

1. ✅ Logo descriptions (NOT filenames)
2. ✅ "Reuse uploaded logos EXACTLY as provided"
3. ✅ "Scale all logos uniformly"
4. ✅ "NO filenames or file labels may appear in the output"
5. ✅ Diagram specification
6. ✅ Component details
7. ✅ Connection information
8. ✅ Layout constraints

## 🎯 Summary

**Question**: Can we pass logo info to all prompts?

**Answer**: ✅ **YES - It's AUTOMATIC and GUARANTEED!**

- Logo descriptions: ✅ Auto-included
- Critical constraints: ✅ Auto-included
- Diagram information: ✅ Auto-included
- Works with ALL templates: ✅ Even minimal ones!

**You can focus on styling - the critical requirements are always handled!** 🎨✨

---

Run `python test-prompt-building.py` to see it in action!
