#!/usr/bin/env python3
"""Record per-issue gate evidence bundles — docs/SPRINT_ORCHESTRATION.md."""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOARD_PATH = ROOT / "game/data/qa/sprint_board.json"
EVIDENCE_ROOT = ROOT / "artifacts/sprint_evidence"


def main() -> int:
    parser = argparse.ArgumentParser(description="Bundle sprint issue evidence")
    parser.add_argument("issue_id", help="e.g. P1-02")
    parser.add_argument("--gate", action="append", default=[], help="Gate ID this artifact satisfies")
    parser.add_argument("--artifact", action="append", default=[], help="Path to evidence file or directory")
    parser.add_argument("--note", default="", help="Optional note")
    parser.add_argument("--list", action="store_true", help="List manifest for issue")
    args = parser.parse_args()

    issue_dir = EVIDENCE_ROOT / args.issue_id
    manifest_path = issue_dir / "manifest.json"

    if args.list:
        if not manifest_path.is_file():
            print(f"No evidence bundle for {args.issue_id}")
            return 1
        print(json.dumps(json.loads(manifest_path.read_text(encoding="utf-8")), indent=2))
        return 0

    if not BOARD_PATH.is_file():
        print("sprint_board.json missing", file=sys.stderr)
        return 1

    board = json.loads(BOARD_PATH.read_text(encoding="utf-8"))
    issue = next((i for i in board["issues"] if i["id"] == args.issue_id), None)
    if not issue:
        print(f"Unknown issue {args.issue_id}", file=sys.stderr)
        return 1

    issue_dir.mkdir(parents=True, exist_ok=True)
    manifest = {"issue_id": args.issue_id, "entries": []}
    if manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    now = datetime.now(timezone.utc).isoformat()
    for src_path in args.artifact:
        src = Path(src_path)
        if not src.is_file() and not src.is_dir():
            print(f"[WARN] artifact not found: {src}", file=sys.stderr)
            continue
        dest = issue_dir / src.name
        if src.is_dir():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(src, dest)
        else:
            shutil.copy2(src, dest)
        manifest["entries"].append(
            {
                "at": now,
                "gates": list(args.gate),
                "path": str(dest.relative_to(ROOT)),
                "note": args.note or None,
            }
        )

    manifest["updated_at"] = now
    manifest["required_gates"] = issue.get("acceptance_gate_ids", [])
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"OK — evidence bundle: {manifest_path.relative_to(ROOT)} ({len(manifest['entries'])} entries)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
