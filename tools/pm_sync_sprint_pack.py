#!/usr/bin/env python3
"""Sync sprint issue pack with sprint_board — fail if pack/board diverge."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from pm_orchestrator_lib import load_board, parse_issue_pack, save_json, sync_missing_from_pack  # noqa: E402

BOARD_PATH = ROOT / "game/data/qa/sprint_board.json"


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync sprint issue pack with board")
    parser.add_argument("--fix", action="store_true", help="Append carry_over_queue entries for pack-only ids")
    args = parser.parse_args()

    board = load_board()
    pack_ref = board.get("active_sprint", {}).get("issue_pack_ref", "")
    pack_path = ROOT / pack_ref if pack_ref else None
    if not pack_path or not pack_path.is_file():
        print(f"[FAIL] issue pack missing: {pack_ref}", file=sys.stderr)
        return 1

    pack_ids = parse_issue_pack(pack_path)
    board_ids = {i["id"] for i in board.get("issues", [])}
    missing_in_board = sorted(set(pack_ids) - board_ids)
    missing_in_pack = sorted(board_ids - set(pack_ids))

    if missing_in_pack:
        print("[FAIL] board has issues not in pack:", ", ".join(missing_in_pack), file=sys.stderr)
        return 1

    if missing_in_board:
        if args.fix:
            added, _ = sync_missing_from_pack(board, dry_run=False)
            save_json(BOARD_PATH, board)
            print(f"[WARN] added {len(added)} ids to carry_over_queue — PM must fill full issue rows")
            return 1
        print("[FAIL] pack issues missing from sprint_board:", ", ".join(missing_in_board), file=sys.stderr)
        print("  Fix: add full issue objects to game/data/qa/sprint_board.json", file=sys.stderr)
        return 1

    if board.get("carry_over_queue"):
        print("[FAIL] carry_over_queue non-empty — PM must resolve before dispatch", file=sys.stderr)
        for item in board["carry_over_queue"]:
            print(f"  - {item.get('id')}: {item.get('reason')}", file=sys.stderr)
        return 1

    print(f"OK — pack and board aligned ({len(pack_ids)} issues)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
