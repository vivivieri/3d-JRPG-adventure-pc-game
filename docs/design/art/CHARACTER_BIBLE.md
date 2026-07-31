---
id: character-bible
type: reference
audience: [visual, builder]
phase: [5]
status: active
authority: art
tokens_est: 816
summary: "High-detail stylized Japanese — automated stylized albedo, readable silhouettes, no primitive placeholders in ship builds."
---
# Tides of Urashima — Character Bible

## When to read

Use **Tides of Urashima — Character Bible** (roles: visual, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (5 sections).

## Jump to

- [1. Global character rules](#1-global-character-rules)
- [Model sheet template](#model-sheet-template)
- [Rig attachment points](#rig-attachment-points)
- [Character LOD (field only)](#character-lod-field-only)
- [Character packs (progressive disclosure)](#character-packs-progressive-disclosure)


## 1. Global character rules

| Rule | Detail |
|------|--------|
| Proportions | Head-to-body **1:5** (adult, not chibi) |
| Poly budget (field) | Hero 12k–18k tris; party 10k–15k; standard enemy 5k–10k; boss 25k–40k |
| Materials | One toon ramp shader family; spirits use additive/alpha on lower body |
| Rig | Humanoid (Mixamo-compatible); 1 skin per character |
| Animations | See §8 master list; no T-pose in shipped scenes |
| Portraits | Painted bust 512×512 min; match field model face/hair |
| Naming | File prefix = character id (`urashima`, `yuzu`, `roku`, etc.) |

**Ship rule:** No `CapsuleMesh`, `BoxMesh`, or Kenney knight placeholders in player-facing builds.

### Model sheet template

Every character and boss requires an orthographic model sheet before modeling. Full template and required fields: `docs/design/art/ITEMS_3D_MODEL_GUIDE.md` §2. Store sheets in `docs/model_sheets/<character_id>.png` (design-time only).

### Rig attachment points

| Empty name | Parent bone | Used by |
|------------|-------------|---------|
| `attach_weapon_r` | `RightHand` | Urashima weapons; Yuzu spirit knife |
| `attach_back_prop` | `Spine2` | Roku harpoon (stowed) |
| `attach_box_hip_l` | `Hips` | Urashima lacquer box |
| `attach_charm_head` | `Head` | Yuzu fox bell (part of hair mesh v1) |

Weapon parenting, combat offsets, and per-item mesh paths: `docs/design/art/ITEMS_3D_MODEL_GUIDE.md` §3–4.

### Character LOD (field only)

Combat uses full-detail mesh. Field exploration may swap LODs for performance.

| LOD | Tris (hero) | Tris (party) | Tris (enemy) | When |
|-----|-------------|--------------|--------------|------|
| LOD0 | 12k–18k | 10k–15k | 5k–10k | Player within 15 m |
| LOD1 | 6k–9k | 5k–8k | 3k–5k | 15–30 m |
| LOD2 | 2k–4k | 2k–3k | 1k–2k | 30 m+ or off-screen |

- **Bosses:** LOD0 only in boss arenas (no swap during fight).
- **Followers:** Yuzu/Roku use LOD1 beyond 10 m from camera.
- **Blend:** 0.2 s cross-fade; no pop on swap.
- **Portraits / combat:** Always LOD0 source mesh.

---

## Character packs (progressive disclosure)

Load the hub + one character/pack — not the whole bible.

| Pack | Path |
|------|------|
| Urashima | [characters/urashima.md](characters/urashima.md) |
| Yuzu | [characters/yuzu.md](characters/yuzu.md) |
| Roku | [characters/roku.md](characters/roku.md) |
| Otohime | [characters/otohime.md](characters/otohime.md) |
| Enemies | [characters/enemies.md](characters/enemies.md) |
| NPC / ambient | [characters/npc_ambient.md](characters/npc_ambient.md) |
| Animation & portraits | [characters/animation_portraits.md](characters/animation_portraits.md) |
| Export & order | [characters/export_order.md](characters/export_order.md) |

