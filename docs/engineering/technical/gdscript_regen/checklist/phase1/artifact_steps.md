---
id: artifact-steps
type: how-to
audience: [architect, builder]
phase: [1]
status: active
authority: engineering
tokens_est: 563
summary: "1. Read `game/data/code/shader_registry.json` → entry `toon_base`"
---
# Phase 1 Visuals Regen — Per-artifact steps

**Hub:** [`phase1_visuals.md`](../phase1_visuals.md)

## When to read

Use **Phase 1 Visuals Regen — Per-artifact steps** (roles: architect, builder) when executing this procedure Jump to a section below instead of reading end-to-end (1 sections).



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
