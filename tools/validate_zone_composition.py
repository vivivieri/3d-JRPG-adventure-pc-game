#!/usr/bin/env python3
"""Validate game/data/qa/zone_composition.json (docs/art/GENERATION_READINESS.md §5)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ZONE_PATH = ROOT / "game/data/qa/zone_composition.json"
BRIEF_DIR = ROOT / "docs/generation_briefs"

REQUIRED_ZONE_KEYS = (
    "phase",
    "scene_path",
    "emotional_mood",
    "min_path_width_m",
    "vista_anchor",
    "gameplay_cam_height_m",
    "golden_screenshot",
    "generation_brief",
)
MOOD_RE = re.compile(r"^[a-z][a-z0-9_]*$")


def main() -> int:
    if not ZONE_PATH.is_file():
        print(f"Missing {ZONE_PATH}", file=sys.stderr)
        return 2

    data = json.loads(ZONE_PATH.read_text(encoding="utf-8"))
    errors: list[str] = []

    if not data.get("version"):
        errors.append("missing version")
    zones = data.get("zones", {})
    if not zones:
        errors.append("zones must be non-empty")

    for zone_id, zone in zones.items():
        prefix = f"zones.{zone_id}"
        for key in REQUIRED_ZONE_KEYS:
            if key not in zone:
                errors.append(f"{prefix} missing required key: {key}")

        mood = zone.get("emotional_mood", "")
        if mood and not MOOD_RE.match(mood):
            errors.append(f"{prefix}.emotional_mood invalid: {mood!r}")

        path_w = zone.get("min_path_width_m")
        if path_w is not None and (not isinstance(path_w, (int, float)) or path_w <= 0):
            errors.append(f"{prefix}.min_path_width_m must be > 0")

        cam_h = zone.get("gameplay_cam_height_m")
        if cam_h is not None and (not isinstance(cam_h, (int, float)) or cam_h <= 0):
            errors.append(f"{prefix}.gameplay_cam_height_m must be > 0")

        scene_path = zone.get("scene_path", "")
        if scene_path and not scene_path.startswith("res://scenes/world/"):
            errors.append(f"{prefix}.scene_path must start with res://scenes/world/")

        brief = zone.get("generation_brief", "")
        if brief:
            brief_path = ROOT / brief
            if not brief_path.is_file():
                errors.append(f"{prefix}.generation_brief not found: {brief}")

        golden = zone.get("golden_screenshot", "")
        if golden and not golden.startswith("artifacts/"):
            errors.append(f"{prefix}.golden_screenshot must be under artifacts/")

        markers = zone.get("markers", [])
        if markers is not None and not isinstance(markers, list):
            errors.append(f"{prefix}.markers must be a list")

    # Cross-check: every zone row has a matching generation brief
    if BRIEF_DIR.is_dir():
        for zid in zones:
            brief_md = BRIEF_DIR / f"{zid}.md"
            if not brief_md.is_file():
                errors.append(f"expected generation brief for zone {zid}: {brief_md}")

    if errors:
        print("ZONE COMPOSITION VALIDATION FAILED", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"OK — {len(zones)} zones, version={data.get('version')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
