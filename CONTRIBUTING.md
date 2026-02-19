# Contributing to bricksmith

Thank you for your interest in contributing to bricksmith! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Project Structure](#project-structure)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)
- [Style Guidelines](#style-guidelines)

## Code of Conduct

This project follows professional standards of conduct:

- Be respectful and inclusive
- Focus on constructive feedback
- Assume good intentions
- Prioritize the project's goals
- Help create a welcoming environment

## Getting Started

### Prerequisites

- Python 3.12 or higher
- `uv` package manager
- Git for version control
- Databricks workspace access
- Google AI API key (for Gemini)

### Initial Setup

1. **Fork and clone the repository**:
   ```bash
   git clone https://github.com/your-username/bricksmith.git
   cd bricksmith
   ```

2. **Install dependencies**:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   uv venv
   source .venv/bin/activate
   uv pip install -e ".[dev]"
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

4. **Verify setup**:
   ```bash
   uv run bricksmith verify-setup
   ```

## Development Setup

### Development Tools

Install recommended development tools:

```bash
# Code formatting
uv pip install black

# Type checking
uv pip install mypy

# Testing
uv pip install pytest pytest-cov

# Linting
uv pip install ruff
```

### IDE Configuration

**VS Code** (recommended):
- Install Python extension
- Enable format on save
- Use Black formatter
- Enable mypy type checking

**PyCharm**:
- Configure Python interpreter to use `.venv`
- Enable Black formatter
- Configure mypy as external tool

### Environment Variables

Key environment variables for development:

```bash
# Required
GEMINI_API_KEY=your-key-here
DATABRICKS_HOST=https://your-workspace.databricks.net
DATABRICKS_TOKEN=your-token-here
DATABRICKS_USER=your.email@company.com
GCP_PROJECT_ID=your-project-id

# Optional
LOG_LEVEL=DEBUG  # For detailed logging
BRICKSMITH_MLFLOW__EXPERIMENT_NAME=/Users/your.email/dev-experiments
```

## Project Structure

```
bricksmith/
├── src/bricksmith/      # Main package
│   ├── cli.py           # Command-line interface
│   ├── models.py        # Data models
│   ├── config.py        # Configuration management
│   ├── prompts.py       # Prompt building
│   ├── logos.py         # Logo management
│   ├── runner.py        # Main orchestration
│   ├── gemini_client.py # Gemini API client
│   ├── mlflow_tracker.py # MLflow integration
│   └── evaluator.py     # Evaluation system
├── configs/             # Configuration files
├── docs/                # Documentation
├── logos/               # Logo assets
├── prompts/             # Prompt templates and specs
└── tests/               # Test suite (to be added)
```

### Key Modules

- **cli.py**: Command-line interface using Click
- **models.py**: Pydantic data models for type safety
- **prompts.py**: Template-based prompt generation
- **runner.py**: Main orchestration logic
- **gemini_client.py**: Google AI integration
- **mlflow_tracker.py**: Experiment tracking

## Making Changes

### Branch Strategy

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Branch naming conventions**:
   - `feature/` - New features
   - `fix/` - Bug fixes
   - `docs/` - Documentation updates
   - `refactor/` - Code refactoring
   - `test/` - Test additions/updates

### Development Workflow

1. **Make your changes**:
   - Write clear, maintainable code
   - Follow style guidelines
   - Add docstrings and comments
   - Update documentation

2. **Test your changes**:
   ```bash
   # Run tests
   uv run pytest
   
   # Run with coverage
   uv run pytest --cov
   
   # Run specific test
   uv run pytest tests/test_specific.py::test_function
   ```

3. **Format code**:
   ```bash
   uv run black src/ tests/
   ```

4. **Type check**:
   ```bash
   uv run mypy src/
   ```

5. **Lint code**:
   ```bash
   uv run ruff check src/
   ```

### Testing Your Changes

Before submitting:

1. **Manual testing**:
   ```bash
   # Test basic generation
   uv run bricksmith generate --diagram-spec prompts/diagram_specs/example_basic.yaml --template baseline
   
   # Test with custom prompt
   uv run bricksmith generate-raw --prompt-file prompts/test_prompt.txt --logo logos/default/databricks-full.png
   ```

2. **Regression testing**:
   - Test existing workflows still work
   - Verify backward compatibility
   - Check MLflow tracking still functions

3. **Integration testing**:
   - Test with real Databricks workspace
   - Verify authentication flows
   - Check artifact uploads

## Testing

### Writing Tests

Place tests in `tests/` directory:

```python
# tests/test_prompts.py
import pytest
from bricksmith.prompts import PromptBuilder

def test_prompt_builder_basic():
    """Test basic prompt building functionality."""
    builder = PromptBuilder()
    result = builder.build_prompt(
        template="baseline",
        diagram_spec={"components": [{"id": "test"}]}
    )
    assert result is not None
    assert len(result) > 0
```

### Test Organization

```
tests/
├── test_cli.py          # CLI command tests
├── test_models.py       # Data model tests
├── test_prompts.py      # Prompt building tests
├── test_logos.py        # Logo management tests
├── test_runner.py       # Runner integration tests
└── fixtures/            # Test fixtures
    ├── diagram_specs/
    └── prompt_templates/
```

### Running Tests

```bash
# All tests
uv run pytest

# Specific module
uv run pytest tests/test_prompts.py

# With coverage
uv run pytest --cov=bricksmith --cov-report=html

# Verbose output
uv run pytest -v

# Stop on first failure
uv run pytest -x
```

## Documentation

### Updating Documentation

When adding features, update:

1. **README.md**: Overview and quick start
2. **CLAUDE.md**: Development patterns
3. **docs/**: Detailed guides
4. **CHANGELOG.md**: Record changes
5. **Docstrings**: In-code documentation

### Documentation Standards

**Functions**:
```python
def generate_diagram(spec: DiagramSpec, template: str) -> DiagramResult:
    """Generate architecture diagram from specification.
    
    Args:
        spec: Diagram specification with components and connections
        template: Template name (baseline, detailed, minimal)
        
    Returns:
        DiagramResult with generated image and metadata
        
    Raises:
        ValueError: If spec is invalid
        APIError: If Gemini API call fails
    """
```

**Classes**:
```python
class DiagramGenerator:
    """Orchestrates diagram generation workflow.
    
    This class handles the complete diagram generation pipeline including
    prompt building, logo processing, API calls, and artifact tracking.
    
    Attributes:
        config: Configuration object
        gemini_client: Client for Gemini API
        mlflow_tracker: MLflow tracking instance
    """
```

### Documentation Guidelines

- Use clear, concise language
- Include examples where helpful
- Keep documentation up-to-date with code
- Link related concepts
- Use proper Markdown formatting

## Submitting Changes

### Commit Messages

Follow conventional commit format:

```
<type>: <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples**:
```
feat: Add conversational diagram refinement

Implement conversation module for interactive diagram improvement
through natural language feedback. Supports iterative refinement
with context preservation.

Closes #123
```

```
fix: Resolve logo path resolution on Windows

Update path handling to use pathlib for cross-platform compatibility.
Fixes issue where logos weren't found on Windows systems.

Fixes #456
```

### Pull Request Process

1. **Create pull request**:
   - Use clear, descriptive title
   - Reference related issues
   - Describe changes made
   - Include testing notes

2. **PR template**:
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Documentation update
   - [ ] Refactoring
   
   ## Testing
   - [ ] Existing tests pass
   - [ ] New tests added
   - [ ] Manually tested
   
   ## Documentation
   - [ ] README updated
   - [ ] Docs updated
   - [ ] Docstrings added
   
   ## Related Issues
   Closes #123
   ```

3. **Review process**:
   - Address reviewer feedback
   - Keep discussions constructive
   - Update PR as needed

## Style Guidelines

### Python Code Style

Follow PEP 8 with these specifics:

**Formatting**:
- Use Black formatter (line length: 100)
- 4 spaces for indentation
- Use type hints for function signatures
- Import organization: stdlib, third-party, local

**Naming Conventions**:
```python
# Classes: PascalCase
class DiagramGenerator:
    pass

# Functions/methods: snake_case
def build_prompt():
    pass

# Constants: UPPER_SNAKE_CASE
MAX_RETRIES = 3

# Private: _leading_underscore
def _internal_helper():
    pass
```

**Type Hints**:
```python
from typing import List, Dict, Optional

def process_components(
    components: List[Dict[str, str]],
    template: str
) -> Optional[str]:
    """Process components with template."""
    pass
```

### Code Organization

**Imports**:
```python
# Standard library
import os
import sys
from pathlib import Path

# Third-party
import click
import yaml
from pydantic import BaseModel

# Local
from bricksmith.config import Config
from bricksmith.models import DiagramSpec
```

**File Structure**:
```python
"""Module docstring describing purpose."""

# Imports
...

# Constants
MAX_RETRIES = 3
DEFAULT_TEMPLATE = "baseline"

# Classes
class MyClass:
    ...

# Functions
def my_function():
    ...

# Main execution (if applicable)
if __name__ == "__main__":
    main()
```

### YAML Style

```yaml
# Use 2-space indentation
# Include comments for clarity
# Use quotes for strings with special characters
# Organize logically

vertex:
  model_id: "gemini-1.5-pro"
  temperature: 0.7
  top_p: 0.9
  top_k: 40

mlflow:
  experiment_name: "/Users/user@company.com/experiments"
  artifact_location: "dbfs:/..."
```

## Questions?

- Check existing documentation in `docs/`
- Review similar code in the codebase
- Open a discussion or issue
- Reach out to maintainers

Thank you for contributing to bricksmith!
