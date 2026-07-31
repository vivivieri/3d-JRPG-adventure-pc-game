---
id: defense-layers
type: how-to
audience: [visual, qa]
status: active
authority: art
tokens_est: 195
summary: "M1–M3b model QA defense layers"
---
# Model QA — Defense Layers

**Hub** — load only the pack for your current pass.

| Pack | Topic |
|------|-------|
| [`m1_m2.md`](m_layers/m1_m2.md) | M1–M2c |
| [`m3_jury.md`](m_layers/m3_jury.md) | M3 turntable + jury |
**Hub:** [`layers_workflow.md`](../layers_workflow.md)

## 2. Defense layers


```
M1  check_model_catalog.py       → required GLBs for phase
M2  check_model_technical.py     → tris, textures, banned sources
M3  blender_render_turntable.py  → 4-view PNG turntable
M3b review_model_vision.py       → 2-of-N LLM on turntable (hero/set-pieces)
L3  in-game screenshot           → VISUAL_QA.md (placement + zone)

