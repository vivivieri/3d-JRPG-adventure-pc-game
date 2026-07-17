#!/usr/bin/env python3
"""Validate game/data/qa/alignment_audit_catalog.json — L0_alignment_audit_catalog gate."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "game/data/qa/alignment_audit_catalog.json"


def main() -> int:
    if not CATALOG.is_file():
        print(f"MISSING: {CATALOG}")
        return 1
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    errors: list[str] = []

    for key in ("version", "authority", "domains", "recommendation_rules", "visual_packs", "outputs"):
        if key not in data:
            errors.append(f"missing key: {key}")

    domain_ids = {d["id"] for d in data.get("domains", [])}
    if "overall_production" not in domain_ids:
        errors.append("domains must include overall_production")

    rule_ids = [r["id"] for r in data.get("recommendation_rules", [])]
    if len(rule_ids) != len(set(rule_ids)):
        errors.append("duplicate recommendation_rules id")

    pack_ids = [p["id"] for p in data.get("visual_packs", [])]
    if len(pack_ids) != len(set(pack_ids)):
        errors.append("duplicate visual_packs id")

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
