---
id: toolchain-base
type: how-to
phase: [0, 1, 8]
audience: [pm, architect, builder]
status: active
authority: workflow
tokens_est: 527
summary: "AI Dev — Build Policy — Toolchain + base classes — Rule: No hand-edited `.tscn` or inspector-only work in Cursor. If GDAI MCP is unavailable → stop and notify t"
---
# AI Dev — Build Policy — Toolchain + base classes

**Hub:** [`build_policy.md`](../build_policy.md)

## When to read

Use **AI Dev — Build Policy — Toolchain + base classes** (roles: pm, architect, builder) when executing this procedure Jump to a section below instead of reading end-to-end (2 sections).

## Jump to

- [1.1 Mandatory toolchain](#11-mandatory-toolchain)
- [1.1b Code base classes (extend-only)](#11b-code-base-classes-extend-only)


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
