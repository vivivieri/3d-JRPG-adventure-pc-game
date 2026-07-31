---
id: checklist-helpers
type: how-to
audience: [architect, builder]
phase: [1, 2]
status: active
authority: engineering
tokens_est: 588
summary: "Checklist, recover, new helpers, ref map"
---
# GDScript Regen — Checklist & Phase 1 — Checklist, recover, new helpers, ref map

**Hub:** [`checklist_recover.md`](../checklist_recover.md)

## When to read

Use **GDScript Regen — Checklist & Phase 1 — Checklist, recover, new helpers, ref map** (roles: architect, builder) when executing this procedure Jump to a section below instead of reading end-to-end (4 sections).

## Jump to

- [6. One-command checklist](#6-one-command-checklist)
- [7. Recovering the previous GDScript ports](#7-recovering-the-previous-gdscript-ports)
- [8. Adding a new helper](#8-adding-a-new-helper)
- [9. Reference map](#9-reference-map)


## 6. One-command checklist

```bash
bash tools/regenerate_core_helpers.sh          # print checklist + run reference tests
bash tools/regenerate_core_helpers.sh --check  # registry validation only
bash tools/regenerate_core_helpers.sh --test   # reference lib tests only
```

---



## 7. Recovering the previous GDScript ports

If you need the exact earlier ports (before spec-first cleanup):

```bash
git show 544dca9^:game/scripts/core/difficulty_service.gd
git show 544dca9^:game/scripts/core/save_integrity.gd
git show 544dca9^:game/scripts/core/settings_store.gd
git show 544dca9^:game/scripts/core/achievement_evaluator.gd
git show 544dca9^:game/scripts/core/event_bus.gd
```

Use these as **diff hints** only — registry + Python reference win on conflicts.

---



## 8. Adding a new helper

1. Add Python reference under `tools/` + tests in `tools/test_reference_libs.py`
2. Add entry to `helpers_registry.json` with full `public_api`
3. Append to `regeneration_order`
4. PR to **`main`** first
5. Port to GDScript on **`game/development`**

---



## 9. Reference map

| GDScript (`game/development`) | Python (`main`) | Data |
|--------------------------------|-----------------|------|
| `event_bus.gd` | — | `helpers_registry.json` signals |
| `settings_store.gd` | `tools/settings_store_lib.py` | `settings_defaults.json` |
| `save_integrity.gd` | `tools/save_integrity_lib.py` | `qa/save_integrity.json` |
| `difficulty_service.gd` | `tools/difficulty_lib.py` | `combat/difficulty.json` |
| `achievement_evaluator.gd` | `tools/achievement_evaluator_lib.py` | `achievements/achievements.json` |
| `zone_visuals.gd` | `tools/zone_visuals_lib.py` | `world/zone_palettes.json`, `code/environment_registry.json` |

---
