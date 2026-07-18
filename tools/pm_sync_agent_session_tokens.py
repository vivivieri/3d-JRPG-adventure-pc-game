#!/usr/bin/env python3
"""Backfill token usage for agent sessions missing cursor_api tokens.

Reads artifacts/agent_session_telemetry/events.jsonl, finds session_end events
with cursor_bc_id but no tokens_total, fetches Cursor API usage, and rewrites
the per-issue evidence rollup.

Usage:
  python3 tools/pm_sync_agent_session_tokens.py
  python3 tools/pm_sync_agent_session_tokens.py --dry-run

Requires: CURSOR_API_KEY in Cursor Secrets (see docs/agents/CURSOR_SECRETS_SETUP.md §8)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from agent_session_telemetry_lib import EVENTS_PATH, read_events  # noqa: E402
from collect_cursor_agent_usage import (  # noqa: E402
    fetch_with_retry,
    resolve_api_key,
    usage_delta,
    usage_to_telemetry_fields,
)

PENDING_PATH = ROOT / "artifacts/agent_session_telemetry/pending_token_sync.jsonl"


def sessions_needing_sync(events: list[dict]) -> list[dict]:
    """Terminal events missing token data but having bc_id."""
    need: list[dict] = []
    for ev in events:
        if ev.get("event") not in ("session_end", "session_failed"):
            continue
        if ev.get("tokens_total") is not None:
            continue
        bc = ev.get("cursor_bc_id")
        if bc:
            need.append(ev)
    return need


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--retries", type=int, default=3)
    args = ap.parse_args()

    if not resolve_api_key():
        print("[FAIL] CURSOR_API_KEY not set — see docs/agents/CURSOR_SECRETS_SETUP.md §8")
        return 1

    events = read_events()
    pending = sessions_needing_sync(events)
    if not pending:
        print("No sessions need token backfill.")
        return 0

    synced = 0
    for ev in pending:
        bc_id = ev["cursor_bc_id"]
        session_id = ev["session_id"]
        print(f"==> Sync {session_id} bc={bc_id}")
        payload = fetch_with_retry(bc_id, retries=args.retries)
        if not payload:
            print(f"  [WARN] usage not available for {bc_id}")
            continue

        fields = usage_to_telemetry_fields(payload)
        if args.dry_run:
            print(f"  [DRY] tokens_total={fields.get('tokens_total')}")
            synced += 1
            continue

        # Append backfill record (immutable log — do not rewrite history)
        backfill = {
            **ev,
            "event": "session_token_backfill",
            "schema_version": ev.get("schema_version", "1.0"),
            **{k: v for k, v in fields.items() if k != "cursor_usage_raw"},
            "cursor_usage_raw": fields.get("cursor_usage_raw"),
            "backfill_note": "pm_sync_agent_session_tokens.py",
        }
        with EVENTS_PATH.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(backfill, ensure_ascii=False) + "\n")
        print(f"  [OK] tokens_total={fields.get('tokens_total')}")
        synced += 1

    print(f"Synced {synced}/{len(pending)} sessions")
    return 0 if synced == len(pending) else 1


if __name__ == "__main__":
    sys.exit(main())
