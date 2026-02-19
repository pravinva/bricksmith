#!/usr/bin/env bash
set -euo pipefail

# Build and deploy Nano Banana as a Databricks App.
# Usage:
#   scripts/deploy_databricks_app.sh
#
# Prerequisites:
#   - databricks CLI authenticated (databricks auth login or profile configured)
#   - app.yaml in repo root

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

echo "Checking required tools..."
command -v uv >/dev/null 2>&1 || { echo "uv is required"; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "npm is required"; exit 1; }
command -v databricks >/dev/null 2>&1 || { echo "databricks CLI is required"; exit 1; }

if [[ ! -f "app.yaml" ]]; then
  echo "app.yaml not found in ${ROOT_DIR}"
  exit 1
fi

if [[ ! -d ".venv" ]]; then
  echo "Creating virtual environment..."
  uv venv
fi

echo "Installing Python web dependencies..."
uv pip install -e ".[web]"

echo "Building frontend artifacts..."
(
  cd frontend
  npm install
  npm run build
)

echo "Deploying Databricks App..."
databricks apps deploy

echo "Deployment command submitted."
echo "Tip: use 'databricks apps list' and 'databricks apps get nano-banana-architect' to monitor status."
