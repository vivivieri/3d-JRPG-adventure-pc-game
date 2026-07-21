#!/usr/bin/env python3
"""Verify required 3D models exist for a phase (docs/art/MODEL_QA.md §M1)."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from model_qa_lib import ROOT, load_catalog, model_path  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="Model catalog check (MODEL_QA.md)")
    ap.add_argument("--phase", default="1", help="1 or m5")
    args = ap.parse_args()

    catalog = load_catalog()
    phase = args.phase.lower()
    required = catalog.get("phase_required", {}).get(phase)
    if not required:
        print(f"Unknown phase: {phase}", file=sys.stderr)
        return 2

    print(f"Model catalog check — phase {phase}")
    missing = []
    for model_id in required:
        path = model_path(model_id, catalog)
        if path.is_file():
            print(f"  [OK]   {model_id} → {path.relative_to(ROOT)}")
        else:
            rel = catalog["models"][model_id]["path"]
            print(f"  [FAIL] {model_id} missing ({rel})", file=sys.stderr)
            missing.append(model_id)

    if missing:
        print(f"\nCatalog FAIL — {len(missing)} missing")
        return 1
    print(f"\nCatalog PASS — {len(required)} model(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
