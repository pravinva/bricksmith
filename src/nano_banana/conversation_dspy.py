"""DSPy signatures and modules for conversational diagram refinement.

Uses DSPy with Databricks model serving endpoints for prompt refinement
based on conversation history, user feedback, and visual analysis.
"""

import os
from typing import Optional

import dspy


class ConversationalRefinementSignature(dspy.Signature):
    """Refine a diagram prompt based on conversation history and feedback.

    Given the original prompt, current prompt, conversation history, user feedback,
    current score, and visual analysis, generate an improved prompt that addresses
    the user's concerns while maintaining diagram quality.
    """

    original_prompt: str = dspy.InputField(
        desc="The original/initial prompt that started the conversation"
    )
    current_prompt: str = dspy.InputField(
        desc="The most recent prompt used for generation"
    )
    conversation_history: str = dspy.InputField(
        desc="JSON array of previous turns with scores, feedback, and analysis"
    )
    current_feedback: str = dspy.InputField(
        desc="User's feedback on the current generation"
    )
    current_score: str = dspy.InputField(
        desc="User's score (1-5) for the current generation"
    )
    visual_analysis: str = dspy.InputField(
        desc="AI analysis of what the current diagram looks like"
    )

    refined_prompt: str = dspy.OutputField(
        desc="The improved prompt that addresses all feedback and issues. "
        "Must preserve logo constraints and critical requirements from the original."
    )
    reasoning: str = dspy.OutputField(
        desc="Explanation of what changes were made and why"
    )
    expected_improvement: str = dspy.OutputField(
        desc="What improvements to expect in the next generation"
    )


class PromptAnalysisSignature(dspy.Signature):
    """Analyze a diagram and its prompt to identify issues.

    Used when the user doesn't provide specific feedback to help identify
    what might need improvement.
    """

    prompt_text: str = dspy.InputField(desc="The prompt used to generate the diagram")
    visual_analysis: str = dspy.InputField(
        desc="AI description of what the generated diagram looks like"
    )
    user_score: str = dspy.InputField(desc="User's score (1-5)")

    issues_identified: str = dspy.OutputField(
        desc="List of specific issues found in the diagram based on the analysis"
    )
    suggested_improvements: str = dspy.OutputField(
        desc="Concrete suggestions for improving the prompt"
    )


class ConversationalRefiner(dspy.Module):
    """DSPy module for iterative prompt refinement through conversation.

    Uses Databricks model serving endpoints with Claude or Llama models.
    """

    # Available Databricks model endpoints (in order of preference/capability)
    DATABRICKS_MODELS = [
        "databricks-claude-opus-4-5",  # Most powerful
        "databricks-claude-sonnet-4",  # Fast and capable
        "databricks-meta-llama-3-3-70b-instruct",  # Open source alternative
        "databricks-meta-llama-3-1-70b-instruct",  # Fallback
    ]

    def __init__(
        self,
        model: Optional[str] = None,
        databricks_host: Optional[str] = None,
        databricks_token: Optional[str] = None,
    ):
        """Initialize the refiner with Databricks model serving.

        Args:
            model: Databricks model endpoint name. Defaults to most powerful available.
            databricks_host: Databricks workspace URL. Uses DATABRICKS_HOST env var if not provided.
            databricks_token: Databricks access token. Uses DATABRICKS_TOKEN env var if not provided.
        """
        super().__init__()

        # Get Databricks credentials
        self.databricks_host = databricks_host or os.getenv("DATABRICKS_HOST")
        self.databricks_token = databricks_token or os.getenv("DATABRICKS_TOKEN")

        if not self.databricks_host:
            raise ValueError(
                "Databricks host required. Set DATABRICKS_HOST environment variable "
                "or pass databricks_host parameter."
            )
        if not self.databricks_token:
            raise ValueError(
                "Databricks token required. Set DATABRICKS_TOKEN environment variable "
                "or pass databricks_token parameter."
            )

        # Configure LiteLLM environment for Databricks (used by DSPy 3.x)
        os.environ["DATABRICKS_API_KEY"] = self.databricks_token
        os.environ["DATABRICKS_API_BASE"] = f"{self.databricks_host.rstrip('/')}/serving-endpoints"

        # Use specified model or default to most powerful
        self.model_name = model or self.DATABRICKS_MODELS[0]

        # Configure DSPy with Databricks model serving (DSPy 3.x uses dspy.LM with LiteLLM)
        self.lm = dspy.LM(
            model=f"databricks/{self.model_name}",
            max_tokens=4096,
            temperature=0.3,  # Lower temperature for more focused refinement
        )

        # Set as default LM for this module
        dspy.settings.configure(lm=self.lm)

        # Initialize chain-of-thought modules
        self.refine = dspy.ChainOfThought(ConversationalRefinementSignature)
        self.analyze = dspy.ChainOfThought(PromptAnalysisSignature)

    def forward(
        self,
        original_prompt: str,
        current_prompt: str,
        conversation_history: str,
        current_feedback: str,
        current_score: str,
        visual_analysis: str,
    ) -> dspy.Prediction:
        """Refine the prompt based on all available context.

        Args:
            original_prompt: The initial prompt
            current_prompt: Most recent prompt
            conversation_history: JSON of previous turns
            current_feedback: User's current feedback
            current_score: User's current score (1-5)
            visual_analysis: AI analysis of current image

        Returns:
            Prediction with refined_prompt, reasoning, expected_improvement
        """
        return self.refine(
            original_prompt=original_prompt,
            current_prompt=current_prompt,
            conversation_history=conversation_history,
            current_feedback=current_feedback,
            current_score=current_score,
            visual_analysis=visual_analysis,
        )

    def analyze_issues(
        self,
        prompt_text: str,
        visual_analysis: str,
        user_score: str,
    ) -> dspy.Prediction:
        """Analyze diagram issues when user doesn't provide specific feedback.

        Args:
            prompt_text: The prompt used
            visual_analysis: AI analysis of the image
            user_score: User's score

        Returns:
            Prediction with issues_identified and suggested_improvements
        """
        return self.analyze(
            prompt_text=prompt_text,
            visual_analysis=visual_analysis,
            user_score=user_score,
        )

    def refine_with_context(
        self,
        session_history: str,
        original_prompt: str,
        current_prompt: str,
        feedback: str,
        score: int,
        visual_analysis: str = "",
    ) -> tuple[str, str, str]:
        """Convenience method for refinement with full context.

        Args:
            session_history: JSON string of conversation history
            original_prompt: Initial prompt
            current_prompt: Latest prompt
            feedback: User feedback
            score: User score (1-5)
            visual_analysis: Optional visual analysis

        Returns:
            Tuple of (refined_prompt, reasoning, expected_improvement)
        """
        # If no feedback provided and score is low, try to analyze issues
        if not feedback.strip() and score < 4:
            if visual_analysis:
                analysis = self.analyze_issues(
                    prompt_text=current_prompt,
                    visual_analysis=visual_analysis,
                    user_score=str(score),
                )
                feedback = f"Auto-identified issues: {analysis.issues_identified}"

        result = self(
            original_prompt=original_prompt,
            current_prompt=current_prompt,
            conversation_history=session_history,
            current_feedback=feedback or "No specific feedback provided",
            current_score=str(score),
            visual_analysis=visual_analysis or "No visual analysis available",
        )

        return (
            result.refined_prompt,
            result.reasoning,
            result.expected_improvement,
        )
