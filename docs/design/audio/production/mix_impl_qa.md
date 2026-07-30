---
id: mix-impl-qa
type: reference
audience: [audio]
status: active
authority: audio
tokens_est: 751
---
# Audio production — Mix, implementation, QA

**Hub:** [`AUDIO_PRODUCTION_GUIDE.md`](../AUDIO_PRODUCTION_GUIDE.md)

## 8. Mix & loudness targets

| Bus | Integrated LUFS | True peak |
|-----|-----------------|-----------|
| Music (each BGM) | -16 LUFS | -1.0 dBTP |
| SFX (category peak) | — | -6.0 dBFS |
| Voice / selective VO | −18 LUFS (short clips) | −3.0 dBTP |
| Ambient beds | -22 LUFS | -6.0 dBTP |

**Relative balance** (from `AUDIO_DIRECTION.md` §5): dialogue always readable over Music; Ambient always under Music.

**Ducking:** Long dialogue scenes may duck Music -6 dB for readability; SC-16 choice ducks to -24 dBFS effective. **Selective VO** (`voice_id` lines): Voice bus −12 dBFS; duck music per `vo_prompts.json` `duck_bgm_db` (SC-16: −18 dB).

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

See `docs/design/ui/SETTINGS_ACCESSIBILITY.md` §1.

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

Automated gates: `docs/design/audio/AUDIO_QA.md`

| Layer | BGM | P0 VO |
|-------|-----|-------|
| Catalog | `check_audio_catalog.py` + `audio_qa_catalog.json` | `audio_qa_catalog.json` `vo_clips` + `vo_prompts.json` |
| Technical | `check_audio_technical.py` | `check_audio_vo.py` (duration, loudness, locale paths) |
| Listen jury | `review_audio_vision.py` — 8 hero tracks, A6/A7 | `review_vo_vision.py` — 5 P0 clips, V6/V7, gate locale `en` |
| Smoke | `bash tools/run_audio_smoke_checks.sh` | Same script when gate VO file exists |

- [ ] All track IDs in §3 exist as `.ogg` under `game/assets/audio/`
- [ ] No audible click at loop points (10 min loop test per BGM)
- [ ] Scene map §4 verified in-game for SC-00, SC-05, SC-09, SC-15, SC-16, SC-17a
- [ ] Boss phase music crossfades at correct HP thresholds
- [ ] SC-16 choice ducks music; attack input blocked
- [ ] Volume sliders affect correct buses
- [ ] Every external asset in `docs/design/art/LICENSES.md` + manifest
- [ ] `bash tools/check_asset_compliance.sh` passes
- [ ] No placeholder procedural audio in ship build
