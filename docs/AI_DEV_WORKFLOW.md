# AI Dev Workflow — Build, Test & Acceptance Criteria

**Version:** 1.1  
**Applies to:** `main` clean baseline → Phases 1–8 rebuild  
**Cross-refs:** `.cursorrules` §0, `AGENTS.md`, `docs/GDAI_CLOUD_SETUP.md`, `docs/AI_TESTING_SPEC.md`, `docs/IMPLEMENTATION_PLAN.md`, `docs/QA_AND_BUG_PROCESS.md`

This document is the **single source of truth** for:

1. **AI build policy** — how Cursor agents implement the game  
2. **AI testing policy** — what agents must verify automatically vs manually (`docs/AI_TESTING_SPEC.md` for L3–L5 detail)  
3. **Unit tests** — headless GDScript tests for logic and data  
4. **Acceptance criteria** — measurable phase gates (`docs/ACCEPTANCE_CRITERIA.md`, `game/data/qa/acceptance_criteria.json`)

---

## 1. AI build policy

### 1.1 Mandatory toolchain

| Tool | Role | Allowed outputs |
|------|------|-----------------|
| **GodotPrompter** (Cursor) | Plan, architect, write GDScript, shaders, test scripts | `.gd`, `.gdshader`, Python tools, docs |
| **GDAI MCP** (`godot-mcp`) | All editor work | `.tscn`, nodes, materials, lights, inspector values, F5 playtest |

**Rule:** No hand-edited `.tscn` or inspector-only work in Cursor. If GDAI MCP is unavailable → **stop and notify the user**. Do not fall back to manual scene edits.

### 1.2 Session startup (every agent run)

```bash
bash tools/ensure_gdai_mcp.sh
```

Both must be true before implementation:

| Check | How |
|-------|-----|
| GDAI HTTP bridge | `curl -sf http://127.0.0.1:3571/tools` returns JSON |
| Cursor MCP | `godot-mcp` connected (desktop Settings or cloud dashboard) |
| Godot Editor | Running with `game/project.godot` open |

### 1.3 Build loop (per task)

```
1. Read design doc section for the task
2. GodotPrompter — draft GDScript / shaders / unit tests
3. GDAI MCP — apply scenes, nodes, materials in live editor
4. GDAI MCP — F5 run scene; read Output / debugger; fix until clean
5. Run automated tests (§3)
6. Confirm acceptance criteria for current phase (§4)
7. Commit + push
```

### 1.4 What AI agents must not do

- Import unknown-license art, audio, or models from the web  
- Hand-edit `.tscn` when GDAI MCP is available  
- Ship with GDAI MCP plugin enabled (dev-only; remove before export)  
- Mark a phase complete without passing its acceptance criteria  

---

## 2. AI testing policy

Testing is **layered**. Higher layers run after lower layers pass.

**Golden rule:** **Human QA (L6) runs only after all AI playthrough layers (L0–L5) pass** on the same release-candidate commit. See `docs/AI_TESTING_SPEC.md` §0.

| Layer | Runner | Who runs it | Purpose |
|-------|--------|-------------|---------|
| **L0 — Data validation** | `python3 tools/validate_story_data.py` | AI agent (every commit) | JSON schema, cross-refs, scene IDs |
| **L1 — Unit tests** | `bash tools/run_unit_tests.sh` | AI agent (every commit) | Pure logic, parsers, calculators, flags |
| **L2 — Smoke tests** | `bash tools/run_playtest_smoke.sh` | AI agent (every commit) | Boot, lint; visual + audio + model smoke when assets exist |
| **L3 — GDAI editor verify** | GDAI MCP F5 + viewport | AI agent (per scene task) | Visual layout, materials, runtime errors in editor |
| **L4 — AI integration tests** | `bash tools/run_integration_tests.sh` | AI agent (phase gate) | Multi-scene flows, combat round, save/load |
| **L5 — AI E2E playthrough** | `bash tools/run_e2e_playthrough.sh` | AI agent (Phase 6 gate + every RC) | Full story + 3 endings (headless or recorded) |
| **L6 — Human QA** | `docs/PLAYTEST_SCRIPT.md` | Human (**after L0–L5 pass**) | Feel, pacing, localization — **ship gate only** |

### 2.1 AI agent obligations

Before marking **any** implementation task done, the agent must:

1. Run L0 + L1 + L2 (always)  
2. Run L3 for any scene/visual change  
3. Run L4 when the phase acceptance criteria require it  
4. Run L5 when Phase 6 is complete and on every release candidate  
5. **Do not request human QA until L0–L5 all pass**  
6. Report pass/fail counts in the PR or session summary (template: `docs/AI_TESTING_SPEC.md` §10)  
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

## 4. Acceptance criteria by phase

A phase is **done** only when **every** criterion below passes. AI agents must check each item explicitly.

### Phase 0 — Dev environment ✅ (baseline)

| # | Criterion | Verification |
|---|-----------|--------------|
| 0.1 | `bash tools/ensure_gdai_mcp.sh` succeeds | Script exit 0; HTTP `:3571` returns tools |
| 0.2 | `python3 tools/validate_story_data.py` passes | Exit 0 |
| 0.3 | `bash tools/run_unit_tests.sh` passes | Exit 0; all registered tests green |
| 0.4 | `bash tools/run_playtest_smoke.sh` passes | Exit 0 |
| 0.5 | F5 boot screen loads; no missing-data errors in Output | GDAI MCP F5 |
| 0.6 | `.cursorrules` §0 and this doc linked from `README.md` | File review |

### Phase 1 — Environment foundation

| # | Criterion | Verification |
|---|-----------|--------------|
| 1.1 | `ruined_village.tscn` exists and loads headless | Smoke/integration |
| 1.2 | WorldEnvironment matches `RENDERING_GUIDE.md` (Filmic tonemap, zone fog) | GDAI screenshot + art checklist `ART_DIRECTION.md` §10 |
| 1.3 | `toon_base.gdshader` on ground meshes; no flat default grey | GDAI viewport |
| 1.4 | `zone_visuals.gd` applies palette from `ENVIRONMENT_KITS.md` §2 | Unit test + GDAI F5 |
| 1.5 | DirectionalLight + fog values match zone table | GDAI inspector readback |
| 1.6 | ProceduralSky (no HDRI) per `RENDERING_GUIDE.md` §4 | GDAI viewport |
| 1.7 | Greybox scenes exist for all 4 zones; each loads headless | Integration test |
| 1.8 | L0 + L1 + L2 + L3 pass after every commit | CI scripts |
| 1.9 | **Vertical slice gate:** SC-02 Ruined Village passes `ART_DIRECTION.md` §10 checklist | AI screenshot in `artifacts/screenshots/` + L3 pass |

### Phase 2 — Core systems shell

| # | Criterion | Verification |
|---|-----------|--------------|
| 2.1 | Autoloads: `GameManager`, `EventBus`, `SaveSystem`, `DialogueRunner`, `CombatManager` | Project settings + unit tests |
| 2.2 | `GameManager.load_json("res://data/...")` works for all data types | Unit test |
| 2.3 | Main menu → New Game → `beach_shore` without errors | GDAI F5 + integration test |
| 2.4 | Player WASD + camera orbit per `GAME_FEEL.md` | GDAI F5 |
| 2.5 | Zone transitions per `WORLD_MAP_AND_FLOW.md` | Integration `test_zone_transitions.gd` |
| 2.6 | Save at village well → reload → flags persist | Unit + integration |
| 2.7 | L0–L4 pass | All test scripts |

### Phase 3 — Narrative & exploration

| # | Criterion | Verification |
|---|-----------|--------------|
| 3.1 | Dialogue box shows speaker + body from `chapter_01.json` | GDAI F5 SC-03 |
| 3.2 | Interactable prompt (E) per `UI_UX_FLOW.md` | GDAI F5 |
| 3.3 | Quest stages advance per `main_quests.json` | Unit `test_flag_system.gd` |
| 3.4 | SC-01 through SC-05 reachable without soft-lock | Integration test |
| 3.5 | 8 lore entries discoverable per `lore_placements.json` | Integration test |
| 3.6 | L0–L4 pass | All test scripts |

### Phase 4 — Combat vertical slice

| # | Criterion | Verification |
|---|-----------|--------------|
| 4.1 | Combat UI: HP/MP, action menu, battle log, enemy intent | GDAI F5 |
| 4.2 | SC-05 Salt Crab tutorial completable | Integration `test_combat_round.gd` |
| 4.3 | Damage matches `COMBAT_SYSTEMS.md` worked examples | Unit `test_damage_calculator.gd` |
| 4.4 | Turn order by speed per `SKILLS_BIBLE.md` | Unit test |
| 4.5 | Boss framework shows phase banner | GDAI F5 |
| 4.6 | L0–L4 pass | All test scripts |

### Phase 5 — Chapter 1 dungeons

| # | Criterion | Verification |
|---|-----------|--------------|
| 5.1 | `tidal_caves.tscn` art pass per `ENVIRONMENT_KITS.md` §5 | GDAI screenshot |
| 5.2 | SC-07 water puzzle: silent, no VO; state machine matches `PUZZLE_DESIGN.md` | Unit + GDAI F5 |
| 5.3 | Shore Wraith SC-09 win/lose paths | Integration test |
| 5.4 | Yuzu joins at SC-10; party size = 2 | Flag unit test |
| 5.5 | L0–L4 pass | All test scripts |

### Phase 6 — Full story & endings

| # | Criterion | Verification |
|---|-----------|--------------|
| 6.1 | Dragon Palace Gate zone per `ENVIRONMENT_KITS.md` §6 | GDAI + screenshot |
| 6.2 | Palace Sentinel + Tide Keeper per `BOSS_DESIGNS.md` | Integration test |
| 6.3 | SC-16 choice UI blocks attack input per `ENDING_DESIGN.md` | GDAI F5 |
| 6.4 | All 3 endings reachable: Rewind, Anchor, Drift | E2E `test_three_endings.gd` |
| 6.5 | Credits roll after each ending | E2E test |
| 6.6 | `bash tools/run_e2e_playthrough.sh` passes | Exit 0 |
| 6.7 | L0–L5 pass | All test scripts |

### Phase 7 — M6 art rebuild

| # | Criterion | Verification |
|---|-----------|--------------|
| 7.1 | No primitive/Kenney placeholder art in shipping scenes | `check_asset_compliance.sh` + human review |
| 7.2 | Hero meshes: Urashima, Yuzu, Roku per `CHARACTER_BIBLE.md` | Screenshot gate |
| 7.3 | Automated stylized zone textures per zone (`palette_remap.py`) | Art checklist |
| 7.4 | Curated BGM per `AUDIO_PRODUCTION_GUIDE.md` | Audio QA §11 |
| 7.5 | `bash tools/check_asset_compliance.sh` passes | Exit 0 |

### Phase 8 — Ship prep

**Order:** L0–L5 on release candidate → **then** L6 human QA → export.

| # | Criterion | Verification |
|---|-----------|--------------|
| 8.1 | GDAI MCP plugin **disabled and removed** from export tree | Manual + export preset review |
| 8.2 | Windows export succeeds (`tools/export_windows.sh`) | Artifact exists |
| 8.3 | `bash tools/check_asset_compliance.sh` passes | Exit 0 |
| 8.4 | **L0–L5 pass** on release candidate | All AI test scripts exit 0 |
| 8.5 | **Human QA** `docs/PLAYTEST_SCRIPT.md` ≥80% complete without guide | Human sign-off **after 8.4** |

---

## 5. Command cheat sheet

```bash
# Every agent session
bash tools/ensure_gdai_mcp.sh

# Every commit (L0–L2)
python3 tools/validate_story_data.py
python3 tools/validate_acceptance_criteria.py
bash tools/run_unit_tests.sh
bash tools/run_playtest_smoke.sh

# Phase gates (L4 — add scripts as phases land)
bash tools/run_integration_tests.sh

# Phase 6+ (L5 — required before human QA)
bash tools/run_e2e_playthrough.sh

# Ship — AI tests first, then human (L6)
bash tools/check_asset_compliance.sh
# Human QA only after L0–L5 pass: docs/PLAYTEST_SCRIPT.md
```

---

## 6. Related docs

| Doc | Focus |
|-----|-------|
| `docs/AI_TESTING_SPEC.md` | **Detailed L0–L6 spec**, L3 procedures, E2E matrix, human QA gate |
| `docs/GDAI_CLOUD_SETUP.md` | MCP install, cloud snapshot, editor bridge |
| `docs/IMPLEMENTATION_PLAN.md` | What to build each phase |
| `docs/QA_AND_BUG_PROCESS.md` | Bug severity, triage, human QA process |
| `docs/PLAYTEST_SCRIPT.md` | Manual 2–3 h playthrough (**after L5**) |
| `AGENTS.md` | Cloud agent quick reference |
