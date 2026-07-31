---
id: zone-textures
type: how-to
audience: [visual, builder]
phase: [1, 5]
status: active
authority: art
tokens_est: 473
summary: "Art Automation Pipeline — Zone texture workflow — GameLab is UI-focused. Zone albedos use ComfyUI or Material Maker."
---
# Art Automation Pipeline — Zone texture workflow

**Hub:** [`ART_AUTOMATION_PIPELINE.md`](../ART_AUTOMATION_PIPELINE.md)

## When to read

Use **Art Automation Pipeline — Zone texture workflow** (roles: visual, builder) when executing this procedure Jump to a section below instead of reading end-to-end (4 sections).

## Jump to

- [3. Zone texture workflow (not GameLab-first)](#3-zone-texture-workflow-not-gamelab-first)
- [3.1 ComfyUI batch (heroes, unique surfaces)](#31-comfyui-batch-heroes-unique-surfaces)
- [3.2 Material Maker (stone, wood, ground — free path)](#32-material-maker-stone-wood-ground-free-path)
- [3.3 Nature meshes (rocks, trees)](#33-nature-meshes-rocks-trees)


## 3. Zone texture workflow (not GameLab-first)

GameLab is **UI-focused**. Zone albedos use ComfyUI or Material Maker.

### 3.1 ComfyUI batch (heroes, unique surfaces)

```
1. READ  docs/design/art/ART_DIRECTION.md §1 palette for zone
2. ComfyUI — locked workflow: stylized NPR tileable, muted coastal decay
3. Export PNG → game/assets/textures/zones/<zone>/
4. python3 tools/palette_remap.py --zone <zone> --input <path>   # enforce §1 hex
5. python3 tools/register_asset.py add --path <path> --license <id> --source <name> --author <name> --used-for <desc>  # see docs/design/art/LICENSES.md
6. GodotPrompter — tune toon_base.gdshader if needed
7. GDAI MCP — assign in zone .tscn, F5 verify
8. bash tools/check_asset_compliance.sh
```

### 3.2 Material Maker (stone, wood, ground — free path)

```
1. Material Maker — procedural weathered wood #5C4A3A, wet stone #3A3A45
2. Export seamless PNG → game/assets/textures/zones/<zone>/
3. palette_remap.py → register → GDAI assign
```

### 3.3 Nature meshes (rocks, trees)

- **Poly Haven** CC0 meshes + project **toon ramp** — no photoreal PBR in player scenes.
- Kenney Nature: **dev greybox only** — not ship art (`docs/design/art/LICENSES.md`).

---
