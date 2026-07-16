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
        atd = p.get("ai_native_target_days")
        if atd is not None and (not isinstance(atd, int) or atd < 1):
            errors.append(f"phase {p.get('phase')}: ai_native_target_days must be positive int")
    batch = data.get("ai_native_batch", {})
    if batch:
        micro = batch.get("micro_cycle", {})
        if micro and micro.get("max_issues", 0) < 1:
            errors.append("ai_native_batch.micro_cycle.max_issues must be >= 1")
        if batch.get("primary_unit") not in (None, "session_batch"):
            errors.append("ai_native_batch.primary_unit must be 'session_batch' when set")
    backlog_path = ROOT / "game/data/qa/generation_readiness_backlog.json"
    backlog_ids: set[str] = set()
    if backlog_path.is_file():
        backlog_ids = {i.get("id") for i in json.loads(backlog_path.read_text(encoding="utf-8")).get("items", [])}
    for p in phases:
        for gr_id in p.get("generation_readiness", []):
            if backlog_ids and gr_id not in backlog_ids:
                errors.append(f"phase {p.get('phase')}: unknown generation_readiness id {gr_id!r}")
    if errors:
        print("SPRINT PHASES VALIDATION FAILED", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print(f"OK — {len(phases)} phases, active_phase={active}, model={data.get('model')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
