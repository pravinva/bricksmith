#!/usr/bin/env bash
set -euo pipefail

# Run Bricksmith web app locally.
# Usage:
#   scripts/run_web_local.sh            # backend on :8080, frontend on :5173
#   scripts/run_web_local.sh --no-dev   # backend only (serves built frontend)
#   scripts/run_web_local.sh --port 9000

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

MODE="dev"
PORT="8080"
HOST="0.0.0.0"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --no-dev)
      MODE="prod"
      shift
      ;;
    --port)
      PORT="${2:-8080}"
      shift 2
      ;;
    --host)
      HOST="${2:-0.0.0.0}"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1"
      exit 1
      ;;
  esac
done

if [[ ! -d ".venv" ]]; then
  echo "Creating virtual environment..."
  uv venv
fi

echo "Installing Python deps (dev + web)..."
uv pip install -e ".[dev,web]"

if [[ "${MODE}" == "dev" ]]; then
  echo "Starting web in dev mode (backend + frontend)..."
  uv run bricksmith web --dev --host "${HOST}" --port "${PORT}"
else
  echo "Building frontend for production mode..."
  (
    cd frontend
    npm install
    npm run build
  )
  echo "Starting backend only (serves built frontend)..."
  uv run bricksmith web --host "${HOST}" --port "${PORT}"
fi
