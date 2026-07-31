---
id: party-xp-ui-qa
type: reference
audience: [builder, builder_combat, qa]
phase: [2, 3]
status: active
authority: gameplay
tokens_est: 511
summary: "Party, XP, UI, hard mode, QA"
---
# Combat Systems — Party, XP, UI, hard mode, QA

**Hub:** [`COMBAT_SYSTEMS.md`](../COMBAT_SYSTEMS.md)

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
