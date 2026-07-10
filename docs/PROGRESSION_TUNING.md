# Tides of Urashima — Progression & Tuning Sheet

**Version:** 1.0 (Pre-build)  
**Cross-refs:** `docs/ENCOUNTER_TABLE.md`, `docs/COMBAT_SYSTEMS.md`, `game/data/characters/party.json`, `game/data/shop/roku_shop.json`, `docs/ITEMS_AND_ECONOMY.md`

**Single source of truth** for level curve, party stats at milestones, economy affordances, and difficulty modes.

---

## 1. Design targets

| Target | Value |
|--------|-------|
| Level cap | 15 |
| Final boss party level (main path) | 8–10 |
| Grinding required (Normal) | No |
| Expected deaths (Normal, main path) | 0–2 total |
| Expected deaths (Hard, first clear) | 1–4 |
| Playtime | 2–3 hours |

---

## 2. XP curve

| Level | Cumulative XP | Typical reach (scene) |
|-------|---------------|------------------------|
| 1 | 0 | Start |
| 2 | 40 | SC-05 tutorial crab |
| 3 | 100 | SC-06–07 caves |
| 4 | 180 | SC-08 pre-boss |
| 5 | 280 | SC-09 Shore Wraith clear |
| 6 | 400 | SC-12 palace approach |
| 7 | 540 | SC-14 Sentinel |
| 8 | 700 | SC-15 Tide Keeper start |
| 9 | 880 | Tide Keeper phase 2 |
| 10 | 1080 | SC-16 choice gate |
| 11–15 | +200/level | Optional / Hard buffer |

**XP per fight:** Trash 25–35 | Pair 55–70 | Boss 100–250 (`ENCOUNTER_TABLE.md`)

### Main-path XP budget

| Fight | XP | Running total (approx) |
|-------|-----|------------------------|
| SC-05 crab | 30 | 30 → L2 |
| SC-06 crab | 30 | 60 |
| SC-08 wraiths | 70 | 130 → L3–4 |
| SC-09 Shore Wraith | 120 | 250 → L5 |
| SC-12 wraiths | 70 | 320 |
| SC-14 Sentinel | 100 | 420 → L6–7 |
| SC-15 Tide Keeper | 250 | 670 → L8–10 |

Quest XP (`QUEST_AND_FLAGS.md`): +30 (Q1) +100 (Q2) + etc. — included in encounter pacing.

---

## 3. Party stats at milestones

Formula: `base + growth × (level − 1)` from `party.json`.

### Urashima (active entire game)

| Level | HP | MP | ATK | DEF | MAG | RES | SPD | Scene |
|-------|-----|-----|-----|-----|-----|-----|-----|-------|
| 1 | 120 | 30 | 14 | 10 | 8 | 9 | 11 | SC-01 |
| 4 | 156 | 39 | 20 | 13 | 11 | 12 | 14 | SC-08 |
| 5 | 168 | 42 | 22 | 14 | 12 | 13 | 15 | SC-09 boss |
| 7 | 192 | 48 | 26 | 16 | 14 | 15 | 17 | SC-14 |
| 10 | 228 | 57 | 32 | 19 | 17 | 18 | 20 | SC-16 |

**Skill unlocks:** Lv5 `ocean_veil` | Lv10 `returning_wave` | Limit `box_unbound`

### Yuzu (joins SC-10, enters at ~party L5)

| Level | HP | MP | MAG | RES | Notes |
|-------|-----|-----|-----|-----|-------|
| 5 | 117 | 65 | 22 | 16 | Join fight |
| 7 | 133 | 75 | 26 | 18 | Sentinel |
| 10 | 157 | 90 | 32 | 21 | Final boss |

**Skill unlocks:** Lv4 `sacred_mend` | Lv8 `torii_ward` | Join: `purify`, `spirit_light`

### Roku (combat SC-12+, enters at ~party L6)

| Level | HP | MP | ATK | DEF | Notes |
|-------|-----|-----|-----|-----|-------|
| 6 | 225 | 25 | 22 | 24 | First fight |
| 7 | 240 | 27 | 24 | 26 | Sentinel |
| 10 | 285 | 33 | 30 | 32 | Final boss |

**Skill unlocks:** Lv3 `harpoon_drive` | Lv7 `tide_taunt` | Join: `shell_guard`

---

## 4. Equipment & power spikes

| Milestone | Urashima weapon | ATK equiv | Other |
|-----------|-----------------|-----------|-------|
| Start | `fisher_katana` | +4 | `worn_haori` +2 DEF |
| SC-07 chest | `tide_cut_saber` | +7 | Optional puzzle reward |
| SC-14 drop | `palace_edge` | +10 | Best weapon |

| Shop (SC-04+) | Price | When affordable |
|---------------|-------|-----------------|
| `sea_salve` ×2 | 80 | Act I |
| `cave_wet_coat` | 120 | Post SC-09 (~200 coins) |
| `shell_charm` | 80 | Act II |
| Skill scroll | 200 | Post boss (~250 coins) |

**Affordance rule:** Main path grants ≥300 coins without optional fights. Player can buy 6–8 salves + one charm OR one scroll.

---

## 5. Boss tuning reference

| Boss | Party at fight | Solo? | HP target (Normal) | Attempts target |
|------|----------------|-------|--------------------|-----------------|
| Shore Wraith | Urashima L4–5 | Yes | ~320 HP (solo tune) | ≤2 |
| Palace Sentinel | Full L6–7 | No | 380 HP | ≤2 |
| Tide Keeper | Full L8–10 | No | 900 HP | ≤3 |

Full patterns: `BOSS_DESIGNS.md`. Sentinel Spirit ×1.5 for Yuzu skills.

---

## 6. Difficulty modes

### Normal (default)

| Parameter | Value |
|-----------|-------|
| Enemy HP | 100% |
| Enemy ATK | 100% |
| Boss intent preview | 1 turn ahead |
| XP | 100% |
| Tutorials | On first play |
| Target player | Story-first; no grind |

### Hard (`hard_mode: true` in settings)

| Parameter | Value |
|-----------|-------|
| Enemy HP | 115% |
| Enemy ATK | 110% |
| Boss phase 2+ intent | Same-turn (no preview) |
| XP | 110% |
| Tide Keeper choice gate | 15% HP (less room) |
| Target player | Pattern mastery; men 20–30 optional challenge |

**Hard does not:** Lock endings, remove tutorials on first play, add permadeath.

### Expected experience

| Mode | Deaths | Item use |
|------|--------|----------|
| Normal | 0–2 | 4–8 salves whole run |
| Hard | 1–4 | 8–12 salves; tonics at bosses |

---

## 7. MP economy by act

| Act | Urashima MP | Fights before empty | Mitigation |
|-----|-------------|---------------------|------------|
| I | 30–42 | 2 skill rotations | 2 start salves |
| II | 42–48 | 3 rotations | Shop tonics |
| III | 48–57 | Limit + full kit | `spirit_tonic` buy |

**Tonic:** 25 MP ≈ 1–2 skills (`SKILLS_BIBLE.md` §5).

---

## 8. Milestone affordance table

| Milestone | Coins (expected) | Can afford |
|-----------|------------------|------------|
| Post SC-05 | ~40 | 1 salve |
| Post SC-09 | ~200 | 3 salves + charm OR save for scroll |
| Pre-Sentinel | ~280 | Coat + salves |
| Pre-Keeper | ~350 | Scroll + stock |

---

## 9. Tuning workflow

1. Run main path at Normal — record level per scene
2. If Sentinel too easy at L7 → reduce trash XP or boss HP −5%
3. If Shore Wraith wipes solo Urashima → HP −10% or ATK −1
4. Hard mode pass after Normal locked
5. Update this doc + `enemies.json` together

---

## 10. QA checklist

- [ ] Main path completable L8+ without optional fights
- [ ] Shore Wraith solo win ≤2 attempts Normal
- [ ] Sentinel beatable without grind; Yuzu Spirit clearly helps
- [ ] Tide Keeper 8–12 min Normal
- [ ] Shop: beat game buying only salves
- [ ] Hard Sentinel noticeably tougher
- [ ] Level-up restores HP/MP fully
