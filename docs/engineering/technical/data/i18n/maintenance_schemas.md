---
id: maintenance-schemas
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, builder]
status: active
authority: engineering
tokens_est: 738
summary: "All spine files below are already present in `game/data/`. This is the dependency order to keep in mind when editing — change upstream files before downstream r"
---
# Data — i18n & Validation — Maintenance + schemas

**Hub:** [`i18n_validation.md`](../i18n_validation.md)

## When to read

Use **Data — i18n & Validation — Maintenance + schemas** (roles: architect, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [15. File maintenance order (all files already exist)](#15-file-maintenance-order-all-files-already-exist)
- [16. Scene index vs storyboard count](#16-scene-index-vs-storyboard-count)
- [17. JSON schema versions](#17-json-schema-versions)


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
| `docs/design/vision/STORYBOARD.md` | **19** narrative beats | SC-00 + 18 main-path scenes |
| `story/scenes.json` | **24** rows | Adds SC-01 driftwood inspect + SC-02 inspectable sub-scenes + SC-17a/b/c ending variants |
| `dialogue/chapter_01.json` | **23** scene keys | SC-07 silent puzzle — no dialogue block by design |

All `scene_id` values in dialogue, encounters, and flags must exist in `scenes.json`.

---


## 17. JSON schema versions

Files use `schema_version` (integer) or `version` (string) to track format evolution. The validator checks content, not version numbers.

| File | Key | Current | Notes |
|------|-----|---------|-------|
| `dialogue/chapter_01.json` | `schema_version` | **5** | Adds `subtext` / `subtext_warm` on SC-16 choices |
| `quests/main_quests.json`, `items/items.json` | `schema_version` | **2** | — |
| Most other `game/data/**/*.json` | `schema_version` | **1** | — |
| `audio/vo_prompts.json`, `ace_step_prompts.json` | `version` | **"1.0"** | Audio generation metadata (not gameplay schema) |
| `audio/audio_qa_catalog.json` | `version` | **"1.0"** | Unified BGM/VO QA catalog — loudness, jury scope, brief paths (`docs/design/audio/AUDIO_QA.md`) |
| `audio/scene_audio_map.json` | `version` | **"1.0"** | Zone/scene → BGM, ambient, sting, duck (`AUDIO_PRODUCTION_GUIDE.md` §4) |
| `qa/generation_readiness_backlog.json` | `version` | **"1.0"** | GR-* items → IMPLEMENTATION_PLAN tasks |

Bump `schema_version` when breaking field renames; run `python3 tools/validate_story_data.py` after edits.

**Dialogue layout:** `chapter_01.json` holds all scenes including SC-00. Optional `dialogue/prologue.json` split is documented but **not used** in this repo.

---
