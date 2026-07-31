---
id: sfx-cues-mix
type: reference
phase: [1, 5]
audience: [audio, builder]
status: active
authority: audio
tokens_est: 481
summary: "Audio Direction — SFX taxonomy, scene cues, mix levels — covers 3. SFX taxonomy; Boss SFX hooks; 4. Scene audio cues; 5. Mix levels (target)"
---
# Audio Direction — SFX taxonomy, scene cues, mix levels

**Hub:** [`AUDIO_DIRECTION.md`](../AUDIO_DIRECTION.md)

## When to read

Use **Audio Direction — SFX taxonomy, scene cues, mix levels** (roles: audio, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (4 sections).

## Jump to

- [3. SFX taxonomy](#3-sfx-taxonomy)
- [Boss SFX hooks](#boss-sfx-hooks)
- [4. Scene audio cues](#4-scene-audio-cues)
- [5. Mix levels (target)](#5-mix-levels-target)


## 3. SFX taxonomy

| Category | Examples | Notes |
|----------|----------|-------|
| UI | confirm, cancel, menu open | Soft wood/block ink style |
| Footstep | sand, wood pier, cave wet, marble | Per-zone surface |
| Combat | hit, heal, skill water, skill spirit | Element-distinct |
| Ambient | surf, cave drip, palace hum | Zone loops |
| Story | box glow pulse, spirit materialize, torii bell | One-shots tied to scenes |

### Boss SFX hooks

| Boss | Key sounds |
|------|------------|
| Shore Wraith | Water surge intro, drowned whispers phase 2 |
| Palace Sentinel | Lacquer footstep, shield clang |
| Tide Keeper | Clock tick (subtle), tidal roar phase 2 |

---


## 4. Scene audio cues

| Scene | Audio beat |
|-------|------------|
| SC-01 | Surf + distant thunder; optional `sc01_urashima_01` VO over ambient |
| SC-03 | Yuzu `sc03_yuzu_01` VO with reverb; fox bell distant |
| SC-08 | Overlapping whisper **SFX** bed under water drone — not voiced crowd |
| SC-10 | Yuzu join fanfare — short, not triumphant |
| SC-11 | Palace harp; unsettling perfect fifth |
| SC-16 | Music drops to near-silence during choice |

---


## 5. Mix levels (target)

| Bus | Relative |
|-----|----------|
| Music | -12 dBFS peak |
| SFX | -6 dBFS peak |
| Voice / dialogue | Selective VO in **en, ja, zh, zh-Hant** (12 clips) — see `docs/design/vision/VO_HIT_LIST.md` |
| Ambient | -18 dBFS under music |

---
