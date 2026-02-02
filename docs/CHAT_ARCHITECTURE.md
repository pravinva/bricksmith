# Chat System Architecture

This document explains the technical architecture of the conversational diagram refinement system.

## Overview

The chat system provides an interactive loop for iterative diagram improvement through a conversation-based interface. It combines Gemini for image generation, DSPy for prompt refinement, and MLflow for experiment tracking.

## System Components

### 1. Conversation Module (`conversation.py`)

The main orchestrator that manages the refinement loop.

**Key Classes:**

- `ConversationBot`: Main class managing the conversation session
  - Handles iteration loop
  - Manages state between turns
  - Coordinates between generation, evaluation, and refinement
  - Tracks conversation history

**Core Methods:**

```python
def run_conversation(self) -> ConversationSession:
    """
    Main entry point. Runs the complete refinement loop:
    1. Generate initial diagram
    2. Get user feedback (or auto-evaluate)
    3. Refine prompt with DSPy
    4. Repeat until done
    
    Returns ConversationSession with full history
    """

def run_iteration(self, prompt: str) -> ConversationTurn:
    """
    Execute a single refinement iteration:
    - Generate diagram with Gemini
    - Log to MLflow
    - Get feedback (manual or auto)
    - Refine prompt with DSPy
    
    Returns ConversationTurn with iteration results
    """
```

**State Management:**

The conversation maintains state across iterations:
- Current prompt text
- Conversation history (all turns)
- Score progression
- Generated images
- Feedback provided
- Refinement reasoning

### 2. DSPy Optimizer (`conversation_dspy.py`)

Uses DSPy framework for intelligent prompt refinement.

**Key Classes:**

- `ConversationalRefiner`: DSPy module for prompt optimization
- `AutoRefineEvaluator`: Automated diagram evaluation

**Refinement Process:**

```python
class ConversationalRefiner(dspy.Module):
    """
    DSPy module that takes:
    - Conversation history
    - Current prompt
    - User feedback
    - Score
    - Visual analysis
    
    And produces:
    - Refined prompt
    - Reasoning for changes
    - Expected improvements
    """
```

**How it works:**

1. **Input Analysis**: Processes conversation history to understand context
2. **Feedback Integration**: Incorporates user feedback into refinement strategy
3. **Prompt Generation**: Creates new prompt that addresses issues
4. **Constraint Preservation**: Ensures logo constraints remain enforced
5. **Reasoning**: Explains what changes were made and why

**Auto-Refine Mode:**

When `--auto-refine` is enabled, the `AutoRefineEvaluator` automatically:
1. Analyzes the generated image
2. Scores it against 5 criteria
3. Identifies specific issues
4. Generates actionable feedback
5. No manual input required

### 3. Gemini Client Integration (`gemini_client.py`)

Handles image generation with Google's Gemini models.

**Key Features:**

- Streaming generation for responsiveness
- Logo conversion and embedding
- Error handling and retries
- Metadata capture
- MLflow artifact logging

**Generation Flow:**

```python
def generate_image(self, prompt: str, logos: List[LogoInfo]) -> Tuple[bytes, str, dict]:
    """
    1. Convert logos to base64
    2. Construct multimodal prompt (text + images)
    3. Stream generate with Gemini
    4. Capture metadata (model, settings, timing)
    5. Return image bytes, response text, metadata
    """
```

### 4. Data Models (`models.py`)

Pydantic models for type safety and validation.

**Key Models:**

```python
class ConversationTurn(BaseModel):
    """Single iteration in the conversation"""
    iteration: int
    prompt: str
    image_path: str
    score: Optional[int]
    feedback: Optional[str]
    refinement_reasoning: Optional[str]
    mlflow_run_id: str
    timestamp: datetime

class ConversationSession(BaseModel):
    """Complete conversation session"""
    session_id: str
    start_time: datetime
    end_time: Optional[datetime]
    turns: List[ConversationTurn]
    target_score: int
    max_iterations: int
    best_turn: Optional[ConversationTurn]
    
class AutoRefineResult(BaseModel):
    """Auto-evaluation results"""
    score: int
    issues: List[str]
    improvements: List[str]
    criteria_scores: Dict[str, int]
```

### 5. CLI Integration (`cli.py`)

Click-based command interface.

**Chat Command:**

```python
@cli.command()
@click.option('--prompt-file', type=click.Path(exists=True))
@click.option('--diagram-spec', type=click.Path(exists=True))
@click.option('--template', default='baseline')
@click.option('--max-iterations', default=10)
@click.option('--target-score', default=5)
@click.option('--auto-refine', is_flag=True)
@click.option('--dspy-model', default='databricks-claude-opus-4-5')
def chat(ctx, **options):
    """
    Start interactive refinement conversation
    Handles:
    - Parameter validation
    - Session initialization
    - Output directory creation
    - Error handling
    - Session summary display
    """
```

## Data Flow

### Complete Refinement Loop

```
┌─────────────────────────────────────────────────┐
│  User starts chat with prompt file/spec         │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│  Initialize ConversationBot                     │
│  - Load prompt                                   │
│  - Load logos                                    │
│  - Create session ID                             │
│  - Initialize MLflow                             │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
        ╔═════════════════════╗
        ║  ITERATION LOOP     ║
        ╚═════════════════════╝
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│  1. Generate Diagram (Gemini)                   │
│     - Build multimodal prompt                   │
│     - Stream generate image                     │
│     - Save to outputs/                          │
│     - Log to MLflow                             │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│  2. Evaluate (Manual or Auto)                   │
│                                                  │
│  Manual Mode:                                   │
│  - User views image                             │
│  - User provides score (1-5)                    │
│  - User provides feedback                       │
│                                                  │
│  Auto-Refine Mode:                              │
│  - AI analyzes image                            │
│  - AI scores against criteria                   │
│  - AI generates feedback                        │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│  3. Check Completion                            │
│     - Score >= target_score?                    │
│     - User typed "done"?                        │
│     - Max iterations reached?                   │
└─────────────────┬───────────────────────────────┘
                  │
                  ├─ YES ──> Session Complete
                  │
                  NO
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│  4. Refine Prompt (DSPy)                        │
│     - Load conversation history                 │
│     - Analyze feedback and score                │
│     - Generate refined prompt                   │
│     - Explain reasoning                         │
│     - Update prompt for next iteration          │
└─────────────────┬───────────────────────────────┘
                  │
                  └────> Loop back to step 1
```

### MLflow Tracking

Each iteration creates an MLflow run with:

**Parameters:**
- `iteration`: Iteration number
- `prompt`: Full prompt text
- `temperature`: Generation temperature
- `model`: Gemini model used
- `session_id`: Conversation session ID

**Metrics:**
- `score`: User or auto-assigned score (1-5)
- `logo_count`: Number of logos used
- `prompt_length`: Character count

**Artifacts:**
- `image.png`: Generated diagram
- `prompt.txt`: Full prompt used
- `feedback.txt`: User/auto feedback
- `refinement.txt`: DSPy reasoning

**Tags:**
- `chat_session`: Session ID
- `iteration`: Iteration number
- `auto_refine`: True/False

## File Output Structure

```
outputs/
└── YYYY-MM-DD/
    └── chat-{session_id}/
        ├── iteration_1.png
        ├── iteration_2.png
        ├── iteration_3.png
        ├── ...
        └── session.json        # Complete session history
```

**session.json structure:**
```json
{
  "session_id": "abc123",
  "start_time": "2026-02-02T10:30:00",
  "end_time": "2026-02-02T10:45:00",
  "target_score": 5,
  "max_iterations": 10,
  "turns": [
    {
      "iteration": 1,
      "prompt": "Full prompt text...",
      "image_path": "outputs/2026-02-02/chat-abc123/iteration_1.png",
      "score": 3,
      "feedback": "Logos too small, text overlapping",
      "refinement_reasoning": "Increasing logo size and spacing...",
      "mlflow_run_id": "run123",
      "timestamp": "2026-02-02T10:31:00"
    }
  ],
  "best_turn": { /* Turn with highest score */ }
}
```

## Configuration

Chat system respects configuration from `configs/default.yaml`:

```yaml
vertex:
  model_id: "gemini-2.0-flash-exp"
  temperature: 0.8
  top_p: 0.95
  top_k: 40

dspy:
  model: "databricks-claude-opus-4-5"
  max_refinement_iterations: 10
  target_score: 5

mlflow:
  experiment_name: "/Users/{user}/chat-refinement"
  tracking_uri: "databricks"
```

## Error Handling

The chat system handles various error conditions:

### API Errors

- **Expired API Key**: Clear message with renewal instructions
- **Rate Limiting**: Automatic retry with exponential backoff
- **Model Overload**: Wait and retry suggestion

### User Errors

- **Invalid Score**: Prompt for 1-5 range
- **Empty Feedback**: Allow but warn if score < 5
- **Invalid File Paths**: Validate before starting

### System Errors

- **MLflow Connection**: Fail fast with auth instructions
- **File Write Errors**: Check permissions, disk space
- **DSPy Errors**: Fall back to manual refinement mode

## Performance Considerations

### Memory Management

- Images are streamed, not held in memory
- Conversation history kept in memory (small overhead)
- Session JSON written incrementally

### Generation Speed

- Typical iteration: 30-60 seconds
  - 20-40s for image generation (Gemini)
  - 5-10s for refinement (DSPy)
  - 5-10s for MLflow logging

### Optimization Tips

1. **Lower Temperature**: Faster, more deterministic (0.4-0.6)
2. **Smaller Images**: Reduce resolution if not needed
3. **Simpler Prompts**: Less text = faster generation
4. **Batch Logos**: Pre-convert logos once

## Extension Points

### Custom Evaluators

Implement custom evaluation logic:

```python
class CustomEvaluator:
    def evaluate(self, image_path: str, prompt: str) -> Tuple[int, str]:
        """Return score and feedback"""
        # Your evaluation logic
        return score, feedback
```

### Custom Refiners

Override DSPy refiner with custom logic:

```python
class CustomRefiner:
    def refine(self, history, feedback, score) -> Tuple[str, str]:
        """Return refined prompt and reasoning"""
        # Your refinement logic
        return new_prompt, reasoning
```

### Custom Generators

Swap Gemini for alternative model:

```python
class CustomGenerator:
    def generate(self, prompt: str, logos: List) -> bytes:
        """Return image bytes"""
        # Your generation logic
        return image_bytes
```

## Troubleshooting

### Chat Won't Start

1. Check authentication: `nano-banana check-auth`
2. Verify API keys in `.env`
3. Test MLflow connection
4. Check file permissions

### Poor Refinements

1. Provide more specific feedback
2. Try different DSPy model
3. Check conversation history is preserved
4. Review refinement reasoning

### Iterations Not Improving

1. Score may be stuck at local maximum
2. Consider restarting with different base prompt
3. Review DSPy model temperature
4. Check if feedback is too vague

## Best Practices

### For Users

1. **Start with solid base prompt**: Include all requirements upfront
2. **Give specific feedback**: "Logos 2x larger" vs "looks bad"
3. **Score consistently**: Use same rubric each iteration
4. **Review refinement reasoning**: Understand what's changing
5. **Know when to stop**: If stuck, restart with better base

### For Developers

1. **Log everything**: Use MLflow extensively
2. **Validate inputs**: Check paths, scores, options
3. **Handle errors gracefully**: Clear messages, recovery paths
4. **Test iteratively**: Start with simple prompts
5. **Monitor performance**: Track generation and refinement times

## Future Enhancements

Potential improvements to the chat system:

1. **Multi-image comparison**: Compare iterations side-by-side
2. **Undo/redo**: Return to previous iterations
3. **Branch conversations**: Explore multiple refinement paths
4. **Batch refinement**: Refine multiple aspects in parallel
5. **Learning from history**: Train on successful sessions
6. **Custom evaluation criteria**: User-defined scoring rubrics
7. **Real-time preview**: Show generation progress
8. **Collaborative sessions**: Multiple users refining together

## References

- **DSPy Documentation**: https://dspy-docs.vercel.app/
- **Gemini API**: https://ai.google.dev/
- **MLflow Tracking**: https://mlflow.org/docs/latest/tracking.html
- **Pydantic Models**: https://docs.pydantic.dev/

## See Also

- [Chat User Guide](nano_banana/CHAT_REFINEMENT.md) - User-facing documentation
- [Best Practices](BEST_PRACTICES.md) - General best practices
- [Workflows](WORKFLOWS.md) - Common workflow patterns
- [Troubleshooting](TROUBLESHOOTING.md) - Problem resolution
