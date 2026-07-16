#!/usr/bin/env python3
"""Validate game/data/qa/escalation_policy.json — L0_escalation_policy gate.

Guarantees the anti-infinite-loop escalation ladder is well-formed:
dev<->QA (capped) -> arbitration (Architect / Design Authority) -> Product Owner.
See docs/qa/ESCALATION_POLICY.md.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "game/data/qa/escalation_policy.json"

REQUIRED_TOP = ("version", "authority", "ladder", "decision_record")
REQUIRED_TIERS = ("dev_qa_loop", "arbitration", "product_owner")


def main() -> int:
    if not CONFIG_PATH.is_file():
        print(f"Missing {CONFIG_PATH}", file=sys.stderr)
        return 1

    data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    errors: list[str] = []

    for key in REQUIRED_TOP:
        if key not in data:
            errors.append(f"missing top-level key: {key}")

    ladder = {t.get("id"): t for t in data.get("ladder", [])}
    for tid in REQUIRED_TIERS:
        if tid not in ladder:
            errors.append(f"ladder missing required tier: {tid}")

    # Tier 1: dev<->QA loop must be capped and escalate on exceed.
    dq = ladder.get("dev_qa_loop", {})
    max_reopens = dq.get("cap", {}).get("max_reopens")
    if not isinstance(max_reopens, int) or max_reopens < 1:
        errors.append("dev_qa_loop.cap.max_reopens must be a positive integer")
    if not str(dq.get("on_cap_exceeded", "")).startswith("escalate:"):
        errors.append("dev_qa_loop.on_cap_exceeded must escalate (e.g. 'escalate:arbitration')")

    # Tier 2: arbitration must classify root cause and resolve each class, and escalate up on exceed.
    arb = ladder.get("arbitration", {})
    classes = arb.get("classify_root_cause", [])
    if not classes:
        errors.append("arbitration.classify_root_cause must be non-empty")
    resolutions = arb.get("resolutions", {})
    for c in classes:
        if c not in resolutions:
            errors.append(f"arbitration.resolutions missing class '{c}'")
    if not str(arb.get("on_cap_exceeded", "")).startswith("escalate:product_owner"):
        errors.append("arbitration.on_cap_exceeded must escalate to product_owner")
    if arb.get("owner") != "architect":
        errors.append("arbitration.owner must be 'architect' (Design Authority / SA)")

    # Tier 3: Product Owner terminal tier with a real channel + decision types.
    po = ladder.get("product_owner", {})
    if po.get("owner") != "human":
        errors.append("product_owner.owner must be 'human'")
    if not po.get("channel"):
        errors.append("product_owner.channel required (e.g. 'telegram')")
    if not po.get("decision_types"):
        errors.append("product_owner.decision_types must be non-empty")

    # Decision record schema.
    dr = data.get("decision_record", {})
    for f in ("issue_id", "root_cause_class", "decision", "decided_by"):
        if f not in dr.get("required_fields", []):
            errors.append(f"decision_record.required_fields must include '{f}'")

    if errors:
        print("escalation_policy.json validation FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"escalation_policy.json: OK ({len(ladder)} tiers, dev_qa max_reopens={max_reopens})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
