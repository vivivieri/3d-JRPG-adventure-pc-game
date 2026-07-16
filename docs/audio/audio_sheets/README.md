# Audio prompt sheets (ACE-Step 1.5)

Per-track generation prompts for **Tides of Urashima** BGM. Source of truth: `game/data/audio/ace_step_prompts.json`. QA targets (loudness, duration, jury scope): `game/data/audio/audio_qa_catalog.json`. Hero emotional briefs: `docs/generation_briefs/audio/`.

## Generate sheets

```bash
bash tools/generate_ai_bgm.sh --all-prompts
# or per category:
bash tools/generate_ai_bgm.sh --category opening
bash tools/generate_ai_bgm.sh --category boss_cinematic
bash tools/generate_ai_bgm.sh --category ending
```

## Categories

| Category | Tracks | Use |
|----------|--------|-----|
| `opening` | menu, prologue, `cine_opening_hero` | Title + SC-00 opening movie |
| `zone` | village, caves, palace, combat | Field loops |
| `boss` | `bgm_boss`, Tide Keeper phases | Fight loops |
| `boss_cinematic` | wraith / sentinel / tide keeper intros | Boss intro movies |
| `ending` | three endings + `cine_ending_*_hero` | SC-17 ending movies |
| `stings` | combat, boss intro, choice gate | Short hits |

## ACE-Step workflow

1. `bash tools/install_ace_step.sh`
2. `cd .cache/ace-step-1.5 && uv run acestep`
3. Open each `*.md` sheet → paste prompt, set BPM/key/duration
4. Export WAV → convert to `.ogg` per `docs/audio/AUDIO_PRODUCTION_GUIDE.md`
5. `python3 tools/check_audio_technical.py` + `review_audio_vision.py` (hero tracks) per `docs/audio/AUDIO_QA.md`
6. `python3 tools/register_asset.py` + `docs/art/LICENSES.md` (MIT / ACE-Step)

Fallback (no GPU): `bash tools/generate_ai_bgm.sh --category zone --fallback`
