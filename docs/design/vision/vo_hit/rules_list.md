---
id: rules-list
type: reference
phase: [1, 6]
audience: [audio, narrative]
status: active
authority: vision
tokens_est: 649
summary: "Design rules + 12-clip list"
---
# Selective VO Hit List — Design rules + 12-clip list

**Hub:** [`VO_HIT_LIST.md`](../VO_HIT_LIST.md)

## Design rules

| Rule | Detail |
|------|--------|
| **All written locales have VO** | **en**, **ja**, **zh**, and **zh-Hant** each ship audio for every hit-list clip — 60 OGG files total |
| One VO clip per scene max | Remaining lines in scene stay text-only |
| Length | ~1–6 seconds spoken |
| Subtitles | Always on (en / ja / zh / zh-Hant text canonical) |
| Voice follows locale | `en`/`ja`/`zh` → `voice/{locale}/`; `zh-Hant` → `voice/zh-Hant/{cant\|cmn}/` |
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
| **P0** | `sc04_roku_01` | SC-04 | Roku | That box isn't a gift. Don't open it. | 4s |
| **P0** | `sc16_tide_keeper_01` | SC-16 | Tide Keeper | The tide waits. So did they. | 3s |
| **P1** | `sc01_urashima_01` | SC-01 / SC-17c | Urashima | Three days... (shore echo / drift ending) | 3s |
| **P1** | `sc08_urashima_01` | SC-08 | Urashima | I know you. I left you all behind. | 3s |
| **P1** | `sc09_shore_wraith_01` | SC-09 | Shore Wraith | You chose the palace over us. | 2s |
| **P1** | `sc10_yuzu_01` | SC-10 | Yuzu | I can't rest until the tide is answered. | 4s |
| **P1** | `sc15_tide_keeper_01` | SC-15 | Tide Keeper | Paradise is mercy. You fled pain — I offered peace. | 5s |
| **P2** | `sc14_narrator_01` | SC-14 | Narrator | No mortal leaves with stolen time. | 3s |

**Totals:** 12 clips × **3 primary VO locales** (`en`, `ja`, `zh`) + 12 clips × **2 zh-Hant dialects** (`cant`, `cmn`) = **60 OGG files**
**Not optional:** English, Japanese, and Simplified Chinese each require a full clip set — same 12 `voice_id` lines as zh-Hant.
**Text-only by design:** SC-02 inspectables, SC-05–07, SC-12 gate (music), SC-17 endings, choice UI

---
