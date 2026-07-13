#!/usr/bin/env python3
"""Factory health watchdog — stall/hang detection and recovery hints.

Authority: docs/FACTORY_WATCHDOG.md
Normal PM flow stays event-driven; this module handles exceptions only.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "game/data/qa/factory_watchdog.json"
BOARD_PATH = ROOT / "game/data/qa/sprint_board.json"
STATE_PATH = ROOT / "artifacts/factory_state.json"
HEARTBEAT_PATH = ROOT / "artifacts/factory_heartbeat.json"
CYCLE_LOG_PATH = ROOT / "artifacts/factory_cycle_log.jsonl"
ORCH_REPORT_PATH = ROOT / "artifacts/pm_orchestrator_report.json"
HEALTH_REPORT_PATH = ROOT / "artifacts/factory_health_report.json"


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _parse_ts(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except ValueError:
        return None


def _hours_since(dt: datetime | None, now: datetime | None = None) -> float | None:
    if dt is None:
        return None
    now = now or _utcnow()
    return (now - dt).total_seconds() / 3600.0


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_config() -> dict[str, Any]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def load_factory_state() -> dict[str, Any]:
    state = load_json(STATE_PATH)
    if not state:
        state = {
            "halted": False,
            "halt_reason": None,
            "halt_at": None,
            "recovery_attempts": {},
            "sprint_recovery_count": 0,
            "last_recovery_at": None,
            "last_orchestrator_result": None,
            "last_orchestrator_at": None,
        }
    return state


def save_factory_state(state: dict[str, Any]) -> None:
    save_json(STATE_PATH, state)


def append_cycle_log(entry: dict[str, Any]) -> None:
    CYCLE_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CYCLE_LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")


def last_cycle_event() -> dict[str, Any] | None:
    snapshot_path = ROOT / "game/data/qa/factory_health_snapshot.json"
    if snapshot_path.is_file():
        snap = load_json(snapshot_path)
        if snap.get("last_event"):
            return {
                "event": snap.get("last_event"),
                "timestamp": snap.get("updated_at"),
                "issue_id": snap.get("last_issue_id"),
                "agent_role": snap.get("last_agent_role"),
                "commit_sha": snap.get("last_commit_sha"),
                "sprint_id": snap.get("sprint_id"),
                "source": "factory_health_snapshot.json",
            }
    if not CYCLE_LOG_PATH.is_file():
        event_file = ROOT / "artifacts/agent_cycle_event.json"
        if event_file.is_file():
            return load_json(event_file)
        return None
    lines = [ln.strip() for ln in CYCLE_LOG_PATH.read_text(encoding="utf-8").splitlines() if ln.strip()]
    if not lines:
        return None
    try:
        return json.loads(lines[-1])
    except json.JSONDecodeError:
        return None


def sprint_incomplete(board: dict[str, Any]) -> bool:
    for issue in board.get("issues", []):
        if issue.get("status") not in ("done", "carry_over"):
            return True
    return False


def active_in_progress(board: dict[str, Any]) -> list[dict[str, Any]]:
    return [i for i in board.get("issues", []) if i.get("status") == "in_progress"]


def recovery_count_for_issue(state: dict[str, Any], issue_id: str) -> int:
    return int(state.get("recovery_attempts", {}).get(issue_id, 0))


def can_recover(
    config: dict[str, Any],
    state: dict[str, Any],
    issue_id: str | None,
    sprint_id: str | None,
) -> tuple[bool, str]:
    if state.get("halted"):
        return False, f"factory halted: {state.get('halt_reason') or 'no reason'}"

    thresholds = config.get("thresholds", {})
    cooldown_h = thresholds.get("recovery_cooldown_hours", 2)
    last_recovery = _parse_ts(state.get("last_recovery_at"))
    since = _hours_since(last_recovery)
    if since is not None and since < cooldown_h:
        return False, f"recovery cooldown ({since:.1f}h < {cooldown_h}h)"

    if issue_id:
        max_issue = thresholds.get("max_recovery_attempts_per_issue", 3)
        count = recovery_count_for_issue(state, issue_id)
        if count >= max_issue:
            return False, f"max recovery attempts for {issue_id} ({count} >= {max_issue})"

    max_sprint = thresholds.get("max_recovery_attempts_per_sprint", 12)
    sprint_count = int(state.get("sprint_recovery_count", 0))
    if sprint_count >= max_sprint:
        return False, f"max sprint recovery attempts ({sprint_count} >= {max_sprint})"

    return True, "ok"


def record_recovery(state: dict[str, Any], issue_id: str | None, reason: str) -> dict[str, Any]:
    now = _utcnow().isoformat()
    state["last_recovery_at"] = now
    state["sprint_recovery_count"] = int(state.get("sprint_recovery_count", 0)) + 1
    if issue_id:
        attempts = state.setdefault("recovery_attempts", {})
        attempts[issue_id] = int(attempts.get(issue_id, 0)) + 1
    state.setdefault("recovery_log", []).append(
        {"at": now, "issue_id": issue_id, "reason": reason}
    )
    save_factory_state(state)
    return state


def set_halt(state: dict[str, Any], reason: str) -> dict[str, Any]:
    now = _utcnow().isoformat()
    state["halted"] = True
    state["halt_reason"] = reason
    state["halt_at"] = now
    save_factory_state(state)
    return state


def clear_halt(state: dict[str, Any]) -> dict[str, Any]:
    state["halted"] = False
    state["halt_reason"] = None
    state["halt_at"] = None
    save_factory_state(state)
    return state


def analyze_health() -> dict[str, Any]:
    config = load_config()
    thresholds = config.get("thresholds", {})
    board = load_json(BOARD_PATH) if BOARD_PATH.is_file() else {"issues": [], "active_sprint": {}}
    state = load_factory_state()
    heartbeat = load_json(HEARTBEAT_PATH)
    orch_report = load_json(ORCH_REPORT_PATH)
    last_event = last_cycle_event()
    now = _utcnow()

    active_sprint = board.get("active_sprint", {})
    sprint_id = active_sprint.get("id")
    incomplete = sprint_incomplete(board)
    in_progress = active_in_progress(board)

    stall_h = thresholds.get("stall_hours_idle", 4)
    stale_h = thresholds.get("stale_hours_in_progress", 24)
    heartbeat_h = thresholds.get("heartbeat_stale_hours", 6)

    last_event_ts = _parse_ts(last_event.get("timestamp") if last_event else None)
    last_event_idle_h = _hours_since(last_event_ts, now)

    findings: list[dict[str, Any]] = []
    status = "healthy"
    recommended_action: str | None = None
    recovery_issue_id: str | None = None

    if state.get("halted"):
        status = "halted"
        findings.append(
            {
                "code": "factory_halt",
                "severity": "critical",
                "message": state.get("halt_reason") or "Factory halted by operator",
                "halt_at": state.get("halt_at"),
            }
        )
        recommended_action = "human_notify"

    # Stale in-progress agents
    stale_issues: list[dict[str, Any]] = []
    for issue in in_progress:
        last_sess = _parse_ts(issue.get("last_agent_session"))
        idle = _hours_since(last_sess, now)
        if idle is not None and idle >= stale_h:
            stale_issues.append(
                {
                    "issue_id": issue["id"],
                    "agent": issue.get("agent_owner"),
                    "idle_hours": round(idle, 2),
                    "threshold_hours": stale_h,
                }
            )
        elif last_sess is None:
            stale_issues.append(
                {
                    "issue_id": issue["id"],
                    "agent": issue.get("agent_owner"),
                    "idle_hours": None,
                    "threshold_hours": stale_h,
                    "reason": "in_progress without last_agent_session",
                }
            )

    if stale_issues:
        findings.append(
            {
                "code": "stale_agent",
                "severity": "high",
                "issues": stale_issues,
            }
        )
        if status == "healthy":
            status = "stale_agent"
        recovery_issue_id = stale_issues[0]["issue_id"]
        recommended_action = recommended_action or "escalate_and_recover"

    # Heartbeat gap for active work
    hb_ts = _parse_ts(heartbeat.get("timestamp"))
    hb_idle = _hours_since(hb_ts, now)
    hb_issue = heartbeat.get("issue_id")
    hb_phase = heartbeat.get("phase")
    if incomplete and in_progress and hb_idle is not None and hb_idle >= heartbeat_h:
        if hb_phase in ("start", "progress", None):
            findings.append(
                {
                    "code": "no_heartbeat",
                    "severity": "high",
                    "issue_id": hb_issue,
                    "last_heartbeat_hours": round(hb_idle, 2),
                    "threshold_hours": heartbeat_h,
                    "agent": heartbeat.get("agent_role"),
                }
            )
            if status == "healthy":
                status = "no_heartbeat"
            recovery_issue_id = recovery_issue_id or hb_issue or (
                in_progress[0]["id"] if in_progress else None
            )
            recommended_action = recommended_action or "watchdog_recovery"

    # Factory stall — no recent cycle event but work remains
    if incomplete and not state.get("halted"):
        if last_event_idle_h is None or last_event_idle_h >= stall_h:
            # Sprint complete on board but incomplete issues shouldn't happen; still check
            findings.append(
                {
                    "code": "stalled",
                    "severity": "high",
                    "idle_hours_since_last_cycle": round(last_event_idle_h or 9999, 2),
                    "threshold_hours": stall_h,
                    "last_event": last_event.get("event") if last_event else None,
                    "incomplete_issues": [
                        i["id"]
                        for i in board.get("issues", [])
                        if i.get("status") not in ("done", "carry_over")
                    ],
                }
            )
            if status == "healthy":
                status = "stalled"
            if not recovery_issue_id:
                pending = [
                    i
                    for i in board.get("issues", [])
                    if i.get("status") in ("pending", "in_progress", "blocked")
                ]
                pending.sort(key=lambda x: x.get("sequence", 999))
                recovery_issue_id = pending[0]["id"] if pending else None
            recommended_action = recommended_action or "watchdog_recovery"

    # Orchestrator last result
    if state.get("last_orchestrator_result") == "fail":
        findings.append(
            {
                "code": "orchestrator_fail",
                "severity": "medium",
                "last_at": state.get("last_orchestrator_at"),
            }
        )
        if status == "healthy":
            status = "orchestrator_fail"
        recommended_action = recommended_action or "watchdog_recovery"

    if orch_report and orch_report.get("orchestrator_pass") is False:
        findings.append(
            {
                "code": "orchestrator_report_fail",
                "severity": "medium",
                "stale_issues": orch_report.get("stale_issues"),
                "wip_violations": orch_report.get("wip_violations"),
            }
        )

    if not incomplete and status == "healthy":
        status = "idle_ok"

    recover_ok, recover_reason = can_recover(config, state, recovery_issue_id, sprint_id)
    if recommended_action in ("watchdog_recovery", "escalate_and_recover") and not recover_ok:
        findings.append(
            {
                "code": "recovery_blocked",
                "severity": "critical",
                "reason": recover_reason,
            }
        )
        if "max recovery" in recover_reason or "max sprint" in recover_reason:
            status = "recovery_exhausted"
            recommended_action = "halt_and_human"

    report = {
        "generated_at": now.isoformat(),
        "status": status,
        "sprint_id": sprint_id,
        "incomplete": incomplete,
        "recommended_action": recommended_action,
        "recovery_issue_id": recovery_issue_id,
        "can_recover": recover_ok,
        "recover_block_reason": None if recover_ok else recover_reason,
        "findings": findings,
        "last_cycle_event": last_event,
        "last_cycle_idle_hours": round(last_event_idle_h, 2) if last_event_idle_h is not None else None,
        "heartbeat": heartbeat or None,
        "factory_halted": bool(state.get("halted")),
        "thresholds": thresholds,
    }
    return report


def write_health_report(report: dict[str, Any]) -> Path:
    save_json(HEALTH_REPORT_PATH, report)
    return HEALTH_REPORT_PATH
