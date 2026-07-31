---
id: weapons-armor-charms
type: reference
audience: [visual, builder]
phase: [2, 5]
status: active
authority: art
tokens_est: 1018
summary: "[`ITEMS_3D_MODEL_GUIDE.md`](../ITEMS_3D_MODEL_GUIDE.md)"
---
# Items 3D — Weapons, armor, charms

**Hub:** [`ITEMS_3D_MODEL_GUIDE.md`](../ITEMS_3D_MODEL_GUIDE.md)

## 4. Equipment — weapons

### `fisher_katana` — Fisher's Katana

| Spec | Value |
|------|-------|
| **Owner** | Urashima (start weapon) |
| **Silhouette** | Short wakizashi-length blade; plain wooden saya; frayed sageo |
| **Dimensions** | Blade 62 cm; total 88 cm |
| **Tris** | ~1.2k |
| **Palette** | Blade `#8A9AAA` (salt dull); saya `#3A2A1A`; wrap `#4A3A2A` |
| **Wear** | Edge chips, salt crust at habaki |
| **Field** | Equipped on hip when in field (saya visible); drawn in combat |
| **Pickup** | N/A (story grant) |
| **GLB** | `game/assets/models/items/fisher_katana/fisher_katana.glb` |
| **Icon** | Diagonal blade, ink-wash border |

### `tide_cut_saber` — Tide-Cut Saber

| Spec | Value |
|------|-------|
| **Owner** | Urashima |
| **Obtain** | SC-07 flooded chest |
| **Silhouette** | Slightly longer katana; wave-shaped hamon line; coral residue on guard |
| **Dimensions** | Blade 72 cm; total 98 cm |
| **Tris** | ~1.5k |
| **Palette** | Blade `#6AB8C8` tint; guard `#4AE8D8` patina; handle `#2A3A4A` |
| **VFX** | Faint cyan trail on `attack_heavy` (combat only) |
| **Field pickup** | Chest prop `env_tidal_chest_open` + embedded blade read |
| **GLB** | `game/assets/models/items/tide_cut_saber/tide_cut_saber.glb` |

### `palace_edge` — Palace Edge

| Spec | Value |
|------|-------|
| **Owner** | Urashima |
| **Obtain** | Palace Sentinel drop (SC-14) |
| **Silhouette** | Elegant katana; lacquered saya with gold mon; ryūgū motif |
| **Dimensions** | Blade 75 cm; total 102 cm |
| **Tris** | ~1.8k |
| **Palette** | Blade `#C8D0E0` (lacquer-slick); saya `#8B2A3A`; trim `#D4A55A` |
| **Wear** | None — pristine, unsettling against ruined coast |
| **GLB** | `game/assets/models/items/palace_edge/palace_edge.glb` |

### `spirit_knife` — Spirit Knife

| Spec | Value |
|------|-------|
| **Owner** | Yuzu |
| **Silhouette** | Short ritual blade; white handle; paper talisman strip on hilt |
| **Dimensions** | Blade 28 cm; total 38 cm |
| **Tris** | ~600 |
| **Palette** | Blade `#E8E4DC`; handle `#F0ECE4`; talisman `#8B2A3A` ink |
| **Spirit treatment** | Blade alpha 90% with soft edge in field; solid in combat |
| **GLB** | `game/assets/models/items/spirit_knife/spirit_knife.glb` |

### `harpoon_rod` — Harpoon Rod

| Spec | Value |
|------|-------|
| **Owner** | Roku |
| **Silhouette** | Wooden shaft, iron tip, rope coil mid-shaft |
| **Dimensions** | Shaft 1.8 m (stowed diagonal on back) |
| **Tris** | ~1.4k |
| **Palette** | Wood `#4A3A2A`; metal `#6A6A6A`; rope `#5C5A48` |
| **Note** | Same mesh as Roku hero prop (`CHARACTER_BIBLE.md` §4); shop version is clean variant |
| **GLB** | `game/assets/models/items/harpoon_rod/harpoon_rod.glb` |

---


## 5. Equipment — armor

Armor v1 uses **character mesh variants** — not standalone pickup props.

| ID | Implementation | Visual delta |
|----|----------------|--------------|
| `worn_haori` | Urashima default coat (`#2A3A4A`) | Faded, salt stains — baseline model |
| `cave_wet_coat` | Material variant on Urashima coat + optional Yuzu/Roku overlays | Darker `#1A2A3A`, wetness gloss mask, drip at hem |
| `diver_mail` | Roku suit mesh swap | Thicker canvas panels, metal clasp at chest, +bulk silhouette |

| Spec | Value |
|------|-------|
| **Tris delta** | +0–800 per variant (overlay patches only) |
| **Textures** | Separate albedo per variant in `game/assets/textures/equipment/<id>.png` |
| **Field pickup** | Shop bag prop `prop_shop_bundle` (generic) — not armor mesh |
| **UI icon** | Folded garment illustration per character silhouette |

---


## 6. Equipment — charms

Charms are **UI-first** v1. No field mesh except where noted.

| ID | Field mesh | Icon description |
|----|------------|------------------|
| `shrine_charm` | None | Paper ofuda, red stamp, frayed edge |
| `shell_charm` | None | Cowrie shell on braided cord |
| `spirit_bell` | On Yuzu hair (existing bell mesh) | Match fox bell; add faint glow when equipped |

| Spec | Value |
|------|-------|
| **Tris** | 0 field (charms); bell already on Yuzu (~200 tris) |
| **Icon size** | 128×128 |

---
