# Tides of Urashima — Skills Bible

**Version:** 1.0 (Pre-build)  
**Cross-refs:** `docs/COMBAT_SYSTEMS.md`, `game/data/skills/skills.json`, `game/data/characters/party.json`

**Player skills:** 15 loadout slots (5 per character) but **14 unique skill IDs** in `game/data/skills/skills.json` — Urashima and Roku both start with the shared basic-attack ID `strike`.  
**Enemy skills:** 6 (documented in `BOSS_DESIGNS.md` / `enemies.json`) — note `BOSS_DESIGNS.md` describes a much larger *target* per-boss kit not yet represented by these 6 IDs; see the reconciliation note at the top of that doc.

> **Sync note:** All tables below have been corrected to match `game/data/skills/skills.json` exactly (MP costs, power multipliers, effect types/potencies/targets). Treat `skills.json` as canonical for combat math; this doc is the annotated reference.

---

## 1. Urashima (Water)

| ID | Name | MP | Target | Power | Effects | Unlock |
|----|------|-----|--------|-------|---------|--------|
| `strike` | Strike | 0 | 1 enemy | ATK ×1.0 physical | — | Start |
| `tidal_slash` | Tidal Slash | 6 | 1 enemy | ATK ×1.35 water | — | Start |
| `ocean_veil` | Ocean Veil | 8 | 1 ally | — | Def Up +4, 3t | Lv 5 |
| `returning_wave` | Returning Wave | 14 | All enemies | MAG ×1.1 water | — | Lv 10 |
| `box_unbound` | Box Unbound | 0 | All enemies | MAG ×2.5 spirit | 50% Stun 1t | Limit |

`strike` is Urashima's basic attack and is shared with Roku (same skill ID, both use `power_stat: atk`).

**Role:** Flexible DPS + party Def buffer; AoE for adds phase.

---

## 2. Yuzu (Spirit)

| ID | Name | MP | Target | Power | Effects | Unlock |
|----|------|-----|--------|-------|---------|--------|
| `purify` | Purify | 5 | 1 enemy | MAG ×1.2 spirit | — | Join |
| `spirit_light` | Spirit Light | 7 | 1 ally | — | Heal 60 (flat) | Join |
| `sacred_mend` | Sacred Mend | 16 | All allies | — | Heal 40 (flat). *(No cleanse/status-cure effect in data — "Cure Def Down" is not implemented; add it to `skills.json` or drop the claim.)* | Lv 4 |
| `torii_ward` | Torii Ward | **12** | All allies | — | Regen 8 (≈% max HP/turn), 3t **+ Def Up +2, 3t** | Lv 8 |
| `last_prayer` | Last Prayer | 0 | All allies | — | Heal 999 (effectively full-heal, not literally "50% max HP") + Cleanse (all status) | Limit |

**Role:** Healer + Sentinel counter (Spirit damage).

---

## 3. Roku (Physical)

| ID | Name | MP | Target | Power | Effects | Unlock |
|----|------|-----|--------|-------|---------|--------|
| `strike` | Strike | 0 | 1 enemy | ATK ×1.0 physical | — | Join |
| `shell_guard` | Shell Guard | 4 | Self | — | Def Up +6, 2t | Join |
| `harpoon_drive` | Harpoon Drive | 8 | 1 enemy | ATK ×1.5 phys | Pierce 50% DEF *(not a Def Down debuff — data has no `def_down` effect on this skill)* | Lv 3 |
| `tide_taunt` | Tide Taunt | 6 | **Self** | — | Taunt (force enemy targeting) 2t + Def Up +3, 2t | Lv 7 |
| `depth_charge` | Depth Charge | 0 | **All enemies** | ATK ×2.2 phys | 80% Def Down -3, 2t | Limit |

**Role:** Tank + DEF shred; joins combat SC-12+.

---

## 4. Enemy skills (reference)

| ID | User | Effect |
|----|------|--------|
| `claw_snap` | Salt Crab | ATK ×1.0 physical |
| `shell_harden` | Salt Crab, Palace Sentinel | Self Def Up +4, 2t |
| `drown_touch` | Tide Wraith, Shore Wraith, Tide Keeper | MAG ×1.1 water + 40% Poison (potency 4, 3t) |
| `regret_surge` | Shore Wraith, Tide Keeper | AoE MAG ×1.3 spirit + 60% Def Down (potency 2, 2t) |
| `sentinel_cleave` | Palace Sentinel | ATK ×1.6 physical, single target |
| `tide_lament` | Tide Keeper | AoE MAG ×1.5 water + 25% Stun 1t — this is the **only** Tide Keeper skill currently in data; `BOSS_DESIGNS.md`'s richer per-phase kit (Tidal Fingers, Maelstrom, Last Mercy, etc.) is not yet implemented (see that doc's reconciliation note) |

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

- [ ] All 14 unique player skill IDs (across 15 loadout slots) usable in combat UI
- [ ] Level unlocks fire at correct levels
- [ ] Limit skills appear only at 100% gauge
- [ ] Yuzu heal sufficient for Normal without spam
