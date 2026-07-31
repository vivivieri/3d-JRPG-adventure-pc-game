---
id: prereqs-order
type: how-to
audience: [architect, builder]
phase: [1]
status: active
authority: engineering
tokens_est: 334
summary: "git checkout game/development"
---
# Phase 1 Visuals Regen — Prereqs + order

**Hub:** [`phase1_visuals.md`](../phase1_visuals.md)

### 10.1 Prerequisites

```bash
git checkout game/development
git merge main
bash tools/run_agent_session_gate.sh architect P1-01
bash tools/regenerate_phase1_visuals.sh --check
bash tools/ensure_mcp_stack.sh    # required before P1-02 scene work
```


### 10.2 Regeneration order (mandatory)

| Step | Artifact | Source on `main` | Output on `game/development` |
|------|----------|------------------|------------------------------|
| 1 | Toon shader | `shader_registry.json` + `tools/godot_templates/shaders/toon_base.gdshader` | `game/shaders/toon_base.gdshader` |
| 2 | Zone visuals script | `base_classes.json` + `tools/zone_visuals_lib.py` | `game/scripts/exploration/zone_visuals.gd` |
| 3 | Env preset (optional) | `environment_registry.json` | `game/environments/ruined_village.tres` |
| 4 | Unit tests | `unit_test_specs.json` | `game/tests/unit/test_zone_visuals.gd` |

**Why this order:** shader is dependency-free; `zone_visuals.gd` reads palette JSON; `.tres` is optional when runtime `build_environment()` is used; tests require the GDScript class.
