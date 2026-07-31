---
id: boss-hooks
type: reference
phase: [1, 5]
audience: [audio, builder]
status: active
authority: audio
tokens_est: 428
summary: "Audio Production — Combat SFX — Combat & boss hooks — → player touches encounter"
---
# Audio Production — Combat SFX — Combat & boss hooks

**Hub:** [`combat_sfx.md`](../combat_sfx.md)

## When to read

Use **Audio Production — Combat SFX — Combat & boss hooks** (roles: audio, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (4 sections).

## Jump to

- [5. Combat & boss audio hooks](#5-combat-boss-audio-hooks)
- [Standard encounter flow](#standard-encounter-flow)
- [Boss-specific overrides](#boss-specific-overrides)
- [Element combat SFX (per skill)](#element-combat-sfx-per-skill)


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
