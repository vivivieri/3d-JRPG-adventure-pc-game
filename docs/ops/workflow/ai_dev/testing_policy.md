---
id: testing-policy
type: how-to
audience: [pm, architect]
status: active
authority: workflow
tokens_est: 1520
summary: "Testing is **layered**. Higher layers run after lower layers pass."
---
# AI Dev Workflow — testing policy

**Hub:** [`AI_DEV_WORKFLOW.md`](../AI_DEV_WORKFLOW.md)

## 2. AI testing policy

Testing is **layered**. Higher layers run after lower layers pass.

**Golden rule:** **Human QA (L6) runs only after all AI playthrough layers (L0–L5) pass** on the same release-candidate commit. See `docs/ops/qa/AI_TESTING_SPEC.md` §0.

**L2.5 (optional):** Champion/challenger zone tournaments run **before merge** when policy requires — `docs/ops/qa/CANDIDATE_TOURNAMENT.md`. Non-ship; does not replace L0–L5.

| Layer | Runner | Who runs it | Purpose |
|-------|--------|-------------|---------|
| **L0 — Data validation** | `python3 tools/validate_story_data.py` + base-class validators | AI agent (every commit) | JSON schema, cross-refs, scene IDs, `base_classes.json` |
| **L1 — Unit tests + lint** | `bash tools/run_unit_tests.sh` + `check_gdscript_changed.sh` | AI agent (every commit) | Pure logic, parsers, calculators, flags; `gdlint` on changed `.gd` |
| **L2 — Smoke tests** | `bash tools/run_playtest_smoke.sh` | AI agent (every commit) | Boot, lint; primitives, animation whitelist, feel smoke, GLB import, visual/audio/model smoke when assets exist |
| **L2.5 — Candidate tournament** | `bash tools/run_candidate_tournament.sh` | Builder / Visual (when policy requires) | Champion/challenger golden harness compare — pre-merge only (`CANDIDATE_TOURNAMENT.md`) |
| **L3 — GDAI editor verify** | GDAI MCP F5 + viewport | AI agent (per scene task) | Visual layout, materials, runtime errors in editor |
| **L4 — AI integration tests** | `bash tools/run_integration_tests.sh` | AI agent (phase gate) | Multi-scene flows, combat round, save/load |
| **L5 — AI E2E playthrough** | `REQUIRE_L5=1 bash tools/run_e2e_playthrough.sh` | AI agent (Phase 6 gate + every RC) | Full story + 3 endings (headless or recorded) |
| **L6 — Human QA** | `docs/ops/qa/PLAYTEST_SCRIPT.md` | Human (**after L0–L5 pass**) | Feel, pacing, localization — **ship gate only** |

**GitHub CI** (`.github/workflows/ci.yml`): runs headless subset via `bash tools/run_docs_ci_checks.sh` on `main`.
**Game CI** (`game-ci.yml` on `game/development`): `bash tools/run_ci_checks.sh`.
**Environments & multi-agent:** `docs/ops/ci-cd/ENVIRONMENTS.md`, `docs/ops/agents/MULTI_AGENT_TEAM.md`, `docs/ops/agents/PROJECT_MANAGEMENT.md`.

### 2.1 AI agent obligations

Before marking **any** implementation task done, the agent must:

1. Run L0 + L1 + L2 (always)
2. Run L3 for any scene/visual change
3. Run L4 when the phase acceptance criteria require it
4. Run L5 when Phase 6 is complete and on every release candidate
5. **Do not request human QA until L0–L5 all pass**
6. Report pass/fail counts in the PR or session summary (template: `docs/ops/qa/AI_TESTING_SPEC.md` §10)
7. **Never** claim “tested” based only on code review

### 2.2 Headless vs editor

| Concern | Tool |
|---------|------|
| Scene tree, materials, lighting | **GDAI MCP** (editor) — headless cannot replace |
| JSON loading, damage math, flag logic | **Unit tests** (headless) |
| Scene loads without crash | **Smoke / integration** (headless) |
| Art checklist (palette, fog, silhouettes) | **GDAI MCP** screenshot + `ART_DIRECTION.md` checklist (AI); human art sign-off post-L5 / Phase 7 |

### 2.3 Test artifacts

Agents should save evidence for phase gates:

```
artifacts/
  screenshots/     # GDAI viewport captures at acceptance checkpoints
  videos/            # E2E playthrough recordings (Phase 6+)
  test-reports/      # Optional junit-style logs from run_unit_tests.sh
```

---

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

