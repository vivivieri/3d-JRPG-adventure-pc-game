# Tides of Urashima

A short **3D JRPG adventure** for PC (Steam), adapted from the public-domain Japanese folktale *Urashima Tarō*.

**Engine:** Godot 4 (MIT, no royalties)  
**Languages:** English, 日本語, 简体中文 (Noto Sans fonts bundled)  
**Target audience:** Men 20–30  
**Playtime:** 2–3 hours  

> **This branch (`main`)** holds game design documents and release plans only. Godot implementation lives on feature branches (e.g. `cursor/urashima-jrpg-scaffold-dc91`, `cursor/japanese-environment-dc91`). Use `docs/GDAI_CLOUD_SETUP.md` when experimenting with GDAI MCP / GodotPrompter on a code branch.

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
| M6 — Art rebuild (high-detail Japanese) | Not started |

---

## Pre-build design package (M0c)

Before the art rebuild, these specs are the source of truth:

| Document | Purpose |
|----------|---------|
| [Character Bible](docs/CHARACTER_BIBLE.md) | Models, colors, animations, portraits |
| [Environment Kits](docs/ENVIRONMENT_KITS.md) | Modular assets per zone + lore placements |
| [Boss Designs](docs/BOSS_DESIGNS.md) | Phases, patterns, hard mode |
| [Encounter Table](docs/ENCOUNTER_TABLE.md) | Pacing, XP, shop, equipment |
| [Cinematics](docs/CINEMATICS.md) | Camera, boss intros, endings |
| [Audio Direction](docs/AUDIO_DIRECTION.md) | Music map, SFX, scene cues |
| [Art Direction](docs/ART_DIRECTION.md) | Visual pivot + poly budgets |

---

## Repository layout (`main` — docs & plans)

```
docs/
  GDD.md                 # Game design document
  STORYBOARD.md          # 18 scene beats
  ART_DIRECTION.md       # Visual style bible (v1.1 — high-detail Japanese)
  CHARACTER_BIBLE.md     # Character models, anims, portraits
  ENVIRONMENT_KITS.md    # Modular environment specs per zone
  BOSS_DESIGNS.md        # Boss phases and patterns
  ENCOUNTER_TABLE.md     # Combat pacing, shop, economy
  CINEMATICS.md          # Camera and cinematic beats
  AUDIO_DIRECTION.md     # Music and SFX spec
  MILESTONES.md          # Implementation checklist
  LOCALIZATION.md        # en / ja / zh notes
  LICENSES.md            # Asset attribution log
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
- **Assets:** Custom high-detail Japanese stylized (CC0 / commissioned); see `docs/ART_DIRECTION.md`

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
- [Environment Kits](docs/ENVIRONMENT_KITS.md)
- [Boss Designs](docs/BOSS_DESIGNS.md)
- [Encounter Table](docs/ENCOUNTER_TABLE.md)
- [Cinematics](docs/CINEMATICS.md)
- [Audio Direction](docs/AUDIO_DIRECTION.md)
- [Localization guide](docs/LOCALIZATION.md)
- [License log](docs/LICENSES.md)
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
