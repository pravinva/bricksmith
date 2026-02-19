# Bricksmith

<p align="center">
  <img src="docs/bricksmith/logo.png" alt="Bricksmith logo" width="220" />
</p>

**POV:** It's 11pm, the deck is due tomorrow, and someone asked for "just a quick architecture diagram."

**Bricksmith:** You describe the architecture in words → Gemini draws it → an LLM judge scores it → DSPy can refine the prompt → repeat until it looks right. Logos stay logos (the AI never sees filenames). MLflow logs every run so you have a full history. Use the **architect** flow to design in conversation, then generate; or deploy as a Databricks App and skip the .vsdx forever.

---

## New here? Start with onboarding

**[→ Onboarding guide (docs/ONBOARDING.md)](docs/ONBOARDING.md)** — Install, configure credentials, and generate your first diagram in about 15 minutes.

---

## Quick start

```bash
# Install
uv venv && source .venv/bin/activate
uv pip install -e .

# Configure credentials
cp .env.example .env   # Add GEMINI_API_KEY, DATABRICKS_* (see docs/ONBOARDING.md)
source .env

# Generate a diagram
bricksmith generate-raw --prompt-file prompts/branding/minimal.txt --logo-dir logos/default
```

---

## Workflows

### 1. Generate from a raw prompt

Write a prompt describing your architecture, then generate directly.

```bash
bricksmith generate-raw \
  --prompt-file prompts/my_prompt.txt \
  --logo-dir logos/default \
  --run-name "lakehouse-v1"
```

Logo constraints are automatically prepended. Every generation is tracked in MLflow.

### 2. Architect — conversational design

Describe your problem and discuss architecture in natural language. The AI produces a diagram prompt when you’re ready.

```bash
bricksmith architect --problem "Build a real-time analytics pipeline for IoT data"

# With customer context
bricksmith architect \
  --problem "Migrate from Snowflake to Databricks" \
  --context prompts/context/customer_background.md
```

Type `output` to generate the prompt, then use it with `generate-raw`.

### 3. Chat — iterative refinement

Interactive loop: generate, review, give feedback, and let DSPy refine the prompt.

```bash
# Interactive mode
bricksmith chat --prompt-file prompts/my_prompt.txt

# Fully autonomous refinement
bricksmith chat --prompt-file prompts/my_prompt.txt --auto-refine --target-score 4

# Match a reference image's style
bricksmith chat --prompt-file prompts/my_prompt.txt --reference-image examples/good_diagram.png
```

### Web interface

Run locally or deploy as a Databricks App for browser-based use.

```bash
make app                   # Run backend + frontend dev servers
bricksmith web             # Run locally (single command)
# databricks apps deploy    # Deploy to Databricks (when configured)
```

---

## Key concepts

- **Logo descriptions, not filenames** — The model sees descriptions (e.g. "red icon"), not filenames, so they don’t leak into the diagram.
- **Automatic constraint injection** — Logo rules and constraints are prepended to every prompt.
- **MLflow tracking** — Every generation is a tracked run with parameters, artifacts, and metrics.
- **DSPy refinement** — Prompt improvement using conversation history and visual feedback (when Databricks is configured).

---

## MLflow tracking

View and filter runs in Databricks:

```bash
bricksmith list-runs
bricksmith list-runs --filter "metrics.overall_score > 4.0"
bricksmith show-run <run-id>
bricksmith evaluate <run-id>
```

---

## Requirements

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- Google AI API key — [get one](https://aistudio.google.com/app/apikey)
- Databricks workspace (for MLflow tracking and DSPy refinement)

---

## Documentation

| Doc | Description |
|-----|-------------|
| [docs/ONBOARDING.md](docs/ONBOARDING.md) | **Start here** — install, credentials, first diagram |
| [docs/SETUP.md](docs/SETUP.md) | Installation, auth, logo setup, configuration |
| [docs/WORKFLOWS.md](docs/WORKFLOWS.md) | generate-raw, architect, chat in detail |
| [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Common issues and solutions |
| [docs/WEB_INTERFACE.md](docs/WEB_INTERFACE.md) | Web UI deployment and usage |
| [docs/bricksmith/LOGO_HINTS.md](docs/bricksmith/LOGO_HINTS.md) | Logo-specific AI instructions |

---

## Development

```bash
uv pip install -e ".[dev]"
uv run pytest
uv run ruff check src/
uv run black src/
```

See [CLAUDE.md](CLAUDE.md) for full dev and architecture notes.
