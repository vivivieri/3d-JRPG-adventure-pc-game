---
id: enemy-mp-scrolls
type: reference
phase: [2, 3]
audience: [builder, builder_combat]
status: active
authority: gameplay
tokens_est: 470
summary: "Skills Bible — Enemy skills, MP, scrolls — Tonic value: 25 MP ≈ 1–2 skills. Price tuned in `ITEMS_AND_ECONOMY.md`."
---
# Skills Bible — Enemy skills, MP, scrolls

**Hub:** [`SKILLS_BIBLE.md`](../SKILLS_BIBLE.md)

## When to read

Use **Skills Bible — Enemy skills, MP, scrolls** (roles: builder, builder_combat) when you need this reference during the current task Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [4. Enemy skills (reference)](#4-enemy-skills-reference)
- [5. MP economy](#5-mp-economy)
- [6. Skill scrolls (shop)](#6-skill-scrolls-shop)


## 4. Enemy skills (reference)

| ID | User | Effect |
|----|------|--------|
| `claw_snap` | Salt Crab | 1 enemy, ATK ×1.0 physical |
| `drown_touch` | Tide Wraith / bosses | 1 enemy, MAG ×1.1 water + 40% Poison 3t |
| `regret_surge` | Shore Wraith / Tide Keeper | All party, MAG ×1.3 spirit + 60% Def Down 2t |
| `sentinel_cleave` | Palace Sentinel | 1 enemy, ATK ×1.6 physical |
| `shell_harden` | Salt Crab / Sentinel | Self Def Up +4, 2t |
| `tide_lament` | Tide Keeper | All party, MAG ×1.5 water + 25% Stun 1t |

---


## 5. MP economy

| Act | Avg MP pool (Urashima) | Fights before oom |
|-----|------------------------|-------------------|
| I | 30 | 2 skills + items |
| II | 45 | 3–4 skills |
| III | 60 | Limit + rotation |

**Tonic value:** 25 MP ≈ 1–2 skills. Price tuned in `ITEMS_AND_ECONOMY.md`.

---


## 6. Skill scrolls (shop)

| Scroll | Teaches | Character | Notes |
|--------|---------|-----------|-------|
| `returning_wave` | Water AoE (normally Lv 10) | Urashima | Early unlock — most runs end before Lv 10 |
| `torii_ward` | Party regen + Def Up (normally Lv 8) | Yuzu | Early unlock for Sentinel/Keeper prep |

*Design: scrolls are an **early-unlock** purchase (200 coins each, stock 1, no restock) — a real
economy decision, not a safety net. If the character already learned the skill by level, the scroll
is greyed out in the shop. Data: `roku_shop.json` → `scrolls[]`.*

---
