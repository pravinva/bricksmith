# Interactive chat refinement

The `nano-banana chat` command provides an interactive refinement loop for iteratively improving architecture diagrams. Instead of manually tweaking prompts and regenerating, you provide feedback and scores, and DSPy-powered AI refines the prompt automatically.

## How it works

The chat command runs a generate -> evaluate -> feedback -> refine loop:

1. **Generate** - Creates a diagram from your prompt using Gemini
2. **Evaluate** - You review the image and provide a score (1-5), or use auto-refine mode
3. **Feedback** - You describe what needs improvement (or AI provides feedback automatically)
4. **Refine** - DSPy analyzes the conversation history and refines the prompt
5. **Repeat** - Until you reach your target score or type "done"

Each iteration is tracked in MLflow, and a session summary is saved at the end.

## Quick start

```bash
# Start with a prompt file (interactive mode)
nano-banana chat --prompt-file prompts/my_prompt.txt

# Auto-refine mode - fully autonomous refinement based on design principles
nano-banana chat --prompt-file prompts/my_prompt.txt --auto-refine

# Set a target score to stop at
nano-banana chat --prompt-file prompts/my_prompt.txt --target-score 4

# Limit iterations
nano-banana chat --prompt-file prompts/my_prompt.txt --max-iterations 5
```

## Auto-refine mode

Use `--auto-refine` to let the AI automatically evaluate and provide feedback based on professional design principles:

```bash
nano-banana chat --prompt-file prompts/my_prompt.txt --auto-refine --target-score 4
```

In auto-refine mode, each diagram is evaluated against five criteria:

| Criterion | What it measures |
|-----------|-----------------|
| **Logo Fidelity** | Are logos crisp, unmodified, and properly sized? |
| **Layout Clarity** | Clear flow direction, logical grouping, balanced composition? |
| **Text Legibility** | All text readable, consistent sizing, proper contrast? |
| **Visual Design** | Clean, professional, presentation-ready appearance? |
| **Data Flow** | Clear directional arrows, logical flow, well-labeled connections? |

The AI provides specific issues found and actionable improvements, then automatically refines the prompt. This continues until the target score is reached or max iterations.

## Reference image mode

Use `--reference-image` to match a specific diagram's style:

```bash
nano-banana chat --prompt-file prompts/my_prompt.txt --reference-image examples/good_diagram.png
```

This mode:
1. Analyzes the reference image to extract design patterns (layout, colors, typography, logo treatment)
2. Compares each generated diagram against the reference
3. Provides feedback on how to better match the reference style
4. Automatically refines prompts to converge on the reference look

This is useful for:
- Matching a company's existing diagram style
- Learning from a well-designed example
- Ensuring consistency across multiple diagrams

## Command options

| Option | Default | Description |
|--------|---------|-------------|
| `--prompt-file` | - | Initial prompt file (.txt) |
| `--diagram-spec` | - | Diagram specification YAML file (alternative to prompt-file) |
| `--template` | baseline | Template ID to use with diagram spec |
| `--logo-dir` | from config | Logo directory to use |
| `--max-iterations` | 10 | Maximum refinement iterations |
| `--target-score` | 5 | Target score to stop (1-5) |
| `--temperature` | 0.8 | Generation temperature (0.0-2.0) |
| `--top-p` | 0.95 | Nucleus sampling (lower=focused, higher=diverse) |
| `--top-k` | 50 | Top-k sampling (0 to disable) |
| `--presence-penalty` | 0.1 | Penalty for repeating elements |
| `--frequency-penalty` | 0.1 | Penalty for frequent patterns |
| `--no-auto-analyze` | false | Disable automatic image analysis |
| `--auto-refine` | false | Automatically refine based on design principles (no manual input) |
| `--reference-image` | - | Reference image to match style (implies --auto-refine) |
| `--dspy-model` | databricks-claude-opus-4-5 | Databricks model for DSPy refinement |

## Starting from a prompt file

The simplest way to start is with a raw prompt file:

```bash
nano-banana chat --prompt-file prompts/my_prompt.txt --logo-dir logos/default
```

Your prompt file should describe the architecture you want. Logo constraints are automatically prepended. Example prompt:

```
Create a Databricks Lakehouse architecture diagram showing:
- Data ingestion from S3 and Kafka
- Bronze, Silver, Gold medallion layers
- Unity Catalog for governance
- SQL Warehouse for BI queries
- Use clean lines and professional styling
```

## Starting from a diagram spec

For more structured generation, use a diagram specification:

```bash
nano-banana chat --diagram-spec prompts/diagram_specs/lakehouse.yaml --template baseline
```

## The feedback loop

During each iteration:

1. The diagram generates and saves to `outputs/<date>/chat-<session-id>/`
2. You see the image path and optional AI analysis
3. You provide a score from 1-5:
   - **1** - Unusable
   - **2** - Major issues
   - **3** - Acceptable with issues
   - **4** - Good with minor issues
   - **5** - Excellent
4. You choose what to do next:
   - **Text feedback** - DSPy refines the prompt based on your feedback
   - **Retry** - Regenerate with same prompt but different temperature/settings
   - **Reference image** - Use an image path as style reference
   - **done** - End the session

### Retry with different settings

When a prompt is "almost right" but the output needs variation, use retry instead of refining:

```
# Retry with slight random temperature variation
r

# Retry with specific temperature (0.0 = deterministic, 2.0 = very creative)
r 0.5
r 1.2

# Retry with specific settings
r t=0.6 p=0.9
r t=0.5 k=30

# Retry with a preset
r deterministic    # t=0.0, most consistent
r conservative     # t=0.4, focused
r balanced         # t=0.8, default
r creative         # t=1.2, more variation
r wild             # t=1.8, high variation
```

This is useful when:
- The layout is good but logos need different placement
- Text rendering varies between generations
- You want to try "rolling the dice" without changing the prompt

### Example feedback

Good feedback is specific and actionable:

- "Logos are too small, make them larger"
- "Text labels are overlapping, add more spacing"
- "The flow direction is confusing, make it left-to-right"
- "Missing the Unity Catalog component"
- "Colors are too bright, use more muted tones"

### Ending the session

Type `done` as feedback or reach the target score to finish. The session summary shows:

- Score progression across iterations
- Best result (highest score)
- Links to MLflow runs
- Session JSON file location

## Session output

Each session creates a directory in `outputs/<date>/chat-<session-id>/` containing:

- `iteration_1.png`, `iteration_2.png`, etc. - Generated diagrams
- `session.json` - Full session history with prompts, scores, feedback

## How DSPy refinement works

The DSPy `ConversationalRefiner` module:

1. Receives conversation history, current prompt, feedback, score, and visual analysis
2. Uses a Databricks-hosted LLM to reason about improvements
3. Outputs a refined prompt that addresses feedback while preserving logo constraints
4. Explains its reasoning and expected improvements

You can specify which model to use:

```bash
nano-banana chat --prompt-file prompt.txt --dspy-model databricks-claude-sonnet-4
```

## Tips for effective refinement

1. **Start with a clear base prompt** - Include layout preferences, style requirements, and all components
2. **Give specific feedback** - "Logos too small" is better than "looks bad"
3. **Score consistently** - Use the same criteria across iterations
4. **Review the AI analysis** - It often catches issues you might miss
5. **Watch the refinement reasoning** - Understand what changes DSPy is making
6. **Don't over-iterate** - If stuck at a score, the prompt may need fundamental changes

## Viewing past sessions

Session data is saved to JSON. To find high-scoring runs:

```bash
nano-banana list-runs --filter "metrics.overall_score > 4.0"
```

To analyze prompts that produced good results:

```bash
nano-banana analyze-prompts --min-score 4.5
```
