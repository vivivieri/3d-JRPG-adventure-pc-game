# Tides of Urashima — Selective VO Hit List (AI generation)

**Version:** 1.0  
**Policy:** Short VO at emotional peaks only — **not** full dialogue.  
**Engine:** ElevenLabs (`eleven_multilingual_v2`) via `tools/generate_ai_vo.py`  
**Cross-refs:** `docs/NARRATIVE_WRITING_GUIDE.md` §1, `game/data/audio/vo_prompts.json`, `game/data/dialogue/chapter_01.json`

---

## Design rules

| Rule | Detail |
|------|--------|
| One VO clip per scene max | Remaining lines in scene stay text-only |
| Length | ~1–6 seconds spoken |
| Subtitles | Always on (en / ja / zh / zh-Hant text canonical) |
| Crowds | SC-08 whispers = SFX bed, not voiced |
| Endings SC-17 | Music + cinematic hero BGM, no narrator VO |
| Mix | Duck music −6 dB (SC-16: −18 dB effective) |

---

## Hit list (12 clips)

| Tier | `voice_id` | Scene | Speaker | Line (EN) | Max |
|------|------------|-------|---------|-----------|-----|
| **P0** | `sc00_urashima_01` | SC-00 | Urashima | Three days. I'll be back in three days. | 3s |
| **P0** | `sc03_yuzu_01` | SC-03 | Yuzu | You left. We waited. | 3s |
| **P0** | `sc11_otohime_01` | SC-11 | Otohime | Stay, Urashima. In the palace, the world will not touch you. | 5s |
| **P0** | `sc13_roku_01` | SC-13 | Roku | The box holds their years. Open it, they live — you won't. | 5s |
| **P0** | `sc16_tide_keeper_01` | SC-16 | Tide Keeper | The tide waits. So did they. | 3s |
| **P1** | `sc01_urashima_01` | SC-01 | Urashima | Three days... it was only three days... | 3s |
| **P1** | `sc08_urashima_01` | SC-08 | Urashima | I know you. I left you all behind. | 3s |
| **P1** | `sc09_shore_wraith_01` | SC-09 | Shore Wraith | You chose her over us. | 2s |
| **P1** | `sc10_yuzu_01` | SC-10 | Yuzu | I can't rest until the tide is answered. | 4s |
| **P1** | `sc15_tide_keeper_01` | SC-15 | Tide Keeper | Paradise is mercy. You fled pain — I offered peace. | 5s |
| **P2** | `sc04_roku_01` | SC-04 | Roku | That box isn't a gift. Don't open it. | 4s |
| **P2** | `sc14_narrator_01` | SC-14 | Narrator | No mortal leaves with stolen time. | 3s |

**Totals:** 12 clips × 3 locales (`en`, `ja`, `zh`) + 12 clips × 2 zh-Hant dialects (`cant`, `cmn`) = **60 OGG files**  
**Text-only by design:** SC-02 inspectables, SC-05–07, SC-12 gate (music), SC-17 endings, choice UI

---

## File layout

```text
game/assets/audio/voice/
  en/sc03_yuzu_01.ogg
  ja/sc03_yuzu_01.ogg
  zh/sc03_yuzu_01.ogg
  zh-Hant/cant/sc03_yuzu_01.ogg
  zh-Hant/cmn/sc03_yuzu_01.ogg
```

Dialogue lines with `voice_id` in `chapter_01.json` resolve to:

- `en` / `ja` / `zh` → `res://assets/audio/voice/{locale}/{voice_id}.ogg`
- `zh-Hant` → `res://assets/audio/voice/zh-Hant/{vo_dialect}/{voice_id}.ogg` (`cant` or `cmn`)

---

## AI VO setup (ElevenLabs)

1. Create voices at [elevenlabs.io](https://elevenlabs.io) per `vo_prompts.json` → `characters.*.casting`
2. Copy each ElevenLabs voice ID into `game/data/audio/vo_prompts.json` (replace `PLACEHOLDER_*`)
3. Add **`ELEVENLABS_API_KEY`** to Cursor Secrets (commercial Steam use — verify ElevenLabs terms)
4. Generate:

```bash
bash tools/generate_ai_vo.sh --list
bash tools/generate_ai_vo.sh --tier p0 --locale ja
bash tools/generate_ai_vo.sh --clip sc03_yuzu_01 --locale en --locale ja --locale zh
bash tools/generate_ai_vo.sh --locale zh-Hant --dialect cant --tier p0
bash tools/generate_ai_vo.sh --locale zh-Hant --all-dialects
bash tools/generate_ai_vo.sh --all
```

5. Listen pass on P0 before generating P1/P2
6. Register: assets auto-logged in `docs/asset_manifest.license.json`

---

## Godot playback (Phase 2+)

`VoiceLinePlayer` resolves paths; `DialogueRunner` plays VO when `voice_id` is set:

- Duck BGM per clip `duck_bgm_db` in `vo_prompts.json`
- Player can advance before VO ends (clip fades)
- Settings: Voice volume; voice language follows text locale

---

## Ship checklist

- [ ] Replace all `PLACEHOLDER_*` voice IDs
- [ ] P0 clips approved in all 3 locales
- [ ] No VO on tutorial / inspectable / puzzle scenes
- [ ] `python3 tools/validate_story_data.py` passes
- [ ] Log ElevenLabs license in `docs/LICENSES.md`
