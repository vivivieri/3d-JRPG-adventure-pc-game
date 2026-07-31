---
id: part-b
type: reference
phase: [1, 5]
audience: [visual, qa]
status: active
authority: art
tokens_est: 750
summary: "Model QA — Who Directs Feel (B)"
---
# Model QA — Who Directs Feel — Model QA — Who Directs Feel (B)

**Hub:** [`who_directs.md`](../who_directs.md)

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
