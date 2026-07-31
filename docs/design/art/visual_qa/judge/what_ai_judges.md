---
id: what-ai-judges
type: how-to
phase: [1, 5]
audience: [visual, qa]
status: active
authority: art
tokens_est: 248
summary: "What AI can/cannot judge"
---
# Visual QA — Judge Layers — What AI can/cannot judge

**Hub:** [`judge_layers.md`](../judge_layers.md)

## 1. What AI can and cannot judge

| AI can automate | AI cannot fully replace (needs human L6) |
|---------------|----------------------------------------|
| Detect `BoxMesh` / primitive meshes in `.tscn` | Emotional pacing, “does this feel sad enough?” |
| Sample screenshot pixels vs zone palette hex | Controller comfort |
| Compare screenshot to golden reference PNG | Localization nuance (ja/zh typography) |
| Flag pink missing-font boxes, UI overlap (vision) | Whether combat is fun |
| Verify fog/tonemap nodes exist in scene | Audio mix quality |

**Honest limit:** Without a **viewport screenshot** reviewed by a **multimodal** agent (or human), the AI is blind. `F5 PASS` + `0 errors` is **not** visual approval.

---
