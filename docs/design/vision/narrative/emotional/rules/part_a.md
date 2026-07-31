---
id: part-a
type: reference
audience: [narrative]
status: active
authority: vision
tokens_est: 569
summary: "Narrative — Project Emotional Rules (A)"
---
# Narrative — Project Emotional Rules — Narrative — Project Emotional Rules (A)

**Hub:** [`project_rules.md`](../project_rules.md)

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
