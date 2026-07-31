---
id: emotional-rules
type: reference
audience: [narrative]
phase: [3, 6]
status: active
authority: narrative
tokens_est: 2004
summary: "Tides of Urashima is a **2–3 hour** game. Depth comes from **restraint**, callbacks, and systems that echo theme — not from cutscene count or word count."
---
# Narrative — Emotional storytelling rules

**Hub:** [`NARRATIVE_WRITING_GUIDE.md`](../NARRATIVE_WRITING_GUIDE.md)

## 11. JRPG emotional storytelling — project rules

Tides of Urashima is a **2–3 hour** game. Depth comes from **restraint**, callbacks, and systems that echo theme — not from cutscene count or word count.

### A. Show before tell

| Technique | Where | Example |
|-----------|-------|---------|
| Inspectables before dialogue | SC-02 | Child's sandal, rotting banner — Urashima says *"Anyone...?"* after player sees emptiness |
| Zone contrast | Beach → village → caves → palace | Grey decay → biolume wonder → sterile gold void |
| Box glow states | All acts | Dim (guilt) → pulse (palace) → blinding (SC-16) — no UI tutorial needed |
| Enemy as metaphor | Combat | Salt Crab / Wraith lines reference abandonment, not random taunts |

**Rule:** If a line explains what the camera already showed, cut the line.

### B. Silence is a beat

| Scene | Silence use |
|-------|-------------|
| SC-07 | Puzzle — **no dialogue** by design |
| SC-08 | Whisper SFX bed under layered text; gaps between lines |
| SC-16 | Near-silence before choice; `sting_choice_silence` |
| SC-17 Drift | Final seconds: surf only, no BGM |

Do not fill quiet moments with narrator exposition.

### C. Callbacks (cheap, high impact)

Wire these in dialogue / barks when flags are set:

| Earlier beat | Later callback |
|--------------|----------------|
| SC-02 sandal inspect | SC-08 drowned faces — optional Urashima line |
| SC-04 Roku warning | SC-13 mirror — Roku doesn't repeat; trusts player |
| SC-11 Otohime offer | SC-16 choice subtext echoes *"stay"* without naming her |
| `mirror_choice` (SC-13) | Ending flavor line variant — not a branch |

One callback per act is enough. Avoid winking at the player.

### D. Party as emotional mirror

| Character | Story function | Writing note |
|-----------|----------------|--------------|
| Yuzu | Accusation → alliance | Fewer words over time; more weight per line |
| Roku | Grounding elder | Gravelly wisdom; never comic relief |
| Urashima | Player avatar | Act I fragments → Act III declarations (`§3`) |

**Field barks:** After `met_yuzu_spirit`, `shore_wraith_defeated`, `knows_box_truth` — swap idle barks so the world feels changed without new cutscenes.

### E. Combat as punctuation

Combat is not filler between movies. Each fight should **change the emotional temperature**:

- SC-05 tutorial: agency after dread
- SC-08 wraiths: guilt made physical — before SC-09 catharsis
- SC-14 sentinel: discipline / Yuzu shines — before final act
- SC-15 Tide Keeper: phases map to ebb → surge → stillness (choice gate)

Boss defeat lines: tragic, not triumphant. No *"You win!"* anime cadence.

### F. Endings earn their length

Endings are the **only** place to spend 60–120s of non-interactive time (`CINEMATICS.md` §8). Each must **look and sound different**:

| Ending | Visual thesis | Audio |
|--------|---------------|-------|
| Rewind | Crowd + dissolve | Bittersweet festival |
| Anchor | Dawn + sapling | Restrained hope |
| Drift | Open sea + palace below | Sparse tragedy |

No morality labels in UI copy (`ENDING_DESIGN.md`).

### G. Replay without bloat

Second run value (`REPLAY_DESIGN.md`):

- Skip SC-00 / SC-11 / SC-12 after 3s — respect player time
- Gallery unlocks ending stills — emotional recap, not lore wiki
- Hard mode: mechanical mastery, **not** secret fourth ending v1

### H. What to avoid (audience 20–30)

- Bright Ghibli banter or chibi reactions
- Long villain monologues — Tide Keeper speaks in tides, not essays
- Moral scoring (*"Anchor ending 78% good"*)
- VO assumptions — prose must read on screen (`§1`)
- Extra mid-game movies beyond SC-12 — dilutes pacing (`PACING_CHART.md`)

### I. Writer smoke test

Before shipping a scene, ask:

1. What does the player **feel** without reading dialogue?
2. Does this scene **change** a flag, relationship, or world read?
3. Could this be 30% shorter and hit harder?
4. Does music/SFX carry emotion when text is removed?

If (1) fails, add environment or camera — not more lines.

---


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
