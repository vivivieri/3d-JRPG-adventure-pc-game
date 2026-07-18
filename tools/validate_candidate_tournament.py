#!/usr/bin/env python3
"""Validate candidate tournament config — L0_candidate_tournament gate.

Schemas:
  game/data/qa/golden_harness.json
  game/data/qa/evaluation_rubrics.json
  game/data/qa/candidate_tournament_policy.json

Authority: docs/qa/CANDIDATE_TOURNAMENT.md
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HARNESS_PATH = ROOT / "game/data/qa/golden_harness.json"
RUBRICS_PATH = ROOT / "game/data/qa/evaluation_rubrics.json"
POLICY_PATH = ROOT / "game/data/qa/candidate_tournament_policy.json"
ZONE_PATH = ROOT / "game/data/qa/zone_composition.json"
CRITERIA_PATH = ROOT / "game/data/qa/acceptance_criteria.json"
COMPARE_PATH = ROOT / "tools/compare_champion_challenger.py"
RUN_PATH = ROOT / "tools/run_candidate_tournament.sh"
LIB_PATH = ROOT / "tools/candidate_tournament_lib.py"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []

    for path in (HARNESS_PATH, RUBRICS_PATH, POLICY_PATH):
        if not path.is_file():
            errors.append(f"missing {path.relative_to(ROOT)}")

    for path in (COMPARE_PATH, RUN_PATH, LIB_PATH):
        if not path.is_file():
            errors.append(f"missing tool {path.relative_to(ROOT)}")

    if errors:
        for e in errors:
            print(f"  - {e}")
        return 1

    harness = load_json(HARNESS_PATH)
    rubrics = load_json(RUBRICS_PATH)
    policy = load_json(POLICY_PATH)
    zones = load_json(ZONE_PATH).get("zones", {}) if ZONE_PATH.is_file() else {}
    criteria = load_json(CRITERIA_PATH)
    jury = criteria.get("jury", {})

    if policy.get("ship_blocking") is not False:
        errors.append("candidate_tournament_policy.ship_blocking must be false")

    if policy.get("layer") != "L2.5":
        errors.append("candidate_tournament_policy.layer must be L2.5")

    gate_id = policy.get("gate_id")
    if gate_id not in criteria.get("gates", {}):
        errors.append(f"policy gate_id {gate_id} missing from acceptance_criteria.json gates")

    for scope_id, scope in harness.get("scopes", {}).items():
        zid = scope.get("zone_composition_id")
        if zid not in zones:
            errors.append(f"golden_harness scope {scope_id} unknown zone_composition_id {zid}")
        for cap in scope.get("captures", []):
            if not cap.get("id"):
                errors.append(f"{scope_id}: capture missing id")
        for gid in scope.get("hard_gates", []):
            jury_gate_ids = {v.get("gate_id") for v in jury.values() if isinstance(v, dict) and v.get("gate_id")}
            if gid not in criteria.get("gates", {}) and gid not in jury_gate_ids:
                errors.append(f"{scope_id}: hard_gate {gid} not in acceptance catalog")

    weights = sum(float(a.get("weight", 0)) for a in rubrics.get("axes", []))
    if abs(weights - 1.0) > 0.05:
        errors.append(f"evaluation_rubrics axis weights sum to {weights:.2f} (expected ~1.0)")

    for axis in rubrics.get("axes", []):
        jury_map = axis.get("jury_criteria") or {}
        for domain, crits in jury_map.items():
            if domain not in jury:
                errors.append(f"rubric {axis.get('id')}: unknown jury domain {domain}")
                continue
            known = set((jury[domain].get("criteria") or {}).keys())
            for crit in crits:
                if crit not in known:
                    errors.append(f"rubric {axis.get('id')}: unknown criterion {crit} in {domain}")

    # Smoke: sample challenger compare must execute (may SKIP captures on main)
    sample = ROOT / "game/data/qa/examples/challenger_manifest_sample.json"
    if sample.is_file():
        import subprocess

        proc = subprocess.run(
            [sys.executable, str(COMPARE_PATH), "--challenger", str(sample)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if proc.returncode not in (0, 1, 2):
            errors.append(f"compare_champion_challenger sample smoke failed: rc={proc.returncode}")

    if errors:
        print("candidate_tournament validation FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1

    n_scopes = len(harness.get("scopes", {}))
    n_axes = len(rubrics.get("axes", []))
    print(
        f"candidate_tournament: OK ({n_scopes} harness scope(s), {n_axes} rubric axes, gate={gate_id})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
