# Tides of Urashima — Implementation Plan

**Version:** 1.2 (Fresh rebuild)  
**Branch:** `main` (documentation + `game/data/` only) · **`game/development`** (Godot implementation)  
**Source of truth:** `main` design docs + `game/data/` JSON + `game/data/code/*_registry.json`  
**Spec-first:** See `docs/technical/SPEC_FIRST_DEVELOPMENT.md` — no ship `.gd`/`.tscn` on `main`; build on `game/development` after `SPEC_DEV_START`.  
**Workflow:** GodotPrompter + full MCP toolchain — see `docs/agents/MCP_STACK.md`.  
**Milestone checklist:** `docs/workflow/MILESTONES.md` (M5 art → M6 Steam).

Previous full implementation on `main` was **stripped** (boot shell + data only). Phases 1–6 rebuild from documentation via GDAI MCP on **`game/development`**.

**All Phase 1–8 implementation work happens on `game/development`.** Do not merge to `main` until M6 ship-ready.

**Sprint execution:** Phase-gated Agile — 2-week Linear cycles inside each phase (`docs/workflow/AGILE_WITHIN_PHASES.md`, `game/data/qa/sprint_phases.json`).

### Phase ↔ milestone map

| Phase | Milestone | Focus |
|-------|-----------|-------|
| 0 | M0, M0c–M0h | Dev environment + design/data baseline ✅ |
| 1 | — | Environment foundation + SC-02 vertical slice gate |
| 2–3 | M1 | Core systems + narrative exploration |
| 4 | M2 | Combat vertical slice |
| 5 | M3 | Chapter 1 dungeons |
| 6 | M4 | Full story + three endings |
| 7 | **M5** | Art rebuild (NPR zones, hero meshes, curated audio) |
| 8 | **M6** | Steam export, compliance, playtest |

---

## Phase 0 — Dev environment ✅ (current)

| Task | Status |
|------|--------|
| `game/project.godot` (Godot 4.7 Forward+) | Done |
| Folder structure (`tools/setup_dev_environment.sh`) | Done |
| `tools/check_dev_environment.sh` | Done |
| `.cursor/mcp.json.example` (GDAI MCP) | Done |
| `game/addons/README.md` | Done |
| Boot / data validation (`GameBootstrap` autoload) | **Specified** on `main` (`autoload_registry.json`) — **built** Phase 2 on `game/development` |
| `game/project.godot` | **Not on `main`** — created Phase 1 on `game/development` |
| Cloud install (`tools/install_cloud_dev.sh`, `.cursor/environment.json`) | Done |
| Story data validator (`tools/validate_story_data.py`) | Done |
| GDAI MCP workflow rules (`.cursorrules`, `tools/ensure_gdai_mcp.sh`) | Done |
| Fresh-rebuild smoke (`tools/run_playtest_smoke.sh`) | Done |
| QA acceptance catalog (`game/data/qa/acceptance_criteria.json`, `docs/qa/ACCEPTANCE_CRITERIA.md`) | Done |
| QA remediation + domain gates (MODEL/VISUAL/AUDIO/FLOW QA docs) | Done |
| AI dev workflow doc (`docs/workflow/AI_DEV_WORKFLOW.md`) | Done |
| AI testing spec (`docs/qa/AI_TESTING_SPEC.md`) | Done |
| Unit tests (`tools/run_unit_tests.sh`, `game/tests/unit/`) | Done |
| Code base class registry (`docs/technical/CODE_BASE_CLASS_RULES.md`, `game/data/code/base_classes.json`) | Done |
| Base-class + animation + gdlint CI gates (`acceptance_criteria.json`, `run_ci_checks.sh`) | Done |

**Verify:**

```bash
bash tools/setup_dev_environment.sh
bash tools/ensure_gdai_mcp.sh
bash tools/check_dev_environment.sh
python3 tools/validate_acceptance_criteria.py
bash tools/run_unit_tests.sh
bash tools/run_playtest_smoke.sh
# Open game/project.godot in Godot 4.7 → F5
```

---

## Phase 1 — Environment foundation (NEXT)

**Read first:** `docs/world/LEVEL_DESIGN.md` (zone `ruined_village`), `docs/art/RENDERING_GUIDE.md`

Build stylized zone rendering before gameplay systems. Follow `docs/art/RENDERING_GUIDE.md`.

| # | Task | Docs |
|---|------|------|
| 1.1 | `environments/*.tres` — WorldEnvironment per zone (tonemap, fog, glow) | RENDERING_GUIDE §3–6 |
| 1.2 | `scripts/exploration/zone_visuals.gd` — apply palette, sky, lights at runtime | ENVIRONMENT_KITS §1 |
| 1.3 | `shaders/toon_base.gdshader` — single ramp family | ART_DIRECTION §7 |
| 1.4 | `shaders/water_stylized.gdshader` — foam + gentle displacement | ART_DIRECTION §3.6 |
| 1.5 | Greybox zone scenes: `beach_shore`, `ruined_village`, `tidal_caves`, `dragon_palace_gate` | STORYBOARD, ENVIRONMENT_KITS |
| 1.6 | DirectionalLight3D + fog per zone table | RENDERING_GUIDE §5 |
| 1.7 | ProceduralSky per zone (no HDRI) | RENDERING_GUIDE §4 |
| 1.8 | Component scenes from `LEVEL_DESIGN.md` §1b — wells, doors, triggers via GDAI | CODE_BASE_CLASS_RULES, LEVEL_DESIGN §1b |
| 1.9 | **Vertical slice gate:** SC-02 Ruined Village passes art checklist (**Phase 1 greybox section** of ART_DIRECTION §10; final-art section lands in Phase 7) | ART_DIRECTION §10 |
| 1.10 | **Golden gameplay screenshot** — `ruined_village` path in `zone_composition.json` → `artifacts/screenshots/phase1_ruined_village_gameplay.png` (GDAI capture) | GENERATION_READINESS §X-02, **GR-001** |
| 1.11 | Zone composition smoke (warn) — `bash tools/run_zone_composition_checks.sh` after greybox zones load | `zone_composition.json`, **GR-003** |

**GDAI workflow:** GodotPrompter drafts shaders/`zone_visuals.gd` → GDAI MCP places nodes in `.tscn` → F5 verify. **Acceptance criteria:** `docs/workflow/AI_DEV_WORKFLOW.md` §4 Phase 1.

---

## Phase 2 — Core systems shell

**Read first:** `docs/technical/TECHNICAL_DESIGN.md`, `docs/technical/CODE_STYLE.md`

| # | Task | Docs |
|---|------|------|
| 2.1 | Autoloads: `GameManager`, `EventBus`, `SaveSystem`, `DialogueRunner`, `CombatManager` | GDD, DATA_ARCHITECTURE |
| 2.2 | `GameManager.load_json("res://data/...")` API | game/data/README.md |
| 2.3 | `LocalizationManager` + `FontThemeManager` + Noto fonts (en / ja / zh / zh-Hant) | LOCALIZATION.md |
| 2.4 | Main menu → New Game → SC-00 prologue → `beach_shore` | UI_UX_FLOW.md, TUTORIAL_DESIGN |
| 2.5 | `PlayerController` base class + `player.tscn` component scene | CODE_BASE_CLASS_RULES, GAME_FEEL.md |
| 2.6 | Scene transitions between zones | WORLD_MAP_AND_FLOW.md |
| 2.7 | `AudioManager` shell — BGM crossfade, SFX buses, procedural placeholders | AUDIO_PRODUCTION_GUIDE |
| 2.8 | Settings menu — language, `vo_dialect` (zh-Hant), volume sliders | SETTINGS_ACCESSIBILITY.md, LOCALIZATION.md |

---

## Phase 3 — Narrative & exploration

| # | Task | Docs |
|---|------|------|
| 3.1 | Dialogue box UI + `DialogueRunner` wired to `game/data/dialogue/` | NARRATIVE_WRITING_GUIDE |
| 3.2 | `VoiceLinePlayer` + `DialogueRunner` VO hookup (locale paths; zh-Hant `cant`/`cmn`; BGM duck) | VO_HIT_LIST.md, TECHNICAL_DESIGN |
| 3.3 | Interactables + interaction prompt HUD | UI_UX_FLOW.md |
| 3.4 | Quest tracker + flag system from `story/flags.json` | QUEST_AND_FLAGS.md |
| 3.5 | Tab inventory / equipment menu | UI_UX_FLOW.md, ITEMS_AND_ECONOMY |
| 3.6 | Roku shop UI (`shop/roku_shop.json`) | ITEMS_AND_ECONOMY |
| 3.7 | SC-00 prologue + `CinematicDirector` opening hook | CINEMATICS.md, TUTORIAL_DESIGN |
| 3.8 | SC-01 through SC-05 field content (village hub) | STORYBOARD.md |
| 3.9 | Lore collectibles | LORE_AND_ENVIRONMENTAL_STORY.md |
| 3.10 | Written i18n — `zh-Hant` in `game/data/` + core `translations.csv` (expand CSV for skills/combat in Phase 3) | LOCALIZATION.md |

---

## Phase 4 — Combat vertical slice

| # | Task | Docs |
|---|------|------|
| 4.1 | Combat UI (HP/MP, intent icons, battle log) | COMBAT_SYSTEMS.md |
| 4.2 | Turn order, skills from `skills.json` | SKILLS_BIBLE.md |
| 4.3 | SC-05 Salt Crab tutorial encounter | TUTORIAL_DESIGN.md |
| 4.4 | Boss framework (phases, intent UI) | BOSS_DESIGNS.md |

---

## Phase 5 — Chapter 1 dungeons

| # | Task | Docs |
|---|------|------|
| 5.1 | Tidal caves greybox → art pass; SC-06 entrance | ENVIRONMENT_KITS §5 |
| 5.2 | Water level puzzle SC-07 (silent — no VO) | PUZZLE_DESIGN.md |
| 5.3 | SC-08 echo vignette (`CinematicDirector` + whisper SFX bed) | CINEMATICS.md, STORYBOARD |
| 5.4 | Shore Wraith boss SC-09 | BOSS_DESIGNS.md |
| 5.5 | Yuzu joins SC-10 | CHARACTER_BIBLE.md |

---

## Phase 6 — Full story & endings

| # | Task | Docs |
|---|------|------|
| 6.1 | Dragon Palace Gate zone + SC-12 gate cinematic | ENVIRONMENT_KITS §6, CINEMATICS.md |
| 6.2 | SC-11 flashback + SC-13 box revelation | STORYBOARD.md, CINEMATICS.md |
| 6.3 | Palace Sentinel SC-14 + Tide Keeper SC-15 | BOSS_DESIGNS.md |
| 6.3b | Expand `palace_sentinel` `CHARACTER_BIBLE.md` row to **boss standard** (mesh breakdown, anims, GLB paths) **before** sentinel GLB gen | GENERATION_READINESS §4, **GR-002** |
| 6.4 | SC-16 choice UI + three endings | ENDING_DESIGN.md |
| 6.5 | Ending environment variants + SC-17 cinematics | ENVIRONMENT_KITS §7, CINEMATICS.md |
| 6.6 | Credits sequence | CINEMATICS.md |
| 6.7 | `bash tools/run_e2e_playthrough.sh` — all 3 endings | AI_TESTING_SPEC.md |

---

## Phase 7 — M5 art rebuild

Replace greybox with automated authored assets per `docs/art/ART_DIRECTION.md` + `docs/art/ART_AUTOMATION_PIPELINE.md`:

| # | Task | Docs |
|---|------|------|
| 7.1 | Hero character models — Urashima, Yuzu, Roku + 5 enemies (Meshy/Tripo/Rodin + Mixamo) | CHARACTER_BIBLE.md |
| 7.1b | GLB post-import NPR sanitizer (`install_glb_import_pipeline.sh`) | MODEL_QA.md §M2b |
| 7.1c | Animation whitelist in `qa_catalog.json` — `check_animation_whitelist.py` | MODEL_QA.md §M2c, CHARACTER_BIBLE §8 |
| 7.2 | Hero set-pieces — torii, `palace_gate_main` (SC-12) | ENVIRONMENT_KITS.md |
| 7.3 | Automated stylized zone textures (ComfyUI/Material Maker + `palette_remap.py`) | ART_AUTOMATION_PIPELINE.md |
| 7.4 | ComfyUI/GameLab portraits (replace procedural silhouettes) | ART_AUTOMATION_PIPELINE.md |
| 7.5 | Curated BGM per act — ACE-Step (`bash tools/generate_ai_bgm.sh`); targets in `audio_qa_catalog.json` | AUDIO_PRODUCTION_GUIDE.md, **GR-004**, **GR-006** |
| 7.6 | SFX + ambient beds per `scene_audio_map.json` | AUDIO_PRODUCTION_GUIDE.md, **GR-006** |
| 7.7 | **ElevenLabs voice casting** — replace `PLACEHOLDER_*` in `vo_prompts.json` (incl. `dialect_voices` for zh-Hant) | VO_HIT_LIST.md, **GR-005** |
| 7.8 | **Generate selective VO** — P0 listen pass → P1/P2; `en`/`ja`/`zh` + `zh-Hant` `cant`/`cmn` (`bash tools/generate_ai_vo.sh`) | VO_HIT_LIST.md, LOCALIZATION.md, **GR-005** |
| 7.9 | Audio QA — `bash tools/run_audio_smoke_checks.sh` + `AUDIO_QA.md` (BGM A6/A7 + P0 VO V6/V7) | AUDIO_QA.md, **GR-004**, **GR-005** |
| 7.10 | Cinematic hero assets — SC-00 opening, SC-12 gate reveal, SC-17 endings | CINEMATICS.md §12 |
| 7.11 | `bash tools/check_asset_compliance.sh` passes on release branch | ASSET_COMPLIANCE.md |
| 7.12 | **M5 visual evidence:** all zone golden screenshots per `zone_composition.json` + `ZONE_COMPOSITION_STRICT=1 bash tools/run_zone_composition_checks.sh` | GENERATION_READINESS §8, **GR-001**, **GR-003** |

**VO clip budget:** 12 clips × 3 locales (`en`, `ja`, `zh`) + 12 × 2 zh-Hant dialects (`cant`, `cmn`) = **60 OGG files**. Runtime `VoiceLinePlayer` ships in Phase 3; clip files land here in M5.

---

## Phase 8 — M6 Steam & ship prep

| # | Task |
|---|------|
| 8.1 | GodotSteam + `tools/export_windows.sh` |
| 8.2 | `bash tools/check_asset_compliance.sh` |
| 8.3 | Graphics quality presets (Low/Med/High) |
| 8.4 | Steam achievements (`AchievementManager` + `game/data/achievements/achievements.json`) | ACHIEVEMENTS.md |
| 8.5 | Steam store page + screenshots from M5 assets | steam/STORE_PAGE.md |
| 8.6 | Playtest script (`docs/qa/PLAYTEST_SCRIPT.md`) |
| 8.7 | Disable/remove GDAI MCP before export |

---

## Zone build order (environment)

1. **ruined_village** — vertical slice gate (SC-02)
2. **beach_shore** — SC-01 arrival
3. **tidal_caves** — biolume + puzzle
4. **dragon_palace_gate** — void sky + glow
5. **ending_*** — per ending doc

---

## Validation commands

```bash
python3 tools/validate_story_data.py
python3 tools/validate_acceptance_criteria.py
python3 tools/validate_audio_qa_catalog.py
python3 tools/validate_scene_audio_map.py
python3 tools/check_audio_vo.py --clip sc00_urashima_01 --locale en
python3 tools/review_vo_vision.py --clip sc00_urashima_01 --locale en
bash tools/ensure_gdai_mcp.sh
bash tools/run_unit_tests.sh
bash tools/check_dev_environment.sh
bash tools/run_playtest_smoke.sh
bash tools/run_model_smoke_checks.sh      # when gate GLBs exist
bash tools/run_visual_smoke_checks.sh     # when zone screenshots exist
bash tools/run_audio_smoke_checks.sh      # when gate BGM + VO clips exist
bash tools/generate_ai_vo.sh --list       # VO plan (dry-run: add --dry-run via python3)
bash tools/run_integration_tests.sh       # Phase 2+ gates
bash tools/run_e2e_playthrough.sh         # Phase 6 gate (not SKIP)
bash tools/check_asset_compliance.sh      # when assets exist
```

**QA policy:** `docs/qa/ACCEPTANCE_CRITERIA.md` · **On FAIL:** `tools/qa_emit_remediation.sh` per `docs/qa/QA_REMEDIATION_LOOP.md`

---

## Coverage review (gaps closed in v1.2)

This plan was audited against `TECHNICAL_DESIGN.md`, `MILESTONES.md`, and `AI_DEV_WORKFLOW.md`. The following were **missing** from earlier versions and are now scheduled:

| Gap | Where added |
|-----|-------------|
| `VoiceLinePlayer` runtime (paths + BGM duck) | Phase 3.2 |
| VO clip **generation** (ElevenLabs batch) | Phase 7.7–7.9 |
| `AudioManager` shell (procedural audio during greybox) | Phase 2.7 |
| Settings menu (language + `vo_dialect` + volumes) | Phase 2.8 |
| SC-00 prologue + `CinematicDirector` | Phase 3.7 |
| Shop + inventory UI | Phase 3.5–3.6 |
| Written `zh-Hant` in `game/data/` + `translations.csv` | Done — expand CSV for skills/combat in Phase 3 |
| SC-08 / SC-11 / SC-12 / SC-13 story beats | Phases 5.3, 6.1–6.2 |
| SFX/ambient production | Phase 7.6 |
| Steam achievements + store assets | Phase 8.4–8.5 |
| E2E three-endings gate | Phase 6.7 |
| Golden zone gameplay screenshots (`GR-001`) | Phase 1.10, 7.12 |
| `palace_sentinel` bible boss-standard row (`GR-002`) | Phase 6.3b (before Phase 7.1 enemy meshes) |
| Zone composition strict smoke (`GR-003`) | Phase 1.11 warn → Phase 7.12 strict at M5 ship |
| Audio QA catalog + hero BGM briefs (`GR-004`) | Phase 7.5, 7.9 — `audio_qa_catalog.json`, `docs/generation_briefs/audio/` |
| P0 VO generation briefs + jury (`GR-005`) | Phase 7.7–7.9 — `docs/generation_briefs/vo/`, `L2_vo_technical`, `L2_vo_jury` |
| Scene audio map (`GR-006`) | Phase 7.5–7.6 — `scene_audio_map.json` |

**Traceability:** `game/data/qa/generation_readiness_backlog.json` — machine-readable **GR-*** items linked to plan tasks and gate IDs.

**Still deferred (intentional):** full dialogue VO (12 selective clips only per `VO_HIT_LIST.md`); human L6 playtest until Phase 8 after L0–L5 pass.

---

## Deprecated

- `docs/deprecated/GDAI_REGEN_PLAN.md` — superseded by this plan (old `gdai-regen-dc91` branch deleted)
- All `*-dc91` implementation branches — deleted; do not restore old code
