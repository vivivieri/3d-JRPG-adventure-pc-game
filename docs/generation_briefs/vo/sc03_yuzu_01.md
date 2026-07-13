# Generation brief — VO `sc03_yuzu_01`

**Status:** P0 selective VO · automated jury on `en` gate locale  
**Authority:** `game/data/audio/vo_prompts.json`, `docs/VO_HIT_LIST.md`  
**Cross-refs:** `docs/NARRATIVE_WRITING_GUIDE.md`, `docs/AUDIO_PRODUCTION_GUIDE.md` §8

---

## Intent (one sentence)

First accusation — still, sharp grief; not bright heroine.

## Emotional intent (jury V6/V7 + human L6 in-engine)

| Field | Value |
|-------|-------|
| Primary mood | Quiet accusation |
| Speaker | Yuzu |
| Line (EN) | You left. We waited. |
| Must avoid | Tsundere comedy, cheerful anime girl |
| Story anchor | SC-03 village encounter |

---

## Tool chain

ElevenLabs `eleven_multilingual_v2` → Ogg per locale + zh-Hant dialects.

```bash
bash tools/generate_ai_vo.sh --clip sc03_yuzu_01 --locale en --locale ja --locale zh
bash tools/generate_ai_vo.sh --clip sc03_yuzu_01 --locale zh-Hant --all-dialects
```

## Acceptance evidence

- [ ] Technical QA PASS (`check_audio_vo.py`)
- [ ] V1–V7 jury PASS on `en` (`review_vo_vision.py`)
- [ ] All P0 locales technical PASS at M5 ship
- [ ] `duck_bgm_db` verified in-engine with subtitles on
- [ ] Duration ≤ catalog `max_duration_ms`
