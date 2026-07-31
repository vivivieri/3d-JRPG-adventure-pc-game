---
id: flags-blockers-party
type: reference
phase: [1, 5]
audience: [narrative, builder, flow]
status: active
authority: world
tokens_est: 879
summary: "Quests & Flags — Flag list, zone blockers, party join — Backtracking: Allowed after Shore Wraith. Hub shop restocks after SC-09."
---
# Quests & Flags — Flag list, zone blockers, party join

**Hub:** [`QUEST_AND_FLAGS.md`](../QUEST_AND_FLAGS.md)

## When to read

Use **Quests & Flags — Flag list, zone blockers, party join** (roles: narrative, builder, flow) when you need this reference during the current task Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [3. Master story flag list](#3-master-story-flag-list)
- [4. Zone blockers](#4-zone-blockers)
- [5. Party join flags](#5-party-join-flags)


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
