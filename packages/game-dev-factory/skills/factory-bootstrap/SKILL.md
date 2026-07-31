---
name: factory-bootstrap
description: >-
  Install the portable game-dev factory control plane into a new or existing
  game repo. Use when extracting PM lifecycle or adopting packages/game-dev-factory.
---

# Factory bootstrap

## Goal

Host repo can run: orchestrate → gate → work → enforced cycle close, with its own
board JSON and toolchain plugin.

## Steps

1. Copy or submodule `packages/game-dev-factory/`.
2. Copy `python/factory_paths.py` + `python/factory_env.sh` into host `tools/`
   (or keep import path pointed at the package).
3. Instantiate templates from `templates/` into `FACTORY_DATA_DIR`
   (default `game/data/qa/`):
   - `sprint_board.template.json`
   - `sprint_phases.template.json`
   - `pm_orchestrator_steps.template.json`
   - `workflow_integration_registry.template.json`
   - `factory_watchdog.template.json`
4. Replace placeholders: `{{PROJECT}}`, `{{IMPL_BRANCH}}`, `{{PHASE_1_NAME}}`,
   `{{PROJECT_FACTORY_DOCS}}`.
5. Point orchestrator `toolchain_preflight` step at the host engine boot command
   (or leave non-blocking `true` until ready).
6. Wire Cursor skills: copy `skills/*/SKILL.md` into the team skills path, or
   document load-from-repo.
7. Prove:

```bash
python3 tools/factory_paths.py
python3 tools/validate_sprint_board.py --strict
python3 tools/validate_sprint_phases.py
bash tools/run_pm_orchestrator.sh   # once steps exist
```

## Do not copy from a donor game

- Live sprint issues / GitHub numbers
- Engine MCP secrets or plugin zips
- Acceptance catalog content / alignment radar art
- Brand-specific `.cursorrules` NPR rules

## Cut line reminder

Control plane ≠ game plugin. See `CONTROL_PLANE.md`.
