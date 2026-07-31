---
id: lore-lod-production
type: reference
audience: [builder, builder_zone, visual]
phase: [1, 5]
status: active
authority: world
tokens_est: 539
summary: "Lore, LOD, production, acceptance"
---
# Environment Kits — Lore, LOD, production, acceptance

**Hub:** [`ENVIRONMENT_KITS.md`](../ENVIRONMENT_KITS.md)

## 8. Lore collectible placements

Map for environment artists — 8 entries (`game/data/lore/lore_entries.json`).

| ID | Zone | Placement | Asset hook |
|----|------|-----------|------------|
| `fishing_ledger` | ruined_village | Near shack | Lore pickup |
| `festival_banner` | ruined_village | On `InspectBanner` | Banner inspectable |
| `yuzu_prayer` | ruined_village | Torii area | Shrine prop |
| `roku_dive_log` | ruined_village | Shack interior | Scroll prop |
| `cave_inscription` | tidal_caves | Puzzle room wall | Carved kanji |
| `sailor_charm` | tidal_caves | Post-boss alcove | Grants `spirit_bell` on read |
| `palace_seal` | dragon_palace_gate | Sentinel hall | Plaque |
| `otohime_letter` | dragon_palace_gate | Mirror chamber | Reflection trigger |

---


## 9. LOD & performance (PC target)

| Tier | Distance | Action |
|------|----------|--------|
| LOD0 | 0–25m | Full mesh |
| LOD1 | 25–60m | 50% tris |
| LOD2 | 60m+ | Impostor or culled |

**Target:** 60 FPS at 1080p on GTX 1060 / equivalent. Hub + palace are heaviest — batch materials per zone (max 8 draw call materials per view).

---


## 10. Production order

1. **Shared rocks + beach terrain** (SC-01 path)
2. **Village hub kit + torii hero** (vertical slice)
3. **Cave tunnel + algae + puzzle basin**
4. **Palace gate hero + modular trim**
5. **Mirror chamber + throne arena**
6. **Ending variants** (reuse village kit where possible)

---


## 11. Acceptance checklist (per zone)

- [ ] No box/primitive placeholders visible
- [ ] Palette matches `ART_DIRECTION.md` hex values
- [ ] Gameplay markers untouched
- [ ] Fog + water + lighting match mood table
- [ ] Japanese motif read clear at 15m camera distance
- [ ] All props logged in `LICENSES.md` if sourced externally
- [ ] Asset registered in `docs/asset_manifest.license.json` and compliance check passes
