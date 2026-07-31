---
id: integrity-extend-pr
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, builder]
status: active
authority: engineering
tokens_est: 695
summary: "Integrity, extend, maintenance, anti-patterns, PR"
---
# JSON Data Style — Integrity, extend, maintenance, anti-patterns, PR

**Hub:** [`JSON_DATA_STYLE.md`](../JSON_DATA_STYLE.md)

## 8. Reference integrity rules

The validator enforces a closed graph — no dangling IDs.

```
scenes.json ──► flags.json
     │              ▲
     ▼              │
dialogue/*.json     │
encounters/*.json ──┘
     │
     ├──► enemies.json ──► skills.json
     ├──► items.json
     └──► quests/main_quests.json
```

```bash
python3 tools/validate_story_data.py   # L0_story_data — run after every edit
```

---


## 9. How to extend (step-by-step)

### New flag

1. Add row to `game/data/story/flags.json`
2. Reference from scene, dialogue choice, encounter, or quest
3. `python3 tools/validate_story_data.py`

### New item

1. Add to `game/data/items/items.json` with `id`, `display_name` i18n, `category`
2. Reference only by `id` from encounters, shop, scenes
3. Validate

### New QA catalog

1. Create `game/data/qa/<name>.json` with `version`, `authority`
2. Create `tools/validate_<name>.py` (PEP 8 — see [`PYTHON_STYLE.md`](../PYTHON_STYLE.md))
3. Add gate to `game/data/qa/acceptance_criteria.json`
4. Add `run_gate` to `tools/run_docs_ci_checks.sh`
5. Link in `docs/README.md` + hub

### New registry entry

See hub §5.4E — always update the authority doc and matching validator.

---


## 10. Maintenance order

Edit upstream before downstream:

1. `story/scenes.json` + `story/flags.json`
2. `quests/main_quests.json`
3. `items/items.json` + `starting/new_game.json`
4. `encounters/story_encounters.json`
5. `dialogue/chapter_01.json`
6. `shop/roku_shop.json` + `achievements/achievements.json`

---


## 11. Anti-patterns

| Don't | Do instead |
|-------|------------|
| Gameplay numbers only in markdown docs | Put values in JSON; docs explain intent |
| New flag inline in dialogue only | Register in `flags.json` first |
| `camelCase` keys | `snake_case` |
| Duplicate IDs across files | One authoritative file per entity type |
| Large prose blocks in JSON | Keep lines concise; long text in dialogue arrays |
| Edit JSON without validation | Always run matching `validate_*.py` |

---


## 12. PR checklist (JSON)

- [ ] 2-space indent, UTF-8, trailing newline
- [ ] `snake_case` keys and IDs
- [ ] i18n objects complete for ship-facing strings
- [ ] `schema_version` / `version` bumped if breaking
- [ ] Upstream-before-downstream edit order
- [ ] `python3 tools/validate_story_data.py` (and domain validator)
- [ ] `python3 tools/check_json_style.py` (`L1_json_style`)
- [ ] `bash tools/run_docs_ci_checks.sh` green
