# Generation brief — VO `sc03_yuzu_01`

**Status:** P0 selective VO · human listen required  
**Authority:** `game/data/audio/vo_prompts.json`, `docs/VO_HIT_LIST.md`  
**Cross-refs:** `docs/NARRATIVE_WRITING_GUIDE.md`, `docs/AUDIO_PRODUCTION_GUIDE.md` §8

---

## Intent (one sentence)

First accusation — still, sharp grief; not bright heroine.

## Emotional intent (human rubric — no automated VO jury v1)

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

- [ ] P0 human listen pass all required locales
- [ ] `duck_bgm_db` verified in-engine with subtitles on
- [ ] Duration ≤ catalog `max_duration_ms`
