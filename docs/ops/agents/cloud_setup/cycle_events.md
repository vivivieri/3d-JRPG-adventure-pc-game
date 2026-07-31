---
id: cycle-events
type: how-to
audience: [pm, builder]
phase: [0, 1]
status: active
authority: agents
tokens_est: 404
---
# Cloud Agent Setup — End-of-cycle & events

**Hub:** [`CLOUD_AGENT_SETUP_RUNBOOK.md`](../CLOUD_AGENT_SETUP_RUNBOOK.md)

## 5. End-of-cycle contract (every worker agent)

Every **non-PM** agent session **must** end with:

```bash
# 1. Gates on PR commit
bash tools/run_ci_checks.sh          # or confirm CI green on PR

# 2–4. Enforced cycle close (board + event + evidence + registry check)
bash tools/run_post_agent_cycle.sh --issue P1-02 --agent builder --commit "$(git rev-parse HEAD)"
# QA with gate evidence: add --gate L2_scene_primitives --artifact artifacts/...
```

If step 3 is skipped, **the factory stalls** — there is no hourly PM to pick it up.

### PM after dispatching work

If PM only **assigns** another Cloud Agent (does not do the work itself), PM session ends with:

```bash
# Optional: confirm dispatch recorded
python3 tools/pm_update_issue.py P1-01 --status in_progress --agent architect
# Do NOT emit agent_cycle_complete — the worker emits when done
```

---


## 6. Event reference

| Event | When to emit | Command |
|-------|--------------|---------|
| `agent_cycle_complete` | Worker or PM finished one issue | `bash tools/run_post_agent_cycle.sh --issue … --agent … --commit …` |
| `sprint_cycle_complete` | Orchestrator `sprint_complete: true` | `pm_emit_cycle_event.sh sprint_cycle_complete --sprint … --next-sprint N` |
| `ci_cycle_complete` | Optional; CI workflow after merge | Automatic via `agent-cycle-pm.yml` if `.cycle_pending` marker exists |
| `uat_ready` | L5 PASS + RC tagged | `pm_emit_cycle_event.sh uat_ready --tag v0.1.0-rc1` |
| `mcp_blocked` | MCP stack down | `pm_emit_cycle_event.sh mcp_blocked --check check_mcp_ready.sh` |

Payload schema: `game/data/qa/agent_cycle_events.json`

---
