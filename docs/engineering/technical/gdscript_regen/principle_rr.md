---
id: principle-rr
type: how-to
audience: [architect, builder]
phase: [1, 2]
status: active
authority: engineering
tokens_est: 832
summary: "Principle, R&R, prerequisites"
---
# GDScript Regeneration — Principle, R&R, prerequisites

**Hub:** [`GDSCRIPT_REGENERATION.md`](../GDSCRIPT_REGENERATION.md)

## 1. Principle

| On `main` | On `game/development` |
|-----------|------------------------|
| **Spec** (`helpers_registry.json`, `autoload_registry.json`) | **GDScript port** |
| **Python reference** (`tools/*_lib.py`) — behavior truth | Must match reference + pass parity tests |
| **Data** (`game/data/`) | Reads same JSON paths via `res://data/` |

**Never invent behavior** when porting — if the reference lib and registry disagree, fix `main` first.

---


## 2. Roles & responsibilities (R&R)

**Authority:** `game/data/code/helpers_registry.json` → `roles_and_responsibilities` · `docs/ops/cheat-sheets/RR_CHEATSHEET.md`

| Work | Owner | Agent | Branch | Must NOT |
|------|-------|-------|--------|----------|
| **Spec + Python reference** | Architect | GodotPrompter | `main` | Ship `.gd` / `.tscn` on `main` |
| **GDScript port** | Architect | GodotPrompter | `game/development` | Register autoloads; invent behavior |
| **Autoload wire-up** (`EventBus`, etc.) | Builder | GDAI Builder | `game/development` | Author helper logic in `.gd` |
| **Parity verification** | QA | QA Agent | both | Port code or mark ship without gates |
| **Dispatch** (when to port) | PM | PM Agent | — | Self-assign; skip `main` spec PR |

### Dispatch by phase (PM assigns issue; Architect executes port)

| Phase | Sprint ref | Helpers to port | Handoff |
|-------|------------|-----------------|---------|
| **1** | **P1-00** bootstrap | `EventBus` (`port_status: pending`) | Architect → `.gd` · Builder → `project.godot` autoload via GDAI |
| **2** | Save/settings shell | `SettingsStore`, `SaveIntegrity` (`port_status: pending`) | Architect → `.gd` + unit tests · Builder → F5 boot |
| **4** | Combat | `DifficultyService` (`port_status: pending`) | Architect → `.gd` before encounter tuning |
| **6** | Achievements | `AchievementEvaluator` (`port_status: pending`) | Architect → `.gd` before Steam hooks |
| **1** | **P1-01** zone visuals | `ZoneVisuals` + `toon_base.gdshader` (`base_classes.json`) | Architect → §10; Builder → P1-02 scenes |

`port_status` in `helpers_registry.json`: `pending` | `ported` | `wired`. Do **not** port ahead of PM dispatch — early ports are reverted to keep phase handoffs clean.

**No agent other than Architect** may author `game/scripts/core/*.gd` for these helpers.
**No agent other than Builder** may register autoloads in `project.godot` (GDAI MCP only).

### Gates per owner

| Owner | Gates |
|-------|-------|
| Architect (`main` spec PR) | `L0_helpers_registry`, `L0_reference_libs` |
| Architect (`game/development` port PR) | `L1_unit_tests`, `L1_gdscript_lint` |
| Builder (autoload PR) | `L3_gdai_built`, `L2_boot_headless` |
| QA (verify) | All of the above on the PR under review |

---


## 3. Prerequisites

```bash
git checkout game/development
git merge main                    # pull latest specs + reference libs
bash tools/regenerate_core_helpers.sh --check   # reference libs + registry OK
bash tools/ensure_mcp_stack.sh    # before wiring autoloads in editor
```

---
