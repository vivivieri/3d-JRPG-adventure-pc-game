---
id: implementation-phase-2
type: how-to
audience: [pm, architect, builder]
phase: [2]
status: active
authority: workflow
tokens_est: 400
---
# Implementation Plan — Phase 2

**Hub:** [`IMPLEMENTATION_PLAN.md`](../IMPLEMENTATION_PLAN.md)

## Phase 2 — Core systems shell

**Read first:** `docs/engineering/technical/TECHNICAL_DESIGN.md`, `docs/engineering/technical/CODE_STYLE.md`

| # | Task | Docs |
|---|------|------|
| 2.1 | Autoloads: `GameManager`, `EventBus`, `SaveSystem`, `DialogueRunner`, `CombatManager` | GDD, DATA_ARCHITECTURE |
| 2.2 | `GameManager.load_json("res://data/...")` API | game/data/README.md |
| 2.3 | `LocalizationManager` + `FontThemeManager` + Noto fonts (en / ja / zh / zh-Hant) | LOCALIZATION.md |
| 2.4 | Main menu → New Game → SC-00 prologue → `beach_shore` | UI_UX_FLOW.md, TUTORIAL_DESIGN |
| 2.5 | `PlayerController` base class + `player.tscn` component scene | CODE_BASE_CLASS_RULES, GAME_FEEL.md |
| 2.6 | Scene transitions between zones | WORLD_MAP_AND_FLOW.md |
| 2.7 | `AudioManager` shell — BGM crossfade, SFX buses, procedural placeholders | AUDIO_PRODUCTION_GUIDE |
| 2.8 | Settings menu — language, `vo_dialect` (zh-Hant), volume sliders | SETTINGS_ACCESSIBILITY.md, LOCALIZATION.md |

---

