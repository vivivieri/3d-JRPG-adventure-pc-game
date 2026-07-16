# Generation brief — `cine_opening_hero`

**Status:** Hero BGM · M5 jury scope  
**Authority:** `game/data/audio/audio_qa_catalog.json`, `game/data/audio/ace_step_prompts.json`  
**Cross-refs:** `docs/audio/AUDIO_PRODUCTION_GUIDE.md`, `docs/audio/AUDIO_DIRECTION.md`

---

## Intent (one sentence)

SC-00 opening montage hero score — mythic gift of lacquer box, swell then ominous turn.

## Emotional intent (jury + human rubric)

| Field | Value |
|-------|-------|
| Primary mood | Mythic fate |
| Secondary mood | Ominous undertone after beauty |
| Audience read | Men 20–30 — melancholy coastal JRPG; restrained NieR-like |
| Listen read (automated jury) | Orchestral swell, shamisen accents, non-loop film intro |
| In-game feel (human L6 only) | Loop seam with dialogue duck; zone crossfade taste |
| Must avoid | Disney adventure, vocals, upbeat pop |
| Story anchor | SC-00 prologue cinematic |

---

## Tool chain

ACE-Step 1.5 → WAV → `ffmpeg` Ogg → `register_asset.py` → `AudioManager` assign.

```bash
bash tools/generate_ai_bgm.sh --track cine_opening_hero
python3 tools/check_audio_technical.py --track cine_opening_hero
python3 tools/review_audio_vision.py --track cine_opening_hero --min-pass 2
```

## Negative prompt (ACE-Step global + track)

vocals, lyrics, upbeat pop, EDM, bright cheerful, European fantasy brass, copyrighted melody

## Acceptance evidence

- [ ] Technical QA PASS (`check_audio_technical.py`)
- [ ] A1–A7 jury PASS on hero listen review
- [ ] 10 min Godot loop test — no click (if `loop: true`)
- [ ] Human L6 listen in target scene
