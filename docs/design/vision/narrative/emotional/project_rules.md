---
id: project-rules
type: reference
phase: [1, 6]
audience: [narrative]
status: active
authority: vision
tokens_est: 1065
summary: "Project emotional rules"
---
# Narrative — Emotional Rules — Project emotional rules

**Hub:** [`emotional_rules.md`](../emotional_rules.md)

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
