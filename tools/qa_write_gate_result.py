#!/usr/bin/env python3
"""Write structured QA gate result JSON (docs/ACCEPTANCE_CRITERIA.md)."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from qa_acceptance_lib import ROOT, gate_result, load_criteria  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="Write QA gate result artifact")
    ap.add_argument("--gate", required=True, help="Gate id from acceptance_criteria.json")
    ap.add_argument("--status", required=True, choices=["pass", "fail", "warn", "skip"])
    ap.add_argument("--message", default="")
    ap.add_argument("--metric", action="append", default=[], help="key=value measured metric")
    ap.add_argument("--evidence", action="append", default=[], help="Path to evidence artifact")
    ap.add_argument(
        "--out-dir",
        type=Path,
        default=ROOT / "artifacts" / "qa_reports",
    )
    args = ap.parse_args()

    criteria = load_criteria()
    if args.gate not in criteria.get("gates", {}) and not args.gate.endswith("_jury"):
        print(f"Unknown gate_id: {args.gate}", file=sys.stderr)
        return 2

    metrics: dict = {}
    for item in args.metric:
        if "=" in item:
            k, v = item.split("=", 1)
            metrics[k.strip()] = v.strip()

    result = gate_result(args.gate, args.status, metrics=metrics, evidence=args.evidence, message=args.message)
    result["timestamp"] = datetime.now(timezone.utc).isoformat()
    result["valid_pass"] = args.status == "pass"

    args.out_dir.mkdir(parents=True, exist_ok=True)
    out = args.out_dir / f"{args.gate}.json"
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Wrote {out}")
    print(f"  status={args.status} valid_pass={result['valid_pass']}")
    if args.message:
        print(f"  message={args.message}")
    return 0 if result["valid_pass"] or args.status in ("warn", "skip") else 1


if __name__ == "__main__":
    raise SystemExit(main())
