---
id: checklist-features
type: how-to
phase: [1, 6]
audience: [pm, architect]
status: active
authority: qa
tokens_est: 807
summary: "Add-feature checklist + registered features"
---
# Workflow Integration — Add-feature checklist + registered features

**Hub:** [`WORKFLOW_INTEGRATION.md`](../WORKFLOW_INTEGRATION.md)

## When to read

Use **Workflow Integration — Add-feature checklist + registered features** (roles: pm, architect) when executing this procedure Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [3. Checklist — adding a new factory feature](#3-checklist-adding-a-new-factory-feature)
- [Where agents see this rule](#where-agents-see-this-rule)
- [4. Registered features (current)](#4-registered-features-current)


## 3. Checklist — adding a new factory feature

Copy this when shipping anything that touches PM dispatch, secrets, or agent sessions:

1. **Authority doc** — create or extend (e.g. `docs/ops/qa/MY_FEATURE.md`)
2. **Registry entry** — add to `workflow_integration_registry.json`:
   - `script_hooks` — every script that must call your feature
   - `required_doc_refs` — **all** `standard_agent_surfaces` plus feature-specific docs
   - `required_secrets` — if any
   - `orchestrator_steps` — if PM orchestrator invokes it
   - `acceptance_gate` — if new L0 schema/gate
3. **Wire hooks** — implement in scripts (do not rely on docs alone)
4. **Register all agent surfaces** — `required_doc_refs` must include `AGENTS.md`, `.cursorrules`, RR + Controls cheatsheets, PM runbook, sprint orchestration, AI dev workflow, PR templates (not authority doc only)
5. **Update docs** — PM runbook, RR cheatsheet, lifecycle, `.cursorrules`, `AGENTS.md`
6. **Agent verify (before commit):** `bash tools/check_feature_integration.sh --remind`
7. **CI verify:** `bash tools/run_docs_ci_checks.sh` — `L0_workflow_integration` must PASS
8. **Alignment audit** — `bash tools/run_alignment_audit.sh --trigger post_merge`

### Where agents see this rule

| Surface | What reminds them |
|---------|-------------------|
| `.cursorrules` §0 | Forbidden without registry |
| `AGENTS.md` | Cloud agent mandatory section |
| `run_agent_session_gate.sh` | Printed every worker session start |
| `RR_CHEATSHEET.md` | Golden rule #8 + forbidden list |
| `PM_AGENT_RUNBOOK.md` §3b | PM rejects PRs without registry |
| `pm_orchestrator_steps.json` | `post_agent_steps.check_feature_integration` |
| `acceptance_criteria.json` | `invalid_pass_patterns` |
| `CANDIDATE_TOURNAMENT.md` | L2.5 champion/challenger when M5 tournament policy applies |
| `CONTROLS_CHEATSHEET.md` | Gate tables include `L0_candidate_tournament` / `L2_candidate_select` |

---


## 4. Registered features (current)

| ID | Label | Authority |
|----|-------|-----------|
| `post_agent_cycle` | Enforced post-agent cycle close | `docs/ops/agents/PM_AGENT_RUNBOOK.md` |
| `agent_session_telemetry` | Auto token/duration logging | `docs/ops/qa/AGENT_SESSION_TELEMETRY.md` |
| `factory_watchdog` | Stall/hang recovery | `docs/ops/agents/FACTORY_WATCHDOG.md` |
| `stakeholder_reporting` | PM status dashboard | `docs/ops/agents/PM_STAKEHOLDER_REPORTING.md` |
| `alignment_audit` | Stakeholder alignment audit | `docs/ops/qa/ALIGNMENT_AUDIT.md` |
| `candidate_tournament` | Champion/challenger golden harness (L2.5) | `docs/ops/qa/CANDIDATE_TOURNAMENT.md` |
| `game_dev_factory_pack` | Portable PM/lifecycle control plane | `packages/game-dev-factory/CONTROL_PLANE.md` |

Add new rows here when registering features.

---
