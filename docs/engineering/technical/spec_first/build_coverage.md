---
id: build-coverage
type: how-to
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, pm]
status: active
authority: engineering
tokens_est: 820
summary: "Build workflow, not on main, coverage, anti-patterns"
---
# Spec-First Development — Build workflow, not on main, coverage, anti-patterns

**Hub:** [`SPEC_FIRST_DEVELOPMENT.md`](../SPEC_FIRST_DEVELOPMENT.md)

## 5. Build workflow (after gate passes)

```text
1. Read spec on main (docs + game/data/code/* + game/data/story/*)
2. PM dispatches port work per helpers_registry.json → dispatch_by_phase
3. GodotPrompter (Architect) — implement .gd / .gdshader to match public_api; core helpers per GDSCRIPT_REGENERATION.md
4. GDAI MCP (Builder) — autoload wire-up + scene_registry nodes; F5 verify
5. Commit only on game/development; never merge implementation to main until M6
```

**Order:** Spec change on `main` → PR → then implementation PR on `game/development`.
Never implement behavior on `game/development` that is not yet specified on `main`.

---


## 6. What is intentionally not on `main`

| Item | Why | Where it is built |
|------|-----|-------------------|
| Full `.tscn` node positions | Editor placement, GDAI MCP | `game/development` |
| Material tuning / light angles | Viewport iteration | `game/development` |
| Hero GLB meshes | Art pipeline M5 | `game/assets/` on dev branch |
| GDAI / Godotiq addons | Dev toolchain (gitignored) | Local install |

**Scene structure** (node *names* and *types*) **is** specified in `scene_registry.json` + `LEVEL_DESIGN.md`. **Transforms** are not.

---


## 7. Current spec coverage (honest)

| Domain | Status | Notes |
|--------|--------|-------|
| Story / dialogue / flags | **Specified** | `game/data/story/`, `chapter_01.json` |
| Combat data | **Specified** | `enemies.json`, `skills.json`, encounters |
| Narrative density | **Specified** | `narrative_density.json` |
| Autoload APIs | **Specified** | `autoload_registry.json` |
| Core helpers | **Specified** | `helpers_registry.json` + `tools/*_lib.py` on `main` |
| Base classes | **Specified** | `base_classes.json` + TDD §2 |
| Zone scene graphs | **Specified** | `scene_registry.json` + `LEVEL_DESIGN.md` |
| Shader source files | **Specified** | `shader_registry.json` + `SHADER_SPECS.md`; `.gdshader` on dev |
| Zone visuals | **Specified** | `zone_palettes.json`, `environment_registry.json`, `zone_visuals_lib.py` |
| Unit test `.gd` | **Specified** | `unit_test_specs.json` mirrors `test_reference_libs.py` cases |

Run `python3 tools/validate_spec_registry.py` for the live gate result.

---


## 8. Anti-patterns

| Do not | Do instead |
|--------|------------|
| Commit `.gd` / `.tscn` to `main` | Add/extend spec registry + docs on `main` |
| Implement on `game/development` before spec PR merges | Spec PR first |
| Mark IMPLEMENTATION_PLAN tasks “Done” without files on dev branch | Mark “Specified on main” vs “Built on dev” separately |
| Hand-edit ship `.tscn` in Cursor | GDAI MCP + `.gdai_built` marker |
| “Quick” `.gd` while refining specs | Python `tools/*_lib.py` on `main`; GDScript only after PM dispatch |
| Self-assign implementation work | `run_pm_orchestrator.sh` → `run_agent_session_gate.sh` |
| Builder writes helper logic | Architect ports `.gd`; Builder wires autoloads only |

---
