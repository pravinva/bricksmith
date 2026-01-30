# Usage Guide

Complete guide to using Nano Banana Pro for diagram generation and evaluation.

## Workflow Overview

1. **Create Diagram Spec** - Define your architecture in YAML
2. **Generate Diagram** - Run experiment with prompt template
3. **Review Output** - Check generated image
4. **Evaluate** - Score diagram quality
5. **Iterate** - Refine prompts and regenerate

## Creating Diagram Specifications

### Basic Structure

Create a YAML file in `examples/diagram_specs/`:

```yaml
name: "my-architecture"
description: "Brief description of the architecture"

components:
  - id: "unique-id"
    label: "Display Name"
    type: "service"  # service, storage, database, external
    logo_name: "databricks"  # Optional: reference to logo

connections:
  - from_id: "source-component-id"
    to_id: "target-component-id"
    label: "Connection Label"  # Optional
    style: "solid"  # solid, dashed, dotted

constraints:
  layout: "left-to-right"  # left-to-right, top-to-bottom, grid
  background: "white"
  label_style: "sentence-case"
  show_grid: false
  spacing: "comfortable"  # compact, comfortable, spacious
```

### Example: Simple Lakehouse

```yaml
name: "simple-lakehouse"
description: "Basic Databricks lakehouse architecture"

components:
  - id: "sources"
    label: "Data Sources"
    type: "external"

  - id: "databricks"
    label: "Databricks"
    type: "service"
    logo_name: "databricks"

  - id: "delta"
    label: "Delta Lake"
    type: "storage"
    logo_name: "delta-lake"

connections:
  - from_id: "sources"
    to_id: "databricks"
    label: "Ingest"

  - from_id: "databricks"
    to_id: "delta"
    label: "Store"

constraints:
  layout: "left-to-right"
  background: "white"
  spacing: "comfortable"
```

## Generating Diagrams

### Basic Generation

```bash
nano-banana generate \
    --diagram-spec examples/diagram_specs/example_basic.yaml \
    --template baseline
```

### With Run Name and Tags

```bash
nano-banana generate \
    --diagram-spec examples/diagram_specs/example_basic.yaml \
    --template baseline \
    --run-name "lakehouse-v1" \
    --tag "experiment=baseline" \
    --tag "version=1" \
    --tag "author=yourname"
```

### Using Different Templates

```bash
# Minimal template
nano-banana generate \
    --diagram-spec examples/diagram_specs/example_basic.yaml \
    --template minimal

# Detailed template
nano-banana generate \
    --diagram-spec examples/diagram_specs/example_complex.yaml \
    --template detailed
```

### Output

Generated images are saved to `outputs/output_<run-id>.png`

```bash
# View output
open outputs/output_abc12345.png  # macOS
xdg-open outputs/output_abc12345.png  # Linux
```

## Creating Prompt Templates

### Template Structure

Create `.txt` files in `examples/prompt_templates/`:

```
You are generating a clean architecture diagram.

{logo_section}

{diagram_section}

Additional instructions...
```

### Required Placeholders

- `{logo_section}` - Logo kit descriptions (auto-generated)
- `{diagram_section}` - Diagram spec details (auto-generated)

### Custom Variables

```
You are generating a {style} architecture diagram.

{logo_section}

{diagram_section}

Use {color_scheme} colors.
```

Use with:

```python
# In code (advanced usage)
prompt = builder.build_prompt(
    template,
    diagram_spec,
    logo_kit,
    variables={"style": "modern", "color_scheme": "professional"}
)
```

## Evaluation

### Interactive Evaluation

```bash
nano-banana evaluate <run-id>
```

You'll be prompted to score (0-5) for:

1. **Logo Fidelity** - Are logos reused exactly?
2. **Layout Clarity** - Is the flow clear?
3. **Text Legibility** - Is all text readable?
4. **Constraint Compliance** - Are requirements met?

### Scoring Guidelines

#### Logo Fidelity (0-5)

- **5**: All logos perfect, no alterations, no filenames
- **4**: Minor scaling issues
- **3**: Some logo issues
- **2**: Significant problems
- **1**: Logos barely recognizable
- **0**: Logos wrong or filenames visible

#### Layout Clarity (0-5)

- **5**: Crystal clear flow, perfect spacing
- **4**: Very clear with minor issues
- **3**: Adequate layout
- **2**: Somewhat confusing
- **1**: Poor layout
- **0**: Completely unclear

#### Text Legibility (0-5)

- **5**: All text perfect
- **4**: Minor formatting issues
- **3**: Mostly readable
- **2**: Some readability issues
- **1**: Significant problems
- **0**: Unreadable

#### Constraint Compliance (0-5)

- **5**: All constraints met perfectly
- **4**: Minor deviations
- **3**: Most constraints met
- **2**: Several violations
- **1**: Many issues
- **0**: Requirements ignored

### File-Based Evaluation

Create `evaluation.json`:

```json
{
  "logo_fidelity_score": 5,
  "layout_clarity_score": 4,
  "text_legibility_score": 5,
  "constraint_compliance_score": 4,
  "notes": "Excellent overall, minor spacing adjustment needed"
}
```

Use with:

```bash
nano-banana evaluate <run-id> --eval-file evaluation.json
```

## Viewing Results

### List Runs

```bash
# List recent runs
nano-banana list-runs

# Limit results
nano-banana list-runs --max-results 20

# Filter by score
nano-banana list-runs --filter "metrics.overall_score > 4.0"

# Filter by template
nano-banana list-runs --filter "params.prompt_template_id = 'baseline'"
```

### Show Run Details

```bash
nano-banana show-run <run-id>
```

Shows:
- Parameters (model, temperature, template, etc.)
- Metrics (scores, timing)
- Artifact locations

### MLflow UI

```bash
# Start MLflow UI
mlflow ui

# Open browser
open http://localhost:5000
```

In MLflow UI you can:
- Compare runs side-by-side
- View all parameters and metrics
- Download artifacts (images, prompts, configs)
- Create charts and visualizations

## Advanced Usage

### Custom Configuration

```bash
nano-banana --config my-config.yaml generate ...
```

### Environment Overrides

```bash
# Use different model
export NANO_BANANA_VERTEX__MODEL_ID="gemini-4-pro-image"

# Increase temperature for more variation
export NANO_BANANA_VERTEX__TEMPERATURE="0.8"

# Use remote MLflow
export NANO_BANANA_MLFLOW__TRACKING_URI="http://mlflow.example.com"

nano-banana generate ...
```

### Batch Generation

```bash
# Generate multiple variants
for template in baseline detailed minimal; do
  nano-banana generate \
    --diagram-spec examples/diagram_specs/example_basic.yaml \
    --template $template \
    --run-name "batch-${template}" \
    --tag "batch=1"
done
```

### Logo Validation

```bash
# Validate logo kit before generation
nano-banana validate-logos --logo-dir examples/logo_kit
```

Shows:
- Logo names and descriptions
- File sizes
- SHA256 hashes (for tracking)

## Best Practices

### 1. Use Descriptive Run Names

```bash
--run-name "lakehouse-baseline-v1"
--run-name "multicloud-detailed-2024-01"
```

### 2. Tag Experiments Consistently

```bash
--tag "experiment=baseline"
--tag "version=1"
--tag "date=2024-01-17"
--tag "author=yourname"
```

### 3. Evaluate Immediately

```bash
# Generate
nano-banana generate ...

# Note the run ID, then evaluate
nano-banana evaluate <run-id>
```

### 4. Compare Runs in MLflow

Use MLflow UI to compare:
- Different templates
- Different temperature settings
- Different diagram specs

### 5. Version Control Diagram Specs

```bash
git add examples/diagram_specs/my-diagram-v1.yaml
git commit -m "Add diagram spec v1"
```

### 6. Document Template Iterations

Create template variants:
- `baseline.txt`
- `baseline-v2.txt`
- `baseline-detailed.txt`

## Common Workflows

### Iteration Workflow

1. Generate initial diagram
2. Evaluate and identify issues
3. Modify prompt template
4. Regenerate with new template
5. Compare runs in MLflow
6. Repeat until satisfied

### Multi-Template Comparison

1. Create 3-5 template variants
2. Generate diagrams with each template
3. Use same run tags for grouping
4. Evaluate all variants
5. Compare in MLflow UI
6. Choose best performing template

### Parameter Tuning

1. Start with default temperature (0.4)
2. Generate baseline diagrams
3. Increase temperature for more variation
4. Decrease for more consistency
5. Compare outputs and scores

## Troubleshooting

### Generation Fails

**Check logs** in MLflow run artifacts

**Verify**:
- Authentication: `nano-banana check-auth`
- Logo kit: `nano-banana validate-logos --logo-dir examples/logo_kit`
- Diagram spec: Valid YAML syntax
- Template: Contains required placeholders

### Low Scores

**Logo Fidelity Issues**:
- Strengthen prompt constraints
- Add explicit "NO filenames" instruction
- Use detailed template

**Layout Issues**:
- Adjust diagram constraints
- Try different layout direction
- Modify spacing setting

**Text Issues**:
- Simplify component labels
- Request larger font in prompt
- Use detailed template

### Evaluation Questions

**What if filenames appear?**
- Score Logo Fidelity as 0
- Note in evaluation notes
- Modify prompt to emphasize "NO filenames"

**What if logos are altered?**
- Reduce Logo Fidelity score proportionally
- Note specific alterations
- Add stronger constraints to prompt

## Next Steps

- Experiment with different prompt templates
- Try various diagram specifications
- Compare temperature settings
- Review evaluation rubric
- Iterate on prompts based on scores

## Support

- See [Setup Guide](setup.md) for configuration help
- Review [README](../README.md) for quick reference
- Check [CLAUDE.md](../CLAUDE.md) for architecture details
