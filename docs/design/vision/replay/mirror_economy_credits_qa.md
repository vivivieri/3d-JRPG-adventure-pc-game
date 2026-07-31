---
id: mirror-economy-credits-qa
type: reference
phase: [1, 6]
audience: [narrative, flow]
status: active
authority: vision
tokens_est: 481
summary: "Flavor only — `mirror_choice` flag adjusts SC-16 subtext warmth. All three endings remain available every run."
---
# Replay Design — Mirror, economy, credits, backlog, QA

**Hub:** [`REPLAY_DESIGN.md`](../REPLAY_DESIGN.md)

## When to read

Use **Replay Design — Mirror, economy, credits, backlog, QA** (roles: narrative, flow) when you need this reference during the current task Jump to a section below instead of reading end-to-end (5 sections).

## Jump to

- [7. SC-13 mirror choice (replay note)](#7-sc-13-mirror-choice-replay-note)
- [8. Economy on replay](#8-economy-on-replay)
- [9. Credits & post-game](#9-credits-post-game)
- [10. Post-v1 backlog (not ship)](#10-post-v1-backlog-not-ship)
- [11. QA checklist](#11-qa-checklist)


## 7. SC-13 mirror choice (replay note)

Flavor only — `mirror_choice` flag adjusts SC-16 subtext warmth. All three endings remain available every run.

Encourage different SC-13 answers across replays for subtle SC-16 copy variation.

---


## 8. Economy on replay

Player knows shop locations and puzzle solution — second run faster. Economy unchanged; no inflation.

Optional fights still optional; speedrun path ~90 min possible (not supported officially).

---


## 9. Credits & post-game

| After credits | Result |
|---------------|--------|
| Return to title | `game_completed` set |
| Save slot | Shows ending icon (Rewind / Anchor / Drift) |
| Gallery | Unlocks achieved endings |
| New Game | Fresh run |

**Credits tag:** "You chose: [ending]" — small text (`ENDING_DESIGN.md`).

---


## 10. Post-v1 backlog (not ship)

| Feature | Status |
|---------|--------|
| NG+ with stat carry | Cut |
| Chapter select | Cut |
| New Game+ items | Cut |
| Random cave encounters | Post-launch optional |

---


## 11. QA checklist

- [ ] 3 separate runs reach 3 different endings
- [ ] Gallery updates after each first unlock
- [ ] Prologue skip works on run 2+
- [ ] Hard mode applies on next combat after toggle
- [ ] No stat carry between New Games
- [ ] Credits ending tag correct per choice
