"""Manual MCP-based context enrichment for diagram prompts.

This version provides helpers for manually enriching prompts with
Databricks documentation context. Use this when working with Claude Code
to have it fetch context for you.
"""

from typing import Optional

from .models import DiagramSpec, Component


class ManualMCPEnricher:
    """Helper for manually enriching diagram specifications with context.

    This class identifies which components need context and provides
    helpers to format that context once you've retrieved it.
    """

    def __init__(self):
        """Initialize manual enricher."""
        self._context: dict[str, str] = {}

    def identify_components_needing_context(self, spec: DiagramSpec) -> dict[str, str]:
        """Identify Databricks components that need technical context.

        Args:
            spec: Diagram specification

        Returns:
            Dictionary mapping component IDs to suggested search queries
        """
        databricks_keywords = [
            "databricks",
            "delta",
            "unity catalog",
            "uc",
            "lakeflow",
            "mosaic",
            "mlflow",
            "automl",
            "lakehouse",
        ]

        queries = {}
        for comp in spec.components:
            # Check if component relates to Databricks
            comp_text = f"{comp.id} {comp.label}".lower()
            if any(keyword in comp_text for keyword in databricks_keywords):
                query = self._build_search_query(comp)
                queries[comp.id] = query

        return queries

    def _build_search_query(self, component: Component) -> str:
        """Build suggested search query for component."""
        query_parts = [component.label]

        # Add specific keywords based on component ID
        if "uc" in component.id.lower() or "unity" in component.id.lower():
            query_parts.append("Unity Catalog architecture")
        elif "delta" in component.id.lower():
            query_parts.append("Delta Lake")
        elif "lakeflow" in component.id.lower():
            query_parts.append("Lakeflow Connect")
        elif "mosaic" in component.id.lower():
            query_parts.append("Agent Bricks")

        return " ".join(query_parts)

    def add_context(self, component_id: str, context: str) -> None:
        """Add context for a component.

        Args:
            component_id: Component identifier
            context: Technical context text
        """
        self._context[component_id] = context

    def build_enriched_prompt_section(self) -> str:
        """Build prompt section with all added context.

        Returns:
            Formatted prompt section
        """
        if not self._context:
            return ""

        lines = ["===== TECHNICAL CONTEXT FROM DATABRICKS DOCUMENTATION ====="]
        lines.append("")
        lines.append(
            "Use this accurate technical information when depicting these components:"
        )
        lines.append("")

        for component_id, context in self._context.items():
            lines.append(f"**{component_id.upper()}**:")
            lines.append(f"{context}")
            lines.append("")

        lines.append(
            "Ensure all terminology and descriptions match this official documentation."
        )

        return "\n".join(lines)

    def get_enrichment_instructions(
        self, queries: dict[str, str]
    ) -> str:
        """Get instructions for how to enrich with Claude Code.

        Args:
            queries: Dictionary of component IDs to search queries

        Returns:
            Instructions text
        """
        lines = ["# MCP Enrichment Instructions"]
        lines.append("")
        lines.append("Ask Claude Code to search Databricks docs for:")
        lines.append("")

        for comp_id, query in queries.items():
            lines.append(f"## {comp_id}")
            lines.append(f"Search query: `{query}`")
            lines.append("")
            lines.append("Example: 'Search Databricks docs for: " + query + "'")
            lines.append("")

        lines.append("## After Getting Context")
        lines.append("")
        lines.append("Add context using:")
        lines.append("```python")
        lines.append("enricher = ManualMCPEnricher()")
        lines.append('enricher.add_context("component-id", "context from docs")')
        lines.append("prompt_section = enricher.build_enriched_prompt_section()")
        lines.append("```")

        return "\n".join(lines)


# Convenience function for quick workflow
def create_enrichment_workflow(spec: DiagramSpec) -> str:
    """Create a workflow guide for enriching a diagram spec.

    Args:
        spec: Diagram specification

    Returns:
        Markdown workflow instructions
    """
    enricher = ManualMCPEnricher()
    queries = enricher.identify_components_needing_context(spec)

    if not queries:
        return "No Databricks components found that need enrichment."

    return enricher.get_enrichment_instructions(queries)
