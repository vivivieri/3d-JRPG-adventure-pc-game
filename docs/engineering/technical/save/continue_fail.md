---
id: continue-fail
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, builder, qa]
status: active
authority: engineering
tokens_est: 464
summary: "Save & Fail States — Continue, fail states, death vs story — - Continue loads the run slot's latest autosave"
---
# Save & Fail States — Continue, fail states, death vs story

**Hub:** [`SAVE_AND_FAIL_STATES.md`](../SAVE_AND_FAIL_STATES.md)

## When to read

Use **Save & Fail States — Continue, fail states, death vs story** (roles: architect, builder, qa) when you need this reference during the current task Jump to a section below instead of reading end-to-end (5 sections).

## Jump to

- [4. Continue behavior (canonical — `ENDING_DESIGN.md` §7 and `REPLAY_DESIGN.md` §3 defer here)](#4-continue-behavior-canonical-ending_designmd-7-and-replay_designmd-3-defer-here)
- [5. Fail states](#5-fail-states)
- [Party wipe (combat)](#party-wipe-combat)
- [Soft-lock prevention](#soft-lock-prevention)
- [6. Death vs story](#6-death-vs-story)


## 4. Continue behavior (canonical — `ENDING_DESIGN.md` §7 and `REPLAY_DESIGN.md` §3 defer here)

- **Continue** loads the run slot's latest autosave
- If save corrupt: message + New Game only
- **Post-credits:** the slot is marked complete (`run_ending` set) and shows the ending icon.
  **Continue is disabled** until the player starts a New Game. Endings are revisited via the
  gallery, not by reloading pre-ending saves.

---


## 5. Fail states

### Party wipe (combat)

1. All party HP → 0
2. Defeat SFX + screen desaturate
3. Game Over screen
4. **Load Save** → last autosave (before encounter if autosave on transition — player retries from zone entry)

**Design:** Autosave before boss triggers so wipe does not lose >5 min.

### Soft-lock prevention

| Risk | Mitigation |
|------|------------|
| Out of salves | Roku shop restock; drops tuned |
| Out of MP | Spirit Tonic affordable |
| Stuck in puzzle | Hint after 3 min; see `PUZZLE_DESIGN.md` |
| Missing key item | Boss drops guaranteed |

---


## 6. Death vs story

- No permadeath
- No ironman mode v1
- Story choices irreversible **after** SC-16 confirm

---
