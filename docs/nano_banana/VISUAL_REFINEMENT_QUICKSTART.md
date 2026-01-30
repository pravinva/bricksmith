# Visual Prompt Refinement - Quick Start

**Close the feedback loop: Use diagram images to systematically improve your prompts.**

## What We Built

A complete visual prompt refinement system that:

1. **Analyzes diagram images** using Gemini's vision capabilities
2. **Identifies strengths & weaknesses** across 4 evaluation dimensions
3. **Generates concrete improvements** to your prompts (not vague suggestions)
4. **Compares diagrams** to extract what makes one better than another
5. **Tracks everything in MLflow** for full traceability

---

## How to Use It

### Quick Example

```bash
# 1. Generate a diagram (as usual)
nano-banana generate \
    --diagram-spec prompts/diagram_specs/basic.yaml \
    --template baseline \
    --run-name "initial-attempt"

# Output: Run ID abc123, diagram saved to outputs/

# 2. Analyze it and get improvements
nano-banana refine-prompt \
    --run-id abc123 \
    --feedback "logos are too small and hard to see"

# Output: Detailed analysis + refined prompt with specific changes:
#   - "Add: Logos should be at least 80px tall"
#   - "Add: Ensure 40px padding around each logo"
#   - Expected: Logos will be 2-3x larger and more visible

# 3. Save the refined prompt
nano-banana refine-prompt \
    --run-id abc123 \
    --feedback "logos too small" \
    --output-template prompts/prompt_templates/baseline_large_logos.txt

# 4. Generate with the improved prompt
nano-banana generate \
    --diagram-spec prompts/diagram_specs/basic.yaml \
    --template baseline_large_logos \
    --run-name "improved-logos"

# 5. Compare the results
nano-banana compare-diagrams --good-run <new-id> --bad-run abc123
```

---

## Key Commands

### Refine from MLflow Run
```bash
nano-banana refine-prompt \
    --run-id <run-id> \
    --feedback "your specific feedback" \
    --output-template path/to/save/refined_prompt.txt
```

### Refine from Any Image
```bash
nano-banana refine-prompt \
    --reference-image path/to/diagram.png \
    --original-prompt path/to/prompt.txt \
    --feedback "your feedback"
```

### Compare Two Diagrams
```bash
nano-banana compare-diagrams \
    --good-run <better-run-id> \
    --bad-run <worse-run-id>
```

---

## What You Get

### Analysis Output

```
Prompt Refinement Summary
==================================================

Key Changes:
  1. Added explicit logo size constraint: "Logos should be at least 80px tall"
  2. Added emphasis on logo prominence: "Make logos the focal point of each component"
  3. Clarified spacing: "Ensure at least 40px padding around logos"

Expected Improvements:
  1. Logos will be 2-3x larger and more visible
  2. Better visual hierarchy with logos as primary elements
  3. Improved readability at presentation distance

Confidence: 85%

Refined Prompt:
────────────────────────────────────────────────────────────
[Full refined prompt text with all changes integrated]
────────────────────────────────────────────────────────────
```

### Comparison Output

```
Visual Differences:
  • Good diagram: Logos are prominently displayed at ~100px height
  • Bad diagram: Logos are barely visible at ~40px height
  • Good diagram: Clean 60px spacing between components
  • Bad diagram: Crowded with only 20px spacing

Prompt Differences:
  • Good prompt includes: "Logos should be at least 80px tall"
  • Good prompt includes: "Ensure 60px spacing between components"
  • Bad prompt lacks specific size/spacing constraints

Recommendations:
  • Add explicit logo height constraint (80px minimum)
  • Specify spacing requirements in pixels
  • Use "focal point" language to emphasize logo importance
```

---

## When to Use It

✅ **Use visual refinement when:**
- Your diagram has obvious issues (logos too small, poor spacing, etc.)
- You want to understand why one diagram is better than another
- You're building a new template and need to iterate quickly
- You want to learn from successful generations

❌ **Don't use it when:**
- The diagram is already perfect
- You haven't generated any diagrams yet
- The issue is with the diagram spec (not the prompt)
- You need to add/remove components (edit the YAML spec instead)

---

## Best Practices

### 1. Be Specific with Feedback

```bash
# ❌ Vague
--feedback "make it better"

# ✅ Specific
--feedback "logos too small, text overlaps arrows, need more vertical spacing"
```

### 2. Iterate in Small Steps

Don't try to fix everything at once:
```bash
# Round 1: Focus on logo sizing
nano-banana refine-prompt --run-id v1 --feedback "logos too small"

# Round 2: Focus on spacing
nano-banana refine-prompt --run-id v2 --feedback "too crowded"

# Round 3: Focus on text
nano-banana refine-prompt --run-id v3 --feedback "text hard to read"
```

### 3. Always Save Your Refined Prompts

```bash
nano-banana refine-prompt \
    --run-id abc123 \
    --feedback "logos perfect, spacing good" \
    --output-template prompts/prompt_templates/proven_winner.txt
```

Build a library of templates for different scenarios:
```
prompts/prompt_templates/
├── baseline.txt                    # Original
├── baseline_large_logos.txt        # When logos need emphasis
├── baseline_compact.txt            # When space is limited
├── baseline_presentation.txt       # For slide decks
└── baseline_technical.txt          # For detailed docs
```

### 4. Compare Before Committing

Always verify improvements:
```bash
nano-banana compare-diagrams --good-run <refined> --bad-run <original>
```

---

## Architecture

The system adds a new refinement pipeline:

```
┌──────────────────────────┐
│  Existing Diagram        │
│  (from MLflow run or     │
│   any image file)        │
└───────────┬──────────────┘
            │
            ▼
┌──────────────────────────────────────────┐
│  Visual Analysis (Gemini Vision)         │
│                                           │
│  • Analyze image with structured prompt  │
│  • Evaluate 4 dimensions (logo, layout,  │
│    text, constraints)                    │
│  • Identify strengths & weaknesses       │
└───────────┬──────────────────────────────┘
            │
            ▼
┌──────────────────────────────────────────┐
│  Refinement Generation                   │
│                                           │
│  • Take original prompt                  │
│  • Preserve what worked (strengths)      │
│  • Fix what didn't (weaknesses)          │
│  • Be concrete and specific              │
└───────────┬──────────────────────────────┘
            │
            ▼
┌──────────────────────────────────────────┐
│  Output: PromptRefinement                │
│                                           │
│  • Refined prompt text                   │
│  • List of key changes                   │
│  • Expected improvements                 │
│  • Confidence score                      │
└──────────────────────────────────────────┘
```

---

## Implementation Details

### New Files Added

1. **`src/nano_banana/prompt_refiner.py`** - Core refinement logic
2. **`src/nano_banana/models.py`** - Added `PromptRefinement` model
3. **`src/nano_banana/gemini_client.py`** - Added vision analysis methods:
   - `analyze_image()` - Analyze single image
   - `analyze_images()` - Compare multiple images
   - `generate_text()` - Generate refinement suggestions

### CLI Commands Added

1. **`nano-banana refine-prompt`** - Main refinement command
2. **`nano-banana compare-diagrams`** - Comparative analysis

### Context Updates

The CLI `Context` class now includes:
```python
self.prompt_refiner = PromptRefiner(
    self.gemini_client,
    self.mlflow_tracker,
    self.prompt_builder,
)
```

---

## Example Workflows

### Workflow 1: Iterative Improvement

```bash
# Start with baseline
nano-banana generate --diagram-spec spec.yaml --template baseline --run-name "v1"

# Improve logos
nano-banana refine-prompt --run-id <v1> --feedback "logos too small" --output-template v2.txt
nano-banana generate --diagram-spec spec.yaml --template v2 --run-name "v2"

# Improve spacing
nano-banana refine-prompt --run-id <v2> --feedback "too crowded" --output-template v3.txt
nano-banana generate --diagram-spec spec.yaml --template v3 --run-name "v3"

# Improve text
nano-banana refine-prompt --run-id <v3> --feedback "text hard to read" --output-template v4.txt
nano-banana generate --diagram-spec spec.yaml --template v4 --run-name "v4"

# Compare final vs initial
nano-banana compare-diagrams --good-run <v4> --bad-run <v1>
```

### Workflow 2: Learn from Success

```bash
# You generated a perfect diagram once
nano-banana generate --diagram-spec spec.yaml --template baseline --run-name "lucky"

# Analyze what made it work
nano-banana refine-prompt --run-id <lucky> --feedback "this is perfect!"

# Save as proven template
nano-banana refine-prompt \
    --run-id <lucky> \
    --output-template prompts/prompt_templates/proven_winner.txt

# Use for all future diagrams
nano-banana generate --diagram-spec new_spec.yaml --template proven_winner
```

### Workflow 3: Template Comparison

```bash
# Generate with multiple templates
nano-banana generate --diagram-spec spec.yaml --template baseline --run-name "baseline"
nano-banana generate --diagram-spec spec.yaml --template detailed --run-name "detailed"
nano-banana generate --diagram-spec spec.yaml --template minimal --run-name "minimal"

# Evaluate all
nano-banana evaluate <baseline-id>
nano-banana evaluate <detailed-id>
nano-banana evaluate <minimal-id>

# Compare best vs worst
nano-banana compare-diagrams --good-run <best> --bad-run <worst>

# Extract lessons and create hybrid template
nano-banana refine-prompt \
    --run-id <best> \
    --feedback "combine best of all three" \
    --output-template prompts/prompt_templates/hybrid.txt
```

---

## Limitations

1. **Subjective**: AI analysis may differ from human perception
2. **Context-dependent**: Quality depends on your feedback specificity
3. **Iterative**: Usually needs multiple rounds for optimal results
4. **Cost**: Each analysis calls Gemini API (but much cheaper than generating images)

---

## Tips & Tricks

### Get Better Analysis

Provide rich context in your feedback:
```bash
--feedback "For a C-level presentation: logos too small (need ~100px), \
           spacing too tight (60px min), text should be bold for projection"
```

### Build Template Variants

Create systematic variations:
```bash
# Base template
nano-banana generate --diagram-spec spec.yaml --template baseline

# Variant: Large logos
nano-banana refine-prompt --run-id <id> \
    --feedback "optimize for logo visibility" \
    --output-template baseline_large_logos.txt

# Variant: Compact
nano-banana refine-prompt --run-id <id> \
    --feedback "optimize for fitting more components" \
    --output-template baseline_compact.txt

# Variant: Presentation
nano-banana refine-prompt --run-id <id> \
    --feedback "optimize for slide deck projection" \
    --output-template baseline_presentation.txt
```

### Track Refinement Lineage

Tag your runs to track evolution:
```bash
nano-banana generate --diagram-spec spec.yaml --template baseline \
    --run-name "v1_baseline" --tag iteration=1

nano-banana generate --diagram-spec spec.yaml --template refined_v2 \
    --run-name "v2_large_logos" --tag iteration=2 --tag refined_from=<v1-id>

nano-banana generate --diagram-spec spec.yaml --template refined_v3 \
    --run-name "v3_spacing_fixed" --tag iteration=3 --tag refined_from=<v2-id>
```

---

## Next Steps

1. Try it out on your existing diagrams
2. Build a library of refined templates
3. Compare templates systematically
4. Share successful templates with your team

**Full documentation:** `docs/nano_banana/PROMPT_REFINEMENT.md`

---

**The feedback loop is now closed. 🎯**
