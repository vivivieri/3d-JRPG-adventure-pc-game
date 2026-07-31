---
id: pre-build
type: reference
phase: [0, 1, 8]
audience: [pm, release, architect]
status: active
authority: workflow
tokens_est: 1335
summary: "- [x] Game Design Document (`docs/design/vision/GDD.md`)"
---
# Milestones — M0 pre-build packs

**Hub:** [`MILESTONES.md`](../MILESTONES.md)

## M0 — Pre-production
- [x] Game Design Document (`docs/design/vision/GDD.md`)
- [x] Storyboard — 20 scene headings (`docs/design/vision/STORYBOARD.md` — SC-00 + SC-01–16 + 3 ending variants; 18 experienced per playthrough)
- [x] Art direction bible (`docs/design/art/ART_DIRECTION.md`)
- [x] License tracking template (`docs/design/art/LICENSES.md`)
- [x] Asset compliance policy + verification tools (`docs/design/art/ASSET_COMPLIANCE.md`, `tools/`)
- [x] Godot 4 project scaffold on **`game/development`** (`game/project.godot` — P1-00; not on `main`)
- [x] Combat JSON schema + sample data (`game/data/`)
- [ ] Core scripts (GameManager, Combat, Dialogue, Save) — Phase 2+ rebuild
- [x] **Multi-language support (en / ja / zh / zh-Hant + dialect VO)** — written data in `game/data/` + `translations.csv`; runtime `LocalizationManager` Phase 2+ via GDAI MCP; VO clips Phase 7


## M0c — Pre-build design (art rebuild specs)
- [x] Character bible (`docs/design/art/CHARACTER_BIBLE.md`) — v1.1: LOD, boss 3D, attachment rig
- [x] Items 3D model guide (`docs/design/art/ITEMS_3D_MODEL_GUIDE.md`)
- [x] Environment kits (`docs/design/world/ENVIRONMENT_KITS.md`)
- [x] Boss design sheets (`docs/design/gameplay/BOSS_DESIGNS.md`)
- [x] Encounter & pacing table (`docs/design/gameplay/ENCOUNTER_TABLE.md`)
- [x] Cinematics & camera spec (`docs/design/ui/CINEMATICS.md`)
- [x] Audio direction (`docs/design/audio/AUDIO_DIRECTION.md`)
- [x] Audio production guide (`docs/design/audio/AUDIO_PRODUCTION_GUIDE.md`) — BGM/SFX specs, scene map
- [x] Art direction pivot — high-detail Japanese stylized (`docs/design/art/ART_DIRECTION.md` v1.1)


## M0d — Pre-build game design (gameplay systems)
- [x] Quest & story flag map (`docs/design/world/QUEST_AND_FLAGS.md`) — 5 main quests
- [x] Tutorial & onboarding (`docs/design/gameplay/TUTORIAL_DESIGN.md`) + SC-00 prologue
- [x] Ending design (`docs/design/vision/ENDING_DESIGN.md`)
- [x] Items & economy (`docs/design/gameplay/ITEMS_AND_ECONOMY.md`)
- [x] Combat systems (`docs/design/gameplay/COMBAT_SYSTEMS.md`)
- [x] Skills bible (`docs/design/gameplay/SKILLS_BIBLE.md`) — 15 player loadout slots / 14 unique skill IDs
- [x] UI / UX flow (`docs/design/ui/UI_UX_FLOW.md`)
- [x] Save & fail states (`docs/engineering/technical/SAVE_AND_FAIL_STATES.md`)
- [x] Settings & accessibility (`docs/design/ui/SETTINGS_ACCESSIBILITY.md`)
- [x] Puzzle design SC-07 (`docs/design/world/PUZZLE_DESIGN.md`)
- [x] Steam achievements (`docs/design/gameplay/ACHIEVEMENTS.md`)
- [x] Playtest script (`docs/ops/qa/PLAYTEST_SCRIPT.md`)
- [x] QA & bug process (`docs/ops/qa/QA_AND_BUG_PROCESS.md`)
- [x] Technical design TDD (`docs/engineering/technical/TECHNICAL_DESIGN.md`)
- [x] Code style guide (`docs/engineering/technical/CODE_STYLE.md`)
- [x] Level design breakdown (`docs/design/world/LEVEL_DESIGN.md`)
- [x] Documentation index (`docs/README.md`)
- [x] Emotional pacing chart (`docs/design/vision/PACING_CHART.md`)


## M0f — Pre-build design (narrative & polish)
- [x] Narrative writing guide (`docs/design/vision/NARRATIVE_WRITING_GUIDE.md`) — selective VO (12 clips); SC-07 silence
- [x] Progression tuning (`docs/design/gameplay/PROGRESSION_TUNING.md`)
- [x] Game feel (`docs/design/gameplay/GAME_FEEL.md`)
- [x] Lore & environmental story (`docs/design/vision/LORE_AND_ENVIRONMENTAL_STORY.md`)
- [x] World map & zone flow (`docs/design/world/WORLD_MAP_AND_FLOW.md`)
- [x] Replay design (`docs/design/vision/REPLAY_DESIGN.md`)


## M0g — Pitch illustrations
- [x] Storyboard illustration spec (`docs/design/vision/STORYBOARD_ILLUSTRATIONS.md`)
- [x] P0 pitch images (`docs/archive/pitch/illustrations/`) — party + 4 key scenes
- [x] P1 full storyboard pass (20 scene images)
- [x] P2 character portraits (4 + party lineup)
- [x] Marketing trailer (`steam/trailer.mp4`, `trailer_ja.mp4`, `trailer_zh.mp4`, `trailer_zh-Hant.mp4`) — four on-screen-text locales + shared procedural BGM


## M0e — Story data layer (main branch)
- [x] Data architecture (`docs/engineering/technical/DATA_ARCHITECTURE.md`)
- [x] Story spine + flags (`game/data/story/`)
- [x] 5 quests, 9 encounters, 20 items, 22 dialogue scenes
- [x] Shop, achievements, new game defaults
- [x] `tools/validate_story_data.py`


## M0h — AI dev workflow & testing (main baseline)
- [x] AI build policy — GodotPrompter + MCP stack (`.cursorrules` §0, `docs/ops/agents/MCP_STACK.md`)
- [x] Unit test scaffold on **`game/development`** (`game/tests/unit/`, `tools/run_unit_tests.sh`) — restored with P1-00
- [x] Smoke tests (`tools/run_playtest_smoke.sh`)
- [x] Acceptance criteria catalog (`docs/ops/qa/ACCEPTANCE_CRITERIA.md`, `game/data/qa/acceptance_criteria.json`)
- [x] Domain QA gates (MODEL/VISUAL/AUDIO/FLOW QA + `QA_REMEDIATION_LOOP.md`)
- [x] Phase acceptance criteria documented (`docs/ops/workflow/AI_DEV_WORKFLOW.md` §4)
- [x] AI testing spec L0–L6 (`docs/ops/qa/AI_TESTING_SPEC.md`) — human QA after L5
- [ ] Integration tests (`tools/run_integration_tests.sh`) — expand Phase 2+
- [ ] E2E three endings (`tools/run_e2e_playthrough.sh`) — Phase 6
