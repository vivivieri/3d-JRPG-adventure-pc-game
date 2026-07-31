---
id: standards-format-naming
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, builder]
status: active
authority: engineering
tokens_est: 749
summary: "Standards, format, naming, schema metadata"
---
# JSON Data Style — Standards, format, naming, schema metadata

**Hub:** [`JSON_DATA_STYLE.md`](../JSON_DATA_STYLE.md)

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
