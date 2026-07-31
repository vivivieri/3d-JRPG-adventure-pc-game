---
id: export-qa
type: reference
audience: [visual, builder]
phase: [5]
status: active
authority: art
tokens_est: 450
summary: "[`ITEMS_3D_MODEL_GUIDE.md`](../ITEMS_3D_MODEL_GUIDE.md)"
---
# Items 3D — Export & QA

**Hub:** [`ITEMS_3D_MODEL_GUIDE.md`](../ITEMS_3D_MODEL_GUIDE.md)

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
- [ ] Log license in `docs/design/art/LICENSES.md`
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
