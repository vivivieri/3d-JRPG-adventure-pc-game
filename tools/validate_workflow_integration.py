#!/usr/bin/env python3
"""Validate factory workflow integration registry — L0_workflow_integration gate.

Ensures registered features have required script hooks, doc cross-refs, secrets,
and orchestrator steps wired. Prevents new features from landing out of sync.

Authority: docs/qa/WORKFLOW_INTEGRATION.md
Registry: game/data/qa/workflow_integration_registry.json
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "game/data/qa/workflow_integration_registry.json"
ORCH_STEPS_PATH = ROOT / "game/data/qa/pm_orchestrator_steps.json"
CYCLE_EVENTS_PATH = ROOT / "game/data/qa/agent_cycle_events.json"
SECRETS_CHECK_PATH = ROOT / "tools/check_day_one_secrets.sh"
RUNNER_PATH = ROOT / "tools/run_docs_ci_checks.sh"
CRITERIA_PATH = ROOT / "game/data/qa/acceptance_criteria.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")


def secrets_from_check_script() -> set[str]:
    text = read_text(SECRETS_CHECK_PATH)
    m = re.search(r"REQUIRED=\(\s*(.*?)\s*\)", text, re.DOTALL)
    if not m:
        return set()
    block = m.group(1)
    return set(re.findall(r"^\s*([A-Z][A-Z0-9_]*)\s*$", block, re.MULTILINE))


def validate_feature(feature: dict, errors: list[str]) -> None:
    fid = feature.get("id", "?")

    authority = feature.get("authority_doc")
    if authority:
        path = ROOT / authority
        if not path.is_file():
            errors.append(f"{fid}: missing authority doc {authority}")

    schema = feature.get("schema")
    if schema and not (ROOT / schema).is_file():
        errors.append(f"{fid}: missing schema {schema}")

    for secret in feature.get("required_secrets", []):
        if secret not in secrets_from_check_script():
            errors.append(
                f"{fid}: secret {secret} not in tools/check_day_one_secrets.sh REQUIRED list"
            )

    for hook in feature.get("script_hooks", []):
        rel = hook.get("path", "")
        needle = hook.get("contains", "")
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"{fid}: missing hook script {rel}")
            continue
        content = read_text(path)
        if needle and needle not in content:
            errors.append(
                f"{fid}: {rel} missing hook '{needle}' ({hook.get('purpose', '')})"
            )

    orch_data = load_json(ORCH_STEPS_PATH) if ORCH_STEPS_PATH.is_file() else {}
    steps = {s.get("id"): s for s in orch_data.get("session_steps", [])}
    for step in feature.get("orchestrator_steps", []):
        sid = step.get("id")
        needle = step.get("command_contains", "")
        row = steps.get(sid)
        if not row:
            errors.append(f"{fid}: orchestrator step missing: {sid}")
            continue
        cmd = row.get("command", "")
        if needle and needle not in cmd:
            errors.append(f"{fid}: orchestrator step {sid} command missing '{needle}'")

    for ref in feature.get("required_doc_refs", []):
        doc = ref.get("doc", "")
        mention = ref.get("must_mention", "")
        path = ROOT / doc
        if not path.is_file():
            errors.append(f"{fid}: required doc missing {doc}")
            continue
        if mention and mention not in read_text(path):
            errors.append(f"{fid}: {doc} must mention '{mention}'")

    cycle = feature.get("cycle_events")
    if cycle and CYCLE_EVENTS_PATH.is_file():
        events = load_json(CYCLE_EVENTS_PATH)
        key = cycle.get("telemetry_side_effects_key", "telemetry_side_effects")
        side = events.get(key)
        if not side:
            errors.append(f"{fid}: agent_cycle_events.json missing '{key}'")
        else:
            blob = json.dumps(side)
            for needle in cycle.get("must_mention_hooks", []):
                if needle not in blob:
                    errors.append(
                        f"{fid}: agent_cycle_events.json {key} missing hook '{needle}'"
                    )

    gate = feature.get("acceptance_gate")
    if gate:
        crit = load_json(CRITERIA_PATH)
        gates = crit.get("gates", {})
        docs_ci = crit.get("docs_ci_gates", {}).get("required_gates", [])
        if gate not in gates:
            errors.append(f"{fid}: acceptance gate {gate} not in acceptance_criteria.json")
        if gate not in docs_ci:
            errors.append(f"{fid}: acceptance gate {gate} not in docs_ci_gates.required_gates")
        runner = read_text(RUNNER_PATH)
        if f'run_gate "{gate}"' not in runner:
            errors.append(f"{fid}: runner missing run_gate for {gate}")


def main() -> int:
    if not REGISTRY_PATH.is_file():
        print(f"MISSING: {REGISTRY_PATH}")
        return 1

    registry = load_json(REGISTRY_PATH)
    errors: list[str] = []

    for key in ("version", "authority", "policy", "features"):
        if key not in registry:
            errors.append(f"registry missing key: {key}")

    feature_ids = [f.get("id") for f in registry.get("features", [])]
    if len(feature_ids) != len(set(feature_ids)):
        errors.append("duplicate feature id in registry")

    for feature in registry.get("features", []):
        validate_feature(feature, errors)

    if errors:
        print("workflow integration FAILED:")
        for err in errors:
            print(f"  - {err}")
        print()
        print("Fix: docs/qa/WORKFLOW_INTEGRATION.md — register hooks + doc refs before merge.")
        return 1

    n = len(registry.get("features", []))
    print(f"workflow integration: OK ({n} registered feature(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
