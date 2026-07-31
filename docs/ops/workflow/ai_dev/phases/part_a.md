---
id: part-a
type: reference
phase: [0, 1, 8]
audience: [pm, qa, architect]
status: active
authority: workflow
tokens_est: 1088
summary: "AI Dev — Phase Acceptance (A)"
---
# AI Dev — Phase Acceptance — AI Dev — Phase Acceptance (A)

**Hub:** [`phase_acceptance.md`](../phase_acceptance.md)

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
