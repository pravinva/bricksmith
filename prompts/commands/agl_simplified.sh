#!/bin/bash
# Generate AGL Simplified Unified Data Intelligence Platform diagram

uv run nano-banana generate-raw \
  --prompt-file prompts/diagram_specs/agl_simplfied.txt \
  --logo-dir logos/default \
  --aspect-ratio 16:9 \
  --size 2K \
  --run-name "agl-simplified" \
  --count 3 \
  --feedback
