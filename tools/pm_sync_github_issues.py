#!/usr/bin/env python3
"""Sync sprint_board issues with GitHub Issues — traceability layer."""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOARD_PATH = ROOT / "game/data/qa/sprint_board.json"
PACK_SECTION_RE = re.compile(
    r"^##\s+(P\d+-\d+)\s+—\s+(.+?)$\n(.*?)(?=^##\s+P|\Z)",
    re.MULTILINE | re.DOTALL,
)

sys.path.insert(0, str(ROOT / "tools"))
from pm_orchestrator_lib import load_board, save_json  # noqa: E402


def parse_pack_sections(pack_path: Path) -> dict[str, dict[str, str]]:
    text = pack_path.read_text(encoding="utf-8")
    sections: dict[str, dict[str, str]] = {}
    for m in PACK_SECTION_RE.finditer(text):
        iid, title, body = m.group(1), m.group(2).strip(), m.group(3).strip()
        sections[iid] = {"title": title, "body": body}
    return sections


def gh_available() -> bool:
    try:
        r = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True)
        return r.returncode == 0
    except FileNotFoundError:
        return False


def create_github_issue(title: str, body: str, labels: list[str]) -> str | None:
    cmd = ["gh", "issue", "create", "--title", title, "--body", body]
    for label in labels:
        cmd.extend(["--label", label])
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    if r.returncode != 0:
        print(r.stderr, file=sys.stderr)
        return None
    # output is URL like https://github.com/owner/repo/issues/42
    url = (r.stdout or "").strip()
    if url.rstrip("/").split("/")[-1].isdigit():
        return url.rstrip("/").split("/")[-1]
    return url or None


def issue_labels(issue: dict) -> list[str]:
    labels = [f"agent/{issue.get('agent_owner', 'pm')}", "env/development"]
    phase = issue.get("phase")
    if phase is not None:
        labels.append(f"phase/{phase}")
    for gate in issue.get("acceptance_gate_ids") or []:
        labels.append(f"gate/{gate}")
    return labels


def validate_github_links(board: dict, require: bool) -> list[str]:
    errors: list[str] = []
    if not require:
        return errors
    for issue in board.get("issues", []):
        iid = issue.get("id", "?")
        if issue.get("status") in ("done", "carry_over"):
            continue
        if not issue.get("github_issue"):
            errors.append(f"{iid}: github_issue missing (orchestration.require_github_issues=true)")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync sprint board with GitHub Issues")
    parser.add_argument("--create", action="store_true", help="Create missing GitHub issues via gh CLI")
    parser.add_argument("--validate", action="store_true", help="Fail if github_issue links missing when required")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without creating")
    args = parser.parse_args()

    board = load_board()
    orch = board.get("orchestration", {})
    require = bool(orch.get("require_github_issues", False))
    pack_ref = board.get("active_sprint", {}).get("issue_pack_ref", "")
    pack_path = ROOT / pack_ref if pack_ref else None
    sections = parse_pack_sections(pack_path) if pack_path and pack_path.is_file() else {}

    errors = validate_github_links(board, require=require if args.validate else False)
    if errors:
        print("GitHub issue sync validation FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    missing = [i for i in board.get("issues", []) if not i.get("github_issue")]
    if not missing:
        print(f"OK — all {len(board.get('issues', []))} board issues have github_issue")
        return 0

    if not args.create:
        print(f"[INFO] {len(missing)} issues without github_issue — run with --create when GH_TOKEN/gh auth ready")
        for issue in missing:
            print(f"  - {issue['id']}: {issue.get('title')}")
        return 0 if not require else 1

    if not gh_available():
        print("[FAIL] gh CLI not authenticated — set GH_TOKEN or run gh auth login", file=sys.stderr)
        return 1

    created = 0
    for issue in missing:
        iid = issue["id"]
        pack = sections.get(iid, {})
        title = f"{iid} — {pack.get('title') or issue.get('title')}"
        body = pack.get("body") or issue.get("title", "")
        body += f"\n\n---\n**Board:** `game/data/qa/sprint_board.json`\n**Gates:** {', '.join(issue.get('acceptance_gate_ids') or [])}\n"
        labels = issue_labels(issue)
        if args.dry_run:
            print(f"[dry-run] create issue: {title}")
            continue
        num = create_github_issue(title, body, labels)
        if not num:
            print(f"[FAIL] could not create issue for {iid}", file=sys.stderr)
            return 1
        issue["github_issue"] = num
        created += 1
        print(f"[OK] {iid} → GitHub issue #{num}")

    if created and not args.dry_run:
        save_json(BOARD_PATH, board)
        print(f"Updated sprint_board.json with {created} github_issue links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
