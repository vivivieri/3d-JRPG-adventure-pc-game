---
id: tools-vs-visual
type: how-to
phase: [1, 5]
audience: [audio, qa]
status: active
authority: audio
tokens_est: 278
summary: "Tools + vs Visual QA"
---
# Audio QA — Tools + vs Visual QA

**Hub:** [`AUDIO_QA.md`](../AUDIO_QA.md)

## 6. Tools

| Tool | Role |
|------|------|
| `tools/check_audio_catalog.py` | Required track manifest per phase |
| `tools/check_audio_technical.py` | ffprobe + ffmpeg ebur128 |
| `tools/review_audio_vision.py` | Multi-LLM listen jury (hero BGM) |
| `tools/check_audio_vo.py` | P0 VO technical (duration, loudness, paths) |
| `tools/review_vo_vision.py` | Multi-LLM listen jury (P0 VO, gate locale) |
| `tools/run_audio_smoke_checks.sh` | L2 smoke wrapper (BGM + P0 VO when files exist) |

---


## 7. vs Visual QA

| | Visual | BGM | P0 VO |
|--|--------|-----|-------|
| Cheap lint | `check_scene_visuals.sh` | `check_audio_technical.py` | `check_audio_vo.py` |
| LLM jury scope | Zone screenshots | 8 hero tracks | 5 P0 clips (`en` gate) |
| Brief-driven mood | `briefs/*.md` M7/M8 | A6/A7 | V6/V7 |
| Human gate | L6 playtest | Loop + crossfade | Duck + subtitle timing |
