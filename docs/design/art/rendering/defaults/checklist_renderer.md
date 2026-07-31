---
id: checklist-renderer
type: reference
audience: [visual, builder]
status: active
authority: art
tokens_est: 544
summary: "Performance gate: 60 FPS @ 1080p on GTX 1060 — test SC-02 Ruined Village vertical slice before full production. Hardware + environment spec."
---
# Rendering — Defaults & Environment — Checklist + renderer

**Hub:** [`defaults_environment.md`](../defaults_environment.md)

## When to read

Use **Rendering — Defaults & Environment — Checklist + renderer** (roles: visual, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (2 sections).

## Jump to

- [1. Summary checklist](#1-summary-checklist)
- [2. Renderer & project defaults](#2-renderer-project-defaults)


## 1. Summary checklist

| Feature | Default Godot | Our target | Apply? |
|---------|---------------|------------|--------|
| **Tonemap** | Linear (flat / washed out) | **Filmic** or **ACES** | ✅ Yes |
| **Shadows** | Off or low res | **On** — soft directional, zone-tuned | ✅ Yes |
| **Sky** | Clear color | **ProceduralSky** per zone (not sunny HDRI) | ✅ Yes |
| **Fog** | Off | **Distance fog** — hub always on | ✅ Yes |
| **Volumetric fog** | Off | **Subtle** in ruined village only | ⚠️ Optional |
| **Glow (bloom)** | Off | **On** for emissive props (box, algae, palace) | ✅ Yes |
| **SSAO / SSIL** | Off | **Skip** (or very subtle SSIL in caves only) | ❌ No (v1) |
| **PBR materials** | StandardMaterial3D | **Toon ramp** + automated stylized albedo + light normals | ✅ Adapted |
| **SDFGI / VoxelGI** | Off | **Skip** — authored fill lights instead | ❌ No (v1) |
| **LightmapGI** | Off | **Defer** — consider for static village later | ⏳ Later |

---



## 2. Renderer & project defaults

| Setting | Value | Notes |
|---------|-------|-------|
| Renderer | **Forward+** | Already set on Godot branches (`config/features=Forward Plus`) |
| MSAA | **2×** default, **4×** on High | Quality preset |
| VSync | User setting | `docs/design/ui/SETTINGS_ACCESSIBILITY.md` |
| Exposure | Authored per zone | Prevent fog `#8B9DAF` and biolume `#4AE8D8` clipping to white |
| Max materials per view | **≤ 8** per zone | `docs/design/world/ENVIRONMENT_KITS.md` §9 |

**Performance gate:** 60 FPS @ 1080p on GTX 1060 — test SC-02 Ruined Village vertical slice before full production. **Hardware + environment spec:** `docs/ops/qa/PERFORMANCE_BASELINE.md` · `game/data/qa/perf_baseline.json`.

---
