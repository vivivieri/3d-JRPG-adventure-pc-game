---
id: close-loop-features
type: how-to
phase: [0, 1]
audience: [pm]
status: active
authority: ops
tokens_est: 778
summary: "Close loop, factory features, stale agents"
---
# PM Agent Runbook — Close loop, factory features, stale agents

**Hub:** [`PM_AGENT_RUNBOOK.md`](../PM_AGENT_RUNBOOK.md)

## When to read

Use **PM Agent Runbook — Close loop, factory features, stale agents** (roles: pm) when executing this procedure Jump to a section below instead of reading end-to-end (4 sections).

## Jump to

- [3. After agent completes — close the loop](#3-after-agent-completes-close-the-loop)
- [3b. Cross-cutting factory features (all agents)](#3b-cross-cutting-factory-features-all-agents)
- [L2.5 candidate tournament (when policy applies)](#l25-candidate-tournament-when-policy-applies)
- [4. When an agent is stale or unresponsive](#4-when-an-agent-is-stale-or-unresponsive)


## 3. After agent completes — close the loop

Agent must deliver: commit SHA, PR URL, gate evidence paths.

```bash
bash tools/run_post_agent_cycle.sh --issue P1-01 --agent architect --commit abc1234
```

QA with gate evidence:

```bash
bash tools/run_post_agent_cycle.sh --issue P1-04 --agent qa --commit abc1234 \
  --gate L2_scene_primitives --artifact artifacts/...
```

This **immediately triggers** the PM Automation webhook (no cron). `run_post_agent_cycle.sh` runs, in order:

1. Factory halt guard (`check_factory_halt.sh`)
2. Done criteria check (`pm_check_done_criteria.py`)
3. Board update (`pm_update_issue.py --status done`)
4. Cycle event (`pm_emit_cycle_event.sh`) — closes telemetry, stakeholder report, PM webhook
5. Evidence bundle (`pm_bundle_evidence.py`) — auto-links `session_*.json` rollup
6. Workflow registry check (`check_feature_integration.sh`)

Do **not** call `pm_emit_cycle_event.sh` directly for normal worker close — use `run_post_agent_cycle.sh`. Do **not** call cycle events when PM only assigns work to another agent.

---


## 3b. Cross-cutting factory features (all agents)

When **any** agent adds or changes PM hooks, telemetry, secrets, cycle events, orchestrator steps, or watchdog behavior:

```bash
# Read checklist
cat docs/ops/qa/WORKFLOW_INTEGRATION.md

# Register + verify before merge
bash tools/check_feature_integration.sh --remind
bash tools/run_docs_ci_checks.sh   # L0_workflow_integration must PASS
```

PM **rejects** PRs that touch factory workflow without registry update.

### L2.5 candidate tournament (when policy applies)

For M5 art / zone vertical slices with tournament policy (`docs/ops/qa/CANDIDATE_TOURNAMENT.md`):

- Builder runs `bash tools/run_candidate_tournament.sh` before PR merge
- PR must include `L2_candidate_select` comparison artifact (`artifacts/candidates/<issue>/comparison_*.json`)
- PM rejects PRs that promote a challenger without comparison evidence when tournament is required

---


## 4. When an agent is stale or unresponsive

Orchestrator FAIL on `stale_issues` or blocked deps.

```bash
bash tools/pm_emit_escalation.sh P1-02 remind    # post comment to GitHub issue
bash tools/pm_emit_escalation.sh P1-02 S1        # stronger escalation body
python3 tools/pm_update_issue.py P1-02 --escalation 2 --note "No commit 24h"
```

Re-dispatch same agent or reassign per R&R — do not mark `done` without gates.

---
