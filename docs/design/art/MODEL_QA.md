---
id: model-qa
type: how-to
audience: [visual, builder]
phase: [5]
status: active
authority: art
tokens_est: 900
---
# 3D Model QA — Technical Gates + Turntable Vision Jury

**Hub** — load the pack for the QA step you are running.

| Pack | Topic |
|------|-------|
| [`layers_workflow.md`](model_qa/layers_workflow.md) | Defense layers & agent workflow |
| [`smoke_report_tools.md`](model_qa/smoke_report_tools.md) | L2 smoke, report, tools |
| [`polish_direction.md`](model_qa/polish_direction.md) | Polish cadence & direction |
# 3D Model QA — Technical Gates + Turntable Vision Jury

**Version:** 1.2
**Problem:** An agent can import a **low-poly blockout**, **Kenney greybox**, or **chibi AI mesh** and call it “Urashima done” — then reuse that quality bar everywhere.

**Rule:** Models pass **catalog + GLB technical lint + turntable vision jury** (hero/set-pieces) before ship. In-game screenshot QA (`docs/design/art/VISUAL_QA.md`) catches placement; this doc catches **the asset itself**.

**Cross-refs:** `docs/design/art/CHARACTER_BIBLE.md`, `docs/design/art/ITEMS_3D_MODEL_GUIDE.md`, `docs/design/art/ART_AUTOMATION_PIPELINE.md` §5, `docs/ops/qa/QA_REMEDIATION_LOOP.md`, `docs/ops/qa/ACCEPTANCE_CRITERIA.md`, `docs/design/art/GENERATION_READINESS.md`, `docs/briefs/`, `game/data/models/qa_catalog.json`

---
