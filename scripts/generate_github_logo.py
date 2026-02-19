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


PROMPT = """Create a funny, meme-ish logo image for "Bricksmith" for a Databricks field engineering org repo.

Vibe:
- Smart chaos, "ship it by Friday", caffeinated architecture wizard energy.
- Playful and slightly absurd, but still sharp enough to use as a GitHub repo logo.

Visual concept ideas:
- A smiling brick with engineer goggles and a tiny blueprint.
- A dramatic "architect brick" wearing a hard hat while dropping perfect data-flow arrows.
- Subtle AI cue (spark/glow/circuit accent), but do not make it overly futuristic.

Constraints:
- Square composition, optimized for small size (GitHub avatar).
- Strong silhouette, high contrast, minimal clutter.
- Flat or subtle depth style; no photorealism.
- No tiny unreadable text. If text appears, only "Bricksmith" and keep it optional.
- Light or transparent-friendly background."""

SYSTEM_INSTRUCTION = """You are generating one logo/icon image for a software repository. Make it humorous and meme-friendly while still polished and legible as a GitHub avatar. Output only the image."""


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
