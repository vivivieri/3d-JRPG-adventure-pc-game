#!/usr/bin/env python3
"""Validate factory automation catalog — L0_factory_automations gate.

Authority: docs/ops/agents/FACTORY_SETUP_GUIDE.md
Catalog: game/data/qa/factory_automations.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "game/data/qa/factory_automations.json"
ORCH_PATH = ROOT / "game/data/qa/pm_orchestrator_steps.json"
REGISTRY_PATH = ROOT / "game/data/qa/workflow_integration_registry.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    if not CATALOG_PATH.is_file():
        print(f"FAIL: missing {CATALOG_PATH}", file=sys.stderr)
        return 1

    catalog = load_json(CATALOG_PATH)
    automations = catalog.get("automations", [])
    if not automations:
        errors.append("automations list empty")

    for rid in ("automation_a_pm", "automation_b_ci_triage", "automation_d_factory_alert", "automation_e_worker"):
        if rid not in {a.get("id") for a in automations}:
            errors.append(f"missing required automation id: {rid}")

    for auto in automations:
        aid = auto.get("id", "?")
        prompt = auto.get("prompt_file")
        if prompt:
            path = ROOT / prompt
            if not path.is_file():
                errors.append(f"{aid}: missing prompt file {prompt}")
        trigger = auto.get("trigger", {})
        if trigger.get("type") == "webhook" and auto.get("required"):
            secret = trigger.get("secret")
            auth_secret = trigger.get("auth_secret")
            allowed = (
                "CURSOR_PM_CYCLE_WEBHOOK_URL",
                "CURSOR_PM_WEBHOOK_AUTH",
                "CURSOR_FACTORY_ALERT_WEBHOOK_URL",
                "CURSOR_ALERT_WEBHOOK_AUTH",
                "CURSOR_WORKER_WEBHOOK_URL",
                "CURSOR_WORKER_WEBHOOK_AUTH",
            )
            if secret and secret not in allowed:
                errors.append(f"{aid}: unexpected webhook secret {secret}")
            if secret and not auth_secret:
                errors.append(f"{aid}: webhook missing auth_secret (Generate auth header in dashboard)")
            if auth_secret and auth_secret not in allowed:
                errors.append(f"{aid}: unexpected auth_secret {auth_secret}")

    env_json = ROOT / ".cursor/environment.json"
    if env_json.is_file():
        env = load_json(env_json)
        ship_branch = (ROOT / "game/project.godot").is_file()
        if ship_branch:
            if not env.get("snapshot"):
                errors.append(".cursor/environment.json missing snapshot field on game/development")
            if "install_cloud_dev.sh" not in str(env.get("install", "")):
                errors.append(".cursor/environment.json install should reference install_cloud_dev.sh")
        elif "install_main_ci.sh" not in str(env.get("install", "")) and "bootstrap_cloud_environment.sh" not in str(
            env.get("install", "")
        ):
            errors.append(".cursor/environment.json on main should reference install_main_ci.sh or bootstrap_cloud_environment.sh")
    else:
        errors.append("missing .cursor/environment.json")

    dispatch_cmd = catalog.get("dispatch", {}).get("command", "")
    if "pm_dispatch_workers" not in dispatch_cmd:
        errors.append("dispatch.command must reference pm_dispatch_workers")

    if ORCH_PATH.is_file():
        steps = load_json(ORCH_PATH).get("session_steps", [])
        ids = [s.get("id") for s in steps]
        if "dispatch_workers" not in ids:
            errors.append("pm_orchestrator_steps.json missing dispatch_workers step")
    else:
        errors.append("missing pm_orchestrator_steps.json")

    workflows = [
        ".github/workflows/agent-cycle-pm.yml",
        ".github/workflows/game-ci-failure-triage.yml",
        ".github/workflows/factory-watchdog.yml",
        ".github/workflows/worker-dispatch.yml",
    ]
    for wf in workflows:
        if not (ROOT / wf).is_file():
            errors.append(f"missing workflow {wf}")

    script_paths = [
        "tools/pm_dispatch_workers.py",
        "tools/check_snapshot_boot.sh",
        "tools/run_pm_orchestrator.sh",
        "tools/run_post_agent_cycle.sh",
        "tools/curl_cursor_webhook.sh",
        "tools/setup_github_actions_secrets.sh",
    ]
    for sp in script_paths:
        if not (ROOT / sp).is_file():
            errors.append(f"missing script {sp}")

    registry = load_json(REGISTRY_PATH) if REGISTRY_PATH.is_file() else {}
    feature_ids = {f.get("id") for f in registry.get("features", [])}
    if "factory_automation_catalog" not in feature_ids:
        errors.append("workflow_integration_registry missing factory_automation_catalog feature")

    if errors:
        print("L0_factory_automations: FAIL", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"L0_factory_automations: PASS ({len(automations)} automations cataloged)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
