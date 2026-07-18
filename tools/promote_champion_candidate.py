#!/usr/bin/env python3
"""Promote challenger to champion registry after L2_candidate_select PASS.

Usage:
  python3 tools/promote_champion_candidate.py --comparison artifacts/candidates/P1-02/comparison_*.json

Authority: docs/qa/CANDIDATE_TOURNAMENT.md
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from candidate_tournament_lib import load_json, load_registry, utc_now_iso  # noqa: E402

REGISTRY_PATH = ROOT / "artifacts/candidates/champion_registry.json"


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote challenger to champion registry")
    parser.add_argument("--comparison", required=True, type=Path, help="Comparison artifact from compare_champion_challenger.py")
    parser.add_argument("--challenger", type=Path, help="Challenger manifest (if not embedded in comparison)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not args.comparison.is_file():
        print(f"Comparison not found: {args.comparison}", file=sys.stderr)
        return 2

    comparison = load_json(args.comparison)
    if not comparison.get("promote_challenger"):
        print(f"REFUSE: verdict={comparison.get('verdict')} — cannot promote", file=sys.stderr)
        return 1

    scope_id = comparison.get("scope_id", "")
    issue_id = comparison.get("issue_id", "")
    challenger_summary = comparison.get("challenger") or {}

    challenger_manifest: dict = {}
    if args.challenger and args.challenger.is_file():
        challenger_manifest = load_json(args.challenger)
    else:
        sample = ROOT / "artifacts/candidates" / issue_id
        if sample.is_dir():
            for path in sorted(sample.glob("challenger_*.json")):
                challenger_manifest = load_json(path)
                break

    registry = load_registry(REGISTRY_PATH)
    champions = registry.setdefault("champions", {})
    champions[scope_id] = {
        "scope_id": scope_id,
        "issue_id": issue_id,
        "commit_sha": challenger_manifest.get("commit_sha") or challenger_summary.get("commit_sha"),
        "promoted_at": utc_now_iso(),
        "comparison_artifact": str(args.comparison.relative_to(ROOT)),
        "challenger_label": challenger_manifest.get("label") or challenger_summary.get("label"),
        "captures": challenger_manifest.get("captures") or {},
        "gates": challenger_manifest.get("gates") or comparison.get("hard_gates", {}).get("results", {}),
        "soft_score": (comparison.get("soft_scores") or {}).get("challenger", {}).get("soft_score"),
    }
    registry["version"] = "1.0"
    registry["updated_at"] = utc_now_iso()

    if args.dry_run:
        print(json.dumps(registry, indent=2))
        return 0

    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY_PATH.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"OK — champion promoted for scope={scope_id} → {REGISTRY_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
