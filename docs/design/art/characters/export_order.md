---
id: export-order
type: reference
audience: [visual, builder]
phase: [5]
status: active
authority: art
tokens_est: 400
---
# Characters — Export & production order

**Hub:** [`CHARACTER_BIBLE.md`](../CHARACTER_BIBLE.md)

## 10. File naming & export

```
game/assets/models/characters/urashima/urashima.glb
game/assets/models/characters/yuzu/yuzu.glb
game/assets/models/characters/roku/roku.glb
game/assets/models/enemies/palace_sentinel/palace_sentinel.glb
game/assets/models/npcs/otohime/otohime_bust.glb
game/assets/models/npcs/crowd/villager_spirit.glb
game/assets/models/npcs/crowd/rebuilder.glb
game/assets/ui/portraits/urashima.png
```

- Export GLB with embedded textures
- Scale: 1 Godot unit = 1 meter; Urashima height ≈ **1.7m**
- Register in manifest: `python3 tools/register_asset.py add --help`
- Log every external source in `docs/design/art/LICENSES.md` + `docs/design/art/ASSET_COMPLIANCE.md`

---

## 11. Production order

1. Urashima model + walk + idle (vertical slice gate)
2. Lacquer box + `fisher_katana` (`docs/design/art/ITEMS_3D_MODEL_GUIDE.md` §4, §8)
3. Torii + shack set dressing with Urashima in SC-02
4. Salt Crab + combat portraits
5. Yuzu + Shore Wraith (Act II gate)
6. Roku + remaining enemies
7. Palace Sentinel + Tide Keeper + Otohime bust
8. Ending crowd (`villager_spirit`, `rebuilder`) + ending variants (boat, restored village kit)
9. Remaining item pickups and weapon tiers
