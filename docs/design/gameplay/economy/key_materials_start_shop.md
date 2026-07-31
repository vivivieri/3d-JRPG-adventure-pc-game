---
id: key-materials-start-shop
type: reference
phase: [2, 3]
audience: [builder, builder_combat, qa]
status: active
authority: gameplay
tokens_est: 560
summary: "Key items, materials, start inv, shop"
---
# Items & Economy — Key items, materials, start inv, shop

**Hub:** [`ITEMS_AND_ECONOMY.md`](../ITEMS_AND_ECONOMY.md)

## 4. Key items (non-sellable)

| ID | Display | Obtain | Purpose |
|----|---------|--------|---------|
| `lacquer_box` | Lacquer Box | Start | Story; glow states; SC-16 choice |
| `cave_map` | Tidal Cave Map | SC-04 Roku | Unlocks cave entrance flag; journal entry |
| `wraith_pearl` | Wraith Pearl | SC-09 boss | Opens palace gate interior |

**Not in inventory UI as usable** — Quest / story flags display in Key Items tab (read-only).

---


## 5. Materials (sell only)

| ID | Display | Sell | Drop source |
|----|---------|------|-------------|
| `spirit_shard` | Spirit Shard | 8 | Tide Wraith |
| `palace_fragment` | Palace Fragment | 25 | Sentinel, Keeper |

No crafting v1. Sell at shop interface (future) or auto — **v1: no sell UI; materials auto-convert to coins on pickup** (optional simplification) OR stack in inventory sellable at Roku. **Decision: stack, sell via Tab → Items → Sell (single item type at a time).**

---


## 6. Starting inventory

| Character | Items |
|-----------|-------|
| Party (shared) | `sea_salve` ×2 |
| Urashima equip | `fisher_katana`, `worn_haori` |
| Yuzu equip | (none) on join |
| Roku equip | (none) on join; `diver_mail` in shop |

**Shell coins at start:** 0

---


## 7. Roku's shop (`roku_shack`)

**Open:** `met_roku` (SC-04)
**Restock:** After `shore_wraith_defeated` — +1 skill scroll each

| Item | Price | Stock |
|------|-------|-------|
| `sea_salve` | 40 | ∞ |
| `spirit_tonic` | 50 | ∞ |
| `coral_antidote` | 30 | ∞ |
| `cave_wet_coat` | 120 | 1 |
| `shell_charm` | 80 | 1 |
| `shrine_charm` | 120 | 1 |
| `diver_mail` | 150 | 1 |
| `harpoon_rod` | 150 | 1 |
| `spirit_knife` | 180 | 1 |
| Skill scroll: `returning_wave` | 200 | 1 (Urashima — early unlock, appears post SC-09 restock) |
| Skill scroll: `torii_ward` | 200 | 1 (Yuzu — early unlock, appears post SC-09 restock) |

**Interact:** E at shack → shop UI OR Tab → Shop when near Roku (shack radius 5m)

---
