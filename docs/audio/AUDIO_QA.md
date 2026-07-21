# Audio QA — Technical Gates + Optional LLM Jury

**Version:** 1.1
**Problem:** An agent can register `bgm_village.ogg` or `sc00_urashima_01.ogg` without listening — often a **procedural sine placeholder**, wrong loudness, or off-direction VO that ships everywhere.

**Rule:** Audio tasks pass **catalog + technical checks** first. **Hero BGM** and **P0 VO** use optional **multi-LLM listen jury** (scoped — not every SFX). Human **L6** still owns in-game mix feel.

**Cross-refs:** `docs/audio/AUDIO_PRODUCTION_GUIDE.md`, `docs/audio/AUDIO_DIRECTION.md`, `docs/art/VISUAL_QA.md`, `docs/qa/QA_REMEDIATION_LOOP.md`, `docs/qa/ACCEPTANCE_CRITERIA.md`, `game/data/audio/ace_step_prompts.json`

---

## 1. What to automate vs human

| Automate (objective) | Human L6 (subjective) |
|----------------------|------------------------|
| File exists, correct name | Loop feel with dialogue ducking |
| Ogg 44.1 kHz, not clipped | Boss tension vs difficulty |
| LUFS / true peak targets | Ending emotional landing |
| Duration in expected range | Zone crossfade taste |
| Not dev procedural placeholder on ship | Controller + mix comfort |
| Hero BGM mood (LLM jury) | P0 VO performance + script semantics (LLM jury, `en` gate) |
| P0 VO duration / loudness / locale paths | Subtitle timing + duck mix in-engine |

**Do not** run multi-LLM jury on every footstep SFX or every locale variant — cost/noise too high. Gate locale for VO jury: **`en`** (all locales still get technical lint at M5 ship).

---

## 2. Defense layers

```
A1  check_audio_catalog.py     → required BGM tracks exist for phase
A2  check_audio_technical.py   → LUFS, peak, format, duration, placeholder flag (BGM/SFX)
A3  review_audio_vision.py      → 2-of-N LLM listen (hero BGM only)
A4  check_audio_vo.py           → P0 VO duration, loudness, locale paths vs dialogue script
A5  review_vo_vision.py         → 2-of-N LLM listen (P0 VO, gate locale en)
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

### Layer A4 — P0 VO technical

```bash
python3 tools/check_audio_vo.py --clip sc00_urashima_01 --locale en
python3 tools/check_audio_vo.py --all-p0 --ship
```

| Check | Fail if |
|-------|---------|
| Path | Missing `game/assets/audio/voice/{locale}/{clip_id}.ogg` (all P0 locales at M5 ship) |
| Duration | Exceeds `max_duration_sec` in `audio_qa_catalog.json` |
| Script | No dialogue line in `chapter_01.json` for clip/locale |
| Loudness | Voice bus outside −18 ± 4 LUFS or peak > −3 dBTP |

Gate: `L2_vo_technical`.

### Layer A5 — Multi-LLM listen jury (P0 VO, gate locale `en`)

```bash
python3 tools/review_vo_vision.py \
  --clip sc00_urashima_01 \
  --locale en \
  --min-pass 2
```

**P0 clips (jury scope):** `sc00_urashima_01`, `sc03_yuzu_01`, `sc11_otohime_01`, `sc13_roku_01`, `sc16_tide_keeper_01`

**Pass:** ≥2 models `acceptance.valid_pass: true` (V1–V7 + confidence ≥ 0.65). Gate `L2_vo_jury`.

V2 checks **semantic** script match (not word-perfect for `ja`/`zh`). V6/V7 load from `docs/generation_briefs/vo/<clip>.md` (same brief pattern as BGM A6/A7).

### Layer L6 — Human

Loop seam in Godot 10 min, SC-16 duck, three endings — `docs/audio/AUDIO_PRODUCTION_GUIDE.md` §11.

---

## 3. L2 smoke integration

```bash
bash tools/run_audio_smoke_checks.sh
```

| State | Behavior |
|-------|----------|
| No `bgm_village.ogg` | **WARN** — BGM smoke skip (Phase 1 not ready) |
| No P0 VO `en` clip | **WARN** — VO smoke skip until ElevenLabs batch |
| Placeholder + dev mode | **WARN** — replace with ACE-Step before M5 |
| Placeholder + `--ship` | **FAIL** |
| ACE-Step export wrong LUFS | **FAIL** |
| Hero BGM jury, no API keys | **WARN** — manual packet |
| P0 VO jury, no API keys | **WARN** — manual packet |

Wired into `bash tools/run_playtest_smoke.sh`.

---

## 4. Agent workflow

### BGM

```
1. bash tools/generate_ai_bgm.sh --track bgm_village --api
2. Loudness normalize toward −16 LUFS in DAW/ffmpeg if needed
3. python3 tools/register_asset.py add --path <path> ...
4. python3 tools/check_audio_catalog.py --phase 1
5. python3 tools/check_audio_technical.py --track bgm_village
6. python3 tools/review_audio_vision.py --track bgm_village  (hero tracks)
7. GDAI MCP — wire in editor, F5 zone test
```

### P0 VO

```
1. bash tools/generate_ai_vo.sh --clip sc00_urashima_01 --locale en --locale ja --locale zh
2. python3 tools/check_audio_vo.py --clip sc00_urashima_01 --locale en
3. python3 tools/review_vo_vision.py --clip sc00_urashima_01 --locale en
4. Repeat technical for all locales; jury gate on en only
5. GDAI MCP — F5 scene with subtitles + duck_bgm_db
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
| `tools/check_audio_vo.py` | P0 VO technical (duration, loudness, paths) |
| `tools/review_vo_vision.py` | Multi-LLM listen jury (P0 VO, gate locale) |
| `tools/run_audio_smoke_checks.sh` | L2 smoke wrapper (BGM + P0 VO when files exist) |

---

## 7. vs Visual QA

| | Visual | BGM | P0 VO |
|--|--------|-----|-------|
| Cheap lint | `check_scene_visuals.sh` | `check_audio_technical.py` | `check_audio_vo.py` |
| LLM jury scope | Zone screenshots | 8 hero tracks | 5 P0 clips (`en` gate) |
| Brief-driven mood | `generation_briefs/*.md` M7/M8 | A6/A7 | V6/V7 |
| Human gate | L6 playtest | Loop + crossfade | Duck + subtitle timing |
