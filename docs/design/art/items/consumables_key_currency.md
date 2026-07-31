---
id: consumables-key-currency
type: reference
audience: [visual, builder]
phase: [2, 5]
status: active
authority: art
tokens_est: 957
summary: "[`ITEMS_3D_MODEL_GUIDE.md`](../ITEMS_3D_MODEL_GUIDE.md)"
---
# Items 3D — Consumables, key items, currency

**Hub:** [`ITEMS_3D_MODEL_GUIDE.md`](../ITEMS_3D_MODEL_GUIDE.md)

## 7. Consumables

Single **shared bottle/pouch family** with palette swaps where possible.

### `sea_salve`

| Spec | Value |
|------|-------|
| **Silhouette** | Small ceramic jar, cork stopper, seaweed wrap |
| **Dimensions** | 8 cm tall |
| **Tris** | ~400 |
| **Palette** | Jar `#5C7A6A`; salve visible `#4AE8D8` through crack |
| **Field pickup** | `pickup_sea_salve.glb` |
| **Use VFX** | Green-cyan particle puff on target (combat/field) |

### `spirit_tonic`

| Spec | Value |
|------|-------|
| **Silhouette** | Lacquered vial, paper label, spirit seal |
| **Dimensions** | 12 cm tall |
| **Tris** | ~450 |
| **Palette** | Vial `#6B1A1A`; liquid `#6EC8C0` emissive |
| **Field pickup** | `pickup_spirit_tonic.glb` |

### `coral_antidote`

| Spec | Value |
|------|-------|
| **Silhouette** | Shell bowl with coral powder; cloth lid |
| **Dimensions** | 10 cm wide |
| **Tris** | ~500 |
| **Palette** | Shell `#E8E4DC`; powder `#D4A55A` |
| **Field pickup** | `pickup_coral_antidote.glb` |

**Shared consumable rules:** Stack in inventory as icon only; field drops use pickup mesh + bob animation (0.05 m sine, 1.5 s period).

---


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


## 9. Materials & currency

### `spirit_shard`

| Spec | Value |
|------|-------|
| **Silhouette** | Jagged crystal sliver; faint inner light |
| **Tris** | ~200 |
| **Palette** | `#6EC8C0` core; `#3A5A6A` shell |
| **Pickup** | `pickup_spirit_shard.glb` — small cluster (1–3 shards) |

### `palace_fragment`

| Spec | Value |
|------|-------|
| **Silhouette** | Lacquer-red shard; gold crack lines like kintsugi |
| **Tris** | ~280 |
| **Palette** | `#8B2A3A`; gold `#D4A55A` veins |
| **Pickup** | `pickup_palace_fragment.glb` |

### `shell_coin` — Shell Coin

| Spec | Value |
|------|-------|
| **Silhouette** | Pierced cowrie-style shell coin |
| **Tris** | ~150 |
| **Palette** | `#C9B89A` with `#8B9DAF` shadow |
| **Field** | Coin scatter on defeat (3–5 instances); no individual pickup mesh in UI |
| **GLB** | `game/assets/models/items/shell_coin/shell_coin.glb` |
| **UI** | Icon only in shop/HUD |

---
