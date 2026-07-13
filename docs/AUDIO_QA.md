# Audio QA — Technical Gates + Optional LLM Jury

**Version:** 1.0  
**Problem:** An agent can register `bgm_village.ogg` without listening — often a **procedural sine placeholder** or wrong loudness that ships everywhere.

**Rule:** Audio tasks pass **catalog + technical checks** first. **Hero BGM** may use optional **multi-LLM listen jury**. Human **L6** still owns in-game mix feel.

**Cross-refs:** `docs/AUDIO_PRODUCTION_GUIDE.md`, `docs/AUDIO_DIRECTION.md`, `docs/VISUAL_QA.md`, `docs/QA_REMEDIATION_LOOP.md`, `docs/ACCEPTANCE_CRITERIA.md`, `game/data/audio/ace_step_prompts.json`

---

## 1. What to automate vs human

| Automate (objective) | Human L6 (subjective) |
|----------------------|------------------------|
| File exists, correct name | Loop feel with dialogue ducking |
| Ogg 44.1 kHz, not clipped | Boss tension vs difficulty |
| LUFS / true peak targets | Ending emotional landing |
| Duration in expected range | Zone crossfade taste |
| Not dev procedural placeholder on ship | Controller + mix comfort |
| Hero mood (optional LLM jury) | Full playthrough listen |

**Do not** run multi-LLM jury on every footstep SFX — cost/noise too high.

---

## 2. Defense layers

```
A1  check_audio_catalog.py     → required tracks exist for phase
A2  check_audio_technical.py   → LUFS, peak, format, duration, placeholder flag
A3  review_audio_vision.py      → optional 2-of-N LLM listen (hero BGM only)
L6  PLAYTEST_SCRIPT.md          → human listen after L0–L5
```

### Layer A1 — Catalog

```bash
python3 tools/check_audio_catalog.py --phase 1
python3 tools/check_audio_catalog.py --phase m5
```

| Phase | Required (minimum) |
|-------|-------------------|
| **1** (vertical slice) | `bgm_village` |
| **m5** (ship) | All tracks in `game/data/audio/ace_step_prompts.json` |

### Layer A2 — Technical

```bash
python3 tools/check_audio_technical.py --track bgm_village
python3 tools/check_audio_technical.py --all-present
```

| Bus (path) | Integrated LUFS | True peak |
|------------|-----------------|-----------|
| `bgm/` | −16 ± 4 LU | ≤ −1.0 dBTP |
| `stings/` (short) | — | ≤ −3.0 dBTP |
| `sfx/` | — | ≤ −6.0 dBFS |
| `voice/` | −18 ± 4 LU | ≤ −3.0 dBTP |
| `amb/` | −22 ± 4 LU | ≤ −6.0 dBTP |

**Placeholder rule:** manifest `source` contains `generate_game_audio.py` → **WARN** in dev smoke, **FAIL** with `--ship` (M5 gate).

### Layer A3 — Multi-LLM listen jury (hero BGM only)

```bash
python3 tools/review_audio_vision.py \
  --track bgm_village \
  --min-pass 2
```

**Hero tracks (jury scope):**

- `bgm_village`, `bgm_caves`, `bgm_palace`
- `cine_opening_hero`
- `cine_ending_rewind_hero`, `cine_ending_anchor_hero`, `cine_ending_drift_hero`
- `bgm_boss`

**API keys:** `OPENAI_API_KEY`, `GEMINI_API_KEY` (audio-capable vision models). No Anthropic audio path in v1.

**Pass:** ≥2 models `acceptance.valid_pass: true` (A1–A7 + confidence ≥ 0.65). Gate `L2_audio_jury`.

Emotional intent for hero tracks loads from `docs/generation_briefs/audio/<track>.md` via `audio_brief_lib.py` (A6/A7 — same pattern as model M7/M8).

### Layer L6 — Human

Loop seam in Godot 10 min, SC-16 duck, three endings — `docs/AUDIO_PRODUCTION_GUIDE.md` §11.

---

## 3. L2 smoke integration

```bash
bash tools/run_audio_smoke_checks.sh
```

| State | Behavior |
|-------|----------|
| No `bgm_village.ogg` | **WARN** — skip (Phase 1 not ready) |
| Placeholder + dev mode | **WARN** — replace with ACE-Step before M5 |
| Placeholder + `--ship` | **FAIL** |
| ACE-Step export wrong LUFS | **FAIL** |
| Hero jury, no API keys | **WARN** — manual packet |

Wired into `bash tools/run_playtest_smoke.sh`.

---

## 4. Agent workflow (audio task)

```
1. bash tools/generate_ai_bgm.sh --track bgm_village --api  (or ACE-Step export)
2. Loudness normalize toward −16 LUFS in DAW/ffmpeg if needed
3. python3 tools/register_asset.py add --path <path> --license <id> --source <name> --author <name> --used-for <desc>
4. python3 tools/check_audio_catalog.py --phase 1
5. python3 tools/check_audio_technical.py --track bgm_village
6. python3 tools/review_audio_vision.py --track bgm_village  (hero tracks)
7. GDAI MCP — wire in editor, F5 zone test
```

---

## 5. Agent report template

```
[AUDIO QA] track=bgm_village
  catalog phase1: PASS
  technical: PASS (I=-16.2 LUFS, peak=-2.1 dBTP)
  placeholder: NO (ACE-Step)
  jury: PASS (2/2) — artifacts/audio_reviews/bgm_village.jury.json
  result: PASS
```

---

## 6. Tools

| Tool | Role |
|------|------|
| `tools/check_audio_catalog.py` | Required track manifest per phase |
| `tools/check_audio_technical.py` | ffprobe + ffmpeg ebur128 |
| `tools/review_audio_vision.py` | Multi-LLM listen jury (hero BGM) |
| `tools/run_audio_smoke_checks.sh` | L2 smoke wrapper |

---

## 7. vs Visual QA

| | Visual | Audio |
|--|--------|-------|
| Cheap lint | `check_scene_visuals.sh` | `check_audio_technical.py` |
| LLM jury scope | Every zone screenshot | **8 hero BGMs only** |
| Golden reference | PNG compare | Optional reference WAV (future) |
| Human gate | L6 playtest | L6 listen + loop test |
