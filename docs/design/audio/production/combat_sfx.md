---
id: combat-sfx
type: reference
audience: [audio]
phase: [1, 5]
status: active
authority: audio
tokens_est: 1243
summary: "[`AUDIO_PRODUCTION_GUIDE.md`](../AUDIO_PRODUCTION_GUIDE.md)"
---
# Audio production — Combat & SFX

**Hub:** [`AUDIO_PRODUCTION_GUIDE.md`](../AUDIO_PRODUCTION_GUIDE.md)

## 5. Combat & boss audio hooks

### Standard encounter flow

```
Field BGM playing
  → player touches encounter
  → sting_combat_start (0.8 s)
  → crossfade 0.5 s → bgm_combat
  → victory: sting_victory (1.0 s) + crossfade 1.5 s → zone BGM
  → game over: sting_game_over → reload UI
```

### Boss-specific overrides

| Boss | Intro SFX | Phase audio | Death |
|------|-----------|-------------|-------|
| Shore Wraith | Water surge 5 s (`BOSS_DESIGNS.md`) | Phase 2: add whisper layer on Music bus | Cloth collapse + pool splash; 2 s silence |
| Palace Sentinel | March + lacquer footstep 3 s | — | Shield clang + lacquer crack |
| Tide Keeper | Rise drone 6 s | P2: `bgm_boss_tide_keeper_p2`; P3: `bgm_boss_tide_keeper_p3` | Dissolve wash; no victory sting before choice |

### Element combat SFX (per skill)

| Element | SFX prefix | Example |
|---------|------------|---------|
| Water | `sfx_combat_water_` | `sfx_combat_water_slash` |
| Spirit | `sfx_combat_spirit_` | `sfx_combat_spirit_purify` |
| Physical | `sfx_combat_phys_` | `sfx_combat_phys_hit` |

Full skill → SFX map: `docs/design/gameplay/SKILLS_BIBLE.md` + §6 below.

---

## 6. SFX manifest

### UI (`sfx/ui/`)

| ID | File | Duration | Trigger |
|----|------|----------|---------|
| `sfx_ui_confirm` | `confirm.ogg` | 0.15 s | Menu confirm, dialogue advance |
| `sfx_ui_cancel` | `cancel.ogg` | 0.12 s | Back / cancel |
| `sfx_ui_menu_open` | `menu_open.ogg` | 0.25 s | Tab menu open |
| `sfx_ui_menu_close` | `menu_close.ogg` | 0.20 s | Tab menu close |
| `sfx_ui_item_get` | `item_get.ogg` | 0.40 s | Pickup, quest reward |
| `sfx_ui_save` | `save.ogg` | 0.50 s | Manual save at well |
| `sfx_ui_shop_buy` | `shop_buy.ogg` | 0.30 s | Purchase |
| `sfx_ui_equip` | `equip.ogg` | 0.25 s | Equipment change |
| `sfx_ui_invalid` | `invalid.ogg` | 0.10 s | Greyed action |

### Footsteps (`sfx/footstep/`)

| ID | Surface | Zones |
|----|---------|-------|
| `sfx_footstep_sand` | Sand / beach | `beach_shore` |
| `sfx_footstep_wood` | Pier, shack | `ruined_village` |
| `sfx_footstep_wet` | Puddles, cave wet | village, caves |
| `sfx_footstep_marble` | Palace floors | `dragon_palace_gate` |

**Rule:** 3 variants per surface (`_01`, `_02`, `_03`); randomize; interval by walk speed.

### Combat (`sfx/combat/`)

| ID | Trigger |
|----|---------|
| `sfx_combat_hit_light` | Basic attack connect |
| `sfx_combat_hit_heavy` | Heavy / boss slam |
| `sfx_combat_miss` | Evade / miss |
| `sfx_combat_defend` | Defend brace |
| `sfx_combat_heal` | Heal skill |
| `sfx_combat_buff` | Buff applied |
| `sfx_combat_debuff` | Debuff applied |
| `sfx_combat_water_slash` | Urashima water skills |
| `sfx_combat_spirit_purify` | Yuzu purify |
| `sfx_combat_spirit_heal` | Yuzu heal pillar |
| `sfx_combat_phys_taunt` | Roku taunt |
| `sfx_combat_phys_harpoon` | Roku harpoon strike |
| `sfx_combat_enemy_wraith` | Tide Wraith attack |
| `sfx_combat_enemy_crab` | Salt Crab pinch |
| `sfx_combat_enemy_sentinel` | Sentinel spear |
| `sfx_combat_enemy_keeper` | Tide Keeper tidal fingers |

### Story (`sfx/story/`)

| ID | Scene | Notes |
|----|-------|-------|
| `sfx_story_box_glow` | SC-02+ | Looping pulse when box awakened; 3 material states |
| `sfx_story_box_glow_strong` | SC-16 | Choice bloom |
| `sfx_story_spirit_materialize` | SC-10 | Yuzu join 2 s |
| `sfx_story_puzzle_switch` | SC-07 | Water switch clunk |
| `sfx_story_chest_open` | SC-07 | Flooded chest |
| `sfx_story_palace_harp` | SC-11 | Unsettling perfect fifth |
| `sfx_story_pearl_insert` | SC-12 | Gate unlock |
| `sfx_story_mirror_shimmer` | SC-13 | Mirror chamber |
| `sfx_story_thunder_distant` | SC-01 | One-shot at spawn |
| `sfx_story_whisper_bed` | SC-08 | Layered drowned voices |

### Ambient beds (`amb/`)

| ID | Loop | Notes |
|----|------|-------|
| `amb_beach_surf` | Yes | Constant on beach; filter when indoors |
| `amb_village_wind` | Yes | Creaking wood occasional one-shot layered |
| `amb_cave_drip` | Yes | Random drip one-shots every 3–8 s |
| `amb_palace_hum` | Yes | Low 60 Hz hum + distant choir |

### Stings (`stings/`)

| ID | Duration | Bus |
|----|----------|-----|
| `sting_combat_start` | 0.8 s | Music |
| `sting_boss_intro` | 1.2 s | Music |
| `sting_yuzu_join` | 1.5 s | Music |
| `sting_phase_change` | 1.0 s | Music |
| `sting_victory` | 1.0 s | Music |
| `sting_game_over` | 1.5 s | Music |
| `sting_choice_silence` | 2.0 s | Music (duck, not mute) |

---

## 7. Loop sheet template

Store per-track loop documentation in `docs/design/audio/audio_sheets/<track_id>.md`:

```markdown
# bgm_village — Loop sheet
- File: game/assets/audio/bgm/bgm_village.ogg
- BPM: 66 | Key: E minor | Length: 3:00
- Loop start: 0:08.000 (bar 5)
- Loop end: 2:58.500 (bar 33)
- Crossfade loop: 0.050 s (DAW export) or seamless bake
- QA: No click at loop point in Godot 10 min play
```

---

