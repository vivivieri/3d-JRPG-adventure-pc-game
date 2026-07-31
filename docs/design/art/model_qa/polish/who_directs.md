---
id: who-directs
type: reference
audience: [visual, qa]
phase: [1, 5]
status: active
authority: art
tokens_est: 1445
summary: "Who sets art direction vs who judges “feels right” — open on model polish disputes, jury FAIL ownership, or L6 handoff"
---
# Model QA — Who Directs Feel

**Hub:** [`polish_direction.md`](../polish_direction.md)

## When to read

Use **Model QA — Who Directs Feel** (roles: visual, qa) when you need this reference during the current task Jump to a section below instead of reading end-to-end (7 sections).

## Jump to

- [9.1 Two questions](#91-two-questions)
- [9.2 Direction authority chain (on-direction)](#92-direction-authority-chain-on-direction)
- [9.3 Who knows “feels right” (in motion)](#93-who-knows-feels-right-in-motion)
- [9.4 How “keep tweaking” works legally](#94-how-keep-tweaking-works-legally)
- [9.5 Role cheat sheet](#95-role-cheat-sheet)
- [9.6 Gaps (honest limits)](#96-gaps-honest-limits)
- [9.7 Audio parallel (BGM + P0 VO)](#97-audio-parallel-bgm-p0-vo)


### 9.1 Two questions

| Question | Meaning | Who **sets** direction | Who **judges** pass/fail |
|----------|---------|------------------------|--------------------------|
| **Are we on-direction?** | Correct brand, culture, silhouette, palette, story read | Design docs on `main` | L2 automated gates + vision jury |
| **Does it feel right?** | Weight, motion, attachment, combat telegraph in play | Human playtest feedback | **Human QA (L6)** after L0–L5 green |

Agents **execute and measure** — they do **not** own taste or redefine the art bible.


### 9.2 Direction authority chain (on-direction)

When in doubt, resolve in this order:

| Priority | Source | Owner role | What it defines |
|----------|--------|------------|-----------------|
| 1 | `docs/design/vision/GDD.md`, `docs/design/vision/STORYBOARD.md` | **PM** (facilitates) | Mood, audience, scene intent |
| 2 | `docs/design/art/ART_DIRECTION.md`, `docs/design/art/CHARACTER_BIBLE.md`, `docs/design/world/ENVIRONMENT_KITS.md` | **PM + design docs** | Palette, silhouettes, zone kits |
| 3 | `docs/briefs/<id>.md` | **Architect + Visual** | Per-asset prompt recipe (plan input) |
| 4 | `game/data/models/qa_catalog.json` | **Architect** | Tris, paths, animation contracts |
| 5 | `game/data/qa/acceptance_criteria.json` | **QA + Architect** | Measurable thresholds (M1–M6, L2 gates) |
| 6 | `game/data/qa/remediation_playbook.json` | **QA** | FAIL code → **one** lever to try next |

**Visual Agent** does not invent direction — it runs jury evidence against rows 2–5.

**Builder (GDAI)** applies meshes in scenes; it does not change prompts or bible rows without Architect handoff.


### 9.3 Who knows “feels right” (in motion)

| Signal | Owner | When |
|--------|-------|------|
| Turntable M4/M5 (static silhouette, detail) | Vision jury (2-of-N LLM) | Before / during import |
| Gameplay screenshot V5 (silhouette in zone) | Vision jury + `VISUAL_QA.md` | After GDAI placement |
| Walk cycle, cloth weight, combat read, attachment | **Human testers** | **L6 only** — `PLAYTEST_SCRIPT.md` §7b |
| Input latency, camera spring | `GAME_FEEL.md` + `feel_thresholds.json` | L2 feel smoke + human F1–F2 |

**Human QA Lead** is the **final arbiter** for subjective enjoyment. No agent may mark M5 art ship-ready on “vibes” alone.

### 9.4 How “keep tweaking” works legally

```
FAIL (automated) ──▶ remediation brief ──▶ ONE lever ──▶ rebuild ──▶ re-measure
                              │
                              ▼
                    cite: gate ID + bible/brief row

L0–L5 PASS ──▶ Human L6 ──▶ feedback ("coat too stiff")
                              │
                              ▼
                    PM/Architect updates brief or bible row
                              │
                              ▼
                    Builder regen/import ──▶ full QA stack again
```

**Traceability rule:** Every polish commit message must cite **what failed** (gate ID or human F#) and **which lever changed**. Example: `fix(urashima): attempt 2 — m4_silhouette, mesh_ops coat hem exaggeration`.


### 9.5 Role cheat sheet

| Role | Gives direction? | Knows “feels right”? |
|------|------------------|----------------------|
| **PM** | Prioritizes *which* asset/zone; does not override palette/bible | Facilitates L6; accepts ship with gate evidence |
| **Architect** | Writes briefs, plans, shaders; extends bible via PR to `main` | No — proposes against docs |
| **Visual Agent** | No — measures vs bible/brief | No — jury is compliance, not enjoyment |
| **Builder** | No | No — F5 verify only |
| **QA Agent** | No — enforces gates | No — proves PASS/FAIL |
| **Vision jury (LLM)** | No — reads bible/brief as rubric | Partial — style/silhouette only, not fun |
| **Human QA** | **Yes** for feel gaps not in automation | **Yes** — L6 sign-off |


### 9.6 Gaps (honest limits)

| Gap | Mitigation today |
|-----|------------------|
| Jury cannot score “fun” or emotional attachment | Human L6 + `PLAYTEST_SCRIPT.md` §7b F6–F8 |
| `animation_timing` GLB duration check | L0 catalog schema + `--check-timing` on game branch when GLBs exist |
| No standing “polish sprint” without FAIL | M5 milestone + per-asset production order (`CHARACTER_BIBLE.md` §11) |

See `docs/design/art/GENERATION_READINESS.md` for per-row ⚠️ Partial items that still need human judgment after gates pass.


### 9.7 Audio parallel (BGM + P0 VO)

Same governance shape as model turntable jury — different metrics:

| | 3D model | BGM | P0 VO |
|--|----------|-----|-------|
| Catalog | `qa_catalog.json` | `audio_qa_catalog.json` | `audio_qa_catalog.json` `vo_clips` |
| Technical | `check_model_technical.py` | `check_audio_technical.py` | `check_audio_vo.py` |
| Brief mood | M7/M8 | A6/A7 | V6/V7 |
| Jury tool | `review_model_vision.py` | `review_audio_vision.py` | `review_vo_vision.py` |
| Scope | Hero/set-pieces | 8 hero tracks | 5 P0 clips (`en` jury gate) |

Authority: `docs/design/audio/AUDIO_QA.md` · Human L6 still owns loop seams, duck mix, subtitle timing.
