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
CRITERIA_PATH = ROOT / "game/data/qa/acceptance_criteria.json"

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


def bootstrap_runner(issue_id: str) -> str | None:
    if not CRITERIA_PATH.is_file():
        return None
    data = json.loads(CRITERIA_PATH.read_text(encoding="utf-8"))
    profile = data.get("issue_bootstrap", {}).get(issue_id)
    if not profile:
        return None
    return profile.get("runner", "bash tools/run_bootstrap_ci_checks.sh")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check issue definition-of-done criteria")
    parser.add_argument("issue_id")
    parser.add_argument("--commit", default="", help="Commit SHA to verify CI against")
    parser.add_argument("--skip-ci", action="store_true", help="Skip CI runner (commit + evidence only)")
    args = parser.parse_args()

    board = load_board()
    issue = next((i for i in board.get("issues", []) if i["id"] == args.issue_id), None)
    if not issue:
        print(f"Unknown issue {args.issue_id}", file=sys.stderr)
        return 1

    done_req = issue.get("done_requires", "pr_merged")
    branch_pattern = issue.get("branch_name_pattern", "cursor/{issue_id}-a091")
    branch = branch_pattern.replace("{issue_id}", args.issue_id)
    commit = args.commit or issue.get("last_commit_sha") or ""

    if done_req == "push_only":
        if commit:
            print("OK — push_only satisfied (commit recorded)")
            return 0
        print("[FAIL] push_only requires last_commit_sha or --commit", file=sys.stderr)
        return 1

    if done_req == "ci_green_on_branch":
        if not commit:
            print("[FAIL] ci_green_on_branch requires commit SHA", file=sys.stderr)
            return 1

        evidence = ROOT / "artifacts/sprint_evidence" / args.issue_id / "manifest.json"
        if not evidence.is_file():
            print(
                "[WARN] commit set but no evidence bundle — run pm_bundle_evidence.py",
                file=sys.stderr,
            )
            return 1

        if args.skip_ci:
            print("OK — ci_green_on_branch (commit + evidence bundle; CI skipped)")
            return 0

        runner = bootstrap_runner(args.issue_id) or "bash tools/run_ci_checks.sh"
        print(f"==> Running CI profile: {runner}")
        r = subprocess.run(runner, shell=True, cwd=ROOT)
        if r.returncode != 0:
            print(f"[FAIL] {runner} exit {r.returncode}", file=sys.stderr)
            if bootstrap_runner(args.issue_id):
                print(
                    "Hint: P1-00 uses bootstrap profile — "
                    "see acceptance_criteria.json → issue_bootstrap.P1-00",
                    file=sys.stderr,
                )
            return 1

        required = issue.get("acceptance_gate_ids", [])
        print(f"OK — ci_green_on_branch ({runner} exit 0; gates: {', '.join(required)})")
        return 0

    if done_req == "pr_merged":
        merged, msg = gh_pr_merged_for_branch(branch)
        if merged:
            print(f"OK — pr_merged: {msg}")
            return 0
        if commit and subprocess.run(["which", "gh"], capture_output=True).returncode != 0:
            print(
                "[WARN] gh unavailable — accepting last_commit_sha only (set done_requires explicitly)",
                file=sys.stderr,
            )
            return 0
        print(f"[FAIL] pr_merged not satisfied: {msg}", file=sys.stderr)
        return 1

    print(f"[FAIL] unknown done_requires: {done_req}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
