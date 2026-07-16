# Generation brief — VO `sc16_tide_keeper_01`

**Status:** P0 selective VO · automated jury on `en` gate locale  
**Authority:** `game/data/audio/vo_prompts.json`, `docs/vision/VO_HIT_LIST.md`  
**Cross-refs:** `docs/vision/NARRATIVE_WRITING_GUIDE.md`, `docs/audio/AUDIO_PRODUCTION_GUIDE.md` §8

---

## Intent (one sentence)

Choice gate whisper — near silence, slow tragic authority.

## Emotional intent (jury V6/V7 + human L6 in-engine)

| Field | Value |
|-------|-------|
| Primary mood | Exhausted mercy |
| Speaker | Tide Keeper |
| Line (EN) | The tide waits. So did they. |
| Must avoid | Shouting boss, modern tech metaphors |
| Story anchor | SC-16 choice freeze |

---

## Tool chain

ElevenLabs `eleven_multilingual_v2` → Ogg per locale + zh-Hant dialects.

```bash
bash tools/generate_ai_vo.sh --clip sc16_tide_keeper_01 --locale en --locale ja --locale zh
bash tools/generate_ai_vo.sh --clip sc16_tide_keeper_01 --locale zh-Hant --all-dialects
```

## Acceptance evidence

- [ ] Technical QA PASS (`check_audio_vo.py`)
- [ ] V1–V7 jury PASS on `en` (`review_vo_vision.py`)
- [ ] All P0 locales technical PASS at M5 ship
- [ ] `duck_bgm_db` verified in-engine with subtitles on
- [ ] Duration ≤ catalog `max_duration_ms`
