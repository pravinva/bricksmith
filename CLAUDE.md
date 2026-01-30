# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

**nano_banana** is an MLflow-tracked prompt engineering system for generating architecture diagrams using Google AI's Gemini models. The system emphasizes reproducibility, logo fidelity, and structured evaluation.

**Note:** While `pyproject.toml` references an `rfp_refiner` package, only `nano_banana` currently exists in the codebase.

## Environment & Dependency Management

**This project uses `uv` exclusively.**

```bash
# Initial setup
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv && source .venv/bin/activate
uv pip install -e .

# Development dependencies
uv pip install -e ".[dev]"

# Run all tests
uv run pytest

# Run single test
uv run pytest tests/test_specific.py::test_function_name

# Run with coverage
uv run pytest --cov

# Code formatting
uv run black src/ tests/

# Type checking
uv run mypy src/
```

## Authentication Setup

### Quick Setup

```bash
# Create .env from template
cp .env.example .env

# Edit with your credentials
nano .env

# Load environment
source .env

# Verify
nano-banana check-auth
```

### Getting Your API Keys

#### Google AI API Key (Required)

1. Go to https://aistudio.google.com/app/apikey
2. Sign in with Google account
3. Click "Get API Key" or "Create API Key"
4. Select/create a project
5. Copy the key (starts with `AIza...`)

#### Databricks Credentials (Required)

1. Go to your Databricks workspace
2. Profile → Settings → Developer → Access tokens
3. Generate new token
4. Copy token (starts with `dapi...`)
5. Note workspace URL and username

### Environment Variables

```bash
# Required: Google AI Studio API key (for Gemini)
export GEMINI_API_KEY="AIza...your-key-here..."

# Required: Databricks MLflow tracking
export DATABRICKS_HOST="https://your-workspace.cloud.databricks.com"
export DATABRICKS_TOKEN="dapi...your-token-here..."
export DATABRICKS_USER="your.email@company.com"

# Optional: GCP (if using Vertex AI directly)
export GCP_PROJECT_ID="fe-dev-sandbox"
```

## CLI Commands

```bash
# Verify complete setup
nano-banana verify-setup

# Generate diagram from spec
nano-banana generate \
    --diagram-spec prompts/diagram_specs/example.yaml \
    --template baseline \
    --run-name "my-diagram" \
    --tag key=value

# Evaluate generated diagram
nano-banana evaluate <run-id>

# List and filter runs
nano-banana list-runs [--filter "metrics.overall_score > 4.0"] [--max-results 10]
nano-banana show-run <run-id>

# Prompt analysis and improvement
nano-banana analyze-prompts --min-score 4.5
nano-banana suggest-improvements --template baseline
nano-banana template-stats
nano-banana dimension-stats

# Visual prompt refinement
nano-banana refine-prompt --run-id <run-id> --feedback "logos too small"
nano-banana refine-prompt --reference-image path/to/diagram.png --original-prompt path/to/prompt.txt

# Scenario to diagram generation (NEW)
nano-banana scenario-to-spec --scenario "Build a lakehouse on AWS" --output spec.yaml
nano-banana generate-from-scenario --scenario "Real-time pipeline with Kafka and Spark" --template baseline
nano-banana compare-diagrams --good-run <id1> --bad-run <id2>

# Logo management
nano-banana validate-logos --logo-dir logos/default/

# Auth check
nano-banana check-auth
```

## Architecture Overview

The system follows a pipeline architecture orchestrated by `runner.py`:

1. **Configuration** (`config.py`): Loads from `configs/default.yaml` with environment variable overrides
2. **Logo Kit** (`logos.py`): Validates and tracks logos with SHA256 hashing
3. **Prompt Building** (`prompts.py`): Template-based with variable substitution and guaranteed logo constraints
4. **Generation** (`gemini_client.py`): Calls Google AI Gemini API with OAuth
5. **MLflow Tracking** (`mlflow_tracker.py`): Logs parameters, metrics, artifacts to Databricks
6. **Evaluation** (`evaluator.py`): Manual rubric-based scoring (0-5 scale)
7. **Analysis** (`analyzer.py`): Cross-run prompt performance analysis
8. **Prompt Refinement** (`prompt_refiner.py`): Visual analysis and prompt improvement suggestions

### Key Architecture Principles

- **Logo Descriptions Not Filenames**: AI model receives logo descriptions ("red icon"), never filenames, preventing filename leakage
- **Automatic Constraint Injection**: Logo requirements automatically prepended to ALL prompts if template doesn't include them
- **MLflow-First**: Every generation creates an MLflow run with full traceability
- **Template Variables**: Prompts use `{variable}` syntax with standard sections: `{logo_section}`, `{diagram_section}`

## File Structure

```
src/nano_banana/
├── cli.py              # Click-based CLI (entry point)
├── runner.py           # Pipeline orchestrator
├── config.py           # Pydantic config with YAML/env loading
├── models.py           # Pydantic data models (DiagramSpec, LogoInfo, PromptRefinement, etc.)
├── logos.py            # Logo validation and SHA tracking
├── prompts.py          # Template loading and prompt building
├── prompt_refiner.py   # Visual analysis and prompt refinement
├── gemini_client.py    # Google AI SDK client (with vision analysis)
├── mlflow_tracker.py   # MLflow integration (Databricks)
├── evaluator.py        # Manual evaluation interface
└── analyzer.py         # Cross-run analysis

configs/
├── default.yaml        # Default configuration
├── databricks.yaml     # Databricks-specific settings
└── local.yaml          # Local development overrides

prompts/
├── diagram_specs/      # YAML diagram specifications
└── prompt_templates/   # .txt prompt templates

logos/                  # Logo kits (organized by use case)
├── default/           # Default Databricks logos
├── aws/              # AWS + Databricks
├── azure/            # Azure + Databricks
└── gcp/              # GCP + Databricks

docs/nano_banana/
├── LOGO_SETUP.md          # Logo configuration guide
└── PROMPT_REFINEMENT.md   # Visual prompt refinement guide
```

## Configuration System

Configuration follows this precedence (highest to lowest):
1. Environment variables (e.g., `NANO_BANANA_VERTEX__MODEL_ID`)
2. YAML config file (default: `configs/default.yaml`)
3. Defaults in code

**Key config sections:**
- `vertex`: Gemini model settings (project, model_id, temperature, etc.)
- `mlflow`: Tracking URI, experiment name, artifact location
- `logo_kit`: Logo directory, size limits, allowed extensions

## Diagram Specification Format

YAML files in `prompts/diagram_specs/`:

```yaml
name: "architecture-name"
description: "What this architecture does"

components:
  - id: "component-1"
    label: "Display Name"
    type: "service"
    logo_name: "databricks"  # Must match logo file in logo_kit

connections:
  - from_id: "component-1"
    to_id: "component-2"
    label: "data flow"
    style: "solid"  # or "dashed"

constraints:
  layout: "left-to-right"
  background: "white"
  label_style: "sentence-case"
  spacing: "comfortable"
```

## Prompt Templates

Text files in `prompts/prompt_templates/` with variable substitution:

```
Generate a clean architecture diagram.

{logo_section}

{diagram_section}

Style: Professional, modern, clean.
```

**Built-in variables:**
- `{logo_section}`: Auto-generated logo descriptions and constraints
- `{diagram_section}`: Components, connections, and requirements from spec

## Evaluation Rubric

All diagrams scored 0-5 across four dimensions:

1. **Logo Fidelity**: Logos reused exactly without modifications
2. **Layout Clarity**: Clear flow, logical grouping, good spacing
3. **Text Legibility**: All labels readable and well-formatted
4. **Constraint Compliance**: All requirements from spec followed

**Critical constraint:** Any filename in output results in automatic penalty.

## Critical Constraints (Auto-Enforced)

These are **automatically guaranteed** by `prompts.py`:

- ✅ No filenames in outputs (only descriptions)
- ✅ Exact logo reuse (no modifications)
- ✅ Uniform scaling across all logos
- ✅ Logo constraints prepended to every prompt if missing from template

See `src/nano_banana/prompts.py` for enforcement logic.

## Common Workflows

### Generate and Evaluate
```bash
# 1. Generate
source .env
nano-banana generate --diagram-spec prompts/diagram_specs/basic.yaml --template baseline

# 2. Note the run_id from output
# 3. Evaluate
nano-banana evaluate <run-id>

# 4. View in Databricks MLflow UI
# Navigate to: ML → Experiments → /Users/your.email/vertexai-nanobanana-arch-diagrams
```

### Prompt Template Experimentation
```bash
# 1. Create new template in prompts/prompt_templates/my_template.txt
# 2. Generate with new template
nano-banana generate --diagram-spec spec.yaml --template my_template

# 3. Compare results
nano-banana template-stats
nano-banana analyze-prompts --min-score 4.0
```

### Logo Kit Updates
```bash
# 1. Add new logo to logos/default/
# 2. Validate
nano-banana validate-logos --logo-dir logos/default/

# 3. Update logo descriptions in src/nano_banana/logos.py if needed
# 4. Generate new diagram using the logo
```

### Visual Prompt Refinement (NEW)
```bash
# 1. Generate initial diagram
nano-banana generate --diagram-spec spec.yaml --template baseline --run-name "v1"

# 2. Analyze and get specific improvements
nano-banana refine-prompt \
    --run-id <v1-run-id> \
    --feedback "logos too small, need more spacing" \
    --output-template prompts/prompt_templates/baseline_v2.txt

# 3. Generate with refined prompt
nano-banana generate --diagram-spec spec.yaml --template baseline_v2 --run-name "v2"

# 4. Compare results
nano-banana compare-diagrams --good-run <v2-run-id> --bad-run <v1-run-id>

# 5. Iterate until satisfied
nano-banana refine-prompt --run-id <v2-run-id> --feedback "perfect!" --output-template proven_winner.txt
```

## Development Notes

- **MLflow tracking** is always on - every `generate` creates a run
- **Logo descriptions** are hardcoded in `logos.py` and mapped by logo name
- **Prompt builder** automatically handles missing template variables
- **OAuth only** - no direct API key usage for Vertex AI (but Google AI Studio key is used for Gemini)
- **Databricks MLflow** is the default tracking backend (see `configs/default.yaml`)

## Documentation

- `README.md` - Overview and quick start
- `docs/nano_banana/AUTHENTICATION.md` - Complete authentication setup guide
- `docs/nano_banana/LOGO_SETUP.md` - Logo configuration details
- `docs/nano_banana/PROMPT_REFINEMENT.md` - Visual prompt refinement guide (NEW)
- `docs/START_HERE.md` - DSPy and MCP integration notes
- `.env.example` - Environment variable template
