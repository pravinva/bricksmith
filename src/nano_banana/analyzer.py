"""Prompt analysis and improvement suggestions for Nano Banana Pro."""

import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Optional

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from .mlflow_tracker import MLflowTracker


console = Console()


class PromptAnalyzer:
    """Analyzes prompts from MLflow runs to find patterns and suggest improvements."""

    def __init__(self, mlflow_tracker: MLflowTracker):
        """Initialize analyzer.

        Args:
            mlflow_tracker: MLflow tracker instance
        """
        self.mlflow_tracker = mlflow_tracker

    def analyze_high_scoring_runs(
        self,
        min_score: float = 4.0,
        dimension: Optional[str] = None,
        max_runs: int = 50,
    ) -> dict[str, Any]:
        """Analyze patterns in high-scoring runs.

        Args:
            min_score: Minimum overall score (or dimension score)
            dimension: Optional specific dimension to analyze
                      (logo_fidelity_score, layout_clarity_score, etc.)
            max_runs: Maximum number of runs to analyze

        Returns:
            Dictionary with analysis results
        """
        console.print(f"\n[bold]🔍 Analyzing High-Scoring Runs[/bold]")
        console.print(f"Minimum score: {min_score}")
        if dimension:
            console.print(f"Focus dimension: {dimension}")
        console.print()

        # Build filter
        if dimension:
            filter_string = f"metrics.{dimension} >= {min_score}"
        else:
            filter_string = f"metrics.overall_score >= {min_score}"

        # Get runs
        runs = self.mlflow_tracker.list_runs(
            filter_string=filter_string,
            max_results=max_runs,
            order_by=["metrics.overall_score DESC"],
        )

        if not runs:
            console.print("[yellow]No runs found matching criteria[/yellow]")
            return {}

        console.print(f"Found {len(runs)} high-scoring runs")
        console.print("Analyzing prompts...\n")

        # Analyze prompts
        patterns = self._extract_patterns(runs)
        phrases = self._extract_common_phrases(runs)
        correlations = self._find_score_correlations(runs, patterns)

        results = {
            "num_runs": len(runs),
            "min_score": min_score,
            "dimension": dimension,
            "patterns": patterns,
            "phrases": phrases,
            "correlations": correlations,
            "runs": runs,
        }

        self._display_analysis(results)
        return results

    def suggest_improvements(
        self,
        template_id: Optional[str] = None,
        current_prompt: Optional[str] = None,
        min_score: float = 4.0,
    ) -> list[str]:
        """Suggest improvements based on successful patterns.

        Args:
            template_id: Template to analyze (if any)
            current_prompt: Current prompt text to analyze
            min_score: Minimum score for reference runs

        Returns:
            List of improvement suggestions
        """
        console.print(f"\n[bold]💡 Generating Improvement Suggestions[/bold]")
        if template_id:
            console.print(f"Template: {template_id}")
        console.print(f"Reference score: {min_score}+")
        console.print()

        # Get high-scoring runs
        analysis = self.analyze_high_scoring_runs(min_score=min_score, max_runs=30)

        if not analysis:
            return []

        suggestions = []

        # Analyze what's missing from current template/prompt
        if template_id or current_prompt:
            missing_patterns = self._find_missing_patterns(
                current_prompt, analysis["patterns"]
            )
            suggestions.extend(missing_patterns)

        # General suggestions based on correlations
        suggestions.extend(self._generate_general_suggestions(analysis))

        self._display_suggestions(suggestions)
        return suggestions

    def _extract_patterns(self, runs: list[dict]) -> dict[str, int]:
        """Extract common patterns from prompts.

        Args:
            runs: List of run dictionaries

        Returns:
            Dictionary of pattern → count
        """
        patterns = Counter()

        # Patterns to look for (case-insensitive)
        pattern_keywords = [
            # Style keywords
            "professional",
            "clean",
            "modern",
            "minimal",
            "detailed",
            "high contrast",
            "crisp",
            "clear",
            # Layout keywords
            "grid",
            "spacing",
            "alignment",
            "hierarchy",
            "flow",
            # Quality keywords
            "readable",
            "legible",
            "clarity",
            "quality",
            # Color keywords
            "color scheme",
            "colors",
            "palette",
            # Text keywords
            "font",
            "label",
            "text",
            # Logo keywords
            "exactly",
            "uniform",
            "scale",
            "reuse",
        ]

        for run in runs:
            # Get prompt from parameters or try to load from artifact
            prompt_template = run.get("params.prompt_template_id", "")

            # Try to extract prompt text (would need artifact access in real impl)
            # For now, use template ID as proxy
            prompt_text = prompt_template.lower()

            for keyword in pattern_keywords:
                if keyword in prompt_text:
                    patterns[keyword] += 1

        return dict(patterns.most_common(20))

    def _extract_common_phrases(self, runs: list[dict]) -> dict[str, int]:
        """Extract common multi-word phrases.

        Args:
            runs: List of run dictionaries

        Returns:
            Dictionary of phrase → count
        """
        phrases = Counter()

        # Common phrases to track
        common_phrases = [
            "high contrast",
            "professional appearance",
            "clean design",
            "modern style",
            "clear labels",
            "reuse exactly",
            "scale uniformly",
            "no filenames",
            "white background",
            "sentence case",
            "left to right",
            "top to bottom",
        ]

        for run in runs:
            prompt_template = run.get("params.prompt_template_id", "").lower()

            for phrase in common_phrases:
                if phrase in prompt_template:
                    phrases[phrase] += 1

        return dict(phrases.most_common(10))

    def _find_score_correlations(
        self, runs: list[dict], patterns: dict[str, int]
    ) -> dict[str, dict[str, float]]:
        """Find correlations between patterns and scores.

        Args:
            runs: List of run dictionaries
            patterns: Pattern counts

        Returns:
            Dictionary of pattern → {avg_score, correlation}
        """
        correlations = {}

        for pattern in patterns.keys():
            runs_with_pattern = []
            runs_without_pattern = []

            for run in runs:
                template = run.get("params.prompt_template_id", "").lower()
                overall_score = run.get("metrics.overall_score", 0)

                if pattern in template:
                    runs_with_pattern.append(overall_score)
                else:
                    runs_without_pattern.append(overall_score)

            if runs_with_pattern:
                avg_with = sum(runs_with_pattern) / len(runs_with_pattern)
                avg_without = (
                    sum(runs_without_pattern) / len(runs_without_pattern)
                    if runs_without_pattern
                    else 0
                )

                correlations[pattern] = {
                    "avg_score_with": avg_with,
                    "avg_score_without": avg_without,
                    "difference": avg_with - avg_without,
                    "count": len(runs_with_pattern),
                }

        # Sort by difference (positive correlation)
        correlations = dict(
            sorted(correlations.items(), key=lambda x: x[1]["difference"], reverse=True)
        )

        return correlations

    def _find_missing_patterns(
        self, current_prompt: Optional[str], patterns: dict[str, int]
    ) -> list[str]:
        """Find patterns missing from current prompt.

        Args:
            current_prompt: Current prompt text
            patterns: Common patterns

        Returns:
            List of suggestions
        """
        if not current_prompt:
            return []

        suggestions = []
        current_lower = current_prompt.lower()

        for pattern, count in list(patterns.items())[:10]:
            if pattern not in current_lower:
                pct = (count / max(patterns.values())) * 100
                suggestions.append(
                    f"Consider adding '{pattern}' (appears in {pct:.0f}% of high-scoring prompts)"
                )

        return suggestions

    def _generate_general_suggestions(self, analysis: dict) -> list[str]:
        """Generate general suggestions from analysis.

        Args:
            analysis: Analysis results

        Returns:
            List of suggestions
        """
        suggestions = []
        correlations = analysis.get("correlations", {})

        # Top correlated patterns
        top_patterns = list(correlations.items())[:5]
        for pattern, data in top_patterns:
            if data["difference"] > 0.2:  # Significant positive correlation
                suggestions.append(
                    f"Strong correlation: '{pattern}' increases score by "
                    f"{data['difference']:.2f} on average"
                )

        # Common phrases
        phrases = analysis.get("phrases", {})
        if phrases:
            top_phrase = list(phrases.items())[0]
            phrase_name, phrase_count = top_phrase
            total_runs = analysis.get("num_runs", 1)
            pct = (phrase_count / total_runs) * 100
            suggestions.append(
                f"Most common phrase: '{phrase_name}' ({pct:.0f}% of high-scoring runs)"
            )

        return suggestions

    def _display_analysis(self, results: dict) -> None:
        """Display analysis results.

        Args:
            results: Analysis results
        """
        # Summary
        console.print(
            Panel(
                f"Analyzed [bold]{results['num_runs']}[/bold] runs with score ≥ {results['min_score']}",
                title="Analysis Summary",
                border_style="green",
            )
        )
        console.print()

        # Top patterns
        if results["patterns"]:
            table = Table(title="📊 Common Patterns in High-Scoring Runs", show_header=True)
            table.add_column("Pattern", style="cyan")
            table.add_column("Frequency", style="yellow")
            table.add_column("% of Runs", style="green")

            total_runs = results["num_runs"]
            for pattern, count in list(results["patterns"].items())[:10]:
                pct = (count / total_runs) * 100
                table.add_row(pattern, str(count), f"{pct:.0f}%")

            console.print(table)
            console.print()

        # Correlations
        if results["correlations"]:
            table = Table(
                title="🎯 Pattern-Score Correlations", show_header=True, border_style="blue"
            )
            table.add_column("Pattern", style="cyan")
            table.add_column("Avg Score (with)", style="green")
            table.add_column("Avg Score (without)", style="yellow")
            table.add_column("Difference", style="magenta")

            for pattern, data in list(results["correlations"].items())[:8]:
                if data["difference"] > 0:  # Only show positive correlations
                    table.add_row(
                        pattern,
                        f"{data['avg_score_with']:.2f}",
                        f"{data['avg_score_without']:.2f}",
                        f"+{data['difference']:.2f}",
                    )

            console.print(table)
            console.print()

    def _display_suggestions(self, suggestions: list[str]) -> None:
        """Display improvement suggestions.

        Args:
            suggestions: List of suggestions
        """
        if not suggestions:
            console.print("[yellow]No specific suggestions available[/yellow]")
            return

        console.print("\n[bold green]✨ Improvement Suggestions:[/bold green]\n")
        for i, suggestion in enumerate(suggestions, 1):
            console.print(f"  {i}. {suggestion}")

        console.print()

    def template_performance(self) -> dict[str, dict[str, float]]:
        """Analyze performance by template.

        Returns:
            Dictionary of template → {avg_score, count, scores}
        """
        console.print("\n[bold]📈 Template Performance Analysis[/bold]\n")

        # Get all runs
        runs = self.mlflow_tracker.list_runs(max_results=200)

        # Group by template
        template_stats = defaultdict(lambda: {"scores": [], "count": 0})

        for run in runs:
            template = run.get("params.prompt_template_id", "unknown")
            overall_score = run.get("metrics.overall_score")

            if overall_score is not None:
                template_stats[template]["scores"].append(overall_score)
                template_stats[template]["count"] += 1

        # Calculate averages
        results = {}
        for template, data in template_stats.items():
            if data["scores"]:
                results[template] = {
                    "avg_score": sum(data["scores"]) / len(data["scores"]),
                    "count": data["count"],
                    "max_score": max(data["scores"]),
                    "min_score": min(data["scores"]),
                }

        # Display
        if results:
            table = Table(title="Template Performance", show_header=True)
            table.add_column("Template", style="cyan")
            table.add_column("Avg Score", style="yellow")
            table.add_column("Runs", style="blue")
            table.add_column("Range", style="white")

            for template, stats in sorted(
                results.items(), key=lambda x: x[1]["avg_score"], reverse=True
            ):
                table.add_row(
                    template,
                    f"{stats['avg_score']:.2f}",
                    str(stats["count"]),
                    f"{stats['min_score']:.1f} - {stats['max_score']:.1f}",
                )

            console.print(table)
            console.print()

        return results

    def dimension_analysis(self, template_id: Optional[str] = None) -> dict[str, float]:
        """Analyze scores by dimension.

        Args:
            template_id: Optional template to filter by

        Returns:
            Dictionary of dimension → avg_score
        """
        console.print("\n[bold]📊 Score Analysis by Dimension[/bold]\n")

        # Build filter
        filter_string = None
        if template_id:
            filter_string = f"params.prompt_template_id = '{template_id}'"
            console.print(f"Template: {template_id}\n")

        # Get runs
        runs = self.mlflow_tracker.list_runs(
            filter_string=filter_string, max_results=100
        )

        # Collect scores by dimension
        dimensions = {
            "logo_fidelity_score": [],
            "layout_clarity_score": [],
            "text_legibility_score": [],
            "constraint_compliance_score": [],
            "overall_score": [],
        }

        for run in runs:
            for dim in dimensions.keys():
                score = run.get(f"metrics.{dim}")
                if score is not None:
                    dimensions[dim].append(score)

        # Calculate averages
        results = {}
        for dim, scores in dimensions.items():
            if scores:
                results[dim] = sum(scores) / len(scores)

        # Display
        if results:
            table = Table(title="Average Scores by Dimension", show_header=True)
            table.add_column("Dimension", style="cyan")
            table.add_column("Average Score", style="yellow")
            table.add_column("Sample Size", style="blue")

            dim_labels = {
                "logo_fidelity_score": "Logo Fidelity",
                "layout_clarity_score": "Layout Clarity",
                "text_legibility_score": "Text Legibility",
                "constraint_compliance_score": "Constraint Compliance",
                "overall_score": "Overall Score",
            }

            for dim, avg in results.items():
                label = dim_labels.get(dim, dim)
                count = len(dimensions[dim])
                table.add_row(label, f"{avg:.2f}/5", str(count))

            console.print(table)
            console.print()

        return results
