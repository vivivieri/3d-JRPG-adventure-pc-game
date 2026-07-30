---
id: phase-acceptance
type: how-to
audience: [pm, architect]
status: active
authority: workflow
tokens_est: 2048
---
# AI Dev Workflow — phase acceptance

**Hub:** [`AI_DEV_WORKFLOW.md`](../AI_DEV_WORKFLOW.md)

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

**Task numbers match `docs/ops/workflow/IMPLEMENTATION_PLAN.md` §Phase 1** (not a separate numbering scheme).

| # | Criterion | Verification |
|---|-----------|--------------|
| 1.1 | `environments/*.tres` — WorldEnvironment per zone (tonemap, fog, glow) | GDAI + `RENDERING_GUIDE.md` |
| 1.2 | `zone_visuals.gd` applies palette, sky, lights at runtime | Unit test + GDAI F5 |
| 1.3 | `toon_base.gdshader` on ground meshes; single ramp family | GDAI viewport |
| 1.4 | `water_stylized.gdshader` — foam + gentle displacement | Shader compiles headless |
| 1.5 | Greybox zone scenes (Sprint1: `ruined_village`; Sprint2: beach/caves/palace) | Integration / headless load |
| 1.6 | DirectionalLight + fog values match zone table | GDAI inspector readback |
| 1.7 | ProceduralSky (no HDRI) per `RENDERING_GUIDE.md` §4 | GDAI viewport |
| 1.8 | Component scenes from `LEVEL_DESIGN.md` §1b (Phase1-Sprint2) | GDAI `.tscn` + L3 |
| 1.9 | **Vertical slice gate:** SC-02 Ruined Village passes `ART_DIRECTION.md` §10 greybox checklist | GDAI F5 + L3 |
| 1.10 | **Golden screenshot** — `phase1_ruined_village_gameplay.png` (**GR-001**) | GDAI capture |
| 1.11 | Zone composition smoke (warn) — `run_zone_composition_checks.sh` (**GR-003**) | Exit 0 warn until M5 strict |
| — | L0 + L1 + L2 + L3 pass after every commit on `game/development` | `bash tools/run_ci_checks.sh` |

### Phase 2 — Core systems shell

| # | Criterion | Verification |
|---|-----------|--------------|
| 2.1 | Autoloads: `GameManager`, `EventBus`, `SaveSystem`, `DialogueRunner`, `CombatManager` | Project settings + unit tests |
| 2.2 | `GameManager.load_json("res://data/...")` works for all data types | Unit test |
| 2.3 | `LocalizationManager` + `FontThemeManager`; en / ja / zh / zh-Hant fonts | GDAI F5 language switch |
| 2.4 | Main menu → New Game → SC-00 prologue → `beach_shore` without errors | GDAI F5 + integration test |
| 2.5 | Player WASD + camera orbit per `GAME_FEEL.md` | GDAI F5 |
| 2.6 | Zone transitions per `WORLD_MAP_AND_FLOW.md` | Integration `test_zone_transitions.gd` |
| 2.7 | `AudioManager` plays zone BGM; SFX on Voice/Music buses | GDAI F5 |
| 2.8 | Settings menu: language, `vo_dialect` (when zh-Hant), volumes persist | GDAI F5 + unit test |
| 2.9 | SaveSystem round-trip: save (well SavePoint in greybox village, or direct API call) → reload → flags persist | Unit + integration |
| 2.10 | L0–L4 pass | All test scripts |

### Phase 3 — Narrative & exploration

| # | Criterion | Verification |
|---|-----------|--------------|
| 3.1 | Dialogue box shows speaker + body from `chapter_01.json` | GDAI F5 SC-03 |
| 3.2 | `VoiceLinePlayer` resolves path for `voice_id`; ducks BGM −6 dB (SC-16: −18 dB); no crash if clip missing | GDAI F5 SC-03; unit test path resolver |
| 3.3 | Interactable prompt (E) per `UI_UX_FLOW.md` | GDAI F5 |
| 3.4 | Quest stages advance per `main_quests.json` | Unit `test_flag_system.gd` |
| 3.5 | Tab inventory + Roku shop prices match `roku_shop.json` | Unit + GDAI F5 |
| 3.6 | SC-00 prologue plays; `prologue_seen` flag set | Integration test |
| 3.7 | SC-01 through SC-05 reachable without soft-lock | Integration test |
| 3.8 | 8 lore entries discoverable per `lore_placements.json` (greybox zones from Phase 1 are sufficient) | Integration test |
| 3.9 | All four written locales render (en / ja / zh / zh-Hant); no raw keys on main path | GDAI F5 + FLOW QA + `validate_story_data.py` |
| 3.10 | L0–L4 pass | All test scripts |

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
| 5.1 | `tidal_caves.tscn` lighting/palette pass per `ENVIRONMENT_KITS.md` §5 (greybox meshes OK — final art is Phase 7) | GDAI screenshot |
| 5.2 | SC-07 water puzzle: silent, no VO; state machine matches `PUZZLE_DESIGN.md` | Unit + GDAI F5 |
| 5.3 | Shore Wraith SC-09 win/lose paths | Integration test |
| 5.4 | Yuzu joins at SC-10; party size = 2 | Flag unit test |
| 5.5 | SC-08 vignette plays; whisper SFX bed, no full VO | GDAI F5 |
| 5.6 | L0–L4 pass | All test scripts |

### Phase 6 — Full story & endings

| # | Criterion | Verification |
|---|-----------|--------------|
| 6.0 | Expand `palace_sentinel` `CHARACTER_BIBLE.md` to boss-standard row **before** SC-14 mesh work (**GR-002**) | Doc review; backlog `status: done` |
| 6.1 | Dragon Palace Gate zone per `ENVIRONMENT_KITS.md` §6 | GDAI + screenshot |
| 6.2 | Palace Sentinel + Tide Keeper per `BOSS_DESIGNS.md` | Integration test |
| 6.3 | SC-16 choice UI blocks attack input per `ENDING_DESIGN.md` | GDAI F5 |
| 6.4 | All 3 endings reachable: Rewind, Anchor, Drift | E2E `test_three_endings.gd` |
| 6.5 | Credits roll after each ending | E2E test |
| 6.6 | SC-12 gate cinematic + SC-11 flashback skippable after 3s | GDAI F5 |
| 6.7 | `bash tools/run_e2e_playthrough.sh` passes | Exit 0 |
| 6.8 | L0–L5 pass | All test scripts |

### Phase 7 — M5 art rebuild

| # | Criterion | Verification |
|---|-----------|--------------|
| 7.1 | No primitive/Kenney placeholder art in shipping scenes | `check_asset_compliance.sh` + human review |
| 7.2 | Hero meshes: Urashima, Yuzu, Roku per `CHARACTER_BIBLE.md` | Screenshot gate |
| 7.3 | Automated stylized zone textures per zone (`palette_remap.py`) | Art checklist |
| 7.4 | Curated BGM per `audio_qa_catalog.json` + `AUDIO_PRODUCTION_GUIDE.md` | `L2_audio_technical` + `L2_audio_jury` |
| 7.5 | SFX + ambient beds per `scene_audio_map.json` | `validate_scene_audio_map.py` + in-game verify |
| 7.6 | Selective VO: 12 clips × locales + zh-Hant dialects; `generate_ai_vo.sh --list` = 60 files | File manifest + `run_audio_smoke_checks.sh` |
| 7.7 | P0 VO: `L2_vo_technical` all locales + `L2_vo_jury` on `en` gate | `check_audio_vo.py` + `review_vo_vision.py` |
| 7.8 | Cinematic hero assets (SC-00, SC-12, SC-17) per `CINEMATICS.md` §12 | GDAI F5 |
| 7.9 | `bash tools/check_asset_compliance.sh` passes | Exit 0 |
| 7.12 | All zone golden screenshots + `ZONE_COMPOSITION_STRICT=1` composition smoke (**GR-001**, **GR-003**) | `run_visual_smoke_checks.sh` + `run_zone_composition_checks.sh` |

### Phase 8 — Ship prep

**Order:** L0–L5 on release candidate → **then** L6 human QA → export.

| # | Criterion | Verification |
|---|-----------|--------------|
| 8.1 | GDAI MCP plugin **disabled and removed** from export tree | Manual + export preset review |
| 8.2 | Windows export succeeds (`tools/export_windows.sh`) | Artifact exists |
| 8.3 | `bash tools/check_asset_compliance.sh` passes | Exit 0 |
| 8.4 | Steam achievements unlock per `ACHIEVEMENTS.md` | Integration test |
| 8.5 | **L0–L5 pass** on release candidate | All AI test scripts exit 0 |
| 8.6 | **Human QA** `docs/ops/qa/PLAYTEST_SCRIPT.md` ≥80% complete without guide | Human sign-off **after 8.5** |

---

