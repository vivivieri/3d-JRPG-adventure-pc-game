#!/usr/bin/env python3
"""Verify required audio tracks exist for a build phase (docs/audio/AUDIO_QA.md §A1)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = ROOT / "game/data/audio/ace_step_prompts.json"

PHASE_REQUIRED: dict[str, list[str]] = {
    "1": ["bgm_village"],
    "m5": [],  # filled from ace_step_prompts tracks
}


def load_track_paths() -> dict[str, Path]:
    data = json.loads(PROMPTS.read_text(encoding="utf-8"))
    out: dict[str, Path] = {}
    for track_id, meta in data.get("tracks", {}).items():
        rel = meta.get("output", "")
        if rel:
            out[track_id] = ROOT / rel
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Audio catalog check (AUDIO_QA.md)")
    ap.add_argument("--phase", default="1", help="Build phase: 1 or m5")
    args = ap.parse_args()

    phase = args.phase.lower()
    track_paths = load_track_paths()

    if phase == "m5":
        required = sorted(track_paths.keys())
    elif phase in PHASE_REQUIRED:
        required = PHASE_REQUIRED[phase]
    else:
        print(f"Unknown phase '{phase}'. Use: 1, m5", file=sys.stderr)
        return 2

    print(f"Audio catalog check — phase {phase}")
    missing: list[str] = []
    for track_id in required:
        path = track_paths.get(track_id, ROOT / "game/assets/audio/missing.ogg")
        if path.is_file():
            print(f"  [OK]   {track_id} → {path.relative_to(ROOT)}")
        else:
            print(f"  [FAIL] {track_id} missing ({path.relative_to(ROOT)})", file=sys.stderr)
            missing.append(track_id)

    if missing:
        print(f"\nCatalog FAIL — {len(missing)} missing track(s)")
        return 1
    print(f"\nCatalog PASS — {len(required)} track(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
