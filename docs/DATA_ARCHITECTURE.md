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
   rewards       →  items.json + shop.json + enemies.json drops
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
| SC-02 | I | ruined_village | explore | inspected_* | — |
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
| SC-13 | III | dragon_palace_gate | dialogue | knows_box_truth *(`mirror_choice` is registered in `flags.json` but not yet set by any `scenes.json`/dialogue row — SC-13 needs a choice block to set it; see `docs/ENDING_DESIGN.md`)* | — |
| SC-14 | III | dragon_palace_gate | boss | sentinel_defeated | — |
| SC-15 | III | dragon_palace_gate | boss | tide_keeper_defeated, tide_keeper_phase3 *(both currently set together in `encounters/story_encounters.json` `on_win`, i.e. after the fight ends — see the open question in `docs/BOSS_DESIGNS.md` §4 about wiring the mid-fight 10%-HP choice gate)* | — |
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
| `depths_of_guilt` | Can the dead forgive? | Yuzu joins + palace vision |
| `palace_gate` | What was stolen? | Defeat Sentinel |
| `the_tide_answer` | What do you owe the living? | Choose ending |

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
  "on_win": { "set_flags": ["tutorial_combat_done"] }
}
```

Maps 1:1 to `ENCOUNTER_TABLE.md`.

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

**Choices** (SC-13, SC-16): add `choices[]` with `set_flags` per option.

---

## 8. Items tied to story beats

| Story beat | Item data |
|------------|-----------|
| SC-01 / start | `lacquer_box`, `fisher_katana`, `worn_haori`, 2× `sea_salve` |
| SC-04 | `cave_map` (key) |
| SC-07 chest | `tide_cut_saber` |
| SC-09 boss | `wraith_pearl` (key) |
| SC-14 boss | `palace_edge` |
| SC-06 lore | `spirit_bell` via `sailor_charm` lore → grant on read (optional) |

---

## 9. Shop as data (`shop/roku_shop.json`)

```json
{
  "vendor_id": "roku_shack",
  "requires_flag": "met_roku",
  "restock_on_flag": "shore_wraith_defeated",
  "inventory": [{ "item_id": "sea_salve", "price": 40, "stock": -1 }],
  "scrolls": [{ "skill_id": "purify", "price": 200, "stock": 1, "character_id": "yuzu", "restock": true }]
}
```

`-1` stock = infinite.

---

## 10. Achievements (`achievements/achievements.json`)

```json
{
  "id": "ACH_ENDING_ANCHOR",
  "steam_api": "ENDING_ANCHOR",
  "trigger": { "flag_equals": { "ending_chosen": "anchor" } },
  "hidden": false
}
```

Trigger shapes actually in use: `{ "flag": "..." }`, `{ "flag_equals": { "<flag>": "<value>" } }`, `{ "all_flags": [...] }`, `{ "lore_count": N }`, `{ "meta_endings_count": N }`, and `{ "flag": "...", "setting": "hard_mode" }` for hard-mode-gated achievements.

---

## 11. New game defaults (`starting/new_game.json`)

```json
{
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

Note the split between `party_field` (who's visible/walking around) and `party_combat` (who's in the active battle roster) — they may diverge once Yuzu/Roku join.

---

## 12. Localization split

| Content | Where |
|---------|-------|
| Dialogue lines | `dialogue/*.json` inline `{ en, ja, zh, zh-Hant }` |
| UI, tutorials | `game/locale/translations.csv` |
| Quest titles | JSON inline OR CSV `quest.{id}.title` |
| Item names | JSON `display_name` + CSV mirror optional |

---

## 13. Validation tools (recommended)

```bash
# Future: validate story data integrity
python3 tools/validate_story_data.py
```

Checks actually implemented in `tools/validate_story_data.py` today:
- `scenes.json` → dialogue/item/flag/cinematic-hook references resolve
- Dialogue `on_complete.set_flags` + line `requires_flags` resolve to `flags.json`
- Every `voice_id` in dialogue exists in `vo_prompts.json` (and vice versa — no orphan clips)
- Cinematic hooks: `scene_id`, `sets_flags`, `skip_if_flag`, `requires_flags`, `requires_items`, and `then` dialogue/encounter references resolve
- Encounters: `scene_id`, `enemies`, `on_win.grant_items`, `cinematic_hook`, `requires_flags` resolve
- Quest count == 5
- Shop `inventory[].item_id` resolves to `items.json`
- `items.json` `story_grant` resolves to `"new_game"`, a real `scene_id`, or a real `lore_entries.json` id (added during the pre-Phase-1 doc audit — this caught a real bug: `spirit_bell.story_grant` pointed at `lore_sailor_charm`, which didn't exist; fixed to `sailor_charm`)

**Not yet implemented** (do not rely on these until added — see `docs/AI_DEV_WORKFLOW.md` L0 gate):
- Cross-check against `docs/STORYBOARD.md` scene headings (the validator never parses Markdown)
- "Every quest `completion.flag` is set somewhere" (quest stage `completion` fields are not read at all)

---

## 14. Migration from old 3-quest data

| Old | New |
|-----|-----|
| 3 quests | 5 quests (split palace + ending) |
| `caves_unlocked` | `caves_entered` + `cave_entrance_unlocked` |
| 10 items | 20 items (equipment + keys) |
| 15 dialogue scenes | 22+ (add SC-00, 05, 09, 16, 17*) |

---

## 15. Priority implementation order

1. `story/scenes.json` + `story/flags.json` — spine
2. `quests/main_quests.json` — 5 quests
3. `items/items.json` + `starting/new_game.json`
4. `encounters/story_encounters.json`
5. `dialogue/chapter_01.json` — fill missing scenes
6. `shop/roku_shop.json` + `achievements/achievements.json`
7. `tools/validate_story_data.py`

---

## 16. Scene index vs storyboard count

| Source | Count | Notes |
|--------|-------|-------|
| `docs/STORYBOARD.md` | **20** scene headings | SC-00 + SC-01–16 + 3 ending variants (SC-17a/b/c); a single playthrough experiences 18 (one ending only) |
| `story/scenes.json` | **23** rows | The 20 headings + 3 SC-02 inspectable sub-scenes |
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
