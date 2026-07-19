#!/usr/bin/env python3
"""Verify GLB animation names ⊆ whitelist and required floor (CHARACTER_BIBLE §8)."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from model_qa_lib import animation_durations_ms, load_catalog, model_path, parse_glb  # noqa: E402


def animation_names(gltf: dict) -> list[str]:
    names: list[str] = []
    for anim in gltf.get("animations", []):
        name = anim.get("name", "").strip()
        if name:
            names.append(name)
    return names


def check_model(model_id: str, catalog: dict, *, strict: bool, check_timing: bool) -> tuple[bool, list[str]]:
    meta = catalog["models"][model_id]
    allowed = meta.get("allowed_animations")
    if not allowed:
        if strict and meta.get("rig"):
            return False, [f"FAIL: rigged model {model_id} missing allowed_animations in catalog"]
        if strict and meta.get("category") in ("boss", "hero", "party", "enemy"):
            return False, [f"FAIL: {model_id} ({meta.get('category')}) missing allowed_animations"]
        return True, [f"SKIP: no allowed_animations for {model_id}"]

    path = model_path(model_id, catalog)
    if not path.is_file():
        if strict:
            return False, [f"FAIL: missing required model {meta['path']}"]
        return True, [f"SKIP: missing {meta['path']}"]

    gltf, _ = parse_glb(path)
    found = animation_names(gltf)
    if not found:
        return False, ["FAIL: GLB has no named animations"]

    allowed_set = set(allowed)
    extra = sorted(set(found) - allowed_set)
    if extra:
        return False, [f"FAIL: animations not in whitelist: {', '.join(extra)}"]

    required = meta.get("required_animations") or allowed
    missing = sorted(set(required) - set(found))
    if missing:
        return False, [f"FAIL: missing required animations: {', '.join(missing)}"]

    lines = [f"OK: {len(found)} animations (required floor met)"]

    if check_timing:
        timing = meta.get("animation_timing") or {}
        if not timing:
            if strict:
                return False, lines + ["FAIL: missing animation_timing in catalog"]
            return True, lines + ["SKIP: no animation_timing in catalog"]

        gltf, bin_data = parse_glb(path)
        measured = animation_durations_ms(gltf, bin_data)
        timing_errors: list[str] = []
        for anim_name, spec in timing.items():
            if anim_name not in found:
                continue
            dur = measured.get(anim_name)
            if dur is None:
                timing_errors.append(f"FAIL: could not measure duration for {anim_name}")
                continue
            lo = int(spec.get("duration_ms_min", 0))
            hi = int(spec.get("duration_ms_max", 0))
            if dur < lo or dur > hi:
                timing_errors.append(
                    f"FAIL: {anim_name} duration {dur}ms outside [{lo}, {hi}]ms"
                )
        if timing_errors:
            return False, lines + timing_errors
        lines.append(f"OK: timing checked for {len(timing)} catalog clips")

    return True, lines


def resolve_phase(catalog: dict, phase: str) -> list[str]:
    phase_required = catalog.get("phase_required", {})
    if phase in phase_required:
        return list(phase_required[phase])
    return []


def main() -> int:
    ap = argparse.ArgumentParser(description="Animation whitelist QA")
    ap.add_argument("--model", action="append", dest="models", default=[])
    ap.add_argument("--phase", default="1", help="Phase key: 1, m5, etc.")
    ap.add_argument(
        "--strict",
        action="store_true",
        help="FAIL on missing models / missing animation policy (ship / game branch)",
    )
    ap.add_argument(
        "--check-timing",
        action="store_true",
        help="When GLB exists, verify clip durations within animation_timing catalog ranges",
    )
    args = ap.parse_args()

    catalog = load_catalog()
    ids = args.models or resolve_phase(catalog, args.phase)
    if not ids:
        print(f"[SKIP] no models for phase={args.phase}")
        return 2

    fail = 0
    checked = 0
    skipped = 0
    for model_id in ids:
        if model_id not in catalog["models"]:
            if args.strict:
                print(f"\n==> {model_id}")
                print("  FAIL: unknown model id in phase_required")
                fail += 1
            continue
        meta = catalog["models"][model_id]
        if "allowed_animations" not in meta and not meta.get("rig") and meta.get("category") not in (
            "boss",
            "hero",
            "party",
            "enemy",
        ):
            continue
        checked += 1
        print(f"\n==> {model_id}")
        ok, lines = check_model(model_id, catalog, strict=args.strict, check_timing=args.check_timing)
        for line in lines:
            print(f"  {line}")
        if not ok:
            fail += 1
        elif lines and lines[0].startswith("SKIP"):
            skipped += 1
            checked -= 1

    if checked == 0 and skipped > 0 and not args.strict:
        print("SKIP: no rigged models with allowed_animations on disk for this phase")
        return 2
    if checked == 0 and not args.strict:
        print("SKIP: no rigged models to check for this phase")
        return 2
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
