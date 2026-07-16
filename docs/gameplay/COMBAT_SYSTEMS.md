# Tides of Urashima — Combat Systems Bible

**Version:** 1.0 (Pre-build)  
**Cross-refs:** `docs/vision/GDD.md` §7, `docs/gameplay/SKILLS_BIBLE.md`, `docs/gameplay/BOSS_DESIGNS.md`

---

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

## 4. Status effects

| Status | Effect | Duration | Stack | Cleanse |
|--------|--------|----------|-------|---------|
| **Poison** | 5% max HP damage at round end | 3 turns | Refresh | `coral_antidote`, Cleanse (`last_prayer`) |
| **Regen** | 8% max HP heal at round end | 3 turns | No stack | — |
| **Stun** | Skip turn | 1 turn | No | Bosses: 50% resist |
| **Def Up** | +DEF (flat, = effect `potency`) | 3 turns | Add potency, cap +6 total | — |
| **Def Down** | −DEF (flat, = effect `potency`) | 2 turns | Refresh | Cleanse (limit `last_prayer`) |
| **SPD Down** | −SPD (flat, = effect `potency`) | 2 turns | Refresh | — |
| **Taunt** | Forces enemies to target bearer; pairs with Def Up on `tide_taunt` | 2 turns | Refresh | — |

**Potency unit:** buff/debuff `potency` is a **flat stat delta** fed into the damage formulas
(e.g. Def Up potency 4 → +4 DEF). Regen/heal `potency` is **flat HP** (e.g. regen 8 → 8 HP/turn);
`heal potency 999` = full heal. Poison is the exception: 5% max HP per round-end tick.

**Tick order:** Poison → Regen → Duration decrement  
**UI:** Icons under HP bar; turns remaining as pips

---

## 5. Limit gauge

| Rule | Value |
|------|-------|
| Max | 100% |
| Gain dealt | +8% per 10 damage dealt (`floor(damage / 10) × 8`; multi-target: sum all targets' damage first) |
| Gain taken | +5% per 10 damage taken (`floor(damage / 10) × 5`) |
| Use | Once per battle per character |
| Reset | Empty after limit skill; **persists between battles** (not reset on battle end) |
| Overfill | No (clamp 100) |

**Party:** Each member has own gauge; only active character's limit usable on their turn.

| Character | Limit skill | ID |
|-----------|-------------|-----|
| Urashima | Box Unbound | `box_unbound` |
| Yuzu | Last Prayer | `last_prayer` |
| Roku | Depth Charge | `depth_charge` |

---

## 6. Enemy intent system

See `BOSS_DESIGNS.md` for bosses. Normal enemies use **data IDs** in `enemies.json` → `intent_display` and i18n keys `combat.intent.*` in `translations.csv`.

| Data ID | UI icon | Meaning |
|---------|---------|---------|
| `attack` | Sword | Physical or standard damage incoming |
| `debuff` | Skull | High damage, status, or DEF break |
| `charge` | Waves / Sparkles | Charged AoE, water burst, or spirit telegraph |

**Targeting:** While **Taunt** is active on ally X, enemy single-target actions prefer X (see §4).

**Delay:** Normal mode — show next turn. Hard mode — phase 2+ bosses same-turn.

---

## 7. Party rules

| Rule | Detail |
|------|--------|
| Active size | 3 |
| Bench | None v1 |
| Swap mid-fight | No |
| KO | Character cannot act; 0 HP |
| Party wipe | **All active party members** at 0 HP → Game Over (solo fights: Urashima alone) |
| Revive | No revive skills v1; use salves before KO |

---

## 8. XP & level up

- XP on battle end (win); **party level is shared** — one level value for the whole party, all
  members' stats derive from it (`base + growth × (level − 1)`). KO'd members still "receive" XP
  because there is no per-character XP. Joining members (Yuzu SC-10, Roku SC-12) enter at the
  current party level with all skill unlocks at or below that level already learned.
- Level up: full HP/MP restore + skill unlock check
- Level up UI: brief banner + fanfare; pause combat flow in field only
- If a queued action's target dies before resolution: single-target actions retarget the next
  living enemy (or fizzle with no MP cost if none); AoE resolves on survivors.

---

## 9. Combat UI states

```
Intro → Player turn (highlight active) → Enemy turn → ...
Win → Rewards (XP, coins, drops) → Exit
Lose → Game Over
```

**Rewards screen:** 3s auto-continue or Confirm

---

## 10. Hard mode deltas

| Parameter | Normal | Hard |
|-----------|--------|------|
| Enemy HP | 100% | 115% |
| Enemy ATK | 100% | 110% |
| Boss intent preview | 1 turn ahead, all phases | 1 turn ahead in phase 1; **hidden (same-turn)** in boss phase 2+ |
| XP | 100% | 110% |
| Tide Keeper choice gate | 10% HP | 15% HP |

---

## 11. QA checklist

- [ ] Defend reduces damage ~50%
- [ ] Spirit skills noticeably stronger vs Sentinel
- [ ] Poison kill rare on Normal
- [ ] Limit once per fight enforced
- [ ] Escape blocked on all bosses
