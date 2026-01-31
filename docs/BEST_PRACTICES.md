# Best Practices for Architecture Diagram Generation

This guide compiles best practices learned from generating high-quality architecture diagrams with nano_banana.

## Prompt Engineering Best Practices

### Structure Your Prompts

**Good Structure:**
```
1. High-level context
2. Specific components and their relationships
3. Visual styling requirements
4. Logo placement instructions
5. Layout constraints
```

**Poor Structure:**
- Wall of text without clear sections
- Missing visual guidance
- Ambiguous relationships
- No layout specifications

### Be Explicit About Layout

**Good:**
```
"Arrange components left-to-right showing data flow from sources to destinations.
Use three clear horizontal layers: ingestion, processing, serving."
```

**Poor:**
```
"Show the components in a logical way."
```

### Specify Component Relationships Clearly

**Good:**
```
"Data flows from Azure Blob Storage → Databricks → Unity Catalog → Power BI.
Show bidirectional sync between Unity Catalog and external metastore."
```

**Poor:**
```
"Connect the components appropriately."
```

## Logo Management Best Practices

### Logo Selection Strategy

1. **Primary Platform Logos**: Use full color, official versions
   - `databricks-full.png` for Databricks platform
   - `unity-catalog.png` for Unity Catalog features

2. **Technology Logos**: Use consistent style (all color or all monochrome)
   - Match the diagram's color scheme
   - Maintain consistent sizing

3. **Custom/Partner Logos**: Store in dedicated kit directories
   - `logos/agl/` for AGL-specific diagrams
   - `logos/aws/`, `logos/azure/`, `logos/gcp/` for cloud providers

### Logo Placement

**Best Practices:**
- Place logos near their corresponding components
- Use consistent sizing across similar component types
- Avoid overlapping logos with text or connections
- Maintain adequate whitespace around logos

**Common Issues:**
- ❌ Logos too large, dominating the diagram
- ❌ Inconsistent logo sizes for similar components
- ❌ Logos obscuring important connections
- ✅ Properly scaled, clearly visible, well-positioned logos

## Template Selection Guide

### Baseline Template
**Use when:**
- Creating standard architecture diagrams
- Need clean, professional output
- Following Databricks branding guidelines
- First iteration of a new diagram

**Characteristics:**
- Moderate detail level
- Balanced styling
- Professional appearance
- Good starting point

### Detailed Template
**Use when:**
- Complex architectures with many components
- Need to show intricate relationships
- Technical audience expecting specificity
- Final polished diagrams

**Characteristics:**
- High detail level
- Comprehensive annotations
- Dense information
- May require larger canvas

### Minimal Template
**Use when:**
- Executive presentations
- Simplified overviews
- Highlighting key concepts only
- Quick mockups or drafts

**Characteristics:**
- Clean, uncluttered
- Essential components only
- High-level relationships
- Easy to understand at a glance

## Branding Best Practices

### Color Schemes

**Databricks Palette:**
- Primary: `#FF3621` (Databricks red)
- Secondary: `#00A972` (green)
- Neutral: `#1B3139` (dark blue-gray)
- Backgrounds: White or very light gray

**When to Deviate:**
- Customer-specific branding requirements
- Industry-standard color coding (e.g., red=critical, green=healthy)
- Accessibility considerations

### Typography

**Best Practices:**
- Use sentence case for labels: "Data ingestion layer"
- Avoid ALL CAPS except for acronyms: "ETL with Unity Catalog"
- Keep labels concise: 3-5 words maximum
- Use consistent font sizing for hierarchy

**Common Issues:**
- ❌ Inconsistent capitalization
- ❌ Labels too long, wrapping awkwardly
- ❌ Font sizes too small to read
- ✅ Clear, readable, consistently formatted text

## Diagram Types and Patterns

### Data Flow Diagrams

**Structure:**
```
Sources → Processing → Storage → Consumption
```

**Best Practices:**
- Show clear directional flow (left-to-right or top-to-bottom)
- Group related components
- Distinguish between data types (streaming vs. batch)
- Show data transformation stages

### Architecture Overview Diagrams

**Structure:**
```
Concentric circles or layered rectangles showing:
- Core platform (center/bottom)
- Services and capabilities (middle)
- Integrations and endpoints (outer/top)
```

**Best Practices:**
- Organize by architectural layer
- Show clear boundaries between layers
- Indicate primary and secondary relationships
- Highlight key capabilities

### Migration/Transformation Diagrams

**Structure:**
```
Before State → Migration Path → After State
```

**Best Practices:**
- Use visual differentiation (color, style) for before/after
- Show migration steps clearly
- Indicate what's changing vs. staying the same
- Highlight benefits of the future state

## Quality Assurance Checklist

Before finalizing a diagram, verify:

### Logo Fidelity (Critical)
- [ ] All logos are unmodified official versions
- [ ] No filenames visible in the diagram
- [ ] Logos are appropriately sized and positioned
- [ ] Logo quality is crisp and clear

### Layout Clarity
- [ ] Components are logically organized
- [ ] Flow direction is clear and consistent
- [ ] Related items are grouped appropriately
- [ ] Adequate whitespace between elements
- [ ] No overlapping elements or connections

### Text Legibility
- [ ] All labels are readable at intended viewing size
- [ ] Consistent capitalization throughout
- [ ] No spelling errors
- [ ] Font sizing creates clear hierarchy
- [ ] Text doesn't overlap with graphics

### Constraint Compliance
- [ ] Follows specified layout requirements
- [ ] Adheres to branding guidelines
- [ ] Matches diagram spec exactly
- [ ] Meets customer-specific requirements

## Common Anti-Patterns to Avoid

### Over-Complexity
**Problem:** Trying to show everything in one diagram
**Solution:** Create multiple focused diagrams, each telling one story

### Inconsistent Styling
**Problem:** Mixing different visual styles, colors, or treatments
**Solution:** Establish style guide upfront, apply consistently

### Unclear Data Flow
**Problem:** Ambiguous or contradictory flow arrows
**Solution:** Use clear directional arrows, label flows explicitly

### Logo Soup
**Problem:** Too many logos crowding the diagram
**Solution:** Use logos strategically, represent similar items with one logo

### Text Overload
**Problem:** Walls of text, tiny fonts, excessive annotations
**Solution:** Keep text minimal, let the visual do the work

## Iteration Strategy

### First Pass: Structure
Focus on:
- Component placement
- Overall layout
- Major relationships
- Basic styling

Don't worry about:
- Fine details
- Perfect colors
- Exact logo positioning

### Second Pass: Refinement
Focus on:
- Logo placement and sizing
- Connection styling
- Text clarity and hierarchy
- Color consistency

### Third Pass: Polish
Focus on:
- Final visual tweaks
- Consistency check
- Constraint compliance
- Customer-specific requirements

### When to Stop Iterating
- Meets all quality checklist items
- Stakeholders approve
- No obvious improvements needed
- Diminishing returns on further changes

## Scaling for Different Audiences

### Executive Presentations
- Minimal detail, clear story
- Focus on business outcomes
- Use analogies and familiar concepts
- Large, readable elements

### Technical Deep-Dives
- Comprehensive detail
- Show implementation specifics
- Include technical annotations
- Assume technical knowledge

### Customer Proposals
- Balance detail with clarity
- Highlight customer-specific elements
- Show clear value proposition
- Professional, polished appearance

### Internal Documentation
- Functional over pretty
- Include implementation notes
- Show technical constraints
- Link to additional resources

## Performance Optimization

### Reduce Generation Time
- Use simpler prompts for initial iterations
- Lower temperature settings (0.4-0.6)
- Reuse successful prompt patterns
- Cache logo conversions when possible

### Improve Output Quality
- Higher temperature (0.7-0.9) for creativity
- More detailed prompts with examples
- Iterate with specific feedback
- Reference successful outputs

### Batch Processing
- Group similar diagrams together
- Use consistent templates for a session
- Prepare all specs before starting
- Parallelize when model capacity allows

## Documentation and Knowledge Sharing

### Document Successful Patterns
When a diagram works well:
1. Save the prompt to template library
2. Note what made it successful
3. Tag with relevant metadata
4. Share with team

### Build a Pattern Library
Organize by:
- Diagram type (flow, architecture, migration)
- Industry or customer
- Complexity level
- Template used

### Team Collaboration
- Establish naming conventions
- Share MLflow workspace
- Conduct prompt reviews
- Create style guides

## Continuous Improvement

### Track Metrics
- Time to generate acceptable output
- Number of iterations needed
- Evaluation scores
- Stakeholder feedback

### Learn from Feedback
- Document what didn't work
- Iterate on prompt patterns
- Refine templates based on results
- Update best practices regularly

### Stay Current
- Monitor model improvements
- Experiment with new features
- Adapt to changing requirements
- Share learnings with community
