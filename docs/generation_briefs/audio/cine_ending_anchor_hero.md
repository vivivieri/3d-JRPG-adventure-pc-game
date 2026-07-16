# Generation brief — `cine_ending_anchor_hero`

**Status:** Hero BGM · M5 jury scope  
**Authority:** `game/data/audio/audio_qa_catalog.json`, `game/data/audio/ace_step_prompts.json`  
**Cross-refs:** `docs/audio/AUDIO_PRODUCTION_GUIDE.md`, `docs/audio/AUDIO_DIRECTION.md`

---

## Intent (one sentence)

SC-17b Anchor ending — dawn hope, imperfect rebuild, honest slow growth.

## Emotional intent (jury + human rubric)

| Field | Value |
|-------|-------|
| Primary mood | Restrained hope |
| Secondary mood | Scarred accountability |
| Audience read | Men 20–30 — melancholy coastal JRPG; restrained NieR-like |
| Listen read (automated jury) | Warm dawn orchestral+koto, sapling beat |
| In-game feel (human L6 only) | Loop seam with dialogue duck; zone crossfade taste |
| Must avoid | Disney triumph, saccharine pop, vocals |
| Story anchor | SC-17b Anchor |

---

## Tool chain

ACE-Step 1.5 → WAV → `ffmpeg` Ogg → `register_asset.py` → `AudioManager` assign.

```bash
bash tools/generate_ai_bgm.sh --track cine_ending_anchor_hero
python3 tools/check_audio_technical.py --track cine_ending_anchor_hero
python3 tools/review_audio_vision.py --track cine_ending_anchor_hero --min-pass 2
```

## Negative prompt (ACE-Step global + track)

vocals, lyrics, upbeat pop, EDM, bright cheerful, European fantasy brass, copyrighted melody

## Acceptance evidence

- [ ] Technical QA PASS (`check_audio_technical.py`)
- [ ] A1–A7 jury PASS on hero listen review
- [ ] 10 min Godot loop test — no click (if `loop: true`)
- [ ] Human L6 listen in target scene
