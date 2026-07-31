---
id: field-puzzle-ui
type: reference
phase: [2, 3]
audience: [builder, visual, qa]
status: active
authority: gameplay
tokens_est: 628
summary: "Game Feel — Field, puzzle, UI feedback — Camera: Orbit smooth; no shake in field except optional boss orbit SC-15 (`screen_shake` setting)."
---
# Game Feel — Field, puzzle, UI feedback

**Hub:** [`GAME_FEEL.md`](../GAME_FEEL.md)

## When to read

Use **Game Feel — Field, puzzle, UI feedback** (roles: builder, visual, qa) when you need this reference during the current task Jump to a section below instead of reading end-to-end (6 sections).

## Jump to

- [3. Field exploration feedback](#3-field-exploration-feedback)
- [Interaction](#interaction)
- [Movement](#movement)
- [Quest & objectives](#quest-objectives)
- [4. Puzzle feedback (SC-07)](#4-puzzle-feedback-sc-07)
- [5. UI & menu feedback](#5-ui-menu-feedback)


## 3. Field exploration feedback

### Interaction

| Action | Feedback |
|--------|----------|
| Enter interact range | Prompt "E — Investigate" (localized) |
| Interact | Brief highlight pulse on object |
| Dialogue start | Soft camera nudge toward speaker |
| Zone transition | 1.5 s fade + BGM crossfade |

### Movement

| Surface | Footstep | Notes |
|---------|----------|-------|
| Sand | `sfx_footstep_sand` | Beach, village paths |
| Wood | `sfx_footstep_wood` | Pier, shack |
| Wet | `sfx_footstep_wet` | Puddles, caves |
| Marble | `sfx_footstep_marble` | Palace |

**Camera:** Orbit smooth; no shake in field except optional boss orbit SC-15 (`screen_shake` setting).

### Quest & objectives

| Type | HUD feedback |
|------|--------------|
| Active quest | Top-right compact tracker; stage text updates |
| New quest | Banner 2 s + quest log ping |
| Stage complete | Checkmark + subtle SFX |
| Soft gate (village) | Pointer toward torii after 2 inspects — **not** hard block |

**SC-02:** Player can reach torii without all inspects; Q1 stage 1 encourages 3 points.

---


## 4. Puzzle feedback (SC-07)

| Event | Feedback |
|-------|----------|
| Switch toggle | Stone grind + water rise 2 s |
| HIGH state | Louder drip ambient |
| Latch open | Metallic clang + quest complete |
| Hint 3 min | Quest log text only — **no dialogue** |
| Hint 5 min | Switch glow pulse + chime |

Silence is intentional — see `NARRATIVE_WRITING_GUIDE.md` §4.

---


## 5. UI & menu feedback

| Action | Feedback |
|--------|----------|
| Confirm | `sfx_ui_confirm` |
| Cancel | `sfx_ui_cancel` |
| Item get | `sfx_ui_item_get` + icon fly to HUD |
| Equip | `sfx_ui_equip` + stat delta flash |
| Save | `sfx_ui_save` + "Saved" toast 1.5 s |
| Invalid | `sfx_ui_invalid` + grey flash |
| Tab open | Movement paused; `sfx_ui_menu_open` |

**Typewriter:** 40 CPS Normal (`SETTINGS_ACCESSIBILITY.md`); speaker nameplate always visible.

---
