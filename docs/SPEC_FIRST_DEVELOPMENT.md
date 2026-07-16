# Spec-first development policy

**Version:** 1.0  
**Authority:** Defines what lives on `main` vs `game/development` and when coding may start.  
**Cross-refs:** `docs/BRANCHING.md`, `docs/IMPLEMENTATION_PLAN.md`, `game/data/code/spec_registry.json`

---

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
| **Code contracts** | `game/data/code/*.json` | `base_classes.json`, `autoload_registry.json`, `scene_registry.json` |
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

```bash
python3 tools/validate_spec_registry.py   # L0_spec_registry
bash tools/check_main_no_ship_code.sh      # L0_main_no_ship_code (main branch only)
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

## 5. Build workflow (after gate passes)

```text
1. Read spec on main (docs + game/data/code/* + game/data/story/*)
2. GodotPrompter — implement .gd / .gdshader to match public_api in registries
3. GDAI MCP — instance scene_registry nodes + component scenes; F5 verify
4. Commit only on game/development; never merge implementation to main until M6
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
| Base classes | **Specified** | `base_classes.json` + TDD §2 |
| Zone scene graphs | **Specified** | `scene_registry.json` + `LEVEL_DESIGN.md` |
| Shader source files | **Partial** | Behavior in `ART_DIRECTION` / `RENDERING_GUIDE`; `.gdshader` files land Phase 1 on dev |
| Unit test `.gd` | **Partial** | `AI_TESTING_SPEC.md`; test files land with implementation |

Run `python3 tools/validate_spec_registry.py` for the live gate result.

---

## 8. Anti-patterns

| Do not | Do instead |
|--------|------------|
| Commit `.gd` / `.tscn` to `main` | Add/extend spec registry + docs on `main` |
| Implement on `game/development` before spec PR merges | Spec PR first |
| Mark IMPLEMENTATION_PLAN tasks “Done” without files on dev branch | Mark “Specified on main” vs “Built on dev” separately |
| Hand-edit ship `.tscn` in Cursor | GDAI MCP + `.gdai_built` marker |

---

## 9. Cross-refs

- `docs/BRANCHING.md` — branch merge policy  
- `docs/TECHNICAL_DESIGN.md` — runtime architecture (prose + diagrams)  
- `docs/CODE_BASE_CLASS_RULES.md` — who writes bases vs instances  
- `docs/IMPLEMENTATION_PLAN.md` — phase task list (execution on `game/development`)
