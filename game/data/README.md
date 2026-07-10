# Data Schema — Tides of Urashima

**Story-driven JSON database.** Read `docs/DATA_ARCHITECTURE.md` for design rationale.

## File layout

```
game/data/
  story/
    scenes.json              # Master scene spine (SC-00 … SC-17c)
    flags.json               # Canonical flag registry
  dialogue/
    chapter_01.json          # Dialogue by scene_id (en / ja / zh)
  quests/
    main_quests.json         # 5 main quests
  encounters/
    story_encounters.json    # Scripted fights per scene
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
    new_game.json
```

## Load API

```gdscript
GameManager.load_json("res://data/story/scenes.json")
```

## Validation

```bash
python3 tools/validate_story_data.py
python3 tools/check_asset_compliance.sh   # when assets exist
```

## Story → data flow

1. **Scene plays** (`story/scenes.json` row)
2. **Dialogue / encounter** fires (`dialogue/`, `encounters/`)
3. **Flags set** (`story/flags.json` names)
4. **Quest stages** advance (`quests/main_quests.json`)
5. **Items granted** (`items.json`)

## Key conventions

| Convention | Example |
|------------|---------|
| Scene IDs | `SC-00` … `SC-17c` match `STORYBOARD.md` |
| Flags | snake_case; defined only in `story/flags.json` |
| Item IDs | snake_case; all drops must exist in `items.json` |
| i18n inline | `{ "en": "...", "ja": "...", "zh": "..." }` |

## Related docs

- `docs/DATA_ARCHITECTURE.md` — full architecture
- `docs/QUEST_AND_FLAGS.md` — quest & flag detail
- `docs/ITEMS_AND_ECONOMY.md` — item catalog
- `docs/ENCOUNTER_TABLE.md` — pacing
