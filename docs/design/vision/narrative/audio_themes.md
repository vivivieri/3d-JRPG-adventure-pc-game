---
id: audio-themes
type: reference
audience: [narrative]
phase: [3, 6]
status: active
authority: narrative
tokens_est: 485
---
# Narrative — Audio & themes

**Hub:** [`NARRATIVE_WRITING_GUIDE.md`](../NARRATIVE_WRITING_GUIDE.md)

## 1. Audio & presentation model

| Layer | v1 ship |
|-------|---------|
| **Dialogue** | Written text — dialogue box + portraits (canonical en / ja / zh / zh-Hant) |
| **Voice acting** | **Selective short VO** — 12 emotional hit clips in **en, ja, zh, and zh-Hant** (`docs/design/vision/VO_HIT_LIST.md`); P0 clips pass `docs/design/audio/AUDIO_QA.md` §A4–A5 |
| **VO engine** | ElevenLabs AI (`tools/generate_ai_vo.py`) — not full script |
| **Music** | BGM per zone / boss (`docs/design/audio/AUDIO_PRODUCTION_GUIDE.md`) |
| **Sound** | SFX + ambient beds; SC-08 crowd = whisper bed, not voiced |

Lines with `voice_id` in `chapter_01.json` play one short clip; **all other lines stay text-only**.

### What “narrator” means

`speaker: "narrator"` is **on-screen text** by default. Only `sc14_narrator_01` has optional VO (P2 tier).

| Term in old notes | Correct v1 term |
|-------------------|-----------------|
| Spirit voice | Yuzu dialogue (text) + optional `sc03_yuzu_01` VO + reverb SFX |
| Drowned whispers (SC-08) | Layered **text** + whisper SFX bed — not 20 voice actors |
| Full voice acting | **Rejected** — hurts pacing in 2–3 h game |

**Mix implication:** Voice bus for `voice_id` clips only; duck music −6 dB (SC-16: −18 dB). Subtitles always on.

---


## 2. Themes & adaptation spine

From `GDD.md` §2 and `STORYBOARD.md`:

| Theme | How it shows in prose |
|-------|----------------------|
| Consequence over nostalgia | Village ruin before palace beauty |
| Masculine duty vs. escape | Urashima's short sentences → declarations |
| Stolen time | Box, mirror, Tide Keeper dialogue |
| No villain princess | Otohime seductive, not cruel |
| Bittersweet endings | No ending labeled “good” or “bad” |

**Folklore anchor:** Public-domain *Urashima Tarō* — spirit-turtle rescue, Dragon Palace, forbidden box, centuries passed. We darken: spirits bound to objects, box holds **village years**, not personal age alone.

---
