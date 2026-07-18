#!/usr/bin/env python3
"""Compare challenger vs champion on golden harness — L2_candidate_select (pre-merge, non-ship).

Usage:
  python3 tools/compare_champion_challenger.py --challenger game/data/qa/examples/challenger_manifest_sample.json
  python3 tools/compare_champion_challenger.py --scope ruined_village --challenger artifacts/candidates/P1-02/challenger_run2.json --write

Authority: docs/qa/CANDIDATE_TOURNAMENT.md
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from candidate_tournament_lib import (  # noqa: E402
    compare_champion_challenger,
    load_json,
    write_comparison_artifact,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Champion vs challenger golden harness compare")
    parser.add_argument("--challenger", required=True, type=Path, help="Challenger manifest JSON")
    parser.add_argument("--scope", default="", help="Override scope_id in manifest")
    parser.add_argument("--write", action="store_true", help="Write comparison artifact under artifacts/candidates/")
    parser.add_argument("--json", action="store_true", help="Print full JSON to stdout")
    args = parser.parse_args()

    if not args.challenger.is_file():
        print(f"Challenger manifest not found: {args.challenger}", file=sys.stderr)
        return 2

    challenger = load_json(args.challenger)
    scope_id = args.scope or challenger.get("scope_id", "")
    if not scope_id:
        print("scope_id required in manifest or --scope", file=sys.stderr)
        return 2

    result = compare_champion_challenger(challenger, scope_id=scope_id)
    payload = result.to_dict()

    if args.write:
        issue_id = challenger.get("issue_id", "unknown")
        out_path = write_comparison_artifact(result, issue_id)
        payload["artifact_path"] = str(out_path.relative_to(ROOT))
        print(f"Wrote {payload['artifact_path']}")

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"scope={result.scope_id} issue={result.issue_id} verdict={result.verdict}")
        print(f"  promote_challenger={result.promote}")
        print(f"  hard_gates_pass={result.hard_gates.get('pass')}")
        print(f"  harness_pass={result.harness.get('pass')}")
        print(f"  challenger_soft={result.challenger_soft.get('soft_score')}")
        if result.champion_soft:
            print(f"  champion_soft={result.champion_soft.get('soft_score')}")
        for reason in result.reasons:
            print(f"  reason: {reason}")

    if not result.hard_gates.get("pass") or not result.harness.get("pass"):
        return 1
    return 0 if result.promote else 2


if __name__ == "__main__":
    raise SystemExit(main())
