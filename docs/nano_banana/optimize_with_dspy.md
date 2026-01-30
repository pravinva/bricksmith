# DSPy-Based Prompt Optimization for Image Generation

## 🎯 Overview

Traditional DSPy optimizers (like in your `agl_rfp_dspy_refinement.py`) work great for **text→text** tasks. For **text→image** (Nano Banana), we need a **hybrid approach**.

## ✅ What Works: The Hybrid Model

```
┌─────────────────────────────────────────────┐
│  DSPy Prompt Refiner                        │
│  (Uses LLM to improve prompt text)          │
└─────────────┬───────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────┐
│  Nano Banana Image Generation               │
│  (gemini-3-pro-image-preview)               │
└─────────────┬───────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────┐
│  Human Evaluation + Scoring                 │
│  (1-5 scores on quality metrics)            │
└─────────────┬───────────────────────────────┘
              │
              ▼ (feedback loop)
┌─────────────────────────────────────────────┐
│  DSPy Learns What Prompts → Good Images     │
└─────────────────────────────────────────────┘
```

## 🔧 How It Works

### Step 1: Initial Prompt
Start with your base template (e.g., `agl_concentric_presentation.txt`)

### Step 2: DSPy Refinement
DSPy uses an LLM (Claude, Llama, etc.) to:
- Analyze the prompt
- Incorporate technical context (from MCP)
- Apply feedback from previous iterations
- Generate a refined version

### Step 3: Generate Image
Use the refined prompt with Nano Banana

### Step 4: Human Evaluation
You score the image on:
- Logo visibility (1-5)
- Technical accuracy (1-5)
- Visual quality (1-5)
- Layout clarity (1-5)
- Presentation readiness (1-5)

### Step 5: Iterate
DSPy learns from your scores and refines again

## 📊 Comparison: Traditional DSPy vs. Our Approach

| Aspect | Traditional DSPy | Nano Banana DSPy |
|--------|------------------|------------------|
| **Task** | Text → Text | Text → Image |
| **Evaluation** | Automatic (accuracy, F1) | Human scoring |
| **Speed** | Fast (100s of variants) | Slow (30-60s each) |
| **Cost** | Low | High (API calls) |
| **Iterations** | 100-1000 | 3-5 |
| **Metrics** | Exact match, F1, accuracy | Visual quality, accuracy |

## 🚀 Practical Workflow

### Option 1: Manual DSPy Refinement

```python
from src.nano_banana.dspy_optimizer import DSPyPromptOptimizer

# Initialize
optimizer = DSPyPromptOptimizer(
    lm_model="databricks-meta-llama-3-1-70b-instruct"
)

# Optimize
best_prompt, history = optimizer.optimize_prompt(
    initial_prompt=your_template,
    diagram_spec=agl_spec,
    technical_context=databricks_docs_context,
    max_iterations=3,
    target_score=4.5
)
```

### Option 2: Simplified Feedback Loop

1. **Generate** with current prompt
2. **Score** the image (1-5 on each metric)
3. **Ask DSPy** to refine based on feedback
4. **Repeat** 2-3 times

### Option 3: Batch Comparison

Use your existing `develop_prompts.py` but add DSPy:
```bash
# Generate 4 variants
uv run python develop_prompts.py

# Pick best based on scores
# Ask DSPy to analyze why it worked
# Generate refined version
```

## 💡 Key Insights

### ✅ DSPy IS Useful For:
1. **Prompt Text Optimization** - Making prompts clearer, more specific
2. **Context Integration** - Weaving in technical docs automatically
3. **Feedback Learning** - Understanding what makes good prompts
4. **Systematic Iteration** - Structured improvement process

### ❌ DSPy Can't Do:
1. **Automatic Image Eval** - Requires human judgment
2. **Rapid Iteration** - Each image = 30-60s
3. **Out-of-box Optimization** - Needs custom workflow

## 🎯 Recommended Approach

**Phase 1: Manual Exploration (Current System)**
- Use `develop_prompts.py` to compare variants
- Manually score each diagram
- Identify what works

**Phase 2: DSPy Refinement (New)**
- Take best template from Phase 1
- Use DSPy to refine based on your feedback
- Generate 2-3 refined variants
- Pick winner

**Phase 3: Production (Final)**
- Lock in best prompt as template
- Use for production diagrams
- Occasionally run Phase 1-2 to improve

## 📝 Example: DSPy-Optimized Workflow

```python
# 1. Start with baseline
baseline_prompt = load_template("agl_concentric_presentation")

# 2. Add MCP enrichment
enriched_context = get_databricks_docs_context(diagram_spec)

# 3. First iteration - generate
generate_image(baseline_prompt + enriched_context)
# Score: 3.2/5.0
# Feedback: "Kaluza logo too small, colors too muted"

# 4. DSPy refines
refined_v1 = dspy_refiner.refine(
    prompt=baseline_prompt,
    context=enriched_context,
    feedback="Make Kaluza logo 50% larger, use more vibrant colors"
)

# 5. Second iteration
generate_image(refined_v1)
# Score: 4.1/5.0
# Feedback: "Much better! AWS logo could be more prominent"

# 6. DSPy refines again
refined_v2 = dspy_refiner.refine(
    prompt=refined_v1,
    context=enriched_context,
    feedback="Increase AWS logo size by 30%"
)

# 7. Final iteration
generate_image(refined_v2)
# Score: 4.7/5.0
# Feedback: "Perfect! Production ready"

# 8. Save as new template
save_template("agl_concentric_optimized", refined_v2)
```

## 🔬 Advanced: Semi-Automated Evaluation

You could add automated checks:

```python
def semi_automated_eval(image_path):
    scores = {}

    # Automated checks
    scores["has_all_logos"] = detect_logos(image_path)  # True/False
    scores["no_spelling_errors"] = check_text_ocr(image_path)  # True/False
    scores["correct_aspect_ratio"] = check_dimensions(image_path)  # True/False

    # Human checks
    scores["visual_quality"] = human_score(1-5)
    scores["technical_accuracy"] = human_score(1-5)

    return scores
```

## 🎓 Best Practices

1. **Start with 3-5 iterations** - Don't over-optimize
2. **Be specific in feedback** - "Logo too small" > "Improve logos"
3. **Track in MLflow** - Compare scores over time
4. **Use MCP enrichment** - Always add technical context
5. **Human evaluation is key** - Automate what you can, but images need eyes

## 🆚 When to Use What

**Use Traditional DSPy (like your RFP script)** when:
- Optimizing TEXT outputs
- Can evaluate automatically
- Need 100s of variants
- Cost is low

**Use DSPy-Hybrid (this system)** when:
- Optimizing IMAGE generation prompts
- Need human evaluation
- Limited to 3-5 iterations
- Each generation costs money/time

**Use Manual Iteration (develop_prompts.py)** when:
- Just exploring
- Trying different styles
- Not sure what you want yet
- Learning the model's capabilities

## 📚 Resources

- Your RFP DSPy script: `agl_rfp_dspy_refinement.py`
- Image prompt optimizer: `src/nano_banana/dspy_optimizer.py`
- Comparison tool: `develop_prompts.py`
- MLflow tracking: `mlflow ui --port 5000`
