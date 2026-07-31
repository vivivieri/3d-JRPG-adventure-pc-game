---
id: order-helpers
type: how-to
audience: [architect, builder]
phase: [1, 2]
status: active
authority: engineering
tokens_est: 400
summary: "Regen order & per-helper steps"
---
# GDScript Regeneration — Regen order & per-helper steps

**Hub:** [`GDSCRIPT_REGENERATION.md`](../GDSCRIPT_REGENERATION.md)

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

