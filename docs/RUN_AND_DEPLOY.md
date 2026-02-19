# Run And Deploy

This guide gives a single path for local execution and Databricks Apps
deployment for the React + FastAPI web application.

## Prerequisites

- Python 3.11+
- `uv`
- Node.js 18+
- Databricks CLI (`databricks`) for deployment

## Local Run

Use the helper script:

```bash
scripts/run_web_local.sh
```

This runs:

- backend (FastAPI) on `:8080`
- frontend dev server on `:5173`

Backend-only mode that serves built frontend:

```bash
scripts/run_web_local.sh --no-dev --port 8080
```

## Deploy To Databricks Apps

Use the deployment helper script:

```bash
scripts/deploy_databricks_app.sh
```

It performs:

1. Python dependency install (`.[web]`)
2. Frontend build (`frontend/dist`)
3. `databricks apps deploy`

## Useful Follow-Up Commands

```bash
databricks apps list
databricks apps get bricksmith-architect
```

## Notes

- Deployment uses `app.yaml` at repo root.
- Ensure Databricks credentials and required environment variables are
  configured before deployment.
