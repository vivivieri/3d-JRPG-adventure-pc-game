#!/usr/bin/env python3
"""Close active sprint — carry incomplete issues to next sprint board."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BOARD_PATH = ROOT / "game/data/qa/sprint_board.json"
PHASES_PATH = ROOT / "game/data/qa/sprint_phases.json"

sys.path.insert(0, str(ROOT / "tools"))
from pm_orchestrator_lib import load_board, save_json  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Close sprint and open next")
    parser.add_argument("--next-sprint-number", type=int, required=True, help="e.g. 2 for Sprint2")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    board = load_board()
    active = board.get("active_sprint", {})
    phase = active.get("phase", 1)
    old_id = active.get("id", "")
    new_id = f"Phase{phase}-Sprint{args.next_sprint_number}"

    incomplete = [i for i in board.get("issues", []) if i.get("status") not in ("done", "carry_over")]
    carry: list[dict[str, Any]] = []
    for issue in incomplete:
        carried = dict(issue)
        carried["status"] = "carry_over"
        carried["carry_over_from"] = old_id
        carried["escalation_level"] = min(4, int(issue.get("escalation_level", 0)) + 1)
        carry.append(carried)

    closed = {
        "id": old_id,
        "closed_at": datetime.now(timezone.utc).isoformat(),
        "incomplete_carried": [i["id"] for i in incomplete],
    }
    board.setdefault("closed_sprints", []).append(closed)

    if args.dry_run:
        print(json.dumps({"would_carry": [i["id"] for i in carry], "new_sprint": new_id}, indent=2))
        return 0

    board["previous_sprint"] = old_id
    board["active_sprint"] = {
        **active,
        "id": new_id,
        "sprint_number": args.next_sprint_number,
        "status": "active",
        "started_at": datetime.now(timezone.utc).date().isoformat(),
    }
    # PM must add new sprint issues + merge carry into issues list
    board["issues"] = carry
    board["carry_over_queue"] = [
        {
            "id": i["id"],
            "reason": f"carried from {old_id} — PM must re-file GitHub issue and reset status",
            "detected_at": datetime.now(timezone.utc).isoformat(),
        }
        for i in carry
    ]

    save_json(BOARD_PATH, board)
    print(f"OK — closed {old_id}; opened {new_id} with {len(carry)} carry-over items")
    print("PM MUST: update docs/sprints/ issue pack + clear carry_over_queue after filing issues")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
