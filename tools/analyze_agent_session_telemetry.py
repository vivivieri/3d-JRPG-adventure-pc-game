#!/usr/bin/env python3
"""Analyze agent session telemetry JSONL — efficiency study reports.

Reads artifacts/agent_session_telemetry/events.jsonl (or a path argument).
Exports JSON, CSV, and Markdown summaries grouped by role, task category, issue.

Usage:
  python3 tools/analyze_agent_session_telemetry.py
  python3 tools/analyze_agent_session_telemetry.py game/data/qa/examples/agent_session_telemetry_sample.jsonl
  python3 tools/analyze_agent_session_telemetry.py --json report.json --csv report.csv
  python3 tools/analyze_agent_session_telemetry.py --parquet out.parquet  # requires pandas+pyarrow

Authority: docs/qa/AGENT_SESSION_TELEMETRY.md
"""
from __future__ import annotations

import argparse
import csv
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "game/data/qa/agent_session_telemetry_schema.json"
DEFAULT_LOG = ROOT / "artifacts/agent_session_telemetry/events.jsonl"
DEFAULT_OUT = ROOT / "artifacts/agent_session_reports"


def load_events(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                print(f"WARN: skipping corrupt telemetry JSONL line: {exc}", file=sys.stderr)
                continue
    return rows


def build_sessions(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Collapse JSONL events into one record per session_id (terminal event wins)."""
    by_id: dict[str, dict[str, Any]] = {}
    progress_counts: dict[str, int] = defaultdict(int)
    backfills: dict[str, dict[str, Any]] = {}

    for ev in events:
        sid = ev.get("session_id")
        if not sid:
            continue
        et = ev.get("event")
        if et == "session_start":
            by_id.setdefault(sid, {}).update(ev)
            by_id[sid]["_started"] = ev
        elif et == "session_progress":
            progress_counts[sid] += 1
        elif et == "session_token_backfill":
            backfills[sid] = ev
        elif et in ("session_end", "session_failed"):
            by_id.setdefault(sid, {}).update(ev)
            by_id[sid]["_terminal"] = ev

    sessions: list[dict[str, Any]] = []
    for sid, rec in by_id.items():
        terminal = rec.get("_terminal") or rec
        start = rec.get("_started") or rec
        bf = backfills.get(sid) or {}
        sessions.append(
            {
                "session_id": sid,
                "issue_id": terminal.get("issue_id") or start.get("issue_id"),
                "agent_role": terminal.get("agent_role") or start.get("agent_role"),
                "sprint_id": terminal.get("sprint_id") or start.get("sprint_id"),
                "phase": terminal.get("phase") or start.get("phase"),
                "task_category": terminal.get("task_category") or start.get("task_category"),
                "task_tags": terminal.get("task_tags") or start.get("task_tags") or [],
                "model_name": terminal.get("model_name") or start.get("model_name"),
                "outcome": terminal.get("outcome") or ("unknown" if "_terminal" not in rec else "open"),
                "duration_seconds": terminal.get("duration_seconds"),
                "started_at": start.get("ts"),
                "ended_at": terminal.get("ts"),
                "tokens_total": bf.get("tokens_total") or terminal.get("tokens_total"),
                "tokens_input": bf.get("tokens_input") or terminal.get("tokens_input"),
                "tokens_output": bf.get("tokens_output") or terminal.get("tokens_output"),
                "tokens_source": bf.get("tokens_source") or terminal.get("tokens_source"),
                "pr_url": terminal.get("pr_url"),
                "pr_number": terminal.get("pr_number"),
                "files_changed": terminal.get("files_changed"),
                "lines_added": terminal.get("lines_added"),
                "lines_removed": terminal.get("lines_removed"),
                "gates_passed": terminal.get("gates_passed") or [],
                "gates_failed": terminal.get("gates_failed") or [],
                "failed_check": terminal.get("failed_check"),
                "heartbeat_count": terminal.get("heartbeat_count", progress_counts.get(sid, 0)),
                "cursor_bc_id": terminal.get("cursor_bc_id") or start.get("cursor_bc_id"),
                "token_backfilled": bool(bf),
            }
        )
    return sessions


def _median(vals: list[float]) -> float | None:
    return statistics.median(vals) if vals else None


def _sum(vals: list[float]) -> float:
    return sum(vals) if vals else 0.0


def rollup_group(sessions: list[dict[str, Any]], key_fn) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for s in sessions:
        groups[key_fn(s)].append(s)

    rows: list[dict[str, Any]] = []
    for key, items in sorted(groups.items()):
        durations = [float(x["duration_seconds"]) for x in items if x.get("duration_seconds") is not None]
        tokens = [float(x["tokens_total"]) for x in items if x.get("tokens_total") is not None]
        complete = sum(1 for x in items if x.get("outcome") == "complete")
        failed = sum(1 for x in items if x.get("outcome") == "failed")
        files = [float(x["files_changed"]) for x in items if x.get("files_changed") is not None]
        rows.append(
            {
                "group": key,
                "session_count": len(items),
                "complete_count": complete,
                "failed_count": failed,
                "complete_rate": round(complete / len(items), 3) if items else 0,
                "failed_rate": round(failed / len(items), 3) if items else 0,
                "total_duration_seconds": round(_sum(durations), 1),
                "median_duration_seconds": round(_median(durations), 1) if _median(durations) is not None else None,
                "tokens_total_sum": int(_sum(tokens)) if tokens else None,
                "tokens_total_median": int(_median(tokens)) if _median(tokens) is not None else None,
                "files_changed_median": int(_median(files)) if _median(files) is not None else None,
            }
        )
    return rows


def remediation_pairs(sessions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Issues with multiple sessions before complete — token efficiency signal."""
    by_issue: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for s in sessions:
        iid = s.get("issue_id")
        if iid:
            by_issue[iid].append(s)

    flags: list[dict[str, Any]] = []
    for iid, items in sorted(by_issue.items()):
        failed_before_pass = 0
        outcomes = [x.get("outcome") for x in sorted(items, key=lambda r: r.get("started_at") or "")]
        for o in outcomes:
            if o == "failed":
                failed_before_pass += 1
            elif o == "complete":
                break
        if failed_before_pass >= 1:
            flags.append(
                {
                    "issue_id": iid,
                    "session_count": len(items),
                    "failed_attempts_before_complete": failed_before_pass,
                    "total_tokens": sum(x.get("tokens_total") or 0 for x in items) or None,
                    "total_duration_seconds": sum(x.get("duration_seconds") or 0 for x in items),
                }
            )
    return flags


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Agent Session Telemetry Report",
        "",
        f"**Source:** `{report.get('source')}`",
        f"**Sessions:** {report.get('session_count', 0)}",
        "",
        "## By agent role",
        "",
        "| Role | Sessions | Complete % | Median duration (s) | Tokens median |",
        "|------|----------|------------|---------------------|---------------|",
    ]
    for row in report.get("by_agent_role", []):
        lines.append(
            f"| {row['group']} | {row['session_count']} | {row['complete_rate']*100:.0f}% | "
            f"{row.get('median_duration_seconds') or '—'} | {row.get('tokens_total_median') or '—'} |"
        )

    lines += [
        "",
        "## By task category",
        "",
        "| Category | Sessions | Failed | Median duration (s) | Tokens sum |",
        "|----------|----------|--------|---------------------|------------|",
    ]
    for row in report.get("by_task_category", []):
        lines.append(
            f"| {row['group']} | {row['session_count']} | {row['failed_count']} | "
            f"{row.get('median_duration_seconds') or '—'} | {row.get('tokens_total_sum') or '—'} |"
        )

    rem = report.get("remediation_flags", [])
    if rem:
        lines += ["", "## Remediation flags (failed before complete)", ""]
        for r in rem:
            lines.append(
                f"- **{r['issue_id']}** — {r['failed_attempts_before_complete']} failed attempt(s), "
                f"{r['session_count']} total sessions, "
                f"{r.get('total_duration_seconds', 0):.0f}s total"
            )

    lines += [
        "",
        "## Efficiency study notes",
        "",
        "- Compare `task_category` token medians to find expensive work types.",
        "- High `failed_rate` + retries → tighten dispatch packets or split issues.",
        "- Long `median_duration_seconds` without heartbeats → hang risk or missing progress logs.",
        "- Export CSV/Parquet for pandas/BI tools after ship.",
        "",
        "_Authority: docs/qa/AGENT_SESSION_TELEMETRY.md_",
    ]
    return "\n".join(lines) + "\n"


def write_csv(path: Path, sessions: list[dict[str, Any]]) -> None:
    if not sessions:
        path.write_text("", encoding="utf-8")
        return
    fields = sorted({k for s in sessions for k in s.keys()})
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for s in sessions:
            row = dict(s)
            for k, v in row.items():
                if isinstance(v, (list, dict)):
                    row[k] = json.dumps(v, ensure_ascii=False)
            w.writerow(row)


def write_parquet(path: Path, sessions: list[dict[str, Any]]) -> None:
    try:
        import pandas as pd  # type: ignore
    except ImportError as exc:
        raise SystemExit("Parquet export requires pandas (pip install pandas pyarrow)") from exc
    df = pd.json_normalize(sessions)
    df.to_parquet(path, index=False)


def main() -> int:
    ap = argparse.ArgumentParser(description="Analyze agent session telemetry JSONL")
    ap.add_argument("log", nargs="?", default=str(DEFAULT_LOG), help="JSONL log path")
    ap.add_argument("--json", dest="json_out", help="Write full JSON report")
    ap.add_argument("--csv", dest="csv_out", help="Write flat session CSV")
    ap.add_argument("--markdown", dest="md_out", help="Write Markdown summary")
    ap.add_argument("--parquet", dest="parquet_out", help="Write Parquet (needs pandas)")
    ap.add_argument(
        "--out-dir",
        default=str(DEFAULT_OUT),
        help="Default output directory when --json/--csv/--markdown omitted",
    )
    args = ap.parse_args()

    log_path = Path(args.log)
    events = load_events(log_path)
    sessions = build_sessions(events)

    report: dict[str, Any] = {
        "source": str(log_path),
        "session_count": len(sessions),
        "event_count": len(events),
        "sessions": sessions,
        "by_agent_role": rollup_group(sessions, lambda s: s.get("agent_role") or "unknown"),
        "by_task_category": rollup_group(sessions, lambda s: s.get("task_category") or "unknown"),
        "by_issue": rollup_group(sessions, lambda s: s.get("issue_id") or "none"),
        "by_model": rollup_group(sessions, lambda s: s.get("model_name") or "unknown"),
        "remediation_flags": remediation_pairs(sessions),
    }

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    json_path = Path(args.json_out) if args.json_out else out_dir / "latest.json"
    csv_path = Path(args.csv_out) if args.csv_out else out_dir / "sessions.csv"
    md_path = Path(args.md_out) if args.md_out else out_dir / "latest.md"

    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(csv_path, sessions)
    md_path.write_text(render_markdown(report), encoding="utf-8")

    if args.parquet_out:
        write_parquet(Path(args.parquet_out), sessions)

    print(f"Sessions analyzed: {len(sessions)} ({len(events)} events)")
    print(f"JSON: {json_path}")
    print(f"CSV:  {csv_path}")
    print(f"MD:   {md_path}")

    for row in report["by_task_category"]:
        print(
            f"  [{row['group']}] sessions={row['session_count']} "
            f"complete={row['complete_rate']*100:.0f}% "
            f"median_s={row.get('median_duration_seconds')}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
