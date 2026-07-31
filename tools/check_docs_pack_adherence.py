#!/usr/bin/env python3
"""Warn when session file reads look outside the resolved docs pack.

Reads artifacts/docs_pack_<issue>.json (allowed_read_paths) and optionally a
newline list of paths the agent opened (DOCS_READ_LOG or --reads-file).

Exit 0 always unless --strict (then exit 1 on extras). Designed for
run_post_agent_cycle.sh as a soft WARN by default.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _normalize(path: str) -> str:
    p = path.strip().lstrip("./")
    if p.startswith("res://"):
        p = p[6:]
    return p


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
        help="Exit 1 when reads fall outside pack∪deferred",
    )
    args = parser.parse_args()

    report = ROOT / "artifacts" / f"docs_pack_{args.issue}.json"
    if not report.is_file():
        print(f"[WARN] docs_pack adherence: missing {report.relative_to(ROOT)}")
        return 0

    try:
        data = json.loads(report.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"[WARN] docs_pack adherence: invalid JSON ({exc})", file=sys.stderr)
        return 0

    allowed = {
        _normalize(p)
        for p in (data.get("allowed_read_paths") or [])
        if isinstance(p, str)
    }
    # Always allow boot + router meta
    allowed.update(
        {
            "docs/ops/BOOT.md",
            "AGENTS.md",
            "docs/INDEX.yaml",
            "docs/llms.txt",
            "docs/README.md",
        }
    )

    reads: list[str] = []
    reads_file = args.reads_file or os.environ.get("DOCS_READ_LOG")
    if reads_file and Path(reads_file).is_file():
        reads = [
            _normalize(line)
            for line in Path(reads_file).read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
    else:
        print(
            "[OK] docs_pack adherence: no reads log "
            "(set DOCS_READ_LOG or --reads-file to enable)"
        )
        return 0

    doc_reads = [
        r
        for r in reads
        if r.startswith("docs/") or r == "AGENTS.md" or r.endswith(".md")
    ]
    extras = sorted({r for r in doc_reads if r not in allowed and "docs/" in r})
    if not extras:
        print(f"[OK] docs_pack adherence — {len(doc_reads)} doc read(s) within pack")
        return 0

    print(f"[WARN] docs_pack adherence — {len(extras)} read(s) outside pack∪deferred:")
    for path in extras[:20]:
        print(f"  - {path}")
    if args.strict:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
