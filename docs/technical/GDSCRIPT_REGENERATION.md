# GDScript regeneration — core helpers & Phase 1 visuals

**Version:** 1.1
**Authority:** How to rebuild deleted `game/scripts/core/*.gd` and Phase 1 visual scripts on `game/development` from `main` specs.
**Cross-refs:** `docs/technical/SPEC_FIRST_DEVELOPMENT.md`, `game/data/code/helpers_registry.json`, `game/data/code/base_classes.json`

---

## 1. Principle

| On `main` | On `game/development` |
|-----------|------------------------|
| **Spec** (`helpers_registry.json`, `autoload_registry.json`) | **GDScript port** |
| **Python reference** (`tools/*_lib.py`) — behavior truth | Must match reference + pass parity tests |
| **Data** (`game/data/`) | Reads same JSON paths via `res://data/` |

**Never invent behavior** when porting — if the reference lib and registry disagree, fix `main` first.

---

## 2. Roles & responsibilities (R&R)

**Authority:** `game/data/code/helpers_registry.json` → `roles_and_responsibilities` · `docs/cheat-sheets/RR_CHEATSHEET.md`

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

## 4. Regeneration order (mandatory)

From `helpers_registry.json` → `regeneration_order`:

| Step | Helper | Type | Why first |
|------|--------|------|-----------|
| 1 | **EventBus** | Autoload | Other systems emit/connect here |
| 2 | **SettingsStore** | RefCounted | Emits `hard_mode_changed` on toggle |
| 3 | **SaveIntegrity** | RefCounted | SaveSystem depends on HMAC |
| 4 | **DifficultyService** | RefCounted | CombatManager reads multipliers |
| 5 | **AchievementEvaluator** | RefCounted | Steam/achievement pass at run end |

---

## 5. Per-helper steps

### Step A — Read spec

```bash
# Example: DifficultyService
python3 -c "
import json
from pathlib import Path
h = json.loads(Path('game/data/code/helpers_registry.json').read_text())
print([x for x in h['helpers'] if x['id']=='DifficultyService'][0])
"
```

### Step B — Read Python reference

Open `tools/<name>_lib.py` listed in `python_reference` (EventBus has none — signals only).

### Step C — Port to GDScript

Create file at `gdscript_path` from registry:

| Python pattern | GDScript pattern |
|----------------|------------------|
| `def foo(...)` static | `static func foo(...)` |
| `dict` / `list` | `Dictionary` / `Array` |
| `Path.read_text` + JSON | `FileAccess` + `JSON.parse_string` |
| `hmac.compare_digest` | `Crypto` / `HMACContext` (see existing `save_integrity` port in git `544dca9^`) |

**EventBus only:**

```gdscript
extends Node
## Global signals — autoload (helpers_registry.json EventBus)

signal locale_changed(locale_code: String)
signal vo_dialect_changed(dialect_code: String)
# ... all signals from helpers_registry.json — no methods
```

Register in `project.godot` autoload section as `/root/EventBus` — **Builder (GDAI MCP) only**, after Architect commits `event_bus.gd`.

### Step D — Verify reference libs (main parity)

```bash
bash tools/regenerate_core_helpers.sh --test
```

### Step E — GDScript unit test (game/development)

When `game/project.godot` exists, add/extend tests under `game/tests/unit/` that mirror `tools/test_reference_libs.py` cases.

### Step F — Commit on `game/development` only

```bash
git add game/scripts/core/
git commit -m "feat(core): port DifficultyService from tools/difficulty_lib.py"
bash tools/run_ci_checks.sh
```

---

## 6. One-command checklist

```bash
bash tools/regenerate_core_helpers.sh          # print checklist + run reference tests
bash tools/regenerate_core_helpers.sh --check  # registry validation only
bash tools/regenerate_core_helpers.sh --test   # reference lib tests only
```

---

## 7. Recovering the previous GDScript ports

If you need the exact earlier ports (before spec-first cleanup):

```bash
git show 544dca9^:game/scripts/core/difficulty_service.gd
git show 544dca9^:game/scripts/core/save_integrity.gd
git show 544dca9^:game/scripts/core/settings_store.gd
git show 544dca9^:game/scripts/core/achievement_evaluator.gd
git show 544dca9^:game/scripts/core/event_bus.gd
```

Use these as **diff hints** only — registry + Python reference win on conflicts.

---

## 8. Adding a new helper

1. Add Python reference under `tools/` + tests in `tools/test_reference_libs.py`
2. Add entry to `helpers_registry.json` with full `public_api`
3. Append to `regeneration_order`
4. PR to **`main`** first
5. Port to GDScript on **`game/development`**

---

## 9. Reference map

| GDScript (`game/development`) | Python (`main`) | Data |
|--------------------------------|-----------------|------|
| `event_bus.gd` | — | `helpers_registry.json` signals |
| `settings_store.gd` | `tools/settings_store_lib.py` | `settings_defaults.json` |
| `save_integrity.gd` | `tools/save_integrity_lib.py` | `qa/save_integrity.json` |
| `difficulty_service.gd` | `tools/difficulty_lib.py` | `combat/difficulty.json` |
| `achievement_evaluator.gd` | `tools/achievement_evaluator_lib.py` | `achievements/achievements.json` |
| `zone_visuals.gd` | `tools/zone_visuals_lib.py` | `world/zone_palettes.json`, `code/environment_registry.json` |

---

## 10. Phase 1 visuals — `ZoneVisuals` + `toon_base` (P1-01)

**Sprint:** `docs/sprints/Phase1-Sprint1-issues.md` §P1-01
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

- Node tree: P1-01 handoff block in `Phase1-Sprint1-issues.md`
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
