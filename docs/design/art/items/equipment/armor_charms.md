---
id: armor-charms
type: reference
phase: [1, 5]
audience: [visual, builder]
status: active
authority: art
tokens_est: 457
summary: "Armor v1 uses **character mesh variants** — not standalone pickup props."
---
# Items — Weapons / Armor / Charms — Armor + charms

**Hub:** [`weapons_armor_charms.md`](../weapons_armor_charms.md)

## When to read

Use **Items — Weapons / Armor / Charms — Armor + charms** (roles: visual, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (2 sections).

## Jump to

- [5. Equipment — armor](#5-equipment-armor)
- [6. Equipment — charms](#6-equipment-charms)


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
