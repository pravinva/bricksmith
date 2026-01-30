# 🍌 Nano Banana Pro

**Reproducible prompt engineering for architecture diagrams that actually look professional.**

Generate client-ready architecture diagrams using AI while maintaining perfect logo fidelity, tracking every experiment, and treating prompt engineering as a scientific discipline.

---

## The Problem

You need to create architecture diagrams for a customer demo. You have:
- A clear mental picture of the architecture
- Logos for Databricks, AWS, Azure, Delta Lake, Unity Catalog
- An LLM that can generate images... but it keeps:
  - Writing logo filenames on the diagrams ("databricks-logo.jpg")
  - Distorting or recreating logos instead of reusing them
  - Making each diagram look completely different with the same prompt
  - Leaving no trace of what prompt produced what result

**Nano Banana Pro solves all of this.**

---

## What Makes This Cool

### 1. **Logo Description Abstraction**

The AI never sees filenames. Instead:

```
databricks-logo.jpg  →  "red icon with white text"
delta-lake-logo.jpg  →  "teal triangular icon"
```

This prevents filename leakage while maintaining perfect logo reuse. The system automatically enforces this constraint in **every single prompt** - even if your template forgets to include it.

### 2. **Prompt Engineering as Science**

Every diagram generation is an MLflow experiment with:
- 📊 Full parameter tracking (temperature, model, template)
- 🎨 Artifact logging (prompt, diagram, logo kit)
- ⭐ Manual evaluation rubric (0-5 scale across 4 dimensions)
- 🔍 Cross-run analysis to find winning patterns

Compare templates, measure improvements, and actually know what works.

### 3. **YAML → Diagram Workflow**

Declare your architecture as data:

```yaml
name: "databricks-lakehouse"

components:
  - id: "databricks"
    label: "Databricks Workspace"
    logo_name: "databricks"

connections:
  - from_id: "databricks"
    to_id: "delta-lake"
    label: "Write"
    style: "solid"

constraints:
  layout: "left-to-right"
  background: "white"
```

No more pixel-pushing in draw.io. Your architecture is now version-controlled and reproducible.

### 4. **Template-Driven Experimentation**

Create reusable prompt templates with variable substitution:

```
Generate a clean architecture diagram for {customer_name}.

{logo_section}
{diagram_section}

Style: Modern, professional, {layout_style}.
```

Test variations systematically, measure results, and build a library of proven templates.

### 5. **Visual Prompt Refinement** ✨ NEW

Use diagram images to improve your prompts:

```bash
# Generate a diagram
nano-banana generate --diagram-spec spec.yaml --template baseline

# Analyze it and get specific improvements
nano-banana refine-prompt \
    --run-id abc123 \
    --feedback "logos too small, need more spacing"

# Get concrete refinements like:
# "Add: Logos should be at least 80px tall"
# "Add: Ensure 40px padding around each logo"
```

The system uses Gemini's vision to:
- **Analyze** what worked and what didn't visually
- **Generate** concrete, actionable prompt improvements
- **Compare** good vs bad diagrams to extract patterns
- **Iterate** systematically toward perfect diagrams

No more guessing what to change—let AI tell you exactly what to fix.

### 6. **Scenario to Diagram Generation** ✨ NEW

Don't know how to structure your diagram spec? Just describe what you want:

```bash
# Describe your architecture in plain English
nano-banana generate-from-scenario \
    --scenario "Build a lakehouse on AWS with Databricks processing data from S3 to Redshift"

# AI generates the YAML spec AND the diagram
# ✓ Identifies components (Databricks, S3, Redshift)
# ✓ Maps data flow connections
# ✓ Matches available logos automatically
# ✓ Creates professional diagram immediately
```

Perfect for:
- **Quick prototyping** - Test architecture ideas in seconds
- **Learning** - See how scenarios map to diagram specs
- **Client demos** - Generate diagrams from meeting notes
- **Exploration** - Try different architectures without manual YAML

---

## Quick Start

### Installation

```bash
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Setup environment
uv venv && source .venv/bin/activate
uv pip install -e .
```

### Get Your API Keys

#### 1. Google AI API Key (Required)

Get your free API key from Google AI Studio:

1. **Go to Google AI Studio**: https://aistudio.google.com/app/apikey
2. **Sign in** with your Google account
3. **Click "Get API Key"** or "Create API Key"
4. **Select a project** (or create a new one)
5. **Copy the API key** (starts with `AIza...`)

#### 2. Databricks Credentials (Required for MLflow)

Get your Databricks workspace credentials:

1. **Go to your Databricks workspace**: https://your-workspace.cloud.databricks.com
2. **Click your profile** (top right) → **Settings**
3. **Go to "Developer"** → **Access tokens**
4. **Click "Manage"** → **Generate new token**
5. **Copy the token** (starts with `dapi...`)
6. **Note your workspace URL** and **username/email**

#### 3. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use your preferred editor
```

Add your credentials to `.env`:
```bash
# Google AI API Key (from step 1)
GEMINI_API_KEY=AIza...your-key-here...

# Databricks MLflow (from step 2)
DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
DATABRICKS_TOKEN=dapi...your-token-here...
DATABRICKS_USER=your.email@company.com

# GCP Project (optional, if using Vertex AI directly)
GCP_PROJECT_ID=your-project-id
```

**Load the environment:**
```bash
source .env
```

**Verify setup:**
```bash
nano-banana check-auth
# Should show: ✓ Google AI API key configured
#              ✓ Databricks credentials configured
```

**Need help?** See the [complete authentication guide](docs/nano_banana/AUTHENTICATION.md) for detailed instructions, troubleshooting, and security best practices.

### Generate Your First Diagram

```bash
# Verify everything is configured
nano-banana verify-setup

# Generate a diagram
nano-banana generate \
    --diagram-spec prompts/diagram_specs/example_basic.yaml \
    --template baseline \
    --run-name "my-first-diagram"

# Output saved to: outputs/diagram_<run-id>.png
```

### Evaluate and Iterate

```bash
# Score the diagram (interactive CLI prompts)
nano-banana evaluate <run-id>

# View all runs with scores
nano-banana list-runs --filter "metrics.overall_score > 4.0"

# Analyze what makes prompts succeed
nano-banana analyze-prompts --min-score 4.5
nano-banana template-stats
```

Your experiment is now in Databricks MLflow:
```
Navigate to: ML → Experiments → /Users/your.email/vertexai-nanobanana-arch-diagrams
```

---

## The Evaluation Rubric

Every diagram gets scored 0-5 on:

| Dimension | What It Measures |
|-----------|------------------|
| **Logo Fidelity** | Logos reused exactly with no distortion or filename leakage |
| **Layout Clarity** | Clear flow, logical grouping, comfortable spacing |
| **Text Legibility** | All labels readable and professionally formatted |
| **Constraint Compliance** | Follows all requirements from the diagram spec |

**Critical Rule:** Any filename visible in the output = automatic penalty.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  nano-banana generate --diagram-spec spec.yaml             │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  Runner Pipeline (runner.py)                                │
│                                                              │
│  1. Load config (configs/default.yaml + env vars)           │
│  2. Validate logo kit (SHA256 tracking)                     │
│  3. Build prompt with variable substitution                 │
│  4. Start MLflow run                                        │
│  5. Generate via Gemini API                                 │
│  6. Log parameters + artifacts + metrics                    │
│  7. Save diagram to outputs/                                │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  Databricks MLflow (mlflow_tracker.py)                      │
│                                                              │
│  • Parameters: template, model, temperature, seed           │
│  • Artifacts: prompt.txt, diagram.png, logo_kit.json        │
│  • Metrics: overall_score, logo_fidelity, layout_clarity    │
└─────────────────────────────────────────────────────────────┘
```

**Key Design Principles:**

- **MLflow-First:** Every generation is tracked, no exceptions
- **Constraint Injection:** Logo rules automatically prepended to prompts
- **Immutable Logos:** SHA256 hashing ensures logo kit consistency
- **Template Composability:** Mix and match reusable prompt sections

---

## Example Workflow: Client Demo Prep

```bash
# 1. Create diagram spec for customer architecture
cat > prompts/diagram_specs/acme-corp.yaml <<EOF
name: "acme-lakehouse"
description: "ACME Corp's Databricks lakehouse on AWS"
components:
  - id: "s3"
    label: "S3 Data Lake"
    logo_name: "aws"
  - id: "databricks"
    label: "Databricks"
    logo_name: "databricks"
  - id: "delta"
    label: "Delta Lake"
    logo_name: "delta-lake"
connections:
  - from_id: "s3"
    to_id: "databricks"
    label: "Ingest"
EOF

# 2. Generate with different prompt templates
nano-banana generate --diagram-spec acme-corp.yaml --template baseline
nano-banana generate --diagram-spec acme-corp.yaml --template detailed
nano-banana generate --diagram-spec acme-corp.yaml --template minimal

# 3. Evaluate each version
nano-banana list-runs --max-results 3
nano-banana evaluate <run-id-1>
nano-banana evaluate <run-id-2>
nano-banana evaluate <run-id-3>

# 4. Pick the winner
nano-banana show-run <winning-run-id>
cp outputs/diagram_<winning-run-id>.png ~/Desktop/acme-architecture.png

# 5. Learn what worked
nano-banana template-stats
nano-banana suggest-improvements --template baseline
```

Now you have:
- ✅ A professional diagram ready for the customer
- ✅ Full traceability of what prompt generated it
- ✅ Data-driven insights on what templates perform best
- ✅ A reproducible process for next time

---

## Under the Hood

### Logo Kit Management

```python
# logos.py automatically maps logo names to descriptions
logo_map = {
    "databricks": "red icon with white text",
    "delta-lake": "teal triangular icon",
    "uc": "pink squares, yellow triangles, hexagon icon",
    "aws": "grey text with orange smile",
    "azure": "blue symbol"
}
```

Every logo is SHA256-hashed to detect changes between runs.

### Prompt Building

```python
# prompts.py guarantees logo constraints in EVERY prompt
def build_prompt(template, diagram_spec, logo_kit):
    prompt = template.template

    # Substitute variables
    prompt = prompt.format(
        logo_section=build_logo_section(logo_kit),
        diagram_section=build_diagram_section(diagram_spec)
    )

    # CRITICAL: Ensure logo constraints are present
    if "DO NOT include filenames" not in prompt:
        prompt = LOGO_CONSTRAINTS + "\n\n" + prompt

    return prompt
```

This automatic enforcement means you can't accidentally create a bad prompt.

### MLflow Tracking

```python
# Every generation logs to Databricks MLflow
with mlflow.start_run(run_name=run_name):
    mlflow.log_params({
        "template_id": template_id,
        "model": "gemini-3-pro-image-preview",
        "temperature": 0.4,
        "diagram_name": spec.name
    })

    diagram = generate_via_gemini(prompt, logos)

    mlflow.log_artifact(prompt, "prompt.txt")
    mlflow.log_artifact(diagram, "diagram.png")
    mlflow.log_artifact(logo_kit, "logo_kit.json")
```

View the full experiment lineage in the Databricks UI.

---

## Configuration

The system uses layered configuration with clear precedence:

```
1. Environment variables (highest)
   └─ NANO_BANANA_VERTEX__MODEL_ID="gemini-3-pro-image-preview"

2. YAML config files
   └─ configs/default.yaml, configs/databricks.yaml

3. Code defaults (lowest)
   └─ Built-in fallbacks
```

Key settings:

```yaml
# configs/default.yaml
vertex:
  model_id: "gemini-3-pro-image-preview"
  temperature: 0.4
  top_p: 0.95
  seed: 42

mlflow:
  tracking_uri: "databricks"
  experiment_name: "/Users/${DATABRICKS_USER}/vertexai-nanobanana-arch-diagrams"

logo_kit:
  logo_dir: "./logos/default"  # or ./logos/aws, ./logos/azure, etc.
  max_logo_size_mb: 5.0
```

---

## CLI Reference

### Generation
```bash
nano-banana generate \
    --diagram-spec path/to/spec.yaml \
    --template baseline \
    --run-name "optional-name" \
    --tag key=value
```

### Evaluation
```bash
nano-banana evaluate <run-id>        # Interactive evaluation
nano-banana list-runs                # View all experiments
nano-banana show-run <run-id>        # Detailed run info
```

### Analysis
```bash
nano-banana analyze-prompts --min-score 4.5    # Find top performers
nano-banana suggest-improvements --template baseline
nano-banana template-stats          # Compare template performance
nano-banana dimension-stats         # Analyze rubric dimensions
```

### Refinement ✨ NEW
```bash
# Analyze diagram and suggest prompt improvements
nano-banana refine-prompt \
    --run-id abc123 \
    --feedback "logos too small" \
    --output-template improved.txt

# Compare two diagrams to extract what makes one better
nano-banana compare-diagrams --good-run abc123 --bad-run def456

# Analyze any image (not just MLflow runs)
nano-banana refine-prompt \
    --reference-image path/to/diagram.png \
    --original-prompt path/to/prompt.txt
```

### Setup
```bash
nano-banana verify-setup            # Check configuration
nano-banana check-auth              # Verify credentials
nano-banana validate-logos          # Check logo kit
```

---

## Development

```bash
# Install with dev dependencies
uv pip install -e ".[dev]"

# Run tests
uv run pytest
uv run pytest tests/test_prompts.py::test_logo_constraint_injection

# Code quality
uv run black src/ tests/
uv run mypy src/
uv run pytest --cov
```

---

## Why "Nano Banana"?

Because generating architecture diagrams should be as easy as grabbing a snack. 🍌

Also, it's a nod to the iterative, incremental approach: start small (nano), iterate quickly (banana-fast), and build up to production-quality diagrams through systematic experimentation.

---

## Requirements

- **Python 3.11+**
- **uv package manager**
- **Google AI API key** (for Gemini)
- **Databricks workspace** (for MLflow tracking)
- **Logo files** in `logos/default/` (or other logo kit directories)

---

## Documentation

- **[docs/nano_banana/AUTHENTICATION.md](docs/nano_banana/AUTHENTICATION.md)** - Complete authentication setup guide
- **[docs/nano_banana/LOGO_SETUP.md](docs/nano_banana/LOGO_SETUP.md)** - Detailed logo configuration
- **[docs/nano_banana/PROMPT_REFINEMENT.md](docs/nano_banana/PROMPT_REFINEMENT.md)** - Visual prompt refinement guide ✨ NEW
- **[docs/nano_banana/SCENARIO_TO_DIAGRAM.md](docs/nano_banana/SCENARIO_TO_DIAGRAM.md)** - Generate diagrams from scenarios ✨ NEW
- **[CLAUDE.md](CLAUDE.md)** - Guide for Claude Code instances working on this repo
- **[.env.example](.env.example)** - Environment variable template
- **[prompts/diagram_specs/](prompts/diagram_specs/)** - Diagram specifications
- **[prompts/prompt_templates/](prompts/prompt_templates/)** - Prompt templates

---

## Key Insights

After dozens of experiments, here's what we've learned:

1. **Logo descriptions matter more than you think.** "red icon" works better than "Databricks logo" because it forces the model to reuse rather than recreate.

2. **Temperature 0.4 is the sweet spot.** Low enough for consistency, high enough for visual creativity.

3. **Automatic constraint injection is essential.** Relying on humans to remember logo rules in every template = guaranteed failures.

4. **YAML specs enable collaboration.** Non-technical stakeholders can edit architecture specs without touching code.

5. **MLflow tracking pays off immediately.** Being able to say "use the prompt from run abc123" is worth the setup cost.

---

## What's Next?

- [x] Visual prompt refinement using diagram analysis ✅ DONE
- [ ] DSPy optimizer for automatic prompt improvement
- [ ] Batch generation for A/B testing multiple templates
- [ ] Automatic A/B testing of refined prompts
- [ ] Web UI for non-CLI users
- [ ] Integration with Confluence/Notion for automatic diagram updates
- [ ] Logo composition engine for complex multi-logo arrangements
- [ ] Refinement history tracking and prompt lineage

---

## License

See PRD document for project details and requirements.

---

**Built with science, shipped with style. 🧪🎨**
