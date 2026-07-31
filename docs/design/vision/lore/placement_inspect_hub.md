---
id: placement-inspect-hub
type: reference
phase: [1, 6]
audience: [narrative, builder, visual]
status: active
authority: vision
tokens_est: 526
summary: "Placement map, inspect vs lore, hub emptiness"
---
# Lore & Environmental Story — Placement map, inspect vs lore, hub emptiness

**Hub:** [`LORE_AND_ENVIRONMENTAL_STORY.md`](../LORE_AND_ENVIRONMENTAL_STORY.md)

## When to read

Use **Lore & Environmental Story — Placement map, inspect vs lore, hub emptiness** (roles: narrative, builder, visual) when you need this reference during the current task Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [4. Placement map](#4-placement-map)
- [5. Inspect scenes vs lore (village)](#5-inspect-scenes-vs-lore-village)
- [6. Hub emptiness (by design)](#6-hub-emptiness-by-design)


## 4. Placement map

From `lore_placements.json` + zone kits:

| Lore ID | Zone | Near landmark | Act |
|---------|------|---------------|-----|
| `fishing_ledger` | Village | Near pier / ledger prop | I |
| `festival_banner` | Village | Festival grounds (near SC-02-BANNER inspect) | I |
| `yuzu_prayer` | Village | Cracked torii (`SC-03` area) | I |
| `roku_dive_log` | Village | Roku shack exterior | I |
| `cave_inscription` | Caves | Mid-path wall | II |
| `sailor_charm` | Caves | Deep path before boss branch | II |
| `palace_seal` | Palace gate | Exterior walkway | III |
| `otohime_letter` | Palace gate | Interior antechamber | III |

**Visual:** Lore objects use subtle cyan interact glow (`ART_DIRECTION.md` cave palette).

---


## 5. Inspect scenes vs lore (village)

| Story beat | Inspect dialogue | Related lore |
|------------|------------------|--------------|
| Rotting banner | `SC-02-BANNER` | `festival_banner` |
| Child sandal | `SC-02-SANDAL` | — |
| Choked well (save) | `SC-02-WELL` | — |
| Torii spirit | `SC-03` | `yuzu_prayer` |

Player may hit inspect first, find lore later — both valid.

---


## 6. Hub emptiness (by design)

| Choice | Rationale |
|--------|-----------|
| No living villagers | Time took them; spirits remain |
| Ambient cats/dogs | Silhouette life only (`CHARACTER_BIBLE.md` §7) |
| Wind + rot | Primary "NPC" in Act I |
| Roku only elder | Living witness; anchor |

**Do not add** chatty town NPCs in v1 — breaks dread (`PACING_CHART.md`).

---
