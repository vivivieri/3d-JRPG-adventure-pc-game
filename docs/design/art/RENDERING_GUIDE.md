---
id: rendering-guide
type: reference
audience: [visual, builder]
phase: [1, 5]
status: active
authority: art
tokens_est: 900
summary: "load the pack for the lighting/material pass you are doing."
---
# Tides of Urashima — Rendering Guide

**Hub** — load the pack for the lighting/material pass you are doing.

| Pack | Topic |
|------|-------|
| [`defaults_environment.md`](rendering/defaults_environment.md) | Defaults, WorldEnvironment, sky |
| [`lighting_fog.md`](rendering/lighting_fog.md) | Lighting & fog |
| [`materials_gi_glow.md`](rendering/materials_gi_glow.md) | Materials, GI, glow |
| [`quality_zones.md`](rendering/quality_zones.md) | Quality presets & zone map |
| [`zone_visuals_contract.md`](rendering/zone_visuals_contract.md) | zone_visuals contract & refs |
# Tides of Urashima — Rendering Guide

**Version:** 1.0 (Pre-build)
**Engine:** Godot 4.7 Forward+
**Visual target:** High-detail **stylized Japanese 3D** — not photoreal PBR.
**Cross-refs:** `docs/design/art/ART_DIRECTION.md`, `docs/design/world/ENVIRONMENT_KITS.md`, `docs/design/ui/CINEMATICS.md`, `docs/design/ui/SETTINGS_ACCESSIBILITY.md`

This document is the single checklist for the M5 art rebuild (Phase 7) and Godot scene polish. It adapts generic “professional 3D” advice to our art bible: automated stylized albedo, toon ramp shaders, muted coastal palette, 60 FPS @ 1080p on GTX 1060.

---
