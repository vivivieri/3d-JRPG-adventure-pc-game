---
id: main-quests-detail
type: reference
phase: [1, 5]
audience: [narrative, builder, flow]
status: active
authority: world
tokens_est: 1012
summary: "Main quests + detail"
---
# Quests & Flags — Main quests + detail

**Hub:** [`QUEST_AND_FLAGS.md`](../QUEST_AND_FLAGS.md)

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
