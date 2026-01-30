#!/bin/bash
# Generate AGL Synapse Migration Architecture Diagram

uv run nano-banana generate-raw \
  --prompt-file examples/prompt_templates/agl_synapse_migration.txt \
  --logo-dir examples/logo_kit \
  --aspect-ratio 16:9 \
  --run-name "agl-synapse-migration" \
  --no-feedback
