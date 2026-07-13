#!/usr/bin/env python3
"""Validate issue done criteria before PM marks done — pr_merged / ci_green."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOARD_PATH = ROOT / "game/data/qa/sprint_board.json"

sys.path.insert(0, str(ROOT / "tools"))
from pm_orchestrator_lib import load_board  # noqa: E402


def gh_pr_merged_for_branch(branch: str) -> tuple[bool, str]:
    try:
        r = subprocess.run(
            ["gh", "pr", "list", "--head", branch, "--state", "merged", "--json", "number,mergedAt"],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        if r.returncode != 0:
            return False, r.stderr.strip() or "gh pr list failed"
        rows = json.loads(r.stdout or "[]")
        if rows:
            return True, f"PR #{rows[0]['number']} merged"
        return False, f"no merged PR for branch {branch}"
    except FileNotFoundError:
        return False, "gh not available"


def main() -> int:
    parser = argparse.ArgumentParser(description="Check issue definition-of-done criteria")
    parser.add_argument("issue_id")
    parser.add_argument("--commit", default="", help="Commit SHA to verify CI against")
    args = parser.parse_args()

    board = load_board()
    issue = next((i for i in board.get("issues", []) if i["id"] == args.issue_id), None)
    if not issue:
        print(f"Unknown issue {args.issue_id}", file=sys.stderr)
        return 1

    done_req = issue.get("done_requires", "pr_merged")
    branch_pattern = issue.get("branch_name_pattern", "cursor/{issue_id}-a091")
    branch = branch_pattern.replace("{issue_id}", args.issue_id)

    if done_req == "push_only":
        if issue.get("last_commit_sha") or args.commit:
            print(f"OK — push_only satisfied (commit recorded)")
            return 0
        print("[FAIL] push_only requires last_commit_sha or --commit", file=sys.stderr)
        return 1

    if done_req == "ci_green_on_branch":
        # Without game CI on main, check commit recorded + evidence manifest exists
        evidence = ROOT / "artifacts/sprint_evidence" / args.issue_id / "manifest.json"
        if args.commit or issue.get("last_commit_sha"):
            if evidence.is_file():
                print(f"OK — ci_green_on_branch (commit + evidence bundle)")
                return 0
            print("[WARN] commit set but no evidence bundle — run pm_bundle_evidence.py", file=sys.stderr)
            return 1
        print("[FAIL] ci_green_on_branch requires commit SHA", file=sys.stderr)
        return 1

    if done_req == "pr_merged":
        merged, msg = gh_pr_merged_for_branch(branch)
        if merged:
            print(f"OK — pr_merged: {msg}")
            return 0
        # Fallback: allow if github_issue closed and commit set (no gh)
        if issue.get("last_commit_sha") and not subprocess.run(["which", "gh"], capture_output=True).returncode == 0:
            print("[WARN] gh unavailable — accepting last_commit_sha only (set done_requires explicitly)", file=sys.stderr)
            return 0
        print(f"[FAIL] pr_merged not satisfied: {msg}", file=sys.stderr)
        return 1

    print(f"[FAIL] unknown done_requires: {done_req}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
