# Collaborative architecture design

The `nano-banana architect` command provides an interactive conversation with an AI solutions architect. Instead of writing a prompt from scratch, you describe your problem and discuss the architecture through natural back-and-forth dialogue. When the design is ready, the AI generates a high-quality diagram prompt.

## How it works

1. **Describe your problem** - Explain what system you need to design
2. **Discuss architecture** - AI asks clarifying questions, proposes solutions
3. **Refine through conversation** - Iterate until the design is solid
4. **Generate prompt** - AI creates a diagram prompt for `generate-raw`

## Quick start

```bash
# Start interactively - you'll be prompted for the problem
nano-banana architect

# Start with a problem description
nano-banana architect --problem "Build a real-time analytics pipeline for IoT data"

# With custom context about the customer/domain
nano-banana architect \
    --problem "Migrate from Snowflake to Databricks" \
    --context prompts/context/customer_background.md

# Use an existing diagram prompt as reference
nano-banana architect \
    --problem "Similar diagram for ANZ Bank" \
    --reference-prompt prompts/coles_semantic_fragmentation.md
```

## Command options

| Option | Default | Description |
|--------|---------|-------------|
| `--problem` | - | Initial problem description (or enter interactively) |
| `--logo-dir` | from config | Logo directory to use |
| `--context` | - | Custom context file with domain knowledge |
| `--reference-prompt` | - | Existing diagram prompt to use as reference for style/structure |
| `--output-format` | prompt | Output: 'prompt' for generate-raw or 'spec' for YAML |
| `--output-file` | - | Save output to specific file |
| `--max-turns` | 20 | Maximum conversation turns |
| `--dspy-model` | databricks-claude-opus-4-5 | Databricks model for DSPy |
| `--name` | - | Session name for output directory |

## Conversation commands

During the conversation, you can use these commands:

| Command | Action |
|---------|--------|
| Natural text | Continue discussing architecture |
| `output` or `generate` | Generate the diagram prompt |
| `status` | Show current architecture state (components, connections) |
| `done` | Save session and exit |

## Example conversation

```
$ nano-banana architect --problem "Coles needs to migrate from Snowflake to Databricks Lakehouse"

Session started: coles-migration

Architect:
I'd like to understand your migration requirements better. Let me ask a few questions:

1. What's the current data volume in Snowflake (TB/PB)?
2. Are there specific workloads - ETL, reporting, ML - that need to migrate?
3. What's the timeline for migration?
4. Are there any existing Azure services in the stack?

You: We have about 50TB of data. Main workloads are ETL from SAP and POS systems,
     reporting through Power BI, and some ML for demand forecasting.

Architect:
Got it - 50TB with ETL, BI, and ML workloads. That's a great fit for Databricks Lakehouse.

Based on this, I'm thinking:
- **Bronze layer**: Raw data ingestion from SAP ERP and POS systems
- **Silver layer**: Cleaned, conformed tables with Delta Lake
- **Gold layer**: Business-ready aggregates for Power BI and ML
- **Unity Catalog**: Central governance across all layers

Should I add Unity Catalog for governance? And do you want to keep Power BI
or consider migrating to Databricks SQL?

You: Yes, Unity Catalog is essential. Keep Power BI for now.

Architect:
I've updated the architecture:

Components:
  - SAP ERP (source)
  - POS Systems (source)
  - Databricks Lakehouse (databricks logo)
  - Unity Catalog (unity-catalog logo)
  - Power BI (powerbi logo)

Connections:
  - SAP ERP → Bronze Layer: Raw ingestion
  - POS → Bronze Layer: Raw ingestion
  - Bronze → Silver: Transformation
  - Silver → Gold: Aggregation
  - Gold → Power BI: BI queries

I believe we have enough to generate a diagram. Type 'output' when ready.

You: output

Generating diagram prompt...

Output saved to: outputs/2026-02-03/architect-coles-migration/
  ├── session.json
  ├── prompt.txt
  ├── architecture.json
  └── rationale.txt

Next steps:
  nano-banana generate-raw --prompt-file outputs/2026-02-03/architect-coles-migration/prompt.txt
```

## Adding custom context

Use `--context` to provide domain knowledge that helps the AI make better suggestions:

```bash
nano-banana architect \
    --problem "Design a data mesh for the retail team" \
    --context prompts/context/retail_domain.md
```

The context file can include:
- Customer background and industry
- Existing technology stack
- Compliance requirements
- Architectural constraints
- Team structure and ownership

## Using a reference prompt

Use `--reference-prompt` to base your new diagram on an existing prompt's style and structure:

```bash
nano-banana architect \
    --problem "Create similar architecture for Woolworths" \
    --reference-prompt prompts/coles_semantic_fragmentation.md
```

This is useful when you want to:
- Create a variant of an existing diagram for a different customer
- Maintain consistent style across multiple diagrams
- Learn from a well-structured prompt
- Adapt an existing architecture to new requirements

The AI will extract components, connections, and design patterns from the reference and use them as inspiration for the new architecture.

## Output files

Each session creates a directory in `outputs/<date>/architect-<session-id>/`:

| File | Contents |
|------|----------|
| `session.json` | Full conversation history with all turns |
| `prompt.txt` | Generated diagram prompt for `generate-raw` |
| `architecture.json` | Final architecture state (components, connections) |
| `rationale.txt` | AI's explanation of the prompt structure |

## Integration with other commands

After an architect session:

```bash
# Generate the diagram
nano-banana generate-raw \
    --prompt-file outputs/2026-02-03/architect-session/prompt.txt \
    --logo-dir logos/default

# Or continue refining with the chat command
nano-banana chat \
    --prompt-file outputs/2026-02-03/architect-session/prompt.txt

# View the generated diagram and provide feedback
nano-banana evaluate <run-id>
```

## Tips for effective sessions

1. **Be specific about requirements** - The more context you provide, the better the architecture suggestions
2. **Ask for alternatives** - "What if we used Kafka instead of direct ingestion?"
3. **Check status frequently** - Use `status` to see the current architecture state
4. **Iterate before output** - Refine the design through conversation before generating the prompt
5. **Use context files** - For customer-specific sessions, include background in a context file

## Architecture tracking

The AI tracks components and connections as you discuss. Each component includes:

- **id**: Unique identifier
- **label**: Display name for the diagram
- **type**: Component type (service, storage, external, compute, network)
- **logo_name**: Reference to available logo

Connections include:
- **from_id**: Source component
- **to_id**: Target component
- **label**: Description of the data flow
