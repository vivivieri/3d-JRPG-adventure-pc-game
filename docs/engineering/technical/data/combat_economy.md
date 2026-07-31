---
id: combat-economy
type: reference
audience: [architect, builder]
status: active
authority: engineering
tokens_est: 1674
summary: "Hand-placed fights only — no random tables."
---
# Data architecture — Combat & economy

**Hub:** [`DATA_ARCHITECTURE.md`](../DATA_ARCHITECTURE.md)

## 6. Encounter data (`encounters/story_encounters.json`)

Hand-placed fights only — no random tables.

```json
{
  "id": "enc_sc05_tutorial_crab",
  "scene_id": "SC-05",
  "zone": "ruined_village",
  "trigger": "TutorialEncounter",
  "enemies": ["salt_crab"],
  "party": ["urashima"],
  "tutorial": true,
  "on_win": { "set_flags": ["tutorial_combat_done"], "grant_items": [] }
}
```

Maps 1:1 to `ENCOUNTER_TABLE.md`. Optional fields: `optional: true`, `boss: true`,
`escape_allowed: false`, `requires_flags: [...]`, `cinematic_hook`, and
`on_phase_trigger: { "set_flags": [...] }` (fires when an enemy's `phases[].triggers_choice`
threshold is hit mid-combat — used by the Tide Keeper choice gate).

**Persistence / re-entry contract:** every encounter ID is appended to the save's
`encounters_completed[]` on **win**. Completed triggers never re-fire (on backtrack, reload, or
zone re-entry). On **escape or defeat** the trigger stays armed. This prevents both retrigger
loops and XP/coin farming.

---

## 8. Items tied to story beats

| Story beat | Item data |
|------------|-----------|
| SC-01 / start | `lacquer_box`, `fisher_katana`, `worn_haori`, 2× `sea_salve` |
| SC-04 | `cave_map` (key) |
| SC-07 chest | `tide_cut_saber` |
| SC-09 boss | `wraith_pearl` (key) |
| SC-14 boss | `palace_edge` |
| Lore read | `spirit_bell` — `items.json` `story_grant: "sailor_charm"` (granted when the `sailor_charm` lore entry is read; matches `lore_entries.json` id) |

### Reward ownership rule (avoid double-grants)

Several story items may be **documented** in multiple files (enemy `drops`, quest `rewards.items`, item `story_grant` trace the story beat), but **exactly one path grants** the item at runtime:

- **Combat/story key items:** the encounter `on_win.grant_items` is the single source that actually adds the item to inventory.
- Enemy `drops`, quest `rewards.items`, and item `story_grant` for the *same* item are **descriptive only** (UI/economy documentation) and must be no-ops at runtime, or de-duplicated by item id on grant.
- Quest `rewards` should otherwise grant only XP/gold (distinct from the combat drop).

The runtime grant code and `validate_story_data.py` should enforce single-grant-per-item-id.

---

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

## 18. `combat_barks` on enemy entries

Boss/elite enemies may define inline combat bark copy in `enemies/enemies.json` (v1 bosses: `shore_wraith`, `palace_sentinel`, `tide_keeper`; field mobs: `salt_crab`, `tide_wraith`). Intent UI shows one bark per telegraphed action; defeat lines are tragic, not celebratory (`BOSS_DESIGNS.md` §1, `NARRATIVE_WRITING_GUIDE.md` §12). Field mobs may omit `battle_start` (tutorial clarity).

```json
"combat_barks": {
  "battle_start": { "en": "...", "ja": "...", "zh": "...", "zh-Hant": "..." },
  "on_defeat": { "en": "...", "ja": "...", "zh": "...", "zh-Hant": "..." },
  "skills": {
    "drown_touch": { "en": "...", "ja": "...", "zh": "...", "zh-Hant": "..." }
  },
  "phases": [
    { "hp_threshold": 0.5, "text": { "en": "...", "ja": "...", "zh": "...", "zh-Hant": "..." } }
  ]
}
```

| Field | Rule |
|-------|------|
| `skills` keys | Must exist in the enemy's `skills[]` array |
| `phases[].hp_threshold` | Should match a `phases[].hp_threshold` on the same enemy when phases exist |
| Locales | `en` / `ja` / `zh` / `zh-Hant` required on every text object |

**Runtime (Phase 3+):** `CombatManager` reads barks by `skill_id` when intent telegraphs; `on_defeat` plays before encounter `on_win` rewards. Data-only until combat UI wires.

### Ending gallery copy

`game/data/narrative/ending_gallery.json` — three ending slots with `philosophy_blurb` per `REPLAY_DESIGN.md` §4. No "recommended" badge. `ending_chosen` values must match `flags.json`.
