# Task: Refactor bricksmith to minimal viable state

## Objective

Clean up the bricksmith/bricksmith codebase by removing the broken YAML spec workflow, consolidating 32+ documentation files into a clear structure, and ensuring the three primary workflows (generate-raw, architect, chat) work correctly with proper documentation.

## Context

Read these files to understand the current state:
- `src/bricksmith/cli.py` - Main CLI entry point with all commands
- `src/bricksmith/models.py` - Data models including DiagramSpec (to be removed)
- `src/bricksmith/prompts.py` - Prompt building (has DiagramSpec dependencies)
- `src/bricksmith/runner.py` - Diagram runner (DiagramSpec heavy)
- `README.md` - Current documentation (needs simplification)
- `CLAUDE.md` - Project guide (needs updating after refactor)
- `docs/bricksmith/AUTHENTICATION.md` - Auth setup (keep)
- `docs/bricksmith/CLI_REFERENCE.md` - CLI docs (needs trimming)

Check recent changes:
```bash
git log --oneline -10
```

## Technical constraints

- Use `uv` for all Python operations (not pip)
- Keep MLflow tracking working for all generation commands
- Preserve the Gemini API integration (gemini_client.py)
- Do not break the web interface (web/ directory)
- Keep logo handling system intact (logos.py)
- Tests should pass after each major change: `uv run pytest`
- Linting must pass: `uv run ruff check src/`

## Requirements

### Phase 1: Code cleanup - remove YAML spec workflow

1. Remove the `generate` CLI command (YAML spec-based generation)
2. Remove `scenario-to-spec` and `generate-from-scenario` CLI commands
3. Remove `DiagramSpec` model from models.py (keep other models)
4. Remove `scenario_generator.py` module
5. Clean up `prompts.py` to remove DiagramSpec dependencies
6. Clean up `runner.py` - either remove or simplify for generate-raw only
7. Remove `prompts/diagram_specs/` directory
8. Remove `prompts/prompt_templates/` directory (if exists)
9. Update CLI Context class to remove unused components

### Phase 2: Remove unused analysis commands

1. Review and potentially remove these commands if they don't work:
   - `analyze-prompts`
   - `suggest-improvements`
   - `template-stats`
   - `dimension-stats`
   - `compare-diagrams`
2. Keep these evaluation commands:
   - `evaluate` (if it works with generate-raw)
   - `list-runs`
   - `show-run`

### Phase 3: Documentation consolidation

1. **Keep these docs** (move to docs/ root if needed):
   - AUTHENTICATION.md - essential for setup
   - One quickstart guide (consolidate from multiple)

2. **Delete these docs** (obsolete or redundant):
   - docs/bricksmith/SCENARIO_TO_DIAGRAM.md (feature removed)
   - docs/SCENARIO_GENERATION_FEATURE.md (feature removed)
   - docs/bricksmith/PROMPT_DEVELOPMENT_GUIDE.md (YAML spec related)
   - docs/bricksmith/LOGO_KITS.md (redundant with LOGO_SETUP)
   - docs/bricksmith/LOGO_QUICK_START.md (redundant)
   - docs/bricksmith/API_KEY_SETUP_SUMMARY.md (redundant with AUTH)
   - docs/bricksmith/GUARANTEED_CONSTRAINTS.md (internal)
   - docs/bricksmith/SAFETY_GUARANTEE.md (internal)
   - docs/bricksmith/SPELLING_CORRECTION_SUMMARY.md (internal)
   - docs/EXAMPLES_TO_PROMPTS_MIGRATION.md (obsolete)
   - docs/LOGO_UPDATE_SUMMARY.md (obsolete)
   - docs/PRD.md (move to archive or delete)
   - docs/START_HERE.md (superseded by README)

3. **Consolidate into these final docs**:
   - `README.md` - Quick start + overview (simplified)
   - `docs/SETUP.md` - Full setup (auth + logos)
   - `docs/WORKFLOWS.md` - The 3 workflows: generate-raw, architect, chat
   - `docs/TROUBLESHOOTING.md` - Keep but update
   - `docs/WEB_INTERFACE.md` - Keep for web deployment

4. **Update CLAUDE.md** to reflect new structure

### Phase 4: Update README.md

Create a new simplified README with:
1. One-paragraph description
2. Quick start (5 commands max)
3. Three workflows with examples
4. Link to detailed docs

### Phase 5: Verify everything works

1. Test generate-raw: `bricksmith generate-raw --help`
2. Test architect: `bricksmith architect --help`
3. Test chat: `bricksmith chat --help`
4. Run full test suite
5. Verify MLflow tracking still works

## Completion criteria

The task is COMPLETE when ALL of these are true:
- [ ] `generate` command removed from CLI
- [ ] `scenario-to-spec` and `generate-from-scenario` removed
- [ ] DiagramSpec model removed from models.py
- [ ] scenario_generator.py deleted
- [ ] prompts/diagram_specs/ directory deleted
- [ ] Docs reduced from 32+ files to ~5 essential files
- [ ] README.md simplified to <200 lines
- [ ] CLAUDE.md updated to reflect new structure
- [ ] `bricksmith generate-raw --help` works
- [ ] `bricksmith architect --help` works
- [ ] `bricksmith chat --help` works
- [ ] All tests pass: `uv run pytest`
- [ ] No linting errors: `uv run ruff check src/`

## Instructions

1. Read the context files listed above to understand current state
2. Start with Phase 1 (code cleanup) - remove DiagramSpec and related code
3. Run tests after each file change to catch breakages early
4. Proceed to Phase 2 (remove unused commands)
5. Move to Phase 3 (documentation consolidation)
6. Update README.md (Phase 4)
7. Final verification (Phase 5)
8. Commit changes with clear, descriptive messages

When ALL completion criteria are verified, output:
<promise>TASK COMPLETE</promise>

IMPORTANT:
- Only output the promise when you have VERIFIED all criteria
- Do NOT output the promise prematurely
- If stuck after multiple attempts, document blockers in a BLOCKERS.md file
- Run tests frequently to catch regressions early
- Make small, incremental commits
