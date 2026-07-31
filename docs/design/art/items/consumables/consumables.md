---
id: consumables
type: reference
audience: [visual, builder]
status: active
authority: art
tokens_est: 366
summary: "Single **shared bottle/pouch family** with palette swaps where possible."
---
# Items — Consumables / Key / Currency — Consumables

**Hub:** [`consumables_key_currency.md`](../consumables_key_currency.md)

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
