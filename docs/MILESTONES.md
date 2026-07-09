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
- [ ] Player movement polish (camera orbit option)
- [x] Interaction prompt HUD (Press E — action, localized)
- [x] Dialogue box UI scene (typewriter, speaker, locale fonts)
- [x] CJK font bundle + locale-aware `FontThemeManager`
- [ ] Quest tracker UI
- [ ] Save point at village well

## M2 — Combat vertical slice
- [x] Combat UI vertical slice (HP/MP bars, action menu, battle log, enemy intent)
- [x] Combat polish (transitions, damage flash, items, escape, boss banners)

## M3 — Chapter 1
- [ ] Tidal Caves greybox map
- [ ] Water level puzzle
- [ ] Shore Wraith boss
- [ ] Yuzu joins party

## M4 — Full game
- [ ] Dragon Palace Gate dungeon
- [ ] Palace Sentinel + Tide Keeper bosses
- [ ] Three endings
- [ ] Credits sequence

## M5 — Steam
- [x] Placeholder BGM/SFX + AudioManager
- [x] Zone art pass (materials, fog, props)
- [x] Field item use + equipment UI (Tab menu)
- [x] Steam store page copy + capsule placeholders
- [x] Windows export preset (`game/export_presets.cfg`)
- [ ] GodotSteam integration
- [ ] Windows export build (run in Godot)
- [ ] Trailer + in-game screenshots
- [ ] Playtest + balance pass
