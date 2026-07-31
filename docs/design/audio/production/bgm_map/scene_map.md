---
id: scene-map
type: reference
phase: [1, 5]
audience: [audio, builder]
status: active
authority: audio
tokens_est: 706
summary: "`game/data/audio/scene_audio_map.json` (validated L0 on `main`). The table below is the human-readable mirror; when they disagree, fix JSON first then sync this"
---
# Audio Production — BGM & Scene Map — Scene → audio map

**Hub:** [`bgm_and_scene_map.md`](../bgm_and_scene_map.md)

## When to read

Use **Audio Production — BGM & Scene Map — Scene → audio map** (roles: audio, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (2 sections).

## Jump to

- [4. Scene → audio map](#4-scene-audio-map)
- [Zone default BGM (field)](#zone-default-bgm-field)


## 4. Scene → audio map

**Machine-readable authority:** `game/data/audio/scene_audio_map.json` (validated L0 on `main`). The table below is the human-readable mirror; when they disagree, fix JSON first then sync this doc.

| Scene | Zone | BGM | Ambient | Stings / one-shots |
|-------|------|-----|---------|-------------------|
| SC-00 | — | `bgm_prologue` | — | Box gift bell |
| SC-01 | `beach_shore` | `bgm_village` | `amb_beach_surf` | Distant thunder at spawn |
| SC-02 | `ruined_village` | `bgm_village` | `amb_village_wind` | Hub pan wind swell |
| SC-03 | `ruined_village` | duck 50% | `amb_village_wind` | Fox bell distant; spirit reverb SFX under text |
| SC-04 | `ruined_village` | `bgm_village` | shack interior dampened | Map handoff paper rustle |
| SC-05 | combat | `bgm_combat` | — | `sting_combat_start`; tutorial confirm |
| SC-06 | `tidal_caves` | `bgm_caves` | `amb_cave_drip` | Zone enter low pass 1 s |
| SC-07 | `tidal_caves` | `bgm_caves` | drip | Switch `sfx_story_puzzle_switch`; chest open |
| SC-08 | `tidal_caves` | duck 40% | drip + whisper bed | Overlapping whisper SFX bed (no VO) |
| SC-09 | boss | `bgm_boss` | water surge | `sting_boss_intro`; phase 2 whispers |
| SC-10 | `tidal_caves` | `bgm_caves` | — | `sting_yuzu_join` (short, not triumphant) |
| SC-11 | cinematic | duck `bgm_caves` 30% | — | Palace harp overlay `sfx_story_palace_harp` |
| SC-12 | `dragon_palace_gate` | `bgm_palace` | `amb_palace_hum` | Pearl gate insert chime |
| SC-13 | `dragon_palace_gate` | `bgm_palace` | hum | Mirror shimmer |
| SC-14 | boss | `bgm_boss` | — | Lacquer footstep intro |
| SC-15 | boss | `bgm_boss` → p2 → p3 | — | Clock tick subtle; phase stings |
| SC-16 | choice | `bgm_boss_tide_keeper_p3` ducked | near silence | `sting_choice_silence` |
| SC-17a/b/c | endings | respective ending BGM | per ending | Credits sting optional |

### Zone default BGM (field)

| Zone ID | Default BGM | Ambient |
|---------|-------------|---------|
| `beach_shore` | `bgm_village` | `amb_beach_surf` |
| `ruined_village` | `bgm_village` | `amb_village_wind` |
| `tidal_caves` | `bgm_caves` | `amb_cave_drip` |
| `dragon_palace_gate` | `bgm_palace` | `amb_palace_hum` |
| `ending_rewind` | `bgm_ending_rewind` | crowd bed |
| `ending_anchor` | `bgm_ending_anchor` | dawn birds sparse |
| `ending_drift` | `bgm_ending_drift` | `amb_beach_surf` |

---
