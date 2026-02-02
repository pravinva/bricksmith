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

## Command options

| Option | Default | Description |
|--------|---------|-------------|
| `--prompt-file` | - | Initial prompt file (.txt) |
| `--diagram-spec` | - | Diagram specification YAML file (alternative to prompt-file) |
| `--template` | baseline | Template ID to use with diagram spec |
| `--logo-dir` | from config | Logo directory to use |
| `--max-iterations` | 10 | Maximum refinement iterations |
| `--target-score` | 5 | Target score to stop (1-5) |
| `--temperature` | 0.8 | Generation temperature |
| `--no-auto-analyze` | false | Disable automatic image analysis |
| `--auto-refine` | false | Automatically refine based on design principles (no manual input) |
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
4. You provide feedback describing what to improve
5. DSPy refines the prompt and shows its reasoning

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
