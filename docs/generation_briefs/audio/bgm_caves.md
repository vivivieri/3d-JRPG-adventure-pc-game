# Generation brief — `bgm_caves`

**Status:** Hero BGM · M5 jury scope  
**Authority:** `game/data/audio/audio_qa_catalog.json`, `game/data/audio/ace_step_prompts.json`  
**Cross-refs:** `docs/audio/AUDIO_PRODUCTION_GUIDE.md`, `docs/audio/AUDIO_DIRECTION.md`

---

## Intent (one sentence)

Tidal caves exploration — wonder mixed with unease; biolume chimes under dripping dark.

## Emotional intent (jury + human rubric)

| Field | Value |
|-------|-------|
| Primary mood | Wonder and wrongness |
| Secondary mood | Biolume curiosity — not horror gore |
| Audience read | Men 20–30 — melancholy coastal JRPG; restrained NieR-like |
| Listen read (automated jury) | Water bells, drip atmosphere, 78 BPM loop |
| In-game feel (human L6 only) | Loop seam with dialogue duck; zone crossfade taste |
| Must avoid | Horror jump-scare stingers, bright fantasy dungeon, metal |
| Story anchor | SC-06–SC-10 tidal_caves |

---

## Tool chain

ACE-Step 1.5 → WAV → `ffmpeg` Ogg → `register_asset.py` → `AudioManager` assign.

```bash
bash tools/generate_ai_bgm.sh --track bgm_caves
python3 tools/check_audio_technical.py --track bgm_caves
python3 tools/review_audio_vision.py --track bgm_caves --min-pass 2
```

## Negative prompt (ACE-Step global + track)

vocals, lyrics, upbeat pop, EDM, bright cheerful, European fantasy brass, copyrighted melody

## Acceptance evidence

- [ ] Technical QA PASS (`check_audio_technical.py`)
- [ ] A1–A7 jury PASS on hero listen review
- [ ] 10 min Godot loop test — no click (if `loop: true`)
- [ ] Human L6 listen in target scene
