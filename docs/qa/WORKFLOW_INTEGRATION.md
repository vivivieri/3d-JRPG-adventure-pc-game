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

---

## 3. Checklist — adding a new factory feature

Copy this when shipping anything that touches PM dispatch, secrets, or agent sessions:

1. **Authority doc** — create or extend (e.g. `docs/qa/MY_FEATURE.md`)
2. **Registry entry** — add to `workflow_integration_registry.json`:
   - `script_hooks` — every script that must call your feature
   - `required_doc_refs` — every workflow doc that must mention it
   - `required_secrets` — if any
   - `orchestrator_steps` — if PM orchestrator invokes it
   - `acceptance_gate` — if new L0 schema/gate
3. **Wire hooks** — implement in scripts (do not rely on docs alone)
4. **Update docs** — PM runbook, RR cheatsheet, lifecycle, `.cursorrules`, `AGENTS.md`
5. **Validate** — `python3 tools/validate_workflow_integration.py` must PASS
6. **Alignment audit** — `bash tools/run_alignment_audit.sh --trigger post_merge`

---

## 4. Registered features (current)

| ID | Label | Authority |
|----|-------|-----------|
| `agent_session_telemetry` | Auto token/duration logging | `docs/qa/AGENT_SESSION_TELEMETRY.md` |

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
