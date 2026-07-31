---
id: materials-gi-glow
type: reference
audience: [visual, builder]
phase: [1, 5]
status: active
authority: art
tokens_est: 653
---
# Rendering — Materials, GI, glow

**Hub:** [`RENDERING_GUIDE.md`](../RENDERING_GUIDE.md)

## 7. Materials & shaders

### 7.1 Use (stylized stack)

| Map / technique | Usage |
|-----------------|-------|
| **Albedo** | Automated stylized (ComfyUI/Material Maker + palette_remap); 4K heroes, 2K modules, 1K weapons |
| **Normal map** | Light normals OK — brick mortar, wood grain, stone cracks |
| **Emission** | Algae, lacquer box, palace gold, spirit lower body |
| **Toon ramp** | Single shader family across scene |
| **Roughness variation** | Via stylized albedo grunge — not metallic PBR workflow |

### 7.2 Do not use (v1)

| Technique | Why |
|-----------|-----|
| Full PBR ORM packs | Conflicts with toon look; art bible §3.4 |
| Metallic / glossy skin | Wrong tone for muted JRPG |
| HDR environment reflections | Breaks stylized readability |
| Realistic water simulation | Use stylized planes + foam decals + custom shader |

### 7.3 Custom shaders (recommended)

| Shader | Purpose | Reference |
|--------|---------|-----------|
| **Water** | Gentle vertex displacement, foam edge, zone tint | `water_stylized.gdshader` |
| **Spirit alpha** | Additive / alpha on Yuzu lower body | `CHARACTER_BIBLE.md` |
| **Lacquer box glow** | 3 emission states by story flag | `CHARACTER_BIBLE.md` §2 |
| **Mirror chamber** | Mirror shader SC-13 | `STORYBOARD.md` |
| **Wind sway** | Coastal grass / reeds vertex offset | Optional polish |
| **Ink-wash combat** | 2D screen shader on transition | `CINEMATICS.md` §9 |

---


## 8. Global illumination

| System | Verdict | Notes |
|--------|---------|-------|
| **SDFGI** | ❌ Skip | Open-world, realistic bounce — wrong for 2–3 h stylized game |
| **VoxelGI** | ❌ Skip (v1) | Expensive; caves can use emissive + fill lights |
| **LightmapGI** | ⏳ Later | Good for static ruined village on low-end; needs bake pipeline |
| **Authored fill** | ✅ Now | Directional + colored ambient + emissive props |

---


## 9. Glow targets (bloom)

Enable `Environment.glow` wherever emissive content should read on screen:

| Asset / moment | Color | Intensity note |
|----------------|-------|----------------|
| Lacquer box (dormant) | `#8B2A3A` seam | Faint — 15% emission |
| Lacquer box (awakened) | `#8B2A3A` pulse | Looping; SC-02+ |
| Lacquer box (choice) | Strong bloom | SC-16 |
| Cave algae | `#4AE8D8` | Primary cave fill |
| Palace gold trim | `#D4A55A` | Palace zone glow enabled |
| Spirit particles | `#6EC8C0` | Additive |
| Lore interactables | Cyan subtle | `LORE_AND_ENVIRONMENTAL_STORY.md` |
| Puzzle switch (stuck 5 min) | Glow pulse + chime | `PUZZLE_DESIGN.md` |

Tune glow so emissive elements **pop without blowing out** the muted palette.

---
