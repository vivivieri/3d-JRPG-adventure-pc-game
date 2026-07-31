---
id: party-kits
type: reference
phase: [2, 3]
audience: [builder, builder_combat]
status: active
authority: gameplay
tokens_est: 518
summary: "Urashima, Yuzu, Roku skills"
---
# Skills Bible — Urashima, Yuzu, Roku skills

**Hub:** [`SKILLS_BIBLE.md`](../SKILLS_BIBLE.md)

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
| `torii_ward` | Torii Ward | 12 | All allies | — | Regen 8/turn 3t + Def Up +2 3t | Lv 8 |
| `last_prayer` | Last Prayer | 0 | All allies | Full heal (999) | Cleanse all status | Limit |

**Role:** Healer + Sentinel counter (Spirit damage).

---


## 3. Roku (Physical)

| ID | Name | MP | Target | Power | Effects | Unlock |
|----|------|-----|--------|-------|---------|--------|
| `strike` | Strike | 0 | 1 enemy | ATK ×1.0 | — | Join |
| `shell_guard` | Shell Guard | 4 | Self | — | Def Up +6, 2t | Join |
| `harpoon_drive` | Harpoon Drive | 8 | 1 enemy | ATK ×1.5 phys | Ignores 50% DEF (`pierce_def: 0.5`) | Lv 3 |
| `tide_taunt` | Tide Taunt | 6 | Self | — | Taunt 2t (enemies target Roku) + Def Up +3 2t | Lv 7 |
| `depth_charge` | Depth Charge | 0 | All enemies | ATK ×2.2 phys | 80% Def Down -3, 2t | Limit |

**Role:** Tank + DEF shred; joins combat SC-12+.

---
