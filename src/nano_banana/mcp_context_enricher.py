"""MCP context enrichment for architect conversations.

This module provides context enrichment by querying internal knowledge sources
(Glean, Slack, JIRA, Confluence) via Claude Code's MCP tools.

The enricher uses a callback pattern - it defines WHAT to search, and Claude Code
executes the actual MCP tool calls.
"""

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Optional

from rich.console import Console

from .mcp_config import MCPEnrichmentConfig

console = Console()


class MCPSource(str, Enum):
    """Available MCP sources for context enrichment."""

    GLEAN = "glean"
    SLACK = "slack"
    JIRA = "jira"
    CONFLUENCE = "confluence"


@dataclass
class MCPQuery:
    """A query to execute against an MCP source.

    This dataclass represents the query specification that gets passed
    to Claude Code's MCP tools via the callback.
    """

    source: MCPSource
    endpoint: str
    params: dict[str, Any]
    description: str

    def __repr__(self) -> str:
        return f"MCPQuery({self.source.value}, {self.endpoint}, {self.description})"


@dataclass
class EnrichmentResult:
    """Result from enrichment queries."""

    source: MCPSource
    query: str
    results: list[dict[str, Any]] = field(default_factory=list)
    error: Optional[str] = None

    @property
    def success(self) -> bool:
        """Check if the query was successful."""
        return self.error is None and len(self.results) > 0


@dataclass
class ExtractedTerms:
    """Terms extracted from user input for searching."""

    customers: list[str] = field(default_factory=list)
    concepts: list[str] = field(default_factory=list)

    @property
    def has_terms(self) -> bool:
        """Check if any terms were extracted."""
        return bool(self.customers or self.concepts)

    def all_terms(self) -> list[str]:
        """Get all extracted terms."""
        return self.customers + self.concepts


class MCPContextEnricher:
    """Enriches conversation context with internal knowledge.

    Uses MCP tools (via callback) to search Glean, Slack, JIRA, and
    Confluence for relevant context based on user input.

    Example usage from Claude Code:
        def mcp_callback(query: MCPQuery) -> Any:
            if query.source == MCPSource.GLEAN:
                return mcp__glean__glean_read_api_call(...)
            # etc.

        enricher = MCPContextEnricher(config, mcp_callback)
        context = enricher.enrich(user_input, history)
    """

    def __init__(
        self,
        config: MCPEnrichmentConfig,
        mcp_callback: Optional[Callable[[MCPQuery], Any]] = None,
    ):
        """Initialize the enricher.

        Args:
            config: Enrichment configuration
            mcp_callback: Callback function that executes MCP queries.
                         If None, enrichment is disabled.
        """
        self.config = config
        self.mcp_callback = mcp_callback
        self._customer_pattern = self._build_customer_pattern()
        self._concept_pattern = self._build_concept_pattern()

    def _build_customer_pattern(self) -> re.Pattern:
        """Build regex pattern for customer name detection."""
        escaped = [re.escape(name) for name in self.config.customer_names]
        pattern = r"\b(" + "|".join(escaped) + r")\b"
        return re.compile(pattern, re.IGNORECASE)

    def _build_concept_pattern(self) -> re.Pattern:
        """Build regex pattern for concept detection."""
        escaped = [re.escape(concept) for concept in self.config.databricks_concepts]
        pattern = r"\b(" + "|".join(escaped) + r")\b"
        return re.compile(pattern, re.IGNORECASE)

    def extract_search_terms(self, user_input: str) -> ExtractedTerms:
        """Extract searchable terms from user input.

        Detects customer names and Databricks concepts mentioned in the input.

        Args:
            user_input: The user's message

        Returns:
            ExtractedTerms with detected customers and concepts
        """
        # Find customer matches
        customer_matches = self._customer_pattern.findall(user_input)
        # Normalize to title case and deduplicate
        customers = list(set(m.title() for m in customer_matches))

        # Find concept matches
        concept_matches = self._concept_pattern.findall(user_input)
        # Normalize casing based on config and deduplicate
        concepts = []
        seen = set()
        for match in concept_matches:
            match_lower = match.lower()
            if match_lower not in seen:
                seen.add(match_lower)
                # Find original casing from config
                for configured in self.config.databricks_concepts:
                    if configured.lower() == match_lower:
                        concepts.append(configured)
                        break

        return ExtractedTerms(customers=customers, concepts=concepts)

    def build_queries(self, terms: ExtractedTerms) -> list[MCPQuery]:
        """Build MCP queries for extracted terms.

        Creates appropriate queries for each enabled source based on
        the detected customers and concepts.

        Args:
            terms: Extracted search terms

        Returns:
            List of MCPQuery objects to execute
        """
        queries = []

        for source_name in self.config.sources:
            try:
                source = MCPSource(source_name.lower())
            except ValueError:
                console.print(f"[yellow]Warning: Unknown MCP source '{source_name}'[/yellow]")
                continue

            if source == MCPSource.GLEAN:
                queries.extend(self._build_glean_queries(terms))
            elif source == MCPSource.SLACK:
                queries.extend(self._build_slack_queries(terms))
            elif source == MCPSource.JIRA:
                queries.extend(self._build_jira_queries(terms))
            elif source == MCPSource.CONFLUENCE:
                queries.extend(self._build_confluence_queries(terms))

        return queries

    def _build_glean_queries(self, terms: ExtractedTerms) -> list[MCPQuery]:
        """Build Glean search queries."""
        queries = []

        # Search for customer-specific content
        for customer in terms.customers:
            queries.append(MCPQuery(
                source=MCPSource.GLEAN,
                endpoint="/search",
                params={
                    "query": f"{customer} Databricks architecture",
                    "pageSize": self.config.max_results_per_source,
                },
                description=f"Search Glean for {customer} architecture docs",
            ))

        # Search for concept best practices
        for concept in terms.concepts:
            queries.append(MCPQuery(
                source=MCPSource.GLEAN,
                endpoint="/search",
                params={
                    "query": f"{concept} best practices implementation",
                    "pageSize": self.config.max_results_per_source,
                },
                description=f"Search Glean for {concept} best practices",
            ))

        return queries

    def _build_slack_queries(self, terms: ExtractedTerms) -> list[MCPQuery]:
        """Build Slack search queries."""
        queries = []

        # Search for customer discussions
        for customer in terms.customers:
            queries.append(MCPQuery(
                source=MCPSource.SLACK,
                endpoint="/search.messages",
                params={
                    "query": f"{customer} architecture",
                    "count": self.config.max_results_per_source,
                },
                description=f"Search Slack for {customer} discussions",
            ))

        # Search for concept discussions
        for concept in terms.concepts[:2]:  # Limit to avoid too many queries
            queries.append(MCPQuery(
                source=MCPSource.SLACK,
                endpoint="/search.messages",
                params={
                    "query": f"{concept} implementation",
                    "count": self.config.max_results_per_source,
                },
                description=f"Search Slack for {concept} discussions",
            ))

        return queries

    def _build_jira_queries(self, terms: ExtractedTerms) -> list[MCPQuery]:
        """Build JIRA search queries."""
        queries = []

        # Search for customer-related tickets
        for customer in terms.customers:
            queries.append(MCPQuery(
                source=MCPSource.JIRA,
                endpoint="/search",
                params={
                    "jql": f'text ~ "{customer}" ORDER BY updated DESC',
                    "maxResults": self.config.max_results_per_source,
                    "fields": "summary,description,status",
                },
                description=f"Search JIRA for {customer} tickets",
            ))

        return queries

    def _build_confluence_queries(self, terms: ExtractedTerms) -> list[MCPQuery]:
        """Build Confluence search queries."""
        queries = []

        # Search for customer documentation
        for customer in terms.customers:
            queries.append(MCPQuery(
                source=MCPSource.CONFLUENCE,
                endpoint="/wiki/rest/api/search",
                params={
                    "cql": f'text ~ "{customer}" AND type = page',
                    "limit": self.config.max_results_per_source,
                },
                description=f"Search Confluence for {customer} pages",
            ))

        # Search for concept documentation
        for concept in terms.concepts[:2]:  # Limit queries
            queries.append(MCPQuery(
                source=MCPSource.CONFLUENCE,
                endpoint="/wiki/rest/api/search",
                params={
                    "cql": f'text ~ "{concept}" AND type = page',
                    "limit": self.config.max_results_per_source,
                },
                description=f"Search Confluence for {concept} docs",
            ))

        return queries

    def enrich(
        self,
        user_input: str,
        conversation_history: Optional[str] = None,
    ) -> str:
        """Enrich context with internal knowledge.

        Main entry point for context enrichment. Extracts terms from
        user input, builds queries, executes them via callback, and
        formats the results.

        Args:
            user_input: The user's current message
            conversation_history: Optional conversation history for context

        Returns:
            Formatted enrichment context string, or empty string if
            no enrichment was performed
        """
        if not self.config.enabled:
            return ""

        if not self.mcp_callback:
            console.print("[dim]MCP enrichment enabled but no callback provided[/dim]")
            return ""

        # Extract search terms
        terms = self.extract_search_terms(user_input)
        if not terms.has_terms:
            return ""

        console.print(f"[dim]Detected terms: {terms.all_terms()}[/dim]")

        # Build queries
        queries = self.build_queries(terms)
        if not queries:
            return ""

        console.print(f"[dim]Executing {len(queries)} MCP queries...[/dim]")

        # Execute queries via callback
        results: list[EnrichmentResult] = []
        for query in queries:
            try:
                response = self.mcp_callback(query)
                results.append(EnrichmentResult(
                    source=query.source,
                    query=query.description,
                    results=self._parse_response(query.source, response),
                ))
            except Exception as e:
                results.append(EnrichmentResult(
                    source=query.source,
                    query=query.description,
                    error=str(e),
                ))

        # Summarize results
        context = self._format_enrichment(results)

        if context:
            console.print("[green]Context enriched with internal knowledge[/green]")

        return context

    def _parse_response(self, source: MCPSource, response: Any) -> list[dict[str, Any]]:
        """Parse MCP response into standardized format.

        Args:
            source: The MCP source
            response: Raw response from MCP callback

        Returns:
            List of standardized result dictionaries
        """
        if response is None:
            return []

        # Handle different response formats
        if isinstance(response, list):
            return response[:self.config.max_results_per_source]
        elif isinstance(response, dict):
            # Common patterns for different sources
            if "results" in response:
                return response["results"][:self.config.max_results_per_source]
            elif "messages" in response:
                return response["messages"][:self.config.max_results_per_source]
            elif "issues" in response:
                return response["issues"][:self.config.max_results_per_source]
            else:
                return [response]
        else:
            return []

    def _format_enrichment(self, results: list[EnrichmentResult]) -> str:
        """Format enrichment results into context string.

        Args:
            results: List of enrichment results

        Returns:
            Formatted context string
        """
        successful_results = [r for r in results if r.success]
        if not successful_results:
            return ""

        sections = []

        # Group by source
        by_source: dict[MCPSource, list[EnrichmentResult]] = {}
        for result in successful_results:
            if result.source not in by_source:
                by_source[result.source] = []
            by_source[result.source].append(result)

        for source, source_results in by_source.items():
            section_lines = [f"## From {source.value.title()}:"]

            for result in source_results:
                for item in result.results:
                    summary = self._summarize_item(source, item)
                    if summary:
                        section_lines.append(f"- {summary}")

            if len(section_lines) > 1:  # Has content beyond header
                sections.append("\n".join(section_lines))

        if not sections:
            return ""

        # Build final context with character limit
        header = "===== RELEVANT INTERNAL KNOWLEDGE ====="
        footer = "===== END INTERNAL KNOWLEDGE ====="

        content = "\n\n".join(sections)

        # Truncate if needed
        max_content_len = self.config.max_context_chars - len(header) - len(footer) - 10
        if len(content) > max_content_len:
            content = content[:max_content_len] + "..."

        return f"{header}\n{content}\n{footer}"

    def _summarize_item(self, source: MCPSource, item: dict[str, Any]) -> str:
        """Summarize a single result item.

        Args:
            source: The MCP source
            item: Result item dictionary

        Returns:
            Summary string
        """
        if source == MCPSource.GLEAN:
            return self._summarize_glean(item)
        elif source == MCPSource.SLACK:
            return self._summarize_slack(item)
        elif source == MCPSource.JIRA:
            return self._summarize_jira(item)
        elif source == MCPSource.CONFLUENCE:
            return self._summarize_confluence(item)
        return ""

    def _summarize_glean(self, item: dict[str, Any]) -> str:
        """Summarize a Glean search result."""
        title = item.get("title", item.get("name", ""))
        snippet = item.get("snippet", item.get("description", ""))[:200]
        if title:
            return f"{title}: {snippet}" if snippet else title
        return snippet

    def _summarize_slack(self, item: dict[str, Any]) -> str:
        """Summarize a Slack message."""
        text = item.get("text", "")[:200]
        channel = item.get("channel", {}).get("name", "")
        if channel:
            return f"#{channel}: {text}"
        return text

    def _summarize_jira(self, item: dict[str, Any]) -> str:
        """Summarize a JIRA issue."""
        key = item.get("key", "")
        fields = item.get("fields", {})
        summary = fields.get("summary", "")
        status = fields.get("status", {}).get("name", "")
        if key:
            return f"{key} ({status}): {summary}"
        return summary

    def _summarize_confluence(self, item: dict[str, Any]) -> str:
        """Summarize a Confluence page."""
        title = item.get("title", "")
        excerpt = item.get("excerpt", item.get("body", {}).get("excerpt", ""))[:200]
        if title:
            return f"{title}: {excerpt}" if excerpt else title
        return excerpt
