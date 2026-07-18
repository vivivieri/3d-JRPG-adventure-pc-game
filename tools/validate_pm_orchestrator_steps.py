#!/usr/bin/env python3
"""Validate game/data/qa/pm_orchestrator_steps.json — L0_pm_orchestrator gate.

The PM Agent's authoritative "what to do each session" (session_steps) and
"what to do after each agent cycle" (post_agent_steps). This gate guarantees the
PM's workflow is well-formed and every step points at a tool that actually exists —
so the PM knows exactly what to do and can't be handed a broken/dangling step.
See docs/agents/PM_AGENT_RUNBOOK.md, docs/agents/SPRINT_ORCHESTRATION.md.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "game/data/qa/pm_orchestrator_steps.json"

REQUIRED_TOP = ("version", "agent_role", "authority", "session_steps", "post_agent_steps")
TOOL_RE = re.compile(r"tools/[\w./-]+\.(?:py|sh)")


def _tool_refs_exist(command: str) -> list[str]:
    """Return missing tool paths referenced by a command (ignores <placeholder> args)."""
    missing = []
    for match in TOOL_RE.findall(command):
        if not (ROOT / match).is_file():
            missing.append(match)
    return missing


def main() -> int:
    if not CONFIG_PATH.is_file():
        print(f"Missing {CONFIG_PATH}", file=sys.stderr)
        return 1

    data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    errors: list[str] = []

    for key in REQUIRED_TOP:
        if key not in data:
            errors.append(f"missing top-level key: {key}")

    if data.get("agent_role") != "pm":
        errors.append(f"agent_role must be 'pm' (got {data.get('agent_role')!r})")

    session = data.get("session_steps", [])
    if not session:
        errors.append("session_steps must be non-empty")
    seen_ids: set[str] = set()
    seen_steps: set[int] = set()
    for s in session:
        sid = s.get("id")
        for field in ("step", "id", "description", "command", "block_on_fail"):
            if field not in s:
                errors.append(f"session step {sid or s.get('step')} missing '{field}'")
        if not isinstance(s.get("block_on_fail"), bool):
            errors.append(f"session step {sid}: block_on_fail must be boolean")
        if sid in seen_ids:
            errors.append(f"duplicate session step id: {sid}")
        seen_ids.add(sid)
        if s.get("step") in seen_steps:
            errors.append(f"duplicate session step number: {s.get('step')}")
        seen_steps.add(s.get("step"))
        for miss in _tool_refs_exist(s.get("command", "")):
            errors.append(f"session step {sid}: command references missing tool '{miss}'")

    # A blocking dispatch step must exist — the core PM action.
    if session and not any(s.get("id") == "dispatch_orchestrator" for s in session):
        errors.append("session_steps missing required 'dispatch_orchestrator' step")

    REQUIRED_POST_AGENT_IDS = (
        "check_done_criteria",
        "bundle_evidence",
        "check_feature_integration",
        "re_run_orchestrator",
    )
    post_ids = {p.get("id") for p in data.get("post_agent_steps", [])}
    for rid in REQUIRED_POST_AGENT_IDS:
        if rid not in post_ids:
            errors.append(f"post_agent_steps missing required step: {rid}")

    post = data.get("post_agent_steps", [])
    if not post:
        errors.append("post_agent_steps must be non-empty")
    for p in post:
        pid = p.get("id")
        for field in ("id", "description", "command", "required"):
            if field not in p:
                errors.append(f"post_agent step {pid} missing '{field}'")
        for miss in _tool_refs_exist(p.get("command", "")):
            errors.append(f"post_agent step {pid}: command references missing tool '{miss}'")

    if errors:
        print("pm_orchestrator_steps.json validation FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"pm_orchestrator_steps.json: OK ({len(session)} session steps, {len(post)} post-agent steps)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
