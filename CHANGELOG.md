# Changelog

All notable changes to the nano_banana project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Conversational diagram generation with iterative refinement
- Scenario-to-diagram feature for rapid prototyping
- Multi-logo kit support with organized directory structure
- Raw prompt generation with custom logo selection
- Enhanced CLI commands for conversation and scenario workflows
- Comprehensive documentation (WORKFLOWS.md, BEST_PRACTICES.md, TROUBLESHOOTING.md)
- Visual refinement quickstart guide
- Authentication documentation
- Prompt refinement capabilities with quality scoring
- Logo kits documentation with usage examples

### Changed
- Reorganized examples/ into prompts/ directory for better clarity
- Moved logo_kit/ to logos/ with multi-kit support
- Updated all configuration files to reference new directory structure
- Enhanced prompt builder for flexible template handling
- Improved runner with support for multiple generation modes
- Updated CLI with additional commands and options
- Refined data models to support conversation state

### Removed
- Deprecated icons directory
- Old AGL-specific examples (moved to prompts/)
- Outdated RFP response examples (moved to prompts/)

## [0.2.0] - 2026-01-30

### Added
- Logo compositor for image processing
- Prompt development utilities
- MCP enrichment capabilities (manual and automatic)
- DSPy optimizer for automated prompt engineering
- Scenario generator module
- Enhanced MLflow integration with detailed tracking
- Template-based prompt generation system
- Multiple branding options (minimal, detailed, custom)

### Changed
- Improved logo validation and SHA256 tracking
- Enhanced evaluation rubric with four-dimension scoring
- Updated Gemini client with better error handling
- Refined configuration system with environment variable support

## [0.1.0] - 2026-01-21

### Added
- Initial project setup with uv dependency management
- Core data models using Pydantic
- Configuration system with YAML and environment variable support
- Logo management with validation and tracking
- Template-based prompt builder with variable substitution
- Google AI Gemini client integration
- Vertex AI client for diagram generation
- Databricks MLflow tracking integration
- Manual evaluation interface with rubric-based scoring
- Cross-run prompt performance analysis
- Click-based CLI with multiple commands
- Pipeline orchestrator for diagram generation workflow
- Comprehensive documentation and guides
- Example diagram specifications and prompt templates
- Logo kit with validated brand assets
- Environment-specific configuration files

### Documentation
- Project README with overview and quick start
- CLAUDE.md with development patterns and architecture
- PRD with detailed project requirements
- Logo setup and quick start guides
- Prompt engineering documentation
- Guaranteed constraints and safety documentation
- Quick start and usage guides

## [0.0.1] - 2026-01-18

### Added
- Initial repository structure
- Python package configuration with pyproject.toml
- Basic .gitignore for Python projects
- Environment file template (.env.example)
- License and basic documentation

---

## Release Notes

### Version 0.2.0 Highlights

This release focuses on extensibility and user experience improvements:

**Conversational Workflows**: Generate diagrams through natural language conversations, refining based on feedback iteratively.

**Multi-Kit Logo Management**: Organize logos by customer, cloud provider, or use case for better reusability.

**Scenario Generation**: Rapidly prototype multiple diagram variations from a single scenario description.

**Enhanced Documentation**: Comprehensive guides for workflows, best practices, and troubleshooting.

### Version 0.1.0 Highlights

First stable release with core functionality:

**Template-Based Generation**: Create professional architecture diagrams from YAML specifications.

**Logo Fidelity**: Automated constraint enforcement ensures exact logo reuse without modifications.

**MLflow Tracking**: Full experiment tracking with Databricks integration for reproducibility.

**Evaluation Framework**: Manual scoring system with four-dimension rubric for quality assessment.

**Prompt Analysis**: Cross-run analysis to identify successful prompt patterns.

---

## Migration Guides

### Upgrading from 0.1.x to 0.2.x

1. **Directory Restructuring**:
   ```bash
   # Old structure
   examples/logo_kit/
   examples/prompt_templates/
   examples/diagram_specs/
   
   # New structure
   logos/default/
   prompts/prompt_templates/
   prompts/diagram_specs/
   ```

2. **Update Configuration**:
   Edit `configs/default.yaml` to reference new paths:
   ```yaml
   logo_kit:
     directory: "logos/default"
   ```

3. **Update Scripts**:
   Replace references to `examples/` with `prompts/` in any custom scripts.

4. **Logo Management**:
   If using custom logos, organize into appropriate kit directory:
   ```bash
   mkdir -p logos/custom
   mv my-logos/* logos/custom/
   ```

5. **Authentication**:
   Refresh Databricks authentication if needed:
   ```bash
   databricks auth login <workspace-url> --profile=<profile>
   ```

See `EXAMPLES_TO_PROMPTS_MIGRATION.md` for detailed migration instructions.

---

## Deprecation Notices

### Deprecated in 0.2.0
- Direct file paths to `examples/` directory (use `prompts/` instead)
- Single logo kit approach (use multi-kit structure)

### To Be Deprecated in 0.3.0
- Legacy prompt template format without variable substitution
- Direct Vertex AI client usage (will be unified with Gemini client)

---

## Roadmap

### Planned for 0.3.0
- Automated evaluation using AI models
- Batch diagram generation workflows
- Template gallery and sharing
- Enhanced conversation capabilities with memory
- Integration with additional diagram tools
- Performance optimizations for large-scale generation

### Future Considerations
- Real-time collaboration features
- Version control for diagram iterations
- Custom plugin system for diagram processors
- Integration with presentation tools
- Automated diagram testing framework

---

## Contributors

Thank you to everyone who has contributed to nano_banana!

For contribution guidelines, see `CONTRIBUTING.md`.

---

## Links

- [Documentation](docs/)
- [Project README](README.md)
- [Issue Tracker](#)
- [Discussions](#)
