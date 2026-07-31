#!/usr/bin/env python3
"""Map agent_owner + docs_task → docs INDEX role (shared by gate / preflight / resolve)."""
from __future__ import annotations

# When agent_owner is the left key and docs_task matches, prefer the specialty role.
TASK_ROLE_REMAP: dict[str, dict[str, str]] = {
    "zone_lighting": {"builder": "builder_zone", "architect": "architect"},
    "level_layout": {"builder": "builder_zone"},
    "water_shader": {"builder": "builder_zone"},
    "combat_balance": {"builder": "builder_combat"},
    "model_qa": {"builder": "visual"},
    "visual_qa": {"builder": "visual", "architect": "visual"},  # QA keeps qa; task pack adds visual docs
    "audio_bgm": {"builder": "audio"},
    "ui_cinematics": {"builder": "builder"},
    # CI / acceptance work uses the QA pack — not the full architect style stack.
    "acceptance_ci": {"builder": "qa", "architect": "qa"},
}

KNOWN_ROLES = frozenset(
    {
        "pm",
        "architect",
        "qa",
        "flow",
        "builder",
        "builder_zone",
        "builder_combat",
        "visual",
        "release",
        "narrative",
        "audio",
    }
)


def remap_docs_role(agent: str, task_id: str | None) -> str:
    """Return INDEX role id for session gate / preflight."""
    role = (agent or "builder").replace("agent/", "").strip()
    if role not in KNOWN_ROLES:
        role = "builder"
    if role in {"builder_zone", "builder_combat"}:
        return role
    if not task_id:
        return role
    mapped = TASK_ROLE_REMAP.get(task_id, {}).get(role)
    return mapped if mapped in KNOWN_ROLES else role


if __name__ == "__main__":
    import sys

    ag = sys.argv[1] if len(sys.argv) > 1 else "builder"
    task = sys.argv[2] if len(sys.argv) > 2 else None
    print(remap_docs_role(ag, task))
