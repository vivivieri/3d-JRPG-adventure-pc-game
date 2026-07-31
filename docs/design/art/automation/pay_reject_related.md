---
id: pay-reject-related
type: how-to
audience: [visual, builder]
phase: [5]
status: active
authority: art
tokens_est: 350
summary: "Pay vs free, rejected tools, related"
---
# Art Automation Pipeline — Pay vs free, rejected tools, related

**Hub:** [`ART_AUTOMATION_PIPELINE.md`](../ART_AUTOMATION_PIPELINE.md)

## 9. Pay vs free decision rule

```
IF free_tool_output >= paid_tool_output on blind review (same prompt, same zone):
    USE free
ELSE:
    USE paid (document cost in LICENSES.md / team notes)
```

Examples where **paid typically wins:** GameLab UI sheets, ElevenLabs VO, Meshy hero characters.
Examples where **free typically wins:** Material Maker stone/wood, Poly Haven rocks, procedural dev audio.

---


## 10. Explicitly rejected

| Approach | Reason |
|----------|--------|
| Human commission / hand-paint ship path | Policy — fully automated pipeline |
| GameLab for **all** zone textures | UI-primary; zone path uses ComfyUI / Material Maker |
| Kenney kits in ship builds | European/wrong read — greybox only |
| Random web images / unknown license | `ASSET_COMPLIANCE.md` |
| FMV in-game | Godot cinematics only |
| Full-script VO | 12 selective clips only |

---


## Related

- `docs/ops/agents/MCP_STACK.md` — MCP R&R map (tiered requirements)
- `docs/design/art/ART_DIRECTION.md` — palette, silhouettes, poly budgets
- `tools/palette_remap.py` — post-gen palette enforcement
- `tools/check_extended_toolchain.sh` — GameLab + Blender FAIL if absent (required)
