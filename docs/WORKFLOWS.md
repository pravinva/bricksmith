# Common Workflows

This guide covers common workflows for using nano_banana effectively.

## Quick Start: Generate Your First Diagram

```bash
# 1. Ensure authentication is set up
source .env

# 2. Generate from a YAML spec
uv run nano-banana generate \
    --diagram-spec prompts/diagram_specs/example_basic.yaml \
    --template baseline \
    --run-name "my-first-diagram"

# 3. View the output
open outputs/output_*.png
```

## Workflow 1: Template-Based Generation

Best for: Standardized diagrams with consistent styling

```bash
# Use an existing diagram spec and template
uv run nano-banana generate \
    --diagram-spec prompts/diagram_specs/coles-future-unity-catalog.yaml \
    --template baseline \
    --run-name "coles-unity-catalog"
```

**When to use:**
- Creating diagrams with predefined components
- Maintaining consistent style across multiple diagrams
- Leveraging existing templates and branding

## Workflow 2: Raw Prompt Generation

Best for: Custom, one-off diagrams with specific requirements

```bash
# Use a custom prompt file with specific logos
uv run nano-banana generate-raw \
    --prompt-file prompts/my_custom_prompt.txt \
    --logo logos/default/databricks-full.png \
    --logo logos/default/unity-catalog.png \
    --logo logos/default/delta.png \
    --run-name "custom-diagram"
```

**When to use:**
- Highly customized diagrams
- Experimenting with new prompt structures
- Fine-grained control over output

## Workflow 3: Scenario-to-Diagram

Best for: Rapidly prototyping multiple diagram variations

```bash
# Generate multiple variations from a scenario description
uv run nano-banana scenario-to-diagram \
    --scenario-file prompts/my_scenario.txt \
    --variations 3 \
    --run-name "scenario-exploration"
```

**When to use:**
- Exploring different visual representations
- A/B testing diagram approaches
- Generating options for stakeholder review

## Workflow 4: Iterative Refinement

Best for: Perfecting a diagram through multiple iterations

```bash
# 1. Generate initial version
uv run nano-banana generate --diagram-spec spec.yaml --template baseline --run-name "v1"

# 2. Evaluate the output
uv run nano-banana evaluate <run-id>

# 3. Refine the prompt based on feedback
# Edit your prompt or spec file

# 4. Generate improved version
uv run nano-banana generate --diagram-spec spec.yaml --template detailed --run-name "v2"

# 5. Compare runs
uv run nano-banana list-runs
```

**When to use:**
- Creating presentation-quality diagrams
- Responding to stakeholder feedback
- Optimizing for specific criteria

## Workflow 5: Multi-Logo Kit Management

Best for: Projects using different logo sets

```bash
# Use logos from a specific kit
uv run nano-banana generate-raw \
    --prompt-file prompts/my_prompt.txt \
    --logo logos/agl/AGL_Energy_logo.png \
    --logo logos/agl/kaluza_logo_black.png \
    --logo logos/default/databricks-full.png \
    --run-name "agl-architecture"
```

**When to use:**
- Customer-specific diagrams
- Multi-cloud architectures
- Partner integration diagrams

## Workflow 6: Prompt Analysis and Optimization

Best for: Understanding what works best

```bash
# Analyze successful prompts
uv run nano-banana analyze-prompts --min-score 4.5

# Get improvement suggestions
uv run nano-banana suggest-improvements --template baseline

# View template performance stats
uv run nano-banana template-stats
```

**When to use:**
- Building a library of effective prompts
- Training team members
- Establishing best practices

## Workflow 7: Batch Generation

Best for: Creating multiple related diagrams

```bash
# Generate a suite of diagrams
for spec in prompts/diagram_specs/coles-*.yaml; do
    name=$(basename "$spec" .yaml)
    uv run nano-banana generate \
        --diagram-spec "$spec" \
        --template baseline \
        --run-name "$name"
done
```

**When to use:**
- Presentation decks
- Documentation suites
- Before/after comparisons

## Workflow 8: MLflow Tracking and Comparison

Best for: Experiment tracking and reproducibility

```bash
# Generate with detailed tracking
uv run nano-banana generate \
    --diagram-spec spec.yaml \
    --template baseline \
    --run-name "experiment-1" \
    --tag iteration=1 \
    --tag customer=acme

# List and filter runs
uv run nano-banana list-runs --filter "metrics.overall_score > 4.0"

# View specific run
uv run nano-banana show-run <run-id>
```

**When to use:**
- A/B testing approaches
- Tracking experiments
- Demonstrating progress to stakeholders

## Tips and Best Practices

### Logo Selection
- Use `databricks-full.png` for primary Databricks branding
- Use `unity-catalog-solo.png` for Unity Catalog-specific diagrams
- Maintain consistent logo sizing within a diagram

### Prompt Engineering
- Start with minimal branding for cleaner outputs
- Be explicit about layout requirements
- Use sentence case for labels
- Specify exact colors when brand consistency matters

### Output Organization
- Use descriptive run names: `customer-usecase-version`
- Tag runs with metadata for easy filtering
- Keep outputs organized by date (automatic)
- Document successful prompts for reuse

### Evaluation
- Score consistently using the same rubric
- Focus on logo fidelity first
- Evaluate layout clarity second
- Check constraint compliance last

### Iteration Strategy
1. Start with a template-based generation
2. Evaluate and identify issues
3. Switch to raw generation for fine-tuning
4. Document successful approaches
5. Create reusable templates from winners

## Troubleshooting

### Model Overload (503 errors)
- Wait 30-60 seconds between requests
- Use lower temperature settings
- Retry failed requests

### Poor Logo Fidelity
- Ensure logos are in the specified kit directory
- Verify logo descriptions in `logos.py`
- Check that prompt includes logo constraints

### Layout Issues
- Be more specific about layout requirements
- Use visual examples in prompts
- Try different branding styles (minimal vs. detailed)

### MLflow Connection Issues
- Verify Databricks authentication: `uv run nano-banana check-auth`
- Refresh token if expired
- Check workspace URL in `.env`
