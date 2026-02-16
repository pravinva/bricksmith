# Prompts Directory

This directory contains all prompt-related resources for nano_banana diagram generation.

## Directory Structure

```
prompts/
├── diagram_specs/       # YAML diagram specifications
├── prompt_templates/    # Reusable prompt templates
├── branding/           # Branding style guides
├── commands/           # Example shell commands
├── migration/          # Migration-specific prompts
├── rfp_response/       # RFP response materials
├── *.txt               # Individual prompt files
├── *.md                # Markdown documentation
└── *.tsv               # Test data files
```

## Diagram Specifications (`diagram_specs/`)

YAML files defining diagram components, connections, and constraints.

### Basic Specification Format

```yaml
name: "architecture-name"
description: "Brief description of the architecture"

components:
  - id: "component-1"
    label: "Display Name"
    type: "service"
    logo_name: "databricks-full"  # Must match logo in logos/ directory
    description: "Component purpose"

connections:
  - from_id: "component-1"
    to_id: "component-2"
    label: "data flow"
    style: "solid"  # or "dashed"
    direction: "right"  # optional

constraints:
  layout: "left-to-right"  # or "top-to-bottom", "concentric", "layered"
  background: "white"
  label_style: "sentence-case"
  spacing: "comfortable"
```

### Example Specifications

- **example_basic.yaml**: Simple architecture with 3-5 components
- **example_complex.yaml**: Complex architecture with multiple layers
- **coles-current-fragmented.yaml**: Current state architecture
- **coles-future-unity-catalog.yaml**: Future state with Unity Catalog

### Usage

```bash
uv run nano-banana generate \
    --diagram-spec prompts/diagram_specs/example_basic.yaml \
    --template baseline \
    --run-name "my-diagram"
```

## Prompt Templates (`prompt_templates/`)

Reusable text templates with variable substitution.

### Template Format

Templates use `{variable}` syntax for substitution:

```
Generate a clean, professional architecture diagram.

{logo_section}

{diagram_section}

Style Requirements:
- Use Databricks color palette
- Clear visual hierarchy
- Professional appearance
```

### Built-in Variables

- `{logo_section}`: Auto-generated logo descriptions and constraints
- `{diagram_section}`: Components, connections from diagram spec
- `{branding_section}`: Branding guidelines (if specified)
- Custom variables: Define in your spec file

### Available Templates

**Standard Templates:**
- `baseline.txt`: Balanced detail, professional styling
- `detailed.txt`: Comprehensive, high detail
- `minimal.txt`: Clean, simplified overview

**Specialized Templates:**
- `agl_concentric.txt`: Concentric ring layout for AGL
- `agl_v6_suite/`: Six presentation styles for AGL diagrams
- `synapse_migration.md`: Migration diagram template

### Usage

```bash
# Use with diagram spec
uv run nano-banana generate \
    --diagram-spec prompts/diagram_specs/my_spec.yaml \
    --template baseline

# Use directly with raw generation
uv run nano-banana generate-raw \
    --prompt-file prompts/prompt_templates/minimal.txt \
    --logo logos/default/databricks-full.png
```

## Individual Prompt Files

Standalone prompt files for raw generation without diagram specs.

### Format

```
ARCHITECTURE DIAGRAM: Current State - Fragmented Data

Create a professional architecture diagram showing...

COMPONENTS:
1. Multiple data sources (left side)
2. Processing layer (center)
3. Multiple destinations (right side)

VISUAL REQUIREMENTS:
- Left-to-right flow
- Clear data paths
- Highlight fragmentation issues
- Use provided logos exactly as given
```

### Key Files

- `coles_current_fragmented_state.txt`: Coles current architecture
- `coles_future_unity_catalog.txt`: Coles target architecture
- `living_intelligence.txt`: Living Intelligence Platform diagram
- `agl_zerobus_business_architecture.txt`: AGL Zerobus **business/executive** overview (5–7 zones, capability-level; derived from technical chat session)

### Usage

```bash
uv run nano-banana generate-raw \
    --prompt-file prompts/coles_current_fragmented_state.txt \
    --logo logos/default/databricks-full.png \
    --logo logos/default/delta.png \
    --run-name "coles-current"
```

## Branding (`branding/`)

Style guides and branding requirements for consistent diagram appearance.

### Files

- `minimal.txt`: Minimal branding, clean aesthetic
- `data_platform_best_practices.txt`: Data platform styling guidelines
- `agl.txt`: AGL-specific branding requirements

### Usage

Branding files can be included in prompts or referenced in templates:

```
{branding_section}

Follow the branding guidelines above for all visual elements.
```

## Commands (`commands/`)

Example shell scripts showing common generation workflows.

### Files

- `agl_simplified.sh`: Generate simplified AGL diagram
- `agl_synapse_migration.sh`: Generate migration diagram
- `full_arch_agl.sh`: Generate comprehensive AGL architecture

### Usage

```bash
chmod +x prompts/commands/agl_simplified.sh
./prompts/commands/agl_simplified.sh
```

## Migration (`migration/`)

Prompts specifically for migration and transformation diagrams.

### Files

- `agl_synapse_simple_v2.md`: Simplified Synapse migration
- `agl_synapse_pro_v2_12mo.md`: Detailed 12-month migration plan

### Usage

These prompts show before/after states and migration paths:

```bash
uv run nano-banana generate-raw \
    --prompt-file prompts/migration/agl_synapse_simple_v2.md \
    --logo logos/azure/Microsoft_Azure.png \
    --logo logos/default/databricks-full.png
```

## RFP Response (`rfp_response/`)

Structured response materials for RFP proposals.

### Structure

```
rfp_response/
├── architecture/        # Architecture-specific content
├── current_state.md    # Current state analysis
├── future_state.md     # Proposed future state
├── proposed_architecture.md  # Architecture proposal
└── technology_response.md    # Technical response
```

### Usage

Reference these documents when creating customer-facing diagrams:

```bash
# Generate architecture for proposal
uv run nano-banana generate-raw \
    --prompt-file prompts/rfp_response/proposed_architecture.md
```

## Test Data

- `*.tsv` files: Test data for evaluation and analysis
- Used for prompt optimization and quality testing

## Best Practices

### Creating New Diagram Specs

1. **Start with an example**: Copy `example_basic.yaml`
2. **Define components clearly**: Use descriptive IDs and labels
3. **Specify logo names**: Must match files in `logos/` directory
4. **Add constraints**: Be explicit about layout and styling
5. **Test incrementally**: Start simple, add complexity

### Writing Effective Prompts

1. **Be specific**: Provide clear, detailed requirements
2. **Use structure**: Organize with headers and sections
3. **Reference examples**: Link to successful previous outputs
4. **Include constraints**: Specify must-have requirements
5. **Iterate**: Refine based on results

### Organizing Your Prompts

1. **Use descriptive names**: `customer-usecase-version.yaml`
2. **Group by purpose**: Keep related prompts together
3. **Version control**: Track changes and improvements
4. **Document success**: Note what worked well
5. **Share learnings**: Contribute successful patterns back

## Examples

### Example 1: Generate from Spec

```bash
uv run nano-banana generate \
    --diagram-spec prompts/diagram_specs/coles-future-unity-catalog.yaml \
    --template baseline \
    --run-name "coles-unity-future"
```

### Example 2: Raw Generation with Custom Prompt

```bash
uv run nano-banana generate-raw \
    --prompt-file prompts/coles_current_fragmented_state.txt \
    --logo logos/default/databricks-full.png \
    --logo logos/default/delta.png \
    --logo logos/default/unity-catalog.png \
    --run-name "coles-current"
```

### Example 3: Use Template with Branding

```bash
uv run nano-banana generate \
    --diagram-spec prompts/diagram_specs/my_spec.yaml \
    --template prompts/prompt_templates/minimal.txt \
    --branding prompts/branding/minimal.txt \
    --run-name "branded-diagram"
```

## Contributing

When adding new prompts:

1. Follow the established directory structure
2. Use clear, descriptive filenames
3. Include documentation in README sections
4. Test thoroughly before committing
5. Update this README with new content

See `CONTRIBUTING.md` for detailed guidelines.

## Resources

- [Main README](../README.md)
- [Workflows Guide](../docs/WORKFLOWS.md)
- [Best Practices](../docs/BEST_PRACTICES.md)
- [Prompt Engineering Guide](../docs/nano_banana/PROMPT_ENGINEERING.md)
- [Logo Setup](../logos/README.md)
