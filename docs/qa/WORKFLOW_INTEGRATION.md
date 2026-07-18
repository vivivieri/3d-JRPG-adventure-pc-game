# Workflow Integration Registry — Avoid Feature Drift

**Version:** 1.0  
**Authority:** `game/data/qa/workflow_integration_registry.json`  
**Gate:** `python3 tools/validate_workflow_integration.py` (`L0_workflow_integration`)  
**Cross-refs:** `docs/qa/ALIGNMENT_AUDIT.md`, `docs/qa/AGENT_SESSION_TELEMETRY.md`

---

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

## 3. Checklist — adding a new factory feature

Copy this when shipping anything that touches PM dispatch, secrets, or agent sessions:

1. **Authority doc** — create or extend (e.g. `docs/qa/MY_FEATURE.md`)
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
| `post_agent_cycle` | Enforced post-agent cycle close | `docs/agents/PM_AGENT_RUNBOOK.md` |
| `agent_session_telemetry` | Auto token/duration logging | `docs/qa/AGENT_SESSION_TELEMETRY.md` |
| `factory_watchdog` | Stall/hang recovery | `docs/agents/FACTORY_WATCHDOG.md` |
| `stakeholder_reporting` | PM status dashboard | `docs/agents/PM_STAKEHOLDER_REPORTING.md` |
| `alignment_audit` | Stakeholder alignment audit | `docs/qa/ALIGNMENT_AUDIT.md` |
| `candidate_tournament` | Champion/challenger golden harness (L2.5) | `docs/qa/CANDIDATE_TOURNAMENT.md` |

Add new rows here when registering features.

---

## 5. Alignment audit cooperation

`alignment_audit_catalog.json` → `pm_workflow` domain includes workflow integration health. On FAIL, recommendation **`REC_WORKFLOW_DRIFT`** points here.

PM should run alignment audit after any registry change:

```bash
bash tools/run_alignment_audit.sh --trigger post_merge --note "workflow integration update"
```

---

## 6. Related gates

| Gate | Role |
|------|------|
| `L0_doc_sync` | README index + runner gate list parity |
| `L0_workflow_integration` | Factory feature hook + doc parity |
| `L0_alignment_audit_catalog` | Stakeholder audit catalog valid |

**`L0_doc_sync`** catches missing README links. **`L0_workflow_integration`** catches missing factory wiring.
