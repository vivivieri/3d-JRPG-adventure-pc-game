---
id: rule-registries-gate
type: how-to
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, pm]
status: active
authority: engineering
tokens_est: 919
summary: "Core rule, what is spec, registries, start gate"
---
# Spec-First Development — Core rule, what is spec, registries, start gate

**Hub:** [`SPEC_FIRST_DEVELOPMENT.md`](../SPEC_FIRST_DEVELOPMENT.md)

## When to read

Use **Spec-First Development — Core rule, what is spec, registries, start gate** (roles: architect, pm) when executing this procedure Jump to a section below instead of reading end-to-end (4 sections).

## Jump to

- [1. Core rule](#1-core-rule)
- [2. What counts as “specification”](#2-what-counts-as-specification)
- [3. Spec registries (machine-readable)](#3-spec-registries-machine-readable)
- [4. Development start gate](#4-development-start-gate)


## 1. Core rule

| Branch | Holds | Does **not** hold |
|--------|--------|-------------------|
| **`main`** | **Complete specifications** — docs, `game/data/` JSON, spec registries, validators, locale | Ship GDScript, `.tscn`, `project.godot`, ship assets |
| **`game/development`** | Implementation **built from** `main` specs | Design changes without a `main` PR first |

**No ship gameplay code before development start.**
Specifications on `main` are the contract. `game/development` is the factory output.

---


## 2. What counts as “specification”

A feature is **specified** when an agent can implement it **without inventing behavior**:

| Spec layer | Location | Example |
|------------|----------|---------|
| **Design prose** | `docs/*.md` | `COMBAT_SYSTEMS.md`, `LEVEL_DESIGN.md` |
| **Machine data** | `game/data/**/*.json` | `enemies.json`, `chapter_01.json` |
| **Code contracts** | `game/data/code/*.json` | `base_classes.json`, `autoload_registry.json`, `scene_registry.json`, `helpers_registry.json` |
| **Reference libs** | `tools/*_lib.py` | Python behavior truth for core helpers — port to GDScript on `game/development` |
| **QA / gates** | `game/data/qa/acceptance_criteria.json` | Measurable pass/fail |

**Not sufficient alone:** a one-line class name in a table, or “TODO in Phase 2” without API/node detail.

---


## 3. Spec registries (machine-readable)

| File | Purpose |
|------|---------|
| `game/data/code/spec_registry.json` | Master index + **development start gate** |
| `game/data/code/autoload_registry.json` | Autoload singletons — responsibilities + public API |
| `game/data/code/scene_registry.json` | Canonical `.tscn` paths + required nodes per zone |
| `game/data/code/base_classes.json` | GDScript base classes + component scene catalog |
| `game/data/code/helpers_registry.json` | Core RefCounted helpers + EventBus signals + regeneration order |
| `docs/engineering/technical/GDSCRIPT_REGENERATION.md` | Step-by-step port workflow for deleted `game/scripts/core/*.gd` |

```bash
python3 tools/validate_spec_registry.py      # L0_spec_registry
python3 tools/validate_helpers_registry.py   # L0_helpers_registry
python3 tools/test_reference_libs.py         # L0_reference_libs
bash tools/regenerate_core_helpers.sh        # checklist + both checks
bash tools/regenerate_phase1_visuals.sh      # P1-01 zone visuals + toon shader checklist
bash tools/check_main_no_ship_code.sh        # L0_main_no_ship_code (main branch only)
```

---


## 4. Development start gate

**Gate id:** `SPEC_DEV_START` (see `spec_registry.json`)

Coding on `game/development` may begin when:

1. `L0_spec_registry` — all **blocking** artifacts are `spec_status: specified`
2. `L0_main_no_ship_code` — `main` has zero ship GDScript / `.tscn` / `project.godot`
3. `L0_story_data` + related data validators pass
4. MCP stack ready (`bash tools/ensure_mcp_stack.sh`) for scene work

**Blocking artifacts** = Phase 0–2 shell: autoloads, base exploration scripts, boot/menu, first zone greybox catalog, core UI scenes (see registry).

---
