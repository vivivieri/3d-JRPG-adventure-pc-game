---
id: dialogue-combat-rewards
type: reference
phase: [1, 5]
audience: [builder, visual]
status: active
authority: ui
tokens_est: 480
summary: "Dialogue, combat, rewards, choice, game over"
---
# UI/UX Flow — Dialogue, combat, rewards, choice, game over

**Hub:** [`UI_UX_FLOW.md`](../UI_UX_FLOW.md)

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
