---
id: quest-detail
type: reference
audience: [narrative, builder]
status: active
authority: world
tokens_est: 779
summary: "*Explore the ruined village and learn what became of home.*"
---
# Main Quests — Detail — Per-quest detail

**Hub:** [`main_quests_detail.md`](../main_quests_detail.md)

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
