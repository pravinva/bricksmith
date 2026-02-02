# Scenario to Diagram Generation - Feature Summary

## Overview

Added AI-powered scenario-to-diagram generation that converts natural language architecture descriptions into structured YAML diagram specifications and optionally generates diagrams immediately.

## What Was Added

### New Module: `scenario_generator.py`

**Location:** `src/nano_banana/scenario_generator.py`

**Key Classes:**
- `ScenarioGenerator` - Main class for generating diagram specs from scenarios

**Key Methods:**
- `generate_spec_from_scenario(scenario, output_path)` - Generate YAML spec from text
- `generate_and_create_diagram(scenario, template, spec_output, run_name)` - Generate spec AND diagram in one step

**How It Works:**
1. Takes natural language scenario description
2. Queries available logos from configured logo kit
3. Uses Gemini AI to analyze scenario and generate structured YAML
4. Validates generated YAML against DiagramSpec model
5. Optionally saves spec to file
6. Optionally generates diagram immediately

### New CLI Commands

#### `scenario-to-spec`

Generate YAML diagram specification from scenario (two-step workflow).

```bash
nano-banana scenario-to-spec \
    --scenario "Build a lakehouse on AWS with Databricks, S3, and Redshift" \
    --output prompts/diagram_specs/my-lakehouse.yaml
```

**Options:**
- `--scenario` (required): Natural language description
- `--output`: Path to save spec (default: auto-generated timestamp)

**Use Case:** When you want to review/edit the spec before generating diagram

#### `generate-from-scenario`

Generate spec AND diagram in one command (one-step workflow).

```bash
nano-banana generate-from-scenario \
    --scenario "Real-time pipeline with Kafka and Spark" \
    --template baseline \
    --run-name "kafka-demo"
```

**Options:**
- `--scenario` (required): Natural language description
- `--template`: Prompt template to use (default: baseline)
- `--save-spec`: Optional path to save the generated spec
- `--run-name`: Optional MLflow run name

**Use Case:** Quick prototyping, demos, exploration

## Documentation Added

### `docs/nano_banana/SCENARIO_TO_DIAGRAM.md`

Comprehensive 400+ line guide covering:
- Quick start examples
- Writing good scenarios (with ✅ good vs ❌ bad examples)
- Command reference
- How it works (architecture analysis)
- Advanced usage (custom logo kits, iterative refinement)
- Example scenarios by use case (lakehouse, streaming, ML, migration, data mesh)
- Troubleshooting
- Best practices

## Updates to Existing Documentation

### `README.md`

Added new section: **"6. Scenario to Diagram Generation ✨ NEW"**
- Explains the feature with example
- Lists use cases (prototyping, learning, demos, exploration)
- Added link to SCENARIO_TO_DIAGRAM.md in documentation section

### `CLAUDE.md`

Added commands to CLI reference:
```bash
# Scenario to diagram generation (NEW)
nano-banana scenario-to-spec --scenario "Build a lakehouse on AWS" --output spec.yaml
nano-banana generate-from-scenario --scenario "Real-time pipeline with Kafka and Spark" --template baseline
```

## Example Usage

### Simple Lakehouse

```bash
nano-banana generate-from-scenario \
    --scenario "Build a lakehouse on AWS with Databricks processing data from S3 to Redshift"
```

**Generated Components:**
- AWS S3 (storage)
- Databricks (service)
- Delta Lake (storage)
- Redshift (storage)
- Appropriate connections with labels

### Real-Time Streaming

```bash
nano-banana scenario-to-spec \
    --scenario "Real-time clickstream analytics with Kafka receiving events,
    Databricks Structured Streaming processing in real-time,
    and Delta Lake storing results" \
    --output prompts/diagram_specs/streaming.yaml
```

**Generated Components:**
- Kafka (service)
- Databricks Structured Streaming (compute)
- Delta Lake (storage)
- Data flow connections

### Migration Scenario

```bash
nano-banana generate-from-scenario \
    --scenario "Migrate from Hadoop to Databricks on GCP with Cloud Storage and BigQuery" \
    --template detailed \
    --save-spec prompts/diagram_specs/migration.yaml \
    --run-name "gcp-migration"
```

## Technical Details

### AI Prompt Structure

The generator creates a structured prompt that:
1. Lists available logos from the configured logo kit
2. Provides the user's scenario
3. Gives explicit instructions for:
   - Component identification
   - Connection types (solid/dashed/dotted)
   - YAML format requirements
   - Naming conventions (snake-case IDs, sentence-case labels)

### Validation

Generated YAML is validated through:
1. YAML syntax parsing (`yaml.safe_load`)
2. Required field checking (name, description, components, connections)
3. Pydantic model validation (`DiagramSpec` model)
4. Error reporting with syntax highlighting

### Integration

- Uses existing `GeminiClient` for text generation
- Leverages existing `LogoKitHandler` for available logos
- Integrates with existing `DiagramRunner` for diagram generation
- Full MLflow tracking for generated diagrams

## Benefits

### For Users

1. **Faster prototyping** - Go from idea to diagram in seconds
2. **Lower barrier to entry** - No need to learn YAML format
3. **Exploration** - Try different architectures quickly
4. **Documentation** - Generate diagrams from meeting notes or requirements

### For Learning

1. **See examples** - Learn YAML format by seeing generated specs
2. **Understand structure** - See how scenarios map to components/connections
3. **Best practices** - Generated specs follow conventions

### For Demos

1. **Live generation** - Create diagrams during customer calls
2. **Quick iterations** - Modify scenario, regenerate immediately
3. **Professional output** - Uses same pipeline as manual specs

## Future Enhancements

Potential improvements:
1. **Multi-turn refinement** - Interactive conversation to refine scenario
2. **Component library** - Suggest additional components based on patterns
3. **Validation rules** - Check for common architecture anti-patterns
4. **Template recommendation** - Suggest best template based on scenario complexity
5. **Batch generation** - Generate multiple variations from one scenario

## Testing

### Manual Verification

```bash
# 1. Check CLI registration
uv run nano-banana --help | grep scenario

# 2. Test scenario-to-spec
uv run nano-banana scenario-to-spec \
    --scenario "Simple lakehouse with Databricks and S3" \
    --output /tmp/test-spec.yaml

# 3. Verify generated YAML
cat /tmp/test-spec.yaml

# 4. Test generate-from-scenario (requires API keys)
uv run nano-banana generate-from-scenario \
    --scenario "Basic data pipeline" \
    --save-spec /tmp/test-generated.yaml
```

## Files Modified/Created

### Created
- ✅ `src/nano_banana/scenario_generator.py` (258 lines)
- ✅ `docs/nano_banana/SCENARIO_TO_DIAGRAM.md` (400+ lines)
- ✅ `SCENARIO_GENERATION_FEATURE.md` (this file)

### Modified
- ✅ `src/nano_banana/cli.py` - Added two new commands (130+ lines)
- ✅ `README.md` - Added feature section and documentation link
- ✅ `CLAUDE.md` - Added CLI command examples

## Summary

This feature transforms Nano Banana from a YAML-first tool to a natural-language-first tool, making it accessible to users who:
- Don't know YAML syntax
- Want to prototype quickly
- Need diagrams during live conversations
- Want to explore architecture patterns

The implementation maintains all existing functionality while adding a new, intuitive interface for diagram generation.
