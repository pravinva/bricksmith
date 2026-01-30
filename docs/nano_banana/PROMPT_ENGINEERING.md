# Prompt Engineering Guide

This guide explains how Nano Banana Pro builds prompts and ensures logo constraints are always included.

## 🎯 Critical Feature: Automatic Logo Constraint Injection

**ALL prompts automatically include logo constraints**, regardless of your template!

The system **guarantees** these constraints appear in every prompt sent to the AI:

```
CRITICAL LOGO REQUIREMENTS (MANDATORY):
- Reuse uploaded logos EXACTLY as provided
- Scale all logos uniformly
- NO filenames or file labels may appear in the output
```

### How It Works

1. **Template has placeholders** (recommended):
   ```
   {logo_section}
   {diagram_section}
   ```
   → Logo section and constraints inserted via placeholders

2. **Template missing placeholders** (still works):
   → System automatically **prepends** logo section and constraints

3. **Double-check validation**:
   → System verifies all critical constraints are present
   → If missing, force-injects them at the top

**Result**: Logo constraints are **GUARANTEED** in every prompt, no matter what!

## 📝 Prompt Template Structure

### Recommended Template Format

```
You are generating a [type] architecture diagram.

{logo_section}

[Your custom instructions here...]

{diagram_section}

[More custom instructions...]
```

### Minimal Template (Also Works!)

Even if you write a simple template like this:

```
Generate a clean diagram.

{diagram_section}
```

The system automatically adds:
- Logo kit descriptions
- All logo constraints
- Critical "NO filenames" requirement

## 🏗️ How Prompts Are Built

### Step 1: Load Template

```python
template = prompt_builder.load_template("baseline")
```

### Step 2: Build Logo Section

```python
logo_section = """
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
"""
```

### Step 3: Build Diagram Section

```python
diagram_section = """
Diagram: my-architecture
Description: Multi-cloud lakehouse platform

Components:
- databricks: Databricks Workspace (type: service) [use databricks logo]
- delta-lake: Delta Lake (type: storage) [use delta-lake logo]

Connections:
- databricks → delta-lake "Store data" (solid)

Layout Constraints:
- Layout: left-to-right
- Background: white
- Spacing: comfortable
"""
```

### Step 4: Substitute Variables

Replace `{logo_section}` and `{diagram_section}` in template

### Step 5: Validate & Force-Inject (if needed)

```python
# Check if constraints are present
if not all_constraints_present:
    # Force-inject at top of prompt
    prompt = constraint_block + prompt
```

### Step 6: Final Prompt

Complete prompt with ALL requirements guaranteed!

## ✅ Validation

### Validate a Template

```python
from nano_banana.prompts import PromptBuilder

builder = PromptBuilder()
template = builder.load_template("baseline")

# Check for recommended placeholders
missing = builder.validate_template(template)
if missing:
    print(f"Template missing recommended placeholders: {missing}")
    print("(Don't worry - constraints are auto-injected anyway!)")
```

### Validate Final Prompt

```python
# After building prompt
validation = builder.validate_final_prompt(final_prompt)

# Check results
assert validation["has_reuse_constraint"]
assert validation["has_scale_constraint"]
assert validation["has_no_filename_constraint"]
```

## 📋 Logo Descriptions Reference

These descriptions are automatically included in ALL prompts:

| Logo | Description in Prompt |
|------|----------------------|
| databricks | "red icon" |
| delta-lake | "teal icon" |
| uc | "pink squares, yellow triangles, hexagon in middle" |
| kaluza | "three hexagons stacked" |
| agl | "AGL Energy logo" |
| aws | "grey text with orange smile" |
| azure | "blue symbol" |

## 🎨 Creating Custom Templates

### Option 1: Use Placeholders (Recommended)

Create `prompts/prompt_templates/my_template.txt`:

```
You are generating a modern, professional architecture diagram.

{logo_section}

Style Guidelines:
- Use clean, modern design
- High contrast colors
- Professional appearance

{diagram_section}

Additional Requirements:
- Add subtle shadows for depth
- Use rounded corners
- Maintain visual hierarchy
```

### Option 2: Skip Placeholders (Still Works!)

Create `prompts/prompt_templates/simple.txt`:

```
Create a simple, clean diagram.

Style: Minimal and professional.
```

Even without `{logo_section}`, the system will automatically add:
- All logo descriptions
- Critical constraints
- Diagram information

## 🔍 Testing Your Prompts

### View Generated Prompt

After generation, check the logged prompt artifact:

```bash
# Generate diagram
nano-banana generate --diagram-spec spec.yaml --template baseline

# View logged prompt
cat mlruns/<experiment-id>/<run-id>/artifacts/prompts/prompt.txt
```

Or in Databricks MLflow:
1. Navigate to run
2. Click **Artifacts** tab
3. Open `prompts/prompt.txt`

### Manual Verification Checklist

Check your final prompt includes:

- ✅ Logo kit list with descriptions
- ✅ "Reuse uploaded logos EXACTLY"
- ✅ "Scale all logos uniformly"
- ✅ "NO filenames"
- ✅ Diagram components
- ✅ Connections
- ✅ Constraints

## 🚨 Common Template Patterns

### Pattern 1: Detailed Specifications

```
You are generating a highly detailed architecture diagram.

{logo_section}

LAYOUT REQUIREMENTS:
- Use grid-based layout
- Minimum 20px spacing between components
- Left-to-right data flow

VISUAL STYLE:
- Rounded rectangles with shadows
- Professional color palette
- High contrast for readability

TEXT FORMATTING:
- Sans-serif fonts
- Component labels: 16pt bold
- Connection labels: 12pt regular
- Sentence case for all labels

{diagram_section}

QUALITY STANDARDS:
- No pixelation
- WCAG AA color contrast
- Executive-ready presentation quality
```

### Pattern 2: Minimal Style

```
Generate a minimal, clean architecture diagram.

{logo_section}

Style: Simple, clean, minimal. White background. Clear labels.

{diagram_section}
```

### Pattern 3: Specific Use Case

```
You are creating a technical architecture diagram for a data engineering team.

{logo_section}

Focus on:
- Clear data flow paths
- Technology stack visibility
- Integration points highlighted

{diagram_section}

Audience: Technical data engineers
```

## 🎯 Best Practices

### ✅ DO:

1. **Include placeholders** for best control:
   ```
   {logo_section}
   {diagram_section}
   ```

2. **Add context** about diagram purpose:
   ```
   "You are creating a diagram for executive presentation..."
   ```

3. **Specify style** clearly:
   ```
   "Use modern, professional design with high contrast..."
   ```

4. **Test variations** with different templates:
   ```bash
   nano-banana generate --template baseline
   nano-banana generate --template detailed
   nano-banana generate --template minimal
   ```

### ❌ DON'T:

1. **Don't worry about forgetting constraints** - they're auto-injected!

2. **Don't duplicate logo instructions** - the system handles this:
   ```
   # DON'T DO THIS (redundant):
   {logo_section}
   Use logos exactly as provided...  # ← Already in {logo_section}!
   ```

3. **Don't reference filenames** in templates:
   ```
   # WRONG:
   Use databricks-logo.jpg for Databricks  # ❌

   # CORRECT:
   {logo_section}  # ✅ Descriptions, not filenames
   ```

## 🧪 Testing Logo Constraints

### Test 1: Verify Auto-Injection

Create a template without `{logo_section}`:

```
# prompts/prompt_templates/test_no_placeholder.txt
Create a diagram.

{diagram_section}
```

Generate and check prompt artifact - should still have logo constraints!

### Test 2: Custom Template

Create your own template and verify:

```bash
nano-banana generate \
    --diagram-spec prompts/diagram_specs/example_basic.yaml \
    --template your_template

# Check prompt artifact includes all constraints
```

### Test 3: Evaluation

After generation, evaluate logo fidelity:

```bash
nano-banana evaluate <run-id>
# Score "Logo Fidelity" based on:
# - Logos reused exactly?
# - Scaled uniformly?
# - No filenames visible?
```

## 📊 Prompt Variables

You can use custom variables in templates:

### Template with Variables

```
You are generating a {style} architecture diagram for {audience}.

{logo_section}

Color scheme: {color_scheme}
Complexity level: {complexity}

{diagram_section}
```

### Using Variables (Advanced)

```python
# In code (custom integration)
from nano_banana.prompts import PromptBuilder

builder = PromptBuilder()
template = builder.load_template("custom")

prompt = builder.build_prompt(
    template,
    diagram_spec,
    logo_kit,
    variables={
        "style": "modern",
        "audience": "executives",
        "color_scheme": "professional blues",
        "complexity": "medium"
    }
)
```

## 🎓 Advanced: Programmatic Prompt Building

For custom workflows:

```python
from nano_banana.prompts import PromptBuilder
from nano_banana.models import DiagramSpec
from nano_banana.logos import LogoKitHandler

# Initialize
builder = PromptBuilder()
logo_handler = LogoKitHandler(config.logo_kit)

# Load components
template = builder.load_template("baseline")
diagram_spec = DiagramSpec.from_yaml("spec.yaml")
logo_kit = logo_handler.load_logo_kit()

# Build prompt
final_prompt = builder.build_prompt(template, diagram_spec, logo_kit)

# Validate
validation = builder.validate_final_prompt(final_prompt)
assert all(validation.values()), f"Validation failed: {validation}"

# Use prompt with Vertex AI
# ...
```

## 📚 Related Documentation

- **LOGO_SETUP.md** - Logo configuration guide
- **LOGO_QUICK_START.md** - Quick logo setup
- **docs/usage.md** - Usage guide with examples
- **prompts/prompt_templates/** - Template examples

---

**Key Takeaway**: Logo constraints are **automatically guaranteed** in ALL prompts. You can focus on styling and layout - the critical logo requirements are always handled! 🎨✨
