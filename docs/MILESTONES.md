# Milestone checklist

Track implementation progress against the GDD milestones.

## M0 — Pre-production
- [x] Game Design Document (`docs/GDD.md`)
- [x] Storyboard — 18 scenes (`docs/STORYBOARD.md`)
- [x] Art direction bible (`docs/ART_DIRECTION.md`)
- [x] License tracking template (`docs/LICENSES.md`)
- [x] Godot 4 project scaffold
- [x] Combat JSON schema + sample data
- [x] Core scripts (GameManager, Combat, Dialogue, Save)
- [x] **Multi-language support (en / ja / zh)** — `docs/LOCALIZATION.md`

## M1 — Greybox exploration
- [x] Player movement polish (camera orbit — right-mouse + scroll)
- [x] Interaction prompt HUD (Press E — action, localized)
- [x] Dialogue box UI scene (typewriter, speaker, locale fonts)
- [x] CJK font bundle + locale-aware `FontThemeManager`
- [x] Quest tracker UI
- [x] Save point at village well

## M2 — Combat vertical slice
- [x] Combat UI vertical slice (HP/MP bars, action menu, battle log, enemy intent)
- [x] Combat polish (transitions, damage flash, items, escape, boss banners)

## M3 — Chapter 1
- [x] Tidal Caves greybox map
- [x] Water level puzzle
- [x] Shore Wraith boss
- [x] Yuzu joins party

## M4 — Full game
- [x] Dragon Palace Gate dungeon
- [x] Palace Sentinel + Tide Keeper bosses
- [x] Three endings
- [x] Credits sequence

## M5 — Steam
- [x] Placeholder BGM/SFX + AudioManager → **procedural coastal JRPG audio** (`tools/generate_game_audio.py`)
- [x] Zone art pass (materials, fog, props) → **tileable zone textures + portraits**
- [x] Field item use + equipment UI (Tab menu)
- [x] Steam store page copy + capsule placeholders
- [x] Windows export preset + `tools/export_windows.sh`
- [x] Steam screenshots + trailer placeholder (`steam/screenshots/`, `steam/trailer.mp4`)
- [x] GodotSteam scaffold (`SteamManager` + `game/addons/godotsteam/README.md`)
- [x] Combat drop rolls + balance pass
- [x] Install GodotSteam GDExtension binaries (`tools/install_godotsteam.sh`)
- [ ] Steamworks app ID + depot upload
- [ ] Final CC0 audio/art replacement (optional — current assets are original procedural)
- [ ] Playtest on Windows hardware
