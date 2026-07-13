#!/usr/bin/env python3
"""Validate game/data/qa/stakeholder_report_config.json — L0_stakeholder_report gate."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "game/data/qa/stakeholder_report_config.json"

REQUIRED = ("version", "product_owner", "telegram", "triggers", "outputs")
VALID_TRIGGERS = {
    "agent_cycle_complete",
    "agent_cycle_failed",
    "sprint_cycle_complete",
    "phase_exit",
    "uat_ready",
    "watchdog_recovery",
    "mcp_blocked",
    "pm_session",
}


def main() -> int:
    if not CONFIG_PATH.is_file():
        print(f"Missing {CONFIG_PATH}", file=sys.stderr)
        return 1

    data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    errors: list[str] = []

    for key in REQUIRED:
        if key not in data:
            errors.append(f"missing {key}")

    triggers = data.get("triggers", {})
    for name in triggers:
        if name not in VALID_TRIGGERS:
            errors.append(f"unknown trigger {name}")

    for name in ("agent_cycle_complete", "sprint_cycle_complete", "uat_ready"):
        if name not in triggers:
            errors.append(f"missing required trigger config: {name}")

    outputs = data.get("outputs", {})
    for key in ("latest_json", "latest_markdown", "latest_html"):
        if key not in outputs:
            errors.append(f"outputs missing {key}")

    if errors:
        print("stakeholder_report_config.json FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("stakeholder_report_config.json: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
