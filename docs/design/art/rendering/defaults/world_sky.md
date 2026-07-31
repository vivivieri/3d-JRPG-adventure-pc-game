---
id: world-sky
type: reference
audience: [visual, builder]
status: active
authority: art
tokens_est: 631
summary: "WorldEnvironment + sky"
---
# Rendering — Defaults & Environment — WorldEnvironment + sky

**Hub:** [`defaults_environment.md`](../defaults_environment.md)

## 3. WorldEnvironment (per zone)

Every world scene needs a `WorldEnvironment` node. Apply via `game/scripts/exploration/zone_visuals.gd` or a saved `.tres` preset per zone.

### 3.1 Global defaults

| Property | Value |
|----------|-------|
| `background_mode` | `BG_SKY` |
| `tonemap_mode` | `TONE_MAPPER_FILMIC` (or `TONE_MAPPER_ACES` — pick one and keep consistent) |
| `ambient_light_source` | `AMBIENT_SOURCE_COLOR` |
| `fog_enabled` | `true` |
| `fog_sky_affect` | `0.85` |
| `fog_light_color` | Zone palette fog hex (see §5) |

### 3.2 Post-processing

| Effect | When | Settings |
|--------|------|----------|
| **Glow** | Palace, caves, any emissive interactable | `glow_enabled = true`; intensity ~0.3–0.4; bloom ~0.15–0.2; mode Softlight |
| **SSAO** | — | **Off** — fights toon ramp |
| **SSIL** | — | **Off** in v1; if caves feel flat, try very low intensity in `tidal_caves` only |
| **Volumetric fog** | Ruined village hub | Light density; do not use in caves or palace void |
| **Adjustments** | Combat defeat only | Desaturate via `CINEMATICS.md` §4 — not a permanent env setting |

### 3.3 What to avoid

- Mixing StandardMaterial3D PBR and toon shaders in the same scene (`ART_DIRECTION.md` §9)
- Pure white directional lights — always tint warm or cool
- HDR reflections, glossy skin, lens flare (`CINEMATICS.md` §9)
- SDFGI (open-world GI — wrong scale and aesthetic for this game)

---



## 4. Sky

Use **ProceduralSkyMaterial**, not PhysicalSky + HDRI. Our mood is grey overcast coast, biolume caves, and void palace — not sunny photoreal outdoors.

| Zone | Sky top | Sky horizon | Ground horizon | Sun |
|------|---------|-------------|----------------|-----|
| `beach_shore` | `#5A98B0` | `#C8E0EC` | `#3A7888` | Low angle, soft (`sun_angle_max` ~32°) |
| `ruined_village` | `#4A7A9A` | `#B8D0E0` | `#6A8A9A` | Overcast (`sun_angle_max` ~28°) |
| `tidal_caves` | `#060C14` | `#1A3048` | `#142838` | No visible sun — emissive fill |
| `dragon_palace_gate` | `#080818` | `#3A2868` | `#1A2858` | Void sky; warm gold light from above |
| Endings | Per ending doc | `ENVIRONMENT_KITS.md` §7 | — | Sunset / cleared fog for Rewind |

**Do not** use a generic sunny PhysicalSky HDRI — it breaks the muted emotional palette.

---
