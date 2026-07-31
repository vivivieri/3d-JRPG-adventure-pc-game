---
id: per-track-specs
type: reference
phase: [1, 5]
audience: [audio, builder]
status: active
authority: audio
tokens_est: 1012
summary: "Per-track production specs"
---
# BGM Track Sheets — Per-track production specs

**Hub:** [`bgm_sheets.md`](../bgm_sheets.md)

### Per-track production spec

#### `bgm_menu`

| Field | Value |
|-------|-------|
| **BPM** | 72 |
| **Key** | D minor |
| **Mood** | Still, distant surf |
| **Instruments** | Solo koto, sparse synth pad, faint wave noise bed |
| **Loop point** | Bar 17 (sample-accurate; document in `docs/design/audio/audio_sheets/bgm_menu.md`) |
| **Intro** | 4-bar fade-in from silence on title load |
| **Do not** | Upbeat melody, percussion forward |

#### `bgm_prologue`

| Field | Value |
|-------|-------|
| **BPM** | 60 |
| **Key** | A minor |
| **Mood** | Mythic, fateful |
| **Instruments** | Low strings, distant choir pad (no lyrics), single bell hit at box gift |
| **Loop** | **No** — plays once SC-00 → fade to `bgm_village` on SC-01 |
| **Length** | 1:30–1:45 max (must fit skippable prologue) |

#### `bgm_village`

| Field | Value |
|-------|-------|
| **BPM** | 66 |
| **Key** | E minor |
| **Mood** | Empty dread, wind |
| **Instruments** | Shakuhachi lead, low cello drone, wind texture |
| **Loop point** | Bar 33 |
| **Layer with** | `amb_village_wind` at -18 dBFS |
| **Zones** | `beach_shore` (SC-01), `ruined_village` (SC-02–05) |

#### `bgm_caves`

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

#### `bgm_palace`

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

#### `bgm_combat`

| Field | Value |
|-------|-------|
| **BPM** | 108 |
| **Key** | C minor |
| **Mood** | Tension, mid tempo |
| **Instruments** | Light taiko, staccato strings, no choir |
| **Loop point** | Bar 17 |
| **Enter** | `sting_combat_start` (0.8 s) then crossfade 0.5 s |
| **Exit** | Crossfade 1.5 s back to zone BGM on victory |

#### `bgm_boss`

| Field | Value |
|-------|-------|
| **BPM** | 120 |
| **Key** | D minor |
| **Mood** | Escalation |
| **Instruments** | Full taiko, low brass, choir hits on bar 1 of each 8-bar phrase |
| **Loop point** | Bar 33 |
| **Enter** | `sting_boss_intro` (1.2 s) after cinematic skip window |
| **Bosses** | `shore_wraith` (SC-09), `palace_sentinel` (SC-14), Tide Keeper **phase 1** (SC-15) |

#### `bgm_boss_tide_keeper_p2`

| Field | Value |
|-------|-------|
| **BPM** | 132 |
| **Key** | D minor → modal lift on relative F |
| **Mood** | Surge, cosmic |
| **Trigger** | Tide Keeper HP ≤ 66%; banner "Then let the sea decide!" |
| **Crossfade** | 2.0 s from `bgm_boss` |
| **Sync** | Camera orbit phase 2 (`CINEMATICS.md`) |

#### `bgm_boss_tide_keeper_p3`

| Field | Value |
|-------|-------|
| **BPM** | 72 |
| **Key** | A minor |
| **Mood** | Ebb, tragic stillness |
| **Trigger** | Tide Keeper HP ≤ 25%; banner "Even mercy... tires." |
| **Crossfade** | 3.0 s |
| **Choice gate** | At 10% HP → `sting_choice_silence` ducks music to -24 dBFS; hold until choice confirmed |

#### `bgm_ending_rewind` / `bgm_ending_anchor` / `bgm_ending_drift`

| Track | BPM | Key | Length | Loop |
|-------|-----|-----|--------|------|
| `bgm_ending_rewind` | 96 | G major | 1:45 | No — credits roll |
| `bgm_ending_anchor` | 80 | C major | 1:30 | No |
| `bgm_ending_drift` | 54 | E minor | 2:00 | No — fade to surf only |

See `AUDIO_DIRECTION.md` §2 for instrument notes. Each ending track **must not** loop; tail fade ≥ 4 s.

---
