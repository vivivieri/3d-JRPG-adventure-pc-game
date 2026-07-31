---
id: act2-act3-summary
type: reference
phase: [2, 3]
audience: [builder, builder_combat, qa]
status: active
authority: gameplay
tokens_est: 708
summary: "Post SC-10 optional (`enc_sc10_optional_wraith` — doubles as heal tutorial, `TUTORIAL_DESIGN.md` SC-10):"
---
# Encounter Table — Act II, Act III, summary

**Hub:** [`ENCOUNTER_TABLE.md`](../ENCOUNTER_TABLE.md)

## When to read

Use **Encounter Table — Act II, Act III, summary** (roles: builder, builder_combat, qa) when you need this reference during the current task Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [4. Act II — The Depths (~60 min)](#4-act-ii-the-depths-60-min)
- [5. Act III — The Tide (~30–45 min)](#5-act-iii-the-tide-3045-min)
- [6. Encounter summary](#6-encounter-summary)


## 4. Act II — The Depths (~60 min)

| # | Scene | Zone | Encounter | Type | Party | XP | Level after |
|---|-------|------|-----------|------|-------|-----|-------------|
| 2 | SC-06 | Cave entrance | Salt Crab ×1 | Scripted (avoidable) | Urashima | 30 | 2–3 |
| 3 | SC-07 area | Flooded chamber (`enc_sc07_optional_crabs`) | Salt Crab ×2 | Optional | Urashima | 60 | 3 |
| 4 | SC-08 | Deep pool | Tide Wraith ×2 | Forced | Urashima | 70 | 4 |
| 5 | SC-09 | Boss arena | **Shore Wraith** | Boss | Urashima solo | 120 | 4–5 |
| — | SC-10 | Shrine alcove | — | Yuzu joins | +party | — | 5 |

**Post SC-10 optional** (`enc_sc10_optional_wraith` — doubles as heal tutorial, `TUTORIAL_DESIGN.md` SC-10):

| # | Zone | Encounter | Type | Party | XP |
|---|------|-----------|------|-------|-----|
| 6 | Caves exit path | Tide Wraith ×1 | Optional | Urashima + Yuzu | 35 |

---


## 5. Act III — The Tide (~30–45 min)

| # | Scene | Zone | Encounter | Type | Party | XP | Level after |
|---|-------|------|-----------|------|-------|-----|-------------|
| 7 | SC-12 approach | Palace exterior | Tide Wraith ×2 | Scripted | Full party | 70 | 6 |
| 8 | SC-13 | Mirror chamber | — | Dialogue only | — | — | — |
| 9 | SC-14 | Sentinel hall | **Palace Sentinel** | Miniboss | Full party | 100 | 7 |
| 10 | SC-15 | Throne arena | **Tide Keeper** | Final boss | Full party | 250 | 8–10 |

**Gate:** SC-13 mirror dialogue sets `knows_box_truth` — required before SC-14 encounter (`enc_sc14_sentinel` `requires_flags`). `sentinel_dialogue_done` is set **after** SC-14 pre-fight dialogue, not as a gate.

**Flee policy:** `escape_allowed: true` only on optional/avoidable encounters (SC-06, SC-07, SC-10). Bosses and story-forced fights block flee (`COMBAT_SYSTEMS.md` §2).

**No fights after choice gate (SC-16).**

---


## 6. Encounter summary

| Enemy | Count (main path) | Role |
|-------|-------------------|------|
| Salt Crab | 2–4 | Tutorial + cave filler |
| Tide Wraith | 3–5 | Guilt / speed threat |
| Shore Wraith | 1 | Act II boss |
| Palace Sentinel | 1 | Spirit tutorial miniboss |
| Tide Keeper | 1 | Final boss |

**Total scripted encounters (data):** 9 in `story_encounters.json` — 6 unavoidable
(SC-05, SC-08, SC-09, SC-12, SC-14, SC-15), 1 avoidable (SC-06), 2 optional (SC-07 crabs, SC-10 wraith).

---
