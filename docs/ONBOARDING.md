# Bricksmith onboarding

This guide gets you from zero to your first architecture diagram in about 15 minutes.

## What is Bricksmith?

Bricksmith turns **text descriptions** into **architecture diagrams** using AI (Gemini). You describe the system in words; the tool generates an image, scores it with an LLM judge, and can refine the prompt automatically. Every run is logged to MLflow so you have a full history.

**You will:**

1. Install the tool and set up credentials
2. Generate your first diagram from a prompt file
3. (Optional) Try the **architect** or **chat** workflows for iterative design

---

## Step 1: Prerequisites

- **Python 3.11+**
- **uv** (Python package manager) — [install](https://github.com/astral-sh/uv)
- **Google AI API key** — [create one](https://aistudio.google.com/app/apikey)
- **Databricks workspace** — for MLflow experiment tracking (optional for a quick local test, but required for full features)

---

## Step 2: Install

```bash
# Clone the repo (or you're already in it)
cd bricksmith

# Create virtual environment and activate
uv venv && source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# Install the package
uv pip install -e .
```

Verify the CLI:

```bash
bricksmith --help
```

You should see commands like `generate-raw`, `chat`, `architect`, `list-runs`, and `check-auth`.

---

## Step 3: Configure credentials

Bricksmith needs at least a **Google AI (Gemini) API key** to generate images. For MLflow tracking and AI-powered refinement you also need **Databricks** credentials.

1. **Copy the environment template:**

   ```bash
   cp .env.example .env
   ```

2. **Edit `.env`** and set:

   | Variable           | Required | Where to get it |
   |--------------------|----------|------------------|
   | `GEMINI_API_KEY`   | Yes      | [Google AI Studio](https://aistudio.google.com/app/apikey) → Create API key (starts with `AIza...`) |
   | `DATABRICKS_HOST`  | For MLflow / refinement | Your workspace URL, e.g. `https://your-workspace.cloud.databricks.com` |
   | `DATABRICKS_TOKEN` | For MLflow / refinement | Workspace → Profile → Settings → Developer → Access tokens (starts with `dapi...`) |
   | `DATABRICKS_USER`  | For MLflow / refinement | Your Databricks login email |

3. **Load the environment:**

   ```bash
   source .env
   ```

4. **Verify auth:**

   ```bash
   bricksmith check-auth
   ```

   You should see ✓ for Google AI and (if configured) ✓ for Databricks.

---

## Step 4: Prepare logos (optional but recommended)

Diagrams can include vendor/product logos (e.g. Databricks, Delta Lake, Unity Catalog). Bricksmith uses a **logo kit**: a folder of images plus descriptions so the AI never sees filenames.

- Default kit: `logos/default/`
- Validate: `bricksmith validate-logos --logo-dir logos/default`

If you skip logos, you can still generate diagrams; the tool will just not inject logo constraints. For a first run, using the default kit is enough.

---

## Step 5: Your first diagram

Create a short prompt file, or use an existing one.

**Option A – Use the minimal example:**

```bash
bricksmith generate-raw \
  --prompt-file prompts/branding/minimal.txt \
  --logo-dir logos/default \
  --run-name "my-first-diagram"
```

**Option B – Use your own prompt:**

1. Create a `.txt` file, e.g. `prompts/my_first.txt`:

   ```
   Draw a simple architecture diagram: a data lake on the left, a processing engine in the middle, and a dashboard on the right. Use clean lines and a professional style. Use the provided logos exactly as given.
   ```

2. Run:

   ```bash
   bricksmith generate-raw \
     --prompt-file prompts/my_first.txt \
     --logo-dir logos/default \
     --run-name "my-first-diagram"
   ```

Output is written to **`outputs/YYYY-MM-DD/<run-folder>/`** (e.g. `outputs/2026-02-19/...`). Open the generated PNG to view your diagram. If you configured Databricks, the run is also in MLflow.

---

## Step 6: What to do next

| Goal | What to do |
|------|------------|
| **Improve this diagram** | Use **chat**: `bricksmith chat --prompt-file prompts/my_first.txt` — generate, give feedback, let the AI refine the prompt. |
| **Design from a problem** | Use **architect**: `bricksmith architect --problem "Real-time analytics pipeline for IoT"` — discuss design in natural language, then type `output` to get a diagram prompt. |
| **See past runs** | `bricksmith list-runs` (and `bricksmith show-run <run-id>`). |
| **Score a diagram** | `bricksmith evaluate <run-id>`. |
| **Use the web UI** | `uv pip install -e ".[web]"` then `bricksmith web --dev`. |

---

## Quick reference

| Command | Purpose |
|--------|--------|
| `bricksmith generate-raw --prompt-file <file> --logo-dir <dir>` | One-shot diagram from a prompt file |
| `bricksmith chat --prompt-file <file>` | Interactive generate → feedback → AI refinement |
| `bricksmith architect --problem "<description>"` | Conversational design; type `output` to get prompt |
| `bricksmith list-runs` | List MLflow runs |
| `bricksmith show-run <run-id>` | Show run details |
| `bricksmith check-auth` | Verify Google AI and Databricks credentials |
| `bricksmith validate-logos --logo-dir <dir>` | Validate logo kit |

---

## Where to read more

- **[Setup guide](SETUP.md)** — Full installation, auth, logo setup, and config.
- **[Workflows](WORKFLOWS.md)** — Detailed guides for generate-raw, architect, and chat.
- **[Troubleshooting](TROUBLESHOOTING.md)** — Common issues and fixes.
- **[Web interface](WEB_INTERFACE.md)** — Deploy and use the web UI.
- **[Logo hints](bricksmith/LOGO_HINTS.md)** — Improve how specific logos are described to the AI.

If something doesn’t work, run `bricksmith check-auth` and check [TROUBLESHOOTING.md](TROUBLESHOOTING.md).
