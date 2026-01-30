# Prompt Development Guide

## 🎯 Goal
Systematically develop and refine prompts to produce high-quality, accurate architecture diagrams with MCP-enriched technical context.

## 🧪 The Prompt Development System

### Components

1. **MCP Enricher** (`src/nano_banana/mcp_enricher.py`)
   - Queries Databricks documentation via MCP
   - Adds accurate technical context to diagrams
   - Ensures consistent terminology

2. **Prompt Development Lab** (`src/nano_banana/prompt_dev.py`)
   - Run multiple prompt variants
   - Compare results side-by-side
   - Track experiments in MLflow

3. **Ready-to-Use Scripts**
   - `demo_mcp_enrichment.py` - See MCP enrichment in action
   - `develop_prompts.py` - Run systematic experiments

## 🚀 Quick Start

### Step 1: Demo MCP Enrichment

```bash
uv run python demo_mcp_enrichment.py
```

**What it does:**
- Shows which components can be enriched
- Fetches context from Databricks docs
- Displays the enriched prompt section

### Step 2: Run Prompt Comparison

```bash
uv run python develop_prompts.py
```

**What it generates:**
- 4 diagram variants:
  1. **v1_baseline** - Original template
  2. **v2_baseline_mcp** - Original + MCP enrichment
  3. **v3_presentation** - Enhanced presentation template
  4. **v4_presentation_mcp** - Enhanced + MCP enrichment

**Outputs:**
- Diagrams: `outputs/prompt_dev/`
- Prompts: `outputs/prompt_dev/*_prompt.txt`
- MLflow traces: Run `mlflow ui --port 5000`

### Step 3: Review & Iterate

1. **Visual Comparison**
   ```bash
   open outputs/prompt_dev/
   ```
   Compare diagrams side-by-side

2. **Analyze Prompts**
   ```bash
   cat outputs/prompt_dev/v4_presentation_mcp_prompt.txt
   ```
   See what worked in each variant

3. **Check MLflow**
   ```bash
   mlflow ui --port 5000
   ```
   View traces, parameters, metrics

4. **Iterate**
   - Identify best elements from each variant
   - Create new template combining best practices
   - Run another comparison

## 📊 Comparison Criteria

When comparing variants, evaluate:

### ✅ Technical Accuracy
- [ ] Correct Databricks terminology
- [ ] Accurate component descriptions
- [ ] Proper logo usage

### 🎨 Visual Quality
- [ ] Professional presentation style
- [ ] Clear hierarchy
- [ ] Good color contrast
- [ ] Readable text

### ✍️ Spelling & Grammar
- [ ] No spelling errors
- [ ] Consistent capitalization
- [ ] Proper product names

### 📐 Layout
- [ ] Well-balanced composition
- [ ] Logos prominently displayed
- [ ] Clear data flow
- [ ] 16:9 aspect ratio optimized

## 🔧 Advanced Usage

### Create Custom Experiments

```python
from src.nano_banana.prompt_dev import PromptDevelopmentLab, PromptExperiment

lab = PromptDevelopmentLab()

# Define custom experiment
exp = PromptExperiment(
    template_id="agl_concentric_presentation",
    variant_name="v5_custom_colors",
    use_mcp_enrichment=True,
    modifications={
        "color_scheme": "vibrant",
        "logo_emphasis": "high"
    }
)

# Run single experiment
result = lab.run_experiment(
    diagram_spec_path=Path("prompts/diagram_specs/agl_data_economy.yaml"),
    experiment=exp,
    aspect_ratio="16:9",
    image_size="2K"
)
```

### Batch Testing Multiple Templates

```python
templates = ["agl_concentric", "detailed", "minimal"]
variants = []

for template in templates:
    variants.extend([
        PromptExperiment(
            template_id=template,
            variant_name=f"{template}_baseline",
            use_mcp_enrichment=False,
        ),
        PromptExperiment(
            template_id=template,
            variant_name=f"{template}_mcp",
            use_mcp_enrichment=True,
        ),
    ])

results = lab.run_comparison(diagram_spec, variants)
```

## 🎓 Best Practices

### 1. Start with MCP Enrichment
Always try MCP enrichment first - it provides:
- Accurate technical descriptions
- Consistent terminology
- Architectural context

### 2. Iterate in Small Steps
Don't change everything at once:
- Baseline → +MCP enrichment
- +MCP → +Visual improvements
- +Visual → +Spelling emphasis

### 3. Use MLflow for Tracking
Every experiment is tracked:
- Compare parameters
- Review traces
- Track improvements over time

### 4. Document What Works
When you find a good variant:
- Save the prompt template
- Note successful patterns
- Create reusable templates

### 5. A/B Test Critical Changes
For important diagrams:
- Generate 2-3 variants
- Compare side-by-side
- Choose the best one

## 📝 Template Development Workflow

### Phase 1: Discovery (2-3 variants)
- Baseline template
- +MCP enrichment
- +Visual improvements

**Goal:** Identify what works

### Phase 2: Refinement (3-5 variants)
- Test color schemes
- Adjust logo prominence
- Refine layout instructions
- Add spelling checks

**Goal:** Optimize the best approach

### Phase 3: Validation (1-2 variants)
- Test on different diagram specs
- Ensure consistency
- Verify technical accuracy

**Goal:** Confirm template works broadly

### Phase 4: Production
- Finalize template
- Document best practices
- Add to template library

## 🎯 Example Workflow: AGL Data Economy

```bash
# 1. Demo MCP
uv run python demo_mcp_enrichment.py

# 2. Generate variants
uv run python develop_prompts.py

# 3. Review outputs
open outputs/prompt_dev/

# 4. Compare in MLflow
mlflow ui --port 5000

# 5. Select winner
# v4_presentation_mcp looks best!

# 6. Use winner for production
uv run nano-banana generate \
  --diagram-spec prompts/diagram_specs/agl_data_economy.yaml \
  --template agl_concentric_presentation \
  --run-name "agl-final"
```

## 🐛 Troubleshooting

### MCP Not Available
If MCP enrichment fails:
- System works without it
- Manually add technical context to prompts
- Use presentation templates for better results

### Spelling Errors Persist
Add explicit checks to prompt:
```
CRITICAL: Verify spelling of ALL terms:
- "Databricks" (not "Databrick")
- "Kaluza" (not variations)
- "Unity Catalog" (not "Catalogue")
```

### Logos Not Visible
Enhance logo descriptions:
```python
# In logos.py
DEFAULT_LOGO_DESCRIPTIONS = {
    "kaluza": "three BLACK hexagons in triangular pattern (IMPORTANT: use exactly as uploaded)",
}
```

### Layout Issues
Adjust template:
- Specify exact positioning
- Add sizing constraints
- Use reference diagrams

## 📚 Resources

- **Template Directory**: `prompts/prompt_templates/`
- **Diagram Specs**: `prompts/diagram_specs/`
- **MCP Docs**: See databricks-docs MCP server
- **MLflow UI**: `http://localhost:5000`

## 💡 Tips for Success

1. **Be Specific** - Vague prompts = inconsistent results
2. **Use MCP** - Accurate docs = better diagrams
3. **Iterate Systematically** - Track what works
4. **Compare Side-by-Side** - Visual review beats metrics
5. **Document Learnings** - Build institutional knowledge
