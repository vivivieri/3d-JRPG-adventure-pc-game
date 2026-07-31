---
id: phase-2-3
type: reference
audience: [pm, qa, architect]
status: active
authority: workflow
tokens_est: 583
summary: "AI Dev — Phases 0–3 — Phases 2–3"
---
# AI Dev — Phases 0–3 — Phases 2–3

**Hub:** [`part_a.md`](../part_a.md)

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
