# Tides of Urashima — Story-Driven Data Architecture

**Version:** 1.0  
**Principle:** Data follows the story spine — scenes drive flags, flags drive quests, quests drive encounters and rewards.  
**Runtime wiring:** `docs/TECHNICAL_DESIGN.md` · **Zone placement:** `docs/LEVEL_DESIGN.md`

**Cross-refs:** `docs/STORYBOARD.md`, `docs/QUEST_AND_FLAGS.md`, `game/data/README.md`

---

## 1. Why story-first data?

This is a **2–3 hour linear narrative JRPG**. The database should mirror the player's journey:

```
SC-00 … SC-17  →  story/scenes.json   (spine)
       ↓
   set_flags     →  story/flags.json    (truth table)
       ↓
   quests        →  quests/main_quests.json
       ↓
dialogue / fights →  dialogue/*.json + encounters/story_encounters.json
       ↓
   rewards       →  items.json + shop/roku_shop.json + enemies.json drops
```

**Rule:** Every flag must trace to a `scene_id`. Every quest stage must trace to a flag. No orphan data.

---

## 2. Recommended file layout

```
game/data/
  README.md
  story/
    scenes.json              # Master scene index (SC-00 … SC-17c)
    flags.json               # All story flags + who sets them
  dialogue/
    chapter_01.json          # All dialogue lines by scene_id
    prologue.json            # Optional: SC-00 only (or keep in chapter_01)
  quests/
    main_quests.json         # 5 quests aligned to acts
  encounters/
    story_encounters.json    # Scripted fights tied to scenes
  characters/
    party.json
  enemies/
    enemies.json
  skills/
    skills.json
  items/
    items.json
  shop/
    roku_shop.json
  lore/
    lore_entries.json
    lore_placements.json
  achievements/
    achievements.json
  starting/
    new_game.json            # Starting inventory, level, flags
```

**Not in DB:** 3D transforms for lore (keep `lore_placements.json`), zone geometry (Godot scenes).

---

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
| SC-15 | III | dragon_palace_gate | boss | tide_keeper_defeated (on win); tide_keeper_phase3 (combat @ 10% HP via `on_phase_trigger`) | — |
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

**Choices** (SC-13, SC-16): add `choices[]` with `set_flags` per option. SC-16 sets `"choice_confirm": true` — UI shows two-step confirm per `ENDING_DESIGN.md` §2 before applying `ending_chosen`.

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

## 12. Localization split

| Content | Where |
|---------|-------|
| Dialogue lines | `dialogue/*.json` inline `{ en, ja, zh, zh-Hant }` |
| UI, tutorials, combat log, skill/enemy names | `game/locale/translations.csv` (core keys ship; expand in Phase 3) |
| Quest / item / lore display text | JSON inline `display_name` / `title` objects — **JSON is authoritative**; CSV mirrors optional |

---

## 13. Validation tools (implemented)

```bash
python3 tools/validate_story_data.py   # L0 gate — run after every data edit
```

Checks (see the script for the authoritative list):
- Every dialogue/scene/hook reference resolves (scenes, dialogue blocks, cinematic hooks, VO clips)
- Every `set_flags` / `requires_flags` (incl. dialogue choices) exists in `flags.json`
- Quest stage completion flags exist in the registry
- Encounter `scene_id` / `enemies` / `grant_items` / `on_phase_trigger` flags resolve
- Enemy `skills` and drop `item_id`s exist; party skills/unlocks/limits exist
- Shop inventory items and scroll `skill_id`s exist

---

## 14. Migration from old 3-quest data

| Old | New |
|-----|-----|
| 3 quests | 5 quests (split palace + ending) |
| `caves_unlocked` | `caves_entered` + `cave_entrance_unlocked` |
| 10 items | 20 items (equipment + keys) |
| 15 dialogue scenes | 22+ (add SC-00, 05, 09, 16, 17*) |

---

## 15. File maintenance order (all files already exist)

All spine files below are already present in `game/data/`. This is the dependency order to keep in mind when editing — change upstream files before downstream references:

1. `story/scenes.json` + `story/flags.json` — spine
2. `quests/main_quests.json` — 5 quests
3. `items/items.json` + `starting/new_game.json`
4. `encounters/story_encounters.json`
5. `dialogue/chapter_01.json`
6. `shop/roku_shop.json` + `achievements/achievements.json`
7. Re-run `python3 tools/validate_story_data.py` after any edit

---

## 16. Scene index vs storyboard count

| Source | Count | Notes |
|--------|-------|-------|
| `docs/STORYBOARD.md` | **19** narrative beats | SC-00 + 18 main-path scenes |
| `story/scenes.json` | **23** rows | Adds SC-02 inspectable sub-scenes + SC-17a/b/c ending variants |
| `dialogue/chapter_01.json` | **22** scene keys | SC-07 silent puzzle — no dialogue block by design |

All `scene_id` values in dialogue, encounters, and flags must exist in `scenes.json`.

---

## 17. JSON schema versions

Files use `schema_version` (integer) or `version` (string) to track format evolution. The validator checks content, not version numbers.

| File | Key | Current | Notes |
|------|-----|---------|-------|
| `dialogue/chapter_01.json` | `schema_version` | **4** | Adds `voice_id` on selective VO lines |
| `quests/main_quests.json`, `items/items.json` | `schema_version` | **2** | — |
| Most other `game/data/**/*.json` | `schema_version` | **1** | — |
| `audio/vo_prompts.json`, `ace_step_prompts.json` | `version` | **"1.0"** | Audio catalog metadata (not gameplay schema) |

Bump `schema_version` when breaking field renames; run `python3 tools/validate_story_data.py` after edits.

**Dialogue layout:** `chapter_01.json` holds all scenes including SC-00. Optional `dialogue/prologue.json` split is documented but **not used** in this repo.
