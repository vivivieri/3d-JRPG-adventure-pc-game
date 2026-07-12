#!/usr/bin/env python3
"""Verify GLB animation names ⊆ qa_catalog whitelist (docs/CHARACTER_BIBLE.md §8)."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from model_qa_lib import ROOT, load_catalog, model_path, parse_glb  # noqa: E402


def animation_names(gltf: dict) -> list[str]:
    names: list[str] = []
    for anim in gltf.get("animations", []):
        name = anim.get("name", "").strip()
        if name:
            names.append(name)
    return names


def check_model(model_id: str, catalog: dict) -> tuple[bool, list[str]]:
    meta = catalog["models"][model_id]
    allowed = meta.get("allowed_animations")
    if not allowed:
        return True, [f"SKIP: no allowed_animations for {model_id}"]

    path = model_path(model_id, catalog)
    if not path.is_file():
        return True, [f"SKIP: missing {meta['path']}"]

    gltf, _ = parse_glb(path)
    found = animation_names(gltf)
    if not found:
        return False, ["FAIL: GLB has no named animations"]

    allowed_set = set(allowed)
    extra = sorted(set(found) - allowed_set)
    if extra:
        return False, [f"FAIL: animations not in whitelist: {', '.join(extra)}"]
    return True, [f"OK: {len(found)} animations ⊆ whitelist"]


def main() -> int:
    ap = argparse.ArgumentParser(description="Animation whitelist QA")
    ap.add_argument("--model", action="append", dest="models", default=[])
    ap.add_argument("--phase", type=int, default=1)
    args = ap.parse_args()

    catalog = load_catalog()
    phase_key = str(args.phase) if str(args.phase) in catalog.get("phase_required", {}) else "m5"
    ids = args.models or catalog.get("phase_required", {}).get(str(args.phase), [])

    fail = 0
    checked = 0
    for model_id in ids:
        if model_id not in catalog["models"]:
            continue
        if "allowed_animations" not in catalog["models"][model_id]:
            continue
        checked += 1
        print(f"\n==> {model_id}")
        ok, lines = check_model(model_id, catalog)
        for line in lines:
            print(f"  {line}")
        if not ok:
            fail += 1

    if checked == 0:
        print("SKIP: no rigged models with allowed_animations on disk for this phase")
        return 0
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
