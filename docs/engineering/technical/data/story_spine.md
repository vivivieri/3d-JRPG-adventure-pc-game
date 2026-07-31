---
id: story-spine
type: reference
audience: [architect, builder]
status: active
authority: engineering
tokens_est: 991
summary: "[`DATA_ARCHITECTURE.md`](../DATA_ARCHITECTURE.md)"
---
# Data architecture — Story spine

**Hub:** [`DATA_ARCHITECTURE.md`](../DATA_ARCHITECTURE.md)

## 3. Story spine (`story/scenes.json`)

One row per storyboard beat. Engine loads this for QA tools and progression validation.

| scene_id | act | zone | type | sets_flags | unlocks_zone |
|----------|-----|------|------|------------|--------------|
| SC-00 | prologue | — | cinematic | prologue_seen | — |
| SC-01 | I | beach_shore | field | tutorial_movement_done | ruined_village |
| SC-02 | I | ruined_village | explore | village_arrival_seen (inspects: SC-02-BANNER/SANDAL/WELL sub-scenes) | — |
| SC-03 | I | ruined_village | dialogue | met_yuzu_spirit | — |
| SC-04 | I | ruined_village | dialogue | met_roku, cave_entrance_unlocked | tidal_caves |
| SC-05 | I | ruined_village | combat | tutorial_combat_done | — |
| SC-06 | II | tidal_caves | field | caves_entered | — |
| SC-07 | II | tidal_caves | puzzle | water_puzzle_solved | — |
| SC-08 | II | tidal_caves | combat | deep_pool_seen | — |
| SC-09 | II | tidal_caves | boss | shore_wraith_defeated | — |
| SC-10 | II | tidal_caves | dialogue | yuzu_joined | — |
| SC-11 | II | tidal_caves | cinematic | saw_palace_vision | — |
| SC-12 | II | dragon_palace_gate | field | gate_reached, roku_combat_active | — |
| SC-13 | III | dragon_palace_gate | dialogue | knows_box_truth, mirror_choice | — |
| SC-14 | III | dragon_palace_gate | boss | sentinel_defeated | — |
| SC-15 | III | dragon_palace_gate | boss | `keeper_dialogue_done` (dialogue); `tide_keeper_phase3` (combat @ 10% HP via `on_phase_trigger`); `tide_keeper_defeated` via `sc16_last_mercy_resolution` after SC-16 | — |
| SC-16 | III | dragon_palace_gate | choice | ending_chosen | ending_* |
| SC-17a/b/c | end | ending_* | cinematic | game_completed | — |

Full table in `game/data/story/scenes.json`.

---

## 4. Flag registry (`story/flags.json`)

Central list prevents `caves_entered` vs `caves_unlocked` drift.

| flag | type | set_by | consumed_by |
|------|------|--------|-------------|
| `prologue_seen` | bool | SC-00 | skip prologue |
| `inspected_banner` | bool | SC-02-BANNER | Q1 stage 1 |
| `met_yuzu_spirit` | bool | SC-03 | Q2 start |
| `met_roku` | bool | SC-04 | Q1 complete, shop |
| `cave_entrance_unlocked` | bool | SC-04 | zone tidal_caves |
| `shore_wraith_defeated` | bool | SC-09 | Q2 complete |
| `yuzu_joined` | bool | SC-10 | party roster |
| `roku_combat_active` | bool | SC-12 | combat roster |
| `knows_box_truth` | bool | SC-13 | Q4, choice context |
| `mirror_choice` | enum | SC-13 | ending subtext flavor |
| `ending_chosen` | enum | SC-16 | rewind \| anchor \| drift |
| `game_completed` | bool | credits | gallery, continue |

---

## 5. Quest data model (5 quests = 3 acts)

| Quest | Story question | Completes |
|-------|----------------|-----------|
| `the_return` | What happened to home? | Meet Roku |
| `echoes_at_torii` | Who waits at the shrine? | Defeat Shore Wraith |
| `depths_of_guilt` | Can the dead forgive? | Reach the palace gate (`gate_reached`) |
| `palace_gate` | What was stolen? | Defeat Sentinel |
| `the_tide_answer` | What do you owe the living? | See the ending (`game_completed`) |

Stages use `completion: { "flag": "..." }` or `{ "all_flags": [...] }`.

---

## 7. Dialogue structure

One file per chapter; scenes reference story IDs.

```json
{
  "scene_id": "SC-03",
  "lines": [{ "speaker": "yuzu", "text": { "en": "...", "ja": "...", "zh": "...", "zh-Hant": "..." } }],
  "on_complete": {
    "set_flags": ["met_yuzu_spirit"],
    "start_quest": "echoes_at_torii"
  }
}
```

**Choices** (SC-13, SC-16): add `choices[]` with `set_flags` per option. SC-16 sets `"choice_confirm": true` — UI shows two-step confirm per `ENDING_DESIGN.md` §2 before applying `ending_chosen`. SC-16 choices may include `subtext` (default) and optional `subtext_warm` + `subtext_warm_requires_flags` for `mirror_choice` flavor (`ENDING_DESIGN.md` §4).

---

