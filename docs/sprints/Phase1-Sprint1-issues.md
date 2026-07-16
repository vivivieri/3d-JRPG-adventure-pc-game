# Phase1-Sprint1 — GitHub Issue Pack

**Cycle:** `Phase1-Sprint1`  
**Branch:** `game/development`  
**Phase exit ref:** `acceptance_criteria.json` → `phase_gates.phase_1`  
**Implementation ref:** `docs/workflow/IMPLEMENTATION_PLAN.md` §Phase 1 (tasks 1.1–1.11)  
**Sprint master:** PM Agent — run `bash tools/run_pm_orchestrator.sh` before dispatch  
**Board:** `game/data/qa/sprint_board.json`  
**Runbook:** `docs/agents/PM_AGENT_RUNBOOK.md`

**WIP limit:** 7 issues · close when gate IDs PASS on merged PRs  

**Dependency order:** `P1-00` → `P1-01` → `P1-02` → `P1-04` / `P1-03` (parallel) → `P1-05` → `P1-06`

---

## Labels (apply to every issue)

```
env/development
milestone:M1-core
```

Plus per-issue: `agent/*`, `gate/*` as listed below.

---

## P1-00 — Bootstrap `game/development` (prerequisite)

**Title:** `[DEV][P1-00] Bootstrap game/development — project.godot + CI baseline`

**Labels:** `agent/pm`, `agent/architect`, `status/blocked` (until MCP secrets set)

| Field | Value |
|-------|-------|
| Phase | 1 |
| Implementation plan | Phase 0 verify + branch bootstrap |
| Lead agent | **pm** (Architect executes) |
| Blocks | P1-01, P1-02, P1-03, P1-04, P1-05 |

### Acceptance gate IDs

```
L0_rr_compliance
L0_story_data
L0_narrative_density
L0_acceptance_catalog
L0_base_classes
L1_unit_tests
L2_boot_headless          # SKIP until main_scene set — OK for this issue only
```

### Spec summary

Merge latest `main` into `game/development`. Run `bash tools/setup_dev_environment.sh`. Create minimal Godot 4.7 Forward+ project shell (`game/project.godot`, autoload stubs, `game/tests/unit/test_runner.gd`). No ship `.tscn` without GDAI — stub `run/main_scene` only when boot test is ready.

**Core helpers (R&R — `docs/technical/GDSCRIPT_REGENERATION.md` §2):**
- **Architect:** port `event_bus.gd` from `helpers_registry.json` (signals only)
- **Builder:** register `EventBus` autoload in `project.godot` via GDAI MCP
- Phase 2+ helpers (`SettingsStore`, `SaveIntegrity`, etc.) are **not** in P1-00 — PM dispatches per `helpers_registry.json` → `dispatch_by_phase`

Verify bootstrap CI (P1-00 profile — art/export gates deferred until `main_scene`):

```bash
bash tools/install_cloud_dev.sh
bash tools/install_extended_toolchain.sh
bash tools/ensure_mcp_stack.sh
bash tools/check_mcp_ready.sh
bash tools/check_extended_toolchain.sh
bash tools/run_bootstrap_ci_checks.sh
```

Full game CI (`bash tools/run_ci_checks.sh`) is required after **P1-02** sets `run/main_scene` and GDAI scenes land.

### Design refs

- `docs/workflow/BRANCHING.md`
- `docs/agents/MCP_STACK.md`
- `AGENTS.md` — Environment bootstrap

### Definition of done

- [ ] `game/project.godot` exists on `game/development`
- [ ] **Architect:** `event_bus.gd` ported per `helpers_registry.json`
- [ ] **Builder:** `EventBus` autoload registered via GDAI MCP
- [ ] `bash tools/run_bootstrap_ci_checks.sh` exits 0 (or document any unexpected FAIL in PR)
- [ ] After P1-02: `bash tools/run_ci_checks.sh` exits 0 on merge commits that add `main_scene`
- [ ] MCP stack PASS (`check_mcp_ready.sh` + `check_extended_toolchain.sh`)
- [ ] PR merged to `game/development`

---

## P1-01 — Architect: toon shader + zone visuals

**Title:** `[DEV][P1-01] Phase 1.1–1.3 — toon_base.gdshader, zone_visuals.gd, ruined_village env preset`

**Labels:** `agent/architect`, `gate/L1_unit_tests`

| Field | Value |
|-------|-------|
| Phase | 1 |
| Implementation plan | **1.1**, **1.2**, **1.3** |
| Lead agent | **architect** |
| Depends on | P1-00 |
| Unblocks | P1-02 |

### Acceptance gate IDs

```
L1_unit_tests
L1_gdscript_lint
L0_base_class_compliance
```

### Spec summary

**Regeneration runbook:** `docs/technical/GDSCRIPT_REGENERATION.md` §10 · `bash tools/regenerate_phase1_visuals.sh`

GodotPrompter drafts (no hand `.tscn`):

1. **`game/shaders/toon_base.gdshader`** — single ramp family (`diffuse_toon`, `specular_toon`); uniforms: `base_color`, `albedo_texture`, optional emission.
2. **`game/scripts/exploration/zone_visuals.gd`** — applies per-zone palette, `WorldEnvironment`, `ProceduralSky`, directional + fill lights from zone id.
3. **`game/environments/ruined_village.tres`** (or runtime-only if Architect prefers) — tonemap Filmic/ACES, fog `#8B9DAF` density `0.008`, glow for emissive props.

**Ruined village targets** (`docs/art/RENDERING_GUIDE.md` §4–§6):

| Property | Value |
|----------|-------|
| Sky top / horizon | `#4A7A9A` / `#B8D0E0` |
| Directional | Cool overcast `#B8C8D8`, ~35° |
| Fill | Warm lantern `#D4A880` (lantern + shack) |
| Fog | `#8B9DAF`, density `0.008`, always on |

Add unit tests for `zone_visuals.gd` palette application (headless).

### Architect → Builder handoff (paste in issue when done)

```markdown
## Handoff to Builder (P1-02)

### Node tree outline — `ruined_village.tscn`
- Root: `Node3D` (zone root)
  - `WorldEnvironment` — assign `ruined_village` preset via `zone_visuals.gd` or `.tres`
  - `DirectionalLight3D` — shadow on, soft filter
  - `OmniLight3D` ×2 — lantern fill `#D4A880` (shack, shrine path)
  - `ZoneVisuals` — script `zone_visuals.gd`, export `zone_id = "ruined_village"`
  - `Terrain` / greybox meshes — material: ShaderMaterial `toon_base.gdshader`
  - `Markers` — empty placeholders per `zone_composition.json` markers
  - `GameplayCamera` — height 1.6 m reference for screenshots

### Shader / uniform list
- `toon_base.gdshader`: `base_color`, `albedo_texture` (placeholder flat `#5C4A3A` wood / `#C9B89A` sand)

### Inspector targets (GDAI sets)
- Directional: `shadow_enabled=true`, light color `#B8C8D8`
- WorldEnvironment: tonemap Filmic, fog on, glow ~0.35
- ZoneVisuals.zone_id = `ruined_village`

### Target gate IDs
- L3_gdai_built
- L2_scene_primitives
- L2_boot_headless (when main_scene wired)

### Component scenes
- `res://scenes/components/lantern_fill.tscn` — warm fill only (Phase 1 catalog)

### Base classes
- None new — no `PlayerController` until Phase 2

### Generation brief
- N/A (greybox slice)
```

### Design refs

- `docs/art/RENDERING_GUIDE.md` §3–§6
- `docs/art/ART_DIRECTION.md` §1 (hub palette), §7
- `docs/world/ENVIRONMENT_KITS.md` §4 (ruined_village)
- `.cursorrules` §6 — toon shader reference

### Definition of done

- [ ] Shaders + script committed; unit tests pass
- [ ] Handoff block above posted in this issue
- [ ] Reassign to `agent/builder`

---

## P1-02 — Builder: GDAI ruined_village greybox vertical slice

**Title:** `[DEV][P1-02] Phase 1.5–1.7 — GDAI ruined_village.tscn greybox + SC-02 lighting`

**Labels:** `agent/builder`, `gate/L2_scene_primitives`, `gate/L3_gdai_built`

| Field | Value |
|-------|-------|
| Phase | 1 |
| Implementation plan | **1.5** (ruined_village only), **1.6**, **1.7**, **1.9** — task **1.8** (component scenes) deferred to Phase1-Sprint2 |
| Lead agent | **builder** |
| Depends on | P1-00, P1-01 handoff |
| Unblocks | P1-04, P1-05 |

### Acceptance gate IDs

```
L3_gdai_built
L3_gdai_f5              # agent-local — GDAI F5 in editor
L2_scene_primitives
L2_boot_headless        # if run/main_scene points here
L2_feel_smoke           # constants only — no player yet OK
```

### Spec summary

**GDAI MCP only** — create `res://scenes/world/ruined_village.tscn`:

1. Apply Architect handoff (lights, fog, sky, toon materials on greybox).
2. Greybox layout per `docs/world/LEVEL_DESIGN.md` §3 (~120×120 m hub): torii north, well/shack mid, pier south, cave entrance marker.
3. Place **markers** from `game/data/qa/zone_composition.json` → `ruined_village.markers` (do not rename).
4. Greybox meshes allowed at Phase 1 gate (`ART_DIRECTION.md` §10) — no Kenney/European kits.
5. F5 verify: 0 errors, 60 FPS target @ 1080p in viewport.
6. Update `game/scenes/.gdai_built` — `verified_f5=true`, scenes touched listed.

**Phase 1 vertical slice checklist** (`ART_DIRECTION.md` §10 Phase 1 gate):

- [ ] Palette matches §1 hex at gameplay camera
- [ ] Filmic/ACES + zone fog (not default grey)
- [ ] Toon ramp on ground/blockout meshes
- [ ] 60 FPS @ 1080p in editor play

### Builder → QA handoff

```markdown
## Handoff to QA

- Commit: `<sha>`
- Scenes touched: `res://scenes/world/ruined_village.tscn`
- `.gdai_built`: verified_f5=true
- Screenshot: `artifacts/screenshots/phase1_ruined_village_wip.png` (optional WIP)
- Main scene: `<set or unset>`
```

### Design refs

- `docs/world/LEVEL_DESIGN.md` §3
- `docs/world/ENVIRONMENT_KITS.md` §4
- `docs/art/ART_DIRECTION.md` §10 (Phase 1 gate)
- `game/data/qa/zone_composition.json` → `ruined_village`

### Definition of done

- [ ] Scene built via GDAI; no hand-edited `.tscn` in Cursor
- [ ] `.gdai_built` updated
- [ ] F5 clean; handoff posted
- [ ] Reassign to `agent/qa`

---

## P1-03 — Architect: water_stylized shader (parallel)

**Title:** `[DEV][P1-03] Phase 1.4 — water_stylized.gdshader (foam + displacement)`

**Labels:** `agent/architect`, `gate/L1_unit_tests`

| Field | Value |
|-------|-------|
| Phase | 1 |
| Implementation plan | **1.4** |
| Lead agent | **architect** |
| Depends on | P1-00 |
| Parallel with | P1-02 |

### Acceptance gate IDs

```
L1_unit_tests
L1_gdscript_lint
```

### Spec summary

Draft `game/shaders/water_stylized.gdshader`:

- Stylized plane water — not fluid sim
- Gentle vertex displacement + foam edge (UV or depth-based)
- Palette: surf teal `#1A6A62` (beach), pier adjacency in village
- Matches toon family — no glossy PBR

Unit test: shader compiles headless (material create smoke if project supports).

### Design refs

- `docs/art/ART_DIRECTION.md` §3.6
- `docs/world/ENVIRONMENT_KITS.md` §3 (`beach_shoreline_water`)

### Definition of done

- [ ] Shader committed + lint clean
- [ ] Note in P1-02 for Builder to assign pier water plane when pier greybox lands

---

## P1-04 — QA: CI green + Phase 1 gate report

**Title:** `[DEV][P1-04] Phase 1 — CI green + L0–L2 gate report on ruined_village PR`

**Labels:** `agent/qa`, `env/qa`, `gate/L1_unit_tests`, `gate/L2_scene_primitives`

| Field | Value |
|-------|-------|
| Phase | 1 |
| Implementation plan | Sprint QA (all Phase 1 PRs) |
| Lead agent | **qa** |
| Depends on | P1-02 merged |

### Acceptance gate IDs

```
L0_rr_compliance
L0_story_data
L0_narrative_density
L0_acceptance_catalog
L0_base_classes
L0_base_class_compliance
L1_unit_tests
L1_gdscript_lint
L2_scene_primitives
L3_gdai_built
L2_feel_smoke
L2_glb_import
```

**Not in Sprint1 scope:** `L4_integration` (Phase 3+ per `sprint_phases.json`; `INT-BOOT-01` runs when `main_scene` is set).

### Commands

```bash
bash tools/run_ci_checks.sh
bash tools/run_playtest_smoke.sh
```

### Gate report template (paste in PR + issue)

```markdown
## Gate report — Phase1-Sprint1

- Commit: `<sha>`
- Branch: `game/development`

| Gate ID | Result | Evidence |
|---------|--------|----------|
| L0_rr_compliance | PASS | check_rr_compliance.sh exit 0 |
| L0_story_data | PASS | validate_story_data.py |
| L0_base_classes | PASS | validate_base_classes.py |
| L0_base_class_compliance | PASS | check_base_class_compliance.sh |
| L1_unit_tests | PASS | run_unit_tests.sh |
| L1_gdscript_lint | PASS/SKIP | check_gdscript_changed.sh |
| L2_scene_primitives | PASS | check_scene_visuals.sh |
| L3_gdai_built | PASS | .gdai_built verified_f5=true |
| L2_feel_smoke | PASS | run_feel_smoke_checks.sh |
| L2_glb_import | PASS/SKIP | strict when GLBs present |

**Not run (expected):** L4_integration (Phase 3+), L2_visual_jury, L5 E2E, L6 human

**Policy:** WARN ≠ PASS · SKIP ≠ PASS on game branch
```

### On FAIL

```bash
bash tools/qa_emit_remediation.sh visual-palette   # or flow-scenario / model-tech as appropriate
```

Post remediation JSON + gate ID; reassign to Architect or Builder.

### Definition of done

- [ ] `run_ci_checks.sh` PASS on merge commit
- [ ] Gate report in PR description
- [ ] Issue updated with evidence paths

---

## P1-05 — QA + Builder: golden screenshot + zone composition (GR-001, GR-003)

**Title:** `[DEV][P1-05] Phase 1.10–1.11 — ruined_village golden screenshot + zone composition smoke`

**Labels:** `agent/qa`, `agent/builder`, `domain/visual`, `gate/L2_zone_composition`

| Field | Value |
|-------|-------|
| Phase | 1 |
| Implementation plan | **1.10**, **1.11** |
| Generation readiness | **GR-001**, **GR-003** |
| Lead agent | **qa** (Builder captures via GDAI) |
| Depends on | P1-02 merged (P1-04 gate report recommended but not blocking) |

### Acceptance gate IDs

```
L2_visual_palette
L2_zone_composition     # warn mode — strict at M5
```

### Spec summary

1. **GDAI capture** gameplay camera screenshot at 1.6 m height, gameplay FOV, torii vista readable.
2. Save to `artifacts/screenshots/phase1_ruined_village_gameplay.png` (path from `zone_composition.json`).
3. Run zone composition smoke:

```bash
bash tools/run_zone_composition_checks.sh
# M5 strict: ZONE_COMPOSITION_STRICT=1 bash tools/run_zone_composition_checks.sh
```

4. Optional palette smoke when screenshot exists:

```bash
bash tools/run_visual_smoke_checks.sh
```

### Evidence

- `artifacts/screenshots/phase1_ruined_village_gameplay.png`
- `artifacts/visual_reviews/` if jury keys available (conditional — SKIP ≠ PASS for M5 ship)

### Design refs

- `docs/art/GENERATION_READINESS.md` §X-02
- `game/data/qa/generation_readiness_backlog.json` → GR-001, GR-003
- `game/data/qa/zone_composition.json` → `ruined_village`

### Definition of done

- [ ] Golden screenshot committed under `artifacts/screenshots/`
- [ ] Zone composition smoke exit 0 (warn OK for Phase 1)
- [ ] GR-001 / GR-003 status updated in backlog PR if closing items

---

## P1-06 — PM: Phase 1 sprint review + carry-over

**Title:** `[DEV][P1-06] Phase1-Sprint1 review — phase_1 exit gap analysis`

**Labels:** `agent/pm`, `agent/qa`

| Field | Value |
|-------|-------|
| Phase | 1 |
| Lead agent | **pm** |
| Depends on | P1-04 (minimum) |

### Phase 1 exit gates (`acceptance_criteria.json`)

**Required:**

```
L0_rr_compliance
L0_story_data
L0_narrative_density
L1_unit_tests
L2_boot_headless
L2_scene_primitives
```

**Conditional (when assets exist):**

```
L2_visual_palette
L2_visual_jury
L2_zone_composition
L2_model_technical
L2_model_jury
L2_audio_technical
L2_audio_jury
```

### Sprint review agenda

1. Paste QA gate report from P1-04.
2. List PASS / FAIL / SKIP per phase_1 required_gates.
3. Carry over to **Phase1-Sprint2**: remaining greybox zones (1.5 beach/caves/palace), `lantern_fill.tscn` component (1.8), water assign on pier.
4. Optional UAT tag when phase_1 required all PASS: `v0.1.0-rc1` (`sprint_phases.json`).

### Definition of done

- [ ] Sprint review comment on this issue
- [ ] Carry-over issues filed for Phase1-Sprint2
- [ ] `status/done` on closed sprint issues

---

## Phase1-Sprint2 preview (file issues next cycle)

| Issue | Agent | Tasks | Gates |
|-------|-------|-------|-------|
| Greybox `beach_shore`, `tidal_caves`, `dragon_palace_gate` | builder | 1.5–1.7 | L2_scene_primitives, L3 |
| `lantern_fill.tscn` + pier water | builder | 1.8, 1.4 assign | L3 |
| Beach golden screenshot | qa | 1.10 | L2_visual_palette, GR-001 |
| Phase 1 exit review | qa | phase_1 all required | tag `v0.1.0-rc1` optional |

---

## Quick copy: GitHub issue titles only

```
[DEV][P1-00] Bootstrap game/development — project.godot + CI baseline
[DEV][P1-01] Phase 1.1–1.3 — toon_base.gdshader, zone_visuals.gd, ruined_village env preset
[DEV][P1-02] Phase 1.5–1.7 — GDAI ruined_village.tscn greybox + SC-02 lighting
[DEV][P1-03] Phase 1.4 — water_stylized.gdshader (foam + displacement)
[DEV][P1-04] Phase 1 — CI green + L0–L2 gate report on ruined_village PR
[DEV][P1-05] Phase 1.10–1.11 — ruined_village golden screenshot + zone composition smoke
[DEV][P1-06] Phase1-Sprint1 review — phase_1 exit gap analysis
```
