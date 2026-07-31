---
id: phase1-visuals
type: how-to
audience: [architect, builder]
phase: [1]
status: active
authority: engineering
tokens_est: 1330
summary: "Phase 1 ZoneVisuals + toon_base"
---
# GDScript Regen — Checklist & Phase 1 — Phase 1 ZoneVisuals + toon_base

**Hub:** [`checklist_recover.md`](../checklist_recover.md)

## 10. Phase 1 visuals — `ZoneVisuals` + `toon_base` (P1-01)

**Sprint:** `docs/ops/sprints/Phase1-Sprint1-issues.md` §P1-01
**Checklist command:** `bash tools/regenerate_phase1_visuals.sh`
**Unblocks:** P1-02 Builder (`ruined_village.tscn` via GDAI MCP)

| On `main` | On `game/development` |
|-----------|------------------------|
| `base_classes.json` → `ZoneVisuals.public_api` | `game/scripts/exploration/zone_visuals.gd` |
| `tools/zone_visuals_lib.py` | Must match reference + `unit_test_specs.json` |
| `shader_registry.json` + template | `game/shaders/toon_base.gdshader` |
| `environment_registry.json` | `game/environments/ruined_village.tres` (optional) |
| `unit_test_specs.json` | `game/tests/unit/test_zone_visuals.gd` |

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

### 10.3 Per-artifact steps

#### Step 1 — `toon_base.gdshader`

1. Read `game/data/code/shader_registry.json` → entry `toon_base`
2. Copy `template_path` to `res://shaders/toon_base.gdshader` (byte match unless registry updated on `main`)
3. Verify `render_mode` includes `diffuse_toon`, `specular_toon`; uniforms match registry

#### Step 2 — `zone_visuals.gd`

1. Read `game/data/code/base_classes.json` → `ZoneVisuals` (`public_api`, `exports`, `constants`)
2. Read `tools/zone_visuals_lib.py` — behavior truth for:
   - `hex_to_color`, `get_preset`, `build_environment`
   - `directional_settings`, `fill_light_settings`
   - `apply_to_scene` (canonical static entry — `TECHNICAL_DESIGN.md` §8)
   - instance `apply_zone_visuals()` using `PALETTE_PATH` = `res://data/world/zone_palettes.json`
3. Port to `game/scripts/exploration/zone_visuals.gd` with `class_name ZoneVisuals`
4. Node discovery per `zone_palettes.json` → `defaults` (`WorldEnvironment`, `DirectionalLight3D`, group `zone_fill_light`)

| Python (`zone_visuals_lib.py`) | GDScript |
|--------------------------------|----------|
| `load_catalog()` | `_load_presets()` via `FileAccess` + `JSON.parse_string` |
| `build_environment(zone_key)` | `build_environment(preset: Dictionary) -> Environment` |
| `apply_to_scene(zone_key)` | `static func apply_to_scene(root: Node, zone_id: String) -> void` |
| `hex_to_color("#RRGGBB")` | `static func hex_to_color(hex: String) -> Color` |

#### Step 3 — `ruined_village.tres` (optional)

- **Option A (preferred v1):** runtime only — `ZoneVisuals.build_environment()` from palette row; skip `.tres`
- **Option B:** bake values from `environment_registry.json` → `presets[ruined_village].properties`

#### Step 4 — unit tests

1. Read `game/data/qa/unit_test_specs.json` → suite `zone_visuals`
2. Create `game/tests/unit/test_zone_visuals.gd` mirroring each `cases[]` entry
3. Register in `game/tests/unit/test_runner.gd` if not auto-discovered

### 10.4 Verify

```bash
# On main specs (any branch)
bash tools/regenerate_phase1_visuals.sh --test

# On game/development after ports
bash tools/run_unit_tests.sh
bash tools/run_ci_checks.sh
```

**Gates:** `L1_unit_tests`, `L1_gdscript_lint`, `L0_base_class_compliance`

### 10.5 Builder handoff (P1-02)

After Architect PR merges, Builder uses GDAI MCP — **do not hand-edit `.tscn` in Cursor**:

- Node tree: P1-01 handoff in `docs/ops/sprints/phase1_sprint1/p1_01_architect_toon.md`
- Scene catalog: `scene_registry.json` → `ruined_village.required_nodes`
- Materials: assign `toon_base.gdshader` on greybox meshes
- Gates: `L3_gdai_built`, `L2_scene_primitives`

### 10.6 Recovering prior ports (diff hints)

```bash
git show 87a5ace:game/scripts/exploration/zone_visuals.gd
git show 87a5ace:game/shaders/toon_base.gdshader
git show 87a5ace:game/environments/ruined_village.tres
git show 87a5ace:game/tests/unit/test_zone_visuals.gd
```

Registry + Python reference win on conflicts.

### 10.7 One-command checklist

```bash
bash tools/regenerate_phase1_visuals.sh          # checklist + validate + reference tests
bash tools/regenerate_phase1_visuals.sh --check   # spec artifacts only
bash tools/regenerate_phase1_visuals.sh --test    # ZoneVisualsLibTests only
```
