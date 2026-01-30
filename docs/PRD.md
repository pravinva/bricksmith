# PRD: MLflow-Tracked Prompt Engineering for Architecture Diagrams with Vertex AI “Nano Banana Pro”

**Document Owner:** You  
**Target Users:** ML/Platform Engineers, Prompt Engineers  
**Last Updated:** 2026-01-17  
**Status:** Draft v1

---

## 1) Purpose

Build a reproducible, MLflow-tracked experimentation system that prompt-engineers architecture diagram generation using **Vertex AI Nano Banana Pro**, with strict control over **logo reuse** and **diagram fidelity**. The system should allow rapid iteration on prompts, parameters, and logo handling, while logging artifacts and metrics for comparison.

---

## 2) Goals & Non-Goals

### Goals
- Track prompt variants, parameters, and outputs via **MLflow 3.8.1**.
- Generate architecture diagrams using **Vertex AI Nano Banana Pro** (image generation).
- Enforce consistent logo usage:
  - *Reuse uploaded logos EXACTLY.*
  - *Scale uniformly.*
  - *No filenames in output.*
- Support **OAuth-only** auth for Google Cloud.
- Provide repeatable evaluation for diagram quality and brand compliance.

### Non-Goals
- Not building a full UI (CLI-first).
- Not training models; only prompt engineering.
- Not introducing external logo URLs (only user-provided uploads).

---

## 3) Key Requirements

### Functional
1. **Prompt Experimentation**
   - Support multiple prompt templates and variants.
   - Variables for layout, diagram style, labeling policy, icon treatment.

2. **Logo Kit Handling**
   - Accept a logo kit as files:
     - `databricks-logo.jpg` (Red Icon)
     - `delta-lake-logo.jpg` (Teal Icon)
     - `uc-logo.jpg` (Pink Squares, Yellow Triangles, Hexagon in Middle = Unity Catalog)
     - `kaluza_logo_black.jpg` (three hexagons stacked)
     - `AGL_Energy_logo.svg.jpg`
     - `AWS logo` (Drawn: Grey text + Orange smile)
     - `Azure logo` (Drawn: Blue symbol)
   - Inject into model inputs as **image parts**, and include explicit prompt instruction:
     - “Reuse uploaded logos EXACTLY. Scale uniformly. No filenames.”

3. **MLflow Tracking**
   - Log:
     - prompt text
     - model name
     - generation config (temperature, top_p, size, etc.)
     - logo kit identifiers (hashes)
     - input diagram spec
     - output images
     - evaluation metrics & rubric scores
   - Use MLflow Experiments & Runs for comparability.

4. **OAuth-only Auth**
   - **No API keys**. Use Google Cloud OAuth tokens.
   - Must run in environments that support ADC or OAuth flow (e.g., gcloud auth application-default login).

5. **Latest Libraries**
   - MLflow 3.8.1+
   - google-genai (latest compatible with Vertex AI)
   - Python 3.11+ recommended

### Non-Functional
- **Reproducibility:** Runs must be deterministic where possible (fixed seeds if supported).
- **Compliance:** No logo filenames appear in outputs.
- **Performance:** Target <60s per generation.

---

## 4) User Stories

1. **Prompt Engineer**  
   “As a prompt engineer, I want to test multiple prompt variants and compare diagram consistency across runs in MLflow.”

2. **Brand Owner**  
   “As a brand owner, I want the system to reuse logos exactly with uniform scale, with no filenames displayed.”

3. **ML Engineer**  
   “As an ML engineer, I want runs logged with parameters, metrics, and artifacts so I can audit results.”

---

## 5) System Overview

**Inputs**
- Diagram spec (text)
- Logo kit (images)
- Prompt template + parameters

**Processing**
- Build prompt with explicit logo instructions
- Pass logo images as input parts to Vertex AI model
- Generate diagram image
- Evaluate against rubric

**Outputs**
- Diagram image artifact
- MLflow run with metadata + metrics

---

## 6) Prompt Engineering Strategy

### Baseline Prompt Template (example)
```
You are generating a clean architecture diagram.
Reuse uploaded logos EXACTLY. Scale uniformly. No filenames.
Use a simple grid layout with clear left-to-right data flow.
Keep labels concise, use sentence case, and avoid clutter.
Output a single diagram image with white background.

Components:
- [list components + labels]
Connections:
- [list edges]
Constraints:
- [diagram constraints]
```

### Logo Injection
Pass each logo as an image part and label it *in the prompt text*, without using filenames in the output. Example snippet:

```
Logo kit provided as image references:
- Databricks logo (red icon)
- Delta Lake logo (teal icon)
- Unity Catalog logo (pink squares + yellow triangles + hexagon)
- Kaluza logo (three stacked hexagons)
- AGL Energy logo
- AWS logo (grey text + orange smile)
- Azure logo (blue symbol)
Reuse these exactly. Scale uniformly. No filenames or file labels.
```

---

## 7) MLflow Experiment Design

### Experiment Name
`vertexai-nanobanana-arch-diagrams`

### Run Parameters
- `model`: `vertex-nano-banana-pro` (exact model string)
- `temperature`, `top_p`, `max_output_tokens`, `image_size`, `aspect_ratio`
- `prompt_template_id`
- `prompt_text`
- `logo_hashes` (sha256 per logo)
- `diagram_spec_id`

### Metrics (examples)
- `logo_fidelity_score` (0–5)
- `layout_clarity_score` (0–5)
- `text_legibility_score` (0–5)
- `constraint_compliance_score` (0–5)
- `overall_score` (avg)

### Artifacts
- `output.png`
- `prompt.txt`
- `config.json`
- `eval.json`
- `diagram_spec.json`

---

## 8) Auth & Security

- Use **OAuth only**:
  - Preferred: **Application Default Credentials** (`gcloud auth application-default login`)
  - Service account impersonation is allowed if it uses OAuth token flow.
- No API keys stored or used.
- Ensure MLflow tracking URI uses secure backend (optional).

---

## 9) Architecture (Logical)

1. **CLI Runner**
   - Loads diagram spec + logo kit
   - Builds prompt
   - Calls Vertex AI Nano Banana Pro
   - Logs run to MLflow
2. **Evaluator**
   - Manual or automated rubric scoring
   - Logs metrics

---

## 10) Acceptance Criteria

- [ ] System authenticates using OAuth only.
- [ ] Each run appears in MLflow with parameters, metrics, and artifacts.
- [ ] Logos are reused exactly and uniformly scaled.
- [ ] Output contains no filenames or file labels.
- [ ] Prompt variants can be compared side-by-side in MLflow UI.

---

## 11) Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Model alters logos | Brand violation | Stronger prompt constraints + multi-pass verification |
| Filenames leaked in output | Brand issue | Explicit “no filenames” instruction + validator |
| Auth misconfig | Runtime failure | Pre-flight OAuth check |

---

## 12) Out of Scope (v1)

- Multi-user UI
- Automated A/B testing dashboard
- Model fine-tuning

---

## 13) Open Questions

1. What is the exact Vertex AI model identifier for “Nano Banana Pro” in your environment?
2. Do you want a **CLI-only** workflow, or also notebooks?
3. How will you define the diagram spec format (YAML/JSON/free text)?
4. Should evaluation be manual, automated, or hybrid?

---

## 14) Suggested Next Steps

1. Confirm model identifier for Nano Banana Pro.
2. Define diagram spec schema (YAML/JSON).
3. Provide sample logo kit files to integrate into the prompt pipeline.
4. Decide on evaluation rubric and whether you want automated scoring.

---

If you want, I can turn this PRD into a **detailed technical design + starter code outline** using MLflow 3.8.1 and OAuth-based Vertex AI calls.