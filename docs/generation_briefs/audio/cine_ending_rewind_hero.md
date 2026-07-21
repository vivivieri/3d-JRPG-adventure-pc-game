# Generation brief — `cine_ending_rewind_hero`

**Status:** Hero BGM · M5 jury scope
**Authority:** `game/data/audio/audio_qa_catalog.json`, `game/data/audio/ace_step_prompts.json`
**Cross-refs:** `docs/audio/AUDIO_PRODUCTION_GUIDE.md`, `docs/audio/AUDIO_DIRECTION.md`

---

## Intent (one sentence)

SC-17a Rewind ending cinematic — bittersweet festival restored, gift costs self.

## Emotional intent (jury + human rubric)

| Field | Value |
|-------|-------|
| Primary mood | Bittersweet nostalgia |
| Secondary mood | Crowd warmth with personal loss |
| Audience read | Men 20–30 — melancholy coastal JRPG; restrained NieR-like |
| Listen read (automated jury) | Festival swell, folk instruments, crane-up dissolve |
| In-game feel (human L6 only) | Loop seam with dialogue duck; zone crossfade taste |
| Must avoid | Pure happy ending, comedy, vocals |
| Story anchor | SC-17a Rewind |

---

## Tool chain

ACE-Step 1.5 → WAV → `ffmpeg` Ogg → `register_asset.py` → `AudioManager` assign.

```bash
bash tools/generate_ai_bgm.sh --track cine_ending_rewind_hero
python3 tools/check_audio_technical.py --track cine_ending_rewind_hero
python3 tools/review_audio_vision.py --track cine_ending_rewind_hero --min-pass 2
```

## Negative prompt (ACE-Step global + track)

vocals, lyrics, upbeat pop, EDM, bright cheerful, European fantasy brass, copyrighted melody

## Acceptance evidence

- [ ] Technical QA PASS (`check_audio_technical.py`)
- [ ] A1–A7 jury PASS on hero listen review
- [ ] 10 min Godot loop test — no click (if `loop: true`)
- [ ] Human L6 listen in target scene
