# Game data — Tides of Urashima

**This folder on `main` holds design data only** — story JSON, QA catalogs, and i18n strings.

**Godot implementation** (project file, scripts, scenes, assets) lives on branch **`game/development`**.  
See `docs/ops/workflow/BRANCHING.md`.

## On `main` (this branch)

```
game/
  data/                 # Story, combat, quests, QA thresholds (source of truth)
  locale/
    translations.csv    # UI / skills / combat i18n keys
  scenes/
    README.md           # GDAI MCP scene policy (no .tscn on main)
```

## Validate data

```bash
python3 tools/validate_story_data.py
python3 tools/validate_acceptance_criteria.py
bash tools/run_docs_ci_checks.sh
```

## Game implementation

```bash
git checkout game/development
bash tools/install_cloud_dev.sh
bash tools/ensure_mcp_stack.sh
# Open game/project.godot in Godot 4.7
```

Build loop: `docs/ops/workflow/AI_DEV_WORKFLOW.md` · Phases: `docs/ops/workflow/IMPLEMENTATION_PLAN.md`

## Related docs

- `docs/ops/workflow/BRANCHING.md` — branch policy
- `docs/ops/cheat-sheets/RR_CHEATSHEET.md` · `docs/ops/cheat-sheets/CONTROLS_CHEATSHEET.md` — agent cheat sheets
- `docs/engineering/technical/DATA_ARCHITECTURE.md` — JSON schema
- `docs/engineering/technical/CODE_BASE_CLASS_RULES.md` — base classes + component scenes
- `docs/ops/workflow/IMPLEMENTATION_PLAN.md` — build phases
