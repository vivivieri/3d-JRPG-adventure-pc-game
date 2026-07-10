# Tides of Urashima

A short **3D JRPG adventure** for PC (Steam), adapted from the public-domain Japanese folktale *Urashima Tarō*.

**Engine:** Godot 4 (MIT, no royalties)  
**Languages:** English, 日本語, 简体中文 (Noto Sans fonts bundled)  
**Target audience:** Men 20–30  
**Playtime:** 2–3 hours  

> **This branch (`main`)** holds game design documents and release plans only. Godot implementation lives on feature branches.
>
> | Branch | Purpose |
> |--------|---------|
> | `cursor/gdai-regen-dc91` | **GDAI MCP-only** regeneration scaffold (no GodotPrompter) |
> | `cursor/urashima-jrpg-scaffold-dc91` | Original code-driven scaffold |
> | `cursor/japanese-environment-dc91` | Procedural environment polish |

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

## Repository layout (`main` — docs & plans)

```
docs/
  GDD.md                 # Game design document
  STORYBOARD.md          # 18 scene beats
  ART_DIRECTION.md       # Visual style bible
  MILESTONES.md          # Implementation checklist
  LOCALIZATION.md        # en / ja / zh notes
  LICENSES.md            # Asset attribution log
  SCREENSHOTS.md         # Screenshot capture notes
  GDAI_CLOUD_SETUP.md    # Dev-only GDAI MCP setup (for code branches)
  GDAI_REGEN_PLAN.md     # GDAI-only build phases (cursor/gdai-regen-dc91)

steam/
  STORE_PAGE.md          # Steam store listing copy + asset checklist
  GODOTSTEAM_SETUP.md    # Steamworks / export checklist
```

Godot project code (`game/`, `tools/`, etc.) is on feature branches — check out a branch such as `cursor/gdai-regen-dc91` (GDAI MCP experiment) or `cursor/urashima-jrpg-scaffold-dc91` to run or build the game.

---

## Getting started (code branches)

Design docs on `main` are the source of truth. To run the game, check out an implementation branch and follow its README:

```bash
git fetch origin
git checkout cursor/urashima-jrpg-scaffold-dc91   # or another feature branch
```

Then open `game/project.godot` in Godot 4.3+ and press **F5**.

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
