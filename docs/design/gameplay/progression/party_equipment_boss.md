---
id: party-equipment-boss
type: reference
audience: [builder, builder_combat, qa]
phase: [2, 3]
status: active
authority: gameplay
tokens_est: 851
summary: "Progression & Tuning — Party stats, equipment, bosses — Formula: `base + growth × (level − 1)` from `party.json`."
---
# Progression & Tuning — Party stats, equipment, bosses

**Hub:** [`PROGRESSION_TUNING.md`](../PROGRESSION_TUNING.md)

## When to read

Use **Progression & Tuning — Party stats, equipment, bosses** (roles: builder, builder_combat, qa) when you need this reference during the current task Jump to a section below instead of reading end-to-end (6 sections).

## Jump to

- [3. Party stats at milestones](#3-party-stats-at-milestones)
- [Urashima (active entire game)](#urashima-active-entire-game)
- [Yuzu (joins SC-10, enters at ~party L5)](#yuzu-joins-sc-10-enters-at-party-l5)
- [Roku (combat SC-12+, enters at ~party L6)](#roku-combat-sc-12-enters-at-party-l6)
- [4. Equipment & power spikes](#4-equipment-power-spikes)
- [5. Boss tuning reference](#5-boss-tuning-reference)


## 3. Party stats at milestones

Formula: `base + growth × (level − 1)` from `party.json`.

### Urashima (active entire game)

| Level | HP | MP | ATK | DEF | MAG | RES | SPD | Scene |
|-------|-----|-----|-----|-----|-----|-----|-----|-------|
| 1 | 120 | 30 | 14 | 10 | 8 | 9 | 11 | SC-01 |
| 4 | 156 | 39 | 20 | 13 | 11 | 12 | 14 | SC-08 |
| 5 | 168 | 42 | 22 | 14 | 12 | 13 | 15 | SC-09 boss |
| 7 | 192 | 48 | 26 | 16 | 14 | 15 | 17 | SC-14 |
| 10 | 228 | 57 | 32 | 19 | 17 | 18 | 20 | SC-16 |

**Skill unlocks:** Lv5 `ocean_veil` | Lv10 `returning_wave` | Limit `box_unbound`

### Yuzu (joins SC-10, enters at ~party L5)

| Level | HP | MP | MAG | RES | Notes |
|-------|-----|-----|-----|-----|-------|
| 5 | 117 | 65 | 22 | 20 | Join fight |
| 7 | 133 | 75 | 26 | 24 | Sentinel |
| 10 | 157 | 90 | 32 | 30 | Final boss |

**Skill unlocks:** Lv4 `sacred_mend` | Lv8 `torii_ward` | Join: `purify`, `spirit_light`

### Roku (combat SC-12+, enters at ~party L6)

| Level | HP | MP | ATK | DEF | Notes |
|-------|-----|-----|-----|-----|-------|
| 6 | 225 | 25 | 22 | 24 | First fight |
| 7 | 240 | 27 | 24 | 26 | Sentinel |
| 10 | 285 | 33 | 30 | 32 | Final boss |

**Skill unlocks:** Lv3 `harpoon_drive` | Lv7 `tide_taunt` | Join: `shell_guard`

---


## 4. Equipment & power spikes

| Milestone | Urashima weapon | ATK equiv | Other |
|-----------|-----------------|-----------|-------|
| Start | `fisher_katana` | +4 | `worn_haori` +2 DEF |
| SC-07 chest | `tide_cut_saber` | +7 | Optional puzzle reward |
| SC-14 drop | `palace_edge` | +10 | Best weapon |

| Shop (SC-04+) | Price | When affordable |
|---------------|-------|-----------------|
| `sea_salve` ×2 | 80 | Post SC-09 |
| `cave_wet_coat` | 120 | Post SC-09 + Q2 (~130 coins) |
| `shell_charm` | 80 | Act II |
| Skill scroll | 200 | Pre-Keeper (~225 coins, if saved) |

**Affordance rule:** Main path grants **≈220–280 coins** before the final boss (mandatory fights
+ Q2 reward + optional fights/material sales — computed from `enemies.json` / `main_quests.json`).
Player can buy several salves + one charm, OR save for **0–1** skill scroll (200 coins) before the final boss — not both a full consumable stock and a scroll.

---


## 5. Boss tuning reference

| Boss | Party at fight | Solo? | HP (Normal, `enemies.json`) | Attempts target |
|------|----------------|-------|------------------------------|-----------------|
| Shore Wraith | Urashima L4–5 | Yes | 320 (solo tune) | ≤2 |
| Palace Sentinel | Full L6–7 | No | 250 | ≤2 |
| Tide Keeper | Full L8–10 | No | 580 | ≤3 |

Full patterns: `BOSS_DESIGNS.md`. Sentinel Spirit ×1.5 for Yuzu skills.

---
