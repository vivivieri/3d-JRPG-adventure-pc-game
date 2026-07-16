# Generation brief — `bgm_palace`

**Status:** Hero BGM · M5 jury scope  
**Authority:** `game/data/audio/audio_qa_catalog.json`, `game/data/audio/ace_step_prompts.json`  
**Cross-refs:** `docs/audio/AUDIO_PRODUCTION_GUIDE.md`, `docs/audio/AUDIO_DIRECTION.md`

---

## Intent (one sentence)

Sterile beautiful palace gate — uncanny major-key wrongness; harp and choir pad without vocals.

## Emotional intent (jury + human rubric)

| Field | Value |
|-------|-------|
| Primary mood | Awe, sterile perfection |
| Secondary mood | Unsettling calm — not evil carnival |
| Audience read | Men 20–30 — melancholy coastal JRPG; restrained NieR-like |
| Listen read (automated jury) | Ethereal harp, void sky mood, seamless loop |
| In-game feel (human L6 only) | Loop seam with dialogue duck; zone crossfade taste |
| Must avoid | European castle fanfare, upbeat royal parade, vocals |
| Story anchor | SC-12–SC-16 dragon_palace_gate |

---

## Tool chain

ACE-Step 1.5 → WAV → `ffmpeg` Ogg → `register_asset.py` → `AudioManager` assign.

```bash
bash tools/generate_ai_bgm.sh --track bgm_palace
python3 tools/check_audio_technical.py --track bgm_palace
python3 tools/review_audio_vision.py --track bgm_palace --min-pass 2
```

## Negative prompt (ACE-Step global + track)

vocals, lyrics, upbeat pop, EDM, bright cheerful, European fantasy brass, copyrighted melody

## Acceptance evidence

- [ ] Technical QA PASS (`check_audio_technical.py`)
- [ ] A1–A7 jury PASS on hero listen review
- [ ] 10 min Godot loop test — no click (if `loop: true`)
- [ ] Human L6 listen in target scene
