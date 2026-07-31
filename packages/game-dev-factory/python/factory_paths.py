#!/usr/bin/env python3
"""Factory control-plane path resolution.

Portable seam for multi-agent game-dev factories. Defaults match this repo
(`game/data/qa`, `artifacts`). Override via env for other projects:

  FACTORY_ROOT          — repo root (default: parent of tools/)
  FACTORY_DATA_DIR      — relative or absolute QA/config dir (default: game/data/qa)
  FACTORY_ARTIFACTS_DIR — relative or absolute artifacts dir (default: artifacts)

Authority: packages/game-dev-factory/CONTROL_PLANE.md
"""
from __future__ import annotations

import os
from pathlib import Path

_DEFAULT_DATA = "game/data/qa"
_DEFAULT_ARTIFACTS = "artifacts"


def repo_root() -> Path:
    """Repository root. FACTORY_ROOT wins; else parent of tools/."""
    env = (os.environ.get("FACTORY_ROOT") or "").strip()
    if env:
        return Path(env).expanduser().resolve()
    return Path(__file__).resolve().parents[1]


def _resolve_under_root(raw: str, default_rel: str) -> Path:
    value = (raw or "").strip() or default_rel
    path = Path(value).expanduser()
    if path.is_absolute():
        return path.resolve()
    return (repo_root() / path).resolve()


def factory_data_dir() -> Path:
    """Committed factory JSON (board, phases, orchestrator steps, registry)."""
    return _resolve_under_root(os.environ.get("FACTORY_DATA_DIR", ""), _DEFAULT_DATA)


def factory_artifacts_dir() -> Path:
    """Ephemeral runtime outputs (orchestrator report, cycle log, halt state)."""
    return _resolve_under_root(
        os.environ.get("FACTORY_ARTIFACTS_DIR", ""), _DEFAULT_ARTIFACTS
    )


def qa_path(*parts: str) -> Path:
    return factory_data_dir().joinpath(*parts)


def artifact_path(*parts: str) -> Path:
    return factory_artifacts_dir().joinpath(*parts)


# Convenience aliases used by many PM modules (resolved at import time).
ROOT = repo_root()
BOARD_PATH = qa_path("sprint_board.json")
PHASES_PATH = qa_path("sprint_phases.json")
ORCHESTRATOR_STEPS_PATH = qa_path("pm_orchestrator_steps.json")
WATCHDOG_CONFIG_PATH = qa_path("factory_watchdog.json")
AUTOMATIONS_PATH = qa_path("factory_automations.json")
REGISTRY_PATH = qa_path("workflow_integration_registry.json")
HEALTH_SNAPSHOT_PATH = qa_path("factory_health_snapshot.json")
STAKEHOLDER_CONFIG_PATH = qa_path("stakeholder_report_config.json")
ESCALATION_POLICY_PATH = qa_path("escalation_policy.json")
ACCEPTANCE_CRITERIA_PATH = qa_path("acceptance_criteria.json")

ORCHESTRATOR_REPORT_PATH = artifact_path("pm_orchestrator_report.json")
DISPATCH_PACKET_PATH = artifact_path("pm_dispatch_packet.json")
FACTORY_STATE_PATH = artifact_path("factory_state.json")
CYCLE_LOG_PATH = artifact_path("factory_cycle_log.jsonl")
HEARTBEAT_PATH = artifact_path("factory_heartbeat.json")
HEALTH_REPORT_PATH = artifact_path("factory_health_report.json")


def refresh_aliases() -> None:
    """Rebind module-level path aliases after env changes (tests / smoke)."""
    global ROOT, BOARD_PATH, PHASES_PATH, ORCHESTRATOR_STEPS_PATH
    global WATCHDOG_CONFIG_PATH, AUTOMATIONS_PATH, REGISTRY_PATH
    global HEALTH_SNAPSHOT_PATH, STAKEHOLDER_CONFIG_PATH, ESCALATION_POLICY_PATH
    global ACCEPTANCE_CRITERIA_PATH
    global ORCHESTRATOR_REPORT_PATH, DISPATCH_PACKET_PATH, FACTORY_STATE_PATH
    global CYCLE_LOG_PATH, HEARTBEAT_PATH, HEALTH_REPORT_PATH

    ROOT = repo_root()
    BOARD_PATH = qa_path("sprint_board.json")
    PHASES_PATH = qa_path("sprint_phases.json")
    ORCHESTRATOR_STEPS_PATH = qa_path("pm_orchestrator_steps.json")
    WATCHDOG_CONFIG_PATH = qa_path("factory_watchdog.json")
    AUTOMATIONS_PATH = qa_path("factory_automations.json")
    REGISTRY_PATH = qa_path("workflow_integration_registry.json")
    HEALTH_SNAPSHOT_PATH = qa_path("factory_health_snapshot.json")
    STAKEHOLDER_CONFIG_PATH = qa_path("stakeholder_report_config.json")
    ESCALATION_POLICY_PATH = qa_path("escalation_policy.json")
    ACCEPTANCE_CRITERIA_PATH = qa_path("acceptance_criteria.json")
    ORCHESTRATOR_REPORT_PATH = artifact_path("pm_orchestrator_report.json")
    DISPATCH_PACKET_PATH = artifact_path("pm_dispatch_packet.json")
    FACTORY_STATE_PATH = artifact_path("factory_state.json")
    CYCLE_LOG_PATH = artifact_path("factory_cycle_log.jsonl")
    HEARTBEAT_PATH = artifact_path("factory_heartbeat.json")
    HEALTH_REPORT_PATH = artifact_path("factory_health_report.json")


def describe() -> dict[str, str]:
    return {
        "FACTORY_ROOT": str(repo_root()),
        "FACTORY_DATA_DIR": str(factory_data_dir()),
        "FACTORY_ARTIFACTS_DIR": str(factory_artifacts_dir()),
        "sprint_board": str(BOARD_PATH),
        "orchestrator_report": str(ORCHESTRATOR_REPORT_PATH),
    }


if __name__ == "__main__":
    import json

    print(json.dumps(describe(), indent=2))
