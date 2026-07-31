---
id: goals-music
type: reference
phase: [1, 5]
audience: [audio, builder]
status: active
authority: audio
tokens_est: 457
summary: "Audio Direction — Design goals + music map — Loop: All field tracks seamless loop; 2–4 min length target."
---
# Audio Direction — Design goals + music map

**Hub:** [`AUDIO_DIRECTION.md`](../AUDIO_DIRECTION.md)

## When to read

Use **Audio Direction — Design goals + music map** (roles: audio, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (2 sections).

## Jump to

- [1. Design goals](#1-design-goals)
- [2. Music map](#2-music-map)


## 1. Design goals

| Goal | Detail |
|------|--------|
| Tone | Melancholy coastal JRPG — not upbeat adventure |
| Reference | *NieR* restraint, *Ghost of Tsushima* wind/shore, traditional koto/shamisen accents |
| Replace | Procedural placeholder audio (`tools/generate_game_audio.py`) before ship |
| Languages | Music is non-vocal or JP lyrics buried in mix; SFX universal |
| Voice acting | **Selective** — 12 short AI clips at peaks in **en, ja, zh, and zh-Hant** (`docs/design/vision/VO_HIT_LIST.md`); all other dialogue text-only |

---


## 2. Music map

| Track ID | Zone / context | Mood | Instruments (suggested) |
|----------|----------------|------|------------------------|
| `bgm_menu` | Main menu | Still, distant surf | Solo koto, sparse pads |
| `bgm_village` | Ruined hub | Empty dread, wind | Shakuhachi, low strings |
| `bgm_caves` | Tidal Caves | Wonder + unease | Synth pad + water bells |
| `bgm_palace` | Dragon Palace Gate | Sterile beauty | Harp, choir pad (no lyrics) |
| `bgm_combat` | Standard fight | Tension, mid tempo | Taiko-light, strings |
| `bgm_boss` | Boss fights | Escalation | Full taiko, choir hits |
| `bgm_ending_rewind` | SC-17a | Bittersweet festival | Shamisen + crowd ambience |
| `bgm_ending_anchor` | SC-17b | Dawn hope | Soft piano, koto |
| `bgm_ending_drift` | SC-17c | Open tragedy | Solo shakuhachi, sea |

**Loop:** All field tracks seamless loop; 2–4 min length target.

---
