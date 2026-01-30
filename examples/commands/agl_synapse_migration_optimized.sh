#!/bin/bash
# Optimized settings for AGL Synapse Migration diagram
# Shows 12-month migration journey from Synapse to Databricks
# Higher top-p (0.95) and top-k (50) for better logo inclusion

uv run nano-banana generate-raw \
  --prompt-file examples/prompt_templates/agl_synapse_migration.txt \
  --logo-dir examples/logo_kit \
  --aspect-ratio 16:9 \
  --size 2K \
  --run-name "agl-synapse-migration" \
  --count 3 \
  --feedback
