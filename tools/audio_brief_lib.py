#!/usr/bin/env python3
"""Load audio generation brief emotional intent (docs/generation_briefs/audio|vo/)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIO_BRIEF_DIR = ROOT / "docs" / "generation_briefs" / "audio"
VO_BRIEF_DIR = ROOT / "docs" / "generation_briefs" / "vo"


def _extract_section(markdown: str, heading: str) -> str:
    pattern = rf"^##\s+{re.escape(heading)}\b.*?(?=^##\s+|\Z)"
    match = re.search(pattern, markdown, flags=re.MULTILINE | re.DOTALL | re.IGNORECASE)
    if not match:
        return ""
    return match.group(0).strip()


def _brief_path(asset_id: str, *, kind: str) -> Path:
    if kind == "vo":
        return VO_BRIEF_DIR / f"{asset_id}.md"
    return AUDIO_BRIEF_DIR / f"{asset_id}.md"


def load_brief_markdown(asset_id: str, *, kind: str = "audio") -> str:
    path = _brief_path(asset_id, kind=kind)
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")


def load_emotional_intent(asset_id: str, *, kind: str = "audio") -> str:
    body = load_brief_markdown(asset_id, kind=kind)
    if not body:
        return ""
    return _extract_section(body, "Emotional intent")


def format_emotional_context(asset_id: str, *, kind: str = "audio") -> str:
    intent = load_emotional_intent(asset_id, kind=kind)
    if intent:
        return intent
    body = load_brief_markdown(asset_id, kind=kind)
    section = _extract_section(body, "Intent")
    if section:
        lines = [ln.strip() for ln in section.splitlines() if ln.strip() and not ln.startswith("#")]
        for ln in lines:
            if not ln.startswith("|") and not ln.startswith("---"):
                return f"Intent (from generation brief): {ln}"
    return ""
