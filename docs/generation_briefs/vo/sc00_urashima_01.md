# Generation brief — VO `sc00_urashima_01`

**Status:** P0 selective VO · human listen required  
**Authority:** `game/data/audio/vo_prompts.json`, `docs/VO_HIT_LIST.md`  
**Cross-refs:** `docs/NARRATIVE_WRITING_GUIDE.md`, `docs/AUDIO_PRODUCTION_GUIDE.md` §8

---

## Intent (one sentence)

Mythic promise — three days — quiet fateful, not boastful.

## Emotional intent (human rubric — no automated VO jury v1)

| Field | Value |
|-------|-------|
| Primary mood | Fateful promise |
| Speaker | Urashima |
| Line (EN) | Three days. I'll be back in three days. |
| Must avoid | Heroic swagger, comedy, horror |
| Story anchor | SC-00 prologue |

---

## Tool chain

ElevenLabs `eleven_multilingual_v2` → Ogg per locale + zh-Hant dialects.

```bash
bash tools/generate_ai_vo.sh --clip sc00_urashima_01 --locale en --locale ja --locale zh
bash tools/generate_ai_vo.sh --clip sc00_urashima_01 --locale zh-Hant --all-dialects
```

## Acceptance evidence

- [ ] P0 human listen pass all required locales
- [ ] `duck_bgm_db` verified in-engine with subtitles on
- [ ] Duration ≤ catalog `max_duration_ms`
