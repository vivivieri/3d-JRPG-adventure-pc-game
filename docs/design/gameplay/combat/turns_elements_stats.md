---
id: turns-elements-stats
type: reference
audience: [builder, builder_combat, qa]
phase: [2]
status: active
authority: gameplay
tokens_est: 899
summary: "Turn structure, elements, stats"
---
# Combat Systems — Turn structure, elements, stats

**Hub:** [`COMBAT_SYSTEMS.md`](../COMBAT_SYSTEMS.md)

## 1. Turn structure

```
Round start → Sort by SPD (desc) → ties random
  → Each combatant: select action → resolve in speed order
Round end → Status tick (poison, regen, duration -1)
```

**Actions:** Attack, Skill, Item, Defend, Escape (non-boss)
**Flee chance:** `50% + (party_avg_spd - enemy_spd) × 5%`, clamp 20–80%

---


## 2. Elements

**Complete matchup matrix** (attacker element → defender element; multiplier applied to final damage):

| Attacker ↓ / Defender → | Physical | Water | Spirit |
|--------------------------|----------|-------|--------|
| **Physical** | ×1.0 | ×1.0 | ×0.75 |
| **Water** | ×1.25 | ×0.75 | ×1.0 |
| **Spirit** | ×1.0 | ×1.0 | ×0.75 |

| Element | UI color |
|---------|----------|
| Physical | White |
| Water | Teal |
| Spirit | Cyan-gold |

**Multiplier vocabulary:** Strong ×1.25 · Neutral ×1.0 · Weak ×0.75 · Immune ×0 (no enemy is immune in v1).

**Sentinel special (overrides matrix):** `spirit_weakness: 1.5` in `enemies.json` — Spirit skills
deal ×1.5 vs Palace Sentinel (tutorial moment for Yuzu). Per-enemy overrides always beat the matrix.

---


## 3. Stats

| Stat | Role |
|------|------|
| HP | Health |
| MP | Skill cost |
| ATK | Physical skill power |
| DEF | Physical damage reduction |
| MAG | Spirit/water spell power |
| RES | Magic damage reduction |
| SPD | Turn order |

**Physical damage:** `power × ATK × (100 / (100 + DEF))` — DEF is the target's current DEF including equipment and Def Up/Down
**Magic damage:** `power × MAG × (100 / (100 + RES))` — skills with `power_stat: "mag"` use this, regardless of element
**Pierce:** skills with `pierce_def: X` (e.g. `harpoon_drive` 0.5) use `DEF × (1 − X)` in the formula
**Element multiplier:** applied after mitigation (see §2 matrix / per-enemy overrides)
**Defend:** Incoming damage ×0.5 this turn (applied last)
**Attack (basic):** the physical formula with `power = 1.0` — i.e. `1.0 × ATK × (100 / (100 + DEF))`, element physical
**Rounding:** final damage `floor()`, minimum 1 on any successful hit
**Hit/crit:** no accuracy, evasion, or critical-hit system in v1 — all actions hit; "miss" never occurs

### Worked examples (unit-test fixtures — `test_damage_calculator.gd`)

Order of operations: `power × stat × mitigation` → `× element multiplier` → `× defend (0.5)` → `floor`, min 1.

1. **Basic Attack** — Urashima L1 (ATK 14 + `fisher_katana` +4 = 18) attacks Salt Crab (DEF 5, physical vs physical ×1.0):
   `1.0 × 18 × (100 / 105) = 17.14…` → **17**
2. **Elemental skill** — Urashima L1 `tidal_slash` (power 1.35, water) vs Salt Crab (DEF 5, physical → water strong ×1.25):
   `1.35 × 18 × (100 / 105) = 23.14 → × 1.25 = 28.93` → **28**
3. **Pierce** — Roku L6 (ATK 22 + `harpoon_rod` +6 = 28) `harpoon_drive` (power 1.5, `pierce_def` 0.5) vs Palace Sentinel (DEF 14 → effective 7; physical vs physical ×1.0):
   `1.5 × 28 × (100 / 107) = 39.25` → **39**
4. **Magic + enemy override** — Yuzu L7 (MAG 26) `purify` (power 1.2, spirit) vs Palace Sentinel (RES 10, `spirit_weakness` 1.5 overrides matrix):
   `1.2 × 26 × (100 / 110) = 28.36 → × 1.5 = 42.54` → **42**
5. **Defend** — Tide Keeper `tide_lament` (power 1.5, MAG 20, water) vs defending Urashima L10 (RES 18; water vs water ×0.75):
   `1.5 × 20 × (100 / 118) = 25.42 → × 0.75 = 19.06 → × 0.5 = 9.53` → **9**

---
