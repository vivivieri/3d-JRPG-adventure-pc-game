---
id: problem-register
type: how-to
phase: [1, 6]
audience: [pm, architect]
status: active
authority: qa
tokens_est: 695
summary: "Problem + register-before-merge"
---
# Workflow Integration — Problem + register-before-merge

**Hub:** [`WORKFLOW_INTEGRATION.md`](../WORKFLOW_INTEGRATION.md)

## 1. Problem

New factory features (telemetry, watchdog hooks, secrets, orchestrator steps) often land in **one script** but not in:

- PM runbook / sprint orchestration docs
- RR cheatsheet / `.cursorrules` / `AGENTS.md`
- Cycle event side effects
- Day-one secrets checklist

This causes **silent drift** — agents follow outdated workflows until someone notices manually.

---


## 2. Solution: register before merge

Every cross-cutting factory feature **must** be listed in:

```
game/data/qa/workflow_integration_registry.json
```

CI gate **`L0_workflow_integration`** verifies:

| Check | What fails |
|-------|------------|
| Standard agent surfaces | Feature missing any doc in `standard_agent_surfaces` |
| Script hooks | Required `contains` strings missing from wired tools |
| Doc cross-refs | Authority docs must mention key terms |
| Secrets | `required_secrets` present in `check_day_one_secrets.sh` |
| Orchestrator steps | Step id + command wired in `pm_orchestrator_steps.json` |
| Cycle events | `telemetry_side_effects` (or equivalent) in `agent_cycle_events.json` |
| Acceptance gate | Gate id in catalog + docs CI runner |

```bash
python3 tools/validate_workflow_integration.py
bash tools/run_docs_ci_checks.sh   # includes L0_workflow_integration
```

### Why gaps can still appear (read this)

Two gates sound similar but enforce **different** things:

| Gate | What it checks | What it does **not** check |
|------|----------------|----------------------------|
| **`L0_doc_sync`** | Every indexed doc is in `docs/README.md`; runner gate ids match `acceptance_criteria.json` | That agent runbooks mention your new feature |
| **`L0_workflow_integration`** | Only docs listed in **`required_doc_refs`** for each registry feature | Docs you forgot to add to `required_doc_refs` |

So a new feature can pass **36/36 docs CI** with only 3 doc refs registered — while `AGENTS.md`, `.cursorrules`, and PM runbook stay silent until someone expands the registry.

**Structural fix (v1.2):** `workflow_integration_registry.json` → `standard_agent_surfaces` lists the 8 docs every feature must include in `required_doc_refs`. The validator fails if any surface is missing — you cannot register a minimal 3-doc entry and pass CI.

**Rule:** When adding a factory feature, copy the **full agent surface list** from §3 checklist (not just the authority doc). Same lesson as `post_agent_cycle` and `agent_session_telemetry` — minimal registry entries cause silent drift.

---
