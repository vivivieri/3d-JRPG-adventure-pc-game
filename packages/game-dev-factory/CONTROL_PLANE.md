# Game Dev Factory — Control Plane

**Version:** 1.0 · **MVP cut line**

This package extracts the **PM + multi-agent development lifecycle** as a reusable
control plane for stylized / indie game projects (Godot or otherwise).

## Cut line (freeze)

| Factory control plane (extract) | Game plugin (stay in each repo) |
|---------------------------------|----------------------------------|
| Orchestrate → gate session → work → enforced cycle close | Engine/MCP boot (`ensure_mcp_stack`, RR, editors) |
| Board / phases / steps **schemas** + empty templates | Real sprint issues, gate IDs, story/art acceptance |
| Role session skills (PM / worker / bootstrap) | Role→toolchain maps (e.g. Builder→GDAI) |
| Path seam: `FACTORY_DATA_DIR` / `FACTORY_ARTIFACTS_DIR` | Alignment domains, radar art, art/audio juries |
| Watchdog + webhook helpers (adapters) | Full acceptance catalog content |

## Session FSM

```
PM:     run_pm_orchestrator
Worker: run_agent_session_gate → work → run_post_agent_cycle
Exception: run_factory_watchdog (stall/hang only)
```

Honor-system closes are forbidden — cycle close is a script, not a checklist.

## Path seam

| Env | Default (this repo) | Purpose |
|-----|---------------------|---------|
| `FACTORY_ROOT` | repo root | Override when tooling lives outside cwd |
| `FACTORY_DATA_DIR` | `game/data/qa` | Committed JSON (board, phases, steps, registry) |
| `FACTORY_ARTIFACTS_DIR` | `artifacts` | Ephemeral reports, halt state, cycle log |

Live implementation: `tools/factory_paths.py` + `tools/factory_env.sh`  
Pack mirror: `python/factory_paths.py` + `python/factory_env.sh` (must stay in sync)

## What NOT to extract (yet)

- Engine MCP stacks / scene mutation rules
- Full `acceptance_criteria.json` content
- Alignment audit visuals / product scoring domains
- Live sprint board issues from a specific game
- Monolithic project `.cursorrules`

## Adopt in a new game

1. Copy `packages/game-dev-factory/` (or submodule / Cursor skills).
2. Copy template JSON into your `FACTORY_DATA_DIR`.
3. Wire `factory_paths.py` into your PM scripts (or vendor the MVP scripts).
4. Fill board/phases with **your** issues and gate ids.
5. Keep engine boot as a **plugin step** in orchestrator steps — not inside skills.

## Tides of Urashima status

First consumer. Defaults keep `game/data/qa` + `artifacts` so existing CI does not break.
