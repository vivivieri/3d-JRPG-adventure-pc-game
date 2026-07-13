#!/usr/bin/env python3
"""Update sprint_board.json issue state — PM Agent only after agent sessions."""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOARD_PATH = ROOT / "game/data/qa/sprint_board.json"

sys.path.insert(0, str(ROOT / "tools"))
from pm_orchestrator_lib import VALID_STATUS, load_board, save_json, validate_board_schema  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Update sprint board issue")
    parser.add_argument("issue_id", help="e.g. P1-02")
    parser.add_argument("--status", choices=sorted(VALID_STATUS))
    parser.add_argument("--agent", help="Record agent role for session")
    parser.add_argument("--commit", help="Last commit SHA")
    parser.add_argument("--github-issue", help="GitHub issue number or URL")
    parser.add_argument("--escalation", type=int, help="Escalation level 0-4")
    parser.add_argument("--note", help="PM note appended to issue")
    args = parser.parse_args()

    board = load_board()
    found = None
    for issue in board.get("issues", []):
        if issue.get("id") == args.issue_id:
            found = issue
            break
    if not found:
        print(f"Unknown issue {args.issue_id}", file=sys.stderr)
        return 1

    now = datetime.now(timezone.utc).isoformat()
    if args.status:
        found["status"] = args.status
        if args.status == "in_progress":
            found["last_agent_session"] = now
    if args.agent:
        found["last_agent_session"] = now
    if args.commit:
        found["last_commit_sha"] = args.commit
        found["last_agent_session"] = now
    if args.github_issue:
        found["github_issue"] = args.github_issue
    if args.escalation is not None:
        found["escalation_level"] = args.escalation
    if args.note:
        notes = found.setdefault("pm_notes", [])
        notes.append({"at": now, "text": args.note})

    errors = validate_board_schema(board, strict=True)
    if errors:
        print("Board invalid after update:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    save_json(BOARD_PATH, board)
    print(f"OK — updated {args.issue_id} status={found.get('status')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
