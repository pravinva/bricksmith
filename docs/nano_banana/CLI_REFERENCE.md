# CLI reference

Complete reference for all `nano-banana` CLI commands.

## Quick reference

| Command | Purpose |
|---------|---------|
| `generate` | Generate diagram from YAML spec |
| `generate-raw` | Generate diagram from raw prompt file |
| `generate-from-scenario` | Generate from natural language description |
| `chat` | Interactive refinement loop |
| `architect` | Collaborative architecture design conversation |
| `web` | Start web interface |
| `evaluate` | Score a generated diagram |
| `refine` | Regenerate with feedback |
| `refine-prompt` | Analyze and improve a prompt |
| `compare-diagrams` | Compare two diagrams |
| `list-runs` | List MLflow experiment runs |
| `show-run` | Show run details |
| `analyze-prompts` | Find patterns in high-scoring prompts |
| `template-stats` | Performance statistics by template |
| `dimension-stats` | Statistics by evaluation dimension |
| `suggest-improvements` | Prompt improvement suggestions |
| `scenario-to-spec` | Convert scenario to YAML spec |
| `validate-logos` | Validate logo kit |
| `check-auth` | Verify authentication |
| `verify-setup` | Check complete system setup |

---

## Global options

These options apply to all commands:

```bash
nano-banana [OPTIONS] COMMAND [ARGS]
```

| Option | Description |
|--------|-------------|
| `--config PATH` | Path to config file (default: `configs/default.yaml`) |
| `--version` | Show version and exit |
| `--help` | Show help message |

---

## Generation commands

### generate

Generate a diagram from a structured YAML specification.

```bash
nano-banana generate [OPTIONS]
```

**Required options:**

| Option | Description |
|--------|-------------|
| `--diagram-spec PATH` | Path to diagram specification YAML file |
| `--template TEXT` | Prompt template ID (e.g., `baseline`, `detailed`) |

**Optional options:**

| Option | Description |
|--------|-------------|
| `--run-name TEXT` | Name for MLflow run |
| `--tag KEY=VALUE` | Tags (can specify multiple times) |

**Example:**

```bash
nano-banana generate \
    --diagram-spec prompts/diagram_specs/lakehouse.yaml \
    --template baseline \
    --run-name "lakehouse-v1" \
    --tag "experiment=baseline" \
    --tag "author=david"
```

---

### generate-raw

Generate a diagram from a raw prompt file with logo kit attached. This is the most flexible generation command - no YAML spec required.

```bash
nano-banana generate-raw [OPTIONS]
```

**Required options:**

| Option | Description |
|--------|-------------|
| `--prompt-file PATH` | Path to prompt file (`.txt` or `.md`) |

**Logo options:**

| Option | Default | Description |
|--------|---------|-------------|
| `--logo-dir PATH` | `logos/default` | Directory containing logo files |
| `--logo PATH` | - | Specific logo file(s) (can specify multiple times). Overrides `--logo-dir` |

**Styling options:**

| Option | Default | Description |
|--------|---------|-------------|
| `--branding PATH` | `prompts/branding/minimal.txt` | Branding/style guide file |
| `--databricks-style` | `false` | Apply official Databricks brand style guide |
| `--avoid TEXT` | - | Things to avoid (simulates negative prompt) |

**Image options:**

| Option | Default | Description |
|--------|---------|-------------|
| `--size` | `1K` | Image resolution: `1K`, `2K`, `4K` |
| `--aspect-ratio` | `16:9` | Aspect ratio: `1:1`, `4:3`, `16:9`, `9:16`, `3:4`, `21:9` |
| `--count` | `1` | Number of images to generate |

**Model parameters:**

| Option | Default | Description |
|--------|---------|-------------|
| `--temperature` | `0.8` | Sampling temperature (0.0-2.0). Lower = deterministic, higher = creative |
| `--top-p` | `0.95` | Nucleus sampling. Lower = focused, higher = diverse |
| `--top-k` | `50` | Top-k sampling. 0 to disable |
| `--presence-penalty` | `0.1` | Penalty for repeating elements (0.0-2.0) |
| `--frequency-penalty` | `0.1` | Penalty for frequent patterns (0.0-2.0) |
| `--system-instruction TEXT` | - | Custom system-level instruction |

**Tracking options:**

| Option | Description |
|--------|-------------|
| `--run-name TEXT` | Name for MLflow run |
| `--tag KEY=VALUE` | Tags (can specify multiple times) |
| `--feedback / --no-feedback` | Prompt for 1-5 scoring after each generation |

**Examples:**

```bash
# Basic generation
nano-banana generate-raw \
    --prompt-file prompts/my_architecture.txt \
    --logo-dir logos/default

# With specific logos only
nano-banana generate-raw \
    --prompt-file prompts/azure_lakehouse.txt \
    --logo logos/default/databricks-logo.png \
    --logo logos/default/azure-logo.png \
    --logo logos/default/delta-lake-logo.png

# Generate multiple variants at different temperatures
nano-banana generate-raw \
    --prompt-file prompts/diagram.txt \
    --count 3 \
    --temperature 0.5

# High-resolution with Databricks branding
nano-banana generate-raw \
    --prompt-file prompts/customer_demo.txt \
    --size 4K \
    --aspect-ratio 16:9 \
    --databricks-style

# With negative prompt
nano-banana generate-raw \
    --prompt-file prompts/clean_diagram.txt \
    --avoid "3D, gradients, shadows, complex backgrounds"

# Interactive feedback collection
nano-banana generate-raw \
    --prompt-file prompts/diagram.txt \
    --count 5 \
    --feedback
```

**Output structure:**

Files are saved to `outputs/YYYY-MM-DD/{run-name}/`:

```
outputs/2026-02-05/my-diagram/
├── prompt.txt                    # Full prompt used
├── diagram_143052_t08.png        # Generated image (timestamp_temperature)
└── metadata_143052_t08.json      # Generation metadata
```

---

### generate-from-scenario

Generate a diagram directly from a natural language description. Combines `scenario-to-spec` and `generate` into one command.

```bash
nano-banana generate-from-scenario [OPTIONS]
```

**Required options:**

| Option | Description |
|--------|-------------|
| `--scenario TEXT` | Natural language description of the architecture |

**Optional options:**

| Option | Default | Description |
|--------|---------|-------------|
| `--template TEXT` | `baseline` | Prompt template to use |
| `--save-spec PATH` | - | Save generated YAML spec to file |
| `--run-name TEXT` | - | Name for MLflow run |

**Example:**

```bash
# Generate from natural language
nano-banana generate-from-scenario \
    --scenario "Real-time streaming pipeline with Kafka ingesting data, Spark processing, and Delta Lake storage"

# Save the intermediate spec
nano-banana generate-from-scenario \
    --scenario "Lakehouse on AWS with S3, Databricks, and Redshift" \
    --save-spec prompts/diagram_specs/aws-lakehouse.yaml \
    --run-name "aws-lakehouse-demo"
```

---

### scenario-to-spec

Generate a YAML diagram specification from a natural language scenario (without generating the diagram).

```bash
nano-banana scenario-to-spec [OPTIONS]
```

**Required options:**

| Option | Description |
|--------|-------------|
| `--scenario TEXT` | Natural language description of the architecture |

**Optional options:**

| Option | Default | Description |
|--------|---------|-------------|
| `--output PATH` | Auto-generated with timestamp | Where to save the YAML spec |

**Example:**

```bash
nano-banana scenario-to-spec \
    --scenario "Multi-cloud data platform with Azure Data Factory, Databricks, and Snowflake" \
    --output prompts/diagram_specs/multicloud.yaml
```

---

## Interactive commands

### chat

Start an interactive refinement conversation. Generates a diagram, lets you provide feedback, and iteratively improves until you're satisfied.

```bash
nano-banana chat [OPTIONS]
```

**Input options (provide one):**

| Option | Description |
|--------|-------------|
| `--prompt-file PATH` | Initial prompt file (`.txt`) |
| `--diagram-spec PATH` | Diagram specification YAML file |

**Session options:**

| Option | Default | Description |
|--------|---------|-------------|
| `--name TEXT` | Filename stem | Session name for output directory |
| `--max-iterations` | `10` | Maximum refinement iterations |
| `--target-score` | `5` | Score to stop at (1-5) |
| `--template TEXT` | `baseline` | Template ID (with `--diagram-spec`) |

**Model parameters:**

| Option | Default | Description |
|--------|---------|-------------|
| `--temperature` | `0.8` | Sampling temperature |
| `--top-p` | `0.95` | Nucleus sampling |
| `--top-k` | `50` | Top-k sampling |
| `--presence-penalty` | `0.1` | Repetition penalty |
| `--frequency-penalty` | `0.1` | Frequency penalty |

**Automation options:**

| Option | Description |
|--------|-------------|
| `--no-auto-analyze` | Disable automatic image analysis |
| `--auto-refine` | Fully autonomous refinement (no manual feedback) |
| `--reference-image PATH` | Image to match style (enables auto-refine) |
| `--persona` | Evaluation persona: `architect` (default), `executive`, `developer`, `auto` |
| `--dspy-model TEXT` | Databricks model for DSPy refinement |

**Logo options:**

| Option | Description |
|--------|-------------|
| `--logo-dir PATH` | Logo directory (default from config) |

**Examples:**

```bash
# Basic interactive refinement
nano-banana chat --prompt-file prompts/my_diagram.txt

# Fully autonomous until score 4
nano-banana chat \
    --prompt-file prompts/diagram.txt \
    --auto-refine \
    --target-score 4

# Match style from reference image
nano-banana chat \
    --prompt-file prompts/new_diagram.txt \
    --reference-image outputs/good_example.png

# Use executive persona (strategic, cost-focused feedback)
nano-banana chat \
    --prompt-file prompts/diagram.txt \
    --auto-refine \
    --persona executive

# From diagram spec with custom iterations
nano-banana chat \
    --diagram-spec prompts/diagram_specs/lakehouse.yaml \
    --template detailed \
    --max-iterations 5
```

**Interactive feedback options:**

During the conversation, you can use:

| Input | Action |
|-------|--------|
| Text feedback | Refines prompt based on your feedback |
| `r` or `retry` | Retry same prompt with slight temperature variation |
| `r 0.5` | Retry with specific temperature |
| `r t=0.5 p=0.9` | Retry with specific temp and top_p |
| `r creative` | Retry with preset: `deterministic`, `conservative`, `balanced`, `creative`, `wild` |
| Image path | Use as style reference |
| `done` | Finish session |

---

### architect

Start a collaborative architecture design conversation. Have a back-and-forth discussion with an AI solutions architect to design your system.

```bash
nano-banana architect [OPTIONS]
```

**Input options:**

| Option | Description |
|--------|-------------|
| `--problem TEXT` | Initial problem description (or enter interactively) |
| `--context PATH` | Custom context file with domain knowledge |
| `--reference-prompt PATH` | Existing prompt to use as style reference |

**Output options:**

| Option | Default | Description |
|--------|---------|-------------|
| `--output-format` | `prompt` | Output format: `prompt` or `spec` |
| `--output-file PATH` | - | Save output to specific file |

**Session options:**

| Option | Default | Description |
|--------|---------|-------------|
| `--name TEXT` | - | Session name for output directory |
| `--max-turns` | `20` | Maximum conversation turns |
| `--logo-dir PATH` | - | Logo directory |
| `--dspy-model TEXT` | - | Databricks model for DSPy |

**Examples:**

```bash
# Start interactively
nano-banana architect

# Start with problem description
nano-banana architect \
    --problem "Design a data lakehouse for a retail company migrating from Snowflake"

# With context and reference
nano-banana architect \
    --problem "Real-time analytics pipeline" \
    --context prompts/context/customer_background.md \
    --reference-prompt prompts/existing_diagram.txt

# Specify output and session name
nano-banana architect \
    --problem "Azure data platform" \
    --output-format prompt \
    --name azure-platform
```

**Interactive commands during conversation:**

| Command | Action |
|---------|--------|
| Natural text | Continue discussing architecture |
| `output` or `generate` | Generate the diagram prompt |
| `status` | Show current architecture state |
| `done` | Save and exit |

---

### web

Start the web interface for architect workflows.

```bash
nano-banana web [OPTIONS]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--host TEXT` | `0.0.0.0` | Host to bind to |
| `--port INT` | `8080` | Port to bind to |
| `--reload` | `false` | Enable auto-reload for development |
| `--dev` | `false` | Development mode (starts both backend and frontend dev servers) |

**Examples:**

```bash
# Start production server
nano-banana web

# Development with auto-reload
nano-banana web --reload

# Full development mode
nano-banana web --dev

# Custom port
nano-banana web --port 3000
```

---

## Refinement commands

### refine

Refine a previous generation based on feedback. Takes the original prompt, appends your feedback, and regenerates.

```bash
nano-banana refine RUN_ID [OPTIONS]
```

**Required arguments:**

| Argument | Description |
|----------|-------------|
| `RUN_ID` | MLflow run ID to refine |

**Required options:**

| Option | Description |
|--------|-------------|
| `--feedback TEXT` | What to improve (e.g., "logos too small, text blurry") |

**Model parameters:**

| Option | Default | Description |
|--------|---------|-------------|
| `--temperature` | `0.8` | Sampling temperature |
| `--top-p` | `0.95` | Nucleus sampling |
| `--top-k` | `40` | Top-k sampling |
| `--presence-penalty` | `0.1` | Repetition penalty |
| `--frequency-penalty` | `0.1` | Frequency penalty |
| `--count` | `1` | Number of refined images to generate |

**Examples:**

```bash
# Basic refinement
nano-banana refine abc123def \
    --feedback "logos are not used, need more spacing between layers"

# Generate multiple refinement attempts
nano-banana refine abc123def \
    --feedback "text is too small, arrows unclear" \
    --count 3 \
    --temperature 0.6
```

---

### refine-prompt

Analyze a generated diagram and get AI-powered prompt improvement suggestions.

```bash
nano-banana refine-prompt [OPTIONS]
```

**Input options (provide one):**

| Option | Description |
|--------|-------------|
| `--run-id TEXT` | MLflow run ID to analyze |
| `--reference-image PATH` | Path to image (requires `--original-prompt`) |

**Additional options:**

| Option | Description |
|--------|-------------|
| `--original-prompt PATH` | Path to prompt file (required with `--reference-image`) |
| `--feedback TEXT` | User feedback about what to improve |
| `--output-template PATH` | Save refined prompt as template |

**Examples:**

```bash
# Analyze a previous run
nano-banana refine-prompt \
    --run-id abc123def \
    --feedback "logos are too small"

# Analyze any image
nano-banana refine-prompt \
    --reference-image outputs/diagram.png \
    --original-prompt prompts/my_prompt.txt \
    --feedback "need clearer data flow"

# Save refined prompt
nano-banana refine-prompt \
    --run-id abc123def \
    --output-template prompts/refined_v2.txt
```

---

### compare-diagrams

Compare two diagrams to identify what makes one better than the other.

```bash
nano-banana compare-diagrams [OPTIONS]
```

**Required options:**

| Option | Description |
|--------|-------------|
| `--good-run TEXT` | MLflow run ID of the better diagram |
| `--bad-run TEXT` | MLflow run ID of the worse diagram |

**Example:**

```bash
nano-banana compare-diagrams \
    --good-run abc123 \
    --bad-run def456
```

**Output includes:**

- Visual differences between diagrams
- Prompt differences
- Actionable recommendations

---

## Evaluation commands

### evaluate

Interactively score a generated diagram using the evaluation rubric.

```bash
nano-banana evaluate RUN_ID [OPTIONS]
```

**Required arguments:**

| Argument | Description |
|----------|-------------|
| `RUN_ID` | MLflow run ID to evaluate |

**Optional options:**

| Option | Description |
|--------|-------------|
| `--eval-file PATH` | Load scores from JSON file instead of interactive |

**Example:**

```bash
# Interactive evaluation
nano-banana evaluate abc123def456

# From file
nano-banana evaluate abc123def456 --eval-file scores.json
```

**Evaluation dimensions (scored 0-5):**

1. **Logo Fidelity** - Are logos reused exactly without modifications?
2. **Layout Clarity** - Is the flow clear with good spacing?
3. **Text Legibility** - Is all text readable and well-formatted?
4. **Constraint Compliance** - Are all requirements from the spec followed?

**Evaluation JSON format:**

```json
{
  "logo_fidelity_score": 5,
  "layout_clarity_score": 4,
  "text_legibility_score": 5,
  "constraint_compliance_score": 4,
  "notes": "Optional notes"
}
```

---

## Analysis commands

### list-runs

List experiment runs from MLflow.

```bash
nano-banana list-runs [OPTIONS]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--filter TEXT` | - | MLflow filter string |
| `--max-results INT` | `10` | Maximum runs to display |

**Examples:**

```bash
# List recent runs
nano-banana list-runs

# More results
nano-banana list-runs --max-results 50

# Filter by score
nano-banana list-runs --filter "metrics.overall_score > 4.0"

# Filter by template
nano-banana list-runs --filter "params.prompt_template_id = 'baseline'"

# Combine filters
nano-banana list-runs --filter "metrics.overall_score > 3.5 AND params.prompt_template_id = 'detailed'"
```

---

### show-run

Show detailed information about a specific run.

```bash
nano-banana show-run RUN_ID
```

**Output includes:**

- Run name and status
- Start/end times
- All parameters (model settings, template, etc.)
- All metrics (scores, generation time)
- Artifact location

**Example:**

```bash
nano-banana show-run abc123def456
```

---

### analyze-prompts

Find patterns in high-scoring prompts to understand what makes prompts effective.

```bash
nano-banana analyze-prompts [OPTIONS]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--min-score FLOAT` | `4.0` | Minimum overall score to include |
| `--dimension TEXT` | - | Focus on specific dimension (see choices below) |
| `--max-runs INT` | `50` | Maximum runs to analyze |

**Dimension choices:**

- `logo_fidelity_score`
- `layout_clarity_score`
- `text_legibility_score`
- `constraint_compliance_score`

**Examples:**

```bash
# Analyze all high-scoring prompts
nano-banana analyze-prompts --min-score 4.5

# Focus on logo fidelity
nano-banana analyze-prompts \
    --dimension logo_fidelity_score \
    --min-score 4.0

# Large-scale analysis
nano-banana analyze-prompts --max-runs 200
```

---

### template-stats

Show performance statistics grouped by template.

```bash
nano-banana template-stats
```

**Output includes:**

- Average scores per template
- Run counts
- Score ranges (min/max)

---

### dimension-stats

Show score statistics by evaluation dimension.

```bash
nano-banana dimension-stats [OPTIONS]
```

| Option | Description |
|--------|-------------|
| `--template TEXT` | Filter by specific template |

**Examples:**

```bash
# All templates
nano-banana dimension-stats

# Specific template
nano-banana dimension-stats --template baseline
```

---

### suggest-improvements

Get AI-powered suggestions for improving prompts based on successful runs.

```bash
nano-banana suggest-improvements [OPTIONS]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--template TEXT` | - | Template to improve |
| `--min-score FLOAT` | `4.0` | Minimum score for reference runs |

**Example:**

```bash
nano-banana suggest-improvements \
    --template baseline \
    --min-score 4.5
```

---

## Utility commands

### validate-logos

Validate a logo kit directory - checks all logos for size, format, and accessibility.

```bash
nano-banana validate-logos --logo-dir PATH
```

**Output includes:**

- Logo names and descriptions
- File sizes
- SHA256 hashes (for tracking reproducibility)

**Example:**

```bash
nano-banana validate-logos --logo-dir logos/default
```

---

### check-auth

Verify Google Cloud OAuth authentication is configured correctly.

```bash
nano-banana check-auth
```

If authentication fails, run:

```bash
gcloud auth application-default login
```

---

### verify-setup

Run complete system verification - checks auth, MLflow, logos, and templates.

```bash
nano-banana verify-setup
```

Use this before your first generation to ensure everything is configured correctly.

---

## Model parameter guide

### Temperature

Controls randomness in generation.

| Value | Behavior | Use case |
|-------|----------|----------|
| `0.0` | Deterministic | Reproducible results |
| `0.4` | Conservative | Consistent outputs |
| `0.8` | Balanced (default) | Good for diagrams |
| `1.2` | Creative | More variation |
| `2.0` | Wild | Maximum creativity |

### Top-p (nucleus sampling)

Controls diversity by limiting cumulative probability.

| Value | Behavior |
|-------|----------|
| `0.5` | More focused |
| `0.95` | Balanced (default) |
| `1.0` | No filtering |

### Top-k

Limits choices to top K tokens.

| Value | Behavior |
|-------|----------|
| `0` | Disabled |
| `40` | Focused |
| `50` | Default |
| `100+` | More diverse |

### Presence/frequency penalty

Reduce repetition in outputs.

| Value | Effect |
|-------|--------|
| `0.0` | No penalty |
| `0.1` | Light penalty (default) |
| `0.5` | Moderate penalty |
| `1.0+` | Strong penalty |

---

## Output directory structure

All outputs are organized by date and run name:

```
outputs/
└── 2026-02-05/
    └── my-diagram/
        ├── prompt.txt              # Full prompt used
        ├── diagram_143052_t08.png  # Image (timestamp_temperature)
        ├── metadata_143052_t08.json
        ├── diagram_143105_t08.png  # Second generation
        ├── metadata_143105_t08.json
        └── feedback_143052.json    # If --feedback enabled
```

---

## Environment variables

Override configuration via environment:

```bash
# Model settings
export NANO_BANANA_VERTEX__MODEL_ID="gemini-4-pro-image"
export NANO_BANANA_VERTEX__TEMPERATURE="0.8"

# MLflow settings
export NANO_BANANA_MLFLOW__TRACKING_URI="databricks"
export NANO_BANANA_MLFLOW__EXPERIMENT_NAME="my-experiment"

# API key (for Gemini)
export GEMINI_API_KEY="your-api-key"

# Databricks (for MLflow tracking)
export DATABRICKS_HOST="https://your-workspace.cloud.databricks.com"
export DATABRICKS_TOKEN="your-token"
```

---

## Common workflows

### Quick diagram generation

```bash
# 1. Create prompt file
cat > prompts/my_diagram.txt << 'EOF'
Create an architecture diagram showing...
EOF

# 2. Generate
nano-banana generate-raw \
    --prompt-file prompts/my_diagram.txt \
    --logo-dir logos/default
```

### Iterative refinement

```bash
# 1. Start chat session
nano-banana chat --prompt-file prompts/diagram.txt

# 2. Review generated image
# 3. Provide feedback: "make logos larger"
# 4. Review new image
# 5. Type "done" when satisfied
```

### Batch generation with feedback

```bash
# Generate multiple and collect scores
nano-banana generate-raw \
    --prompt-file prompts/diagram.txt \
    --count 5 \
    --feedback

# Review each image and score 1-5
# Scores are saved to metadata
```

### Compare templates

```bash
# Generate with different templates
for temp in 0.4 0.8 1.2; do
    nano-banana generate-raw \
        --prompt-file prompts/diagram.txt \
        --temperature $temp \
        --run-name "temp-test-${temp}"
done

# Compare results
nano-banana list-runs --filter "tags.mlflow.runName LIKE 'temp-test%'"
```
