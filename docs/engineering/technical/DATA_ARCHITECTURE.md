---
id: data-architecture
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, builder]
status: active
authority: engineering
tokens_est: 597
summary: "Data follows the story spine — scenes drive flags, flags drive quests, quests drive encounters and rewards."
---
# Tides of Urashima — Story-Driven Data Architecture

**Version:** 1.0
**Hub:** [`CODING_STANDARDS_HUB.md`](CODING_STANDARDS_HUB.md) — naming, schema bumps, extension checklists

## When to read

Use **Tides of Urashima — Story-Driven Data Architecture** (roles: architect, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [1. Why story-first data?](#1-why-story-first-data)
- [2. Recommended file layout](#2-recommended-file-layout)
- [Data packs (progressive disclosure)](#data-packs-progressive-disclosure)


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

## Data packs (progressive disclosure)

| Pack | Path |
|------|------|
| Story spine / flags / dialogue | [data/story_spine.md](data/story_spine.md) |
| Combat & economy | [data/combat_economy.md](data/combat_economy.md) |
| i18n / validation / schema | [data/i18n_validation.md](data/i18n_validation.md) |

