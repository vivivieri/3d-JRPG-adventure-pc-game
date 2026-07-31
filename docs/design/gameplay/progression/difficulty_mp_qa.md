---
id: difficulty-mp-qa
type: reference
audience: [builder, builder_combat, qa]
phase: [2, 3]
status: active
authority: gameplay
tokens_est: 740
summary: "Difficulty, MP, milestones, workflow, QA"
---
# Progression & Tuning — Difficulty, MP, milestones, workflow, QA

**Hub:** [`PROGRESSION_TUNING.md`](../PROGRESSION_TUNING.md)

## When to read

Use **Progression & Tuning — Difficulty, MP, milestones, workflow, QA** (roles: builder, builder_combat, qa) when you need this reference during the current task Jump to a section below instead of reading end-to-end (8 sections).

## Jump to

- [6. Difficulty modes](#6-difficulty-modes)
- [Normal (default)](#normal-default)
- [Hard (`hard_mode: true` in settings)](#hard-hard_mode-true-in-settings)
- [Expected experience](#expected-experience)
- [7. MP economy by act](#7-mp-economy-by-act)
- [8. Milestone affordance table](#8-milestone-affordance-table)
- [9. Tuning workflow](#9-tuning-workflow)
- [10. QA checklist](#10-qa-checklist)


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

| Milestone | Coins (expected, from data) | Can afford |
|-----------|------------------------------|------------|
| Post SC-05 | ~10 | — (window shopping) |
| Post SC-09 (+Q2) | ~130–150 | 2–3 salves OR start saving |
| Pre-Sentinel | ~160–190 | Coat OR salve stock |
| Pre-Keeper | ~225–280 | Scroll (if saved) OR charm + salves |

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
