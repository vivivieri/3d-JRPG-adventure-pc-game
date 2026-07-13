# Generation brief — VO `sc16_tide_keeper_01`

**Status:** P0 selective VO · human listen required  
**Authority:** `game/data/audio/vo_prompts.json`, `docs/VO_HIT_LIST.md`  
**Cross-refs:** `docs/NARRATIVE_WRITING_GUIDE.md`, `docs/AUDIO_PRODUCTION_GUIDE.md` §8

---

## Intent (one sentence)

Choice gate whisper — near silence, slow tragic authority.

## Emotional intent (human rubric — no automated VO jury v1)

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

- [ ] P0 human listen pass all required locales
- [ ] `duck_bgm_db` verified in-engine with subtitles on
- [ ] Duration ≤ catalog `max_duration_ms`
