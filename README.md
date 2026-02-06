# Nano Banana

Prompt engineering toolkit for generating architecture diagrams with Google Gemini. Tracks every experiment in MLflow, enforces logo fidelity through description abstraction, and supports iterative refinement via AI-powered feedback loops.

## Quick start

```bash
# Install
uv venv && source .venv/bin/activate
uv pip install -e .

# Configure credentials
cp .env.example .env  # Add GEMINI_API_KEY, DATABRICKS_HOST, DATABRICKS_TOKEN, DATABRICKS_USER
source .env

# Generate a diagram
nano-banana generate-raw --prompt-file prompts/my_prompt.txt --logo-dir logos/default
```

## Workflows

### 1. Generate from a raw prompt

Write a prompt describing your architecture, then generate directly.

```bash
nano-banana generate-raw \
    --prompt-file prompts/my_prompt.txt \
    --logo-dir logos/default \
    --run-name "lakehouse-v1"
```

Logo constraints are automatically prepended to your prompt. Every generation is tracked in MLflow.

### 2. Architect - conversational design

Describe your problem and discuss architecture through natural dialogue. The AI generates a diagram prompt when the design is ready.

```bash
nano-banana architect --problem "Build a real-time analytics pipeline for IoT data"

# With customer context
nano-banana architect \
    --problem "Migrate from Snowflake to Databricks" \
    --context prompts/context/customer_background.md
```

Type `output` to generate the prompt, then use it with `generate-raw`.

### 3. Chat - iterative refinement

Interactive loop: generate, review, provide feedback, and let DSPy refine the prompt automatically.

```bash
# Interactive mode
nano-banana chat --prompt-file prompts/my_prompt.txt

# Fully autonomous refinement
nano-banana chat --prompt-file prompts/my_prompt.txt --auto-refine --target-score 4

# Match a reference image's style
nano-banana chat --prompt-file prompts/my_prompt.txt --reference-image examples/good_diagram.png
```

### Web interface

Deploy as a Databricks App for browser-based collaborative design.

```bash
nano-banana web              # Run locally
databricks apps deploy       # Deploy to Databricks
```

## Key concepts

- **Logo descriptions, not filenames**: The AI sees "red icon", not "databricks-logo.jpg" - preventing filename leakage
- **Automatic constraint injection**: Logo rules prepended to every prompt
- **MLflow tracking**: Every generation creates a tracked run with parameters, artifacts, and metrics
- **DSPy refinement**: AI-powered prompt improvement using conversation history and visual analysis

## MLflow tracking

View experiments in Databricks:

```bash
nano-banana list-runs                                    # Recent runs
nano-banana list-runs --filter "metrics.overall_score > 4.0"  # Filter by score
nano-banana show-run <run-id>                            # Run details
nano-banana evaluate <run-id>                            # Score a diagram
```

## Requirements

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- Google AI API key ([get one here](https://aistudio.google.com/app/apikey))
- Databricks workspace (for MLflow tracking)

## Documentation

- [docs/SETUP.md](docs/SETUP.md) - Installation, authentication, logo setup, configuration
- [docs/WORKFLOWS.md](docs/WORKFLOWS.md) - Detailed workflow guides for all three modes
- [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) - Common issues and solutions
- [docs/WEB_INTERFACE.md](docs/WEB_INTERFACE.md) - Web interface deployment and usage
- [docs/nano_banana/LOGO_HINTS.md](docs/nano_banana/LOGO_HINTS.md) - Logo-specific AI instructions

## Development

```bash
uv pip install -e ".[dev]"
uv run pytest              # Run tests
uv run ruff check src/     # Lint
uv run black src/          # Format
```
