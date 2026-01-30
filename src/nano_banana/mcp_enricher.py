"""MCP-based context enrichment for diagram prompts.

Uses databricks-docs MCP to add accurate technical context to diagram specifications.
"""

import json
import subprocess
from pathlib import Path
from typing import Any, Optional

from .models import DiagramSpec, Component


class MCPEnricher:
    """Enriches diagram specifications with Databricks documentation context."""

    def __init__(self):
        """Initialize MCP enricher."""
        self._cache: dict[str, str] = {}

    def enrich_diagram_spec(self, spec: DiagramSpec) -> dict[str, str]:
        """Enrich diagram spec with technical context from Databricks docs.

        Args:
            spec: Diagram specification

        Returns:
            Dictionary mapping component names to their technical context
        """
        enriched_context = {}

        # Extract Databricks-related components
        databricks_components = self._extract_databricks_components(spec)

        # Fetch context for each component
        for component_name, component in databricks_components.items():
            context = self._get_component_context(component_name, component)
            if context:
                enriched_context[component_name] = context

        return enriched_context

    def _extract_databricks_components(
        self, spec: DiagramSpec
    ) -> dict[str, Component]:
        """Extract Databricks-related components from spec.

        Args:
            spec: Diagram specification

        Returns:
            Dictionary of component names to Component
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

        components = {}
        for comp in spec.components:
            # Check if component relates to Databricks
            comp_text = f"{comp.id} {comp.label}".lower()
            if any(keyword in comp_text for keyword in databricks_keywords):
                components[comp.id] = comp

        return components

    def _get_component_context(
        self, component_name: str, component: Component
    ) -> Optional[str]:
        """Get technical context for a component from Databricks docs.

        Args:
            component_name: Component identifier
            component: Component specification

        Returns:
            Context string or None if not found
        """
        # Check cache first
        cache_key = f"{component_name}:{component.label}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        # Build search query
        search_query = self._build_search_query(component)

        # Search Databricks docs via MCP
        context = self._search_databricks_docs(search_query)

        if context:
            self._cache[cache_key] = context

        return context

    def _build_search_query(self, component: Component) -> str:
        """Build search query for component.

        Args:
            component: Component specification

        Returns:
            Search query string
        """
        # Combine label and type for better search
        query_parts = [component.label]

        # Add specific keywords based on component ID
        if "uc" in component.id.lower() or "unity" in component.id.lower():
            query_parts.append("Unity Catalog")
        elif "delta" in component.id.lower():
            query_parts.append("Delta Lake")
        elif "lakeflow" in component.id.lower():
            query_parts.append("Lakeflow")
        elif "mosaic" in component.id.lower():
            query_parts.append("Agent Bricks")

        return " ".join(query_parts)

    def _search_databricks_docs(self, query: str) -> Optional[str]:
        """Search Databricks documentation via MCP.

        Args:
            query: Search query

        Returns:
            Context string or None
        """
        try:
            # Call MCP via mcp-cli
            result = subprocess.run(
                [
                    "mcp-cli",
                    "call",
                    "databricks-docs/search_databricks_content",
                    json.dumps({"query": query, "max_results": 1}),
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                response = json.loads(result.stdout)
                # Extract relevant context from response
                return self._extract_context_from_response(response)

        except Exception as e:
            print(f"Warning: MCP search failed for '{query}': {e}")

        return None

    def _extract_context_from_response(self, response: dict[str, Any]) -> str:
        """Extract useful context from MCP response.

        Args:
            response: MCP response dictionary

        Returns:
            Extracted context string
        """
        # This will depend on the actual MCP response format
        # Adjust based on what databricks-docs/search_databricks_content returns
        if "results" in response and response["results"]:
            first_result = response["results"][0]
            # Extract title, description, or summary
            parts = []
            if "title" in first_result:
                parts.append(first_result["title"])
            if "description" in first_result:
                parts.append(first_result["description"])
            if "content" in first_result:
                # Take first 200 chars of content
                parts.append(first_result["content"][:200])

            return " - ".join(parts)

        return ""

    def build_enriched_prompt_section(
        self, enriched_context: dict[str, str]
    ) -> str:
        """Build prompt section with enriched context.

        Args:
            enriched_context: Dictionary of component contexts

        Returns:
            Formatted prompt section
        """
        if not enriched_context:
            return ""

        lines = ["===== TECHNICAL CONTEXT FROM DATABRICKS DOCUMENTATION ====="]
        lines.append("")

        for component_name, context in enriched_context.items():
            lines.append(f"{component_name}:")
            lines.append(f"  {context}")
            lines.append("")

        lines.append(
            "Use this technical context to ensure accurate representation of Databricks components."
        )

        return "\n".join(lines)
