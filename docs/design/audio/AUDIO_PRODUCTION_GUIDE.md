---
id: audio-production-guide
type: reference
audience: [audio]
phase: [1, 5]
status: active
authority: audio
tokens_est: 777
summary: "Melancholy coastal JRPG — restrained, not upbeat adventure."
---
# Tides of Urashima — Audio Production Guide

## When to read

Use **Tides of Urashima — Audio Production Guide** (roles: audio) when you need this reference during the current task Jump to a section below instead of reading end-to-end (4 sections).

## Jump to

- [1. Global audio rules](#1-global-audio-rules)
- [Bus routing (Godot)](#bus-routing-godot)
- [2. File layout](#2-file-layout)
- [Production packs (progressive disclosure)](#production-packs-progressive-disclosure)


## 1. Global audio rules

| Rule | Detail |
|------|--------|
| **Format** | Ogg Vorbis (`.ogg`) for all shipped audio |
| **Sample rate** | 44.1 kHz |
| **Bit depth** | 16-bit export |
| **Channels** | Stereo (BGM, ambient); mono OK for short SFX &lt; 0.5 s |
| **Loop** | Seamless loop on all field BGM and ambient beds |
| **Loudness** | BGM integrated **-16 LUFS**; SFX peak **-6 dBFS** (see §8) |
| **Naming** | `snake_case`; prefix `bgm_` or `sfx_` or `amb_` or `sting_` |
| **Placeholder** | Dev: `tools/generate_game_audio.py` or ACE-Step `--fallback`. **Ship:** curated BGM/SFX per act — no raw procedural placeholders in release build (M5) |
| **Compliance** | Register every external file: `python3 tools/register_asset.py add`; run `bash tools/check_asset_compliance.sh` |

### Bus routing (Godot)

| Bus | Contents | User setting |
|-----|----------|--------------|
| `Master` | All output | `master_volume` |
| `Music` | BGM, stings on music bus | `music_volume` |
| `SFX` | UI, combat, footsteps, one-shots | `sfx_volume` |
| `Voice` | **Selective VO** — 12 `voice_id` clips only (`docs/design/vision/VO_HIT_LIST.md`) | `voice_volume` (Phase 2+) |
| `Ambient` | Zone loops, surf, drips | duck under Music (-3 dB) |

**Crossfade:** `AudioManager` — **1.5 s** linear crossfade between zone BGM tracks.

---

## 2. File layout

```
game/assets/audio/
  bgm/
    bgm_menu.ogg
    bgm_prologue.ogg
    bgm_village.ogg
    bgm_caves.ogg
    bgm_palace.ogg
    bgm_combat.ogg
    bgm_boss.ogg
    bgm_boss_tide_keeper_p2.ogg
    bgm_boss_tide_keeper_p3.ogg
    bgm_ending_rewind.ogg
    bgm_ending_anchor.ogg
    bgm_ending_drift.ogg
    cine_opening_hero.ogg
    cine_ending_rewind_hero.ogg
    cine_ending_anchor_hero.ogg
    cine_ending_drift_hero.ogg
  stings/
    sting_combat_start.ogg
    sting_boss_intro.ogg
    cine_boss_wraith_intro.ogg
    cine_boss_sentinel_intro.ogg
    cine_boss_tide_keeper_intro.ogg
    sting_yuzu_join.ogg
    sting_phase_change.ogg
    sting_victory.ogg
    sting_game_over.ogg
    sting_choice_silence.ogg
  amb/
    amb_beach_surf.ogg
    amb_village_wind.ogg
    amb_cave_drip.ogg
    amb_palace_hum.ogg
  sfx/
    ui/
    footstep/
    combat/
    story/
docs/design/audio/audio_sheets/          # Design-time loop sheets (not shipped)
  <track_id>.md
```

---

## Production packs (progressive disclosure)

| Pack | Path |
|------|------|
| BGM + scene map | [production/bgm_and_scene_map.md](production/bgm_and_scene_map.md) |
| Combat + SFX | [production/combat_sfx.md](production/combat_sfx.md) |
| Mix / impl / QA | [production/mix_impl_qa.md](production/mix_impl_qa.md) |

