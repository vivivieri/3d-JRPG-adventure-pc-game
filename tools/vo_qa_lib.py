#!/usr/bin/env python3
"""Shared VO QA helpers — paths, dialogue lines, catalog (docs/audio/AUDIO_QA.md §A4)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "game/data/audio/audio_qa_catalog.json"
VO_PROMPTS_PATH = ROOT / "game/data/audio/vo_prompts.json"
DIALOGUE_PATH = ROOT / "game/data/dialogue/chapter_01.json"


def load_catalog() -> dict:
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def load_vo_prompts() -> dict:
    return json.loads(VO_PROMPTS_PATH.read_text(encoding="utf-8"))


def dialogue_lines_by_voice_id() -> dict[str, dict]:
    data = json.loads(DIALOGUE_PATH.read_text(encoding="utf-8"))
    out: dict[str, dict] = {}
    for scene in data.get("scenes", []):
        for line in scene.get("lines", []):
            vid = line.get("voice_id")
            if vid:
                out[str(vid)] = {
                    "scene_id": scene.get("scene_id"),
                    "speaker": line.get("speaker"),
                    "text": line.get("text", {}),
                    "tier": line.get("vo_tier", ""),
                }
    return out


def resolve_vo_path(clip_id: str, locale: str, dialect: str | None = None) -> Path:
    if locale == "zh-Hant":
        if not dialect:
            raise ValueError("zh-Hant VO path requires dialect cant|cmn")
        return ROOT / "game/assets/audio/voice" / locale / dialect / f"{clip_id}.ogg"
    return ROOT / "game/assets/audio/voice" / locale / f"{clip_id}.ogg"


def locale_jobs(clip_meta: dict) -> list[tuple[str, str | None]]:
    jobs: list[tuple[str, str | None]] = []
    for locale in clip_meta.get("locales", []):
        jobs.append((locale, None))
    for dialect in clip_meta.get("zh_hant_dialects", []):
        jobs.append(("zh-Hant", dialect))
    return jobs


def clip_meta(clip_id: str) -> dict:
    catalog = load_catalog()
    meta = catalog.get("vo_clips", {}).get(clip_id)
    if not meta:
        raise KeyError(f"Unknown VO clip in audio_qa_catalog: {clip_id}")
    return meta


def expected_line_text(clip_id: str, locale: str) -> str:
    lines = dialogue_lines_by_voice_id()
    line = lines.get(clip_id)
    if not line:
        return ""
    text_map = line.get("text", {})
    if locale == "zh-Hant":
        return str(text_map.get("zh-Hant", text_map.get("zh", ""))).strip()
    return str(text_map.get(locale, "")).strip()


def p0_listen_clips() -> list[str]:
    catalog = load_catalog()
    return list(catalog.get("p0_vo_clips", []))
