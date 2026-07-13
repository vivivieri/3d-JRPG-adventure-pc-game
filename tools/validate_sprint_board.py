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
