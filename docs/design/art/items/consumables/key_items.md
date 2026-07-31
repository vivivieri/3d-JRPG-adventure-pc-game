---
id: key-items
type: reference
audience: [visual, builder]
status: active
authority: art
tokens_est: 590
summary: "Items — Consumables / Key / Currency — Key items"
---
# Items — Consumables / Key / Currency — Key items

**Hub:** [`consumables_key_currency.md`](../consumables_key_currency.md)

## When to read

Use **Items — Consumables / Key / Currency — Key items** (roles: visual, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (4 sections).

## Jump to

- [8. Key items](#8-key-items)
- [`lacquer_box` — Lacquer Box (hero prop)](#lacquer_box-lacquer-box-hero-prop)
- [`cave_map` — Tidal Cave Map](#cave_map-tidal-cave-map)
- [`wraith_pearl` — Wraith Pearl](#wraith_pearl-wraith-pearl)


## 8. Key items

### `lacquer_box` — Lacquer Box (hero prop)

| Spec | Value |
|------|-------|
| **Priority** | **P0** — story-critical; same mesh on Urashima hip + inspect close-up |
| **Silhouette** | Rectangular Edo lacquer box; gold clasp; red cord |
| **Dimensions** | 18 × 12 × 8 cm |
| **Tris** | ~2.5k |
| **Palette** | Lacquer `#6B1A1A`; clasp `#C8A040`; cord `#8B2A3A` |
| **States** | 3 materials: `dormant`, `awakened`, `choice` — see `CHARACTER_BIBLE.md` §2 |
| **GLB** | `game/assets/models/items/lacquer_box/lacquer_box.glb` |
| **Ground prop** | `beach_lacquer_box_prop` in `ENVIRONMENT_KITS.md` — simplified 500 tris for SC-01 |

### `cave_map` — Tidal Cave Map

| Spec | Value |
|------|-------|
| **Silhouette** | Rolled parchment + wax seal; rope tie |
| **Dimensions** | Rolled 15 cm long; unrolled 40 × 30 cm (journal UI) |
| **Tris** | ~350 (rolled); journal uses 2D texture |
| **Palette** | Parchment `#D8C8A8`; ink `#2A2A2A`; seal `#8B3A2A` |
| **Field** | UI/journal only after SC-04; Roku hand-off uses 2D prop in cutscene |
| **GLB** | `game/assets/models/items/cave_map/cave_map_rolled.glb` |
| **Journal art** | `game/assets/ui/journal/cave_map.png` (hand-drawn map) |

### `wraith_pearl` — Wraith Pearl

| Spec | Value |
|------|-------|
| **Obtain** | Shore Wraith (SC-09) |
| **Silhouette** | Opaque orb; faces swirl inside (parallax or layered planes) |
| **Dimensions** | 6 cm diameter |
| **Tris** | ~800 (sphere + inner face cards) |
| **Palette** | Shell `#E8E4DC`; inner glow `#4AE8D8`; face tones desaturated |
| **VFX** | Slow rotation; whisper SFX on inspect |
| **Gate use** | SC-11 palace gate insert — mesh slots into `palace_gate_pearl_socket` |
| **GLB** | `game/assets/models/items/wraith_pearl/wraith_pearl.glb` |

---
