---
id: lighting-fog
type: reference
audience: [visual, builder]
phase: [1, 5]
status: active
authority: art
tokens_est: 427
summary: "[`RENDERING_GUIDE.md`](../RENDERING_GUIDE.md)"
---
# Rendering — Lighting & fog

**Hub:** [`RENDERING_GUIDE.md`](../RENDERING_GUIDE.md)

## 5. Lighting & shadows

### 5.1 Rule

**One dominant DirectionalLight3D + one colored fill per zone** (`ART_DIRECTION.md` §3.7).

| Zone | Directional color | Angle | Fill |
|------|-------------------|-------|------|
| `beach_shore` | Warm `#F0E8D0` | ~−48° / −35° | Ambient × 0.4 |
| `ruined_village` | Cool overcast `#B8C8D8` | 35° | Warm `#D4A880` at lantern + shack |
| `tidal_caves` | Cyan `#6EC8C0` (low) | N/A (no sky) | Emissive algae `#4AE8D8` |
| `dragon_palace_gate` | Gold `#FFD890` | ~−62° / 22° | Ambient × 0.55; glow on trim |

### 5.2 Shadows

| Property | Target |
|----------|--------|
| `shadow_enabled` | `true` on all zone directionals |
| Filter | Soft shadow filter (quality preset) |
| `directional_shadow_mode` | Orthogonal for palace; default elsewhere |
| `shadow_opacity` | ~0.4–0.5 in void palace (softer read) |
| Max distance | Tune so village props stay sharp near camera; fade before horizon |

### 5.3 Point / spot lights

- Caves: cyan pool lights only — **avoid pure white**
- Palace mirror chamber (SC-13): dual rim lights — `CINEMATICS.md`
- Lanterns / shrine glow: warm `#D4A880` omni, low range

---


## 6. Fog

| Zone | Fog color | Density | Aerial perspective | Notes |
|------|-----------|---------|-------------------|-------|
| `beach_shore` | `#9AB8C8` | 0.010 | 0.74 | Light coastal haze |
| `ruined_village` | `#8B9DAF` | 0.008 | 0.75 | **Always on** — draw-distance mask |
| `tidal_caves` | `#0A141C` | 0.028 | 0.72 | Heavier — depth in tunnels |
| `dragon_palace_gate` | `#1A1A3A` | 0.012 | 0.78 | Void atmosphere |

**Hub rule:** Fog always on in ruined village (`ART_DIRECTION.md` §3.5).
**Fog start:** ~20 m in village per `ENVIRONMENT_KITS.md` §4.

---
