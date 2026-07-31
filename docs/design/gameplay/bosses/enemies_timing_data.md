---
id: enemies-timing-data
type: reference
audience: [builder, builder_combat, qa]
phase: [2, 5]
status: active
authority: gameplay
tokens_est: 772
summary: "Tutorial/standard enemies, timing, data, playtest"
---
# Boss Designs — Tutorial/standard enemies, timing, data, playtest

**Hub:** [`BOSS_DESIGNS.md`](../BOSS_DESIGNS.md)

## When to read

Use **Boss Designs — Tutorial/standard enemies, timing, data, playtest** (roles: builder, builder_combat, qa) when you need this reference during the current task Jump to a section below instead of reading end-to-end (7 sections).

## Jump to

- [5. Tutorial enemy — Salt Crab (`salt_crab`)](#5-tutorial-enemy-salt-crab-salt_crab)
- [6. Standard enemies (non-boss patterns)](#6-standard-enemies-non-boss-patterns)
- [Tide Wraith (`tide_wraith`)](#tide-wraith-tide_wraith)
- [Salt Crab (`salt_crab`) — field](#salt-crab-salt_crab-field)
- [7. Boss intro / outro timing](#7-boss-intro-outro-timing)
- [8. Data implementation notes](#8-data-implementation-notes)
- [9. Playtest acceptance](#9-playtest-acceptance)


## 5. Tutorial enemy — Salt Crab (`salt_crab`)

**Storyboard:** SC-05
**Not a boss** but combat template.

| Stat | HP 40 | ATK 7 | DEF 5 | SPD 6 |
|------|-------|-------|-------|-------|
| Skills | `claw_snap` (ATK ×1.0) 80% / `shell_harden` (Def Up) 20% below 50% HP |
| AI | Weighted (see `enemies.json`) |
| Tutorial | Force Attack → Skill → Defend prompts |

Guaranteed win; no escape needed.

---


## 6. Standard enemies (non-boss patterns)

### Tide Wraith (`tide_wraith`)

| HP 50 | ATK 6 | MAG 10 | DEF 4 | RES 6 | SPD 9 |
|-------|-------|--------|-------|-------|-------|
| Skill | `drown_touch` — MAG ×1.1 water + 40% Poison 3 turns |
| AI | Weighted 100% `drown_touch` |
| Drops | `spirit_shard` 30% |

### Salt Crab (`salt_crab`) — field

See tutorial above; field versions identical, lower XP.

---


## 7. Boss intro / outro timing

| Boss | Intro | Phase banner | Death to next scene |
|------|-------|--------------|---------------------|
| Shore Wraith | 5s emerge | 2s | 3s → SC-10 |
| Palace Sentinel | 3s march | — | 2s → SC-15 setup |
| Tide Keeper | 6s rise | 2s each phase | Choice → ending (no return) |

---


## 8. Data implementation notes

Boss phases are already encoded in `game/data/enemies/enemies.json` — the combat runtime consumes:

```json
{
  "ai": { "type": "phase", "phases": [{ "hp_above": 0.5, "weights": [...] }] },
  "phases": [
    { "hp_threshold": 0.5, "announcement": "The drowned rise with me!" },
    { "hp_threshold": 0.1, "announcement": "Choose.", "triggers_choice": true }
  ]
}
```

- `ai.phases[].hp_above` — skill-weight bands (behavior per phase)
- `phases[].hp_threshold` — banner announcements; `triggers_choice: true` freezes combat and sets `tide_keeper_phase3`
- Hard mode multipliers (HP ×1.15, ATK ×1.10, intent delay 0 in phase 2+) are applied at runtime from `user://settings.json` → `hard_mode: bool` — not stored per enemy.

---


## 9. Playtest acceptance

- [ ] First-time player beats Shore Wraith without grinding (≤ 2 attempts)
- [ ] Sentinel teaches Yuzu Spirit skill without explicit text wall
- [ ] Tide Keeper fight 8–12 minutes Normal
- [ ] Choice gate cannot be skipped accidentally; confirm button required
- [ ] All intent icons match action outcome 100%
