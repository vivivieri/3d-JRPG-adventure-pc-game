# Generation brief — VO `sc11_otohime_01`

**Status:** P0 selective VO · automated jury on `en` gate locale  
**Authority:** `game/data/audio/vo_prompts.json`, `docs/VO_HIT_LIST.md`  
**Cross-refs:** `docs/NARRATIVE_WRITING_GUIDE.md`, `docs/AUDIO_PRODUCTION_GUIDE.md` §8

---

## Intent (one sentence)

Seductive flashback — too perfect mercy; uncanny calm.

## Emotional intent (jury V6/V7 + human L6 in-engine)

| Field | Value |
|-------|-------|
| Primary mood | Seductive wrongness |
| Speaker | Otohime |
| Line (EN) | Stay, Urashima. In the palace, the world will not touch you. |
| Must avoid | Fanservice breathiness, villain cackle |
| Story anchor | SC-11 flashback |

---

## Tool chain

ElevenLabs `eleven_multilingual_v2` → Ogg per locale + zh-Hant dialects.

```bash
bash tools/generate_ai_vo.sh --clip sc11_otohime_01 --locale en --locale ja --locale zh
bash tools/generate_ai_vo.sh --clip sc11_otohime_01 --locale zh-Hant --all-dialects
```

## Acceptance evidence

- [ ] Technical QA PASS (`check_audio_vo.py`)
- [ ] V1–V7 jury PASS on `en` (`review_vo_vision.py`)
- [ ] All P0 locales technical PASS at M5 ship
- [ ] `duck_bgm_db` verified in-engine with subtitles on
- [ ] Duration ≤ catalog `max_duration_ms`
