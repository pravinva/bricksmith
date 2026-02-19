# Logo Hints: Automatic Logo-Specific Instructions

## TL;DR

Logo hints automatically inject detailed instructions for logos that AI models commonly misinterpret. Just add a `logo_hints.yaml` file to your logo directory, and bricksmith handles the rest.

## The Problem

Some logos are frequently misinterpreted by AI image generation models:
- **Unity Catalog**: Often rendered as a single hexagon instead of its actual multi-element composition (pink squares + yellow triangles + navy hexagon)
- **Complex logos**: Multi-part logos may be simplified or recreated incorrectly
- **Branded assets**: Logos with specific design requirements that must be pixel-perfect

## The Solution

**Logo hints** provide automatic, per-logo instructions that are injected into every prompt when that logo is detected:

```yaml
# logos/default/logo_hints.yaml
unity-catalog:
  enabled: true
  warning_level: "CRITICAL"
  correct_description: |
    The uploaded Unity Catalog logo file contains MULTIPLE DISTINCT GEOMETRIC SHAPES:
    - Pink/magenta SQUARES (multiple)
    - Yellow/gold TRIANGULAR shapes (multiple)
    - Navy blue HEXAGON (one, in center)
  wrong_patterns:
    - "A single hexagon shape"
    - "A stylized hexagon"
  stop_condition: "If you find yourself drawing ANY hexagon, STOP"
```

## How It Works

1. **Place `logo_hints.yaml`** in your logo directory (e.g., `logos/default/`)
2. **Run any bricksmith command** as usual (generate, chat, refine)
3. **Hints automatically inject** when the logo is detected
4. **Improved logo fidelity** without changing your workflow

## Example Usage

```bash
# No changes needed! Just works automatically:
bricksmith generate-raw --prompt-file prompt.txt --logo-dir logos/default
# Console: "Loaded 7 logos with 3 hints"

bricksmith chat --prompt-file prompt.txt --logo-dir logos/default
# Unity Catalog hints automatically injected on every iteration
```

## Format

Each logo hint has:
- **enabled**: Turn hint on/off
- **warning_level**: CRITICAL (🚨🚨🚨), WARNING (⚠️), or INFO
- **correct_description**: What the logo actually looks like
- **wrong_patterns**: Common mistakes to avoid
- **stop_condition**: Clear instruction to halt incorrect behavior
- **additional_notes**: Extra context

## Verification

When hints load successfully, you'll see:

```
Loading logos from logos/default...
  Loaded 7 logos with 3 hints
```

The hints appear at the top of your prompt:

```
⚠️⚠️⚠️ CRITICAL: LOGO INSTRUCTIONS ⚠️⚠️⚠️

**WHAT THE CORRECT LOGO LOOKS LIKE:**
The uploaded Unity Catalog logo file contains MULTIPLE DISTINCT GEOMETRIC SHAPES...
```

## Key Benefits

✅ **Zero friction** - Works automatically with all commands  
✅ **Consistent** - Same instructions applied every time  
✅ **Maintainable** - Update once, applies everywhere  
✅ **Extensible** - Add hints for any problematic logo  
✅ **Non-invasive** - Doesn't break existing workflows

## Real-World Impact

### Before Logo Hints
❌ Unity Catalog rendered as single hexagon  
❌ Manual prompt editing required  
❌ Inconsistent results across iterations  
❌ No reusable solution

### After Logo Hints
✅ Correct multi-element logo composition  
✅ Zero manual intervention  
✅ Consistent across all commands  
✅ Reusable for all projects

## Commands That Use Logo Hints

Logo hints work automatically with:

- `bricksmith generate-raw` - Raw prompt generation
- `bricksmith chat` - Interactive refinement (every iteration!)
- `bricksmith refine` - Feedback-based refinement
- `bricksmith architect` - Conversational design
- All web API endpoints

## Configuration Files

- **Logo hints**: `logos/{logo_dir}/logo_hints.yaml`
- **Logo files**: `logos/{logo_dir}/*.{png,jpg}`
- **Documentation**: `logos/default/README_LOGO_HINTS.md`

## Adding New Logo Hints

1. Identify a logo that's commonly misinterpreted
2. Edit `logos/default/logo_hints.yaml`
3. Add entry with logo name (without extension)
4. Test with a diagram that uses that logo

```yaml
your-logo-name:
  enabled: true
  warning_level: "CRITICAL"
  correct_description: "Detailed visual description"
  wrong_patterns:
    - "Common mistake 1"
    - "Common mistake 2"
  stop_condition: "What to do if making mistakes"
```

## Technical Architecture

```
┌─────────────────┐
│  bricksmith    │
│  command        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Load logos     │◄──── logos/default/*.png
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Load hints     │◄──── logos/default/logo_hints.yaml
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Build prompt   │
│  + inject hints │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Generate       │
│  diagram        │
└─────────────────┘
```

## FAQs

**Q: Do I need to change my commands?**  
A: No, hints work automatically once the YAML file exists.

**Q: Can I disable hints for specific runs?**  
A: Set `enabled: false` in the YAML, or remove the entry.

**Q: Do hints work with custom logo directories?**  
A: Yes, place `logo_hints.yaml` in any logo directory.

**Q: What if I don't have a hints file?**  
A: The system continues normally without hints (graceful fallback).

**Q: Can I use hints with the chat command?**  
A: Yes! Hints are reapplied on every iteration automatically.

**Q: How do I know if hints are working?**  
A: Check console output: "Loaded X logos with Y hints"

## Related documentation

- [Setup Guide](../SETUP.md) - Complete setup including logo configuration
- [Workflows](../WORKFLOWS.md) - All diagram generation workflows

## Next Steps

1. Review `logos/default/logo_hints.yaml` to see Unity Catalog hints
2. Try generating a diagram with Unity Catalog
3. Add hints for any other problematic logos you encounter
4. Share successful hint configurations with the team!

---

**Status**: ✅ Production Ready  
**Version**: Added in bricksmith 0.2.0+  
**Default Logo Kits with Hints**: `logos/default/`
