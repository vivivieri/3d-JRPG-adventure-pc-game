---
name: worker-session
description: >-
  Run a non-PM factory worker session (architect, builder, qa, flow, release, visual).
  Use at session start for a dispatched sprint issue. Enforced gate + cycle close.
---

# Worker session

## Always

1. Confirm issue id + role from PM dispatch packet.
2. Run: `bash tools/run_agent_session_gate.sh <role> <issue_id>`
3. On FAIL → stop; ask PM to re-run orchestrator.
4. Do the work for that issue only (strict role — no wearing another hat).
5. Close with:

```bash
bash tools/run_post_agent_cycle.sh --issue <issue_id> --agent <role> \
  --commit "$(git rev-parse HEAD)"
```

QA with evidence: add `--gate <gate_id> --artifact <path>`.

## Docs pack

Session gate prints the budgeted docs pack. Read `must_read` paths; post-cycle
enforces adherence. Do not skip the pack.

## Game plugin (host repo)

Toolchain boot (editor, MCP, art generators) is **host-specific**. Follow the
host `AGENTS.md` / BOOT card **after** the session gate passes — not instead of it.

## Forbidden

- Starting work without session gate PASS
- Closing the issue by editing the board by hand
- Skipping `run_post_agent_cycle.sh`
