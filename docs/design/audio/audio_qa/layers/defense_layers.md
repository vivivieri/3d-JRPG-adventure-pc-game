---
id: defense-layers
type: how-to
phase: [1, 5]
audience: [audio, qa]
status: active
authority: audio
tokens_est: 1057
summary: "Audio QA — Automate Layers — Defense layers A1–L6 — A1  check_audio_catalog.py     → required BGM tracks exist for phase"
---
# Audio QA — Automate Layers — Defense layers A1–L6

**Hub:** [`automate_layers.md`](../automate_layers.md)

## When to read

Use **Audio QA — Automate Layers — Defense layers A1–L6** (roles: audio, qa) when executing this procedure Jump to a section below instead of reading end-to-end (7 sections).

## Jump to

- [2. Defense layers](#2-defense-layers)
- [Layer A1 — Catalog](#layer-a1-catalog)
- [Layer A2 — Technical](#layer-a2-technical)
- [Layer A3 — Multi-LLM listen jury (hero BGM only)](#layer-a3-multi-llm-listen-jury-hero-bgm-only)
- [Layer A4 — P0 VO technical](#layer-a4-p0-vo-technical)
- [Layer A5 — Multi-LLM listen jury (P0 VO, gate locale `en`)](#layer-a5-multi-llm-listen-jury-p0-vo-gate-locale-en)
- [Layer L6 — Human](#layer-l6-human)


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

**Key-free alternative:** a QA agent can run the BGM/VO jury with Cursor's own LLMs via subagents (no provider keys) — `tools/ingest_agent_jury.py --domain audio|vo`. See [`AGENT_JURY.md`](../../../../ops/qa/AGENT_JURY.md).

**Pass:** ≥2 models `acceptance.valid_pass: true` (A1–A7 + confidence ≥ 0.65). Gate `L2_audio_jury`.

Emotional intent for hero tracks loads from `docs/briefs/audio/<track>.md` via `audio_brief_lib.py` (A6/A7 — same pattern as model M7/M8).

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

V2 checks **semantic** script match (not word-perfect for `ja`/`zh`). V6/V7 load from `docs/briefs/vo/<clip>.md` (same brief pattern as BGM A6/A7).

### Layer L6 — Human

Loop seam in Godot 10 min, SC-16 duck, three endings — `docs/design/audio/AUDIO_PRODUCTION_GUIDE.md` §11.

---
