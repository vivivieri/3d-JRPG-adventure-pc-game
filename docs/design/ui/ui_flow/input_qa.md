---
id: input-qa
type: reference
phase: [1, 5]
audience: [builder, visual]
status: active
authority: ui
tokens_est: 535
summary: "Keyboard/mouse, controller, QA"
---
# UI/UX Flow — Keyboard/mouse, controller, QA

**Hub:** [`UI_UX_FLOW.md`](../UI_UX_FLOW.md)

## 10. Input — keyboard & mouse

| Context | Keys |
|---------|------|
| Field move | WASD |
| Interact | E |
| Menu | Tab |
| Pause | Esc |
| Confirm | Space / Enter / LMB |
| Cancel | Esc / RMB |
| Camera | RMB drag, scroll zoom |

### Canonical InputMap action names (`project.godot`)

Use exactly these action IDs in GDScript and scene wiring — do not invent variants:

| Action ID | Keyboard | Gamepad |
|-----------|----------|---------|
| `move_left` / `move_right` / `move_forward` / `move_back` | A / D / W / S | Left stick |
| `interact` | E | A |
| `ui_accept` (built-in) | Space / Enter | A |
| `ui_cancel` (built-in) | Esc | B |
| `open_menu` | Tab | Y |
| `pause` | Esc | Start |
| `camera_orbit` | RMB (hold) | Right stick |
| `camera_zoom_in` / `camera_zoom_out` | Scroll up / down | — (auto-frame) |
| `dialogue_advance` | Space / Enter / E | A |
| `skip_hold` (prologue/cinematic skip) | Confirm held 1 s | A held 1 s |

---


## 11. Controller (Xbox layout)

**Ship target:** Full main-path playable on gamepad (M5 polish). No remapping v1.

| Action | Button |
|--------|--------|
| Move | Left stick |
| Interact | A |
| Confirm | A |
| Cancel | B |
| Menu | Y |
| Pause | Start |
| Camera | Right stick |

**Combat:** D-pad menu navigate; A confirm; B back

### SC-16 choice (gamepad)

| Rule | Detail |
|------|--------|
| Default focus | **No** option pre-selected |
| Navigate | D-pad up/down between 3 cards |
| Select | A on card → confirm modal |
| Confirm ending | A on "Are you certain?" |
| Back | B returns to card selection |
| Blocked | Attack/combat inputs disabled |

See `ENDING_DESIGN.md` §2 and `GAME_FEEL.md` §6.

---


## 12. QA checklist

- [ ] Tab menu pauses field movement
- [ ] Combat Esc does not open field pause
- [ ] All screens reachable with controller
- [ ] Lore unread indicator clears on read
- [ ] SC-16 choice requires deliberate confirm
