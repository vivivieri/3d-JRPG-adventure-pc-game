#!/usr/bin/env python3
"""Enforce session file reads stay inside the resolved docs pack.

Reads artifacts/docs_pack_<issue>.json (allowed_read_paths) and a newline list
of paths the agent opened:

  DOCS_READ_LOG                 env override
  --reads-file PATH             explicit
  artifacts/docs_reads_<issue>.log   default (session gate auto-seeds must_read)

Exit 0 on OK. With --strict (post-cycle default): exit 1 on missing pack,
missing/empty reads log, or reads outside pack∪deferred.
Also accepts paths logged as: READ docs/foo.md
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _normalize(path: str) -> str:
    p = path.strip().lstrip("./")
    if p.startswith("res://"):
        p = p[6:]
    p = re.sub(r"^(READ|OPEN|opened|read)\s+", "", p, flags=re.I)
    return p.strip()


def _rel_display(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--issue", required=True)
    parser.add_argument(
        "--reads-file",
        help="Newline-separated paths the agent opened (docs/… or AGENTS.md)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 on missing pack/log, empty reads, or extras outside pack",
    )
    args = parser.parse_args()

    issue_raw = str(args.issue).strip()
    report = ROOT / "artifacts" / f"docs_pack_{issue_raw}.json"
    board_issue_id = issue_raw
    if not report.is_file():
        # Allow GitHub issue numbers: map 130 → P1-01 via sprint_board
        board_path = ROOT / "game/data/qa/sprint_board.json"
        if board_path.is_file():
            try:
                board = json.loads(board_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                msg = f"docs_pack adherence: sprint_board unreadable ({exc})"
                print(f"[FAIL] {msg}" if args.strict else f"[WARN] {msg}", file=sys.stderr)
                return 1 if args.strict else 0
            for row in board.get("issues") or []:
                if str(row.get("github_issue") or "") == issue_raw or str(
                    row.get("id") or ""
                ) == issue_raw:
                    board_issue_id = str(row.get("id") or issue_raw)
                    alt = ROOT / "artifacts" / f"docs_pack_{board_issue_id}.json"
                    if alt.is_file():
                        report = alt
                    break
    if not report.is_file():
        msg = f"docs_pack adherence: missing pack report {_rel_display(report)}"
        print(f"[FAIL] {msg}" if args.strict else f"[WARN] {msg}")
        return 1 if args.strict else 0

    try:
        data = json.loads(report.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        msg = f"docs_pack adherence: invalid JSON ({exc})"
        print(f"[FAIL] {msg}" if args.strict else f"[WARN] {msg}", file=sys.stderr)
        return 1 if args.strict else 0

    allowed = {
        _normalize(p)
        for p in (data.get("allowed_read_paths") or [])
        if isinstance(p, str)
    }
    allowed.update(
        {
            "docs/ops/BOOT.md",
            "AGENTS.md",
            "docs/INDEX.yaml",
            "docs/llms.txt",
            "docs/README.md",
        }
    )
    # Sprint issue leaves are never_autoload for resolve_docs, but reading the
    # active issue pack (or GitHub #N body mirror) is legitimate for the session.
    issue_key = str(board_issue_id).strip().upper().replace("_", "-")
    for path in (
        ROOT.joinpath("docs/ops/sprints").rglob("*.md")
        if (ROOT / "docs/ops/sprints").is_dir()
        else []
    ):
        rel = path.relative_to(ROOT).as_posix()
        stem = path.stem.upper().replace("_", "-")
        text_head = path.read_text(encoding="utf-8", errors="replace")[:2000]
        if issue_key and (
            issue_key in stem
            or f"## {issue_key} " in text_head
            or f"## {issue_key}—" in text_head
            or f"## {issue_key} —" in text_head
        ):
            allowed.add(rel)

    default_log = ROOT / "artifacts" / f"docs_reads_{board_issue_id}.log"
    if not default_log.is_file() and issue_raw != board_issue_id:
        alt_log = ROOT / "artifacts" / f"docs_reads_{issue_raw}.log"
        if alt_log.is_file():
            default_log = alt_log
    reads_file = args.reads_file or os.environ.get("DOCS_READ_LOG") or str(default_log)
    reads_path = Path(reads_file)
    if not reads_path.is_file():
        msg = (
            f"docs_pack adherence: no reads log at {_rel_display(reads_path)} "
            "(session gate must auto-seed via log_docs_read.py --from-pack)"
        )
        print(f"[FAIL] {msg}" if args.strict else f"[OK] {msg}")
        return 1 if args.strict else 0

    raw_lines = reads_path.read_text(encoding="utf-8").splitlines()
    reads = [
        _normalize(line)
        for line in raw_lines
        if line.strip() and not line.strip().startswith("#")
    ]

    doc_reads = [
        r
        for r in reads
        if r.startswith("docs/") or r == "AGENTS.md" or r.endswith(".md")
    ]
    if not doc_reads:
        msg = (
            f"docs_pack adherence: reads log empty of doc paths "
            f"({_rel_display(reads_path)}) — session gate must seed must_read"
        )
        print(f"[FAIL] {msg}" if args.strict else f"[OK] {msg}")
        return 1 if args.strict else 0

    extras = sorted({r for r in doc_reads if r not in allowed and r.startswith("docs/")})
    if not extras:
        print(f"[OK] docs_pack adherence — {len(doc_reads)} doc read(s) within pack")
        return 0

    label = "FAIL" if args.strict else "WARN"
    print(f"[{label}] docs_pack adherence — {len(extras)} read(s) outside pack∪deferred:")
    for path in extras[:20]:
        print(f"  - {path}")
    if args.strict:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
