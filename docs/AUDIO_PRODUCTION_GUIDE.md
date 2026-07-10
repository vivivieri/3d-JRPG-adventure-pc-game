# Tides of Urashima — Audio Production Guide

**Version:** 1.0 (Pre-build)  
**Visual / tonal target:** Melancholy coastal JRPG — restrained, not upbeat adventure.  
**Cross-refs:** `docs/AUDIO_DIRECTION.md` (creative direction), `docs/STORYBOARD.md`, `docs/BOSS_DESIGNS.md`, `game/data/story/scenes.json`, `docs/ASSET_COMPLIANCE.md`

**Canonical rule:** Track and SFX IDs in this doc are the **file names** (without extension). Creative mood notes live in `AUDIO_DIRECTION.md`; this doc is the **production spec** (format, loops, scene hooks, file layout).

---

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
| **Placeholder** | Replace procedural output from `tools/generate_game_audio.py` before ship |
| **Compliance** | Register every external file: `python3 tools/register_asset.py add`; run `bash tools/check_asset_compliance.sh` |

### Bus routing (Godot)

| Bus | Contents | User setting |
|-----|----------|--------------|
| `Master` | All output | `master_volume` |
| `Music` | BGM, stings on music bus | `music_volume` |
| `SFX` | UI, combat, footsteps, one-shots | `sfx_volume` |
| `Voice` | Dialogue VO lines (if recorded) | follows `master_volume` |
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
  stings/
    sting_combat_start.ogg
    sting_boss_intro.ogg
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
docs/audio_sheets/          # Design-time loop sheets (not shipped)
  <track_id>.md
```

---

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
| **Loop point** | Bar 17 (sample-accurate; document in `docs/audio_sheets/bgm_menu.md`) |
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
| **SC-11 flashback** | Duck to 40% under Otohime VO |

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

| Scene | Zone | BGM | Ambient | Stings / one-shots |
|-------|------|-----|---------|-------------------|
| SC-00 | — | `bgm_prologue` | — | Box gift bell |
| SC-01 | `beach_shore` | `bgm_village` | `amb_beach_surf` | Distant thunder at spawn |
| SC-02 | `ruined_village` | `bgm_village` | `amb_village_wind` | Hub pan wind swell |
| SC-03 | `ruined_village` | duck 50% | `amb_village_wind` | Fox bell distant; spirit reverb VO |
| SC-04 | `ruined_village` | `bgm_village` | shack interior dampened | Map handoff paper rustle |
| SC-05 | combat | `bgm_combat` | — | `sting_combat_start`; tutorial confirm |
| SC-06 | `tidal_caves` | `bgm_caves` | `amb_cave_drip` | Zone enter low pass 1 s |
| SC-07 | `tidal_caves` | `bgm_caves` | drip | Switch `sfx_story_puzzle_switch`; chest open |
| SC-08 | `tidal_caves` | duck 40% | drip + whisper bed | Overlapping whisper VO |
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

Full skill → SFX map: `docs/SKILLS_BIBLE.md` + §6 below.

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

Store per-track loop documentation in `docs/audio_sheets/<track_id>.md`:

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

## 8. Mix & loudness targets

| Bus | Integrated LUFS | True peak |
|-----|-----------------|-----------|
| Music (each BGM) | -16 LUFS | -1.0 dBTP |
| SFX (category peak) | — | -6.0 dBFS |
| Voice / dialogue | -18 LUFS | -3.0 dBTP |
| Ambient beds | -22 LUFS | -6.0 dBTP |

**Relative balance** (from `AUDIO_DIRECTION.md` §5): dialogue always readable over Music; Ambient always under Music.

**Ducking:** Story dialogue ducks Music -6 dB; SC-16 choice ducks to -24 dBFS effective.

---

## 9. Implementation (`AudioManager`)

```gdscript
# Expected API (implementation branch)
AudioManager.play_bgm("bgm_village", crossfade_sec=1.5)
AudioManager.play_ambient("amb_village_wind")
AudioManager.play_sfx("sfx_ui_confirm")
AudioManager.duck_music(db=-6.0, duration=0.3)
AudioManager.boss_phase_music("bgm_boss_tide_keeper_p2", crossfade_sec=2.0)
```

| Setting | Key | Default |
|---------|-----|---------|
| Master | `master_volume` | 0.8 |
| Music | `music_volume` | 0.7 |
| SFX | `sfx_volume` | 0.8 |

See `docs/SETTINGS_ACCESSIBILITY.md` §1.

---

## 10. Production order

| Priority | Deliverable |
|----------|-------------|
| P0 | `bgm_village` + `amb_beach_surf` + `amb_village_wind` + footstep sand/wood (vertical slice SC-02) |
| P0 | UI confirm/cancel + `sting_combat_start` + `bgm_combat` |
| P1 | `bgm_caves` + cave ambient + SC-07 puzzle SFX |
| P1 | `bgm_boss` + Shore Wraith boss SFX package |
| P2 | `bgm_palace` + Sentinel package |
| P2 | Tide Keeper p2/p3 BGM + choice silence |
| P3 | Prologue + 3 ending tracks |
| P3 | Remaining combat SFX per `SKILLS_BIBLE.md` |

---

## 11. QA checklist

- [ ] All track IDs in §3 exist as `.ogg` under `game/assets/audio/`
- [ ] No audible click at loop points (10 min loop test per BGM)
- [ ] Scene map §4 verified in-game for SC-00, SC-05, SC-09, SC-15, SC-16, SC-17a
- [ ] Boss phase music crossfades at correct HP thresholds
- [ ] SC-16 choice ducks music; attack input blocked
- [ ] Volume sliders affect correct buses
- [ ] Every external asset in `docs/LICENSES.md` + manifest
- [ ] `bash tools/check_asset_compliance.sh` passes
- [ ] No placeholder procedural audio in ship build
