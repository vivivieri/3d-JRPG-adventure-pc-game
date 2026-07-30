---
id: ai-dev-workflow
type: how-to
audience: [pm, architect]
status: active
authority: workflow
tokens_est: 1322
---
# AI Dev Workflow — Build, Test & Acceptance Criteria

**Version:** 1.3
**Applies to:** `main` clean baseline → Phases 1–8 rebuild
**Cross-refs:** `.cursorrules` §0, `AGENTS.md`, `docs/engineering/technical/CODE_BASE_CLASS_RULES.md`, `docs/ops/agents/GDAI_CLOUD_SETUP.md`, `docs/ops/qa/AI_TESTING_SPEC.md`, `docs/ops/workflow/IMPLEMENTATION_PLAN.md`, `docs/ops/qa/QA_AND_BUG_PROCESS.md`

This document is the **single source of truth** for:

1. **AI build policy** — how Cursor agents implement the game
2. **AI testing policy** — what agents must verify automatically vs manually (`docs/ops/qa/AI_TESTING_SPEC.md` for L3–L5 detail)
3. **Unit tests** — headless GDScript tests for logic and data
4. **Acceptance criteria** — measurable phase gates (`docs/ops/qa/ACCEPTANCE_CRITERIA.md`, `game/data/qa/acceptance_criteria.json`)

---
## 1. AI build policy

### 1.1 Mandatory toolchain

| Tool | Role | Allowed outputs |
|------|------|-----------------|
| **GodotPrompter** (Cursor) | Plan, architect, write GDScript, shaders, test scripts | `.gd`, `.gdshader`, Python tools, docs |
| **GDAI MCP** (`godot-mcp`) | All editor work | `.tscn`, nodes, materials, lights, inspector values, F5 playtest |

**Rule:** No hand-edited `.tscn` or inspector-only work in Cursor. If GDAI MCP is unavailable → **stop and notify the user**. Do not fall back to manual scene edits.

**Enforcement:** `bash tools/check_rr_compliance.sh` (L0 gate) — fails CI/smoke if ship `.tscn` is committed without `game/scenes/.gdai_built`. `bash tools/check_mcp_ready.sh` — agents run before scene work.

### 1.1b Code base classes (extend-only)

Gameplay controllers and interactables **extend Architect-owned base classes** — do not create new `CharacterBody3D` stacks from scratch.

| Base class | Path | Builder uses via |
|------------|------|------------------|
| `PlayerController` | `game/scripts/exploration/player_controller.gd` | `player.tscn` component scene |
| `Combatant` | `game/scripts/combat/combatant.gd` | Enemy/party prefabs |
| `Interactable` | `game/scripts/exploration/interactable.gd` | `interactable_*.tscn` catalog |
| `SavePoint` | `game/scripts/exploration/save_point.gd` | `save_point.tscn` component |

**Authority:** `docs/engineering/technical/CODE_BASE_CLASS_RULES.md` · `game/data/code/base_classes.json` · component scenes in `docs/design/world/LEVEL_DESIGN.md` §1b.

**CI:** `L0_base_classes` (registry schema) · `L0_base_class_compliance` (no rogue controllers) · `L1_gdscript_lint` (changed `.gd` files).

### 1.2 Session startup (every agent run)

```bash
bash tools/ensure_mcp_stack.sh   # full stack — wraps ensure_gdai_mcp.sh
```

**Sprint workers** (after PM dispatch) also run:

```bash
bash tools/run_agent_session_gate.sh <role> <issue_id>   # opens session telemetry
```

**End every worker session** (closes telemetry + triggers PM):

```bash
bash tools/run_post_agent_cycle.sh --issue <id> --agent <role> --commit $(git rev-parse HEAD)
```

Factory telemetry policy: `docs/ops/qa/AGENT_SESSION_TELEMETRY.md` §9. One-time secret: `CURSOR_API_KEY` (`docs/ops/agents/CURSOR_SECRETS_SETUP.md` §8).

**Cross-cutting factory features (register before merge):**

```bash
bash tools/check_feature_integration.sh --remind   # docs/ops/qa/WORKFLOW_INTEGRATION.md
```

**Factory stack scripts** (event-driven PM):

Authority: `docs/ops/agents/FACTORY_SETUP_GUIDE.md`

| Script | Role |
|--------|------|
| `run_factory_watchdog.sh` | Stall detection + PM recovery |
| `pm_emit_stakeholder_report.sh` | Product owner status on cycle events |
| `run_alignment_audit.sh` | Spec/data alignment audit at post-merge — management visuals: `audit_radar_spec.png`, `audit_radar_build.png` |

All must be true before implementation (`.cursorrules` §0 / `MCP_STACK.md`):

| Check | How |
|-------|-----|
| GDAI HTTP bridge | `curl -sf http://127.0.0.1:3571/tools` returns JSON |
| Cursor MCP servers | `godot-mcp`, `godotiq`, `godot-mcp-pro`, `gamelab-mcp`, `notion` all connected |
| Godot Editor | Running with `game/project.godot` open |

If any server is missing → **stop and notify the user** (`godot-mcp-pro` hard-blocks L4/L5 gates;
others block their respective roles — see `MCP_STACK.md`).

### 1.3 Build loop (per task)

```
1. Read design doc section for the task
2. GodotPrompter — draft GDScript / shaders / unit tests
3. GDAI MCP — apply scenes, nodes, materials in live editor
4. GDAI MCP — F5 run scene; read Output / debugger; fix until clean
5. Run automated tests (§3)
6. Confirm acceptance criteria for current phase (§4)
7. Commit + push
```

### 1.4 What AI agents must not do

- Import unknown-license art, audio, or models from the web
- Hand-edit `.tscn` when GDAI MCP is available
- Ship with GDAI MCP plugin enabled (dev-only; remove before export)
- Mark a phase complete without passing its acceptance criteria
- Add new `CharacterBody3D` / `Area3D` interaction stacks outside `base_classes.json` registry

---

## Packs (progressive disclosure)

| Topic | Pack |
|-------|------|
| Testing policy + unit tests | [ai_dev/testing_policy.md](ai_dev/testing_policy.md) |
| Phase acceptance | [ai_dev/phase_acceptance.md](ai_dev/phase_acceptance.md) |
| Commands + related | [ai_dev/commands.md](ai_dev/commands.md) |

## Related gates

- Optional pre-merge: `CANDIDATE_TOURNAMENT` · `docs/ops/qa/CANDIDATE_TOURNAMENT.md`

