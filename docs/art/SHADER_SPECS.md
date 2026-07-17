# Shader Specifications — Tides of Urashima

**Version:** 1.0  
**Authority:** `docs/art/ART_DIRECTION.md` · `docs/art/RENDERING_GUIDE.md`  
**Implementation:** GodotPrompter drafts `.gdshader`; GDAI MCP assigns materials in scenes

---

## 1. Family rules

- One **toon ramp family** project-wide (`toon_base.gdshader` + zone tints)
- `render_mode diffuse_toon, specular_toon` on NPR surfaces
- No full PBR (metallic workflow) on player-facing assets
- Emission restrained; glow post-process handles bloom on heroes

---

## 2. Core shaders (Phase 1+)

| Shader | Path | Purpose |
|--------|------|---------|
| Toon base | `game/shaders/toon_base.gdshader` | Wood, stone, props — stepped diffuse |
| Water stylized | `game/shaders/water_stylized.gdshader` | Zone water planes — foam edge, gentle vertex displacement |
| Zone visuals | `game/scripts/exploration/zone_visuals.gd` | Fog, sky, tonemap presets per zone |

**Machine-readable:** `game/data/code/shader_registry.json` · `game/data/code/environment_registry.json` · `tools/zone_visuals_lib.py`

---

## 3. Hero / story shaders (Phase 5–6)

### Spirit lower body (Yuzu, wraiths)

- **Type:** Alpha blend or additive fragment
- **Uniforms:** `emissive_color`, `fade_height`, `noise_scroll`
- **Read:** Lower body dissolves into mist; upper body uses toon_base
- **Glow:** Enable on emissive; mode Softlight ~0.35

### Lacquer box (Urashima)

- **Type:** Toon base + emission uniform `box_glow_state` (0=dormant, 1=awakening, 2=unbound)
- **States:** Muted lacquer → pulse gold → white-hot rim (SC-16 only)
- **No** animated UV noise on box surface v1

### Mirror chamber (SC-13)

- **Type:** Planar reflection fake — second camera render to ViewportTexture OR matcap sky blend
- **Uniforms:** `distortion_strength`, `fog_tint` (#4AE8D8 cave cyan)
- **Performance:** Single mirror plane; no real-time SSR

### Ink combat VFX (UI overlay)

- **Type:** CanvasItem shader on full-screen `ColorRect` parented under `CombatUI` (`COMBAT_PRESENTATION.md`)
- **Shader:** `ink_combat_overlay.gdshader` — uniforms `ink_strength` (0.8), `pulse_duration` (0.35s)
- **Effect:** Brief ink-wash pulse on skill/limit resolve; not on world meshes
- **Duration:** &lt;0.4s per pulse; skipped when `reduced_motion` is on

---

## 4. Water (`water_stylized.gdshader`)

| Uniform | Default | Notes |
|---------|---------|-------|
| `zone_tint` | per `ENVIRONMENT_KITS.md` | Village grey-teal; cave cyan |
| `foam_edge_width` | 0.08 | Shoreline and prop contact |
| `wave_height` | 0.05–0.12 | Vertex sine; no fluid sim |
| `wave_speed` | 0.3 | Slow coastal rhythm |

**Naming:** Use `water_stylized.gdshader` everywhere — legacy `water_material` alias removed from docs.

---

## 5. QA gates

| Gate | Checks |
|------|--------|
| L1_unit_tests | Shader compiles headless where scripted |
| L2_visual_palette | Zone tint hex within art direction |
| L3 GDAI F5 | Foam/readability in gameplay camera |

---

## Related docs

| Doc | Contents |
|-----|----------|
| `docs/art/RENDERING_GUIDE.md` | Tonemap, fog, glow |
| `docs/art/ENVIRONMENT_KITS.md` | Per-zone palette rows |
| `docs/art/CHARACTER_BIBLE.md` | Spirit/box material states |
