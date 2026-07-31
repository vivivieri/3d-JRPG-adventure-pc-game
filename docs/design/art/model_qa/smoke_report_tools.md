---
id: smoke-report-tools
type: how-to
audience: [visual, builder]
phase: [5]
status: active
authority: art
tokens_est: 451
---
# Model QA — L2 smoke, report, tools

**Hub:** [`MODEL_QA.md`](../MODEL_QA.md)

## 4. L2 smoke

```bash
bash tools/run_model_smoke_checks.sh
```

| State | Behavior |
|-------|----------|
| No `urashima.glb` | **WARN** skip |
| GLB exists | catalog + technical; turntable + jury if Blender + API keys (or key-free agent jury) |
| Jury fail | **FAIL** → run `qa_remediation_brief.py` before rebuild |

Wired into `run_playtest_smoke.sh`.

**Key-free jury:** instead of provider API keys, a QA agent can run the jury with Cursor's own LLMs via subagents — `tools/ingest_agent_jury.py --domain model`. See [`AGENT_JURY.md`](../../../ops/qa/AGENT_JURY.md).

---


## 5. Agent report template

```
[MODEL QA] model=urashima
  catalog phase1: PASS
  technical: PASS (14234 tris, 2 textures)
  turntable: artifacts/model_reviews/urashima/
  jury: PASS (2/3)
  in_game_visual: pending GDAI screenshot
  result: PASS (asset); PENDING (in-scene)
```

---


## 6. Tools

| Tool | Role |
|------|------|
| `game/data/models/qa_catalog.json` | Paths, tri budgets, jury list |
| `tools/check_model_catalog.py` | Phase required models |
| `tools/check_model_technical.py` | GLB lint |
| `tools/render_model_turntable.py` | Blender 4-view render |
| `tools/review_model_vision.py` | Multi-LLM turntable jury (loads generation brief emotional intent) |
| `tools/generation_brief_lib.py` | Load `## Emotional intent` from `docs/briefs/` |
| `tools/run_model_smoke_checks.sh` | L2 smoke wrapper |

---


## 7. vs Visual / Audio QA

| | Visual | Audio | **3D Model** |
|--|--------|-------|----------------|
| Static lint | `.tscn` primitives | LUFS/format | **GLB tris/textures** |
| Render for jury | Game screenshot | Listen to Ogg | **Blender turntable** |
| LLM scope | Every zone shot | 8 hero BGMs | **hero_jury list only** |
| In-engine verify | Required | GDAI wire | **Required (VISUAL_QA)** |

---
