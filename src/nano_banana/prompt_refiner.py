"""Visual prompt refinement using image analysis."""

from pathlib import Path
from typing import Optional

from .gemini_client import GeminiClient
from .mlflow_tracker import MLflowTracker
from .models import PromptRefinement
from .prompts import PromptBuilder


class PromptRefiner:
    """Refines prompts using visual analysis of generated diagrams."""

    def __init__(
        self,
        gemini_client: GeminiClient,
        mlflow_tracker: MLflowTracker,
        prompt_builder: PromptBuilder,
    ):
        """Initialize prompt refiner.

        Args:
            gemini_client: Gemini client for image analysis
            mlflow_tracker: MLflow tracker for loading runs
            prompt_builder: Prompt builder for template management
        """
        self.gemini_client = gemini_client
        self.mlflow_tracker = mlflow_tracker
        self.prompt_builder = prompt_builder

    def analyze_diagram(
        self,
        image_path: Path,
        original_prompt: str,
        user_feedback: Optional[str] = None,
    ) -> dict[str, any]:
        """Analyze a diagram image and identify strengths/weaknesses.

        Args:
            image_path: Path to diagram image
            original_prompt: The prompt used to generate this diagram
            diagram_spec: Optional diagram specification for context
            user_feedback: Optional user feedback about the diagram

        Returns:
            Analysis dict with strengths, weaknesses, and observations
        """
        analysis_prompt = self._build_analysis_prompt(
            original_prompt, user_feedback
        )

        # Use Gemini vision to analyze the image
        response = self.gemini_client.analyze_image(
            image_path=image_path,
            prompt=analysis_prompt,
        )

        return self._parse_analysis_response(response)

    def suggest_improvements(
        self,
        image_path: Path,
        original_prompt: str,
        user_feedback: Optional[str] = None,
    ) -> PromptRefinement:
        """Generate concrete prompt improvement suggestions.

        Args:
            image_path: Path to diagram image
            original_prompt: The prompt used to generate this diagram
            diagram_spec: Optional diagram specification
            user_feedback: Optional user feedback

        Returns:
            PromptRefinement with suggested changes
        """
        # First, analyze the diagram
        analysis = self.analyze_diagram(
            image_path, original_prompt, user_feedback
        )

        # Generate improvement suggestions
        refinement_prompt = self._build_refinement_prompt(
            original_prompt, analysis, user_feedback
        )

        response = self.gemini_client.generate_text(refinement_prompt)

        return self._parse_refinement_response(response, original_prompt, analysis)

    def refine_from_run(
        self,
        run_id: str,
        user_feedback: Optional[str] = None,
    ) -> PromptRefinement:
        """Analyze a previous MLflow run and suggest improvements.

        Args:
            run_id: MLflow run ID to analyze
            user_feedback: Optional user feedback about the run

        Returns:
            PromptRefinement with suggested changes
        """
        # Load run artifacts from MLflow
        run = self.mlflow_tracker.get_run(run_id)

        # Download artifacts
        diagram_path = self.mlflow_tracker.download_artifact(run_id, "diagram.png")
        prompt_path = self.mlflow_tracker.download_artifact(run_id, "prompt.txt")

        # Load prompt
        with open(prompt_path) as f:
            original_prompt = f.read()

        return self.suggest_improvements(
            diagram_path, original_prompt, user_feedback
        )

    def compare_diagrams(
        self,
        good_run_id: str,
        bad_run_id: str,
    ) -> dict[str, any]:
        """Compare two diagrams to extract what makes one better.

        Args:
            good_run_id: MLflow run ID of the better diagram
            bad_run_id: MLflow run ID of the worse diagram

        Returns:
            Dict with comparative analysis
        """
        # Load both runs
        good_diagram = self.mlflow_tracker.download_artifact(good_run_id, "diagram.png")
        bad_diagram = self.mlflow_tracker.download_artifact(bad_run_id, "diagram.png")

        good_prompt_path = self.mlflow_tracker.download_artifact(good_run_id, "prompt.txt")
        bad_prompt_path = self.mlflow_tracker.download_artifact(bad_run_id, "prompt.txt")

        with open(good_prompt_path) as f:
            good_prompt = f.read()
        with open(bad_prompt_path) as f:
            bad_prompt = f.read()

        # Build comparison prompt
        comparison_prompt = f"""
        I have two architecture diagrams generated with different prompts.

        Diagram A (better) was generated with:
        {good_prompt}

        Diagram B (worse) was generated with:
        {bad_prompt}

        Analyze both diagrams and identify:
        1. What visual elements are better in Diagram A
        2. What prompt elements likely caused those improvements
        3. Specific prompt changes that would make B look more like A

        Focus on concrete, actionable differences.
        """

        # Use Gemini to analyze both images
        response = self.gemini_client.analyze_images(
            image_paths=[good_diagram, bad_diagram],
            prompt=comparison_prompt,
        )

        return self._parse_comparison_response(response)

    def _build_analysis_prompt(
        self,
        original_prompt: str,
        user_feedback: Optional[str],
    ) -> str:
        """Build prompt for diagram analysis."""
        prompt = f"""
        Analyze this architecture diagram that was generated with the following prompt:

        ```
        {original_prompt}
        ```

        """

        if user_feedback:
            prompt += f"""
        User feedback: {user_feedback}

        """

        prompt += """
        Evaluate the diagram on:

        1. **Logo Fidelity**: Are logos reused exactly? Any distortion? Any filenames visible?
        2. **Layout Clarity**: Is the flow clear? Good spacing? Logical grouping?
        3. **Text Legibility**: Are all labels readable? Good font sizes?
        4. **Constraint Compliance**: Does it follow the specified requirements?

        For each dimension, identify:
        - What worked well (strengths)
        - What didn't work (weaknesses)
        - What's missing

        Be specific and concrete. Reference actual visual elements.
        """

        return prompt

    def _build_refinement_prompt(
        self,
        original_prompt: str,
        analysis: dict[str, any],
        user_feedback: Optional[str],
    ) -> str:
        """Build prompt for generating refinement suggestions."""
        prompt = f"""
        Based on this analysis of a generated diagram:

        Strengths: {analysis.get('strengths', [])}
        Weaknesses: {analysis.get('weaknesses', [])}

        Original prompt:
        ```
        {original_prompt}
        ```

        """

        if user_feedback:
            prompt += f"User feedback: {user_feedback}\n\n"

        prompt += """
        Generate a refined version of the prompt that:
        1. Preserves what worked (the strengths)
        2. Addresses the weaknesses with specific instructions
        3. Is concrete and actionable (avoid vague terms like "better" or "more")

        Provide:
        - The refined prompt (full text)
        - Explanation of key changes
        - Expected improvements

        Format as:
        REFINED PROMPT:
        [full prompt text]

        KEY CHANGES:
        - [change 1]
        - [change 2]

        EXPECTED IMPROVEMENTS:
        - [improvement 1]
        - [improvement 2]
        """

        return prompt

    def _parse_analysis_response(self, response: str) -> dict[str, any]:
        """Parse Gemini's analysis response into structured data."""
        # This would parse the response into strengths/weaknesses/observations
        # Placeholder implementation
        return {
            "strengths": [],
            "weaknesses": [],
            "observations": response,
        }

    def _parse_refinement_response(
        self, response: str, original_prompt: str, analysis: dict
    ) -> PromptRefinement:
        """Parse refinement response into PromptRefinement object."""
        # Parse the structured response
        # Placeholder implementation
        sections = response.split("REFINED PROMPT:")

        if len(sections) > 1:
            refined_section = sections[1].split("KEY CHANGES:")[0].strip()
        else:
            refined_section = original_prompt

        return PromptRefinement(
            original_prompt=original_prompt,
            refined_prompt=refined_section,
            changes=[],
            expected_improvements=[],
            analysis=analysis,
        )

    def _parse_comparison_response(self, response: str) -> dict[str, any]:
        """Parse comparison response into structured data."""
        return {
            "visual_differences": [],
            "prompt_differences": [],
            "recommendations": [],
            "raw_analysis": response,
        }
