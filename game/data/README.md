# Data Schema — Tides of Urashima

**Story-driven JSON database.** Read `docs/DATA_ARCHITECTURE.md` for design rationale.

## File layout

```
game/data/
  story/
    scenes.json              # Master scene spine (SC-00 … SC-17c)
    flags.json               # Canonical flag registry
    cinematic_hooks.json     # SC-08 vignette + SC-12 gate reveal hooks
  dialogue/
    chapter_01.json          # Dialogue by scene_id; optional voice_id per line
  audio/
    vo_prompts.json          # ElevenLabs casting + 12 selective VO clips
  models/
    qa_catalog.json          # 3D model paths, tri budgets, hero_jury list (docs/MODEL_QA.md)
  qa/
    remediation_playbook.json  # Failure code → fix actions (docs/QA_REMEDIATION_LOOP.md)
    acceptance_criteria.json   # Measurable gate thresholds (docs/ACCEPTANCE_CRITERIA.md)
  code/
    base_classes.json          # Architect-owned base classes + component scenes (docs/CODE_BASE_CLASS_RULES.md)
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
python3 tools/validate_base_classes.py
python3 tools/validate_acceptance_criteria.py
bash tools/check_asset_compliance.sh   # when assets exist
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
| i18n inline | `{ "en": "...", "ja": "...", "zh": "...", "zh-Hant": "..." }` |
| Selective VO | `voice_id` on line → `game/assets/audio/voice/{locale}/{voice_id}.ogg` (zh-Hant: `.../zh-Hant/{dialect}/...`) |

## Schema versions

See `docs/DATA_ARCHITECTURE.md` §17. Summary: `chapter_01.json` = `schema_version: 4`; audio catalogs use `"version": "1.0"`.

## Scene count

- **20** scene headings in `docs/STORYBOARD.md` (`SC-00`…`SC-16` = 17, plus 3 ending variants `SC-17a`/`b`/`c`); a single playthrough experiences **18** (one ending only)
- **23** rows in `story/scenes.json` = the 20 storyboard headings + 3 SC-02 inspectable rows (`SC-02-BANNER`/`SANDAL`/`WELL`)
- **22** dialogue scene keys in `chapter_01.json` = the 23 rows minus the silent `SC-07` (no dialogue block)

## Related docs

- `docs/DATA_ARCHITECTURE.md` — full architecture
- `docs/QUEST_AND_FLAGS.md` — quest & flag detail
- `docs/ITEMS_AND_ECONOMY.md` — item catalog
- `docs/ITEMS_3D_MODEL_GUIDE.md` — item 3D mesh specs
- `docs/ENCOUNTER_TABLE.md` — pacing
- `docs/REPLAY_DESIGN.md` — replay & gallery
- `docs/NARRATIVE_WRITING_GUIDE.md` — writing, selective VO, i18n prose
- `docs/VO_HIT_LIST.md` — emotional VO clip list + ElevenLabs generation
