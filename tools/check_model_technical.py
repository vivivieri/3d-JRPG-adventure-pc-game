#!/usr/bin/env python3
"""Technical GLB QA: triangles, textures, greybox ban (docs/art/MODEL_QA.md §M2)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from model_qa_lib import (  # noqa: E402
    ROOT,
    count_images,
    count_triangles,
    is_greybox_source,
    load_catalog,
    model_path,
    parse_glb,
)

HERO_MIN_BYTES = 100_000


def check_one(model_id: str, catalog: dict, ship: bool) -> tuple[bool, list[str]]:
    meta = catalog["models"][model_id]
    path = ROOT / meta["path"]
    issues: list[str] = []
    ok = True
    rel = meta["path"]

    if not path.is_file():
        return False, [f"FAIL: file missing ({rel})"]

    if is_greybox_source(rel):
        msg = f"{rel} is Kenney/greybox source"
        if ship:
            issues.append(f"FAIL: {msg}")
            ok = False
        else:
            issues.append(f"WARN: {msg}")

    size = path.stat().st_size
    category = meta.get("category", "")
    if category in ("hero", "party", "boss", "set_piece") and size < HERO_MIN_BYTES:
        issues.append(f"WARN: file size {size} bytes — likely blockout/low detail")

    try:
        gltf, _bin = parse_glb(path)
    except (ValueError, json.JSONDecodeError, OSError) as exc:
        return False, [f"FAIL: GLB parse error: {exc}"]

    tris = count_triangles(gltf)
    tmin, tmax = meta.get("tris_min", 0), meta.get("tris_max", 999_999)
    if tris < tmin or tris > tmax:
        level = "FAIL" if ship else "WARN"
        issues.append(f"{level}: {tris} tris, expected {tmin}–{tmax}")
        if level == "FAIL":
            ok = False

    images = count_images(gltf)
    tneed = meta.get("texture_min", 0)
    if images < tneed:
        issues.append(f"FAIL: {images} embedded textures, need >= {tneed}")
        ok = False

    if ok and not any(i.startswith("FAIL") for i in issues):
        issues.append(f"OK: {tris} tris, {images} textures, {size} bytes")
    return ok, issues


def main() -> int:
    ap = argparse.ArgumentParser(description="Technical model QA (MODEL_QA.md)")
    ap.add_argument("--model", action="append", dest="models", default=[])
    ap.add_argument("--all-present", action="store_true")
    ap.add_argument("--ship", action="store_true")
    args = ap.parse_args()

    catalog = load_catalog()
    ids: list[str] = []
    if args.all_present:
        audio_root = ROOT / "game/assets/models"
        for glb in sorted(audio_root.rglob("*.glb")):
            rel = str(glb.relative_to(ROOT))
            found = next((k for k, v in catalog["models"].items() if v["path"] == rel), None)
            ids.append(found or glb.stem)
        # dedupe catalog ids only for known
        ids = [i for i in ids if i in catalog["models"]]
    elif args.models:
        ids = args.models
    else:
        ap.print_help()
        return 2

    fail = 0
    for model_id in ids:
        if model_id not in catalog["models"]:
            print(f"\n==> {model_id} (not in qa_catalog.json — skip)")
            continue
        print(f"\n==> {model_id}")
        ok, issues = check_one(model_id, catalog, ship=args.ship)
        has_fail = False
        for line in issues:
            print(f"  {line}")
            if line.startswith("FAIL"):
                has_fail = True
        if has_fail or not ok:
            print("  [FAIL] technical")
            fail += 1
        elif any(line.startswith("WARN") for line in issues):
            print("  [WARN] technical")
        else:
            print("  [PASS] technical")
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
