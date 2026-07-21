# Tides of Urashima — Quest & Story Flag Map

**Version:** 1.0 (Pre-build)
**Cross-refs:** `docs/vision/STORYBOARD.md`, `docs/vision/GDD.md`, `game/data/quests/main_quests.json`

---

## 1. Main quests (5)

| # | Quest ID | Title | Act | Complete when (final stage flag) |
|---|----------|-------|-----|----------------------------------|
| 1 | `the_return` | The Return | I | `met_roku` |
| 2 | `echoes_at_torii` | Echoes at the Torii | I–II | `shore_wraith_defeated` |
| 3 | `depths_of_guilt` | Depths of Guilt | II | `gate_reached` |
| 4 | `palace_gate` | The Palace Gate | III | `sentinel_defeated` |
| 5 | `the_tide_answer` | The Tide's Answer | III | `game_completed` |

**Rule:** a quest is complete when its **last stage's** completion flag is set (`main_quests.json` stages are ordered).

**Activation:** `start_quest` in dialogue `on_complete` (Q1–Q2, Q4) or `QuestManager` auto-start when the player **enters** the `start_scene` zone after that scene's dialogue completes (Q3 `SC-09`, Q5 `SC-14`). `start_scene` values are **scene IDs** (`SC-*`), not zone ids — distinct from `new_game.json` `start_scene: beach_shore`.

---

## 2. Quest detail

### Q1 — The Return (`the_return`)

**Unlock:** Game start (SC-01)
**Log text:** *Explore the ruined village and learn what became of home.*

| Stage | ID | Objective | Completion flag |
|-------|-----|-----------|-----------------|
| 1 | `explore_village` | Investigate banner, sandal, and well | `inspected_banner` AND `inspected_sandal` AND `inspected_well` |
| 2 | `meet_roku` | Speak with Roku at his shack | `met_roku` |

**Rewards:** 30 XP
**Unblocks:** Cave entrance (`cave_entrance_unlocked` set in SC-04)

---

### Q2 — Echoes at the Torii (`echoes_at_torii`)

**Unlock:** SC-03 (`met_yuzu_spirit`)
**Log text:** *Follow the spirit's voice into the Tidal Caves.*

| Stage | ID | Objective | Completion flag |
|-------|-----|-----------|-----------------|
| 1 | `investigate_shrine` | Hear Yuzu at the cracked torii | `met_yuzu_spirit` |
| 2 | `enter_caves` | Enter Tidal Caves | `caves_entered` |
| 3 | `solve_tide_lock` | Raise/lower water to reach the latch | `water_puzzle_solved` |
| 4 | `defeat_shore_wraith` | Confront the Shore Wraith | `shore_wraith_defeated` |

**Rewards:** 100 XP, 50 shell coins, `wraith_pearl` (key item)

---

### Q3 — Depths of Guilt (`depths_of_guilt`)

**Unlock:** SC-09 complete
**Log text:** *Yuzu joins the journey. Learn what the palace took.*

| Stage | ID | Objective | Completion flag |
|-------|-----|-----------|-----------------|
| 1 | `yuzu_joins` | Accept Yuzu at the shrine alcove | `yuzu_joined` |
| 2 | `palace_vision` | Witness Otohime's flashback | `saw_palace_vision` |
| 3 | `reach_gate` | Arrive at Dragon Palace Gate | `gate_reached` |

**Rewards:** 50 XP
**Party:** Yuzu playable in combat from `yuzu_joined` onward

---

### Q4 — The Palace Gate (`palace_gate`)

**Unlock:** SC-12 (`gate_reached`)
**Log text:** *Enter the stolen-time palace and face its guardian.*

| Stage | ID | Objective | Completion flag |
|-------|-----|-----------|-----------------|
| 1 | `learn_box_truth` | Hear Roku in the mirror chamber | `knows_box_truth` |
| 2 | `defeat_sentinel` | Defeat Palace Sentinel | `sentinel_defeated` |

**Rewards:** 100 XP; `palace_edge` granted by `enc_sc14_sentinel` on win (not quest JSON)
**Blocker:** `wraith_pearl` required to open gate interior (dropped by Shore Wraith at SC-09)

---

### Q5 — The Tide's Answer (`the_tide_answer`)

**Unlock:** SC-14 complete
**Log text:** *Face the Tide Keeper and decide the village's fate.*

| Stage | ID | Objective | Completion flag |
|-------|-----|-----------|-----------------|
| 1 | `face_keeper` | Reach Tide Keeper phase 3 (10% HP) | `tide_keeper_phase3` |
| 2 | `make_choice` | Select Rewind, Anchor, or Drift | `ending_chosen` |
| 3 | `see_ending` | Watch ending cinematic + credits | `game_completed` |

**Rewards:** 250 XP (from boss); ending-specific achievement

---

## 3. Master story flag list

| Flag | Set by | Used for |
|------|--------|----------|
| `prologue_seen` | SC-00 | Skip prologue on replay |
| `tutorial_movement_done` | SC-01 | Hide movement prompts |
| `inspected_banner` | SC-02 inspect | Q1 stage 1 |
| `inspected_sandal` | SC-02 inspect | Q1 stage 1 |
| `inspected_well` | SC-02 inspect / save | Q1 stage 1 |
| `met_yuzu_spirit` | SC-03 | Q2 unlock |
| `met_roku` | SC-04 | Q1 complete; shop open |
| `cave_entrance_unlocked` | SC-04 | Cave zone transition |
| `tutorial_combat_done` | SC-05 | Hide combat prompts |
| `caves_entered` | SC-06 | Q2 stage 2 |
| `water_puzzle_solved` | SC-07 | Deep pool access |
| `deep_pool_vignette_seen` | sc08_deep_pool_vignette | Skip SC-08 vignette on replay |
| `deep_pool_dialogue_done` | SC-08 dialogue | Gates `enc_sc08_deep_pool` |
| `deep_pool_seen` | SC-08 encounter win | Lore / mood |
| `shore_wraith_defeated` | SC-09 | Q2 complete; cave exit |
| `yuzu_joined` | SC-10 | Yuzu in party |
| `saw_palace_vision` | SC-11 | Q3 stage 2 |
| `sc12_gate_reveal_seen` | sc12_gate_reveal | Skip SC-12 gate movie on replay |
| `gate_reached` | SC-12 dialogue | Q3 complete; Q4 unlock |
| `roku_combat_active` | SC-12 dialogue | Roku in combat roster |
| `knows_box_truth` | SC-13 | Q4 stage 1; choice context |
| `mirror_choice` | SC-13 dialogue choice | `open` \| `break` \| `unknown` — SC-16 subtext flavor (ENDING_DESIGN.md §4) |
| `sentinel_defeated` | SC-14 | Q4 complete |
| `tide_keeper_phase3` | SC-15 combat @ 10% HP (`triggers_choice` phase → `on_phase_trigger`) | Choice gate; Q5 stage 1 |
| `ending_chosen` | SC-16 | `rewind` \| `anchor` \| `drift` |
| `game_completed` | Credits end | Continue → title; achievements |

---

## 4. Zone blockers

| Zone | Entry requirement | Exit requirement |
|------|-------------------|------------------|
| `beach_shore` | New game | Walk to village gate |
| `ruined_village` | SC-01 | — |
| `tidal_caves` | `cave_entrance_unlocked` | `shore_wraith_defeated` (boss door) |
| `dragon_palace_gate` | `wraith_pearl` (key item) + `yuzu_joined` | `ending_chosen` |
| `ending_*` | `ending_chosen` matching value | Credits → title |

**Backtracking:** Allowed after Shore Wraith. Hub shop restocks after SC-09.

---

## 5. Party join flags

| Character | Join flag | Combat active | Field visible | Scene |
|-----------|-----------|---------------|---------------|-------|
| Urashima | always | SC-01+ | always | — |
| Roku | `met_roku` (narrative) | `roku_combat_active` — **SC-12+** only | SC-04 shack; SC-12+ follower | SC-04 meet; joins party at SC-12 |
| Yuzu | `yuzu_joined` | SC-10+ | SC-10+ follower | SC-10 |

**Design rule:** Roku is **not** playable before SC-12. In SC-05 he provides bark lines only.
Full 3-party combat from SC-12 onward.

**Clarification:** `met_roku` (SC-04) = narrative met / shop open. `roku_combat_active` (SC-12
dialogue) = Roku enters the combat roster. There is **no** `roku_in_party` flag — the two flags
above are the only Roku state.

---

## 6. Quest UI behavior

- **New quest:** Banner top-right, 3s fade; log sound
- **Stage complete:** Checkmark on quest tracker; brief pulse
- **Quest complete:** Fanfare (short); XP/coins if scripted
- **Tracker:** Tab menu → Quests tab; shows active stage only (no spoilers)

---

## 7. Implementation JSON

`game/data/quests/main_quests.json` already contains all 5 quests with stages matching the
tables above (schema v2). When editing quests, change the JSON first, then this doc.

---

## 8. QA checklist

- [ ] Cannot enter caves before SC-04
- [ ] Cannot pass Shore Wraith arena without win or game over
- [ ] Cannot open palace interior without `wraith_pearl`
- [ ] Yuzu not in SC-09 combat roster
- [ ] Roku not in SC-05–SC-11 combat roster
- [ ] All 5 quests complete across one full playthrough
- [ ] Quest log never references unseen characters by name
