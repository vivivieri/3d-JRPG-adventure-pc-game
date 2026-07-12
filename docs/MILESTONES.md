# Milestone checklist

Track implementation progress against the GDD milestones.

**Planning authority:** Build order and phase gates live in **`docs/IMPLEMENTATION_PLAN.md`** (Phases 0–8). This file is the **deliverable checklist**. When labels conflict, prefer the implementation plan.

**M5 / M6 order (canonical):** **M5 = art rebuild** (Phase 7) → **M6 = Steam & ship** (Phase 8). Art before store/export.

### Phase ↔ milestone map

| Implementation phase | Milestone focus | Primary doc |
|---------------------|-----------------|-------------|
| Phase 0 | M0, M0c–M0h pre-production | This file §M0* |
| Phase 1 | Environment + SC-02 vertical slice gate | `IMPLEMENTATION_PLAN` §Phase 1 |
| Phase 2 | M1 greybox systems shell | `IMPLEMENTATION_PLAN` §Phase 2 |
| Phase 3 | M1 narrative + exploration | `IMPLEMENTATION_PLAN` §Phase 3 |
| Phase 4 | M2 combat vertical slice | `IMPLEMENTATION_PLAN` §Phase 4 |
| Phase 5 | M3 Chapter 1 | `IMPLEMENTATION_PLAN` §Phase 5 |
| Phase 6 | M4 full story + endings | `IMPLEMENTATION_PLAN` §Phase 6 |
| Phase 7 | **M5 art rebuild** | `ART_DIRECTION.md`, `RENDERING_GUIDE.md` |
| Phase 8 | **M6 Steam & ship** | `steam/`, `PLUGIN_COMPATIBILITY.md` |

---

## M0 — Pre-production
- [x] Game Design Document (`docs/GDD.md`)
- [x] Storyboard — 20 scene headings (`docs/STORYBOARD.md` — SC-00 + SC-01–16 + 3 ending variants; 18 experienced per playthrough)
- [x] Art direction bible (`docs/ART_DIRECTION.md`)
- [x] License tracking template (`docs/LICENSES.md`)
- [x] Asset compliance policy + verification tools (`docs/ASSET_COMPLIANCE.md`, `tools/`)
- [x] Godot 4 project scaffold (boot shell on `main`)
- [x] Combat JSON schema + sample data (`game/data/`)
- [ ] Core scripts (GameManager, Combat, Dialogue, Save) — Phase 2+ rebuild
- [x] **Multi-language support (en / ja / zh / zh-Hant + dialect VO)** — spec complete (`docs/LOCALIZATION.md`); **written zh-Hant data** Phase 3.10; runtime `LocalizationManager` Phase 2+

## M0c — Pre-build design (art rebuild specs)
- [x] Character bible (`docs/CHARACTER_BIBLE.md`) — v1.1: LOD, boss 3D, attachment rig
- [x] Items 3D model guide (`docs/ITEMS_3D_MODEL_GUIDE.md`)
- [x] Environment kits (`docs/ENVIRONMENT_KITS.md`)
- [x] Boss design sheets (`docs/BOSS_DESIGNS.md`)
- [x] Encounter & pacing table (`docs/ENCOUNTER_TABLE.md`)
- [x] Cinematics & camera spec (`docs/CINEMATICS.md`)
- [x] Audio direction (`docs/AUDIO_DIRECTION.md`)
- [x] Audio production guide (`docs/AUDIO_PRODUCTION_GUIDE.md`) — BGM/SFX specs, scene map
- [x] Art direction pivot — high-detail Japanese stylized (`docs/ART_DIRECTION.md` v1.1)

## M0d — Pre-build game design (gameplay systems)
- [x] Quest & story flag map (`docs/QUEST_AND_FLAGS.md`) — 5 main quests
- [x] Tutorial & onboarding (`docs/TUTORIAL_DESIGN.md`) + SC-00 prologue
- [x] Ending design (`docs/ENDING_DESIGN.md`)
- [x] Items & economy (`docs/ITEMS_AND_ECONOMY.md`)
- [x] Combat systems (`docs/COMBAT_SYSTEMS.md`)
- [x] Skills bible (`docs/SKILLS_BIBLE.md`) — 15 player loadout slots / 14 unique skill IDs
- [x] UI / UX flow (`docs/UI_UX_FLOW.md`)
- [x] Save & fail states (`docs/SAVE_AND_FAIL_STATES.md`)
- [x] Settings & accessibility (`docs/SETTINGS_ACCESSIBILITY.md`)
- [x] Puzzle design SC-07 (`docs/PUZZLE_DESIGN.md`)
- [x] Steam achievements (`docs/ACHIEVEMENTS.md`)
- [x] Playtest script (`docs/PLAYTEST_SCRIPT.md`)
- [x] QA & bug process (`docs/QA_AND_BUG_PROCESS.md`)
- [x] Technical design TDD (`docs/TECHNICAL_DESIGN.md`)
- [x] Code style guide (`docs/CODE_STYLE.md`)
- [x] Level design breakdown (`docs/LEVEL_DESIGN.md`)
- [x] Documentation index (`docs/README.md`)
- [x] Emotional pacing chart (`docs/PACING_CHART.md`)

## M0f — Pre-build design (narrative & polish)
- [x] Narrative writing guide (`docs/NARRATIVE_WRITING_GUIDE.md`) — selective VO (12 clips); SC-07 silence
- [x] Progression tuning (`docs/PROGRESSION_TUNING.md`)
- [x] Game feel (`docs/GAME_FEEL.md`)
- [x] Lore & environmental story (`docs/LORE_AND_ENVIRONMENTAL_STORY.md`)
- [x] World map & zone flow (`docs/WORLD_MAP_AND_FLOW.md`)
- [x] Replay design (`docs/REPLAY_DESIGN.md`)

## M0g — Pitch illustrations
- [x] Storyboard illustration spec (`docs/STORYBOARD_ILLUSTRATIONS.md`)
- [x] P0 pitch images (`docs/pitch/illustrations/`) — party + 4 key scenes
- [x] P1 full storyboard pass (20 scene images)
- [x] P2 character portraits (4 + party lineup)
- [x] Marketing trailer (`steam/trailer.mp4`, `trailer_ja.mp4`, `trailer_zh.mp4`) — multilingual + procedural BGM

## M0e — Story data layer (main branch)
- [x] Data architecture (`docs/DATA_ARCHITECTURE.md`)
- [x] Story spine + flags (`game/data/story/`)
- [x] 5 quests, 9 encounters, 20 items, 22 dialogue scenes
- [x] Shop, achievements, new game defaults
- [x] `tools/validate_story_data.py`

## M0h — AI dev workflow & testing (main baseline)
- [x] AI build policy — GodotPrompter + MCP stack (`.cursorrules` §0, `docs/MCP_STACK.md`)
- [x] Unit test scaffold (`game/tests/unit/`, `tools/run_unit_tests.sh`)
- [x] Smoke tests (`tools/run_playtest_smoke.sh`)
- [x] Acceptance criteria catalog (`docs/ACCEPTANCE_CRITERIA.md`, `game/data/qa/acceptance_criteria.json`)
- [x] Domain QA gates (MODEL/VISUAL/AUDIO/FLOW QA + `QA_REMEDIATION_LOOP.md`)
- [x] Phase acceptance criteria documented (`docs/AI_DEV_WORKFLOW.md` §4)
- [x] AI testing spec L0–L6 (`docs/AI_TESTING_SPEC.md`) — human QA after L5
- [ ] Integration tests (`tools/run_integration_tests.sh`) — expand Phase 2+
- [ ] E2E three endings (`tools/run_e2e_playthrough.sh`) — Phase 6

## M1 — Greybox exploration
- [ ] Player movement polish (camera orbit — right-mouse + scroll)
- [ ] Interaction prompt HUD (Press E — action, localized)
- [ ] Dialogue box UI scene (typewriter, speaker, locale fonts)
- [ ] CJK font bundle + locale-aware `FontThemeManager` (incl. NotoSansTC for zh-Hant)
- [ ] `LocalizationManager` + settings menu (language + `vo_dialect` for zh-Hant)
- [ ] `AudioManager` shell — procedural BGM/SFX placeholders (upgrade in M5)
- [ ] `VoiceLinePlayer` wired to `DialogueRunner` (runtime paths; clips optional until M5)
- [ ] SC-00 prologue + `CinematicDirector` opening hook
- [ ] Tab inventory / equipment menu
- [ ] Roku shop UI (`shop/roku_shop.json`)
- [ ] Quest tracker UI
- [ ] Save point at village well
- [ ] Written i18n pass — `translations.csv` + `zh-Hant` in `chapter_01.json`

## M2 — Combat vertical slice
- [ ] Combat UI vertical slice (HP/MP bars, action menu, battle log, enemy intent)
- [ ] Combat polish (transitions, damage flash, items, escape, boss banners)

## M3 — Chapter 1
- [ ] Tidal Caves greybox map + SC-06 entrance
- [ ] Water level puzzle (SC-07 — silent, no VO)
- [ ] SC-08 echo vignette (`CinematicDirector` + whisper bed)
- [ ] Shore Wraith boss (SC-09)
- [ ] Yuzu joins party (SC-10)

## M4 — Full game
- [ ] Dragon Palace Gate dungeon + SC-12 gate cinematic
- [ ] SC-11 flashback + SC-13 box revelation
- [ ] Palace Sentinel (SC-14) + Tide Keeper (SC-15) bosses
- [ ] SC-16 choice UI + three endings (SC-17a/b/c)
- [ ] Credits sequence
- [ ] E2E three endings (`bash tools/run_e2e_playthrough.sh`)

## M5 — Art rebuild (high-detail Japanese)
- [ ] Rendering guide applied per zone (`docs/RENDERING_GUIDE.md`)
- [ ] Fresh implementation on `main` per `docs/IMPLEMENTATION_PLAN.md` + `docs/AI_DEV_WORKFLOW.md`
- [ ] Vertical slice: SC-02 Ruined Village + Urashima model (`docs/ART_DIRECTION.md` §10)
- [ ] Replace all primitive / Kenney greybox art in player-facing builds
- [ ] Japanese palace gate hero set-piece (`palace_gate_main` — SC-12)
- [ ] Character models: Urashima, Yuzu, Roku + 5 enemies
- [ ] Automated stylized portraits (ComfyUI/GameLab — replace procedural silhouettes)
- [ ] Ending environment variants (Rewind / Anchor / Drift)
- [ ] Curated BGM per act (ACE-Step curated prompts — replace dev procedural placeholders)
- [ ] SFX + ambient beds per `AUDIO_PRODUCTION_GUIDE.md` scene map
- [ ] ElevenLabs voice casting — replace `PLACEHOLDER_*` in `vo_prompts.json` (incl. zh-Hant `dialect_voices`)
- [ ] Generate selective VO — P0 listen pass → P1/P2; `en`/`ja`/`zh` + zh-Hant `cant`/`cmn` (60 clips)
- [ ] VO passes `AUDIO_QA.md` technical + jury gates (`bash tools/run_audio_smoke_checks.sh`)
- [ ] Cinematic hero assets — SC-00 opening, SC-12 gate reveal, SC-17 endings
- [ ] `bash tools/check_asset_compliance.sh` passes on release branch

### M5 cinematic budget (`docs/CINEMATICS.md` §12)

| Priority | Deliverable | Assets / hooks | Notes |
|----------|-------------|----------------|-------|
| **P0** | SC-00 opening montage | `cine_opening_hero`, prologue BGM | Myth setup; skippable replay |
| **P0** | SC-17 three endings | `cine_ending_*_hero`, ending env kits | Not skippable first play |
| **P0** | SC-02 hub pan | Village kit, torii silhouette | 4s; immediate skip OK |
| **P1** | Boss intros ×3 | Boss models, `cine_boss_*_intro` stings | 3–6s each |
| **P1** | **SC-12 gate reveal** | `palace_gate_main`, `CameraMarker_sc12_*`, `sc12_gate_reveal` | **12–15s** — only mid-game hero movie |
| **P2** | SC-08 pool vignette | `cave_deep_pool`, face decals, whisper bed | **5–8s** — not 15s |
| **P2** | SC-11 flashback | Otohime silhouette, letterbox | Skippable after 3s |

**Marginal cost rule:** SC-12 cinematic is cheap once `palace_gate_main` exists — fund the gate mesh first, camera path second.

## M6 — Steam & ship prep
- [ ] Steam achievements (`AchievementManager` + `game/data/achievements/achievements.json`)
- [ ] Steam store page copy + capsule art from final M5 assets
- [ ] Windows export preset + `tools/export_windows.sh`
- [ ] Steam screenshots from 3D builds (`steam/screenshots/`)
- [ ] Marketing trailer upload (`steam/trailer.mp4` — regenerate after M5 art if needed)
- [ ] GodotSteam scaffold (`SteamManager` + `game/addons/godotsteam/README.md`)
- [ ] Install GodotSteam **4.20+** GDExtension (`bash tools/install_godotsteam.sh`) — required for Godot 4.7
- [ ] Steamworks app ID + depot upload
- [ ] `bash tools/check_asset_compliance.sh` passes
- [ ] Playtest on Windows hardware (`docs/PLAYTEST_SCRIPT.md`)
- [ ] Disable/remove GDAI MCP before export (`docs/IMPLEMENTATION_PLAN.md` Phase 8)
