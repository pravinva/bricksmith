#!/bin/bash
# Generate AGL Synapse Migration Architecture Diagram

uv run bricksmith generate-raw \
  --prompt-file prompts/prompt_templates/agl_synapse_migration.txt \
  --logo-dir logos/default \
  --aspect-ratio 16:9 \
  --run-name "agl-synapse-migration" \
  --no-feedback
