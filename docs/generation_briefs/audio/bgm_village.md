# Generation brief — `bgm_village`

**Status:** Hero BGM · M5 jury scope  
**Authority:** `game/data/audio/audio_qa_catalog.json`, `game/data/audio/ace_step_prompts.json`  
**Cross-refs:** `docs/AUDIO_PRODUCTION_GUIDE.md`, `docs/AUDIO_DIRECTION.md`

---

## Intent (one sentence)

Empty coastal dread — wind, decay, grey overcast hub field loop for beach and ruined village.

## Emotional intent (jury + human rubric)

| Field | Value |
|-------|-------|
| Primary mood | Empty dread, submerged grief |
| Secondary mood | Faint wind texture — not comfort |
| Audience read | Men 20–30 — melancholy coastal JRPG; restrained NieR-like |
| Listen read (automated jury) | Shakuhachi + low drone; muted grey; seamless loop |
| In-game feel (human L6 only) | Loop seam with dialogue duck; zone crossfade taste |
| Must avoid | Upbeat adventure, sunny Ghibli, EDM, vocals, heroic fanfare |
| Story anchor | SC-01–SC-05 field exploration |

---

## Tool chain

ACE-Step 1.5 → WAV → `ffmpeg` Ogg → `register_asset.py` → `AudioManager` assign.

```bash
bash tools/generate_ai_bgm.sh --track bgm_village
python3 tools/check_audio_technical.py --track bgm_village
python3 tools/review_audio_vision.py --track bgm_village --min-pass 2
```

## Negative prompt (ACE-Step global + track)

vocals, lyrics, upbeat pop, EDM, bright cheerful, European fantasy brass, copyrighted melody

## Acceptance evidence

- [ ] Technical QA PASS (`check_audio_technical.py`)
- [ ] A1–A7 jury PASS on hero listen review
- [ ] 10 min Godot loop test — no click (if `loop: true`)
- [ ] Human L6 listen in target scene
