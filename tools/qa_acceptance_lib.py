#!/usr/bin/env python3
"""Shared acceptance criteria enforcement for QA gates (docs/ACCEPTANCE_CRITERIA.md)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CRITERIA_PATH = ROOT / "game/data/qa/acceptance_criteria.json"


def load_criteria() -> dict:
    return json.loads(CRITERIA_PATH.read_text(encoding="utf-8"))


def jury_rules(domain: str, criteria: dict | None = None) -> dict:
    criteria = criteria or load_criteria()
    rules = criteria.get("jury", {}).get(domain)
    if not rules:
        raise KeyError(f"Unknown jury domain: {domain}")
    return rules


def _criterion_ok(parsed: dict, key: str, expect: Any) -> bool:
    val = parsed.get(key)
    if isinstance(expect, bool):
        return val is expect or val == expect
    return bool(val) == bool(expect)


def normalize_jury_review(parsed: dict, domain: str, criteria: dict | None = None) -> dict:
    """Recompute overall_pass from measurable criteria — do not trust model self-report alone."""
    rules = jury_rules(domain, criteria)
    conf_min = float(rules.get("min_confidence", criteria["global_rules"]["jury_min_confidence"]))
    conf = float(parsed.get("confidence", 0) or 0)

    criteria_results: dict[str, bool] = {}
    for key, spec in rules.get("criteria", {}).items():
        criteria_results[key] = _criterion_ok(parsed, key, spec.get("expect"))

    all_criteria_met = all(criteria_results.values())
    confidence_ok = conf >= conf_min
    overall = all_criteria_met and confidence_ok and not parsed.get("error")

    if not overall:
        issues = list(parsed.get("issues") or [])
        failed = [k for k, ok in criteria_results.items() if not ok]
        if failed:
            msg = f"Failed criteria: {', '.join(failed)}"
            if msg not in issues:
                issues.append(msg)
        if not confidence_ok:
            msg = f"Confidence {conf:.2f} < minimum {conf_min:.2f}"
            if msg not in issues:
                issues.append(msg)
        parsed["issues"] = issues[:8]

    parsed["overall_pass"] = overall
    parsed["acceptance"] = {
        "gate_id": rules.get("gate_id"),
        "criteria_results": criteria_results,
        "all_criteria_met": all_criteria_met,
        "confidence": conf,
        "confidence_min": conf_min,
        "confidence_ok": confidence_ok,
        "valid_pass": overall,
    }
    return parsed


def evaluate_jury_consensus(report: dict, domain: str, criteria: dict | None = None) -> dict:
    criteria = criteria or load_criteria()
    rules = jury_rules(domain, criteria)
    global_rules = criteria["global_rules"]
    min_pass = int(rules.get("min_pass_models", global_rules["jury_min_pass_models"]))
    min_active = int(rules.get("min_active_models", global_rules["jury_min_active_models"]))

    reviews = report.get("reviews", [])
    active = 0
    passed = 0
    for rev in reviews:
        if rev.get("skipped") or rev.get("error"):
            continue
        active += 1
        acceptance = rev.get("acceptance", {})
        if acceptance.get("valid_pass") is True:
            passed += 1
        elif acceptance and acceptance.get("valid_pass") is False:
            continue
        elif rev.get("overall_pass"):
            # Legacy reports without acceptance block — do not count as pass
            continue

    consensus = active >= min_active and passed >= min_pass
    return {
        "gate_id": rules.get("gate_id"),
        "min_pass_models": min_pass,
        "min_active_models": min_active,
        "active_models": active,
        "passed_models": passed,
        "consensus_pass": consensus,
        "valid_pass": consensus,
        "skip_is_not_pass": global_rules.get("skip_is_not_pass", True),
    }


def gate_result(
    gate_id: str,
    status: str,
    metrics: dict | None = None,
    evidence: list[str] | None = None,
    message: str = "",
) -> dict:
    criteria = load_criteria()
    gate = criteria.get("gates", {}).get(gate_id, {})
    return {
        "gate_id": gate_id,
        "layer": gate.get("layer"),
        "domain": gate.get("domain"),
        "status": status,
        "valid_pass": status == "pass",
        "metrics": metrics or {},
        "evidence": evidence or [],
        "message": message,
        "design_ref": gate.get("design_ref"),
    }
