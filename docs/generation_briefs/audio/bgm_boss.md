# Generation brief — `bgm_boss`

**Status:** Hero BGM · M5 jury scope  
**Authority:** `game/data/audio/audio_qa_catalog.json`, `game/data/audio/ace_step_prompts.json`  
**Cross-refs:** `docs/audio/AUDIO_PRODUCTION_GUIDE.md`, `docs/audio/AUDIO_DIRECTION.md`

---

## Intent (one sentence)

Boss fight escalation — dread and pressure, not triumphant anime battle hype.

## Emotional intent (jury + human rubric)

| Field | Value |
|-------|-------|
| Primary mood | Escalating dread |
| Secondary mood | Taiko weight — not heroic victory |
| Audience read | Men 20–30 — melancholy coastal JRPG; restrained NieR-like |
| Listen read (automated jury) | Full taiko, low brass stabs, 132 BPM loop |
| In-game feel (human L6 only) | Loop seam with dialogue duck; zone crossfade taste |
| Must avoid | Triumphant anime OP, EDM drop, comedy stings |
| Story anchor | SC-09 Shore Wraith, SC-14 Sentinel, SC-15 Tide Keeper P1 |

---

## Tool chain

ACE-Step 1.5 → WAV → `ffmpeg` Ogg → `register_asset.py` → `AudioManager` assign.

```bash
bash tools/generate_ai_bgm.sh --track bgm_boss
python3 tools/check_audio_technical.py --track bgm_boss
python3 tools/review_audio_vision.py --track bgm_boss --min-pass 2
```

## Negative prompt (ACE-Step global + track)

vocals, lyrics, upbeat pop, EDM, bright cheerful, European fantasy brass, copyrighted melody

## Acceptance evidence

- [ ] Technical QA PASS (`check_audio_technical.py`)
- [ ] A1–A7 jury PASS on hero listen review
- [ ] 10 min Godot loop test — no click (if `loop: true`)
- [ ] Human L6 listen in target scene
