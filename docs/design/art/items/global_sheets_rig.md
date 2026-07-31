---
id: global-sheets-rig
type: reference
audience: [visual, builder]
phase: [2, 5]
status: active
authority: art
tokens_est: 1033
summary: "[`ITEMS_3D_MODEL_GUIDE.md`](../ITEMS_3D_MODEL_GUIDE.md)"
---
# Items 3D — Global rules, sheets, rig

**Hub:** [`ITEMS_3D_MODEL_GUIDE.md`](../ITEMS_3D_MODEL_GUIDE.md)

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
| Compliance | Source + license logged in `docs/design/art/LICENSES.md` |

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
