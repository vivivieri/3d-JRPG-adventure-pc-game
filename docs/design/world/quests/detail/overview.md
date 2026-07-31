---
id: overview
type: reference
audience: [narrative, builder]
status: active
authority: world
tokens_est: 302
summary: "Main quests overview"
---
# Main Quests — Detail — Main quests overview

**Hub:** [`main_quests_detail.md`](../main_quests_detail.md)

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
