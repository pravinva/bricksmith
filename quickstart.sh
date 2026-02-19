#!/bin/bash
# Quick start script for bricksmith
# Run this script to set up and generate your first diagram

set -e  # Exit on error

echo "🍌 bricksmith Quick Start"
echo "=========================="
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv not found. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    uv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install package
echo "📥 Installing bricksmith..."
uv pip install -e .

# Check for .env file
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.example .env
    echo ""
    echo "📝 Please edit .env file with your credentials:"
    echo "   - GEMINI_API_KEY"
    echo "   - DATABRICKS_HOST"
    echo "   - DATABRICKS_TOKEN"
    echo "   - DATABRICKS_USER"
    echo ""
    echo "Run this script again after setting up credentials."
    exit 0
fi

# Source .env
echo "🔐 Loading environment variables..."
source .env

# Verify setup
echo "✅ Verifying setup..."
uv run bricksmith verify-setup

# Ask user if they want to generate an example
echo ""
read -p "Would you like to generate an example diagram? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🎨 Generating example diagram..."
    echo "   This may take 30-60 seconds..."
    echo ""
    
    uv run bricksmith generate \
        --diagram-spec prompts/diagram_specs/example_basic.yaml \
        --template baseline \
        --run-name "quickstart-example"
    
    echo ""
    echo "✅ Example diagram generated!"
    echo "   Check the outputs/ directory for your diagram"
    echo ""
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "  1. View your diagram in outputs/"
echo "  2. Try generating custom diagrams:"
echo "     uv run bricksmith generate --diagram-spec prompts/diagram_specs/example_basic.yaml --template baseline"
echo "  3. Read the documentation: docs/WORKFLOWS.md"
echo "  4. Explore example prompts in prompts/"
echo ""
echo "For help, run: uv run bricksmith --help"
echo ""
