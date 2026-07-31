---
id: ui-art
type: how-to
audience: [visual, builder]
phase: [5]
status: active
authority: art
tokens_est: 202
summary: "1. READ docs/design/art/ART_DIRECTION.md §4 UI style"
---
# Art Automation Pipeline — UI art (GameLab)

**Hub:** [`ART_AUTOMATION_PIPELINE.md`](../ART_AUTOMATION_PIPELINE.md)

## 4. UI art workflow (GameLab-primary)

```
1. READ  docs/design/art/ART_DIRECTION.md §4 UI style
2. GameLab MCP — ink-wash frame, combat icon sheet, menu border (muted, not candy-bright)
3. palette_remap.py on full-color gens
4. Save → game/assets/textures/ui/
5. GDAI MCP — assign to Control themes / TextureRects in UI scenes
```

**Dev asset fallback:** `generate_procedural_portraits.py` and flat-color UI placeholders until GameLab output ships — **does not** waive the `gamelab-mcp` requirement.

---
