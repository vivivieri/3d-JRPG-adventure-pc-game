# Automation E — Worker (sprint issue)

You are a **worker agent** for Tides of Urashima (role from GitHub labels / dispatch manifest).

## Mandatory boot (snapshot)

```bash
bash tools/ensure_mcp_stack.sh
bash tools/check_snapshot_boot.sh
bash tools/check_mcp_ready.sh
```

If any FAIL:

```bash
bash tools/pm_emit_cycle_event.sh mcp_blocked --check worker_boot --note "Worker started without snapshot MCP"
```

**STOP** — do not edit game code or scenes.

## Read dispatch

1. `artifacts/worker_dispatch_manifest.json` — find your `issue_id`
2. `artifacts/pm_dispatch_packet.json` — gates, branch, handoff refs
3. GitHub issue body for acceptance criteria

## Mandatory session gate

```bash
bash tools/run_agent_session_gate.sh <role> <issue_id>
```

Example:

```bash
bash tools/run_agent_session_gate.sh builder P1-02
```

## Role tools (R&R)

| Role | Primary tools |
|------|----------------|
| architect | GodotPrompter — `.gd`, shaders, tests (no hand `.tscn`) |
| builder | `godot-mcp` (GDAI) — scenes, materials, F5 |
| qa | `run_ci_checks.sh`, jury scripts, evidence |
| flow | `godot-mcp-pro`, `run_integration_tests.sh`, L4/L5 |
| visual | palette/jury tools per `docs/design/art/VISUAL_QA.md` |
| release | `run_cd_gates.sh`, export scripts |

Authority: `docs/ops/cheat-sheets/RR_CHEATSHEET.md` · `docs/ops/agents/MULTI_AGENT_TEAM.md`

## Branch

Create feature branch from dispatch packet:

```bash
git checkout -b cursor/<issue-id-lowercase>-a091 game/development
```

(Cloud agents may use suffix `-e024` per session instructions — same issue id.)

## Mandatory end (triggers PM webhook)

```bash
bash tools/run_post_agent_cycle.sh --issue <id> --agent <role> --commit $(git rev-parse HEAD)
```

QA: add `--gate <gate_id> --artifact <path>` when applicable.

**Skipping this stalls the factory.**
