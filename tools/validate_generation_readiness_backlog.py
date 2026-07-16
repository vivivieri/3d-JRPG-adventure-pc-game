#!/usr/bin/env python3
"""Validate generation_readiness_backlog.json ↔ IMPLEMENTATION_PLAN task traceability."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKLOG_PATH = ROOT / "game/data/qa/generation_readiness_backlog.json"
PLAN_PATH = ROOT / "docs/workflow/IMPLEMENTATION_PLAN.md"
CRITERIA_PATH = ROOT / "game/data/qa/acceptance_criteria.json"
ZONE_PATH = ROOT / "game/data/qa/zone_composition.json"

TASK_RE = re.compile(r"^\d+\.\d+[a-z]?$")
PRIORITIES = {"P0", "P1", "P2"}
STATUSES = {"pending", "in_progress", "done", "waived"}


def main() -> int:
    errors: list[str] = []
    if not BACKLOG_PATH.is_file():
        print(f"Missing {BACKLOG_PATH}", file=sys.stderr)
        return 2

    backlog = json.loads(BACKLOG_PATH.read_text(encoding="utf-8"))
    items = backlog.get("items", [])
    if not items:
        errors.append("items must be non-empty")

    plan_text = PLAN_PATH.read_text(encoding="utf-8") if PLAN_PATH.is_file() else ""
    gates: set[str] = set()
    if CRITERIA_PATH.is_file():
        criteria = json.loads(CRITERIA_PATH.read_text(encoding="utf-8"))
        gates = set(criteria.get("gates", {}).keys())
        for section in criteria.get("phase_gates", {}).values():
            if isinstance(section, dict):
                for key in ("required_gates", "conditional_gates"):
                    for gid in section.get(key, []):
                        if isinstance(gid, str):
                            gates.add(gid)
        for gid in criteria.get("ci_gates", {}).get("required_gates", []):
            gates.add(gid)
        for gid in criteria.get("docs_ci_gates", {}).get("required_gates", []):
            gates.add(gid)

    seen_ids: set[str] = set()
    for item in items:
        iid = item.get("id", "")
        if not iid:
            errors.append("item missing id")
            continue
        if iid in seen_ids:
            errors.append(f"duplicate id: {iid}")
        seen_ids.add(iid)

        for key in ("title", "priority", "status", "phases", "owner", "design_ref"):
            if key not in item:
                errors.append(f"{iid}: missing {key}")

        priority = item.get("priority")
        if priority and priority not in PRIORITIES:
            errors.append(f"{iid}: invalid priority {priority!r}")

        status = item.get("status")
        if status and status not in STATUSES:
            errors.append(f"{iid}: invalid status {status!r}")

        phases = item.get("phases", [])
        if not isinstance(phases, list) or not phases:
            errors.append(f"{iid}: phases must be a non-empty list")
        for phase in phases:
            if not isinstance(phase, int) or phase < 0 or phase > 8:
                errors.append(f"{iid}: invalid phase {phase!r}")

        tasks = item.get("implementation_plan_tasks", [])
        if not tasks:
            errors.append(f"{iid}: implementation_plan_tasks must be non-empty")
        for task in tasks:
            if not TASK_RE.match(str(task)):
                errors.append(f"{iid}: invalid task id {task!r}")
            elif plan_text and f"| {task} |" not in plan_text:
                errors.append(f"{iid}: task {task} not found in IMPLEMENTATION_PLAN.md")

        for gid in item.get("gate_ids", []):
            if gates and gid not in gates:
                errors.append(f"{iid}: unknown gate_id {gid!r}")

        data_ref = item.get("data_ref")
        if data_ref and not (ROOT / data_ref).is_file():
            errors.append(f"{iid}: data_ref not found: {data_ref}")

    pending = sum(1 for i in items if i.get("status") == "pending")
    if errors:
        print("GENERATION READINESS BACKLOG VALIDATION FAILED", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(
        f"OK — {len(items)} backlog items ({pending} pending), "
        f"zone_composition={'yes' if ZONE_PATH.is_file() else 'no'}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
