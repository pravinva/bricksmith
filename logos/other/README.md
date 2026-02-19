# Other Tools Logo Kit

Logos for various tools, frameworks, and AI platforms.

## Included Logos

| File | Description | Use Case |
|------|-------------|----------|
| `Claude_AI_symbol.png` | Claude AI (orange/coral symbol) | AI/LLM components |
| `Model_Context_Protocol_logo.png` | MCP (purple logo) | MCP integrations |
| `plotly.png` | Plotly (blue logo) | Data visualization |
| `Python_logo_and_wordmark.png` | Python with text | Python environments |
| `Python-logo-notext.svg.png` | Python icon only | Python without wordmark |

## When to Use This Kit

Use this kit for:
- ✅ AI/ML tool architectures
- ✅ Python-based systems
- ✅ Data visualization pipelines
- ✅ MCP integration diagrams

## Logo Descriptions

When the AI generates diagrams, it uses these descriptions:

| Logo Name | Description in Prompt |
|-----------|----------------------|
| `claude_ai_symbol` | "orange/coral Claude AI symbol" |
| `model_context_protocol_logo` | "purple Model Context Protocol logo" |
| `plotly` | "blue Plotly logo" |
| `python_logo_and_wordmark` | "blue and yellow Python logo with text" |
| `python-logo-notext.svg` | "blue and yellow Python logo without text" |

## Example Diagram Spec

```yaml
name: "ai-data-pipeline"
description: "AI-powered data pipeline with MCP and Claude"

components:
  - id: "python"
    label: "Python Application"
    logo_name: "python_logo_and_wordmark"

  - id: "databricks"
    label: "Databricks"
    logo_name: "databricks-full"

  - id: "claude"
    label: "Claude AI"
    logo_name: "claude_ai_symbol"

  - id: "mcp"
    label: "MCP Server"
    logo_name: "model_context_protocol_logo"

  - id: "plotly"
    label: "Plotly Visualizations"
    logo_name: "plotly"

connections:
  - from_id: "databricks"
    to_id: "python"
    label: "Data Export"

  - from_id: "python"
    to_id: "claude"
    label: "LLM Processing"

  - from_id: "claude"
    to_id: "mcp"
    label: "Tool Calls"
```

## Configuration

```yaml
# configs/ai-tools.yaml
logo_kit:
  logo_dir: "./logos/other"
```

## Usage

```bash
bricksmith generate \
    --config configs/ai-tools.yaml \
    --diagram-spec prompts/diagram_specs/ai-pipeline.yaml \
    --template baseline
```

## Notes

- These logos are for technical architecture diagrams
- Claude AI logo should be used for LLM/AI components
- MCP logo for Model Context Protocol servers/clients
- Python logo available with or without text
- Plotly for data visualization components
