---
id: automate-vs-human
type: how-to
phase: [1, 5]
audience: [audio, qa]
status: active
authority: audio
tokens_est: 274
summary: "run multi-LLM jury on every footstep SFX or every locale variant — cost/noise too high. Gate locale for VO jury: **`en`** (all locales still get technical lint"
---
# Audio QA — Automate Layers — Automate vs human

**Hub:** [`automate_layers.md`](../automate_layers.md)

## When to read

Use **Audio QA — Automate Layers — Automate vs human** (roles: audio, qa) when executing this procedure Jump to a section below instead of reading end-to-end (1 sections).



## 1. What to automate vs human

| Automate (objective) | Human L6 (subjective) |
|----------------------|------------------------|
| File exists, correct name | Loop feel with dialogue ducking |
| Ogg 44.1 kHz, not clipped | Boss tension vs difficulty |
| LUFS / true peak targets | Ending emotional landing |
| Duration in expected range | Zone crossfade taste |
| Not dev procedural placeholder on ship | Controller + mix comfort |
| Hero BGM mood (LLM jury) | P0 VO performance + script semantics (LLM jury, `en` gate) |
| P0 VO duration / loudness / locale paths | Subtitle timing + duck mix in-engine |

**Do not** run multi-LLM jury on every footstep SFX or every locale variant — cost/noise too high. Gate locale for VO jury: **`en`** (all locales still get technical lint at M5 ship).

---
