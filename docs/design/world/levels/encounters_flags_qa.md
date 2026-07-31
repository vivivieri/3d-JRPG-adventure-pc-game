---
id: encounters-flags-qa
type: reference
audience: [builder, builder_zone, architect]
phase: [1, 5]
status: active
authority: world
tokens_est: 560
summary: "Encounters, flags, QA"
---
# Level Design — Encounters, flags, QA

**Hub:** [`LEVEL_DESIGN.md`](../LEVEL_DESIGN.md)

## 7. Encounter index (all zones)

| Encounter ID | Zone | Scene | Boss? |
|--------------|------|-------|-------|
| `enc_sc05_tutorial_crab` | ruined_village | SC-05 | No |
| `enc_sc06_cave_crab` | tidal_caves | SC-06 | No |
| `enc_sc07_optional_crabs` | tidal_caves | SC-07 | No (optional) |
| `enc_sc08_deep_pool` | tidal_caves | SC-08 | No |
| `enc_sc09_shore_wraith` | tidal_caves | SC-09 | **Yes** |
| `enc_sc10_optional_wraith` | tidal_caves | SC-10 | No (optional) |
| `enc_sc12_palace_wraiths` | dragon_palace_gate | SC-12 | No |
| `enc_sc14_sentinel` | dragon_palace_gate | SC-14 | **Yes** |
| `enc_sc15_tide_keeper` | dragon_palace_gate | SC-15 | **Yes** |

Source: `game/data/encounters/story_encounters.json`.

---


## 8. Flag gates summary

| Gate | Flag / item | Blocks |
|------|---------------|--------|
| Cave entrance | `cave_entrance_unlocked` | `ruined_village` → `tidal_caves` |
| Deep pool | `water_puzzle_solved` | SC-08 onward |
| Palace exterior | `yuzu_joined`, `wraith_pearl` | SC-12 zone load |
| Ending branch | `ending_chosen` value | SC-17a/b/c |

Full registry: `game/data/story/flags.json`.

---


## 9. QA checklist (level design)

- [ ] Every `Interactable_*` has matching `chapter_01.json` key or inspect sub-scene
- [ ] Every `EncounterTrigger_*` exists in `story_encounters.json`
- [ ] Spawn markers tested for Continue load
- [ ] No soft-lock: SC-07 hint after 3 min stuck (`PUZZLE_DESIGN.md` §5)
- [ ] Zone transitions show 2s area name toast
- [ ] Backtrack village → caves → village works after Yuzu join
- [ ] SC-12 cinematic skippable after 3s on replay

---


## 10. Related docs (don't duplicate here)

| Topic | Doc |
|-------|-----|
| Zone graph & connections | `WORLD_MAP_AND_FLOW.md` |
| Kit meshes & poly budgets | `ENVIRONMENT_KITS.md` |
| Boss patterns | `BOSS_DESIGNS.md` |
| Water puzzle logic | `PUZZLE_DESIGN.md` |
| Runtime wiring | `TECHNICAL_DESIGN.md` |
| Scene spine JSON | `DATA_ARCHITECTURE.md` |
