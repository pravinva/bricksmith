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
PORT=""
HOST="0.0.0.0"

# Find an open port starting from the given base
find_open_port() {
  local port="${1:-8080}"
  while lsof -iTCP:"${port}" -sTCP:LISTEN >/dev/null 2>&1; do
    port=$((port + 1))
  done
  echo "${port}"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --no-dev)
      MODE="prod"
      shift
      ;;
    --port)
      PORT="${2:-}"
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

# Auto-find open port if none was explicitly set
if [[ -z "${PORT}" ]]; then
  PORT=$(find_open_port 8080)
  echo "Auto-selected open port: ${PORT}"
fi

if [[ ! -d ".venv" ]]; then
  echo "Creating virtual environment..."
  uv venv
fi

# Only install deps if explicitly requested or if packages are missing
if [[ "${SKIP_INSTALL:-}" != "1" ]]; then
  if ! python -c "import bricksmith" 2>/dev/null || ! python -c "import uvicorn" 2>/dev/null; then
    echo "Installing Python deps (dev + web)..."
    uv pip install -e ".[dev,web]"
  fi
fi

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
