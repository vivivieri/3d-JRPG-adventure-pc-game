---
id: intent-choice-outcomes
type: reference
phase: [1, 6]
audience: [narrative, flow]
status: active
authority: vision
tokens_est: 815
summary: "Ending Design — Intent, choice gate, outcomes — The three endings are equally valid. No 'true' ending. No achievement for 'best' choice."
---
# Ending Design — Intent, choice gate, outcomes

**Hub:** [`ENDING_DESIGN.md`](../ENDING_DESIGN.md)

## When to read

Use **Ending Design — Intent, choice gate, outcomes** (roles: narrative, flow) when you need this reference during the current task Jump to a section below instead of reading end-to-end (7 sections).

## Jump to

- [1. Design intent](#1-design-intent)
- [2. Choice gate (SC-16)](#2-choice-gate-sc-16)
- [Choice UI copy](#choice-ui-copy)
- [3. Ending outcomes](#3-ending-outcomes)
- [Rewind (`ending_rewind` — SC-17a)](#rewind-ending_rewind-sc-17a)
- [Anchor (`ending_anchor` — SC-17b)](#anchor-ending_anchor-sc-17b)
- [Drift (`ending_drift` — SC-17c)](#drift-ending_drift-sc-17c)


## 1. Design intent

The three endings are **equally valid**. No "true" ending. No achievement for "best" choice.

**Player question at SC-16:** *Who pays for stolen time — the past, the land, or yourself?*

---


## 2. Choice gate (SC-16)

**Trigger:** Tide Keeper at ≤10% HP → combat freeze → `tide_keeper_phase3` flag
**Timer:** None
**Music:** Fade to near-silence
**Input lock:** Only choice UI active

### Choice UI copy

| Option | ID | Button label (EN) | Subtext (EN) |
|--------|-----|-------------------|--------------|
| **Rewind** | `rewind` | Open the box | Return the stolen years. The village lives — you may not. |
| **Anchor** | `anchor` | Break the box | Bind the spirits to this shore. Begin again, scarred but real. |
| **Drift** | `drift` | Walk into the tide | Refuse the bargain. Let the sea keep its secrets. |

**JA / ZH:** Localize with equal line count; subtext may wrap 2 lines max.

**Confirm:** Two-step — select → "Are you certain?" → Confirm / Go back. Data: `chapter_01.json` SC-16 sets `"choice_confirm": true`; `DialogueRunner` / choice UI must not apply `ending_chosen` until confirm.

---


## 3. Ending outcomes

### Rewind (`ending_rewind` — SC-17a)

| Field | Detail |
|-------|--------|
| **Action** | Urashima opens lacquer box; light floods ruins |
| **World** | Village restored — festival, lanterns, crowd |
| **Urashima** | Dissolves at crowd edge; Yuzu feels breeze |
| **Roku** | Not seen (implied living world without him as spirit) |
| **Tone** | Bittersweet — gift costs self |
| **Theme** | Nostalgia has a price |
| **Steam achievement** | `ENDING_REWIND` |

### Anchor (`ending_anchor` — SC-17b)

| Field | Detail |
|-------|--------|
| **Action** | Urashima shatters box; spirit light scatters into soil |
| **World** | Dawn shore; 3 rebuilders; sapling planted |
| **Urashima** | Stays — visibly older, sitting on driftwood |
| **Yuzu** | Fades into land with other spirits (peace) |
| **Roku** | Plants sapling; speaks one line: "Slow growth. Honest tide." |
| **Tone** | Hopeful — imperfect future |
| **Theme** | Accountability over escape |
| **Steam achievement** | `ENDING_ANCHOR` |

### Drift (`ending_drift` — SC-17c)

| Field | Detail |
|-------|--------|
| **Action** | Urashima rows away; box unopened on boat |
| **World** | Endless sea; palace glimmers below |
| **Urashima** | Silhouette toward horizon |
| **Otohime** | Underwater glimpse only — no dialogue |
| **Tone** | Tragic open cycle |
| **Theme** | Refusal — paradise tempts again |
| **Steam achievement** | `ENDING_DRIFT` |

---
