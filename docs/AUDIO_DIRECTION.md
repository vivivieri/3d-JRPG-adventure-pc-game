# Tides of Urashima — Audio Direction

**Version:** 1.0 (Pre-build)  
**Cross-refs:** `docs/STORYBOARD.md`, `docs/BOSS_DESIGNS.md`, `game/assets/audio/`

---

## 1. Design goals

| Goal | Detail |
|------|--------|
| Tone | Melancholy coastal JRPG — not upbeat adventure |
| Reference | *NieR* restraint, *Ghost of Tsushima* wind/shore, traditional koto/shamisen accents |
| Replace | Procedural placeholder audio (`tools/generate_game_audio.py`) before ship |
| Languages | Music is non-vocal or JP lyrics buried in mix; SFX universal |

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
| SC-01 | Surf + distant thunder; VO line over ambient |
| SC-03 | Spirit voice with reverb; fox bell distant |
| SC-08 | Overlapping whisper VO under water drone |
| SC-10 | Yuzu join fanfare — short, not triumphant |
| SC-11 | Palace harp; unsettling perfect fifth |
| SC-16 | Music drops to near-silence during choice |

---

## 5. Mix levels (target)

| Bus | Relative |
|-----|----------|
| Music | -12 dBFS peak |
| SFX | -6 dBFS peak |
| Voice / dialogue | -9 dBFS (always readable) |
| Ambient | -18 dBFS under music |

---

## 6. Sourcing

| Type | Source options |
|------|----------------|
| Music | Commission, OpenGameArt (CC-BY log), Freesound CC0 layers |
| SFX | Freesound CC0, Sonniss GDC packs (check license) |
| **Rule** | Log in `docs/LICENSES.md`; register with `tools/register_asset.py`; verify with `tools/check_asset_compliance.sh` |

---

## 7. Implementation

- `AudioManager` crossfade 1.5s between zone BGM
- Boss music overrides field; restore on exit
- `user://settings.json`: `music_volume`, `sfx_volume` (0–1)

---

## 8. Production order

1. Village + beach ambient (vertical slice)
2. Combat + boss stems
3. Palace + caves
4. Ending tracks (3)
5. Full SFX pass per `ENCOUNTER_TABLE` fights
