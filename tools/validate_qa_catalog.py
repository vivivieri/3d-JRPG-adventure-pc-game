#!/usr/bin/env python3
"""Validate game/data/models/qa_catalog.json schema and animation_timing (docs/MODEL_QA.md)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "game/data/models/qa_catalog.json"

TIMING_KEYS = ("loop", "duration_ms_min", "duration_ms_max", "root_motion")


def validate_timing_block(
    model_id: str,
    timing: dict,
    allowed: list[str] | None,
    required: list[str] | None,
    errors: list[str],
) -> None:
    if not isinstance(timing, dict):
        errors.append(f"models.{model_id}.animation_timing must be an object")
        return

    allowed_set = set(allowed or [])
    for anim_name, spec in timing.items():
        if allowed_set and anim_name not in allowed_set:
            errors.append(
                f"models.{model_id}.animation_timing[{anim_name!r}] "
                f"not in allowed_animations"
            )
        if not isinstance(spec, dict):
            errors.append(f"models.{model_id}.animation_timing[{anim_name!r}] must be object")
            continue
        for key in TIMING_KEYS:
            if key not in spec:
                errors.append(
                    f"models.{model_id}.animation_timing[{anim_name!r}] missing {key}"
                )
        lo = spec.get("duration_ms_min")
        hi = spec.get("duration_ms_max")
        if isinstance(lo, (int, float)) and isinstance(hi, (int, float)):
            if lo > hi:
                errors.append(
                    f"models.{model_id}.animation_timing[{anim_name!r}] "
                    f"duration_ms_min ({lo}) > duration_ms_max ({hi})"
                )
            if lo < 0 or hi < 0:
                errors.append(
                    f"models.{model_id}.animation_timing[{anim_name!r}] "
                    "durations must be non-negative"
                )
        loop = spec.get("loop")
        root_motion = spec.get("root_motion")
        if loop is not None and not isinstance(loop, bool):
            errors.append(f"models.{model_id}.animation_timing[{anim_name!r}].loop must be bool")
        if root_motion is not None and not isinstance(root_motion, bool):
            errors.append(
                f"models.{model_id}.animation_timing[{anim_name!r}].root_motion must be bool"
            )

    if required:
        missing = sorted(set(required) - set(timing.keys()))
        if missing:
            errors.append(
                f"models.{model_id} required_animations missing animation_timing: "
                + ", ".join(missing)
            )


def main() -> int:
    if not CATALOG_PATH.is_file():
        print(f"Missing {CATALOG_PATH}", file=sys.stderr)
        return 2

    data = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    errors: list[str] = []

    if not data.get("version"):
        errors.append("missing version")

    models = data.get("models", {})
    if not models:
        errors.append("models must be non-empty")

    phase_required = data.get("phase_required", {})
    for phase, ids in phase_required.items():
        if not isinstance(ids, list):
            errors.append(f"phase_required.{phase} must be a list")
            continue
        for model_id in ids:
            if model_id not in models:
                errors.append(f"phase_required.{phase} references unknown model: {model_id}")

    hero_jury = data.get("hero_jury", [])
    for model_id in hero_jury:
        if model_id not in models:
            errors.append(f"hero_jury references unknown model: {model_id}")

    rigged_categories = ("hero", "party", "enemy", "boss")
    timing_count = 0
    for model_id, meta in models.items():
        if not meta.get("path"):
            errors.append(f"models.{model_id} missing path")
        category = meta.get("category", "")
        allowed = meta.get("allowed_animations")
        required = meta.get("required_animations")
        timing = meta.get("animation_timing")

        if category in rigged_categories:
            if not allowed:
                errors.append(f"models.{model_id} ({category}) missing allowed_animations")
            if required is None:
                errors.append(f"models.{model_id} ({category}) missing required_animations field")

        if meta.get("hero_jury") is False and model_id in hero_jury:
            errors.append(f"models.{model_id} has hero_jury:false but is listed in hero_jury")

        if timing:
            timing_count += 1
            validate_timing_block(model_id, timing, allowed, required, errors)
        elif allowed and required and category in rigged_categories:
            errors.append(f"models.{model_id} rigged model missing animation_timing block")

    if errors:
        print("QA CATALOG VALIDATION FAILED", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(
        f"OK — {len(models)} models, {timing_count} with animation_timing, "
        f"version={data.get('version')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
