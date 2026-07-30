---
id: combat-presentation
type: reference
audience: [visual, builder]
status: active
authority: art
tokens_est: 658
---
# Tides of Urashima — Combat Presentation

**Version:** 1.0 (Pre-build)
**Cross-refs:** `docs/design/gameplay/COMBAT_SYSTEMS.md`, `docs/design/ui/UI_UX_FLOW.md`, `docs/design/art/SHADER_SPECS.md`, `game/data/code/shader_registry.json` (`ink_combat_overlay`)

---

## 1. Arena layout

| Element | Spec |
|---------|------|
| **Root** | `combat_instance.tscn` — `BattleField` Node3D center |
| **Party row** | Left third, facing +Z; 1–3 slots by encounter `party` array |
| **Enemy row** | Right third; boss centered, adds flanking |
| **Camera** | Fixed hero angle ~25° down, 12–14 m back; no orbit in v1 |
| **Background** | Zone-tinted void plane + muted sky gradient from active `zone_id` palette |
| **Lighting** | Single directional + low ambient; emissive VFX only on skills/limits |

Boss fights (SC-09, SC-14, SC-15) use wider FOV (+5°) and darker ambient per zone palette.

---

## 2. Ink-wash overlay

| Property | Value |
|----------|-------|
| **Shader** | `ink_combat_overlay.gdshader` (`shader_type canvas_item`) |
| **Parent** | `CombatUI` full-screen `ColorRect` above action menu |
| **Trigger** | Skill/limit resolve, boss phase change, victory/defeat |
| **Uniforms** | `ink_strength` 0.8 default; `pulse_duration` 0.35 s |
| **Policy** | Brief pulse — not persistent combat fog; respects `reduced_motion` (skip pulse) |

---

## 3. Intent & action UI

- **Intent panel:** Top-right; icon + i18n key `combat.intent.*` (`COMBAT_SYSTEMS.md` §6)
- **Action menu:** Bottom ink frame; Attack / Skill / Item / Defend / Escape
- **Turn order:** Left strip; SPD-sorted pips
- **Limit gauge:** Per-character bar under portrait; pulse at 100%

Hard mode: boss phase 2+ hides intent preview (`COMBAT_SYSTEMS.md` §10).

---

## 4. VFX tiers

| Tier | Examples | Budget |
|------|----------|--------|
| **Light** | White flash on hit, defend tint | Every action |
| **Medium** | Skill element streak, status icon pop | Skills |
| **Heavy** | Limit burst, boss phase shatter, ink overlay | Limits + bosses |

No full-screen whiteout; max 2 simultaneous medium VFX per side.

---

## 5. Audio ducking

| Moment | BGM duck |
|--------|----------|
| Normal action | −3 dB, 0.2 s |
| Limit / boss phase | −6 dB, 0.5 s |
| Victory sting | −12 dB until sting ends |

---

## 6. Acceptance (Phase 4+)

- [ ] `combat_instance.tscn` loads with zone palette background
- [ ] Ink overlay pulses on limit use without blocking input
- [ ] Intent readable at 1080p with `intent_contrast: high_contrast`
- [ ] Boss entry resets limit gauges (`COMBAT_SYSTEMS.md` §5)
- [ ] `reduced_motion` disables ink pulse and screen shake
