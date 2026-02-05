"""Configuration for MCP context enrichment.

This module defines the configuration for enriching architect conversations
with context from internal knowledge sources (Glean, Slack, JIRA, Confluence)
via Claude Code's MCP tools.
"""

from typing import Optional

from pydantic import BaseModel, Field


class MCPEnrichmentConfig(BaseModel):
    """Configuration for MCP-based context enrichment.

    When enabled and invoked from Claude Code with an mcp_callback,
    the architect chatbot will automatically search internal knowledge
    sources for relevant context before processing user input.
    """

    enabled: bool = Field(
        default=False,
        description="Enable MCP-based context enrichment (requires Claude Code callback)",
    )

    sources: list[str] = Field(
        default_factory=lambda: ["glean", "confluence"],
        description="MCP sources to query: glean, slack, jira, confluence",
    )

    max_results_per_source: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Maximum results to retrieve per source",
    )

    max_context_chars: int = Field(
        default=2000,
        ge=100,
        le=10000,
        description="Maximum characters for enriched context",
    )

    customer_names: list[str] = Field(
        default_factory=lambda: [
            # Common Australian enterprise customers
            "Coles",
            "Woolworths",
            "ANZ",
            "Commonwealth Bank",
            "CBA",
            "NAB",
            "Westpac",
            "Telstra",
            "Optus",
            "Qantas",
            "BHP",
            "Rio Tinto",
            "AGL",
            "Origin Energy",
            "Medibank",
            "Suncorp",
            "IAG",
            "REA Group",
            "Domain",
            "Seek",
            "Canva",
            "Atlassian",
        ],
        description="Customer names to detect in user input for targeted searches",
    )

    databricks_concepts: list[str] = Field(
        default_factory=lambda: [
            # Core platform
            "Unity Catalog",
            "Delta Lake",
            "Delta Sharing",
            "Lakehouse",
            "Databricks SQL",
            "Photon",
            # Compute
            "Serverless",
            "Jobs",
            "Workflows",
            "Clusters",
            # AI/ML
            "MLflow",
            "Model Serving",
            "Feature Store",
            "Vector Search",
            "Foundation Models",
            "Mosaic AI",
            # Data engineering
            "Auto Loader",
            "Delta Live Tables",
            "DLT",
            "Structured Streaming",
            "Change Data Capture",
            "CDC",
            # Governance
            "Data Governance",
            "Access Control",
            "Row Filters",
            "Column Masks",
            "Lineage",
            "Data Quality",
            # Migration
            "Snowflake Migration",
            "Data Migration",
            "Workspace Migration",
        ],
        description="Databricks concepts to detect for targeted searches",
    )

    def get_search_terms(self) -> set[str]:
        """Get all configured search terms as a set.

        Returns:
            Set of all customer names and Databricks concepts
        """
        return set(self.customer_names) | set(self.databricks_concepts)
