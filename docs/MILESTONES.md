# Milestone checklist

Track implementation progress against the GDD milestones.

## M0 — Pre-production
- [x] Game Design Document (`docs/GDD.md`)
- [x] Storyboard — 19 scenes (`docs/STORYBOARD.md` — SC-00 + 18 main)
- [x] Art direction bible (`docs/ART_DIRECTION.md`)
- [x] License tracking template (`docs/LICENSES.md`)
- [x] Asset compliance policy + verification tools (`docs/ASSET_COMPLIANCE.md`, `tools/`)
- [x] Godot 4 project scaffold
- [x] Combat JSON schema + sample data
- [x] Core scripts (GameManager, Combat, Dialogue, Save)
- [x] **Multi-language support (en / ja / zh)** — `docs/LOCALIZATION.md`

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
- [x] Skills bible (`docs/SKILLS_BIBLE.md`) — 15 player skills
- [x] UI / UX flow (`docs/UI_UX_FLOW.md`)
- [x] Save & fail states (`docs/SAVE_AND_FAIL_STATES.md`)
- [x] Settings & accessibility (`docs/SETTINGS_ACCESSIBILITY.md`)
- [x] Puzzle design SC-07 (`docs/PUZZLE_DESIGN.md`)
- [x] Steam achievements (`docs/ACHIEVEMENTS.md`)
- [x] Playtest script (`docs/PLAYTEST_SCRIPT.md`)
- [x] QA & bug process (`docs/QA_AND_BUG_PROCESS.md`)
- [x] Emotional pacing chart (`docs/PACING_CHART.md`)

## M0f — Pre-build design (narrative & polish)
- [x] Narrative writing guide (`docs/NARRATIVE_WRITING_GUIDE.md`) — no VO; SC-07 silence
- [x] Progression tuning (`docs/PROGRESSION_TUNING.md`)
- [x] Game feel (`docs/GAME_FEEL.md`)
- [x] Lore & environmental story (`docs/LORE_AND_ENVIRONMENTAL_STORY.md`)
- [x] World map & zone flow (`docs/WORLD_MAP_AND_FLOW.md`)
- [x] Replay design (`docs/REPLAY_DESIGN.md`)

## M0e — Story data layer (main branch)
- [x] Data architecture (`docs/DATA_ARCHITECTURE.md`)
- [x] Story spine + flags (`game/data/story/`)
- [x] 5 quests, 8 encounters, 20 items, 22 dialogue scenes
- [x] Shop, achievements, new game defaults
- [x] `tools/validate_story_data.py`

## M1 — Greybox exploration
- [x] Player movement polish (camera orbit — right-mouse + scroll)
- [x] Interaction prompt HUD (Press E — action, localized)
- [x] Dialogue box UI scene (typewriter, speaker, locale fonts)
- [x] CJK font bundle + locale-aware `FontThemeManager`
- [x] Quest tracker UI
- [x] Save point at village well

## M2 — Combat vertical slice
- [x] Combat UI vertical slice (HP/MP bars, action menu, battle log, enemy intent)
- [x] Combat polish (transitions, damage flash, items, escape, boss banners)

## M3 — Chapter 1
- [x] Tidal Caves greybox map
- [x] Water level puzzle
- [x] Shore Wraith boss
- [x] Yuzu joins party

## M4 — Full game
- [x] Dragon Palace Gate dungeon
- [x] Palace Sentinel + Tide Keeper bosses
- [x] Three endings
- [x] Credits sequence

## M5 — Steam
- [x] Placeholder BGM/SFX + AudioManager → **procedural coastal JRPG audio** (`tools/generate_game_audio.py`)
- [x] Zone art pass (materials, fog, props) → **tileable zone textures + portraits**
- [x] Field item use + equipment UI (Tab menu)
- [x] Steam store page copy + capsule placeholders
- [x] Windows export preset + `tools/export_windows.sh`
- [x] Steam screenshots + trailer placeholder (`steam/screenshots/`, `steam/trailer.mp4`)
- [x] GodotSteam scaffold (`SteamManager` + `game/addons/godotsteam/README.md`)
- [x] Combat drop rolls + balance pass
- [x] Install GodotSteam GDExtension binaries (`tools/install_godotsteam.sh`)
- [ ] Steamworks app ID + depot upload
- [ ] Final CC0 audio/art replacement (optional — current assets are original procedural)
- [ ] `bash tools/check_asset_compliance.sh` passes
- [ ] Playtest on Windows hardware

## M6 — Art rebuild (high-detail Japanese)
- [ ] Vertical slice: SC-02 Ruined Village + Urashima model (`docs/ART_DIRECTION.md` §10)
- [ ] Replace all primitive / Kenney placeholder art
- [ ] Japanese palace gate hero set-piece (no European castle kit)
- [ ] Character models: Urashima, Yuzu, Roku + 5 enemies
- [ ] Painted portraits (replace procedural silhouettes)
- [ ] Ending environment variants (Rewind / Anchor / Drift)
- [ ] Curated BGM per act (replace procedural audio)
- [ ] `bash tools/check_asset_compliance.sh` passes on release branch
