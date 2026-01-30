# Visual Prompt Refinement

**Use diagram images to improve your prompts systematically.**

## Overview

The prompt refinement feature uses Gemini's vision capabilities to analyze generated diagrams and suggest concrete improvements to your prompts. Instead of guessing what went wrong, let AI tell you exactly what to fix.

## The Problem

You generate a diagram, but:
- Logos are too small or poorly positioned
- Layout is cluttered or confusing
- Text is hard to read
- Some constraints weren't followed

**Traditional approach:** Manually tweak the prompt, hope it improves, repeat.

**Nano Banana Pro approach:** Analyze the diagram visually, get specific feedback, generate improved prompt.

---

## Features

### 1. Single Diagram Analysis

Analyze any diagram and get prompt improvements:

```bash
# Analyze a previous run
nano-banana refine-prompt \
    --run-id abc123 \
    --feedback "logos are too small, need more spacing"

# Analyze any image
nano-banana refine-prompt \
    --reference-image path/to/diagram.png \
    --original-prompt path/to/prompt.txt \
    --feedback "make it more professional"
```

**What you get:**
- **Strengths**: What worked well (preserve these)
- **Weaknesses**: What didn't work (fix these)
- **Refined Prompt**: Concrete, actionable improvements
- **Expected Improvements**: What should change

### 2. Diagram Comparison

Compare a good diagram against a bad one:

```bash
nano-banana compare-diagrams \
    --good-run abc123 \
    --bad-run def456
```

**What you get:**
- Visual differences between the diagrams
- Prompt elements that likely caused the improvements
- Specific recommendations for making bad → good

---

## How It Works

```
┌─────────────────────────────────────────────────────────┐
│  Input: Diagram Image + Original Prompt                │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│  Visual Analysis (Gemini Vision)                        │
│                                                          │
│  • Evaluate logo fidelity                               │
│  • Assess layout clarity                                │
│  • Check text legibility                                │
│  • Verify constraint compliance                         │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│  Identify Strengths & Weaknesses                        │
│                                                          │
│  Strengths: "Logos correctly positioned and scaled"     │
│  Weaknesses: "Text too small, poor contrast"            │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│  Generate Refined Prompt                                │
│                                                          │
│  • Preserve what worked                                 │
│  • Add specific fixes for weaknesses                    │
│  • Be concrete (not vague like "make it better")        │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│  Output: Refined Prompt + Analysis                      │
└─────────────────────────────────────────────────────────┘
```

---

## Example Workflow

### Scenario: Logos Too Small

**Step 1: Generate initial diagram**
```bash
nano-banana generate \
    --diagram-spec prompts/diagram_specs/basic.yaml \
    --template baseline \
    --run-name "initial-attempt"
```

**Result:** Diagram looks okay but logos are barely visible.

**Step 2: Analyze and refine**
```bash
nano-banana refine-prompt \
    --run-id <run-id-from-step-1> \
    --feedback "logos are too small and hard to see"
```

**Output:**
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
Generate a clean architecture diagram.

LOGO REQUIREMENTS:
- Logos must be at least 80px tall and clearly visible
- Make logos the focal point of each component
- Ensure at least 40px padding around each logo
- Scale all logos uniformly

[... rest of refined prompt ...]
────────────────────────────────────────────────────────────
```

**Step 3: Generate with refined prompt**
```bash
# Save refined prompt
nano-banana refine-prompt \
    --run-id <run-id> \
    --feedback "logos too small" \
    --output-template prompts/prompt_templates/baseline_v2.txt

# Generate with improved prompt
nano-banana generate \
    --diagram-spec prompts/diagram_specs/basic.yaml \
    --template baseline_v2 \
    --run-name "improved-logos"
```

**Result:** Logos are now prominent and clearly visible!

---

## Advanced Usage

### Iterative Refinement

Build up quality through multiple rounds:

```bash
# Round 1: Initial generation
nano-banana generate --diagram-spec spec.yaml --template baseline --run-name "v1"

# Round 2: Fix logos
nano-banana refine-prompt --run-id <v1-id> --feedback "logos too small" --output-template baseline_v2.txt
nano-banana generate --diagram-spec spec.yaml --template baseline_v2 --run-name "v2"

# Round 3: Fix spacing
nano-banana refine-prompt --run-id <v2-id> --feedback "too crowded" --output-template baseline_v3.txt
nano-banana generate --diagram-spec spec.yaml --template baseline_v3 --run-name "v3"

# Compare final vs initial
nano-banana compare-diagrams --good-run <v3-id> --bad-run <v1-id>
```

### Learning from Successes

When you get a great diagram, analyze it to understand why:

```bash
# Analyze successful diagram
nano-banana refine-prompt \
    --run-id <successful-run-id> \
    --feedback "this is perfect, what made it work?"

# Use insights to create new template
nano-banana refine-prompt \
    --run-id <successful-run-id> \
    --output-template prompts/prompt_templates/proven_winner.txt
```

### Comparative Analysis

Compare multiple approaches:

```bash
# Generate with different templates
nano-banana generate --diagram-spec spec.yaml --template baseline --run-name "baseline"
nano-banana generate --diagram-spec spec.yaml --template detailed --run-name "detailed"
nano-banana generate --diagram-spec spec.yaml --template minimal --run-name "minimal"

# Compare best vs worst
nano-banana compare-diagrams --good-run <best> --bad-run <worst>
```

---

## Integration with MLflow

All refinement analyses are tracked:

```python
# In your MLflow experiment
with mlflow.start_run(run_id=original_run_id):
    # Original generation parameters, artifacts, metrics
    pass

# Refinement creates related metadata
refinement = prompt_refiner.refine_from_run(original_run_id)

# Link refined prompt to new generation
with mlflow.start_run(run_name="refined"):
    mlflow.log_param("refined_from", original_run_id)
    mlflow.log_artifact(refined_prompt, "prompt.txt")
    mlflow.log_param("refinement_feedback", user_feedback)
```

---

## Best Practices

### 1. Be Specific in Feedback

❌ **Vague:** "make it better"
✅ **Specific:** "logos too small, text overlaps with arrows, need more vertical spacing"

### 2. Iterate in Small Steps

Don't try to fix everything at once. Focus on one aspect per refinement:
- Round 1: Logo sizing
- Round 2: Layout spacing
- Round 3: Text legibility
- Round 4: Color scheme

### 3. Track Your Changes

Always use `--output-template` to save refined prompts:
```bash
nano-banana refine-prompt \
    --run-id abc123 \
    --feedback "fix spacing" \
    --output-template prompts/prompt_templates/baseline_spacing_v2.txt
```

### 4. Compare Before Moving On

Before committing to a refined prompt, compare results:
```bash
nano-banana compare-diagrams --good-run <new> --bad-run <old>
```

### 5. Build a Template Library

Create versions for different scenarios:
```
prompts/prompt_templates/
├── baseline.txt
├── baseline_large_logos.txt
├── baseline_compact.txt
├── baseline_presentation.txt
└── baseline_detailed.txt
```

---

## API Usage

Use refinement programmatically:

```python
from nano_banana.prompt_refiner import PromptRefiner
from nano_banana.gemini_client import GeminiClient
from nano_banana.mlflow_tracker import MLflowTracker
from nano_banana.prompts import PromptBuilder

# Initialize
gemini_client = GeminiClient()
mlflow_tracker = MLflowTracker(config)
prompt_builder = PromptBuilder()

refiner = PromptRefiner(gemini_client, mlflow_tracker, prompt_builder)

# Refine from run
refinement = refiner.refine_from_run(
    run_id="abc123",
    user_feedback="logos too small"
)

print(refinement.summary())
print(refinement.refined_prompt)

# Save as template
refinement.save_template(Path("prompts/prompt_templates/improved.txt"))

# Compare diagrams
comparison = refiner.compare_diagrams(
    good_run_id="abc123",
    bad_run_id="def456"
)

print(comparison["recommendations"])
```

---

## Technical Details

### Vision Analysis Prompt

The system uses a structured analysis prompt:

```python
analysis_prompt = f"""
Analyze this architecture diagram that was generated with:
{original_prompt}

Evaluate on:
1. Logo Fidelity: Are logos reused exactly? Any distortion? Any filenames?
2. Layout Clarity: Is the flow clear? Good spacing? Logical grouping?
3. Text Legibility: Are all labels readable? Good font sizes?
4. Constraint Compliance: Does it follow requirements?

For each dimension, identify:
- What worked well (strengths)
- What didn't work (weaknesses)
- What's missing

Be specific and concrete. Reference actual visual elements.
"""
```

### Refinement Prompt

The system generates improvements with:

```python
refinement_prompt = f"""
Based on this analysis:
Strengths: {analysis.strengths}
Weaknesses: {analysis.weaknesses}

Original prompt: {original_prompt}

Generate a refined version that:
1. Preserves what worked (the strengths)
2. Addresses weaknesses with specific instructions
3. Is concrete and actionable (avoid vague terms)

Provide:
- The refined prompt (full text)
- Explanation of key changes
- Expected improvements
"""
```

### Model Settings

For analysis tasks, the system uses:
- **Temperature**: 0.2 (factual, consistent analysis)
- **Max tokens**: 2048 (enough for detailed feedback)
- **Response modalities**: TEXT only

---

## Limitations

1. **Subjective Feedback**: The AI analyzes based on its perception, which may differ from human judgment
2. **Context Dependent**: Refinement quality depends on the quality of user feedback
3. **Iterative Process**: Often requires multiple rounds to reach optimal results
4. **API Costs**: Each analysis/refinement calls the Gemini API

---

## Future Enhancements

- [ ] Automatic A/B testing: Generate multiple refined variants
- [ ] Refinement history tracking: See how prompts evolved
- [ ] Batch refinement: Improve multiple diagrams at once
- [ ] Confidence scoring: Know when refinements are reliable
- [ ] Template recommendations: Suggest best template for your spec

---

## Summary

Visual prompt refinement closes the feedback loop in prompt engineering:

```
Generate → Evaluate → Analyze → Refine → Generate
    ↑                                        ↓
    └────────────────────────────────────────┘
```

Instead of guessing what to change, you get:
- ✅ Visual analysis of what worked/didn't work
- ✅ Concrete, specific prompt improvements
- ✅ Comparative insights from multiple diagrams
- ✅ Systematic iteration toward quality

**Result:** Faster convergence to high-quality diagrams with data-driven improvements.
