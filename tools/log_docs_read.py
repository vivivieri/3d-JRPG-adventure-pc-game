#!/usr/bin/env python3
"""Append doc paths to the session docs_reads log (enforced adherence).

Trigger (session gate): seed must_read from the resolved pack JSON.
Follower (post-cycle): check_docs_pack_adherence.py --strict.

Usage:
  python3 tools/log_docs_read.py --issue P1-01 --from-pack
  python3 tools/log_docs_read.py --issue P1-01 docs/foo.md AGENTS.md
  python3 tools/log_docs_read.py --issue P1-01 --from-pack --log /tmp/reads.log
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _board_issue_id(issue_raw: str) -> str:
    board_path = ROOT / "game/data/qa/sprint_board.json"
    if not board_path.is_file():
        return issue_raw
    try:
        board = json.loads(board_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(
            f"[WARN] log_docs_read: sprint_board unreadable ({exc})",
            file=sys.stderr,
        )
        return issue_raw
    for row in board.get("issues") or []:
        if str(row.get("id") or "") == issue_raw or str(
            row.get("github_issue") or ""
        ) == issue_raw:
            return str(row.get("id") or issue_raw)
    return issue_raw


def _pack_path(issue_raw: str, board_id: str) -> Path:
    for key in (issue_raw, board_id):
        cand = ROOT / "artifacts" / f"docs_pack_{key}.json"
        if cand.is_file():
            return cand
    return ROOT / "artifacts" / f"docs_pack_{board_id}.json"


def _default_log(issue_raw: str, board_id: str) -> Path:
    env = os.environ.get("DOCS_READ_LOG")
    if env:
        return Path(env)
    for key in (issue_raw, board_id):
        cand = ROOT / "artifacts" / f"docs_reads_{key}.log"
        if cand.is_file():
            return cand
    return ROOT / "artifacts" / f"docs_reads_{board_id}.log"


def _paths_from_pack(pack: Path) -> list[str]:
    data = json.loads(pack.read_text(encoding="utf-8"))
    out: list[str] = []
    for row in data.get("must_read") or []:
        if isinstance(row, dict):
            p = row.get("path")
        else:
            p = row
        if isinstance(p, str) and p.strip():
            out.append(p.strip().lstrip("./"))
    return out


def _append_paths(log_path: Path, paths: list[str]) -> int:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    existing: set[str] = set()
    if log_path.is_file():
        for line in log_path.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if s and not s.startswith("#"):
                existing.add(s)
    added = 0
    with log_path.open("a", encoding="utf-8") as fh:
        for path in paths:
            if path in existing:
                continue
            fh.write(path + "\n")
            existing.add(path)
            added += 1
    return added


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--issue", required=True)
    parser.add_argument(
        "--from-pack",
        action="store_true",
        help="Seed must_read paths from artifacts/docs_pack_<issue>.json",
    )
    parser.add_argument("--log", help="Override reads log path")
    parser.add_argument(
        "paths",
        nargs="*",
        help="Extra docs/… or AGENTS.md paths to append",
    )
    args = parser.parse_args()

    issue_raw = str(args.issue).strip()
    board_id = _board_issue_id(issue_raw)
    log_path = Path(args.log) if args.log else _default_log(issue_raw, board_id)

    to_add: list[str] = []
    if args.from_pack:
        pack = _pack_path(issue_raw, board_id)
        if not pack.is_file():
            print(
                f"[FAIL] log_docs_read: missing pack report {pack.relative_to(ROOT)}",
                file=sys.stderr,
            )
            return 1
        try:
            to_add.extend(_paths_from_pack(pack))
        except json.JSONDecodeError as exc:
            print(f"[FAIL] log_docs_read: invalid pack JSON ({exc})", file=sys.stderr)
            return 1
        if not to_add:
            print(
                f"[FAIL] log_docs_read: pack has empty must_read ({pack.name})",
                file=sys.stderr,
            )
            return 1

    for p in args.paths:
        s = str(p).strip().lstrip("./")
        if s:
            to_add.append(s)

    if not to_add:
        print(
            "[FAIL] log_docs_read: nothing to append "
            "(pass --from-pack and/or path args)",
            file=sys.stderr,
        )
        return 2

    added = _append_paths(log_path, to_add)
    rel = (
        str(log_path.relative_to(ROOT))
        if str(log_path.resolve()).startswith(str(ROOT))
        else str(log_path)
    )
    print(f"[OK] log_docs_read — appended {added} path(s) → {rel} (total new batch {len(to_add)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
