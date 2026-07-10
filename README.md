# Tides of Urashima

A short **3D JRPG adventure** for PC (Steam), adapted from the public-domain Japanese folktale *Urashima Tarō*.

**Engine:** Godot 4 (MIT, no royalties)  
**Languages:** English, 日本語, 简体中文 (Noto Sans fonts bundled)  
**Target audience:** Men 20–30  
**Playtime:** 2–3 hours  

> **This branch (`main`)** holds game design documents, **story-driven JSON data** (`game/data/`), and release plans. Godot scenes/scripts live on feature branches.

---

## Project status

| Milestone | Status |
|-----------|--------|
| M0 — GDD, storyboard, repo scaffold | Done |
| M0b — Multi-language (en / ja / zh) | Done |
| M1 — Greybox movement + dialogue | Done |
| M2 — Combat vertical slice | Done |
| M3 — Chapter 1 playable | Done |
| M4 — Full story + endings | Done |
| M5 — Polish + Steam page | In progress |
| M0c — Art rebuild specs | Done |
| M0d — Gameplay systems specs | Done |
| M0e — Story data on main | Done |
| M6 — Art rebuild (high-detail Japanese) | Not started |

---

## Pre-build design package

### Art & compliance (M0c)

| Document | Purpose |
|----------|---------|
| [Character Bible](docs/CHARACTER_BIBLE.md) | Models, colors, animations, portraits |
| [Items 3D Model Guide](docs/ITEMS_3D_MODEL_GUIDE.md) | Weapons, props, pickups, attachment rig |
| [Environment Kits](docs/ENVIRONMENT_KITS.md) | Modular assets per zone + lore placements |
| [Boss Designs](docs/BOSS_DESIGNS.md) | Phases, patterns, hard mode |
| [Encounter Table](docs/ENCOUNTER_TABLE.md) | Pacing, XP, shop, equipment |
| [Cinematics](docs/CINEMATICS.md) | Camera, boss intros, endings |
| [Audio Direction](docs/AUDIO_DIRECTION.md) | Music map, SFX, scene cues |
| [Audio Production Guide](docs/AUDIO_PRODUCTION_GUIDE.md) | BGM specs, SFX manifest, scene map |
| [Asset Compliance](docs/ASSET_COMPLIANCE.md) | Copyright-safe policy + verification tools |
| [Art Direction](docs/ART_DIRECTION.md) | Visual pivot + poly budgets |
| [Storyboard Illustrations](docs/STORYBOARD_ILLUSTRATIONS.md) | Pitch art spec + scene briefs |
| [Pitch images](docs/pitch/illustrations/) | P0 concept art (5 images) for presentations |

### Gameplay systems (M0d)

| Document | Purpose |
|----------|---------|
| [Quest & Flags](docs/QUEST_AND_FLAGS.md) | 5 quests, story flags, zone blockers |
| [Tutorial Design](docs/TUTORIAL_DESIGN.md) | Onboarding matrix + SC-00 prologue |
| [Ending Design](docs/ENDING_DESIGN.md) | Choice UI, 3 endings, replay |
| [Items & Economy](docs/ITEMS_AND_ECONOMY.md) | Canonical items, shop, drops |
| [Combat Systems](docs/COMBAT_SYSTEMS.md) | Elements, status, limits |
| [Skills Bible](docs/SKILLS_BIBLE.md) | 15 player skills |
| [UI / UX Flow](docs/UI_UX_FLOW.md) | Menus, HUD, controller |
| [Save & Fail States](docs/SAVE_AND_FAIL_STATES.md) | Autosave, game over |
| [Settings & Accessibility](docs/SETTINGS_ACCESSIBILITY.md) | Options, hard mode, a11y |
| [Puzzle Design](docs/PUZZLE_DESIGN.md) | SC-07 water puzzle |
| [Achievements](docs/ACHIEVEMENTS.md) | 12 Steam achievements |
| [Playtest Script](docs/PLAYTEST_SCRIPT.md) | 2–3h QA path |
| [QA & Bug Process](docs/QA_AND_BUG_PROCESS.md) | Severity, triage, regression |
| [Narrative Writing Guide](docs/NARRATIVE_WRITING_GUIDE.md) | Voice, silence, no VO, i18n prose |
| [Progression Tuning](docs/PROGRESSION_TUNING.md) | XP, stats, economy, difficulty |
| [Game Feel](docs/GAME_FEEL.md) | Combat juice, feedback, rewards |
| [Lore & Environmental Story](docs/LORE_AND_ENVIRONMENTAL_STORY.md) | 8 lore entries, hub emptiness |
| [World Map & Flow](docs/WORLD_MAP_AND_FLOW.md) | Zones, connections, save points |
| [Replay Design](docs/REPLAY_DESIGN.md) | Endings gallery, second run |
| [Pacing Chart](docs/PACING_CHART.md) | Emotional beat timeline |

### Story data (M0e)

| Document / path | Purpose |
|-----------------|---------|
| [Data Architecture](docs/DATA_ARCHITECTURE.md) | Story-first DB design |
| `game/data/story/scenes.json` | Scene spine SC-00…SC-17c |
| `game/data/story/flags.json` | Flag registry |
| `game/data/quests/main_quests.json` | 5 main quests |
| `game/data/encounters/story_encounters.json` | Scripted fights |
| `game/data/dialogue/chapter_01.json` | All dialogue |
| `game/data/items/items.json` | Full item catalog |
| `game/data/shop/roku_shop.json` | Roku shop |
| `game/data/starting/new_game.json` | New game defaults |

```bash
python3 tools/validate_story_data.py
```

```bash
# Register a new external asset
python3 tools/register_asset.py add \
  --path game/assets/models/characters/urashima/urashima.glb \
  --license ORIGINAL --source "Custom Blender" --author "Project" \
  --used-for "Protagonist model"

# Verify all media + generate audit proof
bash tools/check_asset_compliance.sh
```

---

## Repository layout (`main` — docs & plans)

```
docs/
  GDD.md                 # Game design document
  STORYBOARD.md          # 19 scene beats (SC-00 prologue + 18 main)
  ART_DIRECTION.md       # Visual style bible (v1.1 — high-detail Japanese)
  CHARACTER_BIBLE.md     # Character models, anims, portraits
  ITEMS_3D_MODEL_GUIDE.md # Item/prop 3D specs, rig attachments
  ENVIRONMENT_KITS.md    # Modular environment specs per zone
  BOSS_DESIGNS.md        # Boss phases and patterns
  ENCOUNTER_TABLE.md     # Combat pacing, shop, economy
  CINEMATICS.md          # Camera and cinematic beats
  AUDIO_DIRECTION.md     # Music and SFX creative direction
  AUDIO_PRODUCTION_GUIDE.md # BGM/SFX production specs, scene map
  PACING_CHART.md        # Emotional beat timeline
  QUEST_AND_FLAGS.md     # 5 quests + story flags
  TUTORIAL_DESIGN.md     # Onboarding spec
  ENDING_DESIGN.md       # Three endings + choice UI
  ITEMS_AND_ECONOMY.md   # Items, shop, drops
  COMBAT_SYSTEMS.md      # Elements, status, limits
  SKILLS_BIBLE.md        # Player skills
  UI_UX_FLOW.md          # Menus and HUD
  SAVE_AND_FAIL_STATES.md
  SETTINGS_ACCESSIBILITY.md
  PUZZLE_DESIGN.md
  ACHIEVEMENTS.md
  PLAYTEST_SCRIPT.md
  QA_AND_BUG_PROCESS.md  # Bug severity, triage, regression
  NARRATIVE_WRITING_GUIDE.md # Voice, no VO, SC-07 silence
  PROGRESSION_TUNING.md  # XP, stats, economy, difficulty
  GAME_FEEL.md           # Feedback, juice, rewards
  LORE_AND_ENVIRONMENTAL_STORY.md
  WORLD_MAP_AND_FLOW.md
  REPLAY_DESIGN.md
  MILESTONES.md          # Implementation checklist
  LOCALIZATION.md        # en / ja / zh notes
  LICENSES.md            # Asset attribution log
  ASSET_COMPLIANCE.md    # Copyright-safe asset policy (no ARR / NC / SA)
  asset_manifest.license.json  # Machine-readable license manifest

tools/
  check_asset_compliance.sh      # Verify + generate audit proof
  verify_asset_licenses.py       # Scan media vs manifest
  register_asset.py              # Add assets to manifest
  generate_compliance_report.py  # Write COMPLIANCE_REPORT.md
  SCREENSHOTS.md         # Screenshot capture notes
  GDAI_CLOUD_SETUP.md    # Dev-only GDAI MCP setup (for code branches)

steam/
  STORE_PAGE.md          # Steam store listing copy + asset checklist
  GODOTSTEAM_SETUP.md    # Steamworks / export checklist
```

Godot project code (`game/`, `tools/`, etc.) is on feature branches — check out `cursor/gdai-regen-dc91` (GDAI MCP experiment) or `cursor/urashima-jrpg-scaffold-dc91` to run the game.

---

## Getting started (code branches)

Design docs on `main` are the source of truth. To run the game, check out an implementation branch and follow its README:

```bash
git fetch origin
git checkout cursor/urashima-jrpg-scaffold-dc91   # or another feature branch
```

For a GDAI MCP regeneration experiment (GDAI only — **not** GodotPrompter):

```bash
git fetch origin
git checkout cursor/gdai-regen-dc91
```

Then open `game/project.godot` in Godot 4.3+ and follow [`docs/GDAI_REGEN_PLAN.md`](docs/GDAI_REGEN_PLAN.md) + [`docs/GDAI_CLOUD_SETUP.md`](docs/GDAI_CLOUD_SETUP.md).

---

## Design highlights

- **Story:** Dark retelling — Urashima returns to a ruined village; the lacquer box holds stolen years
- **Combat:** Turn-based, speed-initiative, data-driven JSON skills/enemies/AI
- **Endings:** Rewind / Anchor / Drift (player choice at final boss)
- **Assets:** Custom high-detail Japanese stylized — **copyright-safe only** (CC0, MIT, OFL, commissioned). See `docs/ASSET_COMPLIANCE.md`

---

## Data-driven content

All combat and narrative content lives in `game/data/`. See `game/data/README.md` for the JSON schema.

Example — start tutorial combat from code:

```gdscript
GameManager.start_combat(["salt_crab"])
```

Example — play a dialogue scene (UI appears automatically):

```gdscript
DialogueRunner.play_scene("SC-03")
```

---

## Documentation

- [Game Design Document](docs/GDD.md)
- [Storyboard](docs/STORYBOARD.md)
- [Art Direction](docs/ART_DIRECTION.md)
- [Character Bible](docs/CHARACTER_BIBLE.md)
- [Items 3D Model Guide](docs/ITEMS_3D_MODEL_GUIDE.md)
- [Environment Kits](docs/ENVIRONMENT_KITS.md)
- [Boss Designs](docs/BOSS_DESIGNS.md)
- [Encounter Table](docs/ENCOUNTER_TABLE.md)
- [Cinematics](docs/CINEMATICS.md)
- [Audio Direction](docs/AUDIO_DIRECTION.md)
- [Audio Production Guide](docs/AUDIO_PRODUCTION_GUIDE.md)
- [Pacing Chart](docs/PACING_CHART.md)
- [Quest & Flags](docs/QUEST_AND_FLAGS.md)
- [Tutorial Design](docs/TUTORIAL_DESIGN.md)
- [Ending Design](docs/ENDING_DESIGN.md)
- [Items & Economy](docs/ITEMS_AND_ECONOMY.md)
- [Combat Systems](docs/COMBAT_SYSTEMS.md)
- [Skills Bible](docs/SKILLS_BIBLE.md)
- [UI / UX Flow](docs/UI_UX_FLOW.md)
- [Save & Fail States](docs/SAVE_AND_FAIL_STATES.md)
- [Settings & Accessibility](docs/SETTINGS_ACCESSIBILITY.md)
- [Puzzle Design](docs/PUZZLE_DESIGN.md)
- [Achievements](docs/ACHIEVEMENTS.md)
- [Playtest Script](docs/PLAYTEST_SCRIPT.md)
- [QA & Bug Process](docs/QA_AND_BUG_PROCESS.md)
- [Narrative Writing Guide](docs/NARRATIVE_WRITING_GUIDE.md)
- [Progression Tuning](docs/PROGRESSION_TUNING.md)
- [Game Feel](docs/GAME_FEEL.md)
- [Lore & Environmental Story](docs/LORE_AND_ENVIRONMENTAL_STORY.md)
- [World Map & Flow](docs/WORLD_MAP_AND_FLOW.md)
- [Replay Design](docs/REPLAY_DESIGN.md)
- [Localization guide](docs/LOCALIZATION.md)
- [License log](docs/LICENSES.md)
- [Asset compliance policy](docs/ASSET_COMPLIANCE.md)
- [Combat data schema](game/data/README.md)

---

## Steam

Store page copy and capsule placeholders are in [`steam/STORE_PAGE.md`](steam/STORE_PAGE.md).

- Export preset: `game/export_presets.cfg` (Windows Desktop)
- GodotSteam integration: planned (see `docs/MILESTONES.md`)
- Target price: $4.99–$9.99

---

## Credits

- Story adapted from *Urashima Tarō* (Japanese folklore, public domain)
- Built with [Godot Engine](https://godotengine.org) (MIT License)
