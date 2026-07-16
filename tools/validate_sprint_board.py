#!/usr/bin/env python3
"""Validate game/data/qa/sprint_board.json — L0_sprint_board gate."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOARD_PATH = ROOT / "game/data/qa/sprint_board.json"
PHASES_PATH = ROOT / "game/data/qa/sprint_phases.json"

sys.path.insert(0, str(ROOT / "tools"))
from pm_orchestrator_lib import (  # noqa: E402
    load_board,
    parse_issue_pack,
    validate_board_schema,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate sprint board")
    parser.add_argument("--strict", action="store_true", help="Strict field checks")
    args = parser.parse_args()

    errors: list[str] = []
    if not BOARD_PATH.is_file():
        print(f"Missing {BOARD_PATH}", file=sys.stderr)
        return 1

    board = load_board()
    errors.extend(validate_board_schema(board, strict=args.strict))

    # Developer traceability: the acceptance criteria a dev is handed must reference
    # gates that actually exist (and are documented) in acceptance_criteria.json, and
    # implementation issues must point to design docs (handoff_refs) telling the dev
    # what to build. Keeps "what to develop + how it's judged" real and unambiguous.
    crit_path = ROOT / "game/data/qa/acceptance_criteria.json"
    if crit_path.is_file():
        crit = json.loads(crit_path.read_text(encoding="utf-8"))
        known_gates = set(crit.get("gates", {}))
        # Catalog meta-gates validated elsewhere but legitimately referenceable by tasks.
        known_gates.update({"L0_acceptance_catalog", "L0_environments_catalog", "L0_sprint_phases"})

        active = board.get("active_sprint", {})
        for gid in active.get("phase_exit_gate_ids", []):
            if gid not in known_gates:
                errors.append(f"active_sprint.phase_exit_gate_ids references unknown gate '{gid}'")

        impl_owners = {"architect", "builder", "visual", "flow"}
        for issue in board.get("issues", []):
            iid = issue.get("id", "?")
            for gid in issue.get("acceptance_gate_ids", []):
                if gid not in known_gates:
                    errors.append(f"{iid}: acceptance_gate_ids references unknown gate '{gid}'")
            if args.strict and issue.get("status") not in ("done", "carry_over"):
                if issue.get("agent_owner") in impl_owners and not issue.get("handoff_refs"):
                    errors.append(f"{iid}: implementation issue missing handoff_refs (design docs telling the dev what to build)")

    # active phase alignment with sprint_phases.json
    if PHASES_PATH.is_file():
        phases = json.loads(PHASES_PATH.read_text(encoding="utf-8"))
        active_phase = phases.get("active_phase")
        sprint_phase = board.get("active_sprint", {}).get("phase")
        if active_phase is not None and sprint_phase != active_phase:
            errors.append(
                f"active_sprint.phase {sprint_phase} != sprint_phases.active_phase {active_phase}"
            )

    pack_ref = board.get("active_sprint", {}).get("issue_pack_ref", "")
    if pack_ref:
        pack_path = ROOT / pack_ref
        if not pack_path.is_file():
            errors.append(f"issue_pack_ref not found: {pack_ref}")
        else:
            pack_ids = set(parse_issue_pack(pack_path))
            board_ids = {i["id"] for i in board.get("issues", [])}
            missing = sorted(pack_ids - board_ids)
            if missing:
                errors.append(f"issue pack ids missing from board: {', '.join(missing)}")

    if errors:
        print("SPRINT BOARD VALIDATION FAILED", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    n = len(board.get("issues", []))
    sid = board.get("active_sprint", {}).get("id", "?")
    print(f"OK — sprint {sid}, {n} issues, carry_over={len(board.get('carry_over_queue', []))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
