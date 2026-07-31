---
id: encounters-items
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, builder]
status: active
authority: engineering
tokens_est: 626
summary: "Encounters + story items"
---
# Data — Combat & Economy — Encounters + story items

**Hub:** [`combat_economy.md`](../combat_economy.md)

## 6. Encounter data (`encounters/story_encounters.json`)

Hand-placed fights only — no random tables.

```json
{
  "id": "enc_sc05_tutorial_crab",
  "scene_id": "SC-05",
  "zone": "ruined_village",
  "trigger": "TutorialEncounter",
  "enemies": ["salt_crab"],
  "party": ["urashima"],
  "tutorial": true,
  "on_win": { "set_flags": ["tutorial_combat_done"], "grant_items": [] }
}
```

Maps 1:1 to `ENCOUNTER_TABLE.md`. Optional fields: `optional: true`, `boss: true`,
`escape_allowed: false`, `requires_flags: [...]`, `cinematic_hook`, and
`on_phase_trigger: { "set_flags": [...] }` (fires when an enemy's `phases[].triggers_choice`
threshold is hit mid-combat — used by the Tide Keeper choice gate).

**Persistence / re-entry contract:** every encounter ID is appended to the save's
`encounters_completed[]` on **win**. Completed triggers never re-fire (on backtrack, reload, or
zone re-entry). On **escape or defeat** the trigger stays armed. This prevents both retrigger
loops and XP/coin farming.

---


## 8. Items tied to story beats

| Story beat | Item data |
|------------|-----------|
| SC-01 / start | `lacquer_box`, `fisher_katana`, `worn_haori`, 2× `sea_salve` |
| SC-04 | `cave_map` (key) |
| SC-07 chest | `tide_cut_saber` |
| SC-09 boss | `wraith_pearl` (key) |
| SC-14 boss | `palace_edge` |
| Lore read | `spirit_bell` — `items.json` `story_grant: "sailor_charm"` (granted when the `sailor_charm` lore entry is read; matches `lore_entries.json` id) |

### Reward ownership rule (avoid double-grants)

Several story items may be **documented** in multiple files (enemy `drops`, quest `rewards.items`, item `story_grant` trace the story beat), but **exactly one path grants** the item at runtime:

- **Combat/story key items:** the encounter `on_win.grant_items` is the single source that actually adds the item to inventory.
- Enemy `drops`, quest `rewards.items`, and item `story_grant` for the *same* item are **descriptive only** (UI/economy documentation) and must be no-ops at runtime, or de-duplicated by item id on grant.
- Quest `rewards` should otherwise grant only XP/gold (distinct from the combat drop).

The runtime grant code and `validate_story_data.py` should enforce single-grant-per-item-id.

---
