---
id: locale-tools
type: reference
audience: [architect, builder]
status: active
authority: engineering
tokens_est: 401
summary: "Locale + tools + migration"
---
# Data — i18n & Validation — Locale + tools + migration

**Hub:** [`i18n_validation.md`](../i18n_validation.md)

## 12. Localization split

| Content | Where |
|---------|-------|
| Dialogue lines | `dialogue/*.json` inline `{ en, ja, zh, zh-Hant }` |
| UI, tutorials, combat log, skill/enemy names | `game/locale/translations.csv` (core keys ship; expand in Phase 3) |
| Quest / item / lore display text | JSON inline `display_name` / `title` objects — **JSON is authoritative**; CSV mirrors optional |

---


## 13. Validation tools (implemented)

```bash
python3 tools/validate_story_data.py   # L0 gate — run after every data edit
```

Checks (see the script for the authoritative list):
- Every dialogue/scene/hook reference resolves (scenes, dialogue blocks, cinematic hooks, VO clips)
- Every `set_flags` / `requires_flags` (incl. dialogue choices) exists in `flags.json`
- Quest stage completion flags exist in the registry
- Encounter `scene_id` / `enemies` / `grant_items` / `on_phase_trigger` flags resolve
- Enemy `skills` and drop `item_id`s exist; party skills/unlocks/limits exist
- Shop inventory items and scroll `skill_id`s exist

---


## 14. Migration from old 3-quest data

| Old | New |
|-----|-----|
| 3 quests | 5 quests (split palace + ending) |
| `caves_unlocked` | `caves_entered` + `cave_entrance_unlocked` |
| 10 items | 20 items (equipment + keys) |
| 15 dialogue scenes | 22+ (add SC-00, 05, 09, 16, 17*) |

---
