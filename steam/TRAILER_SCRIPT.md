# Tides of Urashima — Marketing Trailer Script

**Version:** 1.0  
**Target length:** ~75 seconds  
**Output:** `steam/trailer.mp4` (1920×1080, H.264)  
**Source art:** `docs/pitch/illustrations/`  
**Generator:** `python3 tools/generate_marketing_trailer.py`

---

## Hook

*The sea returns what it claims.*

A fisherman visits the Dragon Palace for three days — and returns to find his village erased by centuries. **Tides of Urashima** is a 2–3 hour stylized JRPG about consequence, memory, and the price of paradise.

---

## Beat sheet (on-screen text)

| # | Visual | Duration | Headline | Subline |
|---|--------|----------|----------|---------|
| 1 | Title card | 2.5s | **TIDES OF URASHIMA** | A dark Urashima Tarō JRPG |
| 2 | Party lineup | 4.0s | He left for three days. | Centuries had passed. |
| 3 | SC-00 | 3.5s | He saved a wounded spirit. | Paradise gave him a lacquer box. |
| 4 | SC-01 | 3.5s | The sea spat him ashore. | Alone. |
| 5 | SC-02 | 3.0s | His village was gone. | |
| 6 | SC-03 | 3.0s | You left. We waited. | |
| 7 | SC-04 | 3.0s | That box isn't a gift. | Don't open it. |
| 8 | SC-05 | 2.5s | Turn-based combat | Speed · Skills · Strategy |
| 9 | SC-06 | 2.5s | Descend the Tidal Caves. | |
| 10 | SC-07 | 2.0s | | *(silent beat — puzzle)* |
| 11 | SC-08 | 3.0s | The drowned remember. | |
| 12 | SC-09 | 3.5s | Confront the Shore Wraith. | Boss phases · Intent UI |
| 13 | SC-10 | 2.5s | Spirits join the fight. | |
| 14 | SC-11 | 3.0s | Paradise was too perfect. | |
| 15 | SC-12 | 3.5s | The Dragon Palace Gate. | |
| 16 | SC-13 | 3.0s | The box holds stolen years. | |
| 17 | SC-14 | 2.5s | Palace Sentinel | |
| 18 | SC-15 | 3.0s | The Tide Keeper waits. | |
| 19 | SC-16 | 4.0s | Three endings. One choice. | Who pays for stolen time? |
| 20 | SC-17a | 2.0s | **REWIND** | Restore the village |
| 21 | SC-17b | 2.0s | **ANCHOR** | Bind the spirits |
| 22 | SC-17c | 2.0s | **DRIFT** | Refuse the bargain |
| 23 | Party lineup | 4.5s | 2–3 hours · 3 endings | Walk the shore. Answer the tide. |

**Total:** ~75 seconds

---

## Voice-over note

Trailer uses **on-screen text only** (matches game: no VO). Optional future: record narrator reading headline lines.

---

## Localization

v1 trailer is **English only**. For JP/ZH store pages, duplicate script in `TRAILER_SCRIPT_ja.md` / `TRAILER_SCRIPT_zh.md` when localized renders are needed.

---

## Regenerate

```bash
python3 tools/generate_marketing_trailer.py
# Output: steam/trailer.mp4
```

Requires: `ffmpeg`, illustrations in `docs/pitch/illustrations/`
