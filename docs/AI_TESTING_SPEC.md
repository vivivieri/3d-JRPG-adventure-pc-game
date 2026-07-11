# AI Testing Specification

**Version:** 1.1  
**Applies to:** All implementation on `main` (Phases 1–8)  
**Parent doc:** `docs/AI_DEV_WORKFLOW.md` (build policy + acceptance criteria)  
**Cross-refs:** `AGENTS.md`, `docs/PLAYTEST_SCRIPT.md`, `docs/QA_AND_BUG_PROCESS.md`, `docs/FLOW_QA.md`, `docs/QA_REMEDIATION_LOOP.md`

This document is the **detailed spec** for AI agent testing. It defines **how** to run each layer (L0–L5) and when humans may begin QA.

---

## 0. Golden rule — human QA comes last

```
L0 → L1 → L2 → L3 → L4 → L5  (all AI — must pass)
         ↓
L6 Human QA  (only after L0–L5 green on release candidate)
```

| Rule | Detail |
|------|--------|
| **No human playtest for ship** until `bash tools/run_e2e_playthrough.sh` exits 0 | L5 is the final AI gate |
| **No human sign-off** until L0–L5 all pass on the same commit | Same `main` SHA for AI + human |
| **Agents must not** ask humans to playtest to debug incomplete AI coverage | Fix via L0–L5 first |
| **Phase 1–7 work** uses L0–L4 (and L5 at Phase 6); humans do not run `PLAYTEST_SCRIPT.md` mid-rebuild |

Human QA (`docs/PLAYTEST_SCRIPT.md`) is **Phase 8 / ship gate only**, and **always after** the full AI automated suite.

---

## 1. Test layer summary

| Layer | Command / tool | Frequency | Blocks |
|-------|----------------|-----------|--------|
| **L0** | `python3 tools/validate_story_data.py` | Every commit | — |
| **L1** | `bash tools/run_unit_tests.sh` | Every commit | — |
| **L2** | `bash tools/run_playtest_smoke.sh` | Every commit | — |
| **L3** | GDAI MCP (see §3) | Every scene/visual task | — |
| **L4** | `bash tools/run_integration_tests.sh` | Phase gates 2–6 | Phase advance |
| **L5** | `bash tools/run_e2e_playthrough.sh` | Phase 6 complete + release candidate | **Human QA** |
| **L6** | `docs/PLAYTEST_SCRIPT.md` | After L5 on RC | **Ship** |

---

## 2. L0 — Data validation

**Runner:** `python3 tools/validate_story_data.py`  
**Owner:** AI agent  
**Exit:** 0 = pass

### Checks (automated)

- Scene IDs in `scenes.json` match dialogue / encounter references  
- Flag names in `flags.json` referenced by quests exist  
- Item IDs in shop/encounters exist in `items.json`  
- Enemy/skill IDs cross-reference  

### Agent report line

```
[L0] validate_story_data: PASS (0 errors)
```

**On FAIL:** `bash tools/qa_emit_remediation.sh data-story` — fix `game/data/` per brief; do not patch runtime without data fix when L0 fails.

---

## 3. L1 — Unit tests

**Runner:** `bash tools/run_unit_tests.sh`  
**Owner:** GodotPrompter writes tests; AI agent runs them  
**Location:** `game/tests/unit/`

### Current tests (Phase 0)

| Test ID | File | Asserts |
|---------|------|---------|
| `story_data_paths.required_boot_paths_exist` | `test_story_data_paths.gd` | Boot-required JSON files exist |
| `story_data_paths.core_data_catalog_exists` | `test_story_data_paths.gd` | Catalog files exist |
| `story_data_json.scenes_json_parses` | `test_story_data_json.gd` | `scenes.json` structure valid |
| `story_data_json.flags_json_parses` | `test_story_data_json.gd` | `flags.json` parses |
| `story_data_json.chapter_01_dialogue_parses` | `test_story_data_json.gd` | Dialogue JSON valid |

### Tests to add by phase

| Phase | New test file | Minimum cases |
|-------|---------------|---------------|
| 2 | `test_game_manager.gd` | `load_json` valid/invalid paths |
| 2 | `test_save_system.gd` | Round-trip one flag |
| 3 | `test_flag_system.gd` | Set/get/clear flags |
| 3 | `test_dialogue_runner.gd` | Advance to line ID |
| 4 | `test_damage_calculator.gd` | 3 worked examples from `COMBAT_SYSTEMS.md` |
| 4 | `test_turn_order.gd` | Speed sort fixture |
| 5 | `test_water_puzzle.gd` | SC-07 state transitions |
| 6 | `test_ending_flags.gd` | Each choice sets correct ending flag |

### Agent report line

```
[L1] unit tests: 5/5 PASS
```

---

## 4. L2 — Smoke tests

**Runner:** `bash tools/run_playtest_smoke.sh`  
**Owner:** AI agent  
**Includes:** L0 + L1 + dev environment + boot headless load

### Checks

| # | Check |
|---|--------|
| 1 | Story data validates (L0) |
| 2 | Unit tests pass (L1) |
| 3 | Dev environment healthy (`check_dev_environment.sh`) |
| 4 | Boot scene loads headless 3s |

### Agent report line

```
[L2] smoke: 4/4 PASS
```

---

## 5. L3 — GDAI editor verify

**Runner:** GDAI MCP (no shell script — procedural)  
**Owner:** AI agent  
**When:** Every task that touches scenes, materials, lights, or runtime behavior

### 5.1 Prerequisites

```bash
bash tools/ensure_gdai_mcp.sh
# godot-mcp connected; HTTP :3571 OK
```

### 5.2 Standard procedure (every scene task)

| Step | GDAI MCP action | Pass criterion |
|------|-----------------|----------------|
| 1 | Open target `.tscn` or run main scene | Scene opens without load errors |
| 2 | **UI discovery** (menus/HUD) — scan live scene tree for `Control` nodes | Every interactive label found with text + visible state (see §11) |
| 3 | Read Godot **Output** panel | Zero errors; warnings documented if unavoidable |
| 4 | **F5** play scene (or main flow to scene) | No crash; reaches expected state |
| 5 | Read **Debugger** if scripts changed | No unhandled exceptions |
| 6 | **Runtime action sequence** if UI/combat (keypress batch + waits) | Menu opens, selection succeeds (see §11.2) |
| 7 | Capture viewport **screenshot** | Save to `artifacts/screenshots/`; vision jury per `docs/VISUAL_QA.md` §2G |
| 8 | For zones: verify WorldEnvironment | Filmic tonemap, fog per `RENDERING_GUIDE.md` |
| 9 | Stop scene | Clean exit |

### 5.3 Checklists by task type

#### Zone / environment (Phase 1)

- [ ] Ground uses `toon_base.gdshader` (not default grey StandardMaterial3D)  
- [ ] `DirectionalLight3D` rotation and energy match `ENVIRONMENT_KITS.md` zone table  
- [ ] Fog enabled with zone density/color  
- [ ] ProceduralSky (no HDRI import)  
- [ ] Screenshot matches muted coastal palette (`ART_DIRECTION.md` §10 for ruined_village)  

#### UI scene (Phase 2–3)

- [ ] Control anchors correct at 1920×1080  
- [ ] No pink missing-font boxes  
- [ ] Focus navigation works (keyboard)  

#### Combat scene (Phase 4)

- [ ] Combat UI visible; HP/MP bars update on damage  
- [ ] **GDAI UI discovery** finds BattleMenu / action list nodes  
- [ ] **Action sequence:** `ui_down` × N → `ui_accept` opens Skills; screenshot shows no text overlap  
- [ ] Action menu opens; skill selection does not soft-lock  
- [ ] Battle log shows last action  
- [ ] **Edge case (runtime inject):** set player HP to 1 mid-fight → game over screen triggers on death (§11.3)  

#### Boss / ending (Phase 5–6)

- [ ] Phase banner appears on boss phase change  
- [ ] SC-16 choice UI blocks attack input (`ENDING_DESIGN.md`)  

### 5.4 Failure handling

1. Copy exact Output/Debugger text into session notes  
2. GodotPrompter fixes `.gd` / `.gdshader`  
3. GDAI MCP reapplies and re-runs steps 1–7  
4. Do not mark task done until L3 pass **and** `docs/VISUAL_QA.md` report template filled

### Agent report line

```
[L3] GDAI verify: ruined_village.tscn F5 PASS, 0 errors, screenshot artifacts/screenshots/phase1_ruined_village.png
```

---

## 6. L4 — AI integration tests

**Runner:** `bash tools/run_integration_tests.sh`  
**Owner:** GodotPrompter writes `game/tests/integration/*.gd`; AI agent runs at phase gates  
**When:** End of Phases 2, 3, 4, 5, 6 (and after any regression fix to flows)

### 6.1 Current (Phase 0 baseline)

| Scenario ID | Description | Status |
|-------------|-------------|--------|
| `INT-BOOT-01` | Main scene loads headless 3s | ✅ Implemented |

### 6.2 Scenarios to implement

#### Phase 2 — Core shell

| ID | Scenario | Steps | Assert |
|----|----------|-------|--------|
| `INT-MENU-01` | New game start | Main menu → New Game | `beach_shore` active; `game_started` flag |
| `INT-ZONE-01` | Beach → village | Transition beach_shore → ruined_village | No error; zone loaded |
| `INT-SAVE-01` | Well save round-trip | Set flag at well → save → reload | Flag persists |

#### Phase 3 — Narrative

| ID | Scenario | Steps | Assert |
|----|----------|-------|--------|
| `INT-DLG-01` | SC-03 dialogue | Trigger torii interact | Speaker label non-empty |
| `INT-QUEST-01` | Q1 stage 1 | Inspect banner + sandal + well | Quest stage advances |
| `INT-FIELD-01` | SC-01–SC-05 | Scripted movement + interacts | No soft-lock |

#### Phase 4 — Combat

| ID | Scenario | Steps | Assert |
|----|----------|-------|--------|
| `INT-CMB-01` | Salt Crab tutorial | SC-05 encounter | Combat ends win; `tutorial_combat_done` |
| `INT-CMB-02` | One full turn | Attack → enemy turn | HP changes; log entry |

#### Phase 5 — Dungeons

| ID | Scenario | Steps | Assert |
|----|----------|-------|--------|
| `INT-PUZ-01` | SC-07 water puzzle | Raise/lower water | `water_puzzle_solved`; saber granted |
| `INT-BOSS-01` | Shore Wraith | SC-09 fight | Win path grants `wraith_pearl` |
| `INT-PARTY-01` | Yuzu joins | SC-10 | Party size 2 |

#### Phase 6 — Story complete (pre-E2E)

| ID | Scenario | Steps | Assert |
|----|----------|-------|--------|
| `INT-GATE-01` | Palace gate | Enter with pearl | Gate opens |
| `INT-BOSS-02` | Sentinel + Keeper | Boss sequence | Reach SC-16 choice |

### 6.3 Implementation notes

- **Hybrid model:** L4 uses **headless GDScript** for deterministic flag/math checks **plus** **GDAI MCP** for UI menus the headless runner cannot see (inventory, combat menus, dialogue).  
- Headless Godot with scripted `Input` simulation **or** GDAI batched keypresses + timed waits  
- JRPG sub-menus (Equipment, Skills, Items, Save): always **discover UI tree first**, then simulate navigation (§11)  
- Each scenario returns pass/fail; runner exits non-zero on any fail  
- Wire new scenarios in `tools/run_integration_tests.sh` as they land  

### Agent report line

```
[L4] integration: 12/12 PASS
```

**On scenario FAIL:** `bash tools/qa_emit_remediation.sh flow-scenario INT-<ID>` — see `docs/FLOW_QA.md`.

---

## 7. L5 — AI E2E playthrough

**Runner:** `bash tools/run_e2e_playthrough.sh`  
**Owner:** GodotPrompter + AI agent  
**When:** Phase 6 gate complete; **required again** on every release candidate before human QA  
**Blocks:** L6 human QA

### 7.1 Scope

Full story automation per `game/data/story/scenes.json`:

- Acts I–III playable without soft-lock  
- All three endings: **Rewind**, **Anchor**, **Drift**  
- Credits after each ending  
- **GDAI MCP** drives field movement, dialogue advance, combat menus, and shop where headless scripts are brittle  
- Optional: record video to `artifacts/videos/e2e_<ending>_<date>.mp4`

### 7.2 E2E matrix (implement in `game/tests/e2e/`)

| Run ID | Path | Key scenes | Ending flag |
|--------|------|------------|-------------|
| `E2E-REWIND` | Full story → choice A | SC-00 … SC-16 → ending_rewind | `ending_rewind_seen` |
| `E2E-ANCHOR` | Full story → choice B | SC-00 … SC-16 → ending_anchor | `ending_anchor_seen` |
| `E2E-DRIFT` | Full story → choice C | SC-00 … SC-16 → ending_drift | `ending_drift_seen` |

### 7.3 Per-scene beat checklist (agent implements script)

| Scene | Action | Flag / assert |
|-------|--------|---------------|
| SC-00 | Auto-play prologue | `prologue_seen` |
| SC-01 | Move to village trigger | `tutorial_movement_done` |
| SC-02 | Enter village hub | `village_arrival_seen` |
| SC-03 | Torii interact | `met_yuzu_spirit` |
| SC-04 | Roku dialogue | `met_roku`, `cave_entrance_unlocked` |
| SC-05 | Win tutorial combat | `tutorial_combat_done` |
| SC-06 | Enter caves | `caves_entered` |
| SC-07 | Solve water puzzle | `water_puzzle_solved` |
| SC-09 | Defeat Shore Wraith | `shore_wraith_defeated` |
| SC-10 | Yuzu joins | `yuzu_joined` |
| SC-12–15 | Palace progression | Per `scenes.json` flags |
| SC-16 | Choice UI | Correct ending flag per run |
| Credits | Roll to completion | Scene exits cleanly |

### 7.4 Pass criteria

| # | Criterion |
|---|-----------|
| 1 | `run_e2e_playthrough.sh` exit 0 |
| 2 | All three runs (`E2E-REWIND`, `E2E-ANCHOR`, `E2E-DRIFT`) pass |
| 3 | No S0 soft-locks (see `QA_AND_BUG_PROCESS.md`) |
| 4 | L0–L4 also pass on same commit |

### 7.5 Current status

**Not implemented** — stub exits 0 with `[SKIP]`. Implement at Phase 6.  
Until L5 is real, **do not start human QA**.

### Agent report line

```
[L5] E2E: E2E-REWIND PASS, E2E-ANCHOR PASS, E2E-DRIFT PASS (3/3)
```

---

## 8. L6 — Human QA (after all AI playthrough)

**Runner:** Human tester + `docs/PLAYTEST_SCRIPT.md`  
**Owner:** Human (not AI)  
**Prerequisite:** L0–L5 all PASS on release candidate commit

### 8.1 Entry checklist (before human starts)

- [ ] `git rev-parse HEAD` recorded  
- [ ] `bash tools/run_playtest_smoke.sh` → PASS  
- [ ] `bash tools/run_integration_tests.sh` → PASS  
- [ ] `bash tools/run_e2e_playthrough.sh` → PASS (not SKIP)  
- [ ] Windows build exists (Phase 8) OR Godot F5 build for PC tester  
- [ ] GDAI MCP disabled for player build  

### 8.2 What humans test (AI cannot replace)

| Area | Why human |
|------|-----------|
| Game feel, pacing, emotional beats | Subjective |
| Localization quality (en/ja/zh) | Nuance, typography |
| Audio mix, BGM loops | Listening |
| Controller comfort | Physical |
| “Fun” and difficulty feel | Design judgment |

### 8.3 Exit criteria (ship gate)

| Metric | Target |
|--------|--------|
| Complete without guide | ≥80% testers |
| Understand 3 endings | Post-survey |
| Soft-lock | Zero S0 |
| Boss attempts (Normal) | ≤3 |

See `docs/PLAYTEST_SCRIPT.md` for step-by-step script.

### 8.4 Bug flow

Human findings → `docs/QA_AND_BUG_PROCESS.md` → AI agent fixes → **re-run L0–L5** → human retest affected paths only.

---

## 9. Phase → required test layers

| Phase | Layers required before phase sign-off |
|-------|--------------------------------------|
| 0 | L0, L1, L2, L3 (boot) |
| 1 | L0–L3 |
| 2 | L0–L4 |
| 3 | L0–L4 |
| 4 | L0–L4 |
| 5 | L0–L4 |
| 6 | L0–L5 |
| 7 | L0–L5 (+ asset compliance) |
| 8 | L0–L5 on RC → **then L6 human** → export |

**Human QA never runs before Phase 6 L5 is implemented and passing.**

---

## 10. Agent session report template

Copy into PR or session summary:

```markdown
## AI test report — <phase/task>

Commit: <sha>
GDAI MCP: connected / NOT AVAILABLE (blocked)

| Layer | Result | Detail |
|-------|--------|--------|
| L0 | PASS/FAIL | validate_story_data |
| L1 | PASS/FAIL | N/N unit tests |
| L2 | PASS/FAIL | N/N smoke checks |
| L3 | PASS/FAIL/SKIP | <scene> F5, screenshot path |
| L4 | PASS/FAIL/SKIP | N/N integration scenarios |
| L5 | PASS/FAIL/SKIP | E2E 3/3 endings |

Human QA: NOT STARTED (L5 prerequisite) / READY FOR HUMAN / N/A
```

---

## 11. GDAI MCP playtesting toolkit (adopted)

These techniques come from live-runtime MCP testing (recommended for JRPG UI-heavy flows). They extend L3–L5; they **do not** replace L0–L2 headless tests.

### 11.1 Adoption matrix (external advice → this project)

| Technique | Adopt? | Layer | Notes |
|-----------|--------|-------|-------|
| **UI tree discovery** (live `Control` scan) | ✅ Yes | L3, L4 | Required for Equipment / Skills / Items / Save menus |
| **Runtime action sequences** (keypress + wait batches) | ✅ Yes | L3, L4, L5 | `ui_down`, `ui_accept`, `interact`, movement keys |
| **Viewport screenshots + visual review** | ✅ Yes | L3, L4 | Agent analyzes overlap, clipping, missing fonts |
| **Runtime GDScript injection** | ✅ Yes | L4, L5 | Edge cases: HP=1, boss phase, grant item, set flag |
| **GodotPrompter for test code** | ✅ Yes | L1, L4 | Already policy — Godot 4 APIs only, no Unity-style tests |
| **GUT (Godot Unit Test)** | ⚠️ Optional | L1 | Keep lightweight `test_runner.gd`; GUT optional Phase 4+ |
| **Godot MCP Pro** | ✅ Yes | L4, L5 | `run_test_scenario`, `assert_screen_text`, `compare_screenshots` — **test role only** (`--minimal`) |
| **Godotiq** | ✅ Yes | L3–L5 | `godotiq_signal_map`, `godotiq_trace_flow`, `godotiq_ui_map`, `godotiq_read_debug_console`, `godotiq_verify_project_runs` |
| **LimboAI / Beehave** | ❌ No (v1) | — | Turn-based enemy AI is **data-driven** (`enemies.json`) |

### 11.2 UI discovery + action sequences

**When:** Any JRPG menu, combat action select, shop, tab inventory, ending choice UI.

**Procedure:**

1. GDAI MCP: run game to target state (F5 or run scene).  
2. **Discover UI elements** — walk live scene tree; collect `Control` text, name, position, `visible`, focus.  
3. Plan key sequence from discovered nodes (do not hard-code stale node paths from `.tscn` files).  
4. Execute batched input, e.g.:

```
Open inventory → wait 0.5s → ui_down × 3 → ui_accept → verify Equipment label updated
```

5. Screenshot immediately after; agent checks layout + Output panel.

**JRPG menus to cover (Phase 2–4):**

| Menu | Min action sequence |
|------|---------------------|
| Main menu | New Game → zone load |
| Field HUD | Open quest tracker; close |
| Dialogue | Advance to end; no soft-lock |
| Combat | Attack → Skill → Item → Defend paths |
| Shop (Roku) | Buy + sell one item |
| Save / load | Well save → menu continue |

### 11.3 Runtime GDScript injection (edge cases)

Use GDAI MCP to execute **short** runtime scripts for states hard to reach organically.

| Test ID | Inject example | Assert |
|---------|----------------|--------|
| `INJ-GAMEOVER-01` | Set party leader HP to 0 | Game over UI; reload works |
| `INJ-BOSS-01` | Set boss to phase 2 HP threshold | Phase banner + intent change |
| `INJ-FLAG-01` | `GameManager.set_flag("water_puzzle_solved")` | Gate opens without replaying puzzle |
| `INJ-ENDING-01` | Jump to SC-16 with Tide Keeper at low HP | Choice UI blocks attack input |

**Rules:**

- GodotPrompter writes inject snippets; GDAI MCP runs them in live session.  
- Log inject script in test report.  
- Prefer **unit tests** for pure math; use inject only for **UI / state integration**.

### 11.4 Example agent prompts (copy-paste)

**Combat UI smoke (Phase 4):**

```
Using GDAI MCP only: run the project, enter SC-05 tutorial combat.
Discover UI elements for the battle action menu.
Simulate ui_down twice and ui_accept to open Skills.
Capture a viewport screenshot and read the Output panel.
Report any overlapping UI text, errors, or soft-lock.
```

**Inventory equip (Phase 2+):**

```
Using GDAI MCP: from field, open the tab menu inventory.
Discover Equipment list Controls.
Navigate down 3 times, press ui_accept to equip the training sword.
Screenshot the stats panel and confirm ATK changed per items.json.
```

**Boss game-over edge case:**

```
Using GDAI MCP: start Shore Wraith encounter (SC-09).
Inject runtime GDScript to set Urashima HP to 1.
Take one enemy action that deals damage.
Verify game over screen appears and Continue returns to last save.
```

### 11.5 Division of labor (MCP stack)

| Concern | Tool |
|---------|------|
| Fire spell damage 25–30 vs fire-weak enemy | **L1 unit test** |
| Skills menu opens and lists skills | **GDAI** or **Godotiq** `godotiq_ui_map` |
| Why turn order stuck after enemy action | **Godotiq** `godotiq_trace_flow` |
| Automated scenario + on-screen text assert | **Godot MCP Pro** `run_test_scenario`, `assert_screen_text` |
| Full story three endings | **L5** headless + **Godot MCP Pro** input replay |
| Create/edit zone scene | **GDAI only** (`docs/MCP_STACK.md`) |
| JSON flag after quest stage | **L1 unit test** |

See `docs/MCP_STACK.md` for conflict rules and install.

---

## 12. Optional: GUT unit tests (Phase 4+)

If `game/tests/unit/` becomes crowded, adopt **[GUT](https://github.com/bitwes/Gut)** (Godot Unit Test):

- GodotPrompter writes GUT test scripts per `COMBAT_SYSTEMS.md` worked examples.  
- Run headless: `godot4 --headless -s addons/gut/gut_cmdln.gd` (after plugin install).  
- Wire into `tools/run_unit_tests.sh`.  

**Until then:** keep the lightweight `test_runner.gd` scaffold on `main`.

---

## 13. Related files

| Path | Role |
|------|------|
| `tools/run_unit_tests.sh` | L1 |
| `tools/run_playtest_smoke.sh` | L2 |
| `tools/run_integration_tests.sh` | L4 |
| `tools/run_e2e_playthrough.sh` | L5 |
| `game/tests/unit/` | L1 tests |
| `game/tests/integration/` | L4 tests (to add) |
| `game/tests/e2e/` | L5 tests (to add) |
| `docs/PLAYTEST_SCRIPT.md` | L6 human script |
| `docs/AI_DEV_WORKFLOW.md` | Build policy + acceptance criteria |
