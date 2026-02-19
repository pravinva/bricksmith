#!/usr/bin/env -S uv run python
"""Generate a GitHub repo logo for Bricksmith using the Gemini 3 Pro image API.

Usage (from repo root, with GEMINI_API_KEY set):
    uv run python scripts/generate_github_logo.py

Output: logo.png in repo root (and optionally docs/bricksmith/).
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Load .env from repo root so GEMINI_API_KEY is available
try:
    from dotenv import load_dotenv
    load_dotenv(REPO_ROOT / ".env")
except ImportError:
    pass

from bricksmith.gemini_client import GeminiClient


PROMPT = """Create a single, clean logo image for "Bricksmith" – a tool that turns text prompts into architecture diagrams using AI (Gemini). The logo should:
- Be simple and recognizable at small sizes (e.g. GitHub avatar).
- Suggest building/crafting (e.g. bricks, blueprint, or diagram elements) and AI/automation.
- Use a professional, modern style: flat or subtle depth, clear shapes, no photorealism.
- Work on light backgrounds (white or light grey).
- Square composition, no text unless it is the word "Bricksmith" integrated as a wordmark.
- Avoid clutter; one strong concept is enough."""

SYSTEM_INSTRUCTION = """You are generating a single logo or icon image. Output only the image. Keep it simple, iconic, and suitable for a software project avatar."""


def main() -> None:
    out_path = REPO_ROOT / "logo.png"

    client = GeminiClient()
    print("Calling Gemini 3 Pro image API...")
    image_bytes, response_text, metadata = client.generate_image(
        prompt=PROMPT,
        logo_parts=[],
        temperature=0.7,
        aspect_ratio="1:1",
        image_size="2K",
        system_instruction=SYSTEM_INSTRUCTION,
    )
    out_path.write_bytes(image_bytes)
    print(f"Saved: {out_path}")

    docs_logo_dir = REPO_ROOT / "docs" / "bricksmith"
    if docs_logo_dir.is_dir():
        docs_logo_dir.joinpath("logo.png").write_bytes(image_bytes)
        print(f"Saved: {docs_logo_dir / 'logo.png'}")


if __name__ == "__main__":
    main()
