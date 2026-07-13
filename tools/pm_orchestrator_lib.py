#!/usr/bin/env python3
"""Shared sprint board logic — docs/SPRINT_ORCHESTRATION.md."""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BOARD_PATH = ROOT / "game/data/qa/sprint_board.json"
PHASES_PATH = ROOT / "game/data/qa/sprint_phases.json"
REPORT_PATH = ROOT / "artifacts/pm_orchestrator_report.json"

REQUIRED_ISSUE_FIELDS = (
    "id",
    "title",
    "sequence",
    "phase",
    "implementation_plan_tasks",
    "agent_owner",
    "acceptance_gate_ids",
    "status",
    "depends_on",
    "agent_owner",
)
VALID_AGENTS = {"pm", "architect", "builder", "qa", "flow", "release", "visual", "human"}
VALID_STATUS = {"pending", "in_progress", "blocked", "done", "carry_over"}
PACK_ISSUE_RE = re.compile(r"^##\s+(P\d+-\d+)\s+—", re.MULTILINE)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_board() -> dict[str, Any]:
    return load_json(BOARD_PATH)


def issue_index(board: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {i["id"]: i for i in board.get("issues", [])}


def parse_issue_pack(pack_path: Path) -> list[str]:
    if not pack_path.is_file():
        return []
    text = pack_path.read_text(encoding="utf-8")
    return sorted(set(PACK_ISSUE_RE.findall(text)))


def deps_satisfied(issue: dict[str, Any], idx: dict[str, dict[str, Any]]) -> bool:
    for dep in issue.get("depends_on", []):
        dep_issue = idx.get(dep)
        if not dep_issue or dep_issue.get("status") != "done":
            return False
    return True


def validate_board_schema(board: dict[str, Any], strict: bool = False) -> list[str]:
    errors: list[str] = []
    active = board.get("active_sprint")
    if not active:
        errors.append("active_sprint missing")
        return errors
    for key in ("id", "phase", "sprint_number", "status", "issue_pack_ref"):
        if key not in active:
            errors.append(f"active_sprint missing {key}")
    issues = board.get("issues", [])
    if not issues:
        errors.append("issues must be non-empty when sprint active")
    ids = set()
    for issue in issues:
        iid = issue.get("id")
        if not iid:
            errors.append("issue missing id")
            continue
        if iid in ids:
            errors.append(f"duplicate issue id {iid}")
        ids.add(iid)
        for field in (
            "title",
            "sequence",
            "phase",
            "implementation_plan_tasks",
            "agent_owner",
            "acceptance_gate_ids",
            "status",
            "depends_on",
        ):
            if field not in issue:
                errors.append(f"{iid}: missing {field}")
        if issue.get("agent_owner") not in VALID_AGENTS:
            errors.append(f"{iid}: invalid agent_owner {issue.get('agent_owner')!r}")
        if issue.get("status") not in VALID_STATUS:
            errors.append(f"{iid}: invalid status {issue.get('status')!r}")
        if strict and issue.get("status") not in ("done", "carry_over"):
            if not issue.get("implementation_plan_tasks"):
                errors.append(f"{iid}: implementation_plan_tasks empty")
            if issue.get("agent_owner") != "pm" and not issue.get("acceptance_gate_ids") and iid.endswith("-06") is False:
                # sprint review may have empty gates
                if "review" not in issue.get("title", "").lower():
                    errors.append(f"{iid}: acceptance_gate_ids empty")
        for dep in issue.get("depends_on", []):
            if dep not in ids and dep not in {x.get("id") for x in issues}:
                pass  # checked in second pass
    # dependency refs
    for issue in issues:
        iid = issue.get("id", "?")
        for dep in issue.get("depends_on", []):
            if dep not in ids:
                errors.append(f"{iid}: depends_on unknown {dep}")
    # phase alignment
    ap_phase = active.get("phase")
    for issue in issues:
        if issue.get("phase") != ap_phase:
            errors.append(f"{issue.get('id')}: phase {issue.get('phase')} != active_sprint.phase {ap_phase}")
    max_issues = active.get("max_issues", 10)
    if len(issues) > max_issues:
        errors.append(f"too many issues ({len(issues)} > max_issues {max_issues})")
    return errors


def detect_stale(board: dict[str, Any]) -> list[dict[str, Any]]:
    stale: list[dict[str, Any]] = []
    hours = board.get("orchestration", {}).get("stale_hours", 24)
    now = datetime.now(timezone.utc)
    for issue in board.get("issues", []):
        if issue.get("status") != "in_progress":
            continue
        ts = issue.get("last_agent_session")
        if not ts:
            stale.append({"id": issue["id"], "reason": "in_progress without last_agent_session timestamp"})
            continue
        try:
            last = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            if last.tzinfo is None:
                last = last.replace(tzinfo=timezone.utc)
            delta_h = (now - last).total_seconds() / 3600.0
            if delta_h >= hours:
                stale.append(
                    {
                        "id": issue["id"],
                        "reason": f"in_progress stale {delta_h:.1f}h >= {hours}h",
                        "agent_owner": issue.get("agent_owner"),
                    }
                )
        except ValueError:
            stale.append({"id": issue["id"], "reason": f"invalid last_agent_session {ts!r}"})
    return stale


def wip_violations(board: dict[str, Any]) -> list[dict[str, Any]]:
    limits = board.get("orchestration", {}).get("max_in_progress", {})
    counts: dict[str, int] = {}
    for issue in board.get("issues", []):
        if issue.get("status") == "in_progress":
            agent = issue.get("agent_owner", "")
            counts[agent] = counts.get(agent, 0) + 1
    violations = []
    for agent, count in counts.items():
        cap = limits.get(agent)
        if cap is not None and count > cap:
            violations.append({"agent": agent, "count": count, "max": cap})
    return violations


def compute_dispatch(board: dict[str, Any]) -> dict[str, Any]:
    idx = issue_index(board)
    active = board.get("active_sprint", {})
    dispatch: list[dict[str, Any]] = []
    blocked: list[dict[str, Any]] = []

    for issue in sorted(board.get("issues", []), key=lambda x: x.get("sequence", 999)):
        iid = issue["id"]
        status = issue.get("status")
        if status == "done":
            continue
        if status == "carry_over":
            continue
        if not deps_satisfied(issue, idx):
            missing = [d for d in issue.get("depends_on", []) if idx.get(d, {}).get("status") != "done"]
            blocked.append({"id": iid, "blocked_by": missing, "agent_owner": issue.get("agent_owner")})
            continue
        if status in ("pending", "in_progress", "blocked"):
            dispatch.append(
                {
                    "priority": issue.get("sequence", 999),
                    "issue_id": iid,
                    "agent": issue.get("agent_owner"),
                    "co_agent": issue.get("co_agent"),
                    "action": "continue" if status == "in_progress" else "start",
                    "title": issue.get("title"),
                    "acceptance_gate_ids": issue.get("acceptance_gate_ids", []),
                    "implementation_plan_tasks": issue.get("implementation_plan_tasks", []),
                }
            )

    # only head of queue unless in_progress continues
    in_progress = [d for d in dispatch if d["action"] == "continue"]
    pending = [d for d in dispatch if d["action"] == "start"]
    next_dispatch = in_progress[:3] + pending[:1]

    incomplete = [i for i in board.get("issues", []) if i.get("status") not in ("done", "carry_over")]
    sprint_complete = len(incomplete) == 0

    return {
        "sprint_id": active.get("id"),
        "phase": active.get("phase"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sprint_complete": sprint_complete,
        "next_dispatch": next_dispatch,
        "blocked_issues": blocked,
        "stale_issues": detect_stale(board),
        "wip_violations": wip_violations(board),
        "incomplete_count": len(incomplete),
    }


def sync_missing_from_pack(board: dict[str, Any], dry_run: bool = False) -> tuple[list[str], list[str]]:
    """Return (added_ids, missing_in_pack)."""
    pack_ref = board.get("active_sprint", {}).get("issue_pack_ref", "")
    pack_path = ROOT / pack_ref if pack_ref else None
    pack_ids = parse_issue_pack(pack_path) if pack_path else []
    board_ids = {i["id"] for i in board.get("issues", [])}
    pack_set = set(pack_ids)
    missing_in_board = sorted(pack_set - board_ids)
    missing_in_pack = sorted(board_ids - pack_set)
    added: list[str] = []
    if missing_in_board and not dry_run:
        carry = board.setdefault("carry_over_queue", [])
        for mid in missing_in_board:
            carry.append(
                {
                    "id": mid,
                    "reason": "present in issue pack but missing from sprint_board — PM must add full issue row",
                    "detected_at": datetime.now(timezone.utc).isoformat(),
                }
            )
            added.append(mid)
    return added, missing_in_pack


def orchestrator_pass(report: dict[str, Any], board: dict[str, Any]) -> bool:
    if report.get("stale_issues"):
        return False
    if report.get("wip_violations"):
        return False
    if board.get("carry_over_queue"):
        return False
    return True


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="PM sprint orchestrator dispatch")
    parser.add_argument("--dispatch", action="store_true", help="Compute next agent dispatch")
    parser.add_argument("--write-report", action="store_true", help="Write artifacts/pm_orchestrator_report.json")
    parser.add_argument("--json", action="store_true", help="Print report JSON to stdout")
    args = parser.parse_args()

    if not args.dispatch:
        parser.print_help()
        return 2

    board = load_board()
    report = compute_dispatch(board)
    report["orchestrator_pass"] = orchestrator_pass(report, board)

    if args.write_report:
        save_json(REPORT_PATH, report)

    if args.json:
        import json as _json

        print(_json.dumps(report, indent=2))
    else:
        print("==> PM Orchestrator dispatch")
        print(f"    Sprint: {report.get('sprint_id')} (phase {report.get('phase')})")
        print(f"    Incomplete: {report.get('incomplete_count')}")
        print(f"    Sprint complete: {report.get('sprint_complete')}")
        print(f"    Orchestrator pass: {report.get('orchestrator_pass')}")
        if report.get("stale_issues"):
            print("\n[FAIL] Stale issues:")
            for s in report["stale_issues"]:
                print(f"  - {s['id']}: {s['reason']}")
        if report.get("wip_violations"):
            print("\n[FAIL] WIP violations:")
            for v in report["wip_violations"]:
                print(f"  - {v['agent']}: {v['count']} > max {v['max']}")
        if report.get("blocked_issues"):
            print("\n[INFO] Blocked (deps):")
            for b in report["blocked_issues"][:5]:
                print(f"  - {b['id']} blocked by {b['blocked_by']}")
        print("\n==> NEXT DISPATCH (assign these agents now)")
        for d in report.get("next_dispatch", []):
            gates = ", ".join(d.get("acceptance_gate_ids") or []) or "(see issue)"
            print(
                f"  [{d['priority']}] {d['issue_id']} → agent/{d['agent']} "
                f"({d['action']}) gates: {gates}"
            )
        if report.get("next_dispatch"):
            head = report["next_dispatch"][0]
            print("\n==> AGENT_SESSION_COMMAND")
            print(f"bash tools/run_agent_session_gate.sh {head['agent']} {head['issue_id']}")
        if args.write_report:
            print(f"\nReport: {REPORT_PATH.relative_to(ROOT)}")

    return 0 if report.get("orchestrator_pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
