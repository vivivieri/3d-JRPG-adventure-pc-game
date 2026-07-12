#!/usr/bin/env python3
"""Validate game/data/code/base_classes.json (docs/CODE_BASE_CLASS_RULES.md)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "game/data/code/base_classes.json"


def main() -> int:
    if not PATH.is_file():
        print(f"Missing {PATH}", file=sys.stderr)
        return 2
    data = json.loads(PATH.read_text(encoding="utf-8"))
    errors: list[str] = []
    bases = data.get("bases", [])
    if not bases:
        errors.append("bases must be non-empty")
    ids = set()
    for b in bases:
        if "id" not in b or "path" not in b:
            errors.append("each base needs id and path")
            break
        if b["id"] in ids:
            errors.append(f"duplicate base id: {b['id']}")
        ids.add(b["id"])
        if b.get("agent_rule") not in ("extend_only", "architect_only"):
            errors.append(f"invalid agent_rule for {b.get('id')}")
    comps = data.get("component_scenes", [])
    if not comps:
        errors.append("component_scenes must be non-empty")
    if errors:
        print("BASE CLASSES VALIDATION FAILED", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print(f"OK — {len(bases)} bases, {len(comps)} component scenes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
