"""Native MCP client for nano-banana.

Connects to the same MCP servers configured in Claude Code's settings.json,
enabling nano-banana to query Glean, Slack, JIRA, and Confluence directly.

Uses subprocess with JSON-RPC over stdio for reliability.
"""

import json
import os
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from rich.console import Console

console = Console()


@dataclass
class MCPServerConfig:
    """Configuration for an MCP server."""

    name: str
    command: str
    args: list[str]
    env: dict[str, str] = field(default_factory=dict)


def load_claude_mcp_config() -> dict[str, MCPServerConfig]:
    """Load MCP server configs from Claude Code's settings.json.

    Returns:
        Dict mapping server name to MCPServerConfig
    """
    settings_path = Path.home() / ".claude" / "settings.json"

    if not settings_path.exists():
        console.print("[yellow]Warning: Claude Code settings.json not found[/yellow]")
        return {}

    with open(settings_path) as f:
        settings = json.load(f)

    mcp_servers = settings.get("mcpServers", {})
    configs = {}

    for name, config in mcp_servers.items():
        # Expand ~ in paths
        args = [os.path.expanduser(arg) for arg in config.get("args", [])]
        command = os.path.expanduser(config.get("command", ""))

        configs[name] = MCPServerConfig(
            name=name,
            command=command,
            args=args,
            env=config.get("env", {}),
        )

    return configs


class MCPSubprocessClient:
    """MCP client using subprocess with JSON-RPC protocol.

    Spawns the MCP server as a subprocess and communicates via stdin/stdout.
    Each call spawns a fresh process for reliability.
    """

    def __init__(self):
        self._configs = load_claude_mcp_config()
        self._request_id = 0

    def _next_id(self) -> int:
        self._request_id += 1
        return self._request_id

    def call_tool(
        self,
        server_name: str,
        tool_name: str,
        arguments: dict[str, Any],
        timeout: float = 30.0,
    ) -> Optional[dict[str, Any]]:
        """Call a tool on an MCP server.

        Args:
            server_name: Name of the server (e.g., 'glean', 'slack')
            tool_name: Name of the tool to call
            arguments: Tool arguments
            timeout: Timeout in seconds

        Returns:
            Tool result dict or None on error
        """
        if server_name not in self._configs:
            console.print(f"[yellow]Server '{server_name}' not found[/yellow]")
            return None

        config = self._configs[server_name]

        # Build environment
        env = os.environ.copy()
        env.update(config.env)

        # Build JSON-RPC messages
        messages = [
            # Initialize
            json.dumps({
                "jsonrpc": "2.0",
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "nano-banana", "version": "1.0"},
                },
                "id": self._next_id(),
            }),
            # Initialized notification
            json.dumps({
                "jsonrpc": "2.0",
                "method": "notifications/initialized",
                "params": {},
            }),
            # Tool call
            json.dumps({
                "jsonrpc": "2.0",
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments,
                },
                "id": self._next_id(),
            }),
        ]

        # Add small delays between messages
        input_data = "\n".join(messages) + "\n"

        try:
            # Run the MCP server
            cmd = [config.command] + config.args
            result = subprocess.run(
                cmd,
                input=input_data,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=env,
            )

            # Parse output - look for the last JSON object (the tool response)
            responses = []
            for line in result.stdout.strip().split("\n"):
                if line.strip():
                    try:
                        responses.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass

            # Find the tool call response (last response with result/error)
            for resp in reversed(responses):
                if "result" in resp or "error" in resp:
                    if "error" in resp:
                        console.print(f"[red]MCP error: {resp['error']}[/red]")
                        return None
                    return resp.get("result")

            return None

        except subprocess.TimeoutExpired:
            console.print(f"[red]Timeout calling {server_name}.{tool_name}[/red]")
            return None
        except Exception as e:
            console.print(f"[red]Error calling {server_name}.{tool_name}: {e}[/red]")
            return None


# Global client instance
_client: Optional[MCPSubprocessClient] = None


def get_client() -> MCPSubprocessClient:
    """Get or create the global MCP client."""
    global _client
    if _client is None:
        _client = MCPSubprocessClient()
    return _client


def search_glean(query: str, page_size: int = 5) -> list[dict[str, Any]]:
    """Search Glean for documents.

    Args:
        query: Search query
        page_size: Number of results to return

    Returns:
        List of search results
    """
    client = get_client()
    result = client.call_tool(
        "glean",
        "glean_read_api_call",
        {
            "endpoint": "search.query",
            "params": {
                "query": query,
                "page_size": page_size,
            },
        },
    )

    if not result:
        return []

    return _parse_glean_results(result)


def search_slack(query: str, count: int = 5) -> list[dict[str, Any]]:
    """Search Slack messages.

    Args:
        query: Search query
        count: Number of results

    Returns:
        List of message results
    """
    client = get_client()
    result = client.call_tool(
        "slack",
        "slack_read_api_call",
        {
            "endpoint": "search.messages",
            "params": {
                "query": query,
                "count": count,
            },
        },
    )

    if not result:
        return []

    return _parse_slack_results(result)


def search_jira(jql: str, max_results: int = 5) -> list[dict[str, Any]]:
    """Search JIRA issues.

    Args:
        jql: JQL query string
        max_results: Maximum results

    Returns:
        List of issues
    """
    client = get_client()
    result = client.call_tool(
        "jira",
        "jira_read_api_call",
        {
            "endpoint": "/rest/api/3/search",
            "params": {
                "jql": jql,
                "maxResults": max_results,
            },
        },
    )

    if not result:
        return []

    return _parse_jira_results(result)


def search_confluence(cql: str, limit: int = 5) -> list[dict[str, Any]]:
    """Search Confluence pages.

    Args:
        cql: CQL query string
        limit: Maximum results

    Returns:
        List of pages
    """
    client = get_client()
    result = client.call_tool(
        "confluence",
        "search_confluence_pages",
        {
            "query": cql,
            "limit": limit,
        },
    )

    if not result:
        return []

    return _parse_confluence_results(result)


def _parse_glean_results(result: dict[str, Any]) -> list[dict[str, Any]]:
    """Parse Glean search results into standardized format."""
    results = []
    content = result.get("content", [])

    for item in content:
        # Handle both dict and object-like items
        item_type = item.get("type") if isinstance(item, dict) else getattr(item, "type", None)
        item_text = item.get("text", "") if isinstance(item, dict) else getattr(item, "text", "")

        if item_type == "text" and item_text:
            # The Glean server returns formatted text, parse it
            # Format: **N. Title**\n**Document ID:**...\n**URL:**...\n**Snippet:**...
            lines = item_text.split("\n")
            current = {}

            for line in lines:
                line = line.strip()
                if line.startswith("**") and line.endswith("**") and ". " in line:
                    # Title line like "**1. Title Here**"
                    if current and current.get("title"):
                        results.append(current)
                    title = line.strip("*").split(". ", 1)[-1] if ". " in line else line.strip("*")
                    current = {"title": title, "source": "glean"}
                elif line.startswith("**URL:**"):
                    current["url"] = line.replace("**URL:**", "").strip()
                elif line.startswith("**Snippet:**"):
                    current["snippet"] = line.replace("**Snippet:**", "").strip()
                elif line.startswith("**Datasource:**"):
                    current["datasource"] = line.replace("**Datasource:**", "").strip()

            if current and current.get("title"):
                results.append(current)

    return results


def _parse_slack_results(result: dict[str, Any]) -> list[dict[str, Any]]:
    """Parse Slack search results."""
    results = []
    content = result.get("content", [])

    for item in content:
        if item.get("type") == "text":
            try:
                data = json.loads(item.get("text", "{}"))
                messages = data.get("messages", {}).get("matches", [])
                for msg in messages:
                    results.append({
                        "text": msg.get("text", "")[:200],
                        "channel": msg.get("channel", {}).get("name", ""),
                        "user": msg.get("username", ""),
                        "source": "slack",
                    })
            except json.JSONDecodeError:
                pass

    return results


def _parse_jira_results(result: dict[str, Any]) -> list[dict[str, Any]]:
    """Parse JIRA search results."""
    results = []
    content = result.get("content", [])

    for item in content:
        if item.get("type") == "text":
            try:
                data = json.loads(item.get("text", "{}"))
                issues = data.get("issues", [])
                for issue in issues:
                    fields = issue.get("fields", {})
                    results.append({
                        "key": issue.get("key", ""),
                        "summary": fields.get("summary", ""),
                        "status": fields.get("status", {}).get("name", ""),
                        "source": "jira",
                    })
            except json.JSONDecodeError:
                pass

    return results


def _parse_confluence_results(result: dict[str, Any]) -> list[dict[str, Any]]:
    """Parse Confluence search results."""
    results = []
    content = result.get("content", [])

    for item in content:
        if item.get("type") == "text":
            try:
                data = json.loads(item.get("text", "{}"))
                pages = data.get("results", data) if isinstance(data, dict) else data
                if isinstance(pages, list):
                    for page in pages:
                        results.append({
                            "title": page.get("title", ""),
                            "excerpt": page.get("excerpt", "")[:200],
                            "url": page.get("url", page.get("_links", {}).get("webui", "")),
                            "source": "confluence",
                        })
            except json.JSONDecodeError:
                pass

    return results


# CLI test function
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = "Databricks NCC network connectivity"

    print(f"Searching Glean for: {query}")
    print("-" * 50)

    results = search_glean(query, page_size=3)

    if results:
        for i, r in enumerate(results, 1):
            print(f"\n{i}. {r.get('title', 'Untitled')}")
            if r.get("url"):
                print(f"   URL: {r['url']}")
            if r.get("snippet"):
                print(f"   {r['snippet'][:100]}...")
    else:
        print("No results found")
