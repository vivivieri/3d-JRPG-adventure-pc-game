---
id: part-a
type: reference
phase: [0, 1]
audience: [visual, builder, pm]
status: active
authority: ops
tokens_est: 683
summary: "Stylized tileable wood, stone, ground, hero texture sheets."
---
# MCP — Art Tools — MCP — Art Tools (A)

**Hub:** [`art_tools.md`](../art_tools.md)

### ComfyUI / Material Maker — zone NPR albedos

**Role:** Stylized tileable wood, stone, ground, hero texture sheets.
**Does NOT:** Edit `.tscn` — hand off to GDAI after export.

**Workflow:**

```
1. READ  docs/design/art/ART_DIRECTION.md palette for target zone
2. ComfyUI (locked workflow) OR Material Maker — tileable albedo (muted coastal decay)
3. python3 tools/palette_remap.py --zone <zone> --input <png>
4. Save PNG → game/assets/textures/zones/<zone>/
5. python3 tools/register_asset.py add --path <path> --license <id> --source <name> --author <name> --used-for <desc>  # see docs/design/art/LICENSES.md
6. GodotPrompter — tune toon shader if needed
7. GDAI MCP — assign materials in zone .tscn, F5 verify
8. bash tools/check_asset_compliance.sh
```

**Art constraints:** Muted palette (`#8B9DAF` fog, `#5C4A3A` wood, `#4AE8D8` biolume). Japanese coastal motifs — **not** bright Ghibli candy, not PBR realism, no European medieval reads.


### GameLab Studio MCP — UI & 2D sheets (required)

**Role:** Ink-wash UI frames, combat icon sheets, menu borders, VFX sprite sheets.
**Does NOT:** Default path for zone tileables (use ComfyUI/Material Maker) or `.tscn` edits.

**Workflow:**

```
1. READ  docs/design/art/ART_DIRECTION.md §4 UI style
2. GameLab MCP — generate UI frame / icon sheet (muted, not candy-bright)
3. palette_remap.py → game/assets/textures/ui/
4. register_asset.py → GDAI assigns in UI .tscn
```

Setup: [gamelabstudio.co](https://gamelabstudio.co/) API key → register `gamelab-mcp` SSE server. **Required** — procedural UI placeholders OK for asset output until GameLab gen ships.

**Design context:** Read `docs/` + `game/data/` before balancing combat or editing JSON. No external design-index MCP.

**Why not Ink (Inkle):** Story spine is JSON-driven (`scenes.json` → `dialogue/` → `flags.json`). Ink adds a second runtime with no v1 benefit. See `docs/design/vision/NARRATIVE_WRITING_GUIDE.md`.


### AI 3D + Blender — offline hero pipeline (required for turntable QA)

**Role:** Automated stylized meshes and albedos for Japanese coastal heroes and set-pieces.
**Not MCP** — offline batch before Godot import.

```
Meshy / Tripo / Rodin → Blender (decimate, UV) → ComfyUI/Material Maker albedo
  → palette_remap.py → GLB → game/assets/models/
  → toon_base.gdshader → Mixamo rig → GDAI MCP places in zone scene
```

**Use for:** Characters, torii, lacquer box, palace trim (poly budgets per `ART_DIRECTION.md`).
