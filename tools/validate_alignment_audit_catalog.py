#!/usr/bin/env python3
"""Validate game/data/qa/alignment_audit_catalog.json — L0_alignment_audit_catalog gate."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "game/data/qa/alignment_audit_catalog.json"
CRITERIA = ROOT / "game/data/qa/acceptance_criteria.json"
WEIGHT_TOLERANCE = 0.02


def main() -> int:
    if not CATALOG.is_file():
        print(f"MISSING: {CATALOG}")
        return 1
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    errors: list[str] = []

    for key in ("version", "authority", "domains", "streams", "recommendation_rules", "visual_packs", "outputs"):
        if key not in data:
            errors.append(f"missing key: {key}")

    domain_ids = {d["id"] for d in data.get("domains", [])}
    if "overall_production" not in domain_ids:
        errors.append("domains must include overall_production (legacy alias)")

    streams = data.get("streams", {})
    if "spec_readiness" not in streams or "build_readiness" not in streams:
        errors.append("streams must include spec_readiness and build_readiness")

    for stream_id, stream in streams.items():
        for dom_id in stream.get("domains", []):
            if dom_id not in domain_ids:
                errors.append(f"stream {stream_id}: unknown domain '{dom_id}'")
        primary = stream.get("primary_on_branches", [])
        na = stream.get("not_applicable_on_branches", [])
        if set(primary) & set(na):
            errors.append(f"stream {stream_id}: branch in both primary and not_applicable")

    rule_ids = [r["id"] for r in data.get("recommendation_rules", [])]
    if len(rule_ids) != len(set(rule_ids)):
        errors.append("duplicate recommendation_rules id")

    pack_ids = [p["id"] for p in data.get("visual_packs", [])]
    if len(pack_ids) != len(set(pack_ids)):
        errors.append("duplicate visual_packs id")

    known_gates: set[str] = set()
    if CRITERIA.is_file():
        crit = json.loads(CRITERIA.read_text(encoding="utf-8"))
        known_gates = set(crit.get("gates", {}))
        known_gates.update({"L0_acceptance_catalog", "L0_environments_catalog", "L0_sprint_phases"})

    for domain in data.get("domains", []):
        if domain.get("derive"):
            continue
        signals = domain.get("signals", [])
        total_w = sum(float(s.get("weight", 0)) for s in signals)
        if abs(total_w - 1.0) > WEIGHT_TOLERANCE:
            errors.append(
                f"domain {domain.get('id')}: signal weights sum to {total_w:.3f} (expected ~1.0)"
            )
        for sig in signals:
            kind = sig.get("kind", "")
            if kind not in {"gate", "gate_optional"}:
                continue
            gate_id = sig.get("id", "")
            if known_gates and gate_id not in known_gates:
                errors.append(f"domain {domain.get('id')}: unknown gate signal '{gate_id}'")

    for rule in data.get("recommendation_rules", []):
        if rule.get("when") != "gate_fail":
            continue
        gate_id = rule.get("gate", "")
        if known_gates and gate_id not in known_gates:
            errors.append(f"recommendation {rule.get('id')}: unknown gate '{gate_id}'")

    lib = ROOT / "tools/alignment_audit_lib.py"
    if not lib.is_file():
        errors.append("missing tools/alignment_audit_lib.py")

    runner = ROOT / "tools/run_alignment_audit.sh"
    if not runner.is_file():
        errors.append("missing tools/run_alignment_audit.sh")

    if errors:
        print("alignment_audit_catalog.json FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1

    n_domains = len(data.get("domains", []))
    n_rules = len(data.get("recommendation_rules", []))
    n_packs = len(data.get("visual_packs", []))
    n_assets = sum(len(p.get("assets", [])) for p in data.get("visual_packs", []))
    print(
        f"OK — {n_domains} domains, {n_rules} recommendation rules, "
        f"{n_packs} visual packs ({n_assets} assets)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
