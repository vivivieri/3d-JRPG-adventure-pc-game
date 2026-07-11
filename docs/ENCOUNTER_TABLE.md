# Tides of Urashima — Encounter & Pacing Table

**Version:** 1.0 (Pre-build)  
**Cross-refs:** `docs/GDD.md` §4–8, `docs/BOSS_DESIGNS.md`, `game/data/enemies/enemies.json`

---

## 1. Design goals

| Goal | Target |
|------|--------|
| Total combats (main path) | 6 unavoidable, up to 9 with optional |
| Level at final boss | 8–10 (cap 15) |
| Grinding required (Normal) | No |
| Fights per zone before boss | ~2 scripted triggers + 1 boss (no random encounters) |
| Playtime combat portion | ~35–40% of 2–3 hours |

---

## 2. XP & level curve

| Level | Cumulative XP | Expected reach |
|-------|---------------|----------------|
| 1 | 0 | Game start |
| 2 | 40 | After tutorial crab |
| 3 | 100 | Caves entrance |
| 4 | 180 | Pre–Shore Wraith |
| 5 | 280 | Post–Shore Wraith / Yuzu join |
| 6 | 400 | Palace approach |
| 7 | 540 | Sentinel fight |
| 8 | 700 | Pre–Tide Keeper |
| 9 | 880 | Tide Keeper phase 2 |
| 10 | 1080 | Choice gate |
| 11–15 | +200/level | Optional / Hard mode buffer |

**XP per fight (Normal):** Trash 25–35 | Elite 50–70 | Boss 100–250

---

## 3. Act I — The Return (~30 min)

| # | Scene | Zone | Encounter | Type | Party | XP | Level after |
|---|-------|------|-----------|------|-------|-----|-------------|
| 1 | SC-05 | Village outskirts | Salt Crab ×1 | Tutorial | Urashima | 30 | 2 |
| — | — | Village (optional) | — | Explore | — | — | — |

**No random encounters in hub** — fights are scripted triggers only (JRPG story pacing).

---

## 4. Act II — The Depths (~60 min)

| # | Scene | Zone | Encounter | Type | Party | XP | Level after |
|---|-------|------|-----------|------|-------|-----|-------------|
| 2 | SC-06 | Cave entrance | Salt Crab ×1 | Scripted (avoidable) | Urashima | 30 | 2–3 |
| 3 | SC-07 area | Flooded chamber | Salt Crab ×2 | Optional | Urashima | 60 | 3 |
| 4 | SC-08 | Deep pool | Tide Wraith ×2 | Forced | Urashima | 70 | 4 |
| 5 | SC-09 | Boss arena | **Shore Wraith** | Boss | Urashima solo | 120 | 4–5 |
| — | SC-10 | Shrine alcove | — | Yuzu joins | +party | — | 5 |

**Post SC-10 optional** (`enc_sc10_optional_wraith` — doubles as heal tutorial, `TUTORIAL_DESIGN.md` SC-10):

| # | Zone | Encounter | Type | Party | XP |
|---|------|-----------|------|-------|-----|
| 6 | Caves exit path | Tide Wraith ×1 | Optional | Urashima + Yuzu | 35 |

---

## 5. Act III — The Tide (~30–45 min)

| # | Scene | Zone | Encounter | Type | Party | XP | Level after |
|---|-------|------|-----------|------|-------|-----|-------------|
| 7 | SC-12 approach | Palace exterior | Tide Wraith ×2 | Scripted | Full party | 70 | 6 |
| 8 | SC-14 | Sentinel hall | **Palace Sentinel** | Miniboss | Full party | 100 | 7 |
| — | SC-13 | Mirror chamber | — | Dialogue only | — | — | — |
| 9 | SC-15 | Throne arena | **Tide Keeper** | Final boss | Full party | 250 | 8–10 |

**No fights after choice gate (SC-16).**

---

## 6. Encounter summary

| Enemy | Count (main path) | Role |
|-------|-------------------|------|
| Salt Crab | 2–4 | Tutorial + cave filler |
| Tide Wraith | 3–5 | Guilt / speed threat |
| Shore Wraith | 1 | Act II boss |
| Palace Sentinel | 1 | Spirit tutorial miniboss |
| Tide Keeper | 1 | Final boss |

**Total scripted encounters (data):** 9 in `story_encounters.json` — 6 unavoidable
(SC-05, SC-08, SC-09, SC-12, SC-14, SC-15), 1 avoidable (SC-06), 2 optional (SC-07 crabs, SC-10 wraith).

---

## 7. Economy pacing

**Currency:** Shell coins (環貝)

| Source | Amount |
|--------|--------|
| Per trash fight | 10–24 |
| Per boss | 45–100 |
| Q2 quest reward | 50 |
| Material sales (optional) | ~20–40 |
| **Expected total (pre-Keeper)** | ~225–280 coins |

### Roku's shop (`roku_shack`)

Available after SC-04; restocks after SC-09. **Full catalog:** `docs/ITEMS_AND_ECONOMY.md` §7.

| Item ID | Price | Stock | Notes |
|---------|-------|-------|-------|
| `sea_salve` | 40 | ∞ | Heal 80 HP |
| `coral_antidote` | 30 | ∞ | Cure poison |
| `spirit_tonic` | 50 | ∞ | Restore 25 MP |
| `shell_charm` | 80 | 1 | +2 DEF charm |
| Skill scrolls | 200 | 1 each | `returning_wave` (Urashima), `torii_ward` (Yuzu) — early unlocks |

**Design intent:** Player can afford several salves + one charm, OR save for one 200-coin scroll,
on the main path without grind (see `PROGRESSION_TUNING.md` §8 affordance table).

---

## 8. Equipment progression

| Slot | Act I | Act II | Act III |
|------|-------|--------|---------|
| Weapon | `fisher_katana` (start) | `tide_cut_saber` (chest SC-07) | `palace_edge` (Sentinel drop) |
| Armor | `worn_haori` | `cave_wet_coat` (shop) | — |
| Charm | — | `shell_charm` (shop) | `spirit_bell` (lore `sailor_charm`) |

Canonical IDs: `docs/ITEMS_AND_ECONOMY.md` §3.

---

## 9. Limit gauge tutorial

| When | Trigger |
|------|---------|
| SC-05 | First combat; gauge visible but not required |
| SC-09 | Boss at 50% HP — prompt: "Limit Ready" if gauge full |
| SC-15 | Phase 3 — encourage `box_unbound` (Urashima limit) |

**Fill rate:** 8% per 10 damage dealt, 5% per 10 damage taken.

---

## 10. Hard mode encounter deltas

Enable via settings menu (`hard_mode: true`).

| Change | Detail |
|--------|--------|
| Enemy HP | +15% |
| Enemy ATK | +10% |
| Intent delay | 0 on phase 2+ bosses |
| XP | +10% |
| Drops | Same |

**Audience:** Men 20–30 mastery optional — not required for endings.

---

## 11. Random encounter policy (v1)

**None.** All encounters are hand-placed triggers tied to storyboard scenes. This keeps 2–3 hour scope tight and supports authored environment composition (no combat in shrine hub).

Post-launch optional: 1 random encounter table in caves only.

---

## 12. QA checklist

- [ ] Main path completable at level 8 without optional fights
- [ ] Shop prices allow comfortable potion stock
- [ ] No soft-lock if player spends all coins before palace
- [ ] Yuzu present for Sentinel Spirit tutorial
- [ ] Solo Shore Wraith tuned (see `BOSS_DESIGNS.md`)
