#!/usr/bin/env python3
"""Verify ship GLB .import files reference glb_toon_post_import.gd (MODEL_QA §M2b)."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GLB_ROOT = ROOT / "game/assets/models"
POST_IMPORT_RES = "res://scripts/editor/glb_toon_post_import.gd"
POST_IMPORT_REL = "scripts/editor/glb_toon_post_import.gd"


def main() -> int:
    ap = argparse.ArgumentParser(description="GLB post-import script audit")
    ap.add_argument(
        "--strict",
        action="store_true",
        help="FAIL when GLBs exist but post-import not configured",
    )
    args = ap.parse_args()

    if not GLB_ROOT.is_dir():
        print("[SKIP] game/assets/models/ not present")
        return 2

    glbs = sorted(GLB_ROOT.rglob("*.glb"))
    if not glbs:
        print("[SKIP] no .glb files under game/assets/models/")
        return 2

    fail = 0
    checked = 0
    for glb in glbs:
        rel = glb.relative_to(ROOT / "game").as_posix()
        import_path = glb.with_suffix(glb.suffix + ".import")
        checked += 1
        if not import_path.is_file():
            if args.strict:
                print(f"[FAIL] {rel} — missing .import sidecar (reimport in Godot)", file=sys.stderr)
                fail += 1
            else:
                print(f"[WARN] {rel} — no .import sidecar yet")
            continue
        text = import_path.read_text(encoding="utf-8", errors="replace")
        if POST_IMPORT_REL not in text and POST_IMPORT_RES not in text:
            msg = f"[FAIL] {rel} — post_import_script not set to {POST_IMPORT_RES}"
            if args.strict:
                print(msg)
                fail += 1
            else:
                print(msg.replace("[FAIL]", "[WARN]"), file=sys.stderr)
        else:
            print(f"[OK]   {rel}")

    if checked == 0:
        return 2
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
