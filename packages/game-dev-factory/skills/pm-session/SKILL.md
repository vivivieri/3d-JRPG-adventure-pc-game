---
name: pm-session
description: >-
  Run a PM / Sprint Master session for a multi-agent game-dev factory.
  Use when starting PM work, dispatching workers, or closing a sprint cycle.
  Engine-agnostic — do not put Godot/MCP boot steps in this skill.
---

# PM session

## Always

1. Read `packages/game-dev-factory/CONTROL_PLANE.md` (cut line).
2. Run: `bash tools/run_pm_orchestrator.sh`
3. On FAIL → fix blocking step; do **not** assign workers.
4. On PASS → assign from `artifacts/pm_dispatch_packet.json` / orchestrator report `next_dispatch`.

## Path seam

Defaults: `FACTORY_DATA_DIR=game/data/qa`, `FACTORY_ARTIFACTS_DIR=artifacts`.  
Override only when adopting this factory in another repo layout.

## After workers finish (same or next PM session)

```bash
bash tools/run_post_agent_cycle.sh --issue <id> --agent <role> --commit <sha> \
  --run-orchestrator
```

Optional: `--alignment-audit` when the host repo wires that plugin.

## Forbidden

- Honor-system “I remembered the checklist”
- Dispatching an agent not in `next_dispatch`
- Mixing game toolchain fixes into factory JSON schemas
