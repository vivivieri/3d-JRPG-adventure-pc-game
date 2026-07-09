# Fonts — Tides of Urashima

Bundled **Noto Sans** fonts (SIL Open Font License 1.1). See `OFL.txt`.

| File | Language | Use |
|------|----------|-----|
| `NotoSans-Regular.ttf` | English (Latin) | UI body |
| `NotoSans-Bold.ttf` | English (Latin) | Titles |
| `NotoSansJP-Regular.otf` | Japanese | UI body |
| `NotoSansJP-Bold.otf` | Japanese | Titles |
| `NotoSansSC-Regular.otf` | Simplified Chinese | UI body |
| `NotoSansSC-Bold.otf` | Simplified Chinese | Titles |

**Source:** [Noto CJK Sans 2.004](https://github.com/notofonts/noto-cjk/releases/tag/Sans2.004) (JP/SC), [noto-fonts](https://github.com/notofonts/noto-fonts) (Latin)

**Runtime:** `FontThemeManager` autoload switches fonts when the player changes language.

Fonts are loaded via `FontFile.load_dynamic_font()` — no manual Godot import step required.
