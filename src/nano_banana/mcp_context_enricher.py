"""MCP context enrichment for architect conversations.

This module provides context enrichment by querying internal knowledge sources
(Glean, Slack, JIRA, Confluence) via MCP servers.

Supports two modes:
1. Native mode (default): Uses mcp_client to connect directly to MCP servers
2. Callback mode: Uses a provided callback for Claude Code integration
"""

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Optional

from rich.console import Console

from .mcp_config import MCPEnrichmentConfig

console = Console()

# Try to import native MCP client
try:
    from . import mcp_client as native_mcp
    NATIVE_MCP_AVAILABLE = True
except ImportError:
    NATIVE_MCP_AVAILABLE = False


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

    Uses MCP tools to search Glean, Slack, JIRA, and Confluence for
    relevant context based on user input.

    Supports two modes:
    1. Native mode: Uses mcp_client to connect directly to MCP servers
       (requires Claude Code's settings.json to be present)
    2. Callback mode: Uses a provided callback (for Claude Code integration)

    Example usage (native mode):
        enricher = MCPContextEnricher(config)  # Uses native MCP client
        context = enricher.enrich(user_input, history)

    Example usage (callback mode from Claude Code):
        def mcp_callback(query: MCPQuery) -> Any:
            if query.source == MCPSource.GLEAN:
                return mcp__glean__glean_read_api_call(...)

        enricher = MCPContextEnricher(config, mcp_callback)
        context = enricher.enrich(user_input, history)
    """

    def __init__(
        self,
        config: MCPEnrichmentConfig,
        mcp_callback: Optional[Callable[[MCPQuery], Any]] = None,
        use_native: bool = True,
    ):
        """Initialize the enricher.

        Args:
            config: Enrichment configuration
            mcp_callback: Optional callback function that executes MCP queries.
                         If None and use_native=True, uses native MCP client.
            use_native: If True (default), use native MCP client when no callback provided.
        """
        self.config = config
        self.mcp_callback = mcp_callback
        self.use_native = use_native and NATIVE_MCP_AVAILABLE and mcp_callback is None
        self._customer_pattern = self._build_customer_pattern()
        self._concept_pattern = self._build_concept_pattern()

        if self.use_native:
            console.print("[dim]Using native MCP client for enrichment[/dim]")

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
        user input, builds queries, executes them via native MCP client
        or callback, and formats the results.

        Args:
            user_input: The user's current message
            conversation_history: Optional conversation history for context

        Returns:
            Formatted enrichment context string, or empty string if
            no enrichment was performed
        """
        if not self.config.enabled:
            return ""

        # Check if we have a way to execute queries
        if not self.mcp_callback and not self.use_native:
            console.print("[dim]MCP enrichment enabled but no MCP access available[/dim]")
            return ""

        # Extract search terms
        terms = self.extract_search_terms(user_input)
        if not terms.has_terms:
            return ""

        console.print(f"[dim]Detected terms: {terms.all_terms()}[/dim]")

        # Use native MCP client if available
        if self.use_native:
            return self._enrich_native(terms)

        # Fall back to callback mode
        return self._enrich_callback(terms)

    def _enrich_native(self, terms: ExtractedTerms) -> str:
        """Enrich context using native MCP client.

        Args:
            terms: Extracted search terms

        Returns:
            Formatted enrichment context string
        """
        results: list[EnrichmentResult] = []

        # Search Glean for each term
        if "glean" in self.config.sources:
            for term in terms.all_terms()[:3]:  # Limit queries
                console.print(f"[dim]Searching Glean for '{term}'...[/dim]")
                try:
                    glean_results = native_mcp.search_glean(
                        f"{term} Databricks",
                        page_size=self.config.max_results_per_source,
                    )
                    if glean_results:
                        results.append(EnrichmentResult(
                            source=MCPSource.GLEAN,
                            query=f"Search for {term}",
                            results=glean_results,
                        ))
                except Exception as e:
                    console.print(f"[yellow]Glean search failed: {e}[/yellow]")

        # Search Slack for customer terms
        if "slack" in self.config.sources:
            for customer in terms.customers[:2]:
                console.print(f"[dim]Searching Slack for '{customer}'...[/dim]")
                try:
                    slack_results = native_mcp.search_slack(
                        f"{customer} architecture",
                        count=self.config.max_results_per_source,
                    )
                    if slack_results:
                        results.append(EnrichmentResult(
                            source=MCPSource.SLACK,
                            query=f"Search for {customer}",
                            results=slack_results,
                        ))
                except Exception as e:
                    console.print(f"[yellow]Slack search failed: {e}[/yellow]")

        # Search Confluence for concepts
        if "confluence" in self.config.sources:
            for concept in terms.concepts[:2]:
                console.print(f"[dim]Searching Confluence for '{concept}'...[/dim]")
                try:
                    confluence_results = native_mcp.search_confluence(
                        f"{concept} best practices",
                        limit=self.config.max_results_per_source,
                    )
                    if confluence_results:
                        results.append(EnrichmentResult(
                            source=MCPSource.CONFLUENCE,
                            query=f"Search for {concept}",
                            results=confluence_results,
                        ))
                except Exception as e:
                    console.print(f"[yellow]Confluence search failed: {e}[/yellow]")

        # Format results
        context = self._format_enrichment(results)

        if context:
            console.print("[green]Context enriched with internal knowledge[/green]")

        return context

    def _enrich_callback(self, terms: ExtractedTerms) -> str:
        """Enrich context using callback mode (original implementation).

        Args:
            terms: Extracted search terms

        Returns:
            Formatted enrichment context string
        """
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
        url = item.get("url", "")
        if title:
            result = f"{title}: {snippet}" if snippet else title
            if url:
                result += f" ({url})"
            return result
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
