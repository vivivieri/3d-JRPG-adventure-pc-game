#!/usr/bin/env python3
"""Linear sync manifest + optional API push — sprint_phases.json linear config."""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOARD_PATH = ROOT / "game/data/qa/sprint_board.json"
PHASES_PATH = ROOT / "game/data/qa/sprint_phases.json"
MANIFEST_PATH = ROOT / "artifacts/linear_sync_manifest.json"

LINEAR_API = "https://api.linear.app/graphql"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_manifest() -> dict:
    board = load_json(BOARD_PATH)
    phases = load_json(PHASES_PATH)
    active = board.get("active_sprint", {})
    phase_num = active.get("phase")
    phase_row = next((p for p in phases.get("phases", []) if p.get("phase") == phase_num), {})
    linear_project = phase_row.get("linear_project")

    issues = []
    for issue in board.get("issues", []):
        issues.append(
            {
                "identifier": issue["id"],
                "title": issue.get("title"),
                "status": issue.get("status"),
                "agent_owner": issue.get("agent_owner"),
                "github_issue": issue.get("github_issue"),
                "linear_issue_id": issue.get("linear_issue"),
            }
        )

    return {
        "version": "1.0",
        "sprint_id": active.get("id"),
        "phase": phase_num,
        "linear_project": linear_project,
        "team": phases.get("linear", {}).get("team_suggested_name"),
        "issues": issues,
        "label_mirror": phases.get("linear", {}).get("label_mirror", []),
    }


def linear_graphql(query: str, variables: dict | None = None) -> dict:
    token = os.environ.get("LINEAR_API_KEY", "")
    if not token:
        raise RuntimeError("LINEAR_API_KEY not set")
    body = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
    req = urllib.request.Request(
        LINEAR_API,
        data=body,
        headers={"Authorization": token, "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if data.get("errors"):
        raise RuntimeError(json.dumps(data["errors"]))
    return data.get("data", {})


def push_to_linear(manifest: dict) -> int:
    """Best-effort: requires LINEAR_API_KEY and team setup in Linear dashboard."""
    try:
        teams = linear_graphql("{ teams { nodes { id name } } }")
        team_name = manifest.get("team", "")
        team_id = None
        for node in teams.get("teams", {}).get("nodes", []):
            if node.get("name") == team_name:
                team_id = node["id"]
                break
        if not team_id:
            print(f"[WARN] Linear team '{team_name}' not found — manifest only", file=sys.stderr)
            return 0

        for row in manifest.get("issues", []):
            title = f"{row['identifier']} — {row.get('title', '')}"
            desc = f"GitHub: {row.get('github_issue') or 'pending'}\nStatus: {row.get('status')}\nAgent: {row.get('agent_owner')}"
            mutation = """
            mutation IssueCreate($teamId: String!, $title: String!, $description: String) {
              issueCreate(input: { teamId: $teamId, title: $title, description: $description }) {
                success
                issue { id identifier }
              }
            }
            """
            if row.get("linear_issue_id"):
                continue
            data = linear_graphql(mutation, {"teamId": team_id, "title": title, "description": desc})
            created = data.get("issueCreate", {}).get("issue")
            if created:
                print(f"[OK] Linear: {row['identifier']} → {created.get('identifier')}")
        return 0
    except Exception as exc:
        print(f"[WARN] Linear push skipped: {exc}", file=sys.stderr)
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Linear sync manifest for sprint board")
    parser.add_argument("--write", action="store_true", help="Write artifacts/linear_sync_manifest.json")
    parser.add_argument("--push", action="store_true", help="Push new issues to Linear when LINEAR_API_KEY set")
    parser.add_argument("--validate", action="store_true", help="Validate manifest schema")
    args = parser.parse_args()

    manifest = build_manifest()
    if args.write or args.push or args.validate:
        MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
        MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Manifest: {MANIFEST_PATH.relative_to(ROOT)}")

    if args.validate:
        if not manifest.get("issues"):
            print("[FAIL] manifest has no issues", file=sys.stderr)
            return 1
        print(f"OK — {len(manifest['issues'])} issues in manifest")
        return 0

    if args.push:
        return push_to_linear(manifest)

    if args.write:
        return 0

    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
