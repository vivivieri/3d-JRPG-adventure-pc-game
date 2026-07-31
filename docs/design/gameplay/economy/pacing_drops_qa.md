---
id: pacing-drops-qa
type: reference
phase: [2, 3]
audience: [builder, builder_combat, qa]
status: active
authority: gameplay
tokens_est: 403
summary: "Pacing, drops, JSON, QA"
---
# Items & Economy — Pacing, drops, JSON, QA

**Hub:** [`ITEMS_AND_ECONOMY.md`](../ITEMS_AND_ECONOMY.md)

## 8. Economy pacing (main path)

| Milestone | Expected coins (from data) | Expected spends |
|-----------|-----------------------------|-----------------|
| Post Act I | ~10 | — |
| Post Act II (post SC-09 + Q2) | ~130–150 | salves + 1 charm |
| Pre-final boss | ~225–280 | optional equipment or scroll |

**Soft-lock prevention:** Main path grants ≥220 coins (mandatory fights + Q2) without optional fights;
consumables never required to win on Normal. SC-07 chest gives `tide_cut_saber` free.

---


## 9. Drop table summary

| Source | Coins | Items |
|--------|-------|-------|
| Salt Crab | 10 | — |
| Tide Wraith | 12 | `spirit_shard` 30% |
| Shore Wraith | 45 | — (`wraith_pearl` via encounter `enc_sc09_shore_wraith` on_win, not enemy drop) |
| Palace Sentinel | 60 | `palace_fragment` 50% (`palace_edge` via encounter `enc_sc14_sentinel` on_win) |
| Tide Keeper | 100 | `palace_fragment` 100% |

---


## 10. items.json alignment

All equipment and key item IDs listed in §3–4 are present in `game/data/items/items.json` (schema v2). Update this doc if new items are added.

---


## 11. QA checklist

- [ ] Beat game without buying anything (Normal)
- [ ] Beat game without SC-07 chest (saber optional)
- [ ] No negative coin balance
- [ ] Key items cannot be sold or discarded
- [ ] Shop prices match this doc
