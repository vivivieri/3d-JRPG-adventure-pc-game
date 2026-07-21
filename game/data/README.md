# Data Schema — Tides of Urashima

**Story-driven JSON database.**
**Start here for all coding + data rules:** [`docs/technical/CODING_STANDARDS_HUB.md`](../../docs/technical/CODING_STANDARDS_HUB.md)
**JSON detail:** [`docs/technical/JSON_DATA_STYLE.md`](../../docs/technical/JSON_DATA_STYLE.md)
Design rationale: [`docs/technical/DATA_ARCHITECTURE.md`](../../docs/technical/DATA_ARCHITECTURE.md)

## File layout

```
game/data/
  story/
    scenes.json              # Master scene spine (SC-00 … SC-17c)
    flags.json               # Canonical flag registry
    cinematic_hooks.json     # SC-08 vignette + SC-12 gate reveal hooks
  dialogue/
    chapter_01.json          # Dialogue by scene_id; optional voice_id per line
  narrative/
    ending_gallery.json      # Three ending philosophy blurbs (gallery UI)
    narrative_density.json   # Ship budgets for §12 patterns (NARRATIVE_DENSITY.md)
  audio/
    ace_step_prompts.json     # ACE-Step generation prompts (MIT)
    vo_prompts.json            # ElevenLabs selective VO (12 clips)
    audio_qa_catalog.json      # Unified BGM/VO QA catalog (loudness, briefs, jury scope)
    scene_audio_map.json       # Zone/scene → BGM, ambient, sting, duck (AUDIO_PRODUCTION_GUIDE §4)
  models/
    qa_catalog.json          # 3D model paths, tri budgets, allowed/required animations (docs/art/MODEL_QA.md); v1.3+ adds crowd/npc_cinematic rows
  qa/
    remediation_playbook.json  # Failure code → fix actions (docs/qa/QA_REMEDIATION_LOOP.md)
    acceptance_criteria.json   # Measurable gate thresholds (docs/qa/ACCEPTANCE_CRITERIA.md)
    feel_thresholds.json       # GAME_FEEL automated smoke thresholds
    integration_scenarios.json # L4 INT-* catalog (implemented / required flags)
    zone_composition.json      # Per-zone path width, vista anchor, golden screenshot paths (GENERATION_READINESS §5)
    generation_readiness_backlog.json  # GR-* items → IMPLEMENTATION_PLAN tasks (must not miss during dev)
  code/
    base_classes.json          # Architect-owned base classes + component scenes (docs/technical/CODE_BASE_CLASS_RULES.md)
    spec_registry.json         # Spec-first gate + artifact index (docs/technical/SPEC_FIRST_DEVELOPMENT.md)
    autoload_registry.json     # Autoload public API contracts
    helpers_registry.json      # Core helpers + EventBus signals + regen order (docs/technical/GDSCRIPT_REGENERATION.md)
    scene_registry.json        # Canonical .tscn paths + required nodes per zone
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
python3 tools/validate_zone_composition.py
python3 tools/validate_qa_catalog.py
python3 tools/validate_audio_qa_catalog.py
python3 tools/validate_scene_audio_map.py
python3 tools/validate_generation_readiness_backlog.py
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
| Selective VO | `voice_id` on line → **all locales**: `voice/{en|ja|zh}/{voice_id}.ogg`; zh-Hant: `voice/zh-Hant/{cant|cmn}/{voice_id}.ogg` (60 files ship) |

## Schema versions

See `docs/technical/DATA_ARCHITECTURE.md` §17. Summary: `chapter_01.json` = `schema_version: 4`; audio catalogs use `"version": "1.0"`.

## Scene count

- **20** scene headings in `docs/vision/STORYBOARD.md` (`SC-00`…`SC-16` = 17, plus 3 ending variants `SC-17a`/`b`/`c`); a single playthrough experiences **18** (one ending only)
- **24** rows in `story/scenes.json` = storyboard spine + SC-01 driftwood inspect + 3 SC-02 inspectable rows
- **23** dialogue scene keys in `chapter_01.json` = the 24 rows minus silent `SC-07` (no dialogue block)

## Related docs

- [`docs/technical/CODING_STANDARDS_HUB.md`](../../docs/technical/CODING_STANDARDS_HUB.md) — naming, schema bumps, extension checklists
- [`docs/technical/DATA_ARCHITECTURE.md`](../../docs/technical/DATA_ARCHITECTURE.md) — full architecture
- `docs/world/QUEST_AND_FLAGS.md` — quest & flag detail
- `docs/gameplay/ITEMS_AND_ECONOMY.md` — item catalog
- `docs/art/ITEMS_3D_MODEL_GUIDE.md` — item 3D mesh specs
- `docs/gameplay/ENCOUNTER_TABLE.md` — pacing
- `docs/vision/REPLAY_DESIGN.md` — replay & gallery
- `docs/vision/NARRATIVE_WRITING_GUIDE.md` — writing, selective VO, i18n prose
- `docs/vision/VO_HIT_LIST.md` — emotional VO clip list + ElevenLabs generation
- `docs/audio/AUDIO_QA.md` — BGM/P0 VO technical + listen jury gates
