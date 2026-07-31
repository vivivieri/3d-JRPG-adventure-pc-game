---
id: targets-xp
type: reference
audience: [builder, builder_combat, qa]
phase: [2, 3]
status: active
authority: gameplay
tokens_est: 485
summary: "Design targets + XP curve"
---
# Progression & Tuning — Design targets + XP curve

**Hub:** [`PROGRESSION_TUNING.md`](../PROGRESSION_TUNING.md)

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

**Quest XP is additive** (`main_quests.json`): Q1 +30, Q2 +100, Q3 +50, Q4 +100, Q5 +250 (= 530 total).
Pre–Tide Keeper the player has fight XP 420 + quest XP 280 (Q1–Q4) ≈ **700 → L8**, which is how the
curve reaches its target without grinding. Q5's 250 XP lands post-choice (flavor only). Boss kills do
**not** double-grant quest XP — encounter rewards come from `enemies.json`, quest rewards from
`main_quests.json`, both fire once.

---
