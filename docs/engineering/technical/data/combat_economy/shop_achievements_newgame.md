---
id: shop-achievements-newgame
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, builder]
status: active
authority: engineering
tokens_est: 744
summary: "Shop, achievements, new game"
---
# Data — Combat & Economy — Shop, achievements, new game

**Hub:** [`combat_economy.md`](../combat_economy.md)

## 9. Shop as data (`shop/roku_shop.json`)

```json
{
  "vendor_id": "roku_shack",
  "requires_flag": "met_roku",
  "restock_on_flag": "shore_wraith_defeated",
  "inventory": [{ "item_id": "sea_salve", "price": 40, "stock": -1 }],
  "scrolls": [{ "skill_id": "returning_wave", "price": 200, "stock": 1, "character_id": "urashima", "restock": true }]
}
```

`-1` stock = infinite. `scrolls[].restock: true` = the entry appears once `restock_on_flag` is set
(post SC-09). Scrolls teach a skill early (`SKILLS_BIBLE.md` §6); greyed out if already learned.

---


## 10. Achievements (`achievements/achievements.json`)

Trigger forms used in the data (all present in `achievements.json`):

```json
{ "id": "ACH_ENDING_ANCHOR", "trigger": { "flag_equals": { "ending_chosen": "anchor" } }, "steam_api": "ENDING_ANCHOR" }
{ "id": "ACH_FIRST_STEP",    "trigger": { "flag": "game_started" },                      "steam_api": "FIRST_STEP" }
{ "id": "ACH_ALL_ENDINGS",   "trigger": { "meta_endings_count": 3 },                     "steam_api": "ALL_ENDINGS" }
{ "id": "ACH_LORE_COMPLETE", "trigger": { "lore_count": 8 },                             "steam_api": "LORE_COMPLETE" }
{ "id": "ACH_HARD_TIDE",     "trigger": { "flag": "tide_keeper_defeated", "setting": "hard_mode" }, "steam_api": "HARD_TIDE" }
```

| Trigger key | Fires when |
|-------------|-----------|
| `flag` | Bool flag set true (optionally AND `setting` true) |
| `all_flags` | Every listed bool flag true |
| `flag_equals` | Enum flag equals value |
| `meta_endings_count` | `profile_meta.endings_unlocked` size ≥ N |
| `lore_count` | `lore_read` size ≥ N |

---


## 11. New game defaults (`starting/new_game.json`)

```json
{
  "schema_version": 1,
  "start_scene": "beach_shore",
  "spawn_marker": "PlayerSpawn",
  "party_field": ["urashima"],
  "party_combat": ["urashima"],
  "level": 1,
  "inventory": { "sea_salve": 2 },
  "key_items": ["lacquer_box"],
  "equipment": { "urashima": { "weapon": "fisher_katana", "armor": "worn_haori", "charm": null } },
  "gold": 0,
  "flags": {},
  "quests_active": ["the_return"],
  "play_prologue": true
}
```

**Field notes:**
- `start_scene` holds a **zone id** (`beach_shore`), *not* a `SC-*` scene id. It is the first playable **zone** loaded after the optional prologue. (Consider renaming to `start_zone` in a future schema bump for clarity.)
- Load order when `play_prologue: true`: **SC-00 prologue cinematic → load `beach_shore` zone → SC-01** begins there. When `play_prologue: false` (replay with `prologue_seen`), skip straight to the `beach_shore` load.
- `party_field` = follower/overworld roster; `party_combat` = battle roster (they diverge as Yuzu/Roku join).

---
