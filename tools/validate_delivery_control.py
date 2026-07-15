#!/usr/bin/env python3
"""Validate game/data/qa/delivery_control.json — L0_delivery_control gate.

See docs/DELIVERY_CONTROL.md.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "game/data/qa/delivery_control.json"

REQUIRED_TOP = ("version", "policy", "channels", "deliveries")
VALID_OPS = {"==", "!=", "<=", ">=", "<", ">"}
VALID_CHECK_TYPES = {"command", "artifacts_exist", "metric"}


def main() -> int:
    if not CONFIG_PATH.is_file():
        print(f"Missing {CONFIG_PATH}", file=sys.stderr)
        return 1

    data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    errors: list[str] = []

    for key in REQUIRED_TOP:
        if key not in data:
            errors.append(f"missing top-level key: {key}")

    policy = data.get("policy", {})
    if "require_confirmation" not in policy:
        errors.append("policy missing require_confirmation")

    approval = policy.get("approval")
    if approval is not None:
        ra = approval.get("required_approvals")
        if not isinstance(ra, int) or ra < 0:
            errors.append("policy.approval.required_approvals must be a non-negative integer")
        if not isinstance(approval.get("reviewer_roles", []), list):
            errors.append("policy.approval.reviewer_roles must be a list")
        if ra and not approval.get("reviewer_roles"):
            errors.append("policy.approval requires reviewer_roles when required_approvals >= 1")

    channels = data.get("channels", {})
    if not channels:
        errors.append("channels must be non-empty")

    deliveries = data.get("deliveries", {})
    if not deliveries:
        errors.append("deliveries must be non-empty")

    for name, spec in deliveries.items():
        ch = spec.get("channel")
        if ch not in channels:
            errors.append(f"delivery '{name}' references unknown channel '{ch}'")
        if not isinstance(spec.get("review_checklist", []), list):
            errors.append(f"delivery '{name}' review_checklist must be a list")
        checks = spec.get("checks", [])
        if not checks:
            errors.append(f"delivery '{name}' has no checks")
        for c in checks:
            ctype = c.get("type")
            if ctype not in VALID_CHECK_TYPES:
                errors.append(f"delivery '{name}' check '{c.get('id')}' has invalid type '{ctype}'")
            if ctype == "command" and not c.get("cmd"):
                errors.append(f"delivery '{name}' command check '{c.get('id')}' missing cmd")
            if ctype == "metric":
                if c.get("op") not in VALID_OPS:
                    errors.append(f"delivery '{name}' metric check '{c.get('id')}' invalid op '{c.get('op')}'")
                if "field" not in c or "value" not in c:
                    errors.append(f"delivery '{name}' metric check '{c.get('id')}' missing field/value")
            if ctype == "artifacts_exist" and not spec.get("required_artifacts"):
                errors.append(f"delivery '{name}' artifacts_exist check but no required_artifacts")

    if errors:
        print("delivery_control.json validation FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"delivery_control.json: OK ({len(deliveries)} delivery kind(s), {len(channels)} channel(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
