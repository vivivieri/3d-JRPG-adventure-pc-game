---
id: pipeline-mood-avoid
type: reference
audience: [visual, builder]
phase: [1, 5]
status: active
authority: art
tokens_est: 408
summary: "AI→Godot pipeline, mood, avoid list"
---
# Art Direction — AI→Godot pipeline, mood, avoid list

**Hub:** [`ART_DIRECTION.md`](../ART_DIRECTION.md)

## 7. AI 3D → Godot pipeline

1. Generate mesh via Meshy/Tripo/Rodin per `docs/design/art/CHARACTER_BIBLE.md` poly budgets
2. Items & props per `docs/design/art/ITEMS_3D_MODEL_GUIDE.md`
3. Blender — decimate, UV unwrap; ComfyUI/Material Maker albedo (4K heroes, 2K modules, 1K weapons)
4. `python3 tools/palette_remap.py` on texture sheets
5. Export as `.glb` (embedded textures)
6. Import to `game/assets/models/characters/`, `environment/`, or `items/`
7. Rig humanoids via Mixamo if needed
8. Materials: Godot toon shader family; spirits use alpha on lower body

Full workflow: `docs/design/art/ART_AUTOMATION_PIPELINE.md` §5.

---


## 8. Reference mood board (keywords)

- Grey overcast Japanese fishing coast
- Submerged torii gates (real-world photography)
- Dragon Palace — Takato Yamamoto woodblock intensity (tone only, not art theft)
- Combat UI — Persona 5 clarity (without copying layout)
- Boss scale — Shadow of the Colossus (emotional, not technical)

---


## 9. What to avoid

- Bright candy colors in hub
- Overly sexualized character designs
- Generic fantasy medieval props (stay Japanese coastal)
- Mixing realistic and toon shaders in same scene
- Asset Store "office worker" models retextured as fishermen
- **BoxMesh / primitive placeholders in shipped scenes**
- Low-poly CC0 kitbash as final art (prototype only)

---
