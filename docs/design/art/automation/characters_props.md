---
id: characters-props
type: how-to
audience: [visual, builder]
phase: [5]
status: active
authority: art
tokens_est: 380
summary: "3D character & prop workflow"
---
# Art Automation Pipeline — 3D character & prop workflow

**Hub:** [`ART_AUTOMATION_PIPELINE.md`](../ART_AUTOMATION_PIPELINE.md)

## 5. 3D character & prop workflow

```
1. READ  docs/design/art/CHARACTER_BIBLE.md poly budgets + docs/design/art/GENERATION_READINESS.md row (write docs/briefs/<id>.md if missing)
2. Meshy / Tripo / Rodin — text prompt from bible silhouettes (Japanese coastal, not chibi)
3. Blender — decimate to budget, UV unwrap, export GLB
4. ComfyUI or Material Maker — stylized albedo bake / projection
5. palette_remap.py on texture sheets
6. Mixamo — humanoid rig + walk/idle/combat clips (Mixamo ToS); clip names must match §8 below
7. `bash tools/install_glb_import_pipeline.sh` — NPR post-import sanitizer on GLB import
8. Import → game/assets/models/characters/ or environment/
9. GodotPrompter — toon shader + emission states (lacquer box)
10. GDAI MCP — place in scene, F5 verify
11. `python3 tools/check_animation_whitelist.py` — clip names ⊆ `qa_catalog.json` → `allowed_animations`
12. `docs/design/art/MODEL_QA.md` — GLB lint + turntable jury before import; `docs/design/art/VISUAL_QA.md` after in-scene
13. `docs/ops/qa/ACCEPTANCE_CRITERIA.md` — cite gate id + measured values in agent report; FAIL → `QA_REMEDIATION_LOOP.md`
```

**No commission path.** Rights = service ToS + `register_asset.py` + `LICENSES.md`.

---
