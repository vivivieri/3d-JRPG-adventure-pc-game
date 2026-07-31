---
id: i18n-story-registry
type: reference
phase: [1, 2, 3, 4, 5, 6]
audience: [architect, builder]
status: active
authority: engineering
tokens_est: 757
summary: "JSON Data Style — i18n objects, story spine, registries — All player-facing display strings use inline locale objects:"
---
# JSON Data Style — i18n objects, story spine, registries

**Hub:** [`JSON_DATA_STYLE.md`](../JSON_DATA_STYLE.md)

## When to read

Use **JSON Data Style — i18n objects, story spine, registries** (roles: architect, builder) when you need this reference during the current task Jump to a section below instead of reading end-to-end (8 sections).

## Jump to

- [5. i18n object shape](#5-i18n-object-shape)
- [6. Story spine shapes](#6-story-spine-shapes)
- [6.1 `story/scenes.json` row](#61-storyscenesjson-row)
- [6.2 `story/flags.json` row](#62-storyflagsjson-row)
- [6.3 Dialogue line (excerpt)](#63-dialogue-line-excerpt)
- [7. Registry & QA catalog shapes](#7-registry-qa-catalog-shapes)
- [Code registries (`game/data/code/`)](#code-registries-gamedatacode)
- [QA catalogs (`game/data/qa/`)](#qa-catalogs-gamedataqa)


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
  "authority": "docs/ops/qa/EXAMPLE.md",
  "description": "What this catalog gates"
}
```

Wire to CI: `acceptance_criteria.json` + `validate_*.py` + `run_docs_ci_checks.sh`.

---
