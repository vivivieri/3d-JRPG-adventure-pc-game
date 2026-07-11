# Game Flow QA — Progression Gates + Iterative Fix Loop

**Version:** 1.0  
**Problem:** An agent can wire a scene “done” while the **main story soft-locks**, a **quest never advances**, or **combat hangs** — then patch the same trigger logic repeatedly without fixing root cause.

**Rule:** Flow tasks pass **data validation (L0) → integration scenarios (L4) → E2E spine (L5)** before human playtest. Every FAIL produces a **flow remediation brief** with one changed lever — same as art/audio (`docs/QA_REMEDIATION_LOOP.md`).

**Cross-refs:** `docs/AI_TESTING_SPEC.md`, `docs/TECHNICAL_DESIGN.md`, `docs/QUEST_AND_FLAGS.md`, `docs/QA_REMEDIATION_LOOP.md`, `docs/ACCEPTANCE_CRITERIA.md`, `game/data/qa/remediation_playbook.json` §`flow` / §`data`

---

## 1. Industry standards we map to

| Industry practice | What it means | Our equivalent |
|-------------------|---------------|----------------|
| **Critical path testing** | Main story completable without optional content | `story/scenes.json` spine + L5 E2E three endings |
| **Scenario / acceptance testing** | Given-when-then flows with pass/fail asserts | L4 `INT-*` scenarios in `AI_TESTING_SPEC.md` §6 |
| **Milestone acceptance criteria** | Phase gate checklist before advance | `AI_DEV_WORKFLOW.md` per-phase acceptance |
| **Vertical slice playtest** | One playable hub loop before full game | Phase 1 SC-02 ruined_village + INT-ZONE/Save |
| **Functional requirements (TRC-style)** | Save works, no progression blockers, no boot crash | L2 smoke boot + INT-SAVE-01 |
| **Exploratory testing with charter** | Time-boxed “try to break progression” | Human L6 `PLAYTEST_SCRIPT.md` — **after** L5 |
| **Root-cause debugging** | Trace signals/state, not random edits | Godotiq `trace_flow` / `signal_map` before re-patch |

**References:** ISTQB scenario testing; platform manufacturer functional test categories (save data, progression); Valve playtesting (observe blockers, categorize severity).

---

## 2. Defense layers (game flow)

```
F0  validate_story_data.py     → JSON cross-refs (flags, items, dialogue)
F1  run_unit_tests.sh           → parsers, calculators, flag math
F2  run_playtest_smoke.sh       → boot + art/audio/model smoke
F4  run_integration_tests.sh    → INT-* multi-scene scenarios
F5  run_e2e_playthrough.sh      → full spine + 3 endings (Phase 6+)
F6  PLAYTEST_SCRIPT.md          → human 2–3h playthrough (ship only)
```

**Flow QA focuses on F0, F4, F5.** Art/audio/model gates run in F2 but are documented separately.

---

## 3. Integration scenarios (L4)

Implement in `game/tests/integration/` as phases land. IDs from `AI_TESTING_SPEC.md` §6:

| Phase | ID | Asserts |
|-------|-----|---------|
| 2 | `INT-MENU-01` | New game → beach; `game_started` |
| 2 | `INT-ZONE-01` | Beach → ruined_village transition |
| 2 | `INT-SAVE-01` | Well save round-trip |
| 3 | `INT-DLG-01` | SC-03 torii dialogue fires |
| 3 | `INT-QUEST-01` | Q1 stage advances after inspectables |
| 3 | `INT-FIELD-01` | SC-01–05 no soft-lock |
| 4 | `INT-CMB-01` | Salt Crab tutorial win |
| 4 | `INT-CMB-02` | Full combat turn resolves |
| 5 | `INT-PUZ-01` | SC-07 water puzzle + saber |
| 5 | `INT-BOSS-01` | Shore Wraith → `wraith_pearl` |
| 5 | `INT-PARTY-01` | Yuzu joins |
| 6 | `INT-GATE-01` | Palace gate with pearl |
| 6 | `INT-BOSS-02` | Sentinel + Tide Keeper → SC-16 |

**On scenario FAIL:**

```bash
python3 tools/qa_remediation_brief.py --flow-scenario INT-QUEST-01 --log-attempt
```

---

## 4. Flow lever taxonomy (change one per attempt)

| Lever | Fix when | Tools |
|-------|----------|-------|
| `data_fix` | L0 validation: unknown flag/item/dialogue | Edit `game/data/` JSON; re-run `validate_story_data.py` |
| `trigger_wiring` | Interactable never fires | GDAI: Area3D, signals, `interactable.gd` |
| `flag_logic` | Quest stuck, wrong branch | `QUEST_AND_FLAGS.md`; quest stage conditions |
| `combat_logic` | Combat hang, no win | Combat autoload, encounter `on_win` grants |
| `save_system` | Save/load regression | `SAVE_AND_FAIL_STATES.md`; well trigger |
| `zone_transition` | Zone load fail, wrong spawn | `LEVEL_DESIGN.md`; transition volumes |
| `ui_navigation` | Menu/dialogue soft-lock | Godotiq `ui_map`; dialogue block `on_complete` |
| `godotiq_trace` | Unknown hang after 2 blind patches | `godotiq_trace_flow`, `godotiq_signal_map` |

**Forbidden:** Re-run same integration test without changing lever. Patch random `.gd` without tracing failing scenario step.

---

## 5. Agent workflow (flow task)

```
1. READ  TECHNICAL_DESIGN.md + scene row in scenes.json
2. GodotPrompter — plan flags, triggers, encounter hooks
3. GDAI MCP — wire scene (triggers, dialogue, transitions)
4. python3 tools/validate_story_data.py
5. bash tools/run_unit_tests.sh
6. bash tools/run_integration_tests.sh  (when scenario exists)
7. On FAIL → python3 tools/qa_remediation_brief.py --flow-scenario <ID> --log-attempt
8. Change ONE flow lever; commit with scenario ID in message
9. Re-run F0 → F4 for that scenario only, then full suite
```

---

## 6. Unified iterative improvement (all domains)

```
         ┌─────────────────────────────────────────────┐
         │  BUILD (GodotPrompter plan → GDAI execute)  │
         └─────────────────────┬───────────────────────┘
                               ▼
    ┌──────────┬──────────┬──────────┬──────────┬──────────┐
    │ L0 data  │ L2 art   │ L2 audio │ L2 model │ L4 flow  │
    │ validate │ visual   │ audio    │ model    │ INT-*    │
    └────┬─────┴────┬─────┴────┬─────┴────┬─────┴────┬─────┘
         │ FAIL     │ FAIL     │ FAIL     │ FAIL     │ FAIL
         ▼          ▼          ▼          ▼          ▼
    qa_remediation_brief.py  (one lever, revision_log, max 3 attempts)
         │          │          │          │          │
         └──────────┴──────────┴──────────┴──────────┘
                               ▼
                         REBUILD vN+1
```

| Domain | QA doc | Brief trigger |
|--------|--------|---------------|
| Data / story | This doc §2 F0 | `--validate-story` |
| Game flow | This doc | `--flow-scenario INT-*` |
| 3D model | `MODEL_QA.md` | `--technical-model` / `--jury` |
| Visual | `VISUAL_QA.md` | palette / jury |
| Audio | `AUDIO_QA.md` | `--technical-audio` / `--jury` |

Master policy: `docs/QA_REMEDIATION_LOOP.md` §10.

---

## 7. L2 smoke auto-brief

When `run_playtest_smoke.sh` or domain smoke scripts fail technical lint or jury, they call:

```bash
bash tools/qa_emit_remediation.sh <kind> [args]
```

Agents must read the emitted brief before the next build attempt.

---

## 8. Agent report template (flow FAIL)

```markdown
[FLOW QA] scenario=INT-QUEST-01 attempt=2
  validate_story_data: PASS
  integration: FAIL at step "inspect well" — flag well_inspected not set
  lever_changed: trigger_wiring (well Area3D on_interact → set_flags)
  do_not_repeat: editing quest JSON only (attempt 1)
  godotiq: traced StoryManager.inspectable_well → no connection
  next: GDAI wire signal → re-run INT-QUEST-01
```

---

## 9. Tools

| Tool | Role |
|------|------|
| `tools/validate_story_data.py` | F0 data gate |
| `tools/run_integration_tests.sh` | F4 scenario runner |
| `tools/run_e2e_playthrough.sh` | F5 full spine |
| `tools/qa_remediation_brief.py` | Brief for any domain |
| `tools/qa_emit_remediation.sh` | Smoke/integration FAIL → brief |
| `game/data/qa/remediation_playbook.json` | §`data`, §`flow` entries |
