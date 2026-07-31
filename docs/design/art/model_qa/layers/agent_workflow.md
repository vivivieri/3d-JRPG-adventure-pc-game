---
id: agent-workflow
type: how-to
phase: [1, 5]
audience: [visual, qa]
status: active
authority: art
tokens_est: 211
summary: "1. Meshy/Tripo/Rodin → Blender decimate/UV → export GLB"
---
# Model QA — Layers & Workflow — Agent workflow

**Hub:** [`layers_workflow.md`](../layers_workflow.md)

## 3. Agent workflow (3D model task)

```
1. Meshy/Tripo/Rodin → Blender decimate/UV → export GLB
2. ComfyUI/Material Maker albedo + palette_remap.py
3. python3 tools/register_asset.py add --path <path> --license <id> --source <name> --author <name> --used-for <desc>
4. python3 tools/check_model_catalog.py --phase 1
5. python3 tools/check_model_technical.py --model urashima
6. python3 tools/render_model_turntable.py --model urashima
7. python3 tools/review_model_vision.py --model urashima
8. GDAI MCP — import, toon shader, F5 + VISUAL_QA screenshot
```

---
