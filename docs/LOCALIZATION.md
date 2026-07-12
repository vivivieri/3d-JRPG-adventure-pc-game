# Localization (i18n)

**Tides of Urashima** supports four written languages at launch:

| Code | Language | Script | VO |
|------|----------|--------|-----|
| `en` | English | Latin | English TTS |
| `ja` | Japanese | CJK | Japanese TTS |
| `zh` | Simplified Chinese | CJK (NotoSansSC) | Mandarin TTS |
| `zh-Hant` | Traditional Chinese | CJK (NotoSansTC) | **Cantonese or Mandarin** (player choice) |

Players switch **written language** from the **main menu** (saved to `user://settings.json`). When `zh-Hant` is selected, a second setting — **voice dialect** — offers **粵語 (Cantonese)** or **國語 (Mandarin)** for the 12 selective VO clips. Subtitles always use Traditional Chinese text regardless of dialect.

> **Ship data:** `game/data/**` JSON and `game/locale/translations.csv` include `en` / `ja` / `zh` / `zh-Hant` inline text. VO clips for `zh-Hant` (`cant` / `cmn`) are generated in Phase 7 (`docs/VO_HIT_LIST.md`).

---

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

## Adding translations

### UI / game data strings (CSV)

Edit `game/locale/translations.csv`:

```csv
keys,en,ja,zh,zh-Hant
skill.my_skill.name,My Skill,マイスキル,我的技能,我的技能
UI_VOICE_DIALECT_CANT,Cantonese,広東語,粤语,粵語
UI_VOICE_DIALECT_CMN,Mandarin,普通話,普通话,國語
```

**Key conventions:**

| Pattern | Example |
|---------|---------|
| `UI_*` | Menu labels |
| `UI_VOICE_DIALECT_*` | Dialect picker labels (zh-Hant settings only) |
| `speaker.{id}` | Character speaker names in dialogue |
| `character.{id}.name` | Party display names |
| `skill.{id}.name` / `.desc` | Skills |
| `enemy.{id}.name` | Enemies |
| `item.{id}.name` / `.desc` | Items |
| `quest.{id}.title` / `.desc` | Quests |
| `quest.{id}.stage.{stage_id}` | Quest stage text |
| `combat.*` | Battle log (use `{placeholder}` syntax) |
| `status.*` | Status effect names |

### Dialogue (JSON)

Use per-locale objects on the `text` field:

```json
{
  "speaker": "yuzu",
  "text": {
    "en": "You left. We waited.",
    "ja": "あなたは去った。私たちは待っていた。",
    "zh": "你离开了。我们一直等着。",
    "zh-Hant": "你離開了。我們一直等著。"
  }
}
```

`DialogueRunner` emits `text_resolved` and `speaker_name` on each line.

**Simplified vs Traditional:** `zh` and `zh-Hant` are maintained as separate strings — do not auto-convert at runtime. Taiwan/HK word choice may differ (e.g. 軟體 vs 软件).

---

## Fonts (CJK)

Japanese and Chinese use bundled **Noto Sans** fonts (OFL 1.1):

| Locale | Font files |
|--------|------------|
| `en` | `NotoSans-Regular.ttf`, `NotoSans-Bold.ttf` |
| `ja` | `NotoSansJP-Regular.otf`, `NotoSansJP-Bold.otf` |
| `zh` | `NotoSansSC-Regular.otf`, `NotoSansSC-Bold.otf` |
| `zh-Hant` | `NotoSansTC-Regular.otf`, `NotoSansTC-Bold.otf` |

When dialogue is active, `DialogueBox` (CanvasLayer) shows speaker + typewriter text. Advance with **Space / Enter / E**.

- Scene: `game/scenes/ui/dialogue_box.tscn`
- Autoload: `DialogueUiManager` attaches overlay to root viewport
- Signals: `dialogue_started`, `dialogue_line`, `dialogue_finished`
- Fonts: `FontThemeManager.apply_dialogue_*` on locale change

---

## Steam store

Plan separate store pages or one page with language bullets:

- English
- 日本語
- 简体中文
- 繁體中文（粵語／國語配音）

Tag: **Localized** (when all story scenes are translated).

---

## Translator workflow

1. Export `translations.csv` to translators (Excel / Google Sheets)
2. Keep **keys column** unchanged
3. For dialogue, provide `chapter_01.json` with empty `ja` / `zh` / `zh-Hant` fields to fill
4. **Traditional Chinese pass** is separate from Simplified — assign a TW/HK translator, not auto-convert
5. Run game, switch language in menu, verify no missing keys (missing keys show as raw key string)
6. VO: generate Cantonese and Mandarin clips separately (`tools/generate_ai_vo.sh --locale zh-Hant --dialect cant`)

---

## Checklist for new content

- [ ] Add CSV keys for any new skill/item/enemy/quest (all four locale columns)
- [ ] Add `en` + `ja` + `zh` + `zh-Hant` dialogue text objects
- [ ] Test all four written locales in menu
- [ ] Test both `cant` and `cmn` VO under `zh-Hant`
- [ ] Verify battle log placeholders render correctly
- [ ] Verify NotoSansTC renders 繁體字 without tofu
