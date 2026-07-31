---
id: quests-dialogue
type: reference
audience: [architect, narrative, builder]
status: active
authority: engineering
tokens_est: 387
summary: "Stages use `completion: { 'flag': '...' }` or `{ 'all_flags': [...] }`."
---
# Data — Story Spine — Quests + dialogue

**Hub:** [`story_spine.md`](../story_spine.md)

## 5. Quest data model (5 quests = 3 acts)

| Quest | Story question | Completes |
|-------|----------------|-----------|
| `the_return` | What happened to home? | Meet Roku |
| `echoes_at_torii` | Who waits at the shrine? | Defeat Shore Wraith |
| `depths_of_guilt` | Can the dead forgive? | Reach the palace gate (`gate_reached`) |
| `palace_gate` | What was stolen? | Defeat Sentinel |
| `the_tide_answer` | What do you owe the living? | See the ending (`game_completed`) |

Stages use `completion: { "flag": "..." }` or `{ "all_flags": [...] }`.

---


## 7. Dialogue structure

One file per chapter; scenes reference story IDs.

```json
{
  "scene_id": "SC-03",
  "lines": [{ "speaker": "yuzu", "text": { "en": "...", "ja": "...", "zh": "...", "zh-Hant": "..." } }],
  "on_complete": {
    "set_flags": ["met_yuzu_spirit"],
    "start_quest": "echoes_at_torii"
  }
}
```

**Choices** (SC-13, SC-16): add `choices[]` with `set_flags` per option. SC-16 sets `"choice_confirm": true` — UI shows two-step confirm per `ENDING_DESIGN.md` §2 before applying `ending_chosen`. SC-16 choices may include `subtext` (default) and optional `subtext_warm` + `subtext_warm_requires_flags` for `mirror_choice` flavor (`ENDING_DESIGN.md` §4).

---
