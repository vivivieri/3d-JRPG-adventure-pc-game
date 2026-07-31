---
id: architecture-dialect
type: how-to
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, narrative, builder]
status: active
authority: engineering
tokens_est: 761
summary: "Architecture + ZH dialect VO"
---
# Localization — Architecture + ZH dialect VO

**Hub:** [`LOCALIZATION.md`](../LOCALIZATION.md)

## Architecture

```
game/locale/translations.csv     # UI, skills, items, combat log (single source)
game/data/dialogue/*.json        # Story text inline per locale { en, ja, zh, zh-Hant }
game/scripts/core/localization_manager.gd   # Autoload API
game/scripts/story/voice_line_player.gd   # VO path resolver (locale + dialect)
```

### Settings schema (`user://settings.json`)

```json
{
  "locale": "zh-Hant",
  "vo_dialect": "cant"
}
```

| Field | Values | Notes |
|-------|--------|-------|
| `locale` | `en` \| `ja` \| `zh` \| `zh-Hant` | Written UI + dialogue |
| `vo_dialect` | `cant` \| `cmn` | Only used when `locale` is `zh-Hant`; ignored otherwise |

### LocalizationManager API

```gdscript
LocalizationManager.set_locale("zh-Hant")
LocalizationManager.set_vo_dialect("cant")  # or "cmn"
LocalizationManager.tr_key("UI_NEW_GAME")
LocalizationManager.resolve_text({"en": "Hello", "ja": "こんにちは", "zh": "你好", "zh-Hant": "你好"})
LocalizationManager.skill_name("tidal_slash")
LocalizationManager.speaker_name("yuzu")
```

### Signals

- `EventBus.locale_changed(locale_code)` — refresh UI when language changes
- `EventBus.vo_dialect_changed(dialect_code)` — replay VO preview if settings screen open

---


## Traditional Chinese + dialect VO

Written Traditional Chinese and spoken dialect are **separate dimensions**:

| Layer | Source | Example |
|-------|--------|---------|
| **Subtitles / UI** | `zh-Hant` keys in CSV + dialogue JSON | 你離開了。我們一直等著。 |
| **VO audio** | Same `zh-Hant` line text, dialect-specific ElevenLabs voice | `voice/zh-Hant/cant/sc03_yuzu_01.ogg` or `.../cmn/...` |

**Why not two written locales?** Cantonese and Mandarin share Traditional characters for this game's scope. Dialect affects **pronunciation and casting**, not subtitle script.

### VO file layout (zh-Hant)

```text
game/assets/audio/voice/
  en/sc03_yuzu_01.ogg
  ja/sc03_yuzu_01.ogg
  zh/sc03_yuzu_01.ogg
  zh-Hant/cant/sc03_yuzu_01.ogg    # Cantonese
  zh-Hant/cmn/sc03_yuzu_01.ogg     # Mandarin
```

**Clip totals:** 12 selective clips × 3 single-locale VO (`en`, `ja`, `zh`) + 12 × 2 dialects (`cant`, `cmn`) = **60 OGG files**.

`VoiceLinePlayer` resolves:

- `en` / `ja` / `zh` → `res://assets/audio/voice/{locale}/{voice_id}.ogg`
- `zh-Hant` → `res://assets/audio/voice/zh-Hant/{vo_dialect}/{voice_id}.ogg`

### ElevenLabs casting

Each character in `game/data/audio/vo_prompts.json` has:

- `elevenlabs_voice_id` — default (used for `en`, `ja`, `zh`)
- `dialect_voices.cant` — Cantonese voice ID (Traditional text, Yue pronunciation)
- `dialect_voices.cmn` — Mandarin voice ID (Traditional text, Putonghua pronunciation)

Cast Cantonese and Mandarin voices separately in ElevenLabs — do not reuse the Simplified Chinese (`zh`) voice for `zh-Hant` VO.

---
