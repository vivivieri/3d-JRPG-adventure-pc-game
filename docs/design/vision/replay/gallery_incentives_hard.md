---
id: gallery-incentives-hard
type: reference
phase: [1, 6]
audience: [narrative, flow]
status: active
authority: vision
tokens_est: 343
summary: "Gallery, incentives, hard mode"
---
# Replay Design — Gallery, incentives, hard mode

**Hub:** [`REPLAY_DESIGN.md`](../REPLAY_DESIGN.md)

## 4. Ending gallery

**Unlock:** Title menu after `game_completed` once.

| Slot | Shows | Locked state |
|------|-------|--------------|
| Rewind | Festival silhouette | Grey until SC-17a seen |
| Anchor | Dawn shore | Grey until SC-17b seen |
| Drift | Boat horizon | Grey until SC-17c seen |

**Behavior:**
- View cinematic replay (no combat)
- No text spoilers before unlock
- No "recommended" ending badge

---


## 5. Incentives to replay

| Incentive | Type |
|-----------|------|
| See other 2 endings | Narrative |
| `ACH_ALL_ENDINGS` | Achievement |
| `ACH_LORE_COMPLETE` | Optional first run |
| Hard mode clear | Skill / achievement optional |
| Gallery completion | 3/3 slots filled |

**Not used:** Missable weapons, exclusive NG+ gear, ranking screen.

---


## 6. Hard mode on replay

| Setting | When to suggest |
|---------|-----------------|
| `hard_mode` | After first Normal clear OR anytime in settings |

Hard changes (`PROGRESSION_TUNING.md` §6): +15% HP, +10% ATK, hidden boss intents phase 2+.

**Achievements:** Hard clear optional — not required for `game_completed`.

---
