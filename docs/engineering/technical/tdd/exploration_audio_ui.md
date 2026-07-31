---
id: exploration-audio-ui
type: reference
audience: [architect, builder]
phase: [1, 4]
status: active
authority: engineering
tokens_est: 552
summary: "Zone entry: `ZoneVisuals.apply_to_scene(root, zone_id)` (static — `base_classes.json` + `zone_visuals_lib.py`) then `AudioManager.play_bgm(zone_bgm)`."
---
# Technical Design — Exploration, audio, UI

**Hub:** [`TECHNICAL_DESIGN.md`](../TECHNICAL_DESIGN.md)

## When to read

Use **Technical Design — Exploration, audio, UI** (roles: architect, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [8. Exploration stack](#8-exploration-stack)
- [9. Audio routing](#9-audio-routing)
- [10. UI layer](#10-ui-layer)


## 8. Exploration stack

| Component | Responsibility |
|-----------|----------------|
| `PlayerController` | `CharacterBody3D` movement, interaction ray |
| `OrbitCamera` | Third-person follow (`CINEMATICS.md` §2) |
| `Interactable` | Area3D + `scene_id` or inspect flag |
| `ZoneTransition` | Loads target zone + spawn marker |
| `ZoneVisuals` | Applies `environments/*.tres`, lights, fog per zone id |
| `EncounterTrigger` | Starts combat when flag/area conditions met |

**Zone entry:** `ZoneVisuals.apply_to_scene(root, zone_id)` (static — `base_classes.json` + `zone_visuals_lib.py`) then `AudioManager.play_bgm(zone_bgm)`.

Per-zone interactable tables: [LEVEL_DESIGN.md](../../../design/world/LEVEL_DESIGN.md).

---


## 9. Audio routing

| Bus | Contents | Manager API |
|-----|----------|-------------|
| Master | All | `AudioManager.set_bus_volume()` |
| Music | BGM, stings on music bus | `play_bgm(id)`, 1.5s crossfade |
| SFX | UI, combat, footsteps | `play_sfx(id)` |
| Voice | 12 selective VO clips | `VoiceLinePlayer` on Voice bus |
| Ambient | Zone loops | `play_ambient(id)` — ducks under Music −3 dB |

Ducking rules: `AUDIO_PRODUCTION_GUIDE.md` §8; per-clip overrides in `vo_prompts.json`. Scene/zone BGM hooks: `game/data/audio/scene_audio_map.json` (runtime loads by `scene_id` / `zone_id`).

---


## 10. UI layer

| Scene | Layer | Input |
|-------|-------|-------|
| `dialogue_box.tscn` | CanvasLayer 10 | Blocks field movement |
| `interaction_prompt_hud.tscn` | CanvasLayer 5 | Field only |
| `combat_ui.tscn` | CanvasLayer 10 | Combat only |
| `tab_menu.tscn` | CanvasLayer 20 | Pause field |
| `pause_menu.tscn` | CanvasLayer 25 | Pause |

**Screen map:** `UI_UX_FLOW.md` §1. `LocalizationManager` supplies fonts per locale.

---
