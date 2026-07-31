---
id: philosophy-prologue-matrix
type: reference
phase: [2, 3]
audience: [narrative, builder, flow]
status: active
authority: gameplay
tokens_est: 855
summary: "Philosophy, prologue, matrix"
---
# Tutorial Design — Philosophy, prologue, matrix

**Hub:** [`TUTORIAL_DESIGN.md`](../TUTORIAL_DESIGN.md)

## 1. Teaching philosophy

| Rule | Detail |
|------|--------|
| One new system per scene | Never stack 3 tutorials at once |
| Diegetic first | Roku / Yuzu explain; minimal meta text |
| Skippable prompts | Confirm dismisses; flag prevents repeat |
| Fail-forward | Tutorial crab cannot kill player |
| Hard mode | Does not disable tutorials on first play |

---


## 2. Prologue — SC-00 (new)

**Duration:** 45–60s (skippable after first play via `prologue_seen`)

| Beat | Visual | Teach |
|------|--------|-------|
| 1 | Black + surf SFX | Tone |
| 2 | Urashima nets wounded spirit-turtle | Story setup (GDD §2) |
| 3 | Brief palace montage (silhouette) | Dragon Palace exists |
| 4 | Otohime hands lacquer box | Box origin |
| 5 | Cut to SC-01 shore | "I thought it was three days." |

**Skip:** Hold Confirm 1s on "Skip prologue" after 3s

---


## 3. Tutorial matrix

| System | Scene | Trigger | Prompt text (EN) | Flag |
|--------|-------|---------|------------------|------|
| **Movement** | SC-01 | Spawn | "WASD to move" | `tutorial_movement_done` |
| **Camera** | SC-01 | After 5s walk | "Right-mouse drag to look · Scroll to zoom" | `tutorial_camera_done` |
| **Interact** | SC-02 | Near banner | "E — Investigate" | `tutorial_interact_done` |
| **Inspect** | SC-02 | 1st inspect | "Examine objects for clues and lore" | — |
| **Save point** | SC-02 | Near well | "Save points — interact to record progress" | `tutorial_save_done` |
| **Dialogue** | SC-03 | Torii scene start | "Space — advance dialogue" | `tutorial_dialogue_done` |
| **Shop** | SC-04 | Roku shack exit | "Roku's cache — buy supplies here (Tab → Shop)" | `tutorial_shop_done` |
| **Attack** | SC-05 | Combat turn 1 | "Attack — basic strike" | part of `tutorial_combat_done` |
| **Skill** | SC-05 | Combat turn 2 | "Skill — costs MP; stronger" | part of `tutorial_combat_done` |
| **Defend** | SC-05 | Combat turn 3 | "Defend — reduce damage this turn" | `tutorial_combat_done` |
| **Intent UI** | SC-09 | Boss turn 2 | "Enemy intent — plan around telegraphed attacks" | `tutorial_intent_done` |
| **Phase change** | SC-09 | Boss 50% HP | "Boss phase — pattern may change" | — |
| **Party heal** | SC-10 | Post-join dialogue (mandatory) | "Yuzu — Spirit Light heals allies" | `tutorial_heal_done` |
| **Limit gauge** | SC-09 or SC-15 | Gauge full | "Limit ready — devastating once-per-fight skill" | `tutorial_limit_done` |
| **Equipment** | SC-07 chest or SC-04 | First item obtained | "Tab → Equipment — arm yourself" | `tutorial_equip_done` |
| **Lore journal** | SC-02 | First lore read | "Tab → Lore — collected memories" | `tutorial_lore_done` |
| **Field menu** | SC-04 | First Tab press | "Tab — menu (items, equipment, quests, lore)" | `tutorial_menu_done` |

**Flag storage:** all `tutorial_*` flags in the table above are registered in
`game/data/story/flags.json` (set by scene spine / encounters; usable in conditions and
quest gates). The save slot's `tutorial_seen[]` array (`SAVE_AND_FAIL_STATES.md` §2) is an
optional **UI dedupe** list (suppress re-showing the same prompt text within a run) — it does
not replace story flags.

---
