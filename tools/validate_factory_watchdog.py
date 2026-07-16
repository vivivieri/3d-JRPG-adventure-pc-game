#!/usr/bin/env python3
"""Validate game/data/qa/factory_watchdog.json — L0_factory_watchdog gate."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "game/data/qa/factory_watchdog.json"

REQUIRED_TOP = ("version", "thresholds", "triggers", "recovery_actions", "policy")
REQUIRED_THRESHOLDS = (
    "stall_hours_idle",
    "stale_hours_in_progress",
    "recovery_cooldown_hours",
    "max_recovery_attempts_per_issue",
    "max_recovery_attempts_per_sprint",
    "heartbeat_stale_hours",
)


def main() -> int:
    if not CONFIG_PATH.is_file():
        print(f"Missing {CONFIG_PATH}", file=sys.stderr)
        return 1

    data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    errors: list[str] = []

    for key in REQUIRED_TOP:
        if key not in data:
            errors.append(f"missing top-level key: {key}")

    thresholds = data.get("thresholds", {})
    for key in REQUIRED_THRESHOLDS:
        if key not in thresholds:
            errors.append(f"thresholds missing {key}")
        elif not isinstance(thresholds[key], (int, float)) or thresholds[key] <= 0:
            errors.append(f"thresholds.{key} must be positive number")

    # stall must be less than stale (otherwise stall never fires before stale)
    stall = thresholds.get("stall_hours_idle", 0)
    stale = thresholds.get("stale_hours_in_progress", 0)
    if stall and stale and stall >= stale:
        errors.append(f"stall_hours_idle ({stall}) must be < stale_hours_in_progress ({stale})")

    cooldown = thresholds.get("recovery_cooldown_hours", 0)
    if cooldown and stall and cooldown > stall:
        errors.append("recovery_cooldown_hours should not exceed stall_hours_idle")

    if errors:
        print("factory_watchdog.json validation FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("factory_watchdog.json: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
