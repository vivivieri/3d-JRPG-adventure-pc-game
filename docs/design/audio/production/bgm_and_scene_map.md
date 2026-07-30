---
id: bgm-and-scene-map
type: reference
audience: [audio]
status: active
authority: audio
tokens_est: 1912
---
# Audio production — BGM & scene map

**Hub:** [`AUDIO_PRODUCTION_GUIDE.md`](../AUDIO_PRODUCTION_GUIDE.md)

## 3. BGM track sheets

### Master BGM list

| Track ID | File | Duration target | Loop | Used when |
|----------|------|-----------------|------|-----------|
| `bgm_menu` | `bgm/bgm_menu.ogg` | 2:30 | Yes | Title screen |
| `bgm_prologue` | `bgm/bgm_prologue.ogg` | 1:45 | No | SC-00 only |
| `bgm_village` | `bgm/bgm_village.ogg` | 3:00 | Yes | `ruined_village`, `beach_shore` field |
| `bgm_caves` | `bgm/bgm_caves.ogg` | 3:30 | Yes | `tidal_caves` field |
| `bgm_palace` | `bgm/bgm_palace.ogg` | 3:00 | Yes | `dragon_palace_gate` field |
| `bgm_combat` | `bgm/bgm_combat.ogg` | 2:00 | Yes | Standard encounters |
| `bgm_boss` | `bgm/bgm_boss.ogg` | 2:30 | Yes | Shore Wraith, Palace Sentinel |
| `bgm_boss_tide_keeper_p2` | `bgm/bgm_boss_tide_keeper_p2.ogg` | 2:00 | Yes | Tide Keeper phase 2 |
| `bgm_boss_tide_keeper_p3` | `bgm/bgm_boss_tide_keeper_p3.ogg` | 1:30 | Yes | Tide Keeper phase 3 + choice gate |
| `bgm_ending_rewind` | `bgm/bgm_ending_rewind.ogg` | 2:00 | No | SC-17a |
| `bgm_ending_anchor` | `bgm/bgm_ending_anchor.ogg` | 2:00 | No | SC-17b |
| `bgm_ending_drift` | `bgm/bgm_ending_drift.ogg` | 2:30 | No | SC-17c |

**v1 boss music rule:** Shore Wraith and Palace Sentinel share `bgm_boss`. Tide Keeper uses `bgm_boss` in phase 1, then crossfades to phase-specific tracks at thresholds (see §5).

---

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

