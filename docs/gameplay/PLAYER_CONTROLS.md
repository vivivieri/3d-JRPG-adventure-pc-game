# Player Controls — Tides of Urashima

**Version:** 1.0
**Authority:** `docs/ui/UI_UX_FLOW.md` §10–11 · `game/data/code/input_registry.json`
**Ship target:** Keyboard + mouse + Xbox-layout gamepad on main path (M5 polish)

---

## 1. Field exploration

| Action | Keyboard / mouse | Gamepad |
|--------|------------------|---------|
| Move | WASD | Left stick |
| Interact | E | A |
| Menu | Tab | Y |
| Pause | Esc | Start |
| Camera orbit | RMB drag | Right stick |
| Camera zoom | Scroll wheel | — (auto-frame in combat) |
| Dialogue advance | Space / Enter / E | A |

---

## 2. Combat

| Action | Keyboard | Gamepad |
|--------|----------|---------|
| Confirm action | Space / Enter / LMB | A |
| Cancel / back | Esc / RMB | B |
| Menu navigate | Arrow keys / mouse | D-pad |
| Target cycle | Tab (when applicable) | LB / RB |

---

## 3. SC-16 ending choice (gamepad)

| Rule | Detail |
|------|--------|
| Default focus | No option pre-selected |
| Navigate | D-pad up/down between three cards |
| Select | A on card → confirm modal |
| Confirm ending | A on "Are you certain?" |
| Back | B returns to card selection |
| Blocked | Attack/combat inputs disabled |

See `docs/vision/ENDING_DESIGN.md` §2.

---

## 4. InputMap contract

GDAI MCP applies these action IDs to `project.godot` at P1-02+. Do not invent variants in GDScript.

Canonical list: `game/data/code/input_registry.json`

---

## 5. Accessibility

- `hints_enabled` — puzzle hints (default on)
- `intent_contrast` — high-contrast enemy intent icons (`settings_schema.json`)
- Subtitles always on for dialogue; VO optional per clip tier

---

## Related docs

| Doc | Contents |
|-----|----------|
| `docs/ui/UI_UX_FLOW.md` | HUD, menus, pause rules |
| `docs/gameplay/TUTORIAL_DESIGN.md` | Tutorial prompts (`TUTORIAL_*` keys) |
| `docs/gameplay/GAME_FEEL.md` | Camera smoothing, input buffer |
