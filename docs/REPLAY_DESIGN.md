# Tides of Urashima — Replay Design

**Version:** 1.0 (Pre-build)  
**Cross-refs:** `docs/ENDING_DESIGN.md` §7, `docs/ACHIEVEMENTS.md`, `docs/UI_UX_FLOW.md`, `docs/PROGRESSION_TUNING.md`

Expands replay, gallery, and second-run value. **No NG+ stat carry in v1.**

---

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

## 4. Ending gallery

**Unlock:** Title menu after `game_completed` once.

| Slot | Shows | Locked state |
|------|-------|--------------|
| Rewind | Festival silhouette | Grey until SC-17a seen |
| Anchor | Dawn shore | Grey until SC-17b seen |
| Drift | Boat horizon | Grey until SC-17c seen |

**Behavior:**
- View cinematic replay (no combat)
- No text spoilers before unlock
- No "recommended" ending badge

---

## 5. Incentives to replay

| Incentive | Type |
|-----------|------|
| See other 2 endings | Narrative |
| `ACH_ALL_ENDINGS` | Achievement |
| `ACH_LORE_COMPLETE` | Optional first run |
| Hard mode clear | Skill / achievement optional |
| Gallery completion | 3/3 slots filled |

**Not used:** Missable weapons, exclusive NG+ gear, ranking screen.

---

## 6. Hard mode on replay

| Setting | When to suggest |
|---------|-----------------|
| `hard_mode` | After first Normal clear OR anytime in settings |

Hard changes (`PROGRESSION_TUNING.md` §6): +15% HP, +10% ATK, hidden boss intents phase 2+.

**Achievements:** Hard clear optional — not required for `game_completed`.

---

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
