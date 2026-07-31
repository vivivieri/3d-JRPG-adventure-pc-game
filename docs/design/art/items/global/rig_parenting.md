---
id: rig-parenting
type: reference
audience: [visual, builder]
status: active
authority: art
tokens_est: 513
summary: "Items — Global Sheets & Rig — Rig attachment & parenting — Humanoid rigs use Mixamo bone names. Custom attachment empties (child of bone) in Blender, exported i"
---
# Items — Global Sheets & Rig — Rig attachment & parenting

**Hub:** [`global_sheets_rig.md`](../global_sheets_rig.md)

## When to read

Use **Items — Global Sheets & Rig — Rig attachment & parenting** (roles: visual, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (4 sections).

## Jump to

- [3. Rig attachment & parenting](#3-rig-attachment-parenting)
- [Standard attachment points](#standard-attachment-points)
- [Parenting rules](#parenting-rules)
- [Combat pose offset (battle scene)](#combat-pose-offset-battle-scene)


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
