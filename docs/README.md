# Tides of Urashima — Documentation Index

**Start here.** Design and production docs are grouped by topic under `docs/<folder>/`.

### Printable cheat sheets (agents)

| Doc | Purpose |
|-----|---------|
| [RR_CHEATSHEET.md](cheat-sheets/RR_CHEATSHEET.md) | **Roles** — who owns what, handoffs, tools |
| [CONTROLS_CHEATSHEET.md](cheat-sheets/CONTROLS_CHEATSHEET.md) | **Controls** — CI gates, PR templates, branch protection |

---

## Folder map

| Folder | Contents |
|--------|----------|
| [cheat-sheets/](cheat-sheets/) | Agent quick-reference cards |
| [vision/](vision/) | GDD, storyboard, narrative voice, endings |
| [world/](world/) | Levels, zones, quests, environment kits |
| [gameplay/](gameplay/) | Combat, skills, economy, progression, achievements |
| [technical/](technical/) | TDD, data architecture, code style, spec-first |
| [ui/](ui/) | Menus, settings, cinematics |
| [art/](art/) | Art direction, rendering, characters, visual/model QA |
| [audio/](audio/) | Music/SFX direction, production, QA, audio sheets |
| [qa/](qa/) | Acceptance gates, testing, playtest, security, perf |
| [workflow/](workflow/) | Implementation plan, branching, milestones, Agile |
| [ci-cd/](ci-cd/) | CI, CD, environments, GitHub, Steam ship |
| [agents/](agents/) | Multi-agent team, MCP, PM orchestration, cloud setup |
| [generation_briefs/](generation_briefs/README.md) | AI art/audio generation briefs |
| [sprints/](sprints/Phase1-Sprint1-issues.md) | Active sprint issue packs |
| [compliance/](compliance/COMPLIANCE_REPORT.md) | License compliance reports |
| [pitch/](pitch/illustrations/README.md) | Pitch illustrations (not in-game) |
| [deprecated/](deprecated/GDAI_REGEN_PLAN.md) | Superseded docs |

---

## Authority chain (when docs disagree)

| Priority | Document | Answers |
|----------|----------|---------|
| 1 | [IMPLEMENTATION_PLAN.md](workflow/IMPLEMENTATION_PLAN.md) | What to build, in what order (Phases 0–8) |
| 1b | [BRANCHING.md](workflow/BRANCHING.md) | `main` = docs/data · `game/development` = implementation |
| 1b2 | [SPEC_FIRST_DEVELOPMENT.md](technical/SPEC_FIRST_DEVELOPMENT.md) | Complete specs on `main`; code after `SPEC_DEV_START` |
| 1b3 | [GDSCRIPT_REGENERATION.md](technical/GDSCRIPT_REGENERATION.md) | Rebuild core helpers from Python refs |
| 1c | [ENVIRONMENTS.md](ci-cd/ENVIRONMENTS.md) | dev · qa · uat · preprod · prod promotion |
| 1d | [AGILE_WITHIN_PHASES.md](workflow/AGILE_WITHIN_PHASES.md) | Phase-gated Agile + sprint map |
| 2 | [MILESTONES.md](workflow/MILESTONES.md) | Deliverable checklist |
| 3 | [TECHNICAL_DESIGN.md](technical/TECHNICAL_DESIGN.md) | Runtime architecture |
| 4 | [DATA_ARCHITECTURE.md](technical/DATA_ARCHITECTURE.md) + `game/data/` | Story JSON spine + save shape |
| 5 | [MCP_STACK.md](agents/MCP_STACK.md) + [ART_AUTOMATION_PIPELINE.md](art/ART_AUTOMATION_PIPELINE.md) + [`.cursorrules`](../.cursorrules) | Tools and agent rules |

**Numeric values rule:** For runtime numbers — **`game/data/*.json` wins** over design-doc prose. Run `python3 tools/validate_story_data.py` after any data edit.

---

## Quick links by role

| I need to… | Read |
|------------|------|
| Understand the game | [GDD.md](vision/GDD.md) → [STORYBOARD.md](vision/STORYBOARD.md) |
| Build the next phase | [IMPLEMENTATION_PLAN.md](workflow/IMPLEMENTATION_PLAN.md) · branch: `game/development` |
| Sprint planning | [AGILE_WITHIN_PHASES.md](workflow/AGILE_WITHIN_PHASES.md) · `game/data/qa/sprint_phases.json` |
| **Sprint orchestration** | [SPRINT_ORCHESTRATION.md](agents/SPRINT_ORCHESTRATION.md) · [PM_AGENT_RUNBOOK.md](agents/PM_AGENT_RUNBOOK.md) |
| **Cloud Agent factory** | [CLOUD_AGENT_SETUP_RUNBOOK.md](agents/CLOUD_AGENT_SETUP_RUNBOOK.md) |
| **Secrets setup** | [CURSOR_SECRETS_SETUP.md](agents/CURSOR_SECRETS_SETUP.md) |
| **Factory watchdog** | [FACTORY_WATCHDOG.md](agents/FACTORY_WATCHDOG.md) |
| **Branch strategy** | [MULTI_AGENT_BRANCH_STRATEGY.md](agents/MULTI_AGENT_BRANCH_STRATEGY.md) |
| Multi-agent roles | [MULTI_AGENT_TEAM.md](agents/MULTI_AGENT_TEAM.md) · [RR_CHEATSHEET.md](cheat-sheets/RR_CHEATSHEET.md) |
| Role enforcement / CI | [CONTROLS_CHEATSHEET.md](cheat-sheets/CONTROLS_CHEATSHEET.md) · [CI.md](ci-cd/CI.md) |
| Issues / GitHub / Linear | [PROJECT_MANAGEMENT.md](agents/PROJECT_MANAGEMENT.md) |
| Write GDScript | [CODE_STYLE.md](technical/CODE_STYLE.md) + [TECHNICAL_DESIGN.md](technical/TECHNICAL_DESIGN.md) |
| Place zones | [LEVEL_DESIGN.md](world/LEVEL_DESIGN.md) |
| Tune combat | [COMBAT_SYSTEMS.md](gameplay/COMBAT_SYSTEMS.md) + [PROGRESSION_TUNING.md](gameplay/PROGRESSION_TUNING.md) |
| Lighting / materials | [RENDERING_GUIDE.md](art/RENDERING_GUIDE.md) + [ENVIRONMENT_KITS.md](world/ENVIRONMENT_KITS.md) |
| Generate art | [ART_AUTOMATION_PIPELINE.md](art/ART_AUTOMATION_PIPELINE.md) · [GENERATION_READINESS.md](art/GENERATION_READINESS.md) |
| Run agents / MCP | [MCP_STACK.md](agents/MCP_STACK.md) + [AGENTS.md](../AGENTS.md) |
| QA pass/fail | [ACCEPTANCE_CRITERIA.md](qa/ACCEPTANCE_CRITERIA.md) |
| Ship on Steam | [MILESTONES.md](workflow/MILESTONES.md) §M6 + [STEAM_RELEASE_CHECKLIST.md](ci-cd/STEAM_RELEASE_CHECKLIST.md) |

---

## 1. Vision & narrative — `docs/vision/`

| Doc | Purpose |
|-----|---------|
| [GDD.md](vision/GDD.md) | Master game design — scope, pillars, audience |
| [STORYBOARD.md](vision/STORYBOARD.md) | 20-scene narrative bible |
| [NARRATIVE_WRITING_GUIDE.md](vision/NARRATIVE_WRITING_GUIDE.md) | Voice, silence, selective VO, i18n prose |
| [NARRATIVE_DENSITY.md](vision/NARRATIVE_DENSITY.md) | §12 budgets — decision tree + L0 gate |
| [VO_HIT_LIST.md](vision/VO_HIT_LIST.md) | 12 ElevenLabs clips |
| [ENDING_DESIGN.md](vision/ENDING_DESIGN.md) | Three endings, choice UI, replay |
| [LORE_AND_ENVIRONMENTAL_STORY.md](vision/LORE_AND_ENVIRONMENTAL_STORY.md) | Lore entries, environmental storytelling |
| [PACING_CHART.md](vision/PACING_CHART.md) | Emotional beat timeline |
| [REPLAY_DESIGN.md](vision/REPLAY_DESIGN.md) | Ending gallery, second run |
| [STORYBOARD_ILLUSTRATIONS.md](vision/STORYBOARD_ILLUSTRATIONS.md) | Pitch art spec |

---

## 2. World & levels — `docs/world/`

| Doc | Purpose |
|-----|---------|
| [LEVEL_DESIGN.md](world/LEVEL_DESIGN.md) | Per-zone blockouts, interactables, triggers |
| [WORLD_MAP_AND_FLOW.md](world/WORLD_MAP_AND_FLOW.md) | Zone graph, connections, save points |
| [ENVIRONMENT_KITS.md](world/ENVIRONMENT_KITS.md) | Modular art kits, per-zone assets |
| [PUZZLE_DESIGN.md](world/PUZZLE_DESIGN.md) | SC-07 water puzzle |
| [QUEST_AND_FLAGS.md](world/QUEST_AND_FLAGS.md) | 5 quests, flag registry |

---

## 3. Gameplay systems — `docs/gameplay/`

| Doc | Purpose |
|-----|---------|
| [COMBAT_SYSTEMS.md](gameplay/COMBAT_SYSTEMS.md) | Turn order, elements, intent UI |
| [SKILLS_BIBLE.md](gameplay/SKILLS_BIBLE.md) | Player + enemy skills |
| [BOSS_DESIGNS.md](gameplay/BOSS_DESIGNS.md) | Boss fights, emotional facets |
| [ENCOUNTER_TABLE.md](gameplay/ENCOUNTER_TABLE.md) | Pacing, XP, drops |
| [PROGRESSION_TUNING.md](gameplay/PROGRESSION_TUNING.md) | XP curve, difficulty |
| [ITEMS_AND_ECONOMY.md](gameplay/ITEMS_AND_ECONOMY.md) | Items, shop, economy |
| [TUTORIAL_DESIGN.md](gameplay/TUTORIAL_DESIGN.md) | Onboarding + SC-00 |
| [GAME_FEEL.md](gameplay/GAME_FEEL.md) | Juice, feedback, rewards |
| [ACHIEVEMENTS.md](gameplay/ACHIEVEMENTS.md) | Steam achievements |

---

## 4. Technical architecture — `docs/technical/`

| Doc | Purpose |
|-----|---------|
| [TECHNICAL_DESIGN.md](technical/TECHNICAL_DESIGN.md) | TDD — autoloads, combat stack, save |
| [DATA_ARCHITECTURE.md](technical/DATA_ARCHITECTURE.md) | Story-first JSON layout |
| [CODE_BASE_CLASS_RULES.md](technical/CODE_BASE_CLASS_RULES.md) | Extend-only base classes |
| [CODE_STYLE.md](technical/CODE_STYLE.md) | GDScript conventions |
| [SAVE_AND_FAIL_STATES.md](technical/SAVE_AND_FAIL_STATES.md) | Save slots, game over |
| [LOCALIZATION.md](technical/LOCALIZATION.md) | en / ja / zh / zh-Hant |
| [TECH_STACK.md](technical/TECH_STACK.md) | Godot 4.7, plugin versions |
| [PLUGIN_COMPATIBILITY.md](technical/PLUGIN_COMPATIBILITY.md) | GDAI, Godotiq, MCP Pro |
| [SPEC_FIRST_DEVELOPMENT.md](technical/SPEC_FIRST_DEVELOPMENT.md) | Spec on `main`; code after gate |
| [GDSCRIPT_REGENERATION.md](technical/GDSCRIPT_REGENERATION.md) | Core helper port workflow |

---

## 5. UI & cinematics — `docs/ui/`

| Doc | Purpose |
|-----|---------|
| [UI_UX_FLOW.md](ui/UI_UX_FLOW.md) | Menus, HUD, controller map |
| [SETTINGS_ACCESSIBILITY.md](ui/SETTINGS_ACCESSIBILITY.md) | Options, hard mode, a11y |
| [CINEMATICS.md](ui/CINEMATICS.md) | Cameras, boss intros, endings |

---

## 6. Art & assets — `docs/art/`

| Doc | Purpose |
|-----|---------|
| [ART_DIRECTION.md](art/ART_DIRECTION.md) | Palette, silhouettes, muted-coastal look |
| [RENDERING_GUIDE.md](art/RENDERING_GUIDE.md) | Tonemap, fog, glow, zone presets |
| [CHARACTER_BIBLE.md](art/CHARACTER_BIBLE.md) | Models, portraits, rig |
| [ITEMS_3D_MODEL_GUIDE.md](art/ITEMS_3D_MODEL_GUIDE.md) | Props, weapons, pickups |
| [ART_AUTOMATION_PIPELINE.md](art/ART_AUTOMATION_PIPELINE.md) | Automated art/audio tiers |
| [GENERATION_READINESS.md](art/GENERATION_READINESS.md) | Gen briefs, composition contracts |
| [VISUAL_QA.md](art/VISUAL_QA.md) | Screenshot + vision gates |
| [MODEL_QA.md](art/MODEL_QA.md) | GLB lint + turntable jury |
| [ASSET_COMPLIANCE.md](art/ASSET_COMPLIANCE.md) | Copyright-safe policy |
| [LICENSES.md](art/LICENSES.md) | Attribution log |

---

## 7. Audio — `docs/audio/`

| Doc | Purpose |
|-----|---------|
| [AUDIO_DIRECTION.md](audio/AUDIO_DIRECTION.md) | Music map, SFX philosophy |
| [AUDIO_PRODUCTION_GUIDE.md](audio/AUDIO_PRODUCTION_GUIDE.md) | Buses, loudness, scene map |
| [AUDIO_QA.md](audio/AUDIO_QA.md) | BGM + VO listen jury |
| [audio_sheets/](audio/audio_sheets/README.md) | Per-track production sheets |

---

## 8. QA & quality — `docs/qa/`

| Doc | Purpose |
|-----|---------|
| [ACCEPTANCE_CRITERIA.md](qa/ACCEPTANCE_CRITERIA.md) | Measurable gates — WARN/SKIP ≠ PASS |
| [AI_TESTING_SPEC.md](qa/AI_TESTING_SPEC.md) | L0–L6 automated + human QA |
| [QA_AND_BUG_PROCESS.md](qa/QA_AND_BUG_PROCESS.md) | Severity, triage |
| [QA_REMEDIATION_LOOP.md](qa/QA_REMEDIATION_LOOP.md) | FAIL iteration policy |
| [FLOW_QA.md](qa/FLOW_QA.md) | Game flow QA |
| [PLAYTEST_SCRIPT.md](qa/PLAYTEST_SCRIPT.md) | 2–3h human playthrough |
| [PLAYTEST_TELEMETRY.md](qa/PLAYTEST_TELEMETRY.md) | Telemetry tuning loop |
| [PERFORMANCE_BASELINE.md](qa/PERFORMANCE_BASELINE.md) | FPS hardware baseline |
| [PLATFORM_SUPPORT.md](qa/PLATFORM_SUPPORT.md) | Linux + Windows ship |
| [SECURITY.md](qa/SECURITY.md) | Secrets, ship build strip |
| [ESCALATION_POLICY.md](qa/ESCALATION_POLICY.md) | Anti-infinite-loop ladder |

---

## 9. Workflow & production — `docs/workflow/` + `docs/ci-cd/`

| Doc | Purpose |
|-----|---------|
| [IMPLEMENTATION_PLAN.md](workflow/IMPLEMENTATION_PLAN.md) | Rebuild phases 0–8 |
| [BRANCHING.md](workflow/BRANCHING.md) | `main` vs `game/development` |
| [MILESTONES.md](workflow/MILESTONES.md) | M5 art → M6 Steam checklist |
| [AGILE_WITHIN_PHASES.md](workflow/AGILE_WITHIN_PHASES.md) | Phase-gated Agile |
| [AI_DEV_WORKFLOW.md](workflow/AI_DEV_WORKFLOW.md) | Build policy, phase acceptance |
| [DELIVERY_CONTROL.md](workflow/DELIVERY_CONTROL.md) | Pre-delivery review gate |
| [CI.md](ci-cd/CI.md) | GitHub Actions gates |
| [CD.md](ci-cd/CD.md) | Artifact + Steam deploy |
| [ENVIRONMENTS.md](ci-cd/ENVIRONMENTS.md) | dev → prod promotion |
| [GITHUB_SETUP.md](ci-cd/GITHUB_SETUP.md) | Labels, branch protection |
| [STEAM_RELEASE_CHECKLIST.md](ci-cd/STEAM_RELEASE_CHECKLIST.md) | Ship gaps |

---

## 10. Agents & tooling — `docs/agents/`

| Doc | Purpose |
|-----|---------|
| [MULTI_AGENT_TEAM.md](agents/MULTI_AGENT_TEAM.md) | Team roster, handoffs |
| [MULTI_AGENT_BRANCH_STRATEGY.md](agents/MULTI_AGENT_BRANCH_STRATEGY.md) | Branch + done criteria |
| [MCP_STACK.md](agents/MCP_STACK.md) | Full MCP toolchain |
| [SPRINT_ORCHESTRATION.md](agents/SPRINT_ORCHESTRATION.md) | Enforced dispatch |
| [PM_AGENT_RUNBOOK.md](agents/PM_AGENT_RUNBOOK.md) | PM session steps |
| [PM_STAKEHOLDER_REPORTING.md](agents/PM_STAKEHOLDER_REPORTING.md) | Telegram reports |
| [PROJECT_MANAGEMENT.md](agents/PROJECT_MANAGEMENT.md) | GitHub Issues |
| [FACTORY_WATCHDOG.md](agents/FACTORY_WATCHDOG.md) | Stall recovery |
| [GDAI_CLOUD_SETUP.md](agents/GDAI_CLOUD_SETUP.md) | Cloud agent bootstrap |
| [PLUGIN_INSTALL_GUIDE.md](agents/PLUGIN_INSTALL_GUIDE.md) | MCP plugin install |
| [CLOUD_AGENT_SETUP_RUNBOOK.md](agents/CLOUD_AGENT_SETUP_RUNBOOK.md) | Event-driven factory |
| [CLOUD_SNAPSHOT_LAUNCH.md](agents/CLOUD_SNAPSHOT_LAUNCH.md) | Snapshot boot |
| [CURSOR_SECRETS_SETUP.md](agents/CURSOR_SECRETS_SETUP.md) | Day-one secrets |

---

## 11. Data layer (`game/data/`)

| Path | Purpose |
|------|---------|
| [game/data/README.md](../game/data/README.md) | Load API, schema summary |
| `story/scenes.json` | Master scene spine |
| `dialogue/chapter_01.json` | Dialogue + voice_id lines |

```bash
python3 tools/validate_story_data.py
```

---

## 12. Marketing (not in-game)

| Path | Purpose |
|------|---------|
| [steam/STORE_PAGE.md](../steam/STORE_PAGE.md) | Steam store copy |
| [pitch/illustrations/](pitch/illustrations/README.md) | Pitch PNGs |

---

## Deprecated

| Doc | Replacement |
|-----|-------------|
| [GDAI_REGEN_PLAN.md](deprecated/GDAI_REGEN_PLAN.md) | [IMPLEMENTATION_PLAN.md](workflow/IMPLEMENTATION_PLAN.md) |

---

## Industry-standard coverage map

| Studio artifact | Our doc |
|-----------------|---------|
| GDD | `vision/GDD.md` |
| Level design | `world/LEVEL_DESIGN.md` |
| TDD | `technical/TECHNICAL_DESIGN.md` |
| Art bible | `art/ART_DIRECTION.md` + `art/RENDERING_GUIDE.md` |
| Production timeline | `workflow/IMPLEMENTATION_PLAN.md` + `workflow/MILESTONES.md` |
