---
id: translations-fonts
type: how-to
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, narrative, builder]
status: active
authority: engineering
tokens_est: 591
summary: "Adding translations + CJK fonts"
---
# Localization — Adding translations + CJK fonts

**Hub:** [`LOCALIZATION.md`](../LOCALIZATION.md)

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
