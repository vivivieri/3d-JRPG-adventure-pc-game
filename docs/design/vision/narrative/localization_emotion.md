---
id: localization-emotion
type: reference
audience: [narrative]
phase: [3, 6]
status: active
authority: narrative
tokens_est: 433
---
# Narrative — Localization & emotion tags

**Hub:** [`NARRATIVE_WRITING_GUIDE.md`](../NARRATIVE_WRITING_GUIDE.md)

## 6. Localization writing (en / ja / zh / zh-Hant)

| Rule | Detail |
|------|--------|
| **Parity** | Same meaning and emotional beat across all four written locales (`zh-Hant` in `chapter_01.json`) |
| **Line count** | JA/ZH/zh-Hant may use 1–2 lines where EN uses 1; max +1 line vs EN |
| **Choice subtext** | Max 2 lines wrap (`ENDING_DESIGN.md`) |
| **Names** | Urashima, Yuzu, Roku, Otohime — consistent transliteration in CSV |
| **Folklore terms** | 龍宮 / 漆箱 / 環貝 — use established terms in JA; gloss in ZH if needed |

### JA notes

- Roku → 六さん in dialogue (respectful distance)
- Spirit speech: slightly archaic but readable (avoid heavy classical grammar)

### ZH notes (Simplified — `zh`)

- Simplified characters throughout
- 浦岛, 柚, 六, 乙姬 — fixed cast table in `LOCALIZATION.md`

### zh-Hant notes (Traditional)

- Traditional characters throughout — **not** auto-converted from `zh`
- 浦島, 柚, 六, 乙姬 — Taiwan/HK standard forms
- VO dialect (Cantonese / Mandarin) is separate from written text; subtitles always `zh-Hant`
- Cantonese VO may use spoken particles in TTS direction notes only — subtitles stay literary Traditional

### QA

- No raw `UI_*` keys in ship build
- Playtest 1/4 per written language + both zh-Hant dialects (`PLAYTEST_SCRIPT.md`)

---


## 7. Emotion tags (`emotion` field)

Use in `chapter_01.json` for portrait selection:

| Tag | Portrait lean |
|-----|---------------|
| `neutral` | Default / narrator |
| `uneasy` | Urashima wary |
| `confused` | Urashima lost |
| `guilty` | Urashima shame |
| `weary` | Urashima exhausted |
| `accusatory` | Yuzu SC-03 |
| `sorrow` | Yuzu melancholy |
| `grim` | Roku |
| `urgent` | Roku warning |
| `wonder` | Narrator awe |
| `dread` | Horror beats |

---
