# Tides of Urashima

A short **3D JRPG adventure** for PC (Steam), adapted from the public-domain Japanese folktale *Urashima Tarō*.

**Engine:** Godot 4 (MIT, no royalties)  
**Languages:** English, 日本語, 简体中文 (Noto Sans fonts bundled)  
**Target audience:** Men 20–30  
**Playtime:** 2–3 hours  

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

---

## Repository layout

```
docs/
  GDD.md              # Game design document
  STORYBOARD.md       # 18 scene beats
  ART_DIRECTION.md    # Visual style bible
  LICENSES.md         # Asset attribution log

steam/
  STORE_PAGE.md       # Steam store listing copy + asset checklist
  capsule_*.png       # Store capsule placeholders

game/
  project.godot       # Open in Godot 4.3+
  export_presets.cfg  # Windows Desktop export preset
  data/               # JSON — skills, enemies, dialogue, quests
  scripts/            # GDScript systems
  scenes/             # Godot scenes
  assets/             # Models, textures, audio
```

---

## Getting started

### Requirements

- [Godot 4.3+](https://godotengine.org/download)
- Git

### Run locally

1. Clone this repository
2. Open `game/project.godot` in Godot
3. Press **F5** to run (starts at Main Menu)

Optional **dev-only** Godot Editor automation via GDAI MCP (not shipped in Steam builds): [`docs/GDAI_CLOUD_SETUP.md`](docs/GDAI_CLOUD_SETUP.md).

### Controls

| Action | Key |
|--------|-----|
| Move | WASD |
| Interact | E |
| Menu | Tab |
| Confirm | Enter / Space |
| Cancel | Esc |

---

## Design highlights

- **Story:** Dark retelling — Urashima returns to a ruined village; the lacquer box holds stolen years
- **Combat:** Turn-based, speed-initiative, data-driven JSON skills/enemies/AI
- **Endings:** Rewind / Anchor / Drift (player choice at final boss)
- **Assets:** CC0 / public domain only (see `docs/LICENSES.md`)

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
