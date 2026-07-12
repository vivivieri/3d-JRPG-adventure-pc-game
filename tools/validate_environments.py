#!/usr/bin/env python3
"""Validate game/data/qa/environments.json (docs/ENVIRONMENTS.md)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / "game/data/qa/environments.json"


def main() -> int:
    if not ENV_PATH.is_file():
        print(f"Missing {ENV_PATH}", file=sys.stderr)
        return 2
    data = json.loads(ENV_PATH.read_text(encoding="utf-8"))
    errors: list[str] = []
    envs = data.get("environments", {})
    if not envs:
        errors.append("environments must be non-empty")
    required_envs = ("design", "development", "qa", "uat", "production")
    for name in required_envs:
        if name not in envs:
            errors.append(f"missing environment: {name}")
    chain = data.get("promotion_chain", [])
    if "development" not in chain or "qa" not in chain:
        errors.append("promotion_chain must include development and qa")
    if errors:
        print("ENVIRONMENTS VALIDATION FAILED", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print(f"OK — {len(envs)} environments, chain={' → '.join(chain)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
