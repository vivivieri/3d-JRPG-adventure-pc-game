---
id: status-limit-intent
type: reference
audience: [builder, builder_combat, qa]
phase: [2, 3]
status: active
authority: gameplay
tokens_est: 763
summary: "Combat Systems — Status, limit gauge, enemy intent — Potency unit: buff/debuff `potency` is a flat stat delta fed into the damage formulas"
---
# Combat Systems — Status, limit gauge, enemy intent

**Hub:** [`COMBAT_SYSTEMS.md`](../COMBAT_SYSTEMS.md)

## When to read

Use **Combat Systems — Status, limit gauge, enemy intent** (roles: builder, builder_combat, qa) when you need this reference during the current task Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [4. Status effects](#4-status-effects)
- [5. Limit gauge](#5-limit-gauge)
- [6. Enemy intent system](#6-enemy-intent-system)


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
| Boss entry | **All party gauges reset to 0** when a `boss: true` encounter starts (SC-09, SC-14, SC-15) |
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
