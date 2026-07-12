# Noto fonts (OFL)

Bundle these for en / ja / zh / zh-Hant UI (see `docs/LOCALIZATION.md`):

| File | Use |
|------|-----|
| NotoSans-Regular.ttf | Body EN |
| NotoSans-Bold.ttf | Headings EN |
| NotoSansJP-Regular.otf | Body JA |
| NotoSansJP-Bold.otf | Headings JA |
| NotoSansSC-Regular.otf | Body ZH (Simplified) |
| NotoSansSC-Bold.otf | Headings ZH (Simplified) |
| NotoSansTC-Regular.otf | Body zh-Hant (Traditional) |
| NotoSansTC-Bold.otf | Headings zh-Hant (Traditional) |

Download from [Google Noto](https://fonts.google.com/noto) or copy from a previous build.

`FontThemeManager` falls back to the engine default font when files are missing (dev boot without font bundle).

Place files here before Phase 2 UI ship. Log in `docs/LICENSES.md` (OFL).
