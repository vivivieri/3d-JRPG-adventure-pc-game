# JSON Data Style Guide — Tides of Urashima

**Version:** 1.0  
**Scope:** `game/data/**/*.json` — story, combat, registries, QA catalogs  
**Hub:** [`CODING_STANDARDS_HUB.md`](CODING_STANDARDS_HUB.md)  
**Architecture:** [`DATA_ARCHITECTURE.md`](DATA_ARCHITECTURE.md)

---

## 1. Industry standards (authoritative externals)

| Standard | Reference | What it governs |
|----------|-----------|-----------------|
| **JSON syntax** | [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259) | Valid UTF-8, double-quoted keys, no trailing commas |
| **API / schema style** | [Google JSON Style Guide](https://google.github.io/styleguide/jsoncstyleguide.xml) | Property naming, versioning, consistency |
| **i18n keys** | [BCP 47](https://www.rfc-editor.org/info/bcp47) | Locale tags: `en`, `ja`, `zh`, `zh-Hant` |

**Project rule:** `game/data/*.json` is the **runtime source of truth** for numeric gameplay values — design-doc prose is secondary.

---

## 2. File format rules

| Rule | Detail |
|------|--------|
| Encoding | UTF-8 (no BOM) |
| Indentation | **2 spaces** — no tabs |
| Trailing newline | One `\n` at EOF |
| Key quotes | Double quotes only |
| Trailing commas | **Forbidden** (invalid JSON) |
| Comments | **Forbidden** in committed JSON — use `_comment` field only in dev stubs if ever needed |
| Root shape | Object `{}` preferred; top-level arrays only when catalog is naturally a list |

**Pretty-print when committing:**

```python
json.dumps(data, indent=2, ensure_ascii=False) + "\n"
```

---

## 3. Naming conventions

| Kind | Convention | Example |
|------|------------|---------|
| Object keys | `snake_case` | `set_flags`, `requires_flags`, `schema_version` |
| Story scene IDs | `SC-NN` or `SC-NN-NAME` | `SC-02-WELL` |
| Zone IDs | `snake_case` | `ruined_village` |
| Flag / item / enemy / skill IDs | `snake_case` | `shore_wraith_defeated` |
| Encounter IDs | `enc_<context>_<name>` | `enc_sc09_shore_wraith` |
| Quest IDs | `snake_case` | `the_return` |
| Registry artifact IDs | `snake_case` | `data_story_spine` |
| QA gate IDs | `L0_*`, `L1_*`, `INT-*` | `L0_story_data` |

**Avoid:** `camelCase`, `kebab-case`, spaces, ambiguous duplicates (`caves_unlocked` vs `caves_entered`).

---

## 4. Schema metadata

Every catalog or gameplay file should declare version at the top level.

| Key | Type | Used in |
|-----|------|---------|
| `schema_version` | integer | Gameplay files (`scenes.json`, `items.json`, …) |
| `version` | string (`"1.0"`) | QA catalogs, audio metadata |
| `authority` | string path | QA / factory catalogs — doc that owns the schema |
| `description` | string | Human summary (optional) |

**Bump rules:**

| Change | Action |
|--------|--------|
| Add optional field | Usually no bump |
| Rename / remove field | Bump `schema_version` or `version` |
| Change field type | Bump + update validator |
| New required field | Bump + migration note in `DATA_ARCHITECTURE.md` §17 |

---

## 5. i18n object shape

All player-facing display strings use inline locale objects:

```json
{
  "display_name": {
    "en": "Sea Salve",
    "ja": "海の膏",
    "zh": "海之膏",
    "zh-Hant": "海之膏"
  }
}
```

| Rule | Detail |
|------|--------|
| Required locales | `en`, `ja`, `zh`, `zh-Hant` on ship strings |
| Keys | Exact locale tags above — not `EN` or `zh_TW` |
| VO | Separate `voice_id` on dialogue lines — not inside i18n text |
| CSV | UI chrome may mirror in `game/locale/translations.csv` — **JSON wins** for quest/item/lore names |

---

## 6. Story spine shapes

### 6.1 `story/scenes.json` row

```json
{
  "scene_id": "SC-09",
  "act": "II",
  "zone": "tidal_caves",
  "type": "boss",
  "sets_flags": ["shore_wraith_defeated"],
  "requires_flags": {},
  "dialogue": "SC-09"
}
```

- `scene_id` must be unique
- Every `sets_flags` entry must exist in `story/flags.json`
- `dialogue` key must exist in `dialogue/chapter_01.json` unless scene is intentionally silent

### 6.2 `story/flags.json` row

```json
{
  "id": "shore_wraith_defeated",
  "description": "Player defeated the shore wraith in SC-09",
  "set_by": "SC-09 encounter"
}
```

### 6.3 Dialogue line (excerpt)

```json
{
  "scene_id": "SC-03",
  "lines": [
    {
      "speaker": "yuzu",
      "text": { "en": "...", "ja": "...", "zh": "...", "zh-Hant": "..." },
      "voice_id": "sc03_yuzu_01"
    }
  ]
}
```

---

## 7. Registry & QA catalog shapes

### Code registries (`game/data/code/`)

| File | Purpose |
|------|---------|
| `base_classes.json` | Extend-only GDScript classes |
| `autoload_registry.json` | Singleton API contracts |
| `scene_registry.json` | Canonical `.tscn` paths + required nodes |
| `helpers_registry.json` | Core helpers + Python reference paths |
| `spec_registry.json` | Spec-first gate artifacts |

Each entry should include stable `id`, human `label` or `description`, and `paths` or `gdscript_path` where applicable.

### QA catalogs (`game/data/qa/`)

Required top-level fields:

```json
{
  "version": "1.0",
  "authority": "docs/qa/EXAMPLE.md",
  "description": "What this catalog gates"
}
```

Wire to CI: `acceptance_criteria.json` + `validate_*.py` + `run_docs_ci_checks.sh`.

---

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
2. Create `tools/validate_<name>.py` (PEP 8 — see [`PYTHON_STYLE.md`](PYTHON_STYLE.md))
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
- [ ] `bash tools/run_docs_ci_checks.sh` green
