#!/usr/bin/env python3
"""Validate game/data/audio/scene_audio_map.json vs audio_qa_catalog.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "game/data/audio/scene_audio_map.json"
CATALOG_PATH = ROOT / "game/data/audio/audio_qa_catalog.json"


def collect_track_refs(obj: dict) -> set[str]:
    refs: set[str] = set()
    for key in ("bgm", "default_bgm"):
        val = obj.get(key)
        if isinstance(val, str):
            refs.add(val)
    for key in ("boss_phase_tracks", "stings", "ambient", "voice_clips"):
        for item in obj.get(key, []) or []:
            if isinstance(item, str):
                refs.add(item)
    return refs


def main() -> int:
    errors: list[str] = []
    if not MAP_PATH.is_file():
        print(f"Missing {MAP_PATH}", file=sys.stderr)
        return 2
    if not CATALOG_PATH.is_file():
        print(f"Missing {CATALOG_PATH}", file=sys.stderr)
        return 2

    data = json.loads(MAP_PATH.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    track_ids = set(catalog.get("tracks", {}).keys())
    vo_ids = set(catalog.get("vo_clips", {}).keys())
    sting_prefixes = ("sting_", "cine_", "sfx_", "amb_")

    zones = data.get("zones", {})
    scenes = data.get("scenes", {})
    if not zones or not scenes:
        errors.append("zones and scenes must be non-empty")

    for zid, zone in zones.items():
        refs = collect_track_refs(zone)
        for ref in refs:
            if ref.startswith(sting_prefixes) or ref.startswith("sfx_"):
                continue
            if ref not in track_ids:
                errors.append(f"zones.{zid} unknown track ref: {ref}")

    for sid, scene in scenes.items():
        refs = collect_track_refs(scene)
        for ref in refs:
            if ref.startswith(("sfx_", "amb_")) and ref not in track_ids:
                continue  # SFX/amb not all in BGM catalog
            if ref.startswith(("sting_", "cine_")) and ref not in track_ids:
                errors.append(f"scenes.{sid} unknown sting/bgm ref: {ref}")
            elif ref in vo_ids:
                continue
            elif not ref.startswith(("sfx_", "amb_")) and ref not in track_ids:
                errors.append(f"scenes.{sid} unknown track ref: {ref}")
        for vc in scene.get("voice_clips", []) or []:
            if vc not in vo_ids:
                errors.append(f"scenes.{sid} unknown voice_clip: {vc}")

    if errors:
        print("SCENE AUDIO MAP VALIDATION FAILED", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"OK — {len(zones)} zones, {len(scenes)} scenes, version={data.get('version')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
