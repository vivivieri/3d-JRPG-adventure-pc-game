# Tides of Urashima — Skills Bible

**Version:** 1.0 (Pre-build)  
**Cross-refs:** `docs/COMBAT_SYSTEMS.md`, `game/data/skills/skills.json`, `game/data/characters/party.json`

**Player skills:** 14 unique IDs across 15 character slots (`strike` is shared by Urashima & Roku)  
**Enemy skills:** 6 (documented in `BOSS_DESIGNS.md` / `enemies.json`)

> **Source of truth:** `game/data/skills/skills.json` is authoritative for MP cost, target, power, and effects. The tables below mirror it — if they ever diverge, the JSON wins and this doc must be resynced.

---

## 1. Urashima (Water)

| ID | Name | MP | Target | Power | Effects | Unlock |
|----|------|-----|--------|-------|---------|--------|
| `strike` | Strike | 0 | 1 enemy | ATK ×1.0 | — | Start |
| `tidal_slash` | Tidal Slash | 6 | 1 enemy | ATK ×1.35 water | — | Start |
| `ocean_veil` | Ocean Veil | 8 | 1 ally | — | Def Up +4, 3t | Lv 5 |
| `returning_wave` | Returning Wave | 14 | All enemies | MAG ×1.1 water | — | Lv 10 |
| `box_unbound` | Box Unbound | 0 | All enemies | MAG ×2.5 spirit | 50% Stun 1t | Limit |

**Role:** Flexible DPS + party Def buffer; AoE for adds phase.

---

## 2. Yuzu (Spirit)

| ID | Name | MP | Target | Power | Effects | Unlock |
|----|------|-----|--------|-------|---------|--------|
| `purify` | Purify | 5 | 1 enemy | MAG ×1.2 spirit | — | Join |
| `spirit_light` | Spirit Light | 7 | 1 ally | Heal 60 | — | Join |
| `sacred_mend` | Sacred Mend | 16 | All allies | Heal 40 | — | Lv 4 |
| `torii_ward` | Torii Ward | 12 | All allies | — | Regen 3t (+8), Def Up +2 3t | Lv 8 |
| `last_prayer` | Last Prayer | 0 | All allies | Full heal (999) | Cleanse all status | Limit |

**Role:** Healer + Sentinel counter (Spirit damage).

---

## 3. Roku (Physical)

| ID | Name | MP | Target | Power | Effects | Unlock |
|----|------|-----|--------|-------|---------|--------|
| `strike` | Strike | 0 | 1 enemy | ATK ×1.0 | — | Join |
| `shell_guard` | Shell Guard | 4 | Self | — | Def Up +6, 2t | Join |
| `harpoon_drive` | Harpoon Drive | 8 | 1 enemy | ATK ×1.5 phys | Ignore 50% DEF (pierce) | Lv 3 |
| `tide_taunt` | Tide Taunt | 6 | Self | — | Taunt 2t + Def Up +3, 2t | Lv 7 |
| `depth_charge` | Depth Charge | 0 | All enemies | ATK ×2.2 phys | Def Down -3, 2t (80%) | Limit |

**Role:** Tank + DEF shred; joins combat SC-12+.

---

## 4. Enemy skills (reference)

| ID | User | Effect |
|----|------|--------|
| `claw_snap` | Salt Crab | ATK ×1.0 |
| `drown_touch` | Tide Wraith, Shore Wraith, Tide Keeper | MAG ×1.1 water + 40% Poison |
| `regret_surge` | Shore Wraith, Tide Keeper | AoE MAG ×1.3 spirit + 60% Def Down |
| `sentinel_cleave` | Palace Sentinel | ATK ×1.6 |
| `shell_harden` | Salt Crab, Palace Sentinel | Def Up +4, 2t |
| `tide_lament` | Tide Keeper | AoE MAG ×1.5 water + 25% Stun |

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

| Scroll | Teaches | Character |
|--------|---------|-----------|
| `tidal_slash` | Already known at start — scroll is backup if skipped | Urashima |
| `purify` | Backup for Yuzu | Yuzu |

*Design: scrolls are safety net for players who missed join tutorials.*

---

## 7. Animation / SFX hooks

| Skill type | Animation key | SFX |
|------------|---------------|-----|
| Physical melee | `attack_melee` | `hit_physical` |
| Water | `slash_water` / `aoe_water` | `skill_water_*` |
| Spirit | `cast_spirit` / `heal_single` | `skill_spirit_*` / `skill_heal` |
| Limit | `limit_*` | `limit_burst` |

---

## 8. QA checklist

- [ ] All 14 unique player skills usable in combat UI (Strike shared by Urashima & Roku)
- [ ] Level unlocks fire at correct levels
- [ ] Limit skills appear only at 100% gauge
- [ ] Yuzu heal sufficient for Normal without spam
