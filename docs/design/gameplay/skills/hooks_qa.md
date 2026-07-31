---
id: hooks-qa
type: reference
phase: [2, 3]
audience: [builder, builder_combat]
status: active
authority: gameplay
tokens_est: 267
summary: "Skills Bible — Animation/SFX hooks + QA — - [ ] 14 player skills all usable in combat UI (strike shared by Urashima + Roku)"
---
# Skills Bible — Animation/SFX hooks + QA

**Hub:** [`SKILLS_BIBLE.md`](../SKILLS_BIBLE.md)

## When to read

Use **Skills Bible — Animation/SFX hooks + QA** (roles: builder, builder_combat) when you need this reference during the current task Jump to a section below instead of reading end-to-end (2 sections).

## Jump to

- [7. Animation / SFX hooks](#7-animation-sfx-hooks)
- [8. QA checklist](#8-qa-checklist)

## 7. Animation / SFX hooks

| Skill type | Animation key | SFX |
|------------|---------------|-----|
| Physical melee | `attack_melee` | `hit_physical` |
| Water | `slash_water` / `aoe_water` | `skill_water_*` |
| Spirit | `cast_spirit` / `heal_single` | `skill_spirit_*` / `skill_heal` |
| Limit | `limit_*` | `limit_burst` |

---


## 8. QA checklist

- [ ] 14 player skills all usable in combat UI (strike shared by Urashima + Roku)
- [ ] Skills Bible tables match `skills.json` (spot-check MP costs + targets)
- [ ] Level unlocks fire at correct levels
- [ ] Limit skills appear only at 100% gauge
- [ ] Yuzu heal sufficient for Normal without spam
