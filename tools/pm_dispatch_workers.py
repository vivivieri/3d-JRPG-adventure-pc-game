#!/usr/bin/env python3
"""Dispatch worker Cloud Agents via GitHub issue labels + manifest.

After PM orchestrator computes next_dispatch, this script:
  1. Writes artifacts/worker_dispatch_manifest.json
  2. Marks board issues in_progress
  3. Adds dispatch/ready + agent/* labels on linked GitHub issues (triggers Worker automation)

Authority: docs/agents/FACTORY_SETUP_GUIDE.md
Catalog: game/data/qa/factory_automations.json
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOARD_PATH = ROOT / "game/data/qa/sprint_board.json"
REPORT_PATH = ROOT / "artifacts/pm_orchestrator_report.json"
PACKET_PATH = ROOT / "artifacts/pm_dispatch_packet.json"
MANIFEST_PATH = ROOT / "artifacts/worker_dispatch_manifest.json"
CATALOG_PATH = ROOT / "game/data/qa/factory_automations.json"

sys.path.insert(0, str(ROOT / "tools"))
from pm_orchestrator_lib import load_board, save_json  # noqa: E402

WORKER_ROLES = {
    "architect",
    "builder",
    "qa",
    "flow",
    "visual",
    "release",
    "analyst",
}


def gh_available() -> bool:
    try:
        return subprocess.run(["gh", "auth", "status"], capture_output=True).returncode == 0
    except FileNotFoundError:
        print("WARN: gh CLI not found", file=sys.stderr)
        return False


def load_json(path: Path) -> dict:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def issue_number(github_issue: str | int | None) -> str | None:
    if github_issue is None:
        return None
    s = str(github_issue).strip().rstrip("/")
    if s.isdigit():
        return s
    if "/" in s:
        tail = s.split("/")[-1]
        return tail if tail.isdigit() else None
    return None


def gh_issue_edit(num: str, add_labels: list[str], dry_run: bool) -> bool:
    cmd = ["gh", "issue", "edit", num]
    for label in add_labels:
        cmd.extend(["--add-label", label])
    if dry_run:
        print(f"[dry-run] {' '.join(cmd)}")
        return True
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    if r.returncode != 0:
        print(r.stderr or r.stdout, file=sys.stderr)
        return False
    return True


def gh_issue_comment(num: str, body: str, dry_run: bool) -> bool:
    cmd = ["gh", "issue", "comment", num, "--body", body]
    if dry_run:
        print(f"[dry-run] gh issue comment {num} …")
        return True
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    if r.returncode != 0:
        print(r.stderr or r.stdout, file=sys.stderr)
        return False
    return True


def build_manifest(dispatch_packets: list[dict], report: dict) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    entries = []
    for pkt in dispatch_packets:
        agent = pkt.get("agent", "pm")
        if agent == "pm":
            continue
        if agent not in WORKER_ROLES:
            print(f"[WARN] Unknown agent role '{agent}' — skipping dispatch", file=sys.stderr)
            continue
        entries.append(
            {
                "issue_id": pkt.get("issue_id"),
                "agent": agent,
                "action": pkt.get("action"),
                "branch": pkt.get("branch"),
                "sprint_branch": pkt.get("sprint_branch", "game/development"),
                "session_gate_command": pkt.get("session_gate_command"),
                "acceptance_gate_ids": pkt.get("acceptance_gate_ids", []),
                "github_issue": pkt.get("github_issue"),
                "handoff_refs": pkt.get("handoff_refs", []),
                "worker_prompt": "docs/agents/automation_prompts/worker_sprint_issue.md",
                "boot_commands": [
                    "bash tools/ensure_mcp_stack.sh",
                    "bash tools/check_snapshot_boot.sh",
                    "bash tools/check_mcp_ready.sh",
                ],
                "end_command": (
                    f"bash tools/run_post_agent_cycle.sh --issue {pkt.get('issue_id')} "
                    f"--agent {agent} --commit $(git rev-parse HEAD)"
                ),
            }
        )
    return {
        "version": "1.0",
        "generated_at": now,
        "sprint_id": report.get("sprint_id"),
        "dispatch_count": len(entries),
        "trigger_label": "dispatch/ready",
        "workers": entries,
    }


def apply_board_in_progress(issue_id: str, agent: str, dry_run: bool) -> None:
    board = load_board()
    for issue in board.get("issues", []):
        if issue.get("id") != issue_id:
            continue
        if issue.get("status") == "done":
            return
        if dry_run:
            print(f"[dry-run] mark {issue_id} in_progress agent={agent}")
            return
        issue["status"] = "in_progress"
        issue["last_agent_session"] = datetime.now(timezone.utc).isoformat()
        save_json(BOARD_PATH, board)
        print(f"[OK] board: {issue_id} → in_progress")
        return


def dispatch_worker(pkt: dict, catalog: dict, dry_run: bool) -> bool:
    agent = pkt.get("agent", "")
    issue_id = pkt.get("issue_id", "?")
    if agent == "pm":
        print(f"[SKIP] {issue_id} — PM-owned (no worker label dispatch)")
        return True
    if agent not in WORKER_ROLES:
        print(f"[SKIP] {issue_id} — role '{agent}' not a worker role")
        return True

    apply_board_in_progress(issue_id, agent, dry_run)

    trigger = catalog.get("dispatch", {}).get("trigger_label", "dispatch/ready")
    in_prog = catalog.get("dispatch", {}).get("in_progress_label", "status/in-progress")
    labels = [trigger, in_prog, f"agent/{agent}"]

    num = issue_number(pkt.get("github_issue"))
    if not num:
        print(
            f"[WARN] {issue_id} — no github_issue link; manifest written but Worker automation "
            "will not auto-start. Run: python3 tools/pm_sync_github_issues.py --create",
            file=sys.stderr,
        )
        return False

    if not gh_available():
        print(
            f"[WARN] {issue_id} — gh not authenticated; labels not applied. Set GH_TOKEN.",
            file=sys.stderr,
        )
        return False

    if not gh_issue_edit(num, labels, dry_run):
        return False

    comment = (
        f"## Factory dispatch — {issue_id}\n\n"
        f"**Role:** `{agent}`\n"
        f"**Session gate:** `{pkt.get('session_gate_command')}`\n"
        f"**Branch:** `{pkt.get('branch')}`\n"
        f"**Gates:** {', '.join(pkt.get('acceptance_gate_ids') or [])}\n\n"
        f"Worker automation: boot from **Environment snapshot**, then read "
        f"`artifacts/worker_dispatch_manifest.json`.\n\n"
        f"End session: `bash tools/run_post_agent_cycle.sh --issue {issue_id} "
        f"--agent {agent} --commit $(git rev-parse HEAD)`\n"
    )
    if not gh_issue_comment(num, comment, dry_run):
        return False

    print(f"[OK] dispatched {issue_id} → GitHub #{num} labels={labels}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Dispatch worker agents via GitHub labels")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--head-only", action="store_true", help="Dispatch only first worker in packet")
    args = parser.parse_args()

    catalog = load_json(CATALOG_PATH)
    report = load_json(REPORT_PATH)
    packet_doc = load_json(PACKET_PATH)
    packets = packet_doc.get("dispatch") or []

    if not packets and report.get("next_dispatch"):
        print("[WARN] pm_dispatch_packet.json empty — re-run orchestrator with --write-dispatch-packet")
        return 1

    target_packets = packets[:1] if args.head_only else packets
    manifest = build_manifest(target_packets, report)
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    if args.dry_run:
        print(json.dumps(manifest, indent=2))
    else:
        MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        print(f"[OK] wrote {MANIFEST_PATH.relative_to(ROOT)} ({manifest['dispatch_count']} workers)")

    if manifest["dispatch_count"] == 0:
        print("[INFO] No worker roles in next_dispatch — PM session only")
        return 0

    ok = 0
    fail = 0
    for pkt in target_packets:
        if dispatch_worker(pkt, catalog, args.dry_run):
            ok += 1
        else:
            fail += 1

    if fail and not args.dry_run:
        print(f"[WARN] {fail} dispatch(es) incomplete — check GH_TOKEN and github_issue links")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
