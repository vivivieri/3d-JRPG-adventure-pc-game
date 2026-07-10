# Tides of Urashima

A short **3D JRPG adventure** for PC (Steam), adapted from the public-domain Japanese folktale *Urashima Tarō*.

**Engine:** Godot 4 (MIT, no royalties)  
**Languages:** English, 日本語, 简体中文 (Noto Sans fonts bundled)  
**Target audience:** Men 20–30  
**Playtime:** 2–3 hours  

> **This branch (`cursor/godotprompt-complete-c4bf`)** is the **GodotPrompter complete build** — full game implementation guided by [GodotPrompter](https://github.com/jame581/GodotPrompter) agent skills. Do **not** use GDAI MCP here; see `cursor/gdai-regen-dc91` for that experiment. Design docs on `main` remain the source of truth.

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
| M5 — Polish + Steam page | Done |

---

## Repository layout

```
docs/
  GDD.md                      # Game design document
  STORYBOARD.md               # 18 scene beats
  ART_DIRECTION.md            # Visual style bible
  GODOTPROMPTER_BUILD_PLAN.md # GodotPrompter build checklist (this branch)
  MILESTONES.md               # Implementation checklist
  LOCALIZATION.md             # en / ja / zh notes
  LICENSES.md                 # Asset attribution log

game/
  project.godot               # Open in Godot 4.3+
  data/                       # JSON — skills, enemies, dialogue, quests
  scripts/                    # GDScript systems (EventBus, combat, dialogue)
  scenes/                     # World zones + UI
  assets/                     # Fonts, audio, textures

tools/
  install_godotprompter.sh    # Clone GodotPrompter skills for Cursor
  export_windows.sh           # Windows desktop export

steam/
  STORE_PAGE.md               # Steam store listing copy
  GODOTSTEAM_SETUP.md         # Steamworks / export checklist
```

---

## Getting started

### Requirements

- [Godot 4.3+](https://godotengine.org/download)
- Git
- Cursor with GodotPrompter (optional but recommended for AI-assisted edits)

### Install GodotPrompter skills

```bash
./tools/install_godotprompter.sh
```

Or in Cursor: `/add-plugin godot-prompter`

### Run locally

1. Clone and check out this branch:

   ```bash
   git fetch origin
   git checkout cursor/godotprompt-complete-c4bf
   ```

2. Open `game/project.godot` in Godot 4.3+
3. Press **F5** — starts at Main Menu → New Game → Beach Shore (SC-01)

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

```gdscript
GameManager.start_combat(["salt_crab"])
DialogueRunner.play_scene("SC-03")
```

---

## Documentation

- [GodotPrompter Build Plan](docs/GODOTPROMPTER_BUILD_PLAN.md)
- [Game Design Document](docs/GDD.md)
- [Storyboard](docs/STORYBOARD.md)
- [Art Direction](docs/ART_DIRECTION.md)
- [Combat data schema](game/data/README.md)

---

## Steam

Store page copy and capsule placeholders are in [`steam/STORE_PAGE.md`](steam/STORE_PAGE.md).

- Export: `./tools/export_windows.sh`
- GodotSteam scaffold in `game/addons/godotsteam/`
- Target price: $4.99–$9.99

---

## Credits

- Story adapted from *Urashima Tarō* (Japanese folklore, public domain)
- Built with [Godot Engine](https://godotengine.org) (MIT License)
- AI development guided by [GodotPrompter](https://github.com/jame581/GodotPrompter) skills
