# Tides of Urashima — Ending Design

**Version:** 1.0 (Pre-build)
**Cross-refs:** `docs/vision/GDD.md` §10, `docs/vision/STORYBOARD.md` SC-16–17, `docs/ui/CINEMATICS.md`, `docs/vision/REPLAY_DESIGN.md`

---

## 1. Design intent

The three endings are **equally valid**. No "true" ending. No achievement for "best" choice.

**Player question at SC-16:** *Who pays for stolen time — the past, the land, or yourself?*

---

## 2. Choice gate (SC-16)

**Trigger:** Tide Keeper at ≤10% HP → combat freeze → `tide_keeper_phase3` flag
**Timer:** None
**Music:** Fade to near-silence
**Input lock:** Only choice UI active

### Choice UI copy

| Option | ID | Button label (EN) | Subtext (EN) |
|--------|-----|-------------------|--------------|
| **Rewind** | `rewind` | Open the box | Return the stolen years. The village lives — you may not. |
| **Anchor** | `anchor` | Break the box | Bind the spirits to this shore. Begin again, scarred but real. |
| **Drift** | `drift` | Walk into the tide | Refuse the bargain. Let the sea keep its secrets. |

**JA / ZH:** Localize with equal line count; subtext may wrap 2 lines max.

**Confirm:** Two-step — select → "Are you certain?" → Confirm / Go back. Data: `chapter_01.json` SC-16 sets `"choice_confirm": true`; `DialogueRunner` / choice UI must not apply `ending_chosen` until confirm.

---

## 3. Ending outcomes

### Rewind (`ending_rewind` — SC-17a)

| Field | Detail |
|-------|--------|
| **Action** | Urashima opens lacquer box; light floods ruins |
| **World** | Village restored — festival, lanterns, crowd |
| **Urashima** | Dissolves at crowd edge; Yuzu feels breeze |
| **Roku** | Not seen (implied living world without him as spirit) |
| **Tone** | Bittersweet — gift costs self |
| **Theme** | Nostalgia has a price |
| **Steam achievement** | `ENDING_REWIND` |

### Anchor (`ending_anchor` — SC-17b)

| Field | Detail |
|-------|--------|
| **Action** | Urashima shatters box; spirit light scatters into soil |
| **World** | Dawn shore; 3 rebuilders; sapling planted |
| **Urashima** | Stays — visibly older, sitting on driftwood |
| **Yuzu** | Fades into land with other spirits (peace) |
| **Roku** | Plants sapling; speaks one line: "Slow growth. Honest tide." |
| **Tone** | Hopeful — imperfect future |
| **Theme** | Accountability over escape |
| **Steam achievement** | `ENDING_ANCHOR` |

### Drift (`ending_drift` — SC-17c)

| Field | Detail |
|-------|--------|
| **Action** | Urashima rows away; box unopened on boat |
| **World** | Endless sea; palace glimmers below |
| **Urashima** | Silhouette toward horizon |
| **Otohime** | Underwater glimpse only — no dialogue |
| **Tone** | Tragic open cycle |
| **Theme** | Refusal — paradise tempts again |
| **Steam achievement** | `ENDING_DRIFT` |

---

## 4. SC-13 mirror choice (recorded, low branch)

**Scene:** Roku reveals box truth
**Dialogue choice:** "I would open it" / "I would break it" / "I don't know yet"

| Choice | Flag | Effect |
|--------|------|--------|
| Open | `mirror_choice=open` | SC-16 Rewind subtext slightly warmer (1 line variant) |
| Break | `mirror_choice=break` | SC-16 Anchor subtext slightly warmer |
| Don't know | `mirror_choice=unknown` | Default subtext |

**Does NOT lock or disable any ending.** Flavor only.

---

## 5. Post-choice boss resolution

After choice confirmed:
1. Tide Keeper speaks 1 line reacting to choice
2. Urashima uses scripted `Last Mercy` (cosmetic, 1 turn)
3. Keeper dissolves; no additional combat
4. Fade to ending scene (SC-17a/b/c)

---

## 6. Credits

**All endings:** Roll credits after cinematic (60–90s)

| Section | Content |
|---------|---------|
| Dedicated to | "Those who returned too late." |
| Story | Adapted from Urashima Tarō (public domain) |
| Engine | Godot MIT |
| Fonts | Noto OFL |
| Audio/Art | Per `docs/compliance/COMPLIANCE_REPORT.md` |
| Ending tag | "You chose: [Rewind/Anchor/Drift]" — small text |

**After credits:** Return to title. `game_completed` set. Save slot shows ending icon.

---

## 7. Replay & meta

See **`docs/vision/REPLAY_DESIGN.md`** for full replay, gallery, and Hard mode guidance.

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

See `docs/gameplay/ACHIEVEMENTS.md`. Ending achievements are **not** hidden.

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
