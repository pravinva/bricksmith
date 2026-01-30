#!/bin/bash
# Generate AGL Simplified Unified Data Intelligence Platform diagram

uv run nano-banana generate-raw \
  --prompt-file examples/diagram_specs/agl_simplfied.txt \
  --logo-dir examples/logo_kit \
  --aspect-ratio 16:9 \
  --size 2K \
  --run-name "agl-simplified" \
  --count 3 \
  --feedback
