"""DSPy signatures and modules for collaborative architecture design.

Uses DSPy with Databricks model serving endpoints to facilitate
natural conversations about architecture design and generate
diagram prompts.
"""

import os
from typing import Optional

import dspy


class ArchitectConversationSignature(dspy.Signature):
    """Solutions architect conversation turn.

    Act as an expert Databricks solutions architect. Analyze the user's input,
    ask clarifying questions when needed, propose architecture solutions,
    and help refine the design through natural conversation.

    You should:
    - Ask clarifying questions when requirements are unclear
    - Propose concrete architecture components when you have enough information
    - Suggest connections and data flows between components
    - Consider scalability, cost, and operational concerns
    - Use available logos when referencing technologies
    - If a reference prompt is provided, use it as inspiration for style and structure
    """

    user_message: str = dspy.InputField(
        desc="The user's current message or response"
    )
    conversation_history: str = dspy.InputField(
        desc="JSON array of previous conversation turns"
    )
    available_logos: str = dspy.InputField(
        desc="Comma-separated list of logo names available for the diagram"
    )
    custom_context: str = dspy.InputField(
        desc="Optional domain knowledge or customer context"
    )
    current_architecture: str = dspy.InputField(
        desc="JSON object with current components and connections"
    )
    reference_prompt: str = dspy.InputField(
        desc="Optional existing diagram prompt to use as reference for style/structure. "
        "Extract components, connections, and design patterns from this if provided."
    )

    response: str = dspy.OutputField(
        desc="Natural language response to the user. Ask questions, propose solutions, "
        "or acknowledge feedback. Be conversational but focused on architecture."
    )
    updated_architecture: str = dspy.OutputField(
        desc="JSON object with updated components and connections based on this turn. "
        "Format: {\"components\": [{\"id\": \"...\", \"label\": \"...\", \"type\": \"...\", "
        "\"logo_name\": \"...\"}], \"connections\": [{\"from_id\": \"...\", \"to_id\": \"...\", "
        "\"label\": \"...\"}]}. Return existing architecture if no changes."
    )
    ready_for_output: str = dspy.OutputField(
        desc="'yes' if enough information has been gathered to generate a complete "
        "diagram prompt, 'no' if more discussion is needed. Only say 'yes' when "
        "the architecture has at least 3 components and clear data flows."
    )


class ArchitectPromptGenerationSignature(dspy.Signature):
    """Generate a high-quality diagram prompt from the architect conversation.

    Create a professional prompt suitable for Gemini image generation that
    captures the architecture discussed in the conversation. The prompt should
    match the quality and structure of consulting-firm architecture diagrams.
    """

    conversation_summary: str = dspy.InputField(
        desc="Summary of key architectural decisions from the conversation"
    )
    architecture_json: str = dspy.InputField(
        desc="JSON object with final components and connections"
    )
    available_logos: str = dspy.InputField(
        desc="Comma-separated list of logo names available for the diagram"
    )
    style_preferences: str = dspy.InputField(
        desc="Any stated visual preferences or requirements"
    )

    diagram_prompt: str = dspy.OutputField(
        desc="Complete prompt for diagram generation. Include: "
        "1) LOGO KIT section with available logos and rules "
        "2) DESIGN PHILOSOPHY with target audience and visual style "
        "3) CANVAS & TYPOGRAPHY specifications "
        "4) DIAGRAM CONTENT with detailed component and connection descriptions "
        "5) VISUAL RULES with DO/DO NOT guidelines. "
        "Make it professional and detailed enough for high-quality generation."
    )
    prompt_rationale: str = dspy.OutputField(
        desc="Brief explanation of the prompt structure and key design choices"
    )


class ArchitectRefiner(dspy.Module):
    """DSPy module for collaborative architecture design conversations.

    Facilitates natural back-and-forth discussions about architecture,
    tracking proposed components and connections, and eventually
    generating a diagram prompt.
    """

    # Available Databricks model endpoints (in order of preference)
    DATABRICKS_MODELS = [
        "databricks-claude-opus-4-5",
        "databricks-claude-sonnet-4",
        "databricks-meta-llama-3-3-70b-instruct",
        "databricks-meta-llama-3-1-70b-instruct",
    ]

    def __init__(
        self,
        model: Optional[str] = None,
        databricks_host: Optional[str] = None,
        databricks_token: Optional[str] = None,
    ):
        """Initialize the architect refiner with Databricks model serving.

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

        # Configure LiteLLM environment for Databricks
        os.environ["DATABRICKS_API_KEY"] = self.databricks_token
        os.environ["DATABRICKS_API_BASE"] = f"{self.databricks_host.rstrip('/')}/serving-endpoints"

        # Use specified model or default to most powerful
        self.model_name = model or self.DATABRICKS_MODELS[0]

        # Configure DSPy with Databricks model serving
        # Use high max_tokens to handle long diagram prompts (can be 8000+ tokens)
        self.lm = dspy.LM(
            model=f"databricks/{self.model_name}",
            max_tokens=16384,
            temperature=0.4,  # Slightly higher for more conversational responses
        )

        # Set as default LM for this module
        dspy.settings.configure(lm=self.lm)

        # Initialize chain-of-thought modules
        self.converse = dspy.ChainOfThought(ArchitectConversationSignature)
        self.generate_prompt = dspy.ChainOfThought(ArchitectPromptGenerationSignature)

    def forward(
        self,
        user_message: str,
        conversation_history: str,
        available_logos: str,
        custom_context: str,
        current_architecture: str,
        reference_prompt: str = "",
    ) -> dspy.Prediction:
        """Process a conversation turn.

        Args:
            user_message: User's current input
            conversation_history: JSON of previous turns
            available_logos: Available logo names
            custom_context: Domain/customer context
            current_architecture: Current architecture JSON
            reference_prompt: Optional existing prompt to use as reference

        Returns:
            Prediction with response, updated_architecture, ready_for_output
        """
        return self.converse(
            user_message=user_message,
            conversation_history=conversation_history,
            available_logos=available_logos,
            custom_context=custom_context or "No additional context provided.",
            current_architecture=current_architecture,
            reference_prompt=reference_prompt or "No reference prompt provided.",
        )

    def create_diagram_prompt(
        self,
        conversation_summary: str,
        architecture_json: str,
        available_logos: str,
        style_preferences: str = "",
    ) -> tuple[str, str]:
        """Generate a diagram prompt from the conversation.

        Args:
            conversation_summary: Summary of key decisions
            architecture_json: Final architecture JSON
            available_logos: Available logo names
            style_preferences: Visual preferences

        Returns:
            Tuple of (diagram_prompt, rationale)
        """
        result = self.generate_prompt(
            conversation_summary=conversation_summary,
            architecture_json=architecture_json,
            available_logos=available_logos,
            style_preferences=style_preferences or "Professional, clean, consulting-firm quality",
        )

        return result.diagram_prompt, result.prompt_rationale

    def process_turn(
        self,
        user_message: str,
        conversation_history: str,
        available_logos: str,
        current_architecture: str,
        custom_context: str = "",
        reference_prompt: str = "",
    ) -> tuple[str, dict, bool]:
        """Convenience method for processing a conversation turn.

        Args:
            user_message: User's current input
            conversation_history: JSON of previous turns
            available_logos: Available logo names
            current_architecture: Current architecture JSON
            custom_context: Optional domain context
            reference_prompt: Optional existing prompt to use as reference

        Returns:
            Tuple of (response, updated_architecture_dict, ready_for_output)
        """
        import json

        result = self(
            user_message=user_message,
            conversation_history=conversation_history,
            available_logos=available_logos,
            custom_context=custom_context,
            current_architecture=current_architecture,
            reference_prompt=reference_prompt,
        )

        # Parse the updated architecture
        try:
            updated_arch = json.loads(result.updated_architecture)
        except json.JSONDecodeError:
            # If parsing fails, return the current architecture
            updated_arch = json.loads(current_architecture)

        # Determine if ready for output
        ready = result.ready_for_output.lower().strip() == "yes"

        return result.response, updated_arch, ready
