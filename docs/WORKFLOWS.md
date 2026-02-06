# Workflows

Three ways to generate architecture diagrams with nano_banana.

## 1. Generate from a raw prompt

Write a prompt file describing your architecture, then generate directly.

```bash
nano-banana generate-raw \
    --prompt-file prompts/my_prompt.txt \
    --logo-dir logos/default \
    --run-name "lakehouse-v1"
```

Your prompt file should describe the architecture you want. Logo constraints are automatically prepended. Example:

```
Create a Databricks Lakehouse architecture diagram showing:
- Data ingestion from S3 and Kafka
- Bronze, Silver, Gold medallion layers
- Unity Catalog for governance
- SQL Warehouse for BI queries
- Use clean lines and professional styling
```

Key options:

| Option | Default | Description |
|--------|---------|-------------|
| `--prompt-file` | required | Path to prompt text file |
| `--logo-dir` | from config | Logo directory |
| `--run-name` | auto | MLflow run name |
| `--temperature` | 0.8 | Generation temperature (0.0-2.0) |
| `--tag` | - | Key=value tags for MLflow |

Output is saved to `outputs/` and tracked in MLflow.

## 2. Architect - conversational design

Describe your problem and discuss architecture through natural dialogue. The AI generates a diagram prompt when the design is ready.

```bash
# Start with a problem description
nano-banana architect --problem "Build a real-time analytics pipeline for IoT data"

# With customer context
nano-banana architect \
    --problem "Migrate from Snowflake to Databricks" \
    --context prompts/context/customer_background.md

# Use an existing prompt as reference
nano-banana architect \
    --problem "Similar diagram for ANZ Bank" \
    --reference-prompt prompts/coles_semantic_fragmentation.md
```

During the conversation:

| Command | Action |
|---------|--------|
| Natural text | Continue discussing architecture |
| `output` or `generate` | Generate the diagram prompt |
| `status` | Show current architecture state |
| `done` | Save session and exit |

Output files saved to `outputs/<date>/architect-<session>/`:
- `prompt.txt` - Generated diagram prompt for `generate-raw`
- `session.json` - Full conversation history
- `architecture.json` - Final architecture state

After a session, generate the diagram:

```bash
nano-banana generate-raw --prompt-file outputs/<date>/architect-<session>/prompt.txt
```

## 3. Chat - iterative refinement

Interactive loop: generate a diagram, review it, provide feedback, and let DSPy refine the prompt automatically.

```bash
# Interactive mode
nano-banana chat --prompt-file prompts/my_prompt.txt

# Auto-refine (fully autonomous)
nano-banana chat --prompt-file prompts/my_prompt.txt --auto-refine --target-score 4

# Match a reference image's style
nano-banana chat --prompt-file prompts/my_prompt.txt --reference-image examples/good_diagram.png
```

The loop:
1. **Generate** diagram from prompt
2. **Evaluate** - score 1-5 (or auto-refine does this)
3. **Feedback** - describe what needs improvement
4. **Refine** - DSPy analyzes history and refines the prompt
5. **Repeat** until target score or "done"

During feedback, you can:
- Type text feedback for prompt refinement
- `r` or `r 0.5` - retry with different temperature/settings
- `r deterministic` / `r conservative` / `r balanced` / `r creative` / `r wild` - presets
- `done` - end the session

Key options:

| Option | Default | Description |
|--------|---------|-------------|
| `--prompt-file` | required | Initial prompt file |
| `--max-iterations` | 10 | Maximum refinement iterations |
| `--target-score` | 5 | Target score to stop (1-5) |
| `--auto-refine` | false | Autonomous refinement |
| `--reference-image` | - | Reference image to match style |
| `--temperature` | 0.8 | Generation temperature |
| `--dspy-model` | databricks-claude-opus-4-5 | Model for DSPy refinement |

Session output in `outputs/<date>/chat-<session>/`:
- `iteration_1.png`, `iteration_2.png`, ... - Generated diagrams
- `session.json` - Full session history

## MLflow tracking

Every generation creates an MLflow run. View experiments in Databricks:

```
ML > Experiments > /Users/<your-email>/vertexai-nanobanana-arch-diagrams
```

Useful commands:

```bash
# List recent runs
nano-banana list-runs

# Filter by score
nano-banana list-runs --filter "metrics.overall_score > 4.0"

# Show run details
nano-banana show-run <run-id>

# Score a diagram interactively
nano-banana evaluate <run-id>
```

## Web interface

For collaborative, browser-based diagram design:

```bash
# Run locally
nano-banana web

# Or deploy to Databricks Apps
databricks apps deploy
```

See [WEB_INTERFACE.md](WEB_INTERFACE.md) for full documentation.
