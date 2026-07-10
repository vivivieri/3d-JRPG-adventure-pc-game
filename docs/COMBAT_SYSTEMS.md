# Tides of Urashima — Combat Systems Bible

**Version:** 1.0 (Pre-build)  
**Cross-refs:** `docs/GDD.md` §7, `docs/SKILLS_BIBLE.md`, `docs/BOSS_DESIGNS.md`

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

| Element | Color | Strong vs | Weak vs | Resists |
|---------|-------|-----------|---------|---------|
| **Water** | Teal | Physical (soft) | Spirit (soft) | Water |
| **Spirit** | Cyan-gold | Palace lacquer (Sentinel) | — | Spirit |
| **Physical** | White | — | Spirit armor | Physical |

**Damage modifier:**

| Matchup | Multiplier |
|---------|------------|
| Strong | ×1.25 |
| Neutral | ×1.0 |
| Weak | ×0.75 |
| Immune | ×0 (no bosses immune v1) |

**Sentinel special:** Spirit skills deal ×1.5 (tutorial moment for Yuzu).

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

**Physical damage:** `power × ATK × (100 / (100 + DEF))`  
**Magic damage:** `power × MAG × (100 / (100 + RES))`  
**Defend:** Incoming damage ×0.5 this turn  
**Attack (basic):** `1.0 × ATK`, physical

---

## 4. Status effects

| Status | Effect | Duration | Stack | Cleanse |
|--------|--------|----------|-------|---------|
| **Poison** | 5% max HP damage at round end | 3 turns | Refresh | `coral_antidote`, Sacred Mend |
| **Regen** | 8% max HP heal at round end | 3 turns | No stack | — |
| **Stun** | Skip turn | 1 turn | No | Bosses: 50% resist |
| **Def Up** | +DEF potency | 3 turns | Add potency cap +6 | — |
| **Def Down** | -DEF potency | 2 turns | Refresh | Sacred Mend |
| **SPD Down** | -SPD | 2 turns | Refresh | — |

**Tick order:** Poison → Regen → Duration decrement  
**UI:** Icons under HP bar; turns remaining as pips

---

## 5. Limit gauge

| Rule | Value |
|------|-------|
| Max | 100% |
| Gain dealt | +8% per 10 damage dealt |
| Gain taken | +5% per 10 damage taken |
| Use | Once per battle per character |
| Reset | Empty after limit skill |
| Overfill | No |

**Party:** Each member has own gauge; only active character's limit usable on their turn.

| Character | Limit skill | ID |
|-----------|-------------|-----|
| Urashima | Box Unbound | `box_unbound` |
| Yuzu | Last Prayer | `last_prayer` |
| Roku | Depth Charge | `depth_charge` |

---

## 6. Enemy intent system

See `BOSS_DESIGNS.md` for bosses. Normal enemies:

| Intent | Meaning |
|--------|---------|
| Sword | Physical attack incoming |
| Skull | High damage or debuff |
| Sparkles | Spirit attack |
| Waves | Water AoE |

**Delay:** Normal mode — show next turn. Hard mode — phase 2+ bosses same-turn.

---

## 7. Party rules

| Rule | Detail |
|------|--------|
| Active size | 3 |
| Bench | None v1 |
| Swap mid-fight | No |
| KO | Character cannot act; 0 HP |
| Party wipe | All 3 at 0 HP → Game Over |
| Revive | No revive skills v1; use salves before KO |

---

## 8. XP & level up

- XP on battle end (win)
- Level up: full HP/MP restore + skill unlock check
- Level up UI: brief banner + fanfare; pause combat flow in field only

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
| Intent preview | Yes (boss P2+ except Hard) | Phase 2+ hidden |
| XP | 100% | 110% |

---

## 11. QA checklist

- [ ] Defend reduces damage ~50%
- [ ] Spirit skills noticeably stronger vs Sentinel
- [ ] Poison kill rare on Normal
- [ ] Limit once per fight enforced
- [ ] Escape blocked on all bosses
