# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

**nano_banana** is an MLflow-tracked prompt engineering system for generating architecture diagrams using Google AI's Gemini models. The system emphasizes reproducibility, logo fidelity, and structured evaluation.

**Note:** While `pyproject.toml` references an `rfp_refiner` package, only `nano_banana` currently exists in the codebase.

## Development Commands

**This project uses `uv` exclusively.**

```bash
# Quick start (sets up everything)
./quickstart.sh

# Or manual setup
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"

# Run tests
uv run pytest                                      # All tests
uv run pytest tests/test_specific.py::test_name   # Single test
uv run pytest --cov                                # With coverage

# Code quality
uv run black src/ tests/                          # Format
uv run mypy src/                                  # Type check
uv run ruff check src/ tests/                     # Lint
```

### Makefile shortcuts

```bash
make dev-install    # Install with dev dependencies
make test           # Run tests
make test-cov       # Tests with coverage report
make format         # Format code
make lint           # Lint code
make type-check     # Type check
make check          # All quality checks
make verify         # Verify setup
make run-example    # Generate example diagram
make pre-commit     # Run all pre-commit checks
```

## Environment Setup

```bash
cp .env.example .env   # Create from template
source .env            # Load environment
nano-banana check-auth # Verify credentials
```

**Required environment variables:**
- `GEMINI_API_KEY` - Google AI Studio API key (from https://aistudio.google.com/app/apikey)
- `DATABRICKS_HOST` - Databricks workspace URL
- `DATABRICKS_TOKEN` - Databricks access token
- `DATABRICKS_USER` - Databricks username/email

## CLI Commands

### Core Generation
```bash
# Generate from diagram spec (structured YAML)
nano-banana generate --diagram-spec prompts/diagram_specs/example.yaml --template baseline

# Generate from raw prompt file (more flexible, recommended for iteration)
nano-banana generate-raw --prompt-file prompts/my_prompt.txt --logo-dir logos/default

# Generate from natural language scenario
nano-banana generate-from-scenario --scenario "Lakehouse on AWS with S3 and Redshift"
nano-banana scenario-to-spec --scenario "Real-time pipeline" --output spec.yaml
```

### Evaluation & Analysis
```bash
nano-banana evaluate <run-id>                     # Score a diagram interactively
nano-banana list-runs --filter "metrics.overall_score > 4.0"
nano-banana show-run <run-id>
nano-banana template-stats                        # Compare template performance
nano-banana dimension-stats                       # Analyze by rubric dimension
nano-banana analyze-prompts --min-score 4.5       # Find patterns in high-scoring prompts
```

### Refinement
```bash
# Refine based on feedback (regenerates with feedback appended)
nano-banana refine <run-id> --feedback "logos not included, text blurry"

# Analyze diagram and get prompt improvement suggestions
nano-banana refine-prompt --run-id <run-id> --feedback "logos too small"

# Compare two diagrams to extract what makes one better
nano-banana compare-diagrams --good-run <id1> --bad-run <id2>

# Interactive conversation mode for iterative refinement
nano-banana chat --prompt-file prompt.txt --max-iterations 10 --target-score 5
```

### Utilities
```bash
nano-banana validate-logos --logo-dir logos/default/
nano-banana verify-setup
nano-banana check-auth
```

## Architecture Overview

The system follows a pipeline architecture:

1. **Configuration** (`config.py`): YAML + env var loading with Pydantic validation
2. **Logo Kit** (`logos.py`): Logo validation with SHA256 hashing for reproducibility
3. **Prompt Building** (`prompts.py`): Template-based with automatic logo constraint injection
4. **Generation** (`gemini_client.py`): Google AI Gemini API calls
5. **MLflow Tracking** (`mlflow_tracker.py`): Full experiment tracking to Databricks
6. **Evaluation** (`evaluator.py`): Manual rubric-based scoring (0-5 scale)
7. **Analysis** (`analyzer.py`): Cross-run prompt performance analysis
8. **Refinement** (`prompt_refiner.py`, `conversation.py`): Visual analysis and iterative improvement

### Key Principles

- **Logo Descriptions Not Filenames**: AI receives descriptions ("red icon"), never filenames
- **Automatic Constraint Injection**: Logo requirements prepended to ALL prompts automatically
- **MLflow-First**: Every generation creates a tracked run
- **DSPy Integration**: `conversation_dspy.py` enables AI-driven prompt refinement

## Key Modules

| Module | Purpose |
|--------|---------|
| `cli.py` | Click CLI entry point |
| `runner.py` | Pipeline orchestrator |
| `config.py` | Pydantic config (YAML/env) |
| `models.py` | Data models (DiagramSpec, LogoInfo, ConversationSession) |
| `logos.py` | Logo validation and SHA tracking |
| `prompts.py` | Template loading and prompt building |
| `gemini_client.py` | Google AI Gemini client |
| `vertex_client.py` | Vertex AI client (alternative) |
| `mlflow_tracker.py` | MLflow/Databricks integration |
| `evaluator.py` | Manual evaluation interface |
| `analyzer.py` | Cross-run analysis |
| `prompt_refiner.py` | Visual analysis for prompt improvement |
| `conversation.py` | Interactive chatbot for iterative refinement |
| `conversation_dspy.py` | DSPy-based conversational refiner |
| `scenario_generator.py` | Natural language → diagram spec |
| `mcp_enricher.py` | MCP enrichment utilities |
| `dspy_optimizer.py` | DSPy optimizer for automatic prompt improvement |
| `logo_compositor.py` | Logo composition engine |

## Diagram Specification Format

YAML files in `prompts/diagram_specs/`:

```yaml
name: "architecture-name"
description: "What this architecture does"

components:
  - id: "component-1"
    label: "Display Name"
    type: "service"           # service, storage, external, compute, network
    logo_name: "databricks"   # Must match logo file in logo_kit

connections:
  - from_id: "component-1"
    to_id: "component-2"
    label: "data flow"
    style: "solid"            # solid, dashed, dotted

constraints:
  layout: "left-to-right"
  background: "white"
```

## Evaluation Rubric

Diagrams scored 0-5 on four dimensions:
1. **Logo Fidelity**: Logos reused exactly without modifications
2. **Layout Clarity**: Clear flow, logical grouping, good spacing
3. **Text Legibility**: All labels readable and well-formatted
4. **Constraint Compliance**: All requirements from spec followed

**Critical:** Any filename in output = automatic penalty.

## Configuration Precedence

1. Environment variables (e.g., `NANO_BANANA_VERTEX__MODEL_ID`)
2. YAML config file (`configs/default.yaml`)
3. Code defaults

## Rules

- **Documentation location**: All documentation files (`.md`) go in `docs/`. Exceptions: `README.md`, `CLAUDE.md`, `CHANGELOG.md`, `CONTRIBUTING.md` stay in root. Context-specific READMEs (e.g., `logos/*/README.md`) stay with their directories.

## Documentation

- `docs/nano_banana/AUTHENTICATION.md` - Complete auth setup
- `docs/nano_banana/LOGO_SETUP.md` - Logo configuration
- `docs/nano_banana/CHAT_REFINEMENT.md` - Interactive chat loop for iterative diagram refinement
- `docs/nano_banana/PROMPT_REFINEMENT.md` - Visual prompt refinement
- `docs/nano_banana/SCENARIO_TO_DIAGRAM.md` - Scenario-based generation
- `docs/START_HERE.md` - DSPy and MCP integration
