---
id: replay-achievements-qa
type: reference
phase: [1, 6]
audience: [narrative, flow]
status: active
authority: vision
tokens_est: 459
summary: "Ending Design — Replay, achievements, voice notes, QA — See `docs/design/vision/REPLAY_DESIGN.md` for full replay, gallery, and Hard mode guidance."
---
# Ending Design — Replay, achievements, voice notes, QA

**Hub:** [`ENDING_DESIGN.md`](../ENDING_DESIGN.md)

## When to read

Use **Ending Design — Replay, achievements, voice notes, QA** (roles: narrative, flow) when you need this reference during the current task Jump to a section below instead of reading end-to-end (4 sections).

## Jump to

- [7. Replay & meta](#7-replay-meta)
- [8. Achievement mapping](#8-achievement-mapping)
- [9. Writer notes — voice at choice](#9-writer-notes-voice-at-choice)
- [10. QA checklist](#10-qa-checklist)


## 7. Replay & meta

See **`docs/design/vision/REPLAY_DESIGN.md`** for full replay, gallery, and Hard mode guidance.

| Feature | Design |
|---------|--------|
| **New Game** | Fresh run flags; prologue skippable (profile meta persists — `SAVE_AND_FAIL_STATES.md` §1) |
| **Continue** | Disabled after credits until New Game (`SAVE_AND_FAIL_STATES.md` §4 is canonical) |
| **Ending gallery** | Title menu after first completion — unlocks stored in `profile_meta.json`; locked endings greyed |
| **NG+** | **No** stat carry for v1 |
| **Chapter select** | **No** for v1 |

**Gallery unlock:** View any ending cinematic once achieved; no text spoilers before unlock.

---


## 8. Achievement mapping

See `docs/design/gameplay/ACHIEVEMENTS.md`. Ending achievements are **not** hidden.

---


## 9. Writer notes — voice at choice

- **Urashima:** Silent during choice UI; player projects
- **Tide Keeper:** "The tide waits. So did they."
- **No morality score** displayed
- Avoid labeling endings good/bad in UI

---


## 10. QA checklist

- [ ] All 3 endings reachable in one playthrough each (3 runs)
- [ ] Choice cannot be accidental (two-step confirm)
- [ ] No fourth option; Esc does not default-select
- [ ] Credits ending tag matches choice
- [ ] Gallery updates after each first clear
