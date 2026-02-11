"""Conversational diagram refinement chatbot orchestration.

Enables iterative refinement of architecture diagrams through a
generate -> evaluate -> feedback -> refine loop.
"""

import json
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import IntPrompt, Prompt
from rich.table import Table

from .config import AppConfig
from .conversation_dspy import ConversationalRefiner
from .gemini_client import GeminiClient
from .logos import LogoKitHandler
from .mlflow_tracker import MLflowTracker
from .models import (
    ConversationConfig,
    ConversationSession,
    ConversationStatus,
    ConversationTurn,
    GenerationSettings,
)
from .prompts import PromptBuilder


# Preset generation settings for quick access
GENERATION_PRESETS = {
    "deterministic": GenerationSettings(temperature=0.0, top_p=1.0, top_k=1),
    "conservative": GenerationSettings(temperature=0.4, top_p=0.9, top_k=30),
    "balanced": GenerationSettings(temperature=0.8, top_p=0.95, top_k=50),
    "creative": GenerationSettings(temperature=1.2, top_p=0.98, top_k=80),
    "wild": GenerationSettings(temperature=1.8, top_p=1.0, top_k=0),
}

console = Console()

# Design principles evaluation prompt for automatic refinement
REFERENCE_IMAGE_ANALYSIS_PROMPT = """Analyze this reference architecture diagram and extract its design patterns and style characteristics.

Identify and describe:
1. **Layout Pattern** - Flow direction, component arrangement, grouping strategy
2. **Visual Style** - Color palette, background, borders, shadows
3. **Typography** - Font styles, label positioning, text hierarchy
4. **Logo Treatment** - Size, placement, spacing around logos
5. **Connection Style** - Arrow types, line weights, connection routing
6. **Overall Composition** - Balance, whitespace usage, visual hierarchy

Provide a concise summary that can be used to guide generation of similar diagrams.
Format your response as a structured description that another AI can use as style guidance."""


# =============================================================================
# LLM Judge Evaluation Prompts - Architecture-First with Persona Overlays
# =============================================================================

# Base evaluation criteria that apply to ALL architecture diagrams
ARCHITECTURE_JUDGE_BASE = """You are an expert Architecture Diagram Judge evaluating diagrams for enterprise presentations.

Your role is to provide ACTIONABLE feedback that will help an AI system generate better diagrams.
Be specific, concrete, and constructive. Avoid vague feedback like "improve layout" - instead say exactly what to change.

CORE EVALUATION CRITERIA (score each 1-5):

1. **Information Hierarchy** - Can viewers grasp the key message in 5 seconds?
   - 5: Clear focal point, obvious data flow, priority components stand out
   - 3: Main message visible but requires study
   - 1: Cluttered, no clear entry point, viewers don't know where to look

2. **Technical Accuracy** - Does the diagram correctly represent architecture patterns?
   - 5: Correct terminology, logical connections, proper component relationships
   - 3: Minor inaccuracies that don't mislead
   - 1: Misleading flows, incorrect relationships, wrong terminology

3. **Logo Fidelity** - Are provided logos used correctly?
   - 5: All logos crisp, unmodified, appropriately sized (40-60px), no filenames shown
   - 3: Minor sizing issues or slight quality loss
   - 1: Logos distorted, replaced with text, or filenames visible

4. **Visual Clarity** - Is the diagram clean and professional?
   - 5: Excellent whitespace, clear groupings, balanced composition
   - 3: Acceptable but some crowding or imbalance
   - 1: Cluttered, overlapping elements, chaotic layout

5. **Data Flow Legibility** - Are connections and relationships clear?
   - 5: Clear directional arrows, logical routing, well-labeled connections
   - 3: Flow mostly understandable with some ambiguity
   - 1: Confusing arrows, crossing lines, unclear relationships

6. **Text Readability** - Is all text legible and well-formatted?
   - 5: Consistent fonts, good contrast, readable at presentation scale
   - 3: Some text hard to read or inconsistent
   - 1: Text illegible, overlapping, or poorly placed"""

# Persona-specific evaluation addendums
PERSONA_ARCHITECT = """

ENTERPRISE SOLUTIONS ARCHITECT LENS (additional criteria):

7. **Integration Patterns** - Are integration points clearly defined?
   - APIs, events, and data flows should show explicit protocol/format hints
   - Synchronous vs asynchronous patterns should be visually distinct

8. **Scalability Indicators** - Does the diagram suggest scale considerations?
   - Horizontal scaling, caching layers, load balancing should be visible if relevant
   - Bottlenecks or single points of failure should be apparent

9. **Security Boundaries** - Are trust zones and security controls visible?
   - Network boundaries, auth points, encryption in transit should be clear
   - Compliance-relevant components should be identifiable

When providing feedback, think: "What would I need to see to approve this for a customer proposal?"
"""

PERSONA_EXECUTIVE = """

EXECUTIVE/CTO LENS (additional criteria):

7. **Strategic Alignment** - Does the diagram tell a business story?
   - Should clearly show value creation or problem resolution
   - Key investments and their impact should be obvious

8. **Cost Topology** - Are expensive components visually identifiable?
   - Compute vs storage vs network costs should be distinguishable
   - Managed services vs self-managed should be clear

9. **Risk Visibility** - Are potential failure points or complexities apparent?
   - Single points of failure, vendor dependencies, or technical debt should be visible
   - Migration or transformation paths should be suggested if relevant

When providing feedback, think: "Would a CTO understand the strategic implications in 30 seconds?"
"""

PERSONA_DEVELOPER = """

DEVELOPER/ENGINEER LENS (additional criteria):

7. **API Contracts** - Are service boundaries and interfaces clear?
   - REST/GraphQL/gRPC distinctions should be visible
   - Data formats and transformation points should be identifiable

8. **Technology Stack** - Are implementation details appropriately shown?
   - Specific technologies, versions, or frameworks should be visible where relevant
   - Build vs buy decisions should be apparent

9. **Debugging Context** - Can developers trace data flow for troubleshooting?
   - Logging, monitoring, and observability points should be visible
   - Error paths and retry mechanisms should be suggested

When providing feedback, think: "Can an engineer implement this without asking clarifying questions?"
"""

EVALUATION_RESPONSE_FORMAT = """

RESPONSE FORMAT (use exactly this JSON structure):
```json
{{
  "scores": {{
    "information_hierarchy": <1-5>,
    "technical_accuracy": <1-5>,
    "logo_fidelity": <1-5>,
    "visual_clarity": <1-5>,
    "data_flow_legibility": <1-5>,
    "text_readability": <1-5>
  }},
  "overall_score": <1-5 weighted average>,
  "strengths": [
    "specific strength 1",
    "specific strength 2"
  ],
  "issues": [
    "specific issue 1 with concrete details",
    "specific issue 2 with concrete details"
  ],
  "actionable_improvements": [
    "SPECIFIC change: e.g., 'Move the data lake icon 20% left and increase to 60px'",
    "SPECIFIC change: e.g., 'Add a dashed line from Spark to Delta Lake showing batch writes'",
    "SPECIFIC change: e.g., 'Replace the generic database icon with the Unity Catalog logo'"
  ],
  "feedback_for_refinement": "A single, detailed paragraph with SPECIFIC instructions for improving this diagram. Include exact positions, sizes, colors, or text changes. This feedback will be used by an AI to generate a better version, so be extremely concrete. Example: 'Increase the Databricks logo to 60px and center it. Move the arrow from S3 to enter from the left side. Add a label showing \"batch ETL\" on the connection to Delta Lake. The current layout crowds the right side - shift the ML serving components down by 30%.'"
}}
```

Evaluate the diagram and respond with ONLY the JSON - no other text."""


def build_evaluation_prompt(persona: str = "architect") -> str:
    """Build the complete evaluation prompt for the LLM Judge.

    Args:
        persona: One of 'architect', 'executive', 'developer', or 'auto'

    Returns:
        Complete evaluation prompt string
    """
    prompt = ARCHITECTURE_JUDGE_BASE

    if persona == "executive":
        prompt += PERSONA_EXECUTIVE
    elif persona == "developer":
        prompt += PERSONA_DEVELOPER
    else:  # architect (default) or auto
        prompt += PERSONA_ARCHITECT

    prompt += EVALUATION_RESPONSE_FORMAT
    return prompt


REFERENCE_COMPARISON_PROMPT = """You are an expert architecture diagram reviewer. Compare the generated diagram against the reference image and evaluate how well it matches the reference style.

REFERENCE IMAGE STYLE:
{reference_style}

EVALUATION CRITERIA (score each 1-5 based on how well it matches the reference):

1. **Layout Match** - Does it follow the same flow direction and component arrangement?
   - 5: Excellent match to reference layout
   - 3: Partial match, some differences
   - 1: Completely different layout

2. **Visual Style Match** - Does it use similar colors, backgrounds, and styling?
   - 5: Consistent with reference style
   - 3: Some style elements match
   - 1: Very different visual style

3. **Typography Match** - Are labels and text styled similarly?
   - 5: Text treatment matches reference
   - 3: Partial match
   - 1: Very different text styling

4. **Logo Treatment** - Are logos sized and positioned similarly?
   - 5: Logo treatment matches reference
   - 3: Some differences in logo handling
   - 1: Very different logo treatment

5. **Overall Quality** - Is it professional and presentation-ready?
   - 5: Excellent quality, matches reference standard
   - 3: Acceptable quality
   - 1: Poor quality

RESPONSE FORMAT (use exactly this JSON structure):
```json
{{
  "scores": {{
    "layout_match": <1-5>,
    "visual_style_match": <1-5>,
    "typography_match": <1-5>,
    "logo_treatment": <1-5>,
    "overall_quality": <1-5>
  }},
  "overall_score": <1-5 weighted average>,
  "differences": [
    "specific difference from reference 1",
    "specific difference from reference 2"
  ],
  "improvements": [
    "how to better match the reference 1",
    "how to better match the reference 2"
  ],
  "feedback_for_refinement": "A single paragraph describing how to modify the diagram to better match the reference style. Be specific and actionable."
}}
```

Evaluate the generated diagram (second image) against the reference (first image) and respond with ONLY the JSON."""


# Legacy prompt kept for reference - now using build_evaluation_prompt() instead
_LEGACY_DESIGN_PRINCIPLES_EVAL_PROMPT = """[DEPRECATED - See build_evaluation_prompt()]"""


class ConversationChatbot:
    """Interactive chatbot for iterative diagram refinement.

    Workflow:
    1. User provides initial prompt or diagram spec
    2. System generates diagram
    3. User scores result (1-5)
    4. User provides feedback
    5. DSPy refines prompt based on conversation history
    6. Repeat until satisfied
    """

    def __init__(
        self,
        config: AppConfig,
        conv_config: Optional[ConversationConfig] = None,
        dspy_model: Optional[str] = None,
    ):
        """Initialize the chatbot.

        Args:
            config: Application configuration
            conv_config: Conversation configuration (uses defaults if not provided)
            dspy_model: Optional Databricks model endpoint for DSPy refinement
        """
        self.config = config
        self.conv_config = conv_config or ConversationConfig()

        # Initialize components
        self.logo_handler = LogoKitHandler(config.logo_kit)
        self.prompt_builder = PromptBuilder(logo_handler=self.logo_handler)
        self.gemini_client = GeminiClient()
        self.mlflow_tracker = MLflowTracker(config.mlflow)

        # Initialize DSPy refiner (deferred to allow for lazy loading)
        self._refiner: Optional[ConversationalRefiner] = None
        self._dspy_model = dspy_model

        # Session state
        self._session: Optional[ConversationSession] = None
        self._logos: list = []
        self._logo_parts: list = []

        # Reference image state
        self._reference_style: Optional[str] = None

    def analyze_reference_image(self, reference_path: Path) -> str:
        """Analyze a reference image to extract design patterns.

        Args:
            reference_path: Path to the reference image

        Returns:
            Style description extracted from the reference
        """
        console.print(f"[bold]Analyzing reference image:[/bold] {reference_path}")

        try:
            style_description = self.gemini_client.analyze_image(
                str(reference_path),
                REFERENCE_IMAGE_ANALYSIS_PROMPT,
                temperature=0.2,
            )
            self._reference_style = style_description
            console.print("[green]Reference style extracted successfully[/green]")
            console.print(Panel(style_description[:500] + "..." if len(style_description) > 500 else style_description,
                               title="Reference Style", border_style="cyan"))
            return style_description
        except Exception as e:
            console.print(f"[yellow]Warning: Could not analyze reference image: {e}[/yellow]")
            return ""

    @property
    def refiner(self) -> ConversationalRefiner:
        """Lazy-load the DSPy refiner."""
        if self._refiner is None:
            console.print("[dim]Initializing DSPy refiner with Databricks...[/dim]")
            self._refiner = ConversationalRefiner(model=self._dspy_model)
        return self._refiner

    def start_session(
        self,
        initial_prompt: str,
    ) -> ConversationSession:
        """Start a new conversation session.

        Args:
            initial_prompt: Prompt text for the session

        Returns:
            New ConversationSession

        Raises:
            ValueError: If no prompt provided
        """
        if not initial_prompt:
            raise ValueError("Must provide initial_prompt")

        # Load logos and hints
        logo_dir = self.conv_config.logo_dir or self.config.logo_kit.logo_dir
        console.print(f"[bold]Loading logos from {logo_dir}...[/bold]")
        self._logos = self.logo_handler.load_logo_kit(logo_dir)
        logo_hints = self.logo_handler.load_logo_hints(logo_dir)
        hints_msg = f" with {len(logo_hints)} hints" if logo_hints else ""
        console.print(f"  Loaded {len(self._logos)} logos{hints_msg}")

        # Convert logos to image parts for generation
        # Strategy: Pass problematic logos (like Unity Catalog) multiple times
        # for better recognition - once at the start and once at the end
        self._logo_parts = []
        unity_catalog_part = None

        for logo in self._logos:
            part = self.logo_handler.to_image_part(logo)
            # Detect Unity Catalog logo (commonly misrendered)
            if "unity" in logo.name.lower() or "catalog" in logo.name.lower():
                unity_catalog_part = part
                # Add Unity Catalog FIRST for prominence
                self._logo_parts.insert(0, part)
            else:
                self._logo_parts.append(part)

        # Add Unity Catalog again at the END for reinforcement
        if unity_catalog_part:
            self._logo_parts.append(unity_catalog_part)
            console.print("  [cyan]Unity Catalog logo prioritized (first & last position)[/cyan]")

        # Prepend logo section to prompt
        logo_section = self.prompt_builder._build_logo_section(self._logos)
        initial_prompt = f"{logo_section}\n\n{initial_prompt}"

        # Create session ID from name or generate random
        if self.conv_config.session_name:
            # Sanitize name for filesystem
            import re
            safe_name = re.sub(r'[^\w\-_]', '_', self.conv_config.session_name)
            session_id = safe_name[:50]  # Limit length
        else:
            session_id = str(uuid.uuid4())[:8]

        self._session = ConversationSession(
            session_id=session_id,
            initial_prompt=initial_prompt,
            created_at=datetime.now().isoformat(),
        )

        console.print(f"\n[bold green]Session started: {session_id}[/bold green]")
        return self._session

    def run_iteration(
        self,
        prompt: str,
        settings: Optional[GenerationSettings] = None,
        is_retry: bool = False,
    ) -> ConversationTurn:
        """Run a single generation iteration.

        Args:
            prompt: The prompt to use for generation
            settings: Optional generation settings (uses config defaults if not provided)
            is_retry: Whether this is a retry of the same prompt with different settings

        Returns:
            ConversationTurn with generation results
        """
        if not self._session:
            raise ValueError("No active session. Call start_session() first.")

        iteration = len(self._session.turns) + 1

        # Use provided settings or fall back to config defaults
        gen_settings = settings or self.conv_config.get_generation_settings()

        # Initialize MLflow
        self.mlflow_tracker.initialize()

        # Start MLflow run
        retry_suffix = "-retry" if is_retry else ""
        run_name = f"chat-{self._session.session_id}-iter-{iteration}{retry_suffix}"
        run_id = self.mlflow_tracker.start_run(run_name=run_name)

        try:
            # Log parameters
            self.mlflow_tracker.log_parameters({
                "session_id": self._session.session_id,
                "iteration": iteration,
                "prompt_template_id": self._session.template_id or "raw",
                "logo_count": len(self._logos),
                "temperature": gen_settings.temperature,
                "top_p": gen_settings.top_p,
                "top_k": gen_settings.top_k if gen_settings.top_k > 0 else None,
                "presence_penalty": gen_settings.presence_penalty,
                "frequency_penalty": gen_settings.frequency_penalty,
                "is_retry": is_retry,
            })

            # Log prompt
            self.mlflow_tracker.log_prompt(prompt, "prompt.txt")

            console.print(f"\n[bold cyan]═══ Iteration {iteration}{retry_suffix} ═══[/bold cyan]")
            console.print(f"[yellow]Generating diagram...[/yellow] [dim]({gen_settings.summary()})[/dim]")

            # Generate image
            start_time = time.time()
            image_bytes, response_text, metadata = self.gemini_client.generate_image(
                prompt=prompt,
                logo_parts=self._logo_parts,
                temperature=gen_settings.temperature,
                top_p=gen_settings.top_p,
                top_k=gen_settings.top_k if gen_settings.top_k > 0 else None,
                presence_penalty=gen_settings.presence_penalty,
                frequency_penalty=gen_settings.frequency_penalty,
            )
            generation_time = time.time() - start_time

            # Save image and prompt
            output_dir = Path("outputs") / datetime.now().strftime("%Y-%m-%d") / f"chat-{self._session.session_id}"
            output_dir.mkdir(parents=True, exist_ok=True)
            image_path = output_dir / f"iteration_{iteration}.png"
            prompt_path = output_dir / f"iteration_{iteration}_prompt.txt"

            with open(image_path, "wb") as f:
                f.write(image_bytes)
            with open(prompt_path, "w") as f:
                f.write(prompt)

            # Log to MLflow
            self.mlflow_tracker.log_output_image(image_path)
            self.mlflow_tracker.log_metrics({
                "generation_time_seconds": generation_time,
                "iteration": iteration,
            })

            console.print(f"[green]Generated in {generation_time:.1f}s[/green]")
            console.print(f"[bold]Image:[/bold] {image_path}")
            console.print(f"[bold]Prompt:[/bold] {prompt_path}")

            # Create turn
            turn = ConversationTurn(
                iteration=iteration,
                prompt_used=prompt,
                run_id=run_id,
                image_path=image_path,
                generation_time_seconds=generation_time,
            )

            # Auto-analyze if enabled (skip if auto_refine - that does its own evaluation)
            if self.conv_config.auto_analyze and not self.conv_config.auto_refine:
                console.print("[dim]Analyzing image...[/dim]")
                try:
                    analysis = self.gemini_client.analyze_image(
                        str(image_path),
                        "Describe this architecture diagram in detail. "
                        "Note: logo placement, text legibility, layout clarity, "
                        "any visual issues, and overall quality."
                    )
                    turn.visual_analysis = analysis
                except Exception as e:
                    console.print(f"[yellow]Analysis failed: {e}[/yellow]")

            # Don't end MLflow run yet - will be ended after scoring
            return turn

        except Exception:
            self.mlflow_tracker.end_run("FAILED")
            raise

    def _parse_retry_command(self, command: str) -> Optional[GenerationSettings]:
        """Parse a retry command and return generation settings.

        Formats supported:
            r / retry                    - retry with slightly different temp (+/-0.1 random)
            r 0.5                        - retry with specific temperature
            r t=0.5                      - retry with specific temperature
            r t=0.5 p=0.9                - retry with temp and top_p
            r deterministic              - use preset
            r conservative               - use preset
            r balanced                   - use preset
            r creative                   - use preset
            r wild                       - use preset

        Returns:
            GenerationSettings if valid retry command, None otherwise
        """
        cmd = command.strip().lower()

        # Check if it's a retry command
        if not (cmd.startswith('r ') or cmd == 'r' or cmd.startswith('retry')):
            return None

        # Extract args after 'r' or 'retry'
        if cmd.startswith('retry'):
            args = cmd[5:].strip()
        else:
            args = cmd[1:].strip()

        # No args - slight random variation
        if not args:
            import random
            base_temp = self.conv_config.temperature
            # Random variation of +/- 0.15
            new_temp = base_temp + random.uniform(-0.15, 0.15)
            new_temp = max(0.0, min(2.0, new_temp))  # Clamp to valid range
            return GenerationSettings(
                temperature=round(new_temp, 2),
                top_p=self.conv_config.top_p,
                top_k=self.conv_config.top_k,
                presence_penalty=self.conv_config.presence_penalty,
                frequency_penalty=self.conv_config.frequency_penalty,
            )

        # Check for preset name
        if args in GENERATION_PRESETS:
            return GENERATION_PRESETS[args]

        # Parse key=value pairs or single temperature value
        settings = GenerationSettings(
            temperature=self.conv_config.temperature,
            top_p=self.conv_config.top_p,
            top_k=self.conv_config.top_k,
            presence_penalty=self.conv_config.presence_penalty,
            frequency_penalty=self.conv_config.frequency_penalty,
        )

        parts = args.split()
        for part in parts:
            if '=' in part:
                key, value = part.split('=', 1)
                try:
                    if key in ('t', 'temp', 'temperature'):
                        settings.temperature = float(value)
                    elif key in ('p', 'top_p'):
                        settings.top_p = float(value)
                    elif key in ('k', 'top_k'):
                        settings.top_k = int(value)
                    elif key in ('pp', 'presence', 'presence_penalty'):
                        settings.presence_penalty = float(value)
                    elif key in ('fp', 'frequency', 'frequency_penalty'):
                        settings.frequency_penalty = float(value)
                except ValueError:
                    pass
            else:
                # Try as bare temperature value
                try:
                    settings.temperature = float(part)
                except ValueError:
                    pass

        return settings

    def collect_feedback(self, turn: ConversationTurn) -> tuple[int, str, Optional[GenerationSettings]]:
        """Collect user feedback for a turn.

        Args:
            turn: The turn to collect feedback for

        Returns:
            Tuple of (score, feedback_text, retry_settings or None)
        """
        console.print("\n[bold]Please review the image:[/bold]")
        console.print(f"  [cyan]{turn.image_path}[/cyan]")

        if turn.visual_analysis:
            console.print("\n[bold]AI Analysis:[/bold]")
            # Truncate long analysis
            analysis = turn.visual_analysis[:500]
            if len(turn.visual_analysis) > 500:
                analysis += "..."
            console.print(Panel(analysis, title="Visual Analysis", border_style="dim"))

        console.print()

        # Get score
        score = IntPrompt.ask(
            "[bold]Score (1-5)[/bold]",
            default=3,
            choices=["1", "2", "3", "4", "5"],
        )

        # Show retry hint
        console.print("[dim]Options:[/dim]")
        console.print("[dim]  • Text feedback → refine prompt[/dim]")
        console.print("[dim]  • 'r' or 'r 0.5' → retry same prompt with different temp[/dim]")
        console.print("[dim]  • 'r creative' → retry with creative preset[/dim]")
        console.print("[dim]  • Image path → use as style reference[/dim]")
        console.print("[dim]  • 'done' → finish session[/dim]")

        feedback = Prompt.ask(
            "[bold]Feedback[/bold]",
            default="",
        )

        # Check for retry command
        retry_settings = self._parse_retry_command(feedback)
        if retry_settings:
            console.print(f"[cyan]Retrying with settings: {retry_settings.summary()}[/cyan]")
            turn.score = score
            turn.feedback = f"[RETRY] {feedback}"
            return score, feedback, retry_settings

        # Check if feedback is a reference image path
        # Only try to parse as path if it's short enough to be a valid filename
        # (avoid "File name too long" errors on long feedback text)
        if feedback and not feedback.lower() == "done" and len(feedback.strip()) < 256:
            try:
                feedback_path = Path(feedback.strip())
                if feedback_path.exists() and feedback_path.suffix.lower() in ['.png', '.jpg', '.jpeg', '.webp', '.gif']:
                    console.print(f"[cyan]Using as reference image: {feedback_path}[/cyan]")
                    # Analyze the reference and get comparison feedback
                    self.analyze_reference_image(feedback_path)
                    self.conv_config.reference_image = feedback_path
                    # Run reference comparison
                    ref_score, ref_feedback = self._evaluate_against_reference(turn)
                    turn.score = ref_score
                    turn.feedback = ref_feedback
                    return ref_score, ref_feedback, None
            except OSError:
                # Path is too long or invalid - treat as regular feedback
                pass

        turn.score = score
        turn.feedback = feedback

        return score, feedback, None

    def auto_evaluate(self, turn: ConversationTurn) -> tuple[int, str]:
        """Automatically evaluate diagram using the LLM Judge.

        The LLM Judge evaluates against architecture best practices with an
        optional persona lens (architect, executive, developer).

        Args:
            turn: The turn to evaluate

        Returns:
            Tuple of (score, feedback_text)
        """
        # Use reference comparison if we have a reference style
        if self._reference_style and self.conv_config.reference_image:
            return self._evaluate_against_reference(turn)

        # Determine persona for evaluation
        persona = self.conv_config.evaluation_persona.value
        persona_display = {
            "architect": "Enterprise Solutions Architect",
            "executive": "Executive/CTO",
            "developer": "Developer/Engineer",
            "auto": "Enterprise Solutions Architect",  # Default for auto
        }.get(persona, "Enterprise Solutions Architect")

        console.print("\n[bold cyan]LLM Judge Evaluation[/bold cyan]")
        console.print(f"  [dim]Persona: {persona_display}[/dim]")
        console.print(f"  [dim]Image: {turn.image_path}[/dim]")

        try:
            # Build evaluation prompt with persona
            eval_prompt = build_evaluation_prompt(persona)

            # Get structured evaluation from Gemini
            eval_response = self.gemini_client.analyze_image(
                str(turn.image_path),
                eval_prompt,
                temperature=0.2,  # Low temp for consistent evaluation
            )

            # Parse JSON response
            import re
            json_match = re.search(r'\{[\s\S]*\}', eval_response)
            if not json_match:
                raise ValueError("No JSON found in evaluation response")

            eval_data = json.loads(json_match.group())

            # Extract scores
            scores = eval_data.get("scores", {})
            overall_score = int(round(eval_data.get("overall_score", 3)))
            strengths = eval_data.get("strengths", [])
            issues = eval_data.get("issues", [])
            actionable_improvements = eval_data.get("actionable_improvements", [])
            feedback = eval_data.get("feedback_for_refinement", "")

            # Display evaluation results
            score_table = Table(title=f"LLM Judge: {persona_display}", show_header=True)
            score_table.add_column("Criterion", style="cyan")
            score_table.add_column("Score", style="magenta", justify="center")

            for criterion, score_val in scores.items():
                label = criterion.replace("_", " ").title()
                color = "green" if score_val >= 4 else "yellow" if score_val >= 3 else "red"
                score_table.add_row(label, f"[{color}]{score_val}/5[/{color}]")

            score_table.add_row("", "")
            overall_color = "green" if overall_score >= 4 else "yellow" if overall_score >= 3 else "red"
            score_table.add_row("[bold]Overall[/bold]", f"[bold {overall_color}]{overall_score}/5[/bold {overall_color}]")

            console.print(score_table)

            if strengths:
                console.print("\n[bold green]Strengths:[/bold green]")
                for strength in strengths[:3]:
                    console.print(f"  ✓ {strength}")

            if issues:
                console.print("\n[bold red]Issues:[/bold red]")
                for issue in issues[:5]:
                    console.print(f"  ✗ {issue}")

            if actionable_improvements:
                console.print("\n[bold yellow]Actionable Improvements:[/bold yellow]")
                for improvement in actionable_improvements[:5]:
                    console.print(f"  → {improvement}")

            # Store analysis details
            turn.visual_analysis = json.dumps(eval_data, indent=2)
            turn.score = overall_score
            turn.feedback = feedback

            console.print("\n[bold]Feedback for DSPy Optimizer:[/bold]")
            console.print(Panel(feedback, border_style="yellow"))

            return overall_score, feedback

        except Exception as e:
            console.print(f"[yellow]Auto-evaluation failed: {e}[/yellow]")
            console.print("[yellow]Falling back to manual feedback...[/yellow]")
            return self.collect_feedback(turn)

    def _evaluate_against_reference(self, turn: ConversationTurn) -> tuple[int, str]:
        """Evaluate diagram by comparing against reference image.

        Args:
            turn: The turn to evaluate

        Returns:
            Tuple of (score, feedback_text)
        """
        console.print("\n[bold cyan]Comparing against reference image...[/bold cyan]")
        console.print(f"  [dim]Generated: {turn.image_path}[/dim]")
        console.print(f"  [dim]Reference: {self.conv_config.reference_image}[/dim]")

        try:
            # Build the comparison prompt with the extracted style
            comparison_prompt = REFERENCE_COMPARISON_PROMPT.format(
                reference_style=self._reference_style
            )

            # Compare images (reference first, generated second)
            eval_response = self.gemini_client.analyze_images(
                [str(self.conv_config.reference_image), str(turn.image_path)],
                comparison_prompt,
                temperature=0.2,
            )

            # Parse JSON response
            import re
            json_match = re.search(r'\{[\s\S]*\}', eval_response)
            if not json_match:
                raise ValueError("No JSON found in evaluation response")

            eval_data = json.loads(json_match.group())

            # Extract scores
            scores = eval_data.get("scores", {})
            overall_score = int(round(eval_data.get("overall_score", 3)))
            differences = eval_data.get("differences", [])
            improvements = eval_data.get("improvements", [])
            feedback = eval_data.get("feedback_for_refinement", "")

            # Display evaluation results
            score_table = Table(title="Reference Comparison", show_header=True)
            score_table.add_column("Criterion", style="cyan")
            score_table.add_column("Score", style="magenta", justify="center")

            for criterion, score_val in scores.items():
                label = criterion.replace("_", " ").title()
                color = "green" if score_val >= 4 else "yellow" if score_val >= 3 else "red"
                score_table.add_row(label, f"[{color}]{score_val}/5[/{color}]")

            score_table.add_row("", "")
            overall_color = "green" if overall_score >= 4 else "yellow" if overall_score >= 3 else "red"
            score_table.add_row("[bold]Overall[/bold]", f"[bold {overall_color}]{overall_score}/5[/bold {overall_color}]")

            console.print(score_table)

            if differences:
                console.print("\n[bold red]Differences from Reference:[/bold red]")
                for diff in differences[:5]:
                    console.print(f"  • {diff}")

            if improvements:
                console.print("\n[bold green]How to Match Reference:[/bold green]")
                for improvement in improvements[:5]:
                    console.print(f"  • {improvement}")

            # Store analysis details
            turn.visual_analysis = json.dumps(eval_data, indent=2)
            turn.score = overall_score
            turn.feedback = feedback

            console.print("\n[bold]Feedback for refinement:[/bold]")
            console.print(Panel(feedback, border_style="yellow"))

            return overall_score, feedback

        except Exception as e:
            console.print(f"[yellow]Reference comparison failed: {e}[/yellow]")
            console.print("[yellow]Falling back to design principles evaluation...[/yellow]")
            # Fall back to standard evaluation
            self._reference_style = None
            return self.auto_evaluate(turn)

    def refine_prompt(
        self,
        current_prompt: str,
        turn: ConversationTurn,
    ) -> str:
        """Refine the prompt based on feedback using DSPy.

        Args:
            current_prompt: The current prompt
            turn: The turn with feedback

        Returns:
            Refined prompt
        """
        console.print("\n[yellow]Refining prompt with DSPy...[/yellow]")
        console.print("[dim]  (This may take 30-60 seconds for Databricks model serving)[/dim]")

        # Get conversation history
        history = self._session.get_history_json() if self._session else "[]"

        # Run refinement with status update
        import time
        start_time = time.time()

        try:
            refined_prompt, reasoning, expected = self.refiner.refine_with_context(
                session_history=history,
                original_prompt=self._session.initial_prompt if self._session else current_prompt,
                current_prompt=current_prompt,
                feedback=turn.feedback or "",
                score=turn.score or 3,
                visual_analysis=turn.visual_analysis or "",
            )
            elapsed = time.time() - start_time
            console.print(f"[dim]  Refinement completed in {elapsed:.1f}s[/dim]")
        except Exception as e:
            elapsed = time.time() - start_time
            console.print(f"[red]  DSPy refinement failed after {elapsed:.1f}s: {e}[/red]")
            console.print("[yellow]  Falling back to appending feedback to prompt...[/yellow]")
            # Fallback: just append feedback to prompt
            feedback_section = f"\n\n---\nREFINEMENT FEEDBACK (MUST ADDRESS):\n{turn.feedback}\n---\n"
            return current_prompt + feedback_section

        # Store reasoning
        turn.refinement_reasoning = reasoning

        console.print("\n[bold]Refinement Reasoning:[/bold]")
        console.print(Panel(reasoning, border_style="cyan"))
        console.print("\n[bold]Expected Improvement:[/bold]")
        console.print(Panel(expected, border_style="green"))

        return refined_prompt

    def run_conversation(self, resume_prompt: Optional[str] = None) -> ConversationSession:
        """Run the full conversation loop.

        Sessions are automatically saved after each turn for crash recovery.
        If interrupted, use resume_session() to continue from the last turn.

        Args:
            resume_prompt: If resuming, the prompt to continue from.
                If None, starts from initial_prompt.

        Returns:
            Completed ConversationSession
        """
        if not self._session:
            raise ValueError("No active session. Call start_session() first.")

        current_prompt = resume_prompt or self._session.initial_prompt
        mode = "Auto-refine" if self.conv_config.auto_refine else "Interactive"
        current_settings: Optional[GenerationSettings] = None

        existing_turns = len(self._session.turns)
        if existing_turns > 0:
            mode_label = f"{mode} (resumed from iteration {existing_turns})"
        else:
            mode_label = mode

        console.print(Panel(
            f"Starting conversation refinement loop\n"
            f"Mode: [bold]{mode_label}[/bold]\n"
            f"Target score: {self.conv_config.target_score}\n"
            f"Max iterations: {self.conv_config.max_iterations}\n"
            + ("" if self.conv_config.auto_refine else "Type 'done' or score target to finish\nType 'r' or 'r <temp>' to retry with different settings"),
            title="Conversation Session",
            border_style="cyan",
        ))

        try:
            while len(self._session.turns) < self.conv_config.max_iterations:
                # Generate (with optional custom settings from retry)
                is_retry = current_settings is not None
                turn = self.run_iteration(current_prompt, settings=current_settings, is_retry=is_retry)

                # Reset settings after use (one-shot for retries)
                current_settings = None

                # Collect feedback (auto or manual)
                retry_settings: Optional[GenerationSettings] = None
                if self.conv_config.auto_refine:
                    score, feedback = self.auto_evaluate(turn)
                else:
                    score, feedback, retry_settings = self.collect_feedback(turn)

                # Log score to MLflow and end the run
                try:
                    self.mlflow_tracker.log_metrics({"score": score})
                    if turn.feedback:
                        self.mlflow_tracker.log_prompt(turn.feedback, "feedback.txt")
                    self.mlflow_tracker.end_run("FINISHED")
                except Exception:
                    pass  # Run may already be ended

                # Add turn to session
                self._session.add_turn(turn)

                # Check if done
                if feedback.lower() == "done" or score >= self.conv_config.target_score:
                    self._session.status = ConversationStatus.COMPLETED
                    console.print("\n[bold green]Target reached! Conversation complete.[/bold green]")
                    break

                # Handle retry vs refine
                if retry_settings:
                    # Retry: same prompt, different settings
                    current_settings = retry_settings
                    console.print(f"\n[cyan]Retrying with: {retry_settings.summary()}[/cyan]")
                    # Don't refine prompt - reuse current_prompt as-is
                else:
                    # Refine: update prompt based on feedback
                    current_prompt = self.refine_prompt(current_prompt, turn)

                # Save session after each turn for crash recovery
                self._save_session(current_prompt=current_prompt)

            else:
                # Max iterations reached
                console.print("\n[yellow]Max iterations reached.[/yellow]")
                self._session.status = ConversationStatus.COMPLETED

        except KeyboardInterrupt:
            console.print("\n[yellow]Session interrupted - saving progress...[/yellow]")
            self._session.status = ConversationStatus.ACTIVE
            session_file = self._save_session(current_prompt=current_prompt)
            console.print(f"[bold green]Progress saved![/bold green]")
            console.print(f"  Resume with: [cyan]nano-banana chat --resume {session_file.parent}[/cyan]")
            self._show_summary()
            return self._session

        # Show summary
        self._show_summary()

        return self._session

    def _show_summary(self) -> None:
        """Display conversation summary."""
        if not self._session:
            return

        console.print("\n[bold]Conversation Summary[/bold]")

        # Create summary table
        table = Table(show_header=True)
        table.add_column("Iter", style="cyan", width=4)
        table.add_column("Score", style="magenta", width=5)
        table.add_column("Time", style="yellow", width=6)
        table.add_column("Feedback", style="white")

        for turn in self._session.turns:
            table.add_row(
                str(turn.iteration),
                str(turn.score) if turn.score else "-",
                f"{turn.generation_time_seconds:.1f}s",
                (turn.feedback or "-")[:50],
            )

        console.print(table)

        # Show best result
        best = self._session.get_best_turn()
        if best:
            console.print(f"\n[bold green]Best result:[/bold green] Iteration {best.iteration} (Score: {best.score})")
            console.print(f"  Image: {best.image_path}")
            console.print(f"  Run ID: {best.run_id}")

        # Save session
        self._save_session()

    def _save_session(self, current_prompt: Optional[str] = None) -> Path:
        """Save session to JSON file for crash recovery.

        Saves full state after every turn so sessions can be resumed
        if interrupted. Includes all data needed to restore the chatbot.

        Args:
            current_prompt: The current/latest prompt (for resume continuity)

        Returns:
            Path to the saved session file
        """
        if not self._session:
            return Path()

        # Use the session's created_at date for consistent output directory
        try:
            created_date = datetime.fromisoformat(self._session.created_at).strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            created_date = datetime.now().strftime("%Y-%m-%d")

        output_dir = Path("outputs") / created_date / f"chat-{self._session.session_id}"
        output_dir.mkdir(parents=True, exist_ok=True)

        session_file = output_dir / "session.json"
        session_data = {
            "session_id": self._session.session_id,
            "initial_prompt": self._session.initial_prompt,
            "current_prompt": current_prompt or self._session.get_latest_prompt(),
            "status": self._session.status.value,
            "created_at": self._session.created_at,
            "diagram_spec_path": str(self._session.diagram_spec_path) if self._session.diagram_spec_path else None,
            "template_id": self._session.template_id,
            "turns": [
                {
                    "iteration": t.iteration,
                    "prompt_used": t.prompt_used,
                    "run_id": t.run_id,
                    "image_path": str(t.image_path),
                    "generation_time_seconds": t.generation_time_seconds,
                    "score": t.score,
                    "feedback": t.feedback,
                    "visual_analysis": t.visual_analysis,
                    "refinement_reasoning": t.refinement_reasoning,
                }
                for t in self._session.turns
            ],
            # Save config for restoration
            "_config": {
                "max_iterations": self.conv_config.max_iterations,
                "target_score": self.conv_config.target_score,
                "auto_analyze": self.conv_config.auto_analyze,
                "auto_refine": self.conv_config.auto_refine,
                "reference_image": str(self.conv_config.reference_image) if self.conv_config.reference_image else None,
                "session_name": self.conv_config.session_name,
                "temperature": self.conv_config.temperature,
                "top_p": self.conv_config.top_p,
                "top_k": self.conv_config.top_k,
                "presence_penalty": self.conv_config.presence_penalty,
                "frequency_penalty": self.conv_config.frequency_penalty,
                "logo_dir": str(self.conv_config.logo_dir) if self.conv_config.logo_dir else None,
                "evaluation_persona": self.conv_config.evaluation_persona.value,
            },
            "_reference_style": self._reference_style,
            "_dspy_model": self._dspy_model,
            "_last_saved": datetime.now().isoformat(),
        }

        with open(session_file, "w") as f:
            json.dump(session_data, f, indent=2)

        console.print(f"[dim]Session saved: {session_file}[/dim]")
        return session_file

    @classmethod
    def find_sessions(cls, base_dir: Path = Path("outputs")) -> list[dict]:
        """Find all saved chat sessions available for resume.

        Args:
            base_dir: Base directory to search (default: outputs/)

        Returns:
            List of session info dicts with path, session_id, turns, status, etc.
        """
        sessions = []

        if not base_dir.exists():
            return sessions

        # Search for session.json files in chat-* directories
        for date_dir in sorted(base_dir.iterdir(), reverse=True):
            if not date_dir.is_dir():
                continue

            for session_dir in date_dir.iterdir():
                if not session_dir.is_dir() or not session_dir.name.startswith("chat-"):
                    continue

                session_file = session_dir / "session.json"
                if session_file.exists():
                    try:
                        data = json.loads(session_file.read_text())
                        sessions.append({
                            "path": session_dir,
                            "session_id": data.get("session_id", "unknown"),
                            "turns": len(data.get("turns", [])),
                            "status": data.get("status", "unknown"),
                            "created_at": data.get("created_at", ""),
                            "last_saved": data.get("_last_saved", ""),
                            "initial_prompt_preview": data.get("initial_prompt", "")[:80],
                        })
                    except (json.JSONDecodeError, KeyError):
                        continue

        return sessions

    @classmethod
    def _reconstruct_session_from_files(cls, session_dir: Path) -> Optional[dict]:
        """Reconstruct session data from iteration files on disk.

        Handles sessions that were interrupted before session.json was written
        (e.g. sessions started before the recovery feature was added, or
        interrupted during the very first iteration).

        Args:
            session_dir: Directory containing iteration_N.png and iteration_N_prompt.txt files

        Returns:
            Reconstructed session data dict, or None if no iteration files found
        """
        import re

        if not session_dir.exists() or not session_dir.is_dir():
            return None

        # Find all iteration prompt files
        prompt_files = sorted(session_dir.glob("iteration_*_prompt.txt"))
        image_files = sorted(session_dir.glob("iteration_*.png"))

        if not prompt_files and not image_files:
            return None

        # Extract session_id from directory name (chat-<session_id>)
        dir_name = session_dir.name
        session_id = dir_name.removeprefix("chat-") if dir_name.startswith("chat-") else dir_name

        # Extract date from parent directory name
        date_str = session_dir.parent.name  # e.g. "2026-02-11"

        # Build turns from files
        turns = []
        iteration_nums = set()

        for pf in prompt_files:
            match = re.search(r'iteration_(\d+)_prompt\.txt', pf.name)
            if match:
                iteration_nums.add(int(match.group(1)))

        for img in image_files:
            match = re.search(r'iteration_(\d+)\.png', img.name)
            if match:
                iteration_nums.add(int(match.group(1)))

        for iteration in sorted(iteration_nums):
            prompt_file = session_dir / f"iteration_{iteration}_prompt.txt"
            image_file = session_dir / f"iteration_{iteration}.png"

            prompt_used = prompt_file.read_text() if prompt_file.exists() else ""

            turns.append({
                "iteration": iteration,
                "prompt_used": prompt_used,
                "run_id": f"reconstructed-{session_id}-iter-{iteration}",
                "image_path": str(image_file) if image_file.exists() else "",
                "generation_time_seconds": 0.0,
                "score": None,
                "feedback": None,
                "visual_analysis": None,
                "refinement_reasoning": None,
            })

        # Use the first iteration's prompt as initial_prompt
        initial_prompt = ""
        if turns:
            initial_prompt = turns[0].get("prompt_used", "")

        # Use the last iteration's prompt as current_prompt
        current_prompt = ""
        if turns:
            current_prompt = turns[-1].get("prompt_used", "")

        console.print(f"  [dim]Reconstructed {len(turns)} turn(s) from iteration files[/dim]")

        return {
            "session_id": session_id,
            "initial_prompt": initial_prompt,
            "current_prompt": current_prompt,
            "status": "active",
            "created_at": f"{date_str}T00:00:00",
            "diagram_spec_path": None,
            "template_id": None,
            "turns": turns,
        }

    @classmethod
    def resume_session(
        cls,
        session_path: Path,
        config: AppConfig,
        dspy_model: Optional[str] = None,
    ) -> tuple["ConversationChatbot", str]:
        """Resume a saved session from disk.

        Restores full chatbot state including session history, config,
        logos, and reference style so the conversation can continue
        seamlessly from where it left off.

        Args:
            session_path: Path to session.json file or session directory
            config: Application configuration
            dspy_model: Optional Databricks model endpoint override

        Returns:
            Tuple of (restored ConversationChatbot, current_prompt to continue from)

        Raises:
            FileNotFoundError: If session file not found
            ValueError: If session data is invalid
        """
        # Handle both file path and directory path
        if session_path.is_dir():
            session_dir = session_path
            session_file = session_path / "session.json"
        else:
            session_dir = session_path.parent
            session_file = session_path

        if not session_file.exists():
            # No session.json - try to reconstruct from iteration files on disk
            # This handles sessions that were interrupted before the first save
            session_data = cls._reconstruct_session_from_files(session_dir)
            if session_data is None:
                raise FileNotFoundError(
                    f"No session.json or iteration files found in {session_dir}"
                )
            console.print("[yellow]No session.json found - reconstructed session from iteration files[/yellow]")
        else:
            # Load session data
            session_data = json.loads(session_file.read_text())

        # Restore conversation config from saved data
        saved_config = session_data.get("_config", {})
        from .models import EvaluationPersona

        conv_config = ConversationConfig(
            max_iterations=saved_config.get("max_iterations", 10),
            target_score=saved_config.get("target_score", 5),
            auto_analyze=saved_config.get("auto_analyze", True),
            auto_refine=saved_config.get("auto_refine", False),
            reference_image=Path(saved_config["reference_image"]) if saved_config.get("reference_image") else None,
            session_name=saved_config.get("session_name"),
            temperature=saved_config.get("temperature", 0.8),
            top_p=saved_config.get("top_p", 0.95),
            top_k=saved_config.get("top_k", 50),
            presence_penalty=saved_config.get("presence_penalty", 0.1),
            frequency_penalty=saved_config.get("frequency_penalty", 0.1),
            logo_dir=Path(saved_config["logo_dir"]) if saved_config.get("logo_dir") else None,
            evaluation_persona=EvaluationPersona(saved_config.get("evaluation_persona", "architect")),
        )

        # Use saved dspy_model unless overridden
        restored_dspy_model = dspy_model or session_data.get("_dspy_model")

        # Create chatbot instance
        chatbot = cls(
            config=config,
            conv_config=conv_config,
            dspy_model=restored_dspy_model,
        )

        # Load logos
        logo_dir = conv_config.logo_dir or config.logo_kit.logo_dir
        console.print(f"[bold]Loading logos from {logo_dir}...[/bold]")
        chatbot._logos = chatbot.logo_handler.load_logo_kit(logo_dir)
        logo_hints = chatbot.logo_handler.load_logo_hints(logo_dir)
        hints_msg = f" with {len(logo_hints)} hints" if logo_hints else ""
        console.print(f"  Loaded {len(chatbot._logos)} logos{hints_msg}")

        # Rebuild logo parts (same strategy as start_session)
        chatbot._logo_parts = []
        unity_catalog_part = None

        for logo in chatbot._logos:
            part = chatbot.logo_handler.to_image_part(logo)
            if "unity" in logo.name.lower() or "catalog" in logo.name.lower():
                unity_catalog_part = part
                chatbot._logo_parts.insert(0, part)
            else:
                chatbot._logo_parts.append(part)

        if unity_catalog_part:
            chatbot._logo_parts.append(unity_catalog_part)
            console.print("  [cyan]Unity Catalog logo prioritized (first & last position)[/cyan]")

        # Determine session directory for reading prompt files
        session_dir = session_file.parent

        # Recover initial_prompt from saved data or from iteration_1_prompt.txt
        initial_prompt = session_data.get("initial_prompt", "")
        if not initial_prompt:
            iter1_prompt_file = session_dir / "iteration_1_prompt.txt"
            if iter1_prompt_file.exists():
                initial_prompt = iter1_prompt_file.read_text()
                console.print("[dim]  Recovered initial_prompt from iteration_1_prompt.txt[/dim]")

        # Restore session state
        chatbot._session = ConversationSession(
            session_id=session_data["session_id"],
            initial_prompt=initial_prompt,
            created_at=session_data.get("created_at", datetime.now().isoformat()),
            status=ConversationStatus(session_data.get("status", "active")),
            template_id=session_data.get("template_id"),
            diagram_spec_path=Path(session_data["diagram_spec_path"]) if session_data.get("diagram_spec_path") else None,
        )

        # Restore turns, recovering prompt_used from disk if not in session data
        for turn_data in session_data.get("turns", []):
            prompt_used = turn_data.get("prompt_used", "")
            if not prompt_used:
                # Fall back to reading iteration_N_prompt.txt from disk
                iter_prompt_file = session_dir / f"iteration_{turn_data['iteration']}_prompt.txt"
                if iter_prompt_file.exists():
                    prompt_used = iter_prompt_file.read_text()

            turn = ConversationTurn(
                iteration=turn_data["iteration"],
                prompt_used=prompt_used,
                run_id=turn_data["run_id"],
                image_path=Path(turn_data["image_path"]),
                generation_time_seconds=turn_data["generation_time_seconds"],
                score=turn_data.get("score"),
                feedback=turn_data.get("feedback"),
                visual_analysis=turn_data.get("visual_analysis"),
                refinement_reasoning=turn_data.get("refinement_reasoning"),
            )
            chatbot._session.add_turn(turn)

        # Restore reference style
        chatbot._reference_style = session_data.get("_reference_style")

        # Determine the prompt to continue from:
        # 1. Explicit current_prompt saved in session (best - includes refined prompt)
        # 2. Latest turn's prompt_used (fallback)
        # 3. initial_prompt (last resort)
        current_prompt = session_data.get("current_prompt") or chatbot._session.get_latest_prompt()

        num_turns = len(chatbot._session.turns)
        console.print(f"\n[bold green]Session restored: {chatbot._session.session_id}[/bold green]")
        console.print(f"  Turns completed: {num_turns}")
        console.print(f"  Remaining iterations: {conv_config.max_iterations - num_turns}")
        if chatbot._session.turns:
            last_turn = chatbot._session.turns[-1]
            console.print(f"  Last score: {last_turn.score or 'N/A'}")
            console.print(f"  Last image: {last_turn.image_path}")

        return chatbot, current_prompt
