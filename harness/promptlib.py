"""Load model-facing prompts from disk so tests never embed instructions."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = ROOT / "prompts"


def load(name: str) -> str:
    """Load prompts/<name>.md, stripping the leading heading line."""
    path = PROMPTS / f"{name}.md"
    if not path.is_file():
        raise FileNotFoundError(f"missing prompt: {path}")
    lines = path.read_text(encoding="utf-8").splitlines()
    if lines and lines[0].startswith("#"):
        lines = lines[1:]
        while lines and not lines[0].strip():
            lines = lines[1:]
    return "\n".join(lines).strip()
