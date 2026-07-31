---
id: combat-barks
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, builder]
status: active
authority: engineering
tokens_est: 487
summary: "Data — Combat & Economy — Enemy combat_barks — Boss/elite enemies may define inline combat bark copy in `enemies/enemies.json` (v1 bosses: `shore_wraith`."
---
# Data — Combat & Economy — Enemy combat_barks

**Hub:** [`combat_economy.md`](../combat_economy.md)

## When to read

Use **Data — Combat & Economy — Enemy combat_barks** (roles: architect, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (2 sections).

## Jump to

- [18. `combat_barks` on enemy entries](#18-combat_barks-on-enemy-entries)
- [Ending gallery copy](#ending-gallery-copy)


## 18. `combat_barks` on enemy entries

Boss/elite enemies may define inline combat bark copy in `enemies/enemies.json` (v1 bosses: `shore_wraith`, `palace_sentinel`, `tide_keeper`; field mobs: `salt_crab`, `tide_wraith`). Intent UI shows one bark per telegraphed action; defeat lines are tragic, not celebratory (`BOSS_DESIGNS.md` §1, `NARRATIVE_WRITING_GUIDE.md` §12). Field mobs may omit `battle_start` (tutorial clarity).

```json
"combat_barks": {
  "battle_start": { "en": "...", "ja": "...", "zh": "...", "zh-Hant": "..." },
  "on_defeat": { "en": "...", "ja": "...", "zh": "...", "zh-Hant": "..." },
  "skills": {
    "drown_touch": { "en": "...", "ja": "...", "zh": "...", "zh-Hant": "..." }
  },
  "phases": [
    { "hp_threshold": 0.5, "text": { "en": "...", "ja": "...", "zh": "...", "zh-Hant": "..." } }
  ]
}
```

| Field | Rule |
|-------|------|
| `skills` keys | Must exist in the enemy's `skills[]` array |
| `phases[].hp_threshold` | Should match a `phases[].hp_threshold` on the same enemy when phases exist |
| Locales | `en` / `ja` / `zh` / `zh-Hant` required on every text object |

**Runtime (Phase 3+):** `CombatManager` reads barks by `skill_id` when intent telegraphs; `on_defeat` plays before encounter `on_win` rewards. Data-only until combat UI wires.

### Ending gallery copy

`game/data/narrative/ending_gallery.json` — three ending slots with `philosophy_blurb` per `REPLAY_DESIGN.md` §4. No "recommended" badge. `ending_chosen` values must match `flags.json`.
