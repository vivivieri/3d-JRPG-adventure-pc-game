---
id: menu-zones
type: reference
audience: [audio, builder]
status: active
authority: audio
tokens_est: 588
summary: "BGM — Per-track Specs — Menu + zone BGM — covers `bgm_menu`; `bgm_prologue`; `bgm_village`; `bgm_caves`"
---
# BGM — Per-track Specs — Menu + zone BGM

**Hub:** [`per_track_specs.md`](../per_track_specs.md)

## When to read

Use **BGM — Per-track Specs — Menu + zone BGM** (roles: audio, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (5 sections).

## Jump to

- [`bgm_menu`](#bgm_menu)
- [`bgm_prologue`](#bgm_prologue)
- [`bgm_village`](#bgm_village)
- [`bgm_caves`](#bgm_caves)
- [`bgm_palace`](#bgm_palace)


## `bgm_menu`

| Field | Value |
|-------|-------|
| **BPM** | 72 |
| **Key** | D minor |
| **Mood** | Still, distant surf |
| **Instruments** | Solo koto, sparse synth pad, faint wave noise bed |
| **Loop point** | Bar 17 (sample-accurate; document in `docs/design/audio/audio_sheets/bgm_menu.md`) |
| **Intro** | 4-bar fade-in from silence on title load |
| **Do not** | Upbeat melody, percussion forward |


## `bgm_prologue`

| Field | Value |
|-------|-------|
| **BPM** | 60 |
| **Key** | A minor |
| **Mood** | Mythic, fateful |
| **Instruments** | Low strings, distant choir pad (no lyrics), single bell hit at box gift |
| **Loop** | **No** — plays once SC-00 → fade to `bgm_village` on SC-01 |
| **Length** | 1:30–1:45 max (must fit skippable prologue) |


## `bgm_village`

| Field | Value |
|-------|-------|
| **BPM** | 66 |
| **Key** | E minor |
| **Mood** | Empty dread, wind |
| **Instruments** | Shakuhachi lead, low cello drone, wind texture |
| **Loop point** | Bar 33 |
| **Layer with** | `amb_village_wind` at -18 dBFS |
| **Zones** | `beach_shore` (SC-01), `ruined_village` (SC-02–05) |


## `bgm_caves`

| Field | Value |
|-------|-------|
| **BPM** | 78 |
| **Key** | F# minor |
| **Mood** | Wonder + unease |
| **Instruments** | Synth pad, water bells, occasional biolume chime |
| **Loop point** | Bar 25 |
| **Layer with** | `amb_cave_drip` |
| **Zones** | `tidal_caves` (SC-06–11) |
| **Duck** | -6 dB during SC-08 whisper dialogue |


## `bgm_palace`

| Field | Value |
|-------|-------|
| **BPM** | 84 |
| **Key** | Bb major (uncanny — major key feels wrong) |
| **Mood** | Sterile beauty |
| **Instruments** | Harp arpeggios, choir pad, no vocals |
| **Loop point** | Bar 29 |
| **Layer with** | `amb_palace_hum` |
| **Zones** | `dragon_palace_gate` (SC-12–16 field) |
| **SC-11 flashback** | Duck to 40% during Otohime dialogue (text on screen) |
