---
id: m1-m4-gameplay
type: reference
audience: [pm, release, architect]
status: active
authority: workflow
tokens_est: 487
summary: "M1–M4 gameplay milestones"
---
# Milestones — M1–M4 gameplay milestones

**Hub:** [`MILESTONES.md`](../MILESTONES.md)

## M1 — Greybox exploration
- [ ] Player movement polish (camera orbit — right-mouse + scroll)
- [ ] Interaction prompt HUD (Press E — action, localized)
- [ ] Dialogue box UI scene (typewriter, speaker, locale fonts)
- [ ] CJK font bundle + locale-aware `FontThemeManager` (incl. NotoSansTC for zh-Hant) — GDAI MCP + GodotPrompter Phase 2
- [ ] `LocalizationManager` + settings menu (language + `vo_dialect` for zh-Hant) — GDAI MCP builds UI scenes Phase 2
- [ ] `AudioManager` shell — procedural BGM/SFX placeholders (upgrade in M5)
- [ ] `VoiceLinePlayer` wired to `DialogueRunner` (runtime paths; clips optional until M5)
- [ ] SC-00 prologue + `CinematicDirector` opening hook
- [ ] Tab inventory / equipment menu
- [ ] Roku shop UI (`shop/roku_shop.json`)
- [ ] Quest tracker UI
- [ ] Save point at village well
- [x] Written i18n data — `zh-Hant` in `game/data/` + expanded `game/locale/translations.csv` (skills, enemies, combat, status)


## M2 — Combat vertical slice
- [ ] Combat UI vertical slice (HP/MP bars, action menu, battle log, enemy intent)
- [ ] Combat polish (transitions, damage flash, items, escape, boss banners)


## M3 — Chapter 1
- [ ] Tidal Caves greybox map + SC-06 entrance
- [ ] Water level puzzle (SC-07 — silent, no VO)
- [ ] SC-08 echo vignette (`CinematicDirector` + whisper bed)
- [ ] Shore Wraith boss (SC-09)
- [ ] Yuzu joins party (SC-10)


## M4 — Full game
- [ ] Dragon Palace Gate dungeon + SC-12 gate cinematic
- [ ] SC-11 flashback + SC-13 box revelation
- [ ] Palace Sentinel (SC-14) + Tide Keeper (SC-15) bosses
- [ ] SC-16 choice UI + three endings (SC-17a/b/c)
- [ ] Credits sequence
- [ ] E2E three endings (`bash tools/run_e2e_playthrough.sh`)
