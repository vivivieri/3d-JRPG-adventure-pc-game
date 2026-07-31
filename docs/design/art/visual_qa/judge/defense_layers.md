---
id: defense-layers
type: reference
phase: [1, 5]
audience: [visual, qa]
status: active
authority: art
tokens_est: 189
summary: "Layers A–G defense stack"
---
# Visual QA — Defense Layers

**Hub** — load only the pack for your current pass.

| Pack | Topic |
|------|-------|
| [`part_a.md`](layers/part_a.md) | Visual QA — Defense Layers (A) |
| [`part_b.md`](layers/part_b.md) | Visual QA — Defense Layers (B) |
**Hub:** [`judge_layers.md`](../judge_layers.md)

## 2. Defense layers (use all — not pick one)


```
L1  check_scene_visuals.sh     → block BoxMesh/primitives in ship .tscn
L2.5 run_candidate_tournament.sh → champion/challenger (`golden_harness.json` — CANDIDATE_TOURNAMENT.md)
L3  GDAI screenshot            → artifacts/screenshots/<zone>_<camera>.png

