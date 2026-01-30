# Examples to Prompts Migration Summary

## What Changed

The `examples/` directory has been removed and all its content has been consolidated into the `prompts/` directory.

## Directory Structure

### Before
```
examples/
├── diagram_specs/
│   └── example_basic.yaml
├── prompt_templates/
│   └── baseline.txt
└── README.md
```

### After
```
prompts/
├── diagram_specs/          # Diagram specifications (YAML)
│   ├── example_basic.yaml  # ✅ Updated with correct logo names
│   ├── all_logos_example.yaml
│   ├── agl_*.yaml
│   └── ... (many more)
│
├── prompt_templates/       # Prompt templates (TXT/MD)
│   ├── baseline.txt
│   ├── detailed.txt
│   ├── minimal.txt
│   ├── agl_*.txt
│   └── ... (many more)
│
├── branding/              # Branding-specific prompts
├── commands/              # Shell scripts for common operations
├── migration/             # Migration-related files
└── rfp_response/          # RFP response data
```

## Files Updated

### Python Source Code
- ✅ `src/nano_banana/prompts.py` - Changed default template directory from `examples/prompt_templates` to `prompts/prompt_templates`
- ✅ `src/nano_banana/config.py` - Changed default logo directory from `examples/logo_kit` to `logos/default`
- ✅ `src/nano_banana/prompt_dev.py` - Updated logo kit path
- ✅ `src/nano_banana/cli.py` - Updated all example paths in help text and defaults

### Configuration Files
- ✅ `configs/local.yaml` - Changed `logo_dir: "./examples/logo_kit"` to `"./logos/default"`
- ✅ `configs/databricks.yaml` - Changed `logo_dir: "./examples/logo_kit"` to `"./logos/default"`

### Documentation
- ✅ `README.md` - Updated all `examples/` references to `prompts/`
- ✅ `CLAUDE.md` - Updated all paths and examples
- ✅ `docs/nano_banana/*.md` (13 files) - Bulk updated all references
- ✅ `logos/*/README.md` - Updated logo kit documentation

### Scripts
- ✅ `prompts/commands/*.sh` (4 files) - Updated all command scripts

### Diagram Specs
- ✅ `prompts/diagram_specs/example_basic.yaml` - Updated logo names to match actual files:
  - `databricks` → `databricks-full`
  - `delta-lake` → `delta`
  - `uc` → `unity-catalog`

## Key Improvements

1. **Consolidation** - All prompts, templates, and specifications now live in one place
2. **Consistency** - Logo kit references now correctly point to `logos/default/`
3. **Clarity** - The `prompts/` directory now serves as the single source of truth for all prompt-related content
4. **Organization** - Better structure with subdirectories for different types of content

## Usage Examples

### Before (deprecated)
```bash
nano-banana generate \
    --diagram-spec examples/diagram_specs/example_basic.yaml \
    --template baseline
```

### After (current)
```bash
nano-banana generate \
    --diagram-spec prompts/diagram_specs/example_basic.yaml \
    --template baseline
```

## Verification

All changes have been tested:
- ✅ CLI still works (`nano-banana --help`)
- ✅ Key files exist (`prompts/diagram_specs/example_basic.yaml`, `prompts/prompt_templates/baseline.txt`)
- ✅ No dangling references to `examples/` directory (verified with grep)
- ✅ Default paths updated in code

## Migration Complete

The `examples/` directory has been completely removed and all functionality has been preserved under `prompts/`.
