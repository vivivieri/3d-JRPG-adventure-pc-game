---
id: quality-zones
type: reference
audience: [visual, builder]
phase: [1, 5]
status: active
authority: art
tokens_est: 650
summary: "Add to settings menu (`docs/design/ui/SETTINGS_ACCESSIBILITY.md`). Store in `user://settings.json`."
---
# Rendering — Quality presets & zone map

**Hub:** [`RENDERING_GUIDE.md`](../RENDERING_GUIDE.md)

## 10. Graphics quality presets

Add to settings menu (`docs/design/ui/SETTINGS_ACCESSIBILITY.md`). Store in `user://settings.json`.

| Preset | Shadows | MSAA | Glow | Fog density | Notes |
|--------|---------|------|------|-------------|-------|
| **Low** | Off or hard only | Off | Off | 50% | GTX 1050 / laptop |
| **Medium** | Soft, 1024 | 2× | On | 100% | Default — target GTX 1060 |
| **High** | Soft, 2048 | 4× | On + HQ | 100% | Desktop |

**Storage keys (proposed):** `graphics_quality`, `shadows_enabled`, `msaa`, `glow_enabled`, `fog_density_scale`

Apply at runtime by updating `WorldEnvironment.environment` and `DirectionalLight3D` shadow settings when the player changes preset.

---


## 11. Zone implementation map

| Scene | `zone_id` | WorldEnvironment | Sky | Glow | Special |
|-------|-----------|-------------------|-----|------|---------|
| `beach_shore.tscn` | `beach_shore` | ✅ | ProceduralSky | Off (`glow_enabled: false`) | Coastal haze |
| `ruined_village.tscn` | `ruined_village` | ✅ | Overcast | On emissive (`glow_use_case: emissive_only`) | Vertical slice gate |
| `tidal_caves.tscn` | `tidal_caves` | ✅ | Dark | On (`glow_use_case: emissive_algae`) | No sky; emissive primary |
| `dragon_palace_gate.tscn` | `dragon_palace_gate` | ✅ | Void | On | Gold directional |
| `ending_*.tscn` | per ending | ✅ | Custom | Per scene | Fog cleared on Rewind |

**Code entry point:** `ZoneVisuals.apply_to_scene(root, zone_id)` — Godot feature branches.

---


## 12. M5 art acceptance checklist

Before marking an M5 art-pass zone complete, verify:

- [ ] `WorldEnvironment` present; tonemap Filmic or ACES
- [ ] Directional shadows on; light color matches zone table (§5)
- [ ] Fog color + density match palette (§5–6)
- [ ] Sky matches zone (ProceduralSky — not default clear color)
- [ ] Materials use toon ramp family — no stray PBR glossy materials
- [ ] Emissive glow reads on box / algae / palace trim
- [ ] No `BoxMesh` / primitive placeholders in player-facing view
- [ ] ≤ 8 materials visible per zone at gameplay camera
- [ ] 60 FPS @ 1080p on target hardware
- [ ] Graphics Low/Medium/High presets functional (when implemented)

**Vertical slice gate:** SC-02 Ruined Village first — `docs/design/art/ART_DIRECTION.md` §10.

---
