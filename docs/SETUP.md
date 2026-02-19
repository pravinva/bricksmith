# Setup guide

Complete setup for Bricksmith — architecture diagram generation with AI. New users should start with [Onboarding](ONBOARDING.md).

## Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- Google account (for AI Studio API key)
- Databricks workspace (for MLflow tracking)

## Installation

```bash
# Install uv if needed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and install
git clone <repo-url> && cd bricksmith
uv venv && source .venv/bin/activate
uv pip install -e .
```

## Authentication

### 1. Google AI API key

Required for diagram generation via Gemini.

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Get API Key" or "Create API Key"
4. Select or create a project
5. Copy the key (starts with `AIza...`)

### 2. Databricks credentials

Required for MLflow experiment tracking.

1. Go to your Databricks workspace
2. Click profile (top right) > Settings > Developer > Access tokens
3. Generate a new token (starts with `dapi...`)
4. Note your workspace URL and username/email

### 3. Configure environment

```bash
cp .env.example .env
# Edit .env with your credentials:
#   GEMINI_API_KEY=AIza...
#   DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
#   DATABRICKS_TOKEN=dapi...
#   DATABRICKS_USER=your.email@company.com

source .env
```

## Logo setup

Logos live in `logos/default/` (or other kit directories). The system maps filenames to descriptions so the AI never sees filenames.

```bash
# Validate your logo kit
bricksmith validate-logos --logo-dir logos/default
```

Key concepts:
- **Descriptions, not filenames**: `databricks-logo.jpg` becomes "red icon" in the prompt
- **Automatic constraint injection**: Logo rules are prepended to every prompt
- **SHA256 tracking**: Logo hashes logged to MLflow for reproducibility

### Logo hints

For logos that AI commonly misinterprets (e.g., Unity Catalog), add hints in `logos/default/logo_hints.yaml`. See [LOGO_HINTS.md](bricksmith/LOGO_HINTS.md) for details.

### Multiple logo kits

Organize logos by cloud provider or customer:

```
logos/
  default/      # Core logos (Databricks, Delta Lake, UC)
  aws/          # AWS-specific logos
  azure/        # Azure-specific logos
```

Use `--logo-dir` to select a kit, or set `logo_kit.logo_dir` in config.

## Configuration

The system uses layered configuration:

1. **Environment variables** (highest priority): e.g., `BRICKSMITH_VERTEX__MODEL_ID`
2. **YAML config**: `configs/default.yaml`
3. **Code defaults** (lowest priority)

Key config settings in `configs/default.yaml`:

```yaml
vertex:
  model_id: "gemini-3-pro-image-preview"
  temperature: 0.4

mlflow:
  tracking_uri: "databricks"
  experiment_name: "/Users/${DATABRICKS_USER}/vertexai-nanobanana-arch-diagrams"

logo_kit:
  logo_dir: "./logos/default"
```

## Verify setup

```bash
source .env
bricksmith validate-logos --logo-dir logos/default
bricksmith check-auth          # Verify credentials
bricksmith generate-raw --help # Check CLI works
```

## Development

```bash
# Install with dev dependencies
uv pip install -e ".[dev]"

# Run tests
uv run pytest

# Code quality
uv run black src/ tests/
uv run ruff check src/ tests/
uv run mypy src/
```

Or use Makefile shortcuts: `make test`, `make format`, `make lint`, `make check`.
