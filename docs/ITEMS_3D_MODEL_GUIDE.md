# Tides of Urashima — Items & Props 3D Model Guide

**Version:** 1.0 (Pre-build)  
**Visual target:** High-detail stylized Japanese — automated stylized albedo, readable silhouettes at inventory icon size and field pickup distance.  
**Cross-refs:** `docs/ITEMS_AND_ECONOMY.md`, `docs/CHARACTER_BIBLE.md`, `docs/ART_DIRECTION.md`, `game/data/items/items.json`

**Canonical rule:** Item IDs in this doc match `items.json`. Every shippable item has a **3D mesh** (field/combat), a **UI icon** (inventory/shop), or both as specified below.

---

## 1. Global item & prop rules

| Rule | Detail |
|------|--------|
| Style | Same toon ramp shader family as characters (`ART_DIRECTION.md` §7) |
| Poly budget — handheld prop | 300–1.2k tris |
| Poly budget — worn weapon (combat) | 800–2.5k tris |
| Poly budget — key story prop | 1k–3k tris |
| Poly budget — field pickup cluster | 200–600 tris per instance |
| Textures | 512×512 (consumables, charms); 1K (weapons); 2K (lacquer box hero prop) |
| Scale | 1 Godot unit = 1 meter |
| Naming | File prefix = item id (`fisher_katana`, `lacquer_box`, etc.) |
| Ship rule | No `BoxMesh` / primitive placeholders for item pickups or equipped weapons |

### Representation matrix

| Context | What renders |
|---------|----------------|
| **Equipped weapon** | Mesh parented to character attachment bone; only active weapon visible |
| **Equipped armor** | Mesh swap or material variant on character (see §4) |
| **Equipped charm** | No field mesh v1 — UI icon + stat only (except `spirit_bell` on Yuzu hair) |
| **Inventory / shop UI** | Painted icon 128×128 min (256×256 weapons/key items) |
| **Field pickup** | Small 3D prop + optional glow; despawns on collect |
| **Key item inspect** | Close-up in journal / cutscene — use hero prop mesh |
| **Combat** | Equipped weapon visible in attack anims; consumables = UI flash only |

---

## 2. Model sheet template

Use this layout for every new item or character prop before modeling. Store sheets in `docs/model_sheets/<id>.png` (not shipped in game build).

```
┌─────────────────────────────────────────────────────────────┐
│  ITEM: <id>          Display: <name>         v1.0           │
├──────────────┬──────────────┬──────────────┬────────────────┤
│   FRONT      │   SIDE       │   BACK       │  PERSPECTIVE   │
│  (ortho)     │  (ortho)     │  (ortho)     │  (3/4 hero)    │
├──────────────┴──────────────┴──────────────┴────────────────┤
│  Dimensions (m): L ___ × W ___ × H ___                      │
│  Tris target: ___    Texture: ___    Pivot: ___             │
│  Palette swatches: [■][■][■][■]                             │
│  Attachment: bone ___ / world placement ___                   │
│  Notes: wear, story beat, VFX state                          │
└─────────────────────────────────────────────────────────────┘
```

### Required fields per sheet

| Field | Example |
|-------|---------|
| ID | `fisher_katana` |
| Real-world scale | Blade 70 cm, total 95 cm |
| Pivot | Guard center at origin; blade +Y |
| Material notes | Salt pitting on blade; cord wrap `#4A3A2A` |
| LOD | Single mesh v1 (no LOD on handheld props) |
| Compliance | Source + license logged in `docs/LICENSES.md` |

---

## 3. Rig attachment & parenting

Humanoid rigs use Mixamo bone names. Custom attachment empties (child of bone) in Blender, exported in GLB.

### Standard attachment points

| Bone / empty | Name | Used by |
|--------------|------|---------|
| `RightHand` | `attach_weapon_r` | Urashima katana/saber/edge; Yuzu knife |
| `LeftHand` | `attach_weapon_l` | (reserved; unused v1) |
| `Spine2` | `attach_back_prop` | Roku harpoon (default stowed) |
| `Hips` | `attach_box_hip_l` | Urashima lacquer box (always on) |
| `Head` | `attach_charm_head` | Yuzu fox bell (part of hair mesh v1) |

### Parenting rules

1. **Weapons:** Parent to `attach_weapon_r`; align grip to palm; blade points forward (+Z in Godot combat stance).
2. **Harpoon:** Stowed on back via `attach_back_prop`; combat anim may detach to hand for `harpoon_strike`.
3. **Lacquer box:** Separate mesh from body; never merged — enables glow material swap (`CHARACTER_BIBLE.md` §2).
4. **Weapon swap:** Hide previous weapon mesh when equipment changes; no holster mesh v1.
5. **Scale lock:** Weapons authored at real scale; uniform scale only in engine (no non-uniform stretch).

### Combat pose offset (battle scene)

| Character | Weapon offset (local) | Notes |
|-----------|----------------------|-------|
| Urashima | Rot X -15°, Y 90° | Two-hand ready; katana family |
| Yuzu | Rot X -10°, Y 0° | Short reverse grip |
| Roku | Harpoon in hand at strike; on back otherwise | Wide grip |

---

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

## 10. File layout & export

```
game/assets/models/items/
  fisher_katana/fisher_katana.glb
  tide_cut_saber/tide_cut_saber.glb
  palace_edge/palace_edge.glb
  spirit_knife/spirit_knife.glb
  harpoon_rod/harpoon_rod.glb
  lacquer_box/lacquer_box.glb
  cave_map/cave_map_rolled.glb
  wraith_pearl/wraith_pearl.glb
  pickups/
    pickup_sea_salve.glb
    pickup_spirit_tonic.glb
    pickup_coral_antidote.glb
    pickup_spirit_shard.glb
    pickup_palace_fragment.glb
  shell_coin/shell_coin.glb
game/assets/textures/items/
  <item_id>_albedo.png
game/assets/ui/icons/items/
  <item_id>.png
```

### Export checklist

- [ ] GLB with embedded textures; Y-up → Godot import correct
- [ ] Pivot at grip (weapons) or base center (props)
- [ ] Register: `python3 tools/register_asset.py add --help`
- [ ] Log license in `docs/LICENSES.md`
- [ ] Run `bash tools/check_asset_compliance.sh`

---

## 11. Production order

| Priority | Item | Reason |
|----------|------|--------|
| P0 | `lacquer_box` | Vertical slice + all acts |
| P0 | `fisher_katana` | Urashima combat + field |
| P1 | Consumable pickups (×3) | Shop + drops |
| P1 | `shell_coin` | Economy feedback |
| P2 | `tide_cut_saber`, `cave_map` | Act I–II |
| P2 | `wraith_pearl` | SC-09 gate |
| P3 | `palace_edge`, materials | Act III |
| P3 | Remaining weapons, charm icons | Polish |

---

## 12. QA checklist

- [ ] Equipped weapon visible in combat for Urashima / Yuzu / Roku
- [ ] Weapon swap hides previous mesh without pop
- [ ] Lacquer box glow states match zone flags
- [ ] No primitive placeholders in pickup or weapon meshes
- [ ] Icons readable at 64×64 (inventory grid)
- [ ] Key items cannot be dropped as field props
- [ ] `wraith_pearl` fits palace gate socket without z-fighting
- [ ] All item IDs match `items.json`
