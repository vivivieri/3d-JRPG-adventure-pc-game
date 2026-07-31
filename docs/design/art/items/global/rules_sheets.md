---
id: rules-sheets
type: reference
audience: [visual, builder]
status: active
authority: art
tokens_est: 735
summary: "Rules + sheet template"
---
# Items — Global Sheets & Rig — Rules + sheet template

**Hub:** [`global_sheets_rig.md`](../global_sheets_rig.md)

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
