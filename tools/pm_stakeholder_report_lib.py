#!/usr/bin/env python3
"""Build stakeholder status reports + optional Telegram delivery.

Authority: docs/PM_STAKEHOLDER_REPORTING.md
"""
from __future__ import annotations

import html
import json
import os
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "game/data/qa/stakeholder_report_config.json"
BOARD_PATH = ROOT / "game/data/qa/sprint_board.json"
PHASES_PATH = ROOT / "game/data/qa/sprint_phases.json"
ORCH_PATH = ROOT / "artifacts/pm_orchestrator_report.json"
DISPATCH_PATH = ROOT / "artifacts/pm_dispatch_packet.json"
HEALTH_SNAPSHOT_PATH = ROOT / "game/data/qa/factory_health_snapshot.json"
HEALTH_REPORT_PATH = ROOT / "artifacts/factory_health_report.json"

sys_path = str(ROOT / "tools")
import sys

if sys_path not in sys.path:
    sys.path.insert(0, sys_path)


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_config() -> dict[str, Any]:
    return load_json(CONFIG_PATH)


def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def sprint_progress(board: dict[str, Any]) -> dict[str, Any]:
    issues = board.get("issues", [])
    total = len(issues)
    by_status: dict[str, int] = {}
    for i in issues:
        st = i.get("status", "?")
        by_status[st] = by_status.get(st, 0) + 1
    done = by_status.get("done", 0)
    pct = round(100.0 * done / total, 1) if total else 0.0
    return {
        "total": total,
        "done": done,
        "in_progress": by_status.get("in_progress", 0),
        "pending": by_status.get("pending", 0),
        "blocked": by_status.get("blocked", 0),
        "carry_over": by_status.get("carry_over", 0),
        "percent_complete": pct,
        "issues_summary": [
            {
                "id": i["id"],
                "status": i.get("status"),
                "title": i.get("title"),
                "agent": i.get("agent_owner"),
            }
            for i in sorted(issues, key=lambda x: x.get("sequence", 999))
        ],
    }


def phase_context(phases: dict[str, Any], board: dict[str, Any]) -> dict[str, Any]:
    active = board.get("active_sprint", {})
    phase_num = active.get("phase")
    row = next((p for p in phases.get("phases", []) if p.get("phase") == phase_num), {})
    return {
        "phase": phase_num,
        "name": row.get("name"),
        "status": row.get("status"),
        "exit_gates_required": active.get("phase_exit_gate_ids") or row.get("exit_gates_required", []),
        "exit_gates_conditional": row.get("exit_gates_conditional", []),
        "milestone": row.get("milestone"),
    }


def build_report(
    *,
    trigger: str,
    issue_id: str | None = None,
    agent_role: str | None = None,
    commit_sha: str | None = None,
    note: str | None = None,
    event_payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    config = load_config()
    board = load_json(BOARD_PATH)
    phases = load_json(PHASES_PATH)
    orch = load_json(ORCH_PATH)
    dispatch_pkt = load_json(DISPATCH_PATH)
    snapshot = load_json(HEALTH_SNAPSHOT_PATH)
    health = load_json(HEALTH_REPORT_PATH)

    trigger_cfg = config.get("triggers", {}).get(trigger, {})
    report_kind = trigger_cfg.get("report_kind", trigger)
    active = board.get("active_sprint", {})
    progress = sprint_progress(board)
    phase = phase_context(phases, board)

    sprint_complete = progress["done"] == progress["total"] and progress["total"] > 0
    if trigger == "sprint_cycle_complete" or (sprint_complete and trigger == "agent_cycle_complete"):
        report_kind = "sprint_cycle" if trigger == "sprint_cycle_complete" else report_kind

    phase_exit = sprint_complete and progress["done"] == progress["total"]
    if trigger == "phase_exit" or (phase_exit and report_kind == "sprint_cycle"):
        report_kind = "phase_exit" if trigger == "phase_exit" else report_kind

    blockers = []
    for i in board.get("issues", []):
        if i.get("status") in ("blocked", "in_progress") and i.get("escalation_level", 0) > 0:
            blockers.append({"id": i["id"], "level": i.get("escalation_level"), "title": i.get("title")})
    if orch.get("stale_issues"):
        blockers.extend({"id": s["id"], "level": "stale", "title": s.get("reason")} for s in orch["stale_issues"])

    report = {
        "version": "1.0",
        "generated_at": _utcnow(),
        "trigger": trigger,
        "report_kind": report_kind,
        "product_owner": config.get("product_owner", {}),
        "repo": config.get("repo_links", {}),
        "sprint": {
            "id": active.get("id"),
            "phase": active.get("phase"),
            "sprint_number": active.get("sprint_number"),
            "branch": active.get("branch"),
        },
        "phase": phase,
        "progress": progress,
        "cycle": {
            "issue_id": issue_id,
            "agent_role": agent_role,
            "commit_sha": commit_sha,
            "note": note,
            "event": event_payload,
        },
        "orchestrator": {
            "pass": orch.get("orchestrator_pass"),
            "sprint_complete": orch.get("sprint_complete"),
            "next_dispatch": orch.get("next_dispatch", []),
            "blocked_issues": orch.get("blocked_issues", []),
            "session_budget_exceeded": orch.get("session_budget_exceeded"),
            "session_budget_message": orch.get("session_budget_message"),
            "phase_exit": orch.get("phase_exit"),
        },
        "dispatch_packet_head": (dispatch_pkt.get("dispatch") or [None])[0],
        "factory": {
            "snapshot": snapshot,
            "health_status": health.get("status"),
            "health_findings": health.get("findings", []),
            "halted": snapshot.get("factory_halted"),
            "agent_sessions_this_sprint": snapshot.get("agent_sessions_this_sprint", 0),
        },
        "blockers": blockers,
        "headline": _headline(report_kind, progress, issue_id, agent_role, note),
    }
    return report


def _headline(
    kind: str,
    progress: dict[str, Any],
    issue_id: str | None,
    agent: str | None,
    note: str | None,
) -> str:
    pct = progress.get("percent_complete", 0)
    if kind == "micro_cycle_failure":
        return f"Cycle FAIL — {issue_id or '?'} ({note or 'see report'})"
    if kind == "uat_ready":
        return "UAT ready — human playtest required (L6)"
    if kind == "phase_exit":
        return f"Phase exit review — sprint {pct}% complete"
    if kind == "sprint_cycle":
        return f"Sprint cycle complete — {progress.get('done')}/{progress.get('total')} issues done"
    if kind == "factory_alert":
        return f"Factory alert — {note or 'watchdog/MCP'}"
    if issue_id:
        return f"Cycle complete — {issue_id} by {agent or 'agent'} · sprint {pct}%"
    return f"PM status — sprint {pct}% ({progress.get('done')}/{progress.get('total')})"


def report_to_markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# Tides of Urashima — Stakeholder Report",
        "",
        f"**{report.get('headline')}**",
        f"Generated: {report.get('generated_at')}",
        f"Kind: `{report.get('report_kind')}` · Trigger: `{report.get('trigger')}`",
        "",
        "## Sprint",
        f"- **{report['sprint'].get('id')}** (phase {report['sprint'].get('phase')})",
        f"- Progress: **{report['progress']['done']}/{report['progress']['total']}** "
        f"({report['progress']['percent_complete']}%)",
        f"- In progress: {report['progress']['in_progress']} · Pending: {report['progress']['pending']}",
        "",
        "## Phase",
        f"- {report['phase'].get('name')}",
        f"- Exit gates (required): {', '.join(report['phase'].get('exit_gates_required') or []) or '—'}",
        "",
    ]

    cycle = report.get("cycle", {})
    if cycle.get("issue_id"):
        lines.extend(
            [
                "## Last cycle",
                f"- Issue: **{cycle['issue_id']}** · Agent: `{cycle.get('agent_role')}`",
                f"- Commit: `{cycle.get('commit_sha') or '—'}`",
                "",
            ]
        )

    nd = report.get("orchestrator", {}).get("next_dispatch") or []
    if nd:
        lines.append("## Next dispatch")
        for d in nd[:3]:
            lines.append(f"- **{d.get('issue_id')}** → `{d.get('agent')}` ({d.get('action')})")
        lines.append("")

    if report.get("blockers"):
        lines.append("## Blockers / alerts")
        for b in report["blockers"][:5]:
            lines.append(f"- {b.get('id')}: {b.get('title')} (level {b.get('level')})")
        lines.append("")

    fac = report.get("factory", {})
    lines.extend(
        [
            "## Factory health",
            f"- Status: `{fac.get('health_status') or 'unknown'}` · Halted: `{fac.get('halted')}`",
            f"- Agent sessions this sprint: {fac.get('agent_sessions_this_sprint', 0)}",
            "",
            "## Links",
            f"- Repo: {report.get('repo', {}).get('github', '')}",
            f"- Actions: {report.get('repo', {}).get('actions', '')}",
        ]
    )
    return "\n".join(lines) + "\n"


def report_to_telegram_html(report: dict[str, Any]) -> str:
    """Compact HTML message for Telegram (parse_mode=HTML)."""
    esc = html.escape

    def b(s: str) -> str:
        return f"<b>{esc(s)}</b>"

    lines = [
        f"🎮 {b('Tides of Urashima')}",
        esc(report.get("headline", "Status update")),
        "",
        f"{b('Sprint')}: {esc(str(report['sprint'].get('id', '')))} "
        f"({report['progress']['done']}/{report['progress']['total']} · "
        f"{report['progress']['percent_complete']}%)",
        f"{b('Phase')}: {esc(str(report['phase'].get('name', '')))}",
    ]

    cycle = report.get("cycle", {})
    if cycle.get("issue_id"):
        lines.append(
            f"{b('Cycle')}: {esc(cycle['issue_id'])} · {esc(str(cycle.get('agent_role') or ''))}"
        )
        if cycle.get("commit_sha"):
            sha = str(cycle["commit_sha"])[:8]
            lines.append(f"Commit: <code>{esc(sha)}</code>")

    nd = report.get("orchestrator", {}).get("next_dispatch") or []
    if nd:
        nxt = nd[0]
        lines.append(
            f"{b('Next')}: {esc(nxt.get('issue_id', ''))} → {esc(nxt.get('agent', ''))}"
        )

    if report.get("blockers"):
        lines.append(f"⚠️ {b('Blockers')}: {len(report['blockers'])}")

    fac = report.get("factory", {})
    if fac.get("halted"):
        lines.append(f"🛑 {b('Factory HALTED')}")
    elif fac.get("health_status") not in (None, "healthy", "idle_ok"):
        lines.append(f"⚠️ Factory: {esc(str(fac.get('health_status')))}")

    gh = report.get("repo", {}).get("github", "")
    if gh:
        lines.append(f'<a href="{esc(gh)}">GitHub</a>')

    return "\n".join(lines)


def write_outputs(report: dict[str, Any], config: dict[str, Any]) -> dict[str, str]:
    outputs = config.get("outputs", {})
    out_dir = ROOT / outputs.get("json_dir", "artifacts/stakeholder_reports")
    out_dir.mkdir(parents=True, exist_ok=True)

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    stamp_path = out_dir / f"{ts}_{report.get('report_kind', 'report')}.json"
    save_json(stamp_path, report)

    latest_json = ROOT / outputs.get("latest_json", "artifacts/stakeholder_reports/latest.json")
    latest_md = ROOT / outputs.get("latest_markdown", "artifacts/stakeholder_reports/latest.md")
    latest_html = ROOT / outputs.get("latest_html", "artifacts/stakeholder_dashboard.html")

    save_json(latest_json, report)
    latest_md.write_text(report_to_markdown(report), encoding="utf-8")
    latest_html.write_text(render_html_dashboard(report), encoding="utf-8")

    # Trim history
    keep = int(outputs.get("history_keep", 50))
    history = sorted(out_dir.glob("*.json"))
    history = [p for p in history if p.name != "latest.json"]
    for old in history[:-keep]:
        old.unlink(missing_ok=True)

    return {
        "json": str(latest_json.relative_to(ROOT)),
        "markdown": str(latest_md.relative_to(ROOT)),
        "html": str(latest_html.relative_to(ROOT)),
        "stamped": str(stamp_path.relative_to(ROOT)),
    }


def render_html_dashboard(report: dict[str, Any]) -> str:
    """Single-file HTML dashboard for product owner."""
    data = json.dumps(report, ensure_ascii=False)
    headline = html.escape(report.get("headline", "Status"))
    pct = report.get("progress", {}).get("percent_complete", 0)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Tides of Urashima — Stakeholder Dashboard</title>
  <style>
    :root {{ font-family: system-ui, sans-serif; background: #1a1f2e; color: #e8ecf0; }}
    body {{ max-width: 960px; margin: 0 auto; padding: 1.5rem; }}
    h1 {{ font-size: 1.25rem; color: #b8c8d8; }}
    .headline {{ font-size: 1.1rem; margin: 1rem 0; }}
    .bar {{ background: #2a3344; border-radius: 6px; height: 12px; overflow: hidden; }}
    .bar > div {{ background: #4ae8d8; height: 100%; width: {pct}%; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 1rem 0; }}
    .card {{ background: #242b3a; padding: 1rem; border-radius: 8px; border: 1px solid #3a4556; }}
    .card h2 {{ margin: 0 0 0.5rem; font-size: 0.85rem; color: #8b9daf; text-transform: uppercase; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; }}
    td, th {{ padding: 0.35rem 0.5rem; text-align: left; border-bottom: 1px solid #3a4556; }}
    .status-done {{ color: #7dcea0; }}
    .status-in_progress {{ color: #d4a880; }}
    .status-pending {{ color: #8b9daf; }}
    .status-blocked {{ color: #e88; }}
    pre {{ background: #12161f; padding: 1rem; overflow: auto; font-size: 0.75rem; border-radius: 6px; }}
  </style>
</head>
<body>
  <h1>Tides of Urashima — Stakeholder Dashboard</h1>
  <p class="headline">{headline}</p>
  <p><small>Updated {html.escape(report.get("generated_at", ""))} · {html.escape(report.get("report_kind", ""))}</small></p>
  <div class="bar"><div></div></div>
  <p>{report.get("progress", {}).get("done", 0)}/{report.get("progress", {}).get("total", 0)} issues ({pct}%)</p>
  <div class="grid">
    <div class="card"><h2>Sprint</h2><p>{html.escape(str(report.get("sprint", {}).get("id", "")))}</p></div>
    <div class="card"><h2>Phase</h2><p>{html.escape(str(report.get("phase", {}).get("name", "")))}</p></div>
    <div class="card"><h2>Factory</h2><p>{html.escape(str(report.get("factory", {}).get("health_status") or "—"))}</p></div>
    <div class="card"><h2>Sessions</h2><p>{report.get("factory", {}).get("agent_sessions_this_sprint", 0)}</p></div>
  </div>
  <h2>Issues</h2>
  <table>
    <tr><th>ID</th><th>Status</th><th>Agent</th><th>Title</th></tr>
    {"".join(_issue_row(i) for i in report.get("progress", {}).get("issues_summary", []))}
  </table>
  <h2>Raw JSON</h2>
  <pre id="data"></pre>
  <script>
    const report = {data};
    document.getElementById("data").textContent = JSON.stringify(report, null, 2);
  </script>
</body>
</html>
"""


def _issue_row(issue: dict[str, Any]) -> str:
    st = issue.get("status", "")
    cls = f"status-{st}" if st else ""
    return (
        f"<tr><td>{html.escape(issue.get('id', ''))}</td>"
        f"<td class='{cls}'>{html.escape(st)}</td>"
        f"<td>{html.escape(str(issue.get('agent', '')))}</td>"
        f"<td>{html.escape(issue.get('title', ''))}</td></tr>"
    )


def send_telegram(message: str, config: dict[str, Any]) -> tuple[bool, str]:
    tg = config.get("telegram", {})
    if not tg.get("enabled", True):
        return False, "telegram disabled in config"

    token = os.environ.get(tg.get("secret_bot_token", "TELEGRAM_BOT_TOKEN"), "")
    chat_id = os.environ.get(tg.get("secret_chat_id", "TELEGRAM_CHAT_ID"), "")
    if not token or not chat_id:
        return False, "TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set"

    max_len = int(tg.get("max_message_chars", 4000))
    if len(message) > max_len:
        message = message[: max_len - 20] + "\n…(truncated)"

    parse_mode = tg.get("parse_mode", "HTML")
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": parse_mode,
        "disable_web_page_preview": tg.get("disable_web_page_preview", True),
    }
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        if body.get("ok"):
            return True, f"telegram message_id={body.get('result', {}).get('message_id')}"
        return False, json.dumps(body)
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        return False, f"HTTP {e.code}: {err}"
    except Exception as exc:
        return False, str(exc)


def emit_report(
    *,
    trigger: str,
    issue_id: str | None = None,
    agent_role: str | None = None,
    commit_sha: str | None = None,
    note: str | None = None,
    event_payload: dict[str, Any] | None = None,
    send_telegram_flag: bool | None = None,
) -> dict[str, Any]:
    config = load_config()
    report = build_report(
        trigger=trigger,
        issue_id=issue_id,
        agent_role=agent_role,
        commit_sha=commit_sha,
        note=note,
        event_payload=event_payload,
    )
    paths = write_outputs(report, config)

    tg_cfg = config.get("triggers", {}).get(trigger, {})
    should_send = send_telegram_flag
    if should_send is None:
        should_send = bool(tg_cfg.get("send_telegram", False))

    telegram_result = {"sent": False, "detail": "skipped"}
    if should_send:
        msg = report_to_telegram_html(report)
        ok, detail = send_telegram(msg, config)
        telegram_result = {"sent": ok, "detail": detail}

    return {
        "report": report,
        "paths": paths,
        "telegram": telegram_result,
    }
