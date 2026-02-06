# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository overview

**nano_banana** is an MLflow-tracked prompt engineering system for generating architecture diagrams using Google AI's Gemini models. The system emphasizes reproducibility, logo fidelity, and iterative refinement.

**Note:** While `pyproject.toml` references an `rfp_refiner` package, only `nano_banana` currently exists in the codebase.

## Development commands

**This project uses `uv` exclusively.**

```bash
# Setup
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"

# Run tests
uv run pytest

# Code quality
uv run black src/ tests/
uv run ruff check src/ tests/
uv run mypy src/
```

### Makefile shortcuts

```bash
make test           # Run tests
make format         # Format code
make lint           # Lint code
make check          # All quality checks
```

## Environment setup

```bash
cp .env.example .env   # Create from template
source .env            # Load environment
```

**Required environment variables:**
- `GEMINI_API_KEY` - Google AI Studio API key
- `DATABRICKS_HOST` - Databricks workspace URL
- `DATABRICKS_TOKEN` - Databricks access token
- `DATABRICKS_USER` - Databricks username/email

## CLI commands

### Generation
```bash
# Generate from raw prompt file (primary workflow)
nano-banana generate-raw --prompt-file prompts/my_prompt.txt --logo-dir logos/default
```

### Evaluation
```bash
nano-banana evaluate <run-id>                     # Score a diagram interactively
nano-banana list-runs --filter "metrics.overall_score > 4.0"
nano-banana show-run <run-id>
```

### Refinement
```bash
# Refine based on feedback
nano-banana refine <run-id> --feedback "logos not included, text blurry"

# Analyze diagram and get prompt improvement suggestions
nano-banana refine-prompt --run-id <run-id> --feedback "logos too small"

# Interactive conversation mode for iterative refinement
nano-banana chat --prompt-file prompt.txt --max-iterations 10 --target-score 5

# Auto-refine (fully autonomous)
nano-banana chat --prompt-file prompt.txt --auto-refine --target-score 4
```

### Collaborative design
```bash
# Conversational architecture design
nano-banana architect --problem "Build a real-time analytics pipeline"
```

### Web interface
```bash
nano-banana web                                    # Run locally
```

### Utilities
```bash
nano-banana validate-logos --logo-dir logos/default/
```

## Architecture overview

1. **Configuration** (`config.py`): YAML + env var loading with Pydantic validation
2. **Logo Kit** (`logos.py`): Logo validation with SHA256 hashing for reproducibility
3. **Prompt Building** (`prompts.py`): Automatic logo constraint injection
4. **Generation** (`gemini_client.py`): Google AI Gemini API calls
5. **MLflow Tracking** (`mlflow_tracker.py`): Full experiment tracking to Databricks
6. **Evaluation** (`evaluator.py`): Manual rubric-based scoring (0-5 scale)
7. **Refinement** (`prompt_refiner.py`, `conversation.py`): Visual analysis and iterative improvement
8. **Architect** (`architect.py`): Conversational architecture design with DSPy

### Key principles

- **Logo descriptions, not filenames**: AI receives descriptions ("red icon"), never filenames
- **Automatic constraint injection**: Logo requirements prepended to ALL prompts
- **MLflow-first**: Every generation creates a tracked run
- **DSPy integration**: `conversation_dspy.py` enables AI-driven prompt refinement

## Key modules

| Module | Purpose |
|--------|---------|
| `cli.py` | Click CLI entry point |
| `config.py` | Pydantic config (YAML/env) |
| `models.py` | Data models (LogoInfo, ConversationSession, ArchitectSession) |
| `logos.py` | Logo validation and SHA tracking |
| `prompts.py` | Logo section building and prompt validation |
| `gemini_client.py` | Google AI Gemini client |
| `mlflow_tracker.py` | MLflow/Databricks integration |
| `evaluator.py` | Manual evaluation interface |
| `prompt_refiner.py` | Visual analysis for prompt improvement |
| `conversation.py` | Interactive chatbot for iterative refinement |
| `conversation_dspy.py` | DSPy-based conversational refiner |
| `architect.py` | Conversational architecture design |

## Evaluation rubric

Diagrams scored 0-5 on four dimensions:
1. **Logo fidelity**: Logos reused exactly without modifications
2. **Layout clarity**: Clear flow, logical grouping, good spacing
3. **Text legibility**: All labels readable and well-formatted
4. **Constraint compliance**: All requirements from prompt followed

**Critical:** Any filename in output = automatic penalty.

## Configuration precedence

1. Environment variables (e.g., `NANO_BANANA_VERTEX__MODEL_ID`)
2. YAML config file (`configs/default.yaml`)
3. Code defaults

## Rules

- **Documentation location**: All documentation files (`.md`) go in `docs/`. Exceptions: `README.md`, `CLAUDE.md`, `CHANGELOG.md`, `CONTRIBUTING.md` stay in root. Context-specific READMEs (e.g., `logos/*/README.md`) stay with their directories.

## Documentation

- `docs/SETUP.md` - Installation, authentication, logo setup, configuration
- `docs/WORKFLOWS.md` - All three workflows (generate-raw, architect, chat)
- `docs/TROUBLESHOOTING.md` - Common issues and solutions
- `docs/WEB_INTERFACE.md` - Web interface deployment
- `docs/nano_banana/LOGO_HINTS.md` - Automatic logo-specific instructions
