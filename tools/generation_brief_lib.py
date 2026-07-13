#!/usr/bin/env python3
"""Load generation brief sections for jury prompts (docs/generation_briefs/)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRIEF_DIR = ROOT / "docs" / "generation_briefs"

# Visual jury --zone values → brief filename stem
ZONE_BRIEF_IDS: dict[str, str] = {
    "ruined_village": "ruined_village",
    "beach": "beach_shore",
    "beach_shore": "beach_shore",
    "tidal_caves": "tidal_caves",
    "palace_gate": "dragon_palace_gate",
    "dragon_palace_gate": "dragon_palace_gate",
}


def brief_path(asset_id: str) -> Path:
    return BRIEF_DIR / f"{asset_id}.md"


def extract_section(markdown: str, heading: str) -> str:
    """Return body of first ## <heading> section (case-insensitive), until next ##."""
    pattern = rf"^##\s+{re.escape(heading)}\b.*?(?=^##\s+|\Z)"
    match = re.search(pattern, markdown, flags=re.MULTILINE | re.DOTALL | re.IGNORECASE)
    if not match:
        return ""
    return match.group(0).strip()


def load_brief_markdown(asset_id: str) -> str:
    path = brief_path(asset_id)
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")


def load_emotional_intent(asset_id: str) -> str:
    """Emotional intent block from docs/generation_briefs/<id>.md."""
    body = load_brief_markdown(asset_id)
    if not body:
        return ""
    return extract_section(body, "Emotional intent")


def load_intent_sentence(asset_id: str) -> str:
    body = load_brief_markdown(asset_id)
    if not body:
        return ""
    section = extract_section(body, "Intent")
    if not section:
        return ""
    lines = [ln.strip() for ln in section.splitlines() if ln.strip() and not ln.strip().startswith("#")]
    for ln in lines:
        if ln.startswith("|") or ln.startswith("---"):
            continue
        return ln
    return ""


def brief_id_for_zone(zone: str) -> str:
    return ZONE_BRIEF_IDS.get(zone, zone)


def format_emotional_context(asset_id: str) -> str:
    """Compact block for LLM jury prompts."""
    intent = load_emotional_intent(asset_id)
    if intent:
        return intent
    one_line = load_intent_sentence(asset_id)
    if one_line:
        return f"Intent (from generation brief): {one_line}"
    return ""
