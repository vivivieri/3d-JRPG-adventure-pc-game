# Tides of Urashima — Items & Economy

**Version:** 1.0 (Pre-build)  
**Cross-refs:** `docs/ENCOUNTER_TABLE.md`, `game/data/items/items.json`, `docs/QUEST_AND_FLAGS.md`, `docs/ITEMS_3D_MODEL_GUIDE.md`

**Canonical rule:** Item IDs in this doc match `items.json`. Display names shown for UI. **3D mesh specs:** `docs/ITEMS_3D_MODEL_GUIDE.md`.

---

## 1. Currency

| ID | Display name | Symbol | Notes |
|----|--------------|--------|-------|
| `shell_coin` | Shell Coin | 環貝 | Only currency; integer, no decimals |

**Sources:** Combat drops, quest rewards, lore (5 coins ×8 optional), sell materials  
**Sinks:** Roku's shop, no other vendors v1

---

## 2. Consumables

| ID | Display (EN) | Effect | Buy | Sell | Shop |
|----|--------------|--------|-----|------|------|
| `sea_salve` | Sea Salve | Heal 80 HP | 40 | 20 | ✓ ∞ |
| `spirit_tonic` | Spirit Tonic | Restore 25 MP | 50 | 25 | ✓ ∞ |
| `coral_antidote` | Coral Antidote | Cure poison | 30 | 15 | ✓ ∞ |

**Field use:** Allowed out of combat (except antidote if not poisoned — greyed)  
**Battle use:** All three  
**Stack limit:** 99 per slot type in inventory

*ENCOUNTER_TABLE "Potion/Antidote/Ether" names deprecated — use IDs above.*

---

## 3. Equipment

### Weapons

| ID | Display | Slot | Stats | Obtain | Equip |
|----|---------|------|-------|--------|-------|
| `fisher_katana` | Fisher's Katana | weapon | ATK +4, water | Start (Urashima) | urashima |
| `tide_cut_saber` | Tide-Cut Saber | weapon | ATK +7, water | SC-07 chest | urashima |
| `palace_edge` | Palace Edge | weapon | ATK +10, water | Sentinel drop | urashima |
| `spirit_knife` | Spirit Knife | weapon | MAG +5 | Shop 180 | yuzu |
| `harpoon_rod` | Harpoon Rod | weapon | ATK +6 | Shop 150 | roku |

### Armor

| ID | Display | Slot | Stats | Obtain | Equip |
|----|---------|------|-------|--------|-------|
| `worn_haori` | Worn Haori | armor | DEF +2 | Start (Urashima) | urashima |
| `cave_wet_coat` | Cave-Wet Coat | armor | DEF +4, RES +2 | Shop 120 | all |
| `diver_mail` | Diver's Mail | armor | DEF +5, HP +20 | Shop 150 | roku |

### Charms

| ID | Display | Slot | Stats | Obtain | Equip |
|----|---------|------|-------|--------|-------|
| `shrine_charm` | Shrine Charm | charm | MAG +3, RES +2 | Shop 120 | all |
| `spirit_bell` | Spirit Bell | charm | MAG +4, SPD +1 | Lore `lore_06` | all |
| `shell_charm` | Shell Charm | charm | DEF +2 | Shop 80 | all |

**Slots:** weapon + armor + charm (3 per character)  
**Swap:** Tab → Equipment; instant in field; not mid-combat

---

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
| Skill scroll: `tidal_slash` | 200 | 1 (Urashima) |
| Skill scroll: `purify` | 200 | 1 (Yuzu) |

**Interact:** E at shack → shop UI OR Tab → Shop when near Roku (shack radius 5m)

---

## 8. Economy pacing (main path)

| Milestone | Expected coins | Expected spends |
|-----------|----------------|-----------------|
| Post Act I | ~80 | 2 salves |
| Post Act II | ~200 | salves + 1 charm |
| Pre-final boss | ~350 | optional equipment |

**Soft-lock prevention:** Main path drops ≥300 coins without optional fights. SC-07 chest gives `tide_cut_saber` free.

---

## 9. Drop table summary

| Source | Coins | Items |
|--------|-------|-------|
| Salt Crab | 10 | — |
| Tide Wraith | 12 | `spirit_shard` 30% |
| Shore Wraith | 45 | `wraith_pearl` 100% |
| Palace Sentinel | 60 | `palace_edge` 100%, `palace_fragment` 50% |
| Tide Keeper | 100 | `palace_fragment` 100% |

---

## 10. items.json alignment

All equipment and key item IDs listed in §3–4 are present in `game/data/items/items.json` (schema v2). Update this doc if new items are added.

---

## 11. QA checklist

- [ ] Beat game without buying anything (Normal)
- [ ] Beat game without SC-07 chest (saber optional)
- [ ] No negative coin balance
- [ ] Key items cannot be sold or discarded
- [ ] Shop prices match this doc
