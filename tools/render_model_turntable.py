#!/usr/bin/env python3
"""Render 4-view turntable PNGs for a GLB via Blender (docs/art/MODEL_QA.md §M3).

Usage:
  python3 tools/render_model_turntable.py --model urashima
  blender --background --python tools/blender_turntable_render.py -- <args>
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from model_qa_lib import ROOT, load_catalog, model_path  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="Render model turntable (MODEL_QA.md)")
    ap.add_argument("--model", required=True)
    ap.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Default: artifacts/model_reviews/<model_id>/",
    )
    args = ap.parse_args()

    catalog = load_catalog()
    if args.model not in catalog["models"]:
        print(f"Unknown model: {args.model}", file=sys.stderr)
        return 2

    glb = model_path(args.model, catalog)
    if not glb.is_file():
        print(f"GLB missing: {glb}", file=sys.stderr)
        return 2

    out_dir = args.out_dir or (ROOT / "artifacts/model_reviews" / args.model)
    out_dir.mkdir(parents=True, exist_ok=True)

    script = ROOT / "tools/blender_turntable_render.py"
    cmd = [
        "blender",
        "--background",
        "--python",
        str(script),
        "--",
        str(glb),
        str(out_dir),
    ]
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)
    print(f"Turntable written to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
