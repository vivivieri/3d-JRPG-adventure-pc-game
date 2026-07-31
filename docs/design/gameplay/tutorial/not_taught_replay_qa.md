---
id: not-taught-replay-qa
type: reference
phase: [2, 3]
audience: [narrative, builder, flow]
status: active
authority: gameplay
tokens_est: 376
summary: "Tutorial Design — Not taught, replay, QA — - Speed initiative order math"
---
# Tutorial Design — Not taught, replay, QA

**Hub:** [`TUTORIAL_DESIGN.md`](../TUTORIAL_DESIGN.md)

## When to read

Use **Tutorial Design — Not taught, replay, QA** (roles: narrative, builder, flow) when you need this reference during the current task Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [6. What we deliberately do NOT tutorialize](#6-what-we-deliberately-do-not-tutorialize)
- [7. Replay behavior](#7-replay-behavior)
- [8. QA checklist](#8-qa-checklist)


## 6. What we deliberately do NOT tutorialize

- Speed initiative order math
- Status effect stacking (see `COMBAT_SYSTEMS.md` — learn by play)
- Hard mode (menu description only)
- Ending choice (SC-16 — no timer, no hint toward "correct" ending)

---


## 7. Replay behavior

| Flag | Where stored | Replay behavior |
|------|--------------|-----------------|
| `prologue_seen` | `profile_meta.json` (cross-run) | Skip prologue offered on every later run |
| `tutorial_*` | run save slot | Suppressed within a run; **reset on New Game** (prompts reshow) |
| `game_completed_once` | `profile_meta.json` (cross-run) | All tutorials auto-skipped on later runs; optional "Hints" in settings |

---


## 8. QA checklist

- [ ] New player reaches SC-05 combat without reading a manual
- [ ] Intent UI understood by 90% playtesters without extra text
- [ ] Shop tutorial does not trap player in UI
- [ ] All tutorial strings exist in en / ja / zh / zh-Hant
- [ ] No tutorial prompt during SC-16 choice
