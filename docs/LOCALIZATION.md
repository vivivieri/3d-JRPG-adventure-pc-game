# Localization (i18n)

**Tides of Urashima** supports three languages at launch:

| Code | Language | Script |
|------|----------|--------|
| `en` | English | Latin |
| `ja` | Japanese | CJK |
| `zh` | Simplified Chinese | CJK |

Players switch language from the **main menu** (saved to `user://settings.json`).

---

## Architecture

```
game/locale/translations.csv     # UI, skills, items, combat log (single source)
game/data/dialogue/*.json        # Story text inline per locale { en, ja, zh }
game/scripts/core/localization_manager.gd   # Autoload API
```

### LocalizationManager API

```gdscript
LocalizationManager.set_locale("ja")
LocalizationManager.tr_key("UI_NEW_GAME")
LocalizationManager.resolve_text({"en": "Hello", "ja": "こんにちは", "zh": "你好"})
LocalizationManager.skill_name("tidal_slash")
LocalizationManager.speaker_name("yuzu")
```

### Signals

- `EventBus.locale_changed(locale_code)` — refresh UI when language changes

---

## Adding translations

### UI / game data strings (CSV)

Edit `game/locale/translations.csv`:

```csv
keys,en,ja,zh
skill.my_skill.name,My Skill,マイスキル,我的技能
```

**Key conventions:**

| Pattern | Example |
|---------|---------|
| `UI_*` | Menu labels |
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
    "zh": "你离开了。我们一直等着。"
  }
}
```

`DialogueRunner` emits `text_resolved` and `speaker_name` on each line.

---

## Fonts (CJK)

Japanese and Chinese use bundled **Noto Sans** fonts (OFL 1.1):

| Locale | Font files |
|--------|------------|
| `en` | `NotoSans-Regular.ttf`, `NotoSans-Bold.ttf` |
| `ja` | `NotoSansJP-Regular.otf`, `NotoSansJP-Bold.otf` |
| `zh` | `NotoSansSC-Regular.otf`, `NotoSansSC-Bold.otf` |

`FontThemeManager` autoload applies the correct font when the locale changes. See `game/assets/fonts/README.md`.

---

## Steam store

Plan separate store pages or one page with language bullets:

- English
- 日本語
- 简体中文

Tag: **Localized** (when all story scenes are translated).

---

## Translator workflow

1. Export `translations.csv` to translators (Excel / Google Sheets)
2. Keep **keys column** unchanged
3. For dialogue, provide `chapter_01.json` with empty `ja`/`zh` fields to fill
4. Run game, switch language in menu, verify no missing keys (missing keys show as raw key string)

---

## Checklist for new content

- [ ] Add CSV keys for any new skill/item/enemy/quest
- [ ] Add `en` + `ja` + `zh` dialogue text objects
- [ ] Test all three locales in menu
- [ ] Verify battle log placeholders render correctly
