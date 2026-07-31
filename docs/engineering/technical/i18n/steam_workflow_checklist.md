---
id: steam-workflow-checklist
type: how-to
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, narrative, builder]
status: active
authority: engineering
tokens_est: 440
summary: "Localization — Steam, translator workflow, checklist — Plan separate store pages or one page with language bullets:"
---
# Localization — Steam, translator workflow, checklist

**Hub:** [`LOCALIZATION.md`](../LOCALIZATION.md)

## When to read

Use **Localization — Steam, translator workflow, checklist** (roles: architect, narrative, builder) when executing this procedure Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [Steam store](#steam-store)
- [Translator workflow](#translator-workflow)
- [Checklist for new content](#checklist-for-new-content)


## Steam store

Plan separate store pages or one page with language bullets:

- English
- 日本語
- 简体中文
- 繁體中文（粵語／國語配音）

**Marketing trailers:** `steam/trailer.mp4` (EN), `trailer_ja.mp4`, `trailer_zh.mp4` (Simplified), `trailer_zh-Hant.mp4` (Traditional) — on-screen text only; see `steam/TRAILER_SCRIPT.md`.

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
