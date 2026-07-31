---
id: dialogue-combat-rewards
type: reference
phase: [1, 5]
audience: [builder, visual]
status: active
authority: ui
tokens_est: 539
summary: "Dialogue, combat, rewards, choice, game over"
---
# UI/UX Flow — Dialogue, combat, rewards, choice, game over

**Hub:** [`UI_UX_FLOW.md`](../UI_UX_FLOW.md)

## When to read

Use **UI/UX Flow — Dialogue, combat, rewards, choice, game over** (roles: builder, visual) when you need this reference during the current task Jump to a section below instead of reading end-to-end (5 sections).

## Jump to

- [5. Dialogue box](#5-dialogue-box)
- [6. Combat UI](#6-combat-ui)
- [7. Battle rewards](#7-battle-rewards)
- [8. Choice UI (SC-16)](#8-choice-ui-sc-16)
- [9. Game Over](#9-game-over)


## 5. Dialogue box

| Field | Spec |
|-------|------|
| Position | Lower third |
| Background | `#1A1A2ECC` ink panel |
| Portrait | Left 128×128; character bust |
| Text | Typewriter 40 cps; click to advance |
| Speaker | Gold nameplate |
| Choices | Max 3; vertical list SC-13 |

**Auto-advance:** Off default; option in Settings

---


## 6. Combat UI

```
┌─────────────────────────────────────────┐
│ [Enemy intent icons]     Enemy HP bars  │
├─────────────────────────────────────────┤
│                                         │
│   Battle stage (3D arena, fixed cam)    │
│                                         │
├─────────────────────────────────────────┤
│ Party HP/MP/Limit    │ Action menu       │
│ Battle log (scroll)  │ Attack/Skill/... │
└─────────────────────────────────────────┘
```

| State | Input |
|-------|-------|
| Player turn | Menu + target select |
| Target select | Highlight valid targets; Esc back |
| Enemy turn | Input locked |
| Victory | Rewards overlay |

**Action menu order:** Attack → Skill → Item → Defend → Escape

---


## 7. Battle rewards

| Field | Display |
|-------|---------|
| XP gained | Number + bar fill |
| Shell coins | +N |
| Items | Icons if dropped |
| Level up | If applicable → skill unlock toast |

Confirm or 3s auto-advance.

---


## 8. Choice UI (SC-16)

- Full-screen dim overlay 60% black
- 3 vertical cards with label + subtext
- Cursor / gamepad default: no selection until moved
- Two-step confirm modal

---


## 9. Game Over

- Desaturate 0.5s
- "The tide claims you" (localized)
- Options: **Load Save** | **Title**

No retry-in-place v1.

---
