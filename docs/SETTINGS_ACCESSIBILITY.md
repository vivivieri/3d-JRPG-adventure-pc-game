# Tides of Urashima — Settings & Accessibility

**Version:** 1.0 (Pre-build)  
**Cross-refs:** `docs/UI_UX_FLOW.md`, `user://settings.json`

---

## 1. Settings menu (global)

Accessible from: Main menu, Pause menu (field + combat)

| Setting | Type | Default | Storage key |
|---------|------|---------|-------------|
| **Language** | en / ja / zh | System or en | `locale` |
| **Master volume** | 0–100% | 80 | `master_volume` |
| **Music volume** | 0–100% | 70 | `music_volume` |
| **SFX volume** | 0–100% | 80 | `sfx_volume` |
| **Fullscreen** | On / Off / Borderless | Windowed | `fullscreen` |
| **Resolution** | 1280×720 … 3840×2160 | Desktop | `resolution` |
| **VSync** | On / Off | On | `vsync` |
| **Text speed** | Slow / Normal / Fast / Instant | Normal | `text_speed` |
| **Auto-advance dialogue** | Off / On | Off | `dialogue_auto` |
| **Screen shake** | On / Off | On | `screen_shake` |
| **Hard mode** | Off / On | Off | `hard_mode` |
| **Hints** | On / Off | On | `hints_enabled` |
| **Intent icon style** | Standard / High contrast | Standard | `intent_contrast` |

---

## 2. Text speed values

| Preset | CPS (characters per second) |
|--------|----------------------------|
| Slow | 25 |
| Normal | 40 |
| Fast | 60 |
| Instant | 999 (full line) |

---

## 3. Accessibility features (v1)

| Feature | Implementation |
|---------|----------------|
| **Subtitles** | All dialogue + VO lines in dialogue box (always on) |
| **Speaker labels** | Nameplate on every line |
| **Intent high contrast** | Adds white outline + text label under icon |
| **Colorblind-safe intents** | Shape + icon differ per type (sword vs skull vs waves) |
| **No quick-time events** | None in game |
| **Pause anytime** | Field + combat pause (not during SC-16 choice overlay) |
| **Reduced motion** | `screen_shake=off` disables boss camera orbit shake |
| **Font** | Noto Sans / JP / SC — readable 16px min body |

**Not in v1:** Remap controls, dyslexia font, TTS

---

## 4. Hard mode

See `COMBAT_SYSTEMS.md` §10. Toggle in settings; applies on **next combat** load.

First-play tutorials still run unless `game_completed`.

---

## 5. Hints system

When `hints_enabled` and stuck:

| Condition | Hint |
|-----------|------|
| 3 min in water puzzle | Quest log updates with switch hint |
| 2 wipes same boss | Roku bark with pattern tip |
| Low HP entering boss | Shop reminder if near shack |

---

## 6. Controller

Full mapping in `UI_UX_FLOW.md` §11. Controller detected automatically; UI glyphs swap.

---

## 7. QA checklist

- [ ] Settings persist across sessions
- [ ] Language swap immediate on menu
- [ ] High contrast intents distinguishable in grayscale
- [ ] Hard mode toggle does not mid-fight change boss HP
- [ ] Reduced motion disables SC-15 camera orbit shake only
