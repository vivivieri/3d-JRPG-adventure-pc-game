---
id: layout-elevenlabs
type: reference
phase: [1, 6]
audience: [audio, narrative]
status: active
authority: vision
tokens_est: 438
summary: "File layout + ElevenLabs setup"
---
# Selective VO Hit List — File layout + ElevenLabs setup

**Hub:** [`VO_HIT_LIST.md`](../VO_HIT_LIST.md)

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

5. **P0 QA pass** (before P1/P2 batch):

```bash
python3 tools/check_audio_vo.py --clip sc00_urashima_01 --locale en
python3 tools/review_vo_vision.py --clip sc00_urashima_01 --locale en --min-pass 2
# Repeat for each P0 clip; all locales: check_audio_vo.py --all-p0 --ship at M5
```

6. Register: assets auto-logged in `docs/asset_manifest.license.json`

---
