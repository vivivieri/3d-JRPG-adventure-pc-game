---
id: external-steals
type: reference
phase: [1, 6]
audience: [narrative]
status: active
authority: vision
tokens_est: 1099
summary: "Purpose: Actionable patterns from acclaimed JRPG stories — adapted to a 2–3 hour scope."
---
# Narrative — Emotional Rules — External JRPG steals

**Hub:** [`emotional_rules.md`](../emotional_rules.md)

## When to read

Use **Narrative — Emotional Rules — External JRPG steals** (roles: narrative) when you need this reference during the current task Jump to a section below instead of reading end-to-end (6 sections).

## Jump to

- [12. Narrative reference steals (external JRPGs)](#12-narrative-reference-steals-external-jrpgs)
- [What we borrow](#what-we-borrow)
- [What we do not borrow](#what-we-do-not-borrow)
- [Five ship checklist items (writers + combat)](#five-ship-checklist-items-writers-combat)
- [Companion coping (one line each, optional barks)](#companion-coping-one-line-each-optional-barks)
- [Density gate (optimized application)](#density-gate-optimized-application)


## 12. Narrative reference steals (external JRPGs)

**Purpose:** Actionable patterns from acclaimed JRPG stories — adapted to a **2–3 hour** scope.
**Source note:** Curated from comparative JRPG storytelling discourse (e.g. Ni no Kuni, Trails, Xenoblade 3, FFX, Expedition 33, FF Tactics, Persona, 13 Sentinels, Metaphor, Star Ocean 2).
**Scope rule:** Steal **emotion and structure**, not runtime length, school sims, or bright Ghibli banter (`ART_DIRECTION.md`).

### What we borrow

| Reference | Steal | Ship in v1 |
|-----------|-------|------------|
| **Ni no Kuni** | Grief externalized as fantasy; healing = learning to **carry** loss | Box glow states, spirits in objects, endings don't "fix" death |
| **Trails in the Sky** | Hub feels **lived-in**; small inspectables earn the ending | Ruined village inspectables (`ACH_EMPTY_HOME`), Roku shop as place |
| **Xenoblade 3 / Expedition 33** | Bonds matter under **inevitable** time; small wins feel huge | One quiet beat per act; Tide Keeper clock motif; no false cheer after bosses |
| **FFX** | **Outsider** learns a broken world; intimate pilgrimage | Urashima returns wrong; Yuzu dignity; village → caves → palace → choice |
| **FF Tactics** | History is **contested**; no clean heroes | Lore entries slightly contradict; gallery has no single "true" history |
| **Persona 5** | Agency through **empathy**; fight harm people feel, not abstract evil | Bosses as emotional facets (`BOSS_DESIGNS.md` §1) |
| **13 Sentinels** (lite) | Mid-game **reframe** reshapes earlier lines | SC-11 flashback + `knows_box_truth` retone SC-04/SC-11 callbacks |
| **Metaphor** | Companions as **philosophies**, not archetypes | Three endings = three worldviews — equally valid (`ENDING_DESIGN.md`) |
| **Star Ocean 2** (lite) | Different lenses on same theme | `mirror_choice` (SC-13) flavors SC-16 subtext on replay |

### What we do not borrow

| Pattern | Why |
|---------|-----|
| Dozens-of-hours slow burn only | Density over padding — `PACING_CHART.md` |
| Bright whimsy / chibi comedy | Muted coastal decay; men 20–30 tone |
| Shock twists for shock value | Earned emotion; box truth foreshadowed |
| "True ending" or morality score | Three endings, no UI judgment |
| Full multi-POV mystery | One reframe beat (SC-11), not 13 parallel arcs |

### Five ship checklist items (writers + combat)

1. **Boss bark** ties intent to emotional facet (Wraith = guilt, Sentinel = frozen duty, Keeper = erase-pain temptation).
2. **Hub inspectable** has one line of life before Urashima speaks (Trails-style).
3. **One non-combat quiet beat** per act — bonds under time pressure (no quest log pop).
4. **SC-11 / box truth** changes read of at least one earlier line (13 Sentinels lite).
5. **Ending gallery** copy presents three philosophies — no "best" ending badge.

### Companion coping (one line each, optional barks)

| Character | Coping style | When to show |
|-----------|--------------|--------------|
| Urashima | Escape → accountability | SC-02 slouch → SC-16 straight posture |
| Yuzu | Ritual / remembrance | Shrine lines, Spirit skills |
| Roku | Blunt duty, shop pragmatism | SC-04 warning, post-wraith restock |

Hard mode is **mechanical mastery only** — not a secret fourth ending (`REPLAY_DESIGN.md` §6).

### Density gate (optimized application)

Do not apply every §12 pattern everywhere. Use the **decision tree + ship budgets** in `docs/design/vision/NARRATIVE_DENSITY.md` and enforce with:

```bash
python3 tools/validate_narrative_density.py   # L0_narrative_density
```

Budgets live in `game/data/narrative/narrative_density.json`.
