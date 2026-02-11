# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository overview

**nano_banana** is an MLflow-tracked prompt engineering system for generating architecture diagrams using Google AI's Gemini models (`gemini-3-pro-image-preview`). It uses DSPy with Databricks model serving for AI-driven prompt refinement, and MLflow on Databricks for experiment tracking.

**Note:** `pyproject.toml` also references `rfp_refiner` scripts, but only `nano_banana` exists in the codebase.

## Development commands

**This project uses `uv` exclusively. Python 3.11+.**

```bash
# Setup
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"

# Run all tests
uv run pytest

# Run a single test file or test
uv run pytest tests/test_config.py
uv run pytest tests/test_config.py::test_function_name -v

# Code quality
uv run black src/ tests/        # Format (line-length: 100)
uv run ruff check src/ tests/   # Lint (line-length: 100)
uv run mypy src/                # Type check

# Makefile shortcuts
make test        # Run tests
make format      # Format code
make lint        # Lint code
make type-check  # Type check
make check       # All quality checks (format + lint + type-check)
```

## Environment setup

```bash
cp .env.example .env   # Create from template, fill in values
source .env            # Load environment
```

**Required environment variables:**
- `GEMINI_API_KEY` - Google AI Studio API key (for image generation)
- `DATABRICKS_HOST` - Databricks workspace URL (for MLflow + DSPy model serving)
- `DATABRICKS_TOKEN` - Databricks access token
- `DATABRICKS_USER` - Databricks username/email

## CLI overview

Entry point: `nano-banana` (defined in `cli.py` via Click). Use `nano-banana <command> --help` for full options.

**Primary workflows:**
- `generate-raw` - Generate diagram from a prompt file with logos attached
- `chat` - Interactive generate/evaluate/refine loop (supports `--auto-refine` for fully autonomous mode)
- `architect` - Conversational architecture design that produces a diagram prompt

**Supporting commands:**
- `evaluate`, `list-runs`, `show-run` - MLflow experiment management
- `refine`, `refine-prompt` - One-shot prompt refinement from a previous run
- `validate-logos` - Check logo kit integrity
- `web` - Web interface (FastAPI backend + React frontend)

## Architecture

### Data flow

```
User prompt (.txt) + Logo kit (images/)
    → PromptBuilder (prepends logo constraints)
    → GeminiClient (generates image via Google AI API)
    → MLflowTracker (logs run to Databricks)
    → Output: PNG + metadata in outputs/YYYY-MM-DD/<session>/
```

For iterative workflows (`chat`, `architect`), DSPy modules on Databricks model serving refine prompts between iterations:

```
Generated image → LLM Judge evaluation (via GeminiClient)
    → ConversationalRefiner (DSPy on Databricks) → refined prompt
    → GeminiClient → new image → repeat until target score
```

### Key design patterns

- **Logo descriptions, not filenames**: AI receives descriptions ("red icon"), never filenames. Any filename in output is an automatic quality penalty.
- **Automatic constraint injection**: `PromptBuilder` prepends logo rules, sizing constraints, and negative prompts to ALL user prompts before generation.
- **MLflow-first**: Every generation creates a tracked run with parameters, prompts, images, and metrics.
- **Session persistence**: Both `chat` and `architect` auto-save `session.json` after each turn for crash recovery. Sessions can be resumed with `--resume`.
- **Unity Catalog logo special handling**: The UC logo is passed first AND last in the image parts array to improve Gemini's recognition of it.

### Module relationships

All source is in `src/nano_banana/`. The CLI (`cli.py`) orchestrates everything through a `Context` object that initializes the core components:

- **Config layer**: `config.py` (Pydantic `AppConfig` loaded from `configs/default.yaml` + env vars) and `models.py` (data models for sessions, turns, evaluation)
- **Logo pipeline**: `logos.py` (loading, validation, SHA256 hashing) → `prompts.py` (builds the logo constraint section)
- **Generation**: `gemini_client.py` - Google AI client using `google-genai` SDK. Handles image generation, image analysis, and multi-image comparison. Built-in retry with exponential backoff.
- **Tracking**: `mlflow_tracker.py` - Wraps MLflow for Databricks experiment tracking
- **Refinement via DSPy**: `conversation_dspy.py` and `architect_dspy.py` define DSPy `Signature` and `Module` classes. They connect to Databricks model serving endpoints (e.g., `databricks-claude-opus-4-6`) via LiteLLM.
- **Orchestration**: `conversation.py` (chat loop with LLM Judge evaluation) and `architect.py` (conversational design loop)
- **Web**: `web/` subpackage - FastAPI backend (`web/main.py`) with React/Vite/Tailwind frontend in `frontend/`

### Output structure

All outputs go to `outputs/YYYY-MM-DD/<type>-<session-id>/`:
- `chat-*` directories for chat sessions
- `architect-*` directories for architect sessions
- Direct batch directories for `generate-raw`

Each contains: `session.json`, `iteration_N.png`, `iteration_N_prompt.txt`, `prompt.txt`, `metadata_*.json`

## Configuration precedence

1. Environment variables (prefix `NANO_BANANA_`, nested with `__`, e.g., `NANO_BANANA_VERTEX__MODEL_ID`)
2. YAML config file (`configs/default.yaml`)
3. Code defaults in Pydantic models

## Evaluation

The LLM Judge (`conversation.py:build_evaluation_prompt()`) scores diagrams on 6 criteria (1-5 each): information hierarchy, technical accuracy, logo fidelity, visual clarity, data flow legibility, text readability. Supports persona overlays: architect (default), executive, developer.

Manual evaluation (`evaluator.py`) uses a simpler 4-dimension rubric: logo fidelity, layout clarity, text legibility, constraint compliance.

## Rules

- **Documentation location**: All `.md` files go in `docs/`. Exceptions: `README.md`, `CLAUDE.md`, `CHANGELOG.md`, `CONTRIBUTING.md` stay in root. Context-specific READMEs (e.g., `logos/*/README.md`) stay with their directories.
- **Code style**: Black + Ruff at 100 char line length, target Python 3.11

## Documentation

- `docs/SETUP.md` - Installation, authentication, logo setup, configuration
- `docs/WORKFLOWS.md` - All three workflows (generate-raw, architect, chat)
- `docs/TROUBLESHOOTING.md` - Common issues and solutions
- `docs/WEB_INTERFACE.md` - Web interface deployment
- `docs/nano_banana/LOGO_HINTS.md` - Automatic logo-specific instructions
