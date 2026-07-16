# GDScript regeneration — core helpers

**Version:** 1.0  
**Authority:** How to rebuild deleted `game/scripts/core/*.gd` on `game/development` from `main` specs.  
**Cross-refs:** `docs/technical/SPEC_FIRST_DEVELOPMENT.md`, `game/data/code/helpers_registry.json`

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
| **0** | **P1-00** bootstrap | `EventBus` | Architect → `.gd` · Builder → `project.godot` autoload |
| **2** | Save/settings shell | `SettingsStore`, `SaveIntegrity` | Architect → `.gd` + unit tests · Builder → F5 boot |
| **4** | Combat | `DifficultyService` | Architect → `.gd` before encounter tuning |
| **6** | Achievements | `AchievementEvaluator` | Architect → `.gd` before Steam hooks |

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
