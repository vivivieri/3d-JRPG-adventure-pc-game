# Tides of Urashima — Documentation Index

**Start here.** All design, technical, and production docs for the 2–3 hour stylized 3D JRPG.

### Printable cheat sheets (agents)

| Doc | Purpose |
|-----|---------|
| [RR_CHEATSHEET.md](RR_CHEATSHEET.md) | **Roles** — who owns what, handoffs, tools |
| [CONTROLS_CHEATSHEET.md](CONTROLS_CHEATSHEET.md) | **Controls** — CI gates, PR templates, branch protection |

---

## Authority chain (when docs disagree)

| Priority | Document | Answers |
|----------|----------|---------|
| 1 | [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) | What to build, in what order (Phases 0–8) |
| 1b | [BRANCHING.md](BRANCHING.md) | `main` = docs/data · `game/development` = implementation |
| 1c | [ENVIRONMENTS.md](ENVIRONMENTS.md) | dev · qa · uat · preprod · prod promotion |
| 1d | [AGILE_WITHIN_PHASES.md](AGILE_WITHIN_PHASES.md) | Phase-gated Agile + Linear sprint map |
| 2 | [MILESTONES.md](MILESTONES.md) | Deliverable checklist |
| 3 | [TECHNICAL_DESIGN.md](TECHNICAL_DESIGN.md) | How runtime code fits together |
| 4 | [DATA_ARCHITECTURE.md](DATA_ARCHITECTURE.md) + `game/data/` | Story JSON spine + save shape |
| 5 | [MCP_STACK.md](MCP_STACK.md) + [ART_AUTOMATION_PIPELINE.md](ART_AUTOMATION_PIPELINE.md) + [`.cursorrules`](../.cursorrules) | Tools and agent rules |

**Numeric values rule:** For any runtime number — enemy/party stats, skill costs and powers, prices, XP, drop rates, flag names — **`game/data/*.json` wins** over design-doc prose. Design docs mirror the JSON; when tuning changes, update the JSON first, then the doc tables. Run `python3 tools/validate_story_data.py` after any data edit.

---

## Quick links by role

| I need to… | Read |
|------------|------|
| Understand the game | [GDD.md](GDD.md) → [STORYBOARD.md](STORYBOARD.md) |
| Build the next phase | [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) · branch: `game/development` |
| Sprint planning (Linear) | [AGILE_WITHIN_PHASES.md](AGILE_WITHIN_PHASES.md) · `game/data/qa/sprint_phases.json` |
| **Sprint orchestration (enforced)** | [SPRINT_ORCHESTRATION.md](SPRINT_ORCHESTRATION.md) · [PM_AGENT_RUNBOOK.md](PM_AGENT_RUNBOOK.md) · `bash tools/run_pm_orchestrator.sh` |
| **Cloud Agent factory (event-driven)** | [CLOUD_AGENT_SETUP_RUNBOOK.md](CLOUD_AGENT_SETUP_RUNBOOK.md) · `bash tools/pm_emit_cycle_event.sh` |
| **Day-one secrets (how to get every key)** | [CURSOR_SECRETS_SETUP.md](CURSOR_SECRETS_SETUP.md) · `bash tools/check_day_one_secrets.sh` |
| **Factory watchdog (stall/hang recovery)** | [FACTORY_WATCHDOG.md](FACTORY_WATCHDOG.md) · `bash tools/run_factory_watchdog.sh` |
| **Branch + done criteria** | [MULTI_AGENT_BRANCH_STRATEGY.md](MULTI_AGENT_BRANCH_STRATEGY.md) |
| **Stakeholder / Telegram reports** | [PM_STAKEHOLDER_REPORTING.md](PM_STAKEHOLDER_REPORTING.md) |
| Branch / merge policy | [BRANCHING.md](BRANCHING.md) |
| Environments (dev/qa/uat/preprod) | [ENVIRONMENTS.md](ENVIRONMENTS.md) |
| Multi-agent roles & handoffs | [MULTI_AGENT_TEAM.md](MULTI_AGENT_TEAM.md) · [RR_CHEATSHEET.md](RR_CHEATSHEET.md) |
| Role enforcement / CI | [CONTROLS_CHEATSHEET.md](CONTROLS_CHEATSHEET.md) · [CI.md](CI.md) |
| Issues, logs, GitHub / Linear / Notion | [PROJECT_MANAGEMENT.md](PROJECT_MANAGEMENT.md) |
| GitHub labels, environments, branch rules | [GITHUB_SETUP.md](GITHUB_SETUP.md) |
| Write GDScript | [CODE_STYLE.md](CODE_STYLE.md) + [TECHNICAL_DESIGN.md](TECHNICAL_DESIGN.md) |
| Place zones & interactables | [LEVEL_DESIGN.md](LEVEL_DESIGN.md) |
| Tune combat / economy | [COMBAT_SYSTEMS.md](COMBAT_SYSTEMS.md) + [PROGRESSION_TUNING.md](PROGRESSION_TUNING.md) |
| Author dialogue / flags | [QUEST_AND_FLAGS.md](QUEST_AND_FLAGS.md) + `game/data/dialogue/` |
| Set up lighting / materials | [RENDERING_GUIDE.md](RENDERING_GUIDE.md) + [ENVIRONMENT_KITS.md](ENVIRONMENT_KITS.md) |
| Generate art (automated) | [ART_AUTOMATION_PIPELINE.md](ART_AUTOMATION_PIPELINE.md) · [GENERATION_READINESS.md](GENERATION_READINESS.md) |
| Run agents / MCP | [MCP_STACK.md](MCP_STACK.md) + [AGENTS.md](../AGENTS.md) |
| Cloud snapshot launch | [CLOUD_SNAPSHOT_LAUNCH.md](CLOUD_SNAPSHOT_LAUNCH.md) — snapshot id + boot checklist (`game/development`) |
| Code base classes (extend-only) | [CODE_BASE_CLASS_RULES.md](CODE_BASE_CLASS_RULES.md) · `game/data/code/base_classes.json` |
| Component scenes (GDAI) | [LEVEL_DESIGN.md](LEVEL_DESIGN.md) §1b |
| QA pass/fail (measurable) | [ACCEPTANCE_CRITERIA.md](ACCEPTANCE_CRITERIA.md) → domain QA below |
| Review look & feel (AI + human) | [VISUAL_QA.md](VISUAL_QA.md) + [MODEL_QA.md](MODEL_QA.md) + [AUDIO_QA.md](AUDIO_QA.md) |
| Fix QA FAIL (no infinite retry) | [QA_REMEDIATION_LOOP.md](QA_REMEDIATION_LOOP.md) |
| Ship on Steam | [MILESTONES.md](MILESTONES.md) §M6 + [STEAM_RELEASE_CHECKLIST.md](STEAM_RELEASE_CHECKLIST.md) + [CD.md](CD.md) |

---

## 1. Vision & narrative

| Doc | Purpose |
|-----|---------|
| [GDD.md](GDD.md) | Master game design — scope, pillars, audience |
| [STORYBOARD.md](STORYBOARD.md) | 20-scene narrative bible (SC-00…SC-17a/b/c; 18 experienced per run) |
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
| [SKILLS_BIBLE.md](SKILLS_BIBLE.md) | 14 player + 6 enemy skills |
| [BOSS_DESIGNS.md](BOSS_DESIGNS.md) | Shore Wraith, Sentinel, Tide Keeper |
| [ENCOUNTER_TABLE.md](ENCOUNTER_TABLE.md) | Pacing, XP, drops, shop timing |
| [PROGRESSION_TUNING.md](PROGRESSION_TUNING.md) | XP curve, stats at milestones, difficulty |
| [ITEMS_AND_ECONOMY.md](ITEMS_AND_ECONOMY.md) | 20 items, shop, drops, inflation guards |
| [TUTORIAL_DESIGN.md](TUTORIAL_DESIGN.md) | Onboarding + SC-00 prologue |
| [GAME_FEEL.md](GAME_FEEL.md) | Juice, feedback, rewards · `game/data/qa/feel_thresholds.json` |
| [ACHIEVEMENTS.md](ACHIEVEMENTS.md) | 13 Steam achievements |

---

## 4. Technical architecture

| Doc | Purpose |
|-----|---------|
| [TECHNICAL_DESIGN.md](TECHNICAL_DESIGN.md) | **TDD** — autoloads, scene flow, combat stack, save pipeline |
| [CODE_BASE_CLASS_RULES.md](CODE_BASE_CLASS_RULES.md) | **Extend-only** base classes + component scene catalog |
| [CODE_STYLE.md](CODE_STYLE.md) | GDScript conventions, folders, signals, naming |
| [DATA_ARCHITECTURE.md](DATA_ARCHITECTURE.md) | Story-first JSON layout, schema versions |
| [SAVE_AND_FAIL_STATES.md](SAVE_AND_FAIL_STATES.md) | Save slots, autosave, game over |
| [LOCALIZATION.md](LOCALIZATION.md) | en / ja / zh / zh-Hant, dialect VO, CSV, fonts |
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
| [MODEL_QA.md](MODEL_QA.md) | **3D GLB lint + turntable vision jury** |
| [VISUAL_QA.md](VISUAL_QA.md) | Screenshot + vision gates (in-scene) |
| [ART_AUTOMATION_PIPELINE.md](ART_AUTOMATION_PIPELINE.md) | **Quality-first automated art/audio** — tier matrix, workflows |
| [GENERATION_READINESS.md](GENERATION_READINESS.md) | **Human-expectation gaps** — per-character/zone gen briefs, composition contracts |
| [generation_briefs/](generation_briefs/README.md) | **30 gen briefs** — 3D heroes/zones + 8 hero BGM + 5 P0 VO |
| [RENDERING_GUIDE.md](RENDERING_GUIDE.md) | Forward+ tonemap, fog, glow, zone presets |
| [ART_DIRECTION.md](ART_DIRECTION.md) | Palette, silhouettes, muted-coastal look — what to avoid |
| [CHARACTER_BIBLE.md](CHARACTER_BIBLE.md) | Models, portraits, boss meshes, rig |
| [ITEMS_3D_MODEL_GUIDE.md](ITEMS_3D_MODEL_GUIDE.md) | Props, weapons, pickup meshes |
| [AUDIO_DIRECTION.md](AUDIO_DIRECTION.md) | Music map, SFX philosophy |
| [AUDIO_QA.md](AUDIO_QA.md) | **BGM + P0 VO** — technical lint + scoped LLM listen jury |
| [AUDIO_PRODUCTION_GUIDE.md](AUDIO_PRODUCTION_GUIDE.md) | Buses, loudness; scene map in `scene_audio_map.json` |
| [STORYBOARD_ILLUSTRATIONS.md](STORYBOARD_ILLUSTRATIONS.md) | Pitch art spec |
| [ASSET_COMPLIANCE.md](ASSET_COMPLIANCE.md) | Copyright-safe policy |
| [LICENSES.md](LICENSES.md) | Attribution log |

---

## 7. Production & QA

**Start:** [ACCEPTANCE_CRITERIA.md](ACCEPTANCE_CRITERIA.md) (measurable gates) · `game/data/qa/acceptance_criteria.json`  
**Agents:** [RR_CHEATSHEET.md](RR_CHEATSHEET.md) · [CONTROLS_CHEATSHEET.md](CONTROLS_CHEATSHEET.md)

| Doc | Purpose |
|-----|---------|
| [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) | Rebuild phases 0–8 |
| [BRANCHING.md](BRANCHING.md) | `main` vs `game/development` merge policy |
| [AGILE_WITHIN_PHASES.md](AGILE_WITHIN_PHASES.md) | Phase-gated Agile + sprint cadence |
| [MILESTONES.md](MILESTONES.md) | Feature checklist (M5 art → M6 Steam) |
| [CI.md](CI.md) | GitHub Actions — `main` vs `game/development` gates |
| [CD.md](CD.md) | Artifact + Steam deploy pipelines |
| [STEAM_RELEASE_CHECKLIST.md](STEAM_RELEASE_CHECKLIST.md) | Ship gaps (technical + store) |
| [AI_DEV_WORKFLOW.md](AI_DEV_WORKFLOW.md) | Build policy, phase acceptance |
| [AI_TESTING_SPEC.md](AI_TESTING_SPEC.md) | L0–L6 automated + human QA |
| [QA_AND_BUG_PROCESS.md](QA_AND_BUG_PROCESS.md) | Severity, triage, milestone gates |
| [ACCEPTANCE_CRITERIA.md](ACCEPTANCE_CRITERIA.md) | Measurable QA gates — WARN/SKIP ≠ PASS |
| [QA_REMEDIATION_LOOP.md](QA_REMEDIATION_LOOP.md) | FAIL iteration — industry refs + anti-retry |
| [ESCALATION_POLICY.md](ESCALATION_POLICY.md) | Anti-infinite-loop ladder — dev↔QA → Architect/SA → Product Owner |
| [FLOW_QA.md](FLOW_QA.md) | Game flow QA + iterative fix loop |
| [PLAYTEST_TELEMETRY.md](PLAYTEST_TELEMETRY.md) | Playtest telemetry (GUR) — pacing/combat/ending tuning loop |
| [DELIVERY_CONTROL.md](DELIVERY_CONTROL.md) | Pre-delivery review gate — review + confirm before outbound delivery |
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
| `encounters/story_encounters.json` | 9 scripted fights |

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
| Generation readiness (AI 3D + audio) | `GENERATION_READINESS.md` + [`generation_briefs/`](generation_briefs/README.md) + `game/data/audio/audio_qa_catalog.json` |
| Asset registry | `LICENSES.md` + `asset_manifest.license.json` |
| Production timeline | `IMPLEMENTATION_PLAN.md` + `MILESTONES.md` |
