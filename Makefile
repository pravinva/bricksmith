.PHONY: help install dev-install test test-cov format lint type-check clean verify run-example docs web-dev web-prod app-deploy

# Default target
help:
	@echo "nano_banana Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install       Install package"
	@echo "  make dev-install   Install with dev dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make test          Run tests"
	@echo "  make test-cov      Run tests with coverage"
	@echo "  make format        Format code with black"
	@echo "  make lint          Lint code with ruff"
	@echo "  make type-check    Type check with mypy"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean         Remove generated files"
	@echo "  make verify        Verify complete setup"
	@echo "  make run-example   Run example diagram generation"
	@echo "  make docs          Generate documentation"
	@echo ""
	@echo "Web App:"
	@echo "  make web-dev       Run backend + frontend dev servers"
	@echo "  make web-prod      Run backend serving built frontend"
	@echo "  make app-deploy    Build frontend and deploy Databricks App"

# Installation
install:
	uv pip install -e .

dev-install:
	uv pip install -e ".[dev]"

# Testing
test:
	uv run pytest

test-cov:
	uv run pytest --cov=nano_banana --cov-report=html --cov-report=term

# Code Quality
format:
	uv run black src/ tests/

lint:
	uv run ruff check src/ tests/

type-check:
	uv run mypy src/

# All quality checks
check: format lint type-check
	@echo "All quality checks passed!"

# Cleanup
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage 2>/dev/null || true
	@echo "Cleaned up generated files"

# Verification
verify:
	uv run nano-banana verify-setup

# Run example
run-example:
	@echo "Generating example diagram..."
	uv run nano-banana generate \
		--diagram-spec prompts/diagram_specs/example_basic.yaml \
		--template baseline \
		--run-name "makefile-example"

# Run with custom prompt
run-custom:
	@echo "Generating custom diagram..."
	uv run nano-banana generate-raw \
		--prompt-file prompts/coles_current_fragmented_state.txt \
		--logo logos/default/databricks-full.png \
		--logo logos/default/delta.png \
		--logo logos/default/unity-catalog.png \
		--run-name "makefile-custom"

# List recent runs
list-runs:
	uv run nano-banana list-runs

# Documentation (placeholder - add sphinx or mkdocs if needed)
docs:
	@echo "Documentation generation not yet configured"
	@echo "See docs/ directory for existing documentation"

# Web app local run and deploy
web-dev:
	bash scripts/run_web_local.sh

web-prod:
	bash scripts/run_web_local.sh --no-dev

app-deploy:
	bash scripts/deploy_databricks_app.sh

# Development workflow
dev-workflow: clean dev-install format lint type-check test
	@echo "Development workflow complete!"

# Pre-commit checks
pre-commit: format lint type-check
	@echo "Pre-commit checks passed!"

# Complete setup from scratch
setup: clean
	@echo "Setting up development environment..."
	uv venv
	@echo "Activate virtual environment with: source .venv/bin/activate"
	@echo "Then run: make dev-install"
