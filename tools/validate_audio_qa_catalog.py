#!/usr/bin/env python3
"""Validate game/data/audio/audio_qa_catalog.json (docs/audio/AUDIO_QA.md, AUDIO_PRODUCTION_GUIDE)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "game/data/audio/audio_qa_catalog.json"
ACE_PATH = ROOT / "game/data/audio/ace_step_prompts.json"
VO_PATH = ROOT / "game/data/audio/vo_prompts.json"


def main() -> int:
    errors: list[str] = []
    if not CATALOG_PATH.is_file():
        print(f"Missing {CATALOG_PATH}", file=sys.stderr)
        return 2

    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    ace = json.loads(ACE_PATH.read_text(encoding="utf-8")) if ACE_PATH.is_file() else {"tracks": {}}
    vo = json.loads(VO_PATH.read_text(encoding="utf-8")) if VO_PATH.is_file() else {"clips": {}}

    tracks = catalog.get("tracks", {})
    vo_clips = catalog.get("vo_clips", {})
    if not tracks:
        errors.append("tracks must be non-empty")

    hero = catalog.get("hero_jury_tracks", [])
    p0 = catalog.get("p0_vo_clips", [])
    for tid in hero:
        if tid not in tracks:
            errors.append(f"hero_jury_tracks unknown track: {tid}")
    for cid in p0:
        if cid not in vo_clips:
            errors.append(f"p0_vo_clips unknown clip: {cid}")

    for phase, ids in catalog.get("phase_required", {}).items():
        for tid in ids:
            if tid not in tracks:
                errors.append(f"phase_required.{phase} unknown track: {tid}")

    for tid, meta in tracks.items():
        prefix = f"tracks.{tid}"
        if not meta.get("path"):
            errors.append(f"{prefix} missing path")
        if meta.get("hero_jury") and not meta.get("generation_brief"):
            errors.append(f"{prefix} hero_jury requires generation_brief")
        brief = meta.get("generation_brief")
        if brief and not (ROOT / brief).is_file():
            errors.append(f"{prefix} generation_brief not found: {brief}")
        ace_meta = ace.get("tracks", {}).get(tid)
        if ace_meta and ace_meta.get("output") != meta.get("path"):
            errors.append(f"{prefix} path mismatch vs ace_step_prompts.json")
        if meta.get("loop") and meta.get("loudness_lufs_target") is None:
            errors.append(f"{prefix} loop track needs loudness_lufs_target")

    for cid, meta in vo_clips.items():
        prefix = f"vo_clips.{cid}"
        if meta.get("tier") == "p0" and not meta.get("generation_brief"):
            errors.append(f"{prefix} p0 clip requires generation_brief")
        if cid in p0 and not meta.get("hero_listen_review"):
            errors.append(f"{prefix} p0 clip requires hero_listen_review: true")
        if meta.get("hero_listen_review") and not meta.get("generation_brief"):
            errors.append(f"{prefix} hero_listen_review requires generation_brief")
        brief = meta.get("generation_brief")
        if brief and not (ROOT / brief).is_file():
            errors.append(f"{prefix} generation_brief not found: {brief}")
        if cid not in vo.get("clips", {}):
            errors.append(f"{prefix} not in vo_prompts.json clips")

    if len(tracks) != len(ace.get("tracks", {})):
        errors.append(
            f"track count {len(tracks)} != ace_step_prompts {len(ace.get('tracks', {}))}"
        )

    if errors:
        print("AUDIO QA CATALOG VALIDATION FAILED", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(
        f"OK — {len(tracks)} tracks, {len(vo_clips)} vo clips, "
        f"{len(hero)} hero jury, {len(p0)} p0 vo, version={catalog.get('version')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
