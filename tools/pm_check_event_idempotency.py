#!/usr/bin/env python3
"""Check cycle event idempotency before PM orchestrator runs."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVENT_FILE = ROOT / "artifacts/agent_cycle_event.json"

sys.path.insert(0, str(ROOT / "tools"))
from pm_event_lib import mark_event_handled, should_skip_duplicate_event  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="PM event idempotency guard")
    parser.add_argument("--mark-handled", action="store_true", help="Record event as handled after orchestrator PASS")
    parser.add_argument("--cooldown-minutes", type=int, default=30)
    args = parser.parse_args()

    if not EVENT_FILE.is_file():
        print("OK — no pending agent_cycle_event.json (cold start or manual PM)")
        return 0

    payload = json.loads(EVENT_FILE.read_text(encoding="utf-8"))
    skip, reason = should_skip_duplicate_event(payload, cooldown_minutes=args.cooldown_minutes)
    if skip and not args.mark_handled:
        print(f"[SKIP] Duplicate event — {reason}")
        print(f"       event={payload.get('event')} issue={payload.get('issue_id')}")
        return 0

    if args.mark_handled:
        mark_event_handled(payload)
        print(f"OK — marked handled: {payload.get('event')} {payload.get('issue_id')}")
        return 0

    print(f"OK — new event: {payload.get('event')} issue={payload.get('issue_id')} ({reason})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
