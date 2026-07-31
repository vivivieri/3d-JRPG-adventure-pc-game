---
id: intent-first-newgame
type: reference
phase: [1, 6]
audience: [narrative, flow]
status: active
authority: vision
tokens_est: 446
summary: "Intent, first vs replay, New Game"
---
# Replay Design — Intent, first vs replay, New Game

**Hub:** [`REPLAY_DESIGN.md`](../REPLAY_DESIGN.md)

## 1. Design intent

| Goal | Detail |
|------|--------|
| Three endings | Equally valid; player may want all 3 |
| Replay time | 1.5–2 h second run (skips, knowledge) |
| No FOMO | No missable permanent stat boosts |
| Hard mode | Optional mastery layer |

**Player message:** *"The tide offers three answers — which debt will you pay?"* (store copy, not in-game morality score)

---


## 2. First run vs replay

| Feature | First run | Replay |
|---------|-----------|--------|
| SC-00 prologue | Full | Skippable (hold Confirm 1 s after 3 s — `prologue_seen` in profile meta) |
| Tutorials | Shown | Reshown (run flags reset) — auto-skipped entirely once `game_completed_once` in profile meta |
| Story | Full dialogue | Same |
| Combat | Normal default | Player may enable Hard |
| Lore | Discover 8 | Can re-read in gallery run |
| Ending | One chosen | One per run |

---


## 3. New Game flow

1. Title → **New Game** (overwrites `user://save_slot_0.json` — single run slot v1)
2. All **run** flags cleared; `user://profile_meta.json` (gallery, prologue skip, playtime) persists (`SAVE_AND_FAIL_STATES.md` §1)
3. `prologue_seen` (profile meta) allows prologue skip only — not other shortcuts
4. **No chapter select** v1

**Continue:** Available until credits complete. After `game_completed`, the slot shows the ending
icon and **Continue is disabled until a New Game is started** (canonical rule:
`SAVE_AND_FAIL_STATES.md` §4). Other endings are earned via replay, not save reload.

---
