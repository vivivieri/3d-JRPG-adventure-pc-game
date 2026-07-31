---
id: unit-tests
type: how-to
phase: [0, 1, 8]
audience: [pm, qa, architect, builder]
status: active
authority: workflow
tokens_est: 649
summary: "test_runner.gd # Headless entry point (-s)"
---
# AI Dev — Testing Policy — Unit tests

**Hub:** [`testing_policy.md`](../testing_policy.md)

## 3. Unit tests

### 3.1 Location & naming

```
game/tests/
  unit/
    test_runner.gd           # Headless entry point (-s)
    test_story_data_paths.gd # Phase 0 — required files exist
    test_story_data_json.gd  # Phase 0 — JSON parses
    test_game_manager.gd     # Phase 2+ — load_json API
    test_damage_calculator.gd # Phase 4+ — combat math
    test_flag_system.gd      # Phase 3+ — quest flags
  integration/
    test_boot_smoke.gd       # Phase 0+ — main scene loads
    test_zone_transitions.gd # Phase 2+ — scene changes
    test_combat_round.gd     # Phase 4+ — one full turn
  e2e/
    test_three_endings.gd    # Phase 6 — ending branches
```

**Naming:** `test_<system>.gd` with static methods `test_<behavior>()` returning `""` on pass or an error string on fail.

### 3.2 Running unit tests

```bash
bash tools/run_unit_tests.sh
# or directly:
godot4 --headless --path game -s res://tests/unit/test_runner.gd
```

Exit code `0` = all pass; non-zero = failure count.

### 3.3 What must have unit tests

| System | Phase | Minimum tests |
|--------|-------|----------------|
| Story data paths | 0 | All required `res://data/` files exist |
| Story JSON parse | 0 | `scenes.json`, `flags.json`, `chapter_01.json` parse |
| `GameManager.load_json` | 2 | Valid path returns Dictionary; invalid path errors |
| Scene transition | 2 | `change_scene` does not error for each zone |
| Flag set/get | 3 | Set flag → persist → query returns true |
| Dialogue node advance | 3 | Linear branch reaches expected line ID |
| Damage calculator | 4 | Physical/magic/element table matches `COMBAT_SYSTEMS.md` samples |
| Turn order | 4 | Speed sort matches fixture |
| Save/load round-trip | 2 | Write slot → read slot → flags match |
| Shop prices | 3 | Match `game/data/shop/roku_shop.json` |
| Puzzle state SC-07 | 5 | Water level transitions match `PUZZLE_DESIGN.md` |
| Ending choice gate | 6 | Each choice sets correct ending flag |

### 3.4 Writing new unit tests (GodotPrompter)

GodotPrompter authors test files. **Do not** use GDAI MCP for test scripts.

```gdscript
# game/tests/unit/test_example.gd
class_name TestExample
extends RefCounted

static func test_addition() -> String:
	if 1 + 1 != 2:
		return "expected 2"
	return ""
```

Register new test classes in `test_runner.gd` → `_collect_tests()`.

---
