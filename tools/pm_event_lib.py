#!/usr/bin/env python3
"""Event idempotency and cycle logging — docs/agents/SPRINT_ORCHESTRATION.md."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "artifacts/factory_state.json"
CYCLE_LOG_PATH = ROOT / "artifacts/factory_cycle_log.jsonl"
SNAPSHOT_PATH = ROOT / "game/data/qa/factory_health_snapshot.json"


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_factory_state() -> dict[str, Any]:
    return load_json(STATE_PATH)


def save_factory_state(state: dict[str, Any]) -> None:
    save_json(STATE_PATH, state)


def event_fingerprint(payload: dict[str, Any]) -> str:
    """Stable hash for duplicate webhook / double-emit detection."""
    key_fields = {
        "event": payload.get("event"),
        "issue_id": payload.get("issue_id"),
        "commit_sha": payload.get("commit_sha"),
        "agent_role": payload.get("agent_role"),
        "sprint_id": payload.get("sprint_id"),
    }
    raw = json.dumps(key_fields, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def should_skip_duplicate_event(payload: dict[str, Any], cooldown_minutes: int = 30) -> tuple[bool, str]:
    """Return (skip, reason). Skip if same fingerprint handled recently."""
    fp = event_fingerprint(payload)
    state = load_factory_state()
    last_fp = state.get("last_handled_event_id")
    last_at = state.get("last_handled_event_at")
    if last_fp != fp:
        return False, "new event"

    if not last_at:
        return False, "no prior timestamp"

    try:
        prev = datetime.fromisoformat(str(last_at).replace("Z", "+00:00"))
        if prev.tzinfo is None:
            prev = prev.replace(tzinfo=timezone.utc)
        age_min = (datetime.now(timezone.utc) - prev).total_seconds() / 60.0
        if age_min < cooldown_minutes:
            return True, f"duplicate within {age_min:.0f}m (cooldown {cooldown_minutes}m)"
    except ValueError:
        pass
    return False, "cooldown expired"


def mark_event_handled(payload: dict[str, Any]) -> None:
    state = load_factory_state()
    state["last_handled_event_id"] = event_fingerprint(payload)
    state["last_handled_event_at"] = datetime.now(timezone.utc).isoformat()
    state["last_handled_event_type"] = payload.get("event")
    state["last_handled_issue_id"] = payload.get("issue_id")
    save_factory_state(state)


def append_cycle_log(payload: dict[str, Any]) -> None:
    CYCLE_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CYCLE_LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False) + "\n")


def write_health_snapshot(
    *,
    event: str | None = None,
    issue_id: str | None = None,
    agent_role: str | None = None,
    commit_sha: str | None = None,
    sprint_id: str | None = None,
    status: str = "active",
    note: str | None = None,
) -> Path:
    """Committed snapshot for remote watchdog (game/data/qa/)."""
    now = datetime.now(timezone.utc).isoformat()
    prev = load_json(SNAPSHOT_PATH)
    sessions = int(prev.get("agent_sessions_this_sprint", 0))
    if event in ("agent_cycle_complete", "agent_cycle_failed", "watchdog_recovery"):
        sessions += 1

    snapshot = {
        "version": "1.0",
        "updated_at": now,
        "status": status,
        "last_event": event,
        "last_issue_id": issue_id,
        "last_agent_role": agent_role,
        "last_commit_sha": commit_sha,
        "sprint_id": sprint_id,
        "note": note,
        "agent_sessions_this_sprint": sessions,
        "factory_halted": bool(load_factory_state().get("halted")),
    }
    save_json(SNAPSHOT_PATH, snapshot)
    return SNAPSHOT_PATH
