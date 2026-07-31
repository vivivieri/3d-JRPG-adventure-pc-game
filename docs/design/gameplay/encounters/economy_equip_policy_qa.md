---
id: economy-equip-policy-qa
type: reference
phase: [2, 3]
audience: [builder, builder_combat, qa]
status: active
authority: gameplay
tokens_est: 718
summary: "Economy, equipment, limit, hard, random, QA"
---
# Encounter Table — Economy, equipment, limit, hard, random, QA

**Hub:** [`ENCOUNTER_TABLE.md`](../ENCOUNTER_TABLE.md)

## 7. Economy pacing

**Currency:** Shell coins (環貝)

| Source | Amount |
|--------|--------|
| Per trash fight | 10–24 |
| Per boss | 45–100 |
| Q2 quest reward | 50 |
| Material sales (optional) | ~20–40 |
| **Expected total (pre-Keeper)** | ~225–280 coins |

### Roku's shop (`roku_shack`)

Available after SC-04; restocks after SC-09. **Full catalog:** `docs/design/gameplay/ITEMS_AND_ECONOMY.md` §7.

| Item ID | Price | Stock | Notes |
|---------|-------|-------|-------|
| `sea_salve` | 40 | ∞ | Heal 80 HP |
| `coral_antidote` | 30 | ∞ | Cure poison |
| `spirit_tonic` | 50 | ∞ | Restore 25 MP |
| `shell_charm` | 80 | 1 | +2 DEF charm |
| Skill scrolls | 200 | 1 each | `returning_wave` (Urashima), `torii_ward` (Yuzu) — early unlocks |

**Design intent:** Player can afford several salves + one charm, OR save for one 200-coin scroll,
on the main path without grind (see `PROGRESSION_TUNING.md` §8 affordance table).

---


## 8. Equipment progression

| Slot | Act I | Act II | Act III |
|------|-------|--------|---------|
| Weapon | `fisher_katana` (start) | `tide_cut_saber` (chest SC-07) | `palace_edge` (Sentinel drop) |
| Armor | `worn_haori` | `cave_wet_coat` (shop) | — |
| Charm | — | `shell_charm` (shop) | `spirit_bell` (lore `sailor_charm`) |

Canonical IDs: `docs/design/gameplay/ITEMS_AND_ECONOMY.md` §3.

---


## 9. Limit gauge tutorial

| When | Trigger |
|------|---------|
| SC-05 | First combat; gauge visible but not required |
| SC-09 | Boss at 50% HP — prompt: "Limit Ready" if gauge full |
| SC-15 | Phase 3 — encourage `box_unbound` (Urashima limit) |

**Fill rate:** 8% per 10 damage dealt, 5% per 10 damage taken.

---


## 10. Hard mode encounter deltas

Enable via settings menu (`hard_mode: true`).

| Change | Detail |
|--------|--------|
| Enemy HP | +15% |
| Enemy ATK | +10% |
| Intent delay | 0 on phase 2+ bosses |
| XP | +10% |
| Drops | Same |

**Audience:** Men 20–30 mastery optional — not required for endings.

---


## 11. Random encounter policy (v1)

**None.** All encounters are hand-placed triggers tied to storyboard scenes. This keeps 2–3 hour scope tight and supports authored environment composition (no combat in shrine hub).

Post-launch optional: 1 random encounter table in caves only.

---


## 12. QA checklist

- [ ] Main path completable at level 8 without optional fights
- [ ] Shop prices allow comfortable potion stock
- [ ] No soft-lock if player spends all coins before palace
- [ ] Yuzu present for Sentinel Spirit tutorial
- [ ] Solo Shore Wraith tuned (see `BOSS_DESIGNS.md`)
