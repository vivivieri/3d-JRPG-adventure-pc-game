---
id: p1-01-architect-toon
type: how-to
audience: [pm, architect, builder, qa]
phase: [1]
status: active
authority: ops
tokens_est: 1089
summary: "Title: `[DEV][P1-01] Phase 1.1–1.3 — toon_base.gdshader, zone_visuals.gd, ruined_village env preset"
---
# Phase1-Sprint1 — P1-01 architect toon + Builder handoff

**Hub:** [`Phase1-Sprint1-issues.md`](../Phase1-Sprint1-issues.md)

## When to read

Use **Phase1-Sprint1 — P1-01 architect toon + Builder handoff** (roles: pm, architect, builder, qa) when executing this procedure Jump to a section below instead of reading end-to-end (14 sections).

## Jump to

- [P1-01 — Architect: toon shader + zone visuals](#p1-01-architect-toon-shader-zone-visuals)
- [Acceptance gate IDs](#acceptance-gate-ids)
- [Spec summary](#spec-summary)
- [Architect → Builder handoff (paste in issue when done)](#architect-builder-handoff-paste-in-issue-when-done)
- [Handoff to Builder (P1-02)](#handoff-to-builder-p1-02)
- [Node tree outline — `ruined_village.tscn`](#node-tree-outline-ruined_villagetscn)
- [Shader / uniform list](#shader-uniform-list)
- [Inspector targets (GDAI sets)](#inspector-targets-gdai-sets)
- [Target gate IDs](#target-gate-ids)
- [Component scenes](#component-scenes)
- [Base classes](#base-classes)
- [Generation brief](#generation-brief)
- [Design refs](#design-refs)
- [Definition of done](#definition-of-done)


## P1-01 — Architect: toon shader + zone visuals

**Title:** `[DEV][P1-01] Phase 1.1–1.3 — toon_base.gdshader, zone_visuals.gd, ruined_village env preset`

**Labels:** `agent/architect`, `gate/L1_unit_tests`

| Field | Value |
|-------|-------|
| Phase | 1 |
| Implementation plan | **1.1**, **1.2**, **1.3** |
| Lead agent | **architect** |
| Depends on | P1-00 |
| Unblocks | P1-02 |

### Acceptance gate IDs

```
L1_unit_tests
L1_gdscript_lint
L0_base_class_compliance
```

### Spec summary

**Regeneration runbook:** `docs/engineering/technical/GDSCRIPT_REGENERATION.md` §10 · `bash tools/regenerate_phase1_visuals.sh`

GodotPrompter drafts (no hand `.tscn`):

1. **`game/shaders/toon_base.gdshader`** — single ramp family (`diffuse_toon`, `specular_toon`); uniforms: `base_color`, `albedo_texture`, optional emission.
2. **`game/scripts/exploration/zone_visuals.gd`** — applies per-zone palette, `WorldEnvironment`, `ProceduralSky`, directional + fill lights from zone id.
3. **`game/environments/ruined_village.tres`** (or runtime-only if Architect prefers) — tonemap Filmic/ACES, fog `#8B9DAF` density `0.008`, glow for emissive props.

**Ruined village targets** (`docs/design/art/RENDERING_GUIDE.md` §4–§6):

| Property | Value |
|----------|-------|
| Sky top / horizon | `#4A7A9A` / `#B8D0E0` |
| Directional | Cool overcast `#B8C8D8`, ~35° |
| Fill | Warm lantern `#D4A880` (lantern + shack) |
| Fog | `#8B9DAF`, density `0.008`, always on |

Add unit tests for `zone_visuals.gd` palette application (headless).

### Architect → Builder handoff (paste in issue when done)

```markdown

## Handoff to Builder (P1-02)

### Node tree outline — `ruined_village.tscn`
- Root: `Node3D` (zone root)
  - `WorldEnvironment` — assign `ruined_village` preset via `zone_visuals.gd` or `.tres`
  - `DirectionalLight3D` — shadow on, soft filter
  - `OmniLight3D` ×2 — lantern fill `#D4A880` (shack, shrine path)
  - `ZoneVisuals` — script `zone_visuals.gd`, export `zone_id = "ruined_village"`
  - `Terrain` / greybox meshes — material: ShaderMaterial `toon_base.gdshader`
  - `Markers` — empty placeholders per `zone_composition.json` markers
  - `GameplayCamera` — height 1.6 m reference for screenshots

### Shader / uniform list
- `toon_base.gdshader`: `base_color`, `albedo_texture` (placeholder flat `#5C4A3A` wood / `#C9B89A` sand)

### Inspector targets (GDAI sets)
- Directional: `shadow_enabled=true`, light color `#B8C8D8`
- WorldEnvironment: tonemap Filmic, fog on, glow ~0.35
- ZoneVisuals.zone_id = `ruined_village`

### Target gate IDs
- L3_gdai_built
- L2_scene_primitives
- L2_boot_headless (when main_scene wired)

### Component scenes
- `res://scenes/components/lantern_fill.tscn` — warm fill only (Phase 1 catalog)

### Base classes
- None new — no `PlayerController` until Phase 2

### Generation brief
- N/A (greybox slice)
```

### Design refs

- `docs/design/art/RENDERING_GUIDE.md` §3–§6
- `docs/design/art/ART_DIRECTION.md` §1 (hub palette), §7
- `docs/design/world/ENVIRONMENT_KITS.md` §4 (ruined_village)
- `.cursorrules` §6 — toon shader reference

### Definition of done

- [ ] Shaders + script committed; unit tests pass
- [ ] Handoff block above posted in this issue
- [ ] Reassign to `agent/builder`

---
