# Tides of Urashima — Documentation Index

**Start here.** All design, technical, and production docs for the 2–3 hour stylized 3D JRPG.

---

## Authority chain (when docs disagree)

| Priority | Document | Answers |
|----------|----------|---------|
| 1 | [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) | What to build, in what order (Phases 0–8) |
| 2 | [MILESTONES.md](MILESTONES.md) | Deliverable checklist |
| 3 | [TECHNICAL_DESIGN.md](TECHNICAL_DESIGN.md) | How runtime code fits together |
| 4 | [DATA_ARCHITECTURE.md](DATA_ARCHITECTURE.md) + `game/data/` | Story JSON spine + save shape |
| 5 | [MCP_STACK.md](MCP_STACK.md) + [ART_AUTOMATION_PIPELINE.md](ART_AUTOMATION_PIPELINE.md) + [`.cursorrules`](../.cursorrules) | Tools and agent rules |

---

## Quick links by role

| I need to… | Read |
|------------|------|
| Understand the game | [GDD.md](GDD.md) → [STORYBOARD.md](STORYBOARD.md) |
| Build the next phase | [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) |
| Write GDScript | [CODE_STYLE.md](CODE_STYLE.md) + [TECHNICAL_DESIGN.md](TECHNICAL_DESIGN.md) |
| Place zones & interactables | [LEVEL_DESIGN.md](LEVEL_DESIGN.md) |
| Tune combat / economy | [COMBAT_SYSTEMS.md](COMBAT_SYSTEMS.md) + [PROGRESSION_TUNING.md](PROGRESSION_TUNING.md) |
| Author dialogue / flags | [QUEST_AND_FLAGS.md](QUEST_AND_FLAGS.md) + `game/data/dialogue/` |
| Set up lighting / materials | [RENDERING_GUIDE.md](RENDERING_GUIDE.md) + [ENVIRONMENT_KITS.md](ENVIRONMENT_KITS.md) |
| Generate art (automated) | [ART_AUTOMATION_PIPELINE.md](ART_AUTOMATION_PIPELINE.md) |
| Run agents / MCP | [MCP_STACK.md](MCP_STACK.md) + [AGENTS.md](../AGENTS.md) |
| Review look & feel (AI + human) | [VISUAL_QA.md](VISUAL_QA.md) |
| Ship on Steam | [MILESTONES.md](MILESTONES.md) §M6 + [steam/GODOTSTEAM_SETUP.md](../steam/GODOTSTEAM_SETUP.md) |

---

## 1. Vision & narrative

| Doc | Purpose |
|-----|---------|
| [GDD.md](GDD.md) | Master game design — scope, pillars, audience |
| [STORYBOARD.md](STORYBOARD.md) | 19-scene narrative bible (SC-00 + 18 main) |
| [NARRATIVE_WRITING_GUIDE.md](NARRATIVE_WRITING_GUIDE.md) | Voice, silence, selective VO, i18n prose |
| [VO_HIT_LIST.md](VO_HIT_LIST.md) | 12 ElevenLabs clips — not full dialogue |
| [ENDING_DESIGN.md](ENDING_DESIGN.md) | Three endings, choice UI, replay |
| [LORE_AND_ENVIRONMENTAL_STORY.md](LORE_AND_ENVIRONMENTAL_STORY.md) | 8 lore entries, environmental storytelling |
| [PACING_CHART.md](PACING_CHART.md) | Emotional beat timeline |
| [REPLAY_DESIGN.md](REPLAY_DESIGN.md) | Ending gallery, second run |

---

## 2. World & levels

| Doc | Purpose |
|-----|---------|
| [LEVEL_DESIGN.md](LEVEL_DESIGN.md) | **Per-zone blockouts, interactables, triggers, encounters** |
| [WORLD_MAP_AND_FLOW.md](WORLD_MAP_AND_FLOW.md) | Zone graph, connections, save points (summary) |
| [ENVIRONMENT_KITS.md](ENVIRONMENT_KITS.md) | Modular art kits, poly budgets, per-zone assets |
| [PUZZLE_DESIGN.md](PUZZLE_DESIGN.md) | SC-07 water puzzle (silent) |
| [QUEST_AND_FLAGS.md](QUEST_AND_FLAGS.md) | 5 quests, flag registry, stage logic |

---

## 3. Gameplay systems

| Doc | Purpose |
|-----|---------|
| [COMBAT_SYSTEMS.md](COMBAT_SYSTEMS.md) | Turn order, elements, status, intent UI |
| [SKILLS_BIBLE.md](SKILLS_BIBLE.md) | 15 player + 6 enemy skills |
| [BOSS_DESIGNS.md](BOSS_DESIGNS.md) | Shore Wraith, Sentinel, Tide Keeper |
| [ENCOUNTER_TABLE.md](ENCOUNTER_TABLE.md) | Pacing, XP, drops, shop timing |
| [PROGRESSION_TUNING.md](PROGRESSION_TUNING.md) | XP curve, stats at milestones, difficulty |
| [ITEMS_AND_ECONOMY.md](ITEMS_AND_ECONOMY.md) | 20 items, shop, drops, inflation guards |
| [TUTORIAL_DESIGN.md](TUTORIAL_DESIGN.md) | Onboarding + SC-00 prologue |
| [GAME_FEEL.md](GAME_FEEL.md) | Juice, feedback, rewards |
| [ACHIEVEMENTS.md](ACHIEVEMENTS.md) | 12 Steam achievements |

---

## 4. Technical architecture

| Doc | Purpose |
|-----|---------|
| [TECHNICAL_DESIGN.md](TECHNICAL_DESIGN.md) | **TDD** — autoloads, scene flow, combat stack, save pipeline |
| [CODE_STYLE.md](CODE_STYLE.md) | GDScript conventions, folders, signals, naming |
| [DATA_ARCHITECTURE.md](DATA_ARCHITECTURE.md) | Story-first JSON layout, schema versions |
| [SAVE_AND_FAIL_STATES.md](SAVE_AND_FAIL_STATES.md) | Save slots, autosave, game over |
| [LOCALIZATION.md](LOCALIZATION.md) | en / ja / zh, CSV, fonts |
| [TECH_STACK.md](TECH_STACK.md) | Godot 4.7, plugin versions |
| [PLUGIN_COMPATIBILITY.md](PLUGIN_COMPATIBILITY.md) | GDAI, Godotiq, MCP Pro, GodotSteam |

---

## 5. UI & cinematics

| Doc | Purpose |
|-----|---------|
| [UI_UX_FLOW.md](UI_UX_FLOW.md) | Menus, HUD, controller, screen map |
| [SETTINGS_ACCESSIBILITY.md](SETTINGS_ACCESSIBILITY.md) | Options, hard mode, a11y |
| [CINEMATICS.md](CINEMATICS.md) | Cameras, boss intros, endings — **no FMV** |

---

## 6. Art, audio & assets

| Doc | Purpose |
|-----|---------|
| [VISUAL_QA.md](VISUAL_QA.md) | **Screenshot + vision gates** — prevent primitive/placeholder spread |
| [ART_AUTOMATION_PIPELINE.md](ART_AUTOMATION_PIPELINE.md) | **Quality-first automated art/audio** — tier matrix, workflows |
| [RENDERING_GUIDE.md](RENDERING_GUIDE.md) | Forward+ tonemap, fog, glow, zone presets |
| [CHARACTER_BIBLE.md](CHARACTER_BIBLE.md) | Models, portraits, boss meshes, rig |
| [ITEMS_3D_MODEL_GUIDE.md](ITEMS_3D_MODEL_GUIDE.md) | Props, weapons, pickup meshes |
| [AUDIO_DIRECTION.md](AUDIO_DIRECTION.md) | Music map, SFX philosophy |
| [AUDIO_QA.md](AUDIO_QA.md) | **Technical + optional LLM listen jury** for BGM |
| [AUDIO_PRODUCTION_GUIDE.md](AUDIO_PRODUCTION_GUIDE.md) | Buses, loudness, scene→track map |
| [STORYBOARD_ILLUSTRATIONS.md](STORYBOARD_ILLUSTRATIONS.md) | Pitch art spec |
| [ASSET_COMPLIANCE.md](ASSET_COMPLIANCE.md) | Copyright-safe policy |
| [LICENSES.md](LICENSES.md) | Attribution log |

---

## 7. Production & QA

| Doc | Purpose |
|-----|---------|
| [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) | Rebuild phases 0–8 |
| [MILESTONES.md](MILESTONES.md) | Feature checklist (M5 art → M6 Steam) |
| [AI_DEV_WORKFLOW.md](AI_DEV_WORKFLOW.md) | Build policy, phase acceptance |
| [AI_TESTING_SPEC.md](AI_TESTING_SPEC.md) | L0–L6 automated + human QA |
| [QA_AND_BUG_PROCESS.md](QA_AND_BUG_PROCESS.md) | Severity, triage, milestone gates |
| [PLAYTEST_SCRIPT.md](PLAYTEST_SCRIPT.md) | 2–3h human playthrough path |
| [GDAI_CLOUD_SETUP.md](GDAI_CLOUD_SETUP.md) | Cloud agent bootstrap |
| [PLUGIN_INSTALL_GUIDE.md](PLUGIN_INSTALL_GUIDE.md) | MCP plugin install |

---

## 8. Data layer (`game/data/`)

| Path | Purpose |
|------|---------|
| [game/data/README.md](../game/data/README.md) | Load API, conventions, schema summary |
| `story/scenes.json` | 23 scene rows — master spine |
| `story/flags.json` | Canonical flag registry |
| `dialogue/chapter_01.json` | All dialogue + 12 `voice_id` lines |
| `quests/main_quests.json` | 5 main quests |
| `encounters/story_encounters.json` | 8 scripted fights |

```bash
python3 tools/validate_story_data.py
```

---

## 9. Marketing (not in-game)

| Path | Purpose |
|------|---------|
| [steam/STORE_PAGE.md](../steam/STORE_PAGE.md) | Steam store copy |
| [steam/TRAILER_SCRIPT.md](../steam/TRAILER_SCRIPT.md) | Trailer beat sheet |
| `docs/pitch/illustrations/` | 25 pitch PNGs |
| `steam/trailer.mp4` | ~75s EN / JA / ZH marketing trailer |

---

## Deprecated

| Doc | Replacement |
|-----|-------------|
| [GDAI_REGEN_PLAN.md](GDAI_REGEN_PLAN.md) | [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) |

---

## Industry-standard coverage map

| Studio-style artifact | Our doc |
|----------------------|---------|
| GDD | `GDD.md` |
| System design macro | `PROGRESSION_TUNING.md` + `COMBAT_SYSTEMS.md` + `game/data/` |
| Economy spreadsheet | `ITEMS_AND_ECONOMY.md` + `ENCOUNTER_TABLE.md` |
| Quest / dialogue script | `QUEST_AND_FLAGS.md` + `chapter_01.json` |
| Lore bible | `LORE_AND_ENVIRONMENTAL_STORY.md` + `CHARACTER_BIBLE.md` |
| Level design breakdown | **`LEVEL_DESIGN.md`** |
| Technical design (TDD) | **`TECHNICAL_DESIGN.md`** |
| Database / save schema | `DATA_ARCHITECTURE.md` + `SAVE_AND_FAIL_STATES.md` |
| Code style guide | **`CODE_STYLE.md`** |
| Art bible / asset pipeline | `ART_AUTOMATION_PIPELINE.md` + `ART_DIRECTION.md` + `RENDERING_GUIDE.md` |
| Asset registry | `LICENSES.md` + `asset_manifest.license.json` |
| Production timeline | `IMPLEMENTATION_PLAN.md` + `MILESTONES.md` |
