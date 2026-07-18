#!/usr/bin/env python3
"""Agent session telemetry — append-only JSONL logging for AI factory efficiency studies.

Authority: docs/qa/AGENT_SESSION_TELEMETRY.md
Schema: game/data/qa/agent_session_telemetry_schema.json
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "game/data/qa/agent_session_telemetry_schema.json"
TELEMETRY_DIR = ROOT / "artifacts/agent_session_telemetry"
EVENTS_PATH = TELEMETRY_DIR / "events.jsonl"
ACTIVE_PATH = TELEMETRY_DIR / "active_sessions.json"
SCHEMA_VERSION = "1.0"

ROLE_CATEGORIES: dict[str, str] = {
    "pm": "pm_orchestration",
    "architect": "spec_architecture",
    "builder": "scene_build",
    "qa": "qa_verification",
    "flow": "flow_integration",
    "visual": "visual_jury",
    "release": "release_cd",
    "debugger": "remediation",
}


def _utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_ts(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def load_schema() -> dict[str, Any]:
    if SCHEMA_PATH.is_file():
        return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    return {}


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_event(event: dict[str, Any]) -> Path:
    """Append one telemetry event to the primary JSONL log."""
    TELEMETRY_DIR.mkdir(parents=True, exist_ok=True)
    event.setdefault("schema_version", SCHEMA_VERSION)
    event.setdefault("ts", _utcnow())
    with EVENTS_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event, ensure_ascii=False) + "\n")
    return EVENTS_PATH


def load_active_sessions() -> dict[str, Any]:
    return load_json(ACTIVE_PATH)


def save_active_sessions(data: dict[str, Any]) -> None:
    save_json(ACTIVE_PATH, data)


def _session_key(agent_role: str, issue_id: str | None) -> str:
    return f"{agent_role}:{issue_id or '_pm_'}"


def _git_short_sha() -> str | None:
    try:
        return (
            subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True)
            .strip()
        )
    except subprocess.CalledProcessError:
        return None


def _git_branch() -> str | None:
    try:
        return (
            subprocess.check_output(
                ["bash", str(ROOT / "tools/git_branch_name.sh")], cwd=ROOT, text=True
            )
            .strip()
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            return (
                subprocess.check_output(
                    ["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=ROOT, text=True
                )
                .strip()
            )
        except subprocess.CalledProcessError:
            return None


def _git_diff_stats(base_sha: str | None) -> dict[str, int | None]:
    stats = {"files_changed": None, "lines_added": None, "lines_removed": None}
    if not base_sha:
        return stats
    try:
        out = subprocess.check_output(
            ["git", "diff", "--shortstat", base_sha, "HEAD"], cwd=ROOT, text=True
        ).strip()
        if not out:
            return stats
        fm = re.search(r"(\d+) files? changed", out)
        im = re.search(r"(\d+) insertions?\(\+\)", out)
        dm = re.search(r"(\d+) deletions?\(-\)", out)
        if fm:
            stats["files_changed"] = int(fm.group(1))
        if im:
            stats["lines_added"] = int(im.group(1))
        if dm:
            stats["lines_removed"] = int(dm.group(1))
    except subprocess.CalledProcessError:
        pass
    return stats


def _pr_info() -> dict[str, Any]:
    info: dict[str, Any] = {"pr_url": None, "pr_number": None}
    if not shutil_which("gh"):
        return info
    try:
        out = subprocess.check_output(
            ["gh", "pr", "view", "--json", "url,number"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        )
        data = json.loads(out)
        info["pr_url"] = data.get("url")
        info["pr_number"] = data.get("number")
    except (subprocess.CalledProcessError, json.JSONDecodeError, FileNotFoundError):
        pass
    return info


def shutil_which(cmd: str) -> str | None:
    from shutil import which

    return which(cmd)


def collect_cursor_metadata() -> dict[str, Any]:
    """Best-effort Cursor Cloud / agent metadata from env and known injection points."""
    meta: dict[str, Any] = {}
    env_map = {
        "cursor_bc_id": [
            "CURSOR_AGENT_BC_ID",
            "CURSOR_CLOUD_AGENT_BC_ID",
            "CURSOR_BC_ID",
        ],
        "cursor_agent_url": ["CURSOR_AGENT_URL", "CURSOR_CLOUD_AGENT_URL"],
        "model_name": [
            "CURSOR_AGENT_MODEL",
            "CURSOR_MODEL",
            "ORIGINAL_MODEL_NAME",
        ],
        "cloud_environment": ["CURSOR_CLOUD_ENVIRONMENT", "CURSOR_ENVIRONMENT_NAME"],
        "cloud_snapshot_id": ["CURSOR_SNAPSHOT_ID", "CURSOR_CLOUD_SNAPSHOT_ID"],
    }
    for field, keys in env_map.items():
        for key in keys:
            val = os.environ.get(key, "").strip()
            if val:
                meta[field] = val
                break

    if meta.get("cursor_bc_id") and not meta.get("cursor_agent_url"):
        meta["cursor_agent_url"] = f"https://cursor.com/agents/{meta['cursor_bc_id']}"

    if meta.get("model_name"):
        meta["model_provider"] = "cursor"

    # Optional agent-written enrichment file (agents can write at session end)
    enrich = ROOT / "artifacts/agent_session_telemetry/session_enrichment.json"
    if enrich.is_file():
        try:
            extra = json.loads(enrich.read_text(encoding="utf-8"))
            for k, v in extra.items():
                if v is not None and k not in meta:
                    meta[k] = v
        except json.JSONDecodeError:
            pass

    return meta


def load_issue_context(issue_id: str | None) -> dict[str, Any]:
    if not issue_id:
        return {}
    board_path = ROOT / "game/data/qa/sprint_board.json"
    if not board_path.is_file():
        return {}
    board = json.loads(board_path.read_text(encoding="utf-8"))
    issue = next((i for i in board.get("issues", []) if i.get("id") == issue_id), None)
    if not issue:
        return {}
    active = board.get("active_sprint", {})
    return {
        "issue": issue,
        "sprint_id": active.get("id"),
        "phase": issue.get("phase") or active.get("phase"),
        "sprint_branch": active.get("branch", "game/development"),
    }


def load_dispatch_context(issue_id: str | None, agent_role: str) -> dict[str, Any]:
    report_path = ROOT / "artifacts/pm_orchestrator_report.json"
    if not issue_id or not report_path.is_file():
        return {}
    report = json.loads(report_path.read_text(encoding="utf-8"))
    for d in report.get("next_dispatch", []):
        if d.get("issue_id") == issue_id and d.get("agent") == agent_role:
            return {"dispatch": d, "orchestrator_generated_at": report.get("generated_at")}
    return {}


def infer_task_category(
    agent_role: str,
    issue: dict[str, Any] | None = None,
) -> str:
    role = (agent_role or "").lower().replace("agent/", "")
    if role in ROLE_CATEGORIES:
        base = ROLE_CATEGORIES[role]
    else:
        base = "other"

    if not issue:
        return base

    blob = " ".join(
        [
            issue.get("title", ""),
            issue.get("id", ""),
            " ".join(issue.get("implementation_plan_tasks") or []),
            issue.get("generation_readiness_id") or "",
        ]
    ).lower()

    schema = load_schema()
    for cat in schema.get("task_categories", []):
        cid = cat.get("id")
        if not cid:
            continue
        keywords = cat.get("keywords") or []
        if any(kw.lower() in blob for kw in keywords):
            return cid
        roles = cat.get("agent_roles") or []
        if roles and role in roles and cid != "other":
            return cid

    if "bootstrap" in blob or issue.get("id") == "P1-00":
        return "bootstrap"
    if "remediation" in blob or issue.get("status") == "blocked":
        return "remediation"
    return base


def infer_task_tags(issue: dict[str, Any] | None) -> list[str]:
    if not issue:
        return []
    tags: list[str] = []
    for task in issue.get("implementation_plan_tasks") or []:
        tags.append(str(task))
    if issue.get("generation_readiness_id"):
        tags.append(issue["generation_readiness_id"])
    title = (issue.get("title") or "").lower()
    for kw in ("shader", "scene", "zone", "combat", "audio", "visual", "docs", "bootstrap", "gdai"):
        if kw in title and kw not in tags:
            tags.append(kw)
    return tags


def start_session(
    agent_role: str,
    issue_id: str | None = None,
    *,
    note: str | None = None,
) -> dict[str, Any]:
    """Open a new agent session and log session_start."""
    agent_role = agent_role.replace("agent/", "")
    session_id = str(uuid.uuid4())
    ctx = load_issue_context(issue_id)
    issue = ctx.get("issue") or {}
    dispatch_ctx = load_dispatch_context(issue_id, agent_role)
    dispatch = dispatch_ctx.get("dispatch") or {}
    cursor_meta = collect_cursor_metadata()
    branch_name = None
    if issue_id and issue.get("branch_name_pattern"):
        branch_name = issue["branch_name_pattern"].replace("{issue_id}", issue_id.lower())

    start_ts = _utcnow()
    commit_sha = _git_short_sha()
    event: dict[str, Any] = {
        "session_id": session_id,
        "event": "session_start",
        "ts": start_ts,
        "t": 0,
        "issue_id": issue_id,
        "agent_role": agent_role,
        "sprint_id": ctx.get("sprint_id") or dispatch.get("sprint_id"),
        "phase": ctx.get("phase"),
        "task_category": infer_task_category(agent_role, issue or None),
        "task_tags": infer_task_tags(issue or None),
        "acceptance_gate_ids": dispatch.get("acceptance_gate_ids")
        or issue.get("acceptance_gate_ids"),
        "done_requires": issue.get("done_requires") or dispatch.get("done_requires"),
        "branch_name": branch_name,
        "sprint_branch": ctx.get("sprint_branch"),
        "dispatch_action": dispatch.get("action"),
        "handoff_refs": issue.get("handoff_refs"),
        "github_issue": issue.get("github_issue"),
        "co_agent": issue.get("co_agent") or dispatch.get("co_agent"),
        "implementation_plan_tasks": issue.get("implementation_plan_tasks"),
        "generation_readiness_id": issue.get("generation_readiness_id"),
        "commit_sha_start": commit_sha,
        "git_branch": _git_branch(),
        "repo": os.environ.get("GITHUB_REPOSITORY", "vivivieri/3d-JRPG-adventure-pc-game"),
        "mcp_stack_required": ["godot-mcp", "godotiq", "godot-mcp-pro"]
        if agent_role == "builder"
        else None,
        "session_gate_command": f"bash tools/run_agent_session_gate.sh {agent_role} {issue_id}"
        if issue_id
        else None,
        "orchestrator_generated_at": dispatch_ctx.get("orchestrator_generated_at"),
        **cursor_meta,
    }
    if note:
        event["note"] = note

    append_event(event)

    active = load_active_sessions()
    key = _session_key(agent_role, issue_id)
    active[key] = {
        "session_id": session_id,
        "started_at": start_ts,
        "agent_role": agent_role,
        "issue_id": issue_id,
        "commit_sha_start": commit_sha,
        "heartbeat_count": 0,
        "task_category": event.get("task_category"),
        "task_tags": event.get("task_tags"),
        "model_name": event.get("model_name"),
        "cursor_bc_id": event.get("cursor_bc_id"),
    }
    save_active_sessions(active)
    return event


def _elapsed_seconds(started_at: str) -> float:
    start = _parse_ts(started_at)
    now = datetime.now(timezone.utc)
    return max(0.0, (now - start).total_seconds())


def progress_session(
    agent_role: str,
    issue_id: str | None = None,
    *,
    note: str | None = None,
    phase_marker: str | None = None,
) -> dict[str, Any] | None:
    """Log session_progress heartbeat; returns event or None if no active session."""
    agent_role = agent_role.replace("agent/", "")
    active = load_active_sessions()
    key = _session_key(agent_role, issue_id)
    sess = active.get(key)
    if not sess:
        return None

    sess["heartbeat_count"] = int(sess.get("heartbeat_count", 0)) + 1
    save_active_sessions(active)

    event: dict[str, Any] = {
        "session_id": sess["session_id"],
        "event": "session_progress",
        "ts": _utcnow(),
        "t": round(_elapsed_seconds(sess["started_at"]), 3),
        "issue_id": issue_id,
        "agent_role": agent_role,
        "heartbeat_seq": sess["heartbeat_count"],
    }
    if note:
        event["note"] = note
    if phase_marker:
        event["phase_marker"] = phase_marker

    append_event(event)
    return event


def end_session(
    agent_role: str,
    issue_id: str | None = None,
    *,
    outcome: str = "complete",
    failed_check: str | None = None,
    error_message: str | None = None,
    note: str | None = None,
    gates_passed: list[str] | None = None,
    gates_failed: list[str] | None = None,
    ci_pass_count: int | None = None,
    ci_fail_count: int | None = None,
    tokens_input: int | None = None,
    tokens_output: int | None = None,
    tokens_total: int | None = None,
    tokens_cache_read: int | None = None,
    tokens_cache_write: int | None = None,
    tokens_source: str | None = None,
    tool_calls_reported: int | None = None,
) -> dict[str, Any] | None:
    """Close an active session and log session_end or session_failed."""
    agent_role = agent_role.replace("agent/", "")
    active = load_active_sessions()
    key = _session_key(agent_role, issue_id)
    sess = active.pop(key, None)
    if not sess:
        # No active session — still log a terminal event for traceability
        session_id = str(uuid.uuid4())
        started_at = _utcnow()
        duration = 0.0
    else:
        session_id = sess["session_id"]
        started_at = sess["started_at"]
        duration = _elapsed_seconds(started_at)
        save_active_sessions(active)

    cursor_meta = collect_cursor_metadata()
    commit_end = _git_short_sha()
    diff = _git_diff_stats(sess.get("commit_sha_start") if sess else None)
    pr = _pr_info()
    ctx = load_issue_context(issue_id)
    issue = ctx.get("issue") or {}

    event_name = "session_failed" if outcome == "failed" else "session_end"
    event: dict[str, Any] = {
        "session_id": session_id,
        "event": event_name,
        "ts": _utcnow(),
        "t": round(duration, 3),
        "issue_id": issue_id,
        "agent_role": agent_role,
        "outcome": outcome,
        "duration_seconds": round(duration, 3),
        "commit_sha_start": sess.get("commit_sha_start") if sess else None,
        "commit_sha_end": commit_end,
        "task_category": (sess or {}).get("task_category")
        or infer_task_category(agent_role, issue or None),
        "task_tags": (sess or {}).get("task_tags") or infer_task_tags(issue or None),
        "heartbeat_count": (sess or {}).get("heartbeat_count", 0),
        "pr_url": pr.get("pr_url"),
        "pr_number": pr.get("pr_number"),
        **diff,
        **cursor_meta,
    }

    if sess and sess.get("model_name") and not event.get("model_name"):
        event["model_name"] = sess["model_name"]
    if sess and sess.get("cursor_bc_id") and not event.get("cursor_bc_id"):
        event["cursor_bc_id"] = sess["cursor_bc_id"]

    if gates_passed is not None:
        event["gates_passed"] = gates_passed
    if gates_failed is not None:
        event["gates_failed"] = gates_failed
    if ci_pass_count is not None:
        event["ci_pass_count"] = ci_pass_count
    if ci_fail_count is not None:
        event["ci_fail_count"] = ci_fail_count
    if failed_check:
        event["failed_check"] = failed_check
    if error_message:
        event["error_message"] = error_message
    if note:
        event["note"] = note

    # Token fields — env override for agent self-report at end
    token_env = {
        "tokens_input": ["AGENT_TOKENS_INPUT", "CURSOR_TOKENS_INPUT"],
        "tokens_output": ["AGENT_TOKENS_OUTPUT", "CURSOR_TOKENS_OUTPUT"],
        "tokens_total": ["AGENT_TOKENS_TOTAL", "CURSOR_TOKENS_TOTAL"],
        "tokens_cache_read": ["AGENT_TOKENS_CACHE_READ"],
        "tokens_cache_write": ["AGENT_TOKENS_CACHE_WRITE"],
    }
    for field, keys in token_env.items():
        val = locals().get(field)
        if val is None:
            for k in keys:
                raw = os.environ.get(k, "").strip()
                if raw.isdigit():
                    val = int(raw)
                    break
        if val is not None:
            event[field] = val

    if any(event.get(f) is not None for f in token_env):
        event["tokens_source"] = tokens_source or os.environ.get("AGENT_TOKENS_SOURCE", "agent_report")
    if tool_calls_reported is not None:
        event["tool_calls_reported"] = tool_calls_reported
    elif os.environ.get("AGENT_TOOL_CALLS", "").isdigit():
        event["tool_calls_reported"] = int(os.environ["AGENT_TOOL_CALLS"])

    append_event(event)
    _write_issue_evidence(session_id, event, sess)
    return event


def _write_issue_evidence(
    session_id: str,
    terminal_event: dict[str, Any],
    sess: dict[str, Any] | None,
) -> None:
    """Per-issue session rollup for sprint evidence bundles."""
    issue_id = terminal_event.get("issue_id")
    if not issue_id:
        return
    evidence_dir = ROOT / "artifacts/sprint_evidence" / issue_id
    evidence_dir.mkdir(parents=True, exist_ok=True)

    # Collect all events for this session from log
    events: list[dict[str, Any]] = []
    if EVENTS_PATH.is_file():
        for line in EVENTS_PATH.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if row.get("session_id") == session_id:
                events.append(row)

    rollup = {
        "session_id": session_id,
        "issue_id": issue_id,
        "agent_role": terminal_event.get("agent_role"),
        "outcome": terminal_event.get("outcome"),
        "started_at": (sess or {}).get("started_at"),
        "ended_at": terminal_event.get("ts"),
        "duration_seconds": terminal_event.get("duration_seconds"),
        "task_category": terminal_event.get("task_category"),
        "task_tags": terminal_event.get("task_tags"),
        "model_name": terminal_event.get("model_name"),
        "cursor_bc_id": terminal_event.get("cursor_bc_id"),
        "tokens_total": terminal_event.get("tokens_total"),
        "tokens_input": terminal_event.get("tokens_input"),
        "tokens_output": terminal_event.get("tokens_output"),
        "pr_url": terminal_event.get("pr_url"),
        "gates_passed": terminal_event.get("gates_passed"),
        "gates_failed": terminal_event.get("gates_failed"),
        "events": events,
    }
    out = evidence_dir / f"session_{session_id}.json"
    out.write_text(json.dumps(rollup, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_events(path: Path | None = None) -> list[dict[str, Any]]:
    log = path or EVENTS_PATH
    if not log.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for line in log.read_text(encoding="utf-8").splitlines():
        if line.strip():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows
