---
id: currency-consumables-equip
type: reference
phase: [2, 3]
audience: [builder, builder_combat, qa]
status: active
authority: gameplay
tokens_est: 690
summary: "Sources: Combat drops, quest rewards, sell materials *(lore-entry coin bonus cut for v1 — `lore_entries.json` has no reward field)*"
---
# Items & Economy — Currency, consumables, equipment

**Hub:** [`ITEMS_AND_ECONOMY.md`](../ITEMS_AND_ECONOMY.md)

## When to read

Use **Items & Economy — Currency, consumables, equipment** (roles: builder, builder_combat, qa) when you need this reference during the current task Jump to a section below instead of reading end-to-end (6 sections).

## Jump to

- [1. Currency](#1-currency)
- [2. Consumables](#2-consumables)
- [3. Equipment](#3-equipment)
- [Weapons](#weapons)
- [Armor](#armor)
- [Charms](#charms)


## 1. Currency

| ID | Display name | Symbol | Notes |
|----|--------------|--------|-------|
| `shell_coin` | Shell Coin | 環貝 | Only currency; integer, no decimals |

**Sources:** Combat drops, quest rewards, sell materials *(lore-entry coin bonus cut for v1 — `lore_entries.json` has no reward field)*
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
| `spirit_bell` | Spirit Bell | charm | MAG +4, SPD +1 | Lore `sailor_charm` (read grant) | all |
| `shell_charm` | Shell Charm | charm | DEF +2 | Shop 80 | all |

**Slots:** weapon + armor + charm (3 per character)
**Swap:** Tab → Equipment; instant in field; not mid-combat

---
