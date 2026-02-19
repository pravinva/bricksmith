#!/bin/bash
# Generate Full AGL Architecture diagram

uv run bricksmith generate-raw \
  --prompt-file prompts/prompt_templates/full_arch_agl.md \
  --logo-dir logos/default \
  --aspect-ratio 16:9 \
  --size 2K \
  --run-name "full-arch-agl" \
  --count 3 \
  --feedback
