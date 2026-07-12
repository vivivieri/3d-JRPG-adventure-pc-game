#!/usr/bin/env python3
"""Validate game/data/qa/sprint_phases.json (docs/AGILE_WITHIN_PHASES.md)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "game/data/qa/sprint_phases.json"


def main() -> int:
    if not PATH.is_file():
        print(f"Missing {PATH}", file=sys.stderr)
        return 2
    data = json.loads(PATH.read_text(encoding="utf-8"))
    errors: list[str] = []
    phases = data.get("phases", [])
    if not phases:
        errors.append("phases must be non-empty")
    active = data.get("active_phase")
    phase_nums = [p.get("phase") for p in phases]
    if active is not None and active not in phase_nums:
        errors.append(f"active_phase {active} not in phases list")
    for p in phases:
        if "phase" not in p or "name" not in p:
            errors.append("each phase needs phase and name")
            break
    linear_projects = data.get("linear", {}).get("projects", [])
    if not linear_projects:
        errors.append("linear.projects must be non-empty")
    sm = data.get("sprint_master", {})
    if sm and sm.get("role") not in (None, "pm"):
        errors.append("sprint_master.role must be 'pm' when set")
    cadence = data.get("sprint_cadence", {})
    if cadence:
        for key in ("default_weeks", "min_weeks", "max_weeks"):
            if key in cadence and not isinstance(cadence[key], int):
                errors.append(f"sprint_cadence.{key} must be int")
        if all(k in cadence for k in ("min_weeks", "max_weeks", "default_weeks")):
            if not (cadence["min_weeks"] <= cadence["default_weeks"] <= cadence["max_weeks"]):
                errors.append("sprint_cadence min <= default <= max")
    for p in phases:
        rc = p.get("recommended_cadence_weeks")
        if rc is not None and (not isinstance(rc, int) or rc < 1 or rc > 4):
            errors.append(f"phase {p.get('phase')}: recommended_cadence_weeks must be 1-4")
    if errors:
        print("SPRINT PHASES VALIDATION FAILED", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print(f"OK — {len(phases)} phases, active_phase={active}, model={data.get('model')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
