---
id: startup-done
type: explanation
phase: [0, 1]
audience: [pm, builder, qa]
status: active
authority: ops
tokens_est: 659
summary: "Cloud startup, subagents, DoD, refs"
---
# Multi-Agent Team — Cloud startup, subagents, DoD, refs

**Hub:** [`MULTI_AGENT_TEAM.md`](../MULTI_AGENT_TEAM.md)

## 7. Cloud agent startup (every role)

```bash
bash tools/ensure_mcp_stack.sh
bash tools/check_mcp_ready.sh          # Builder, Flow, Debugger
bash tools/check_rr_compliance.sh      # All roles touching game/
```

**PM / Sprint Master session (mandatory first):**
```bash
bash tools/run_pm_orchestrator.sh      # FAIL = do not dispatch agents
```

**Other agents (before any work on a sprint issue):**
```bash
bash tools/run_agent_session_gate.sh <agent_role> <issue_id>
```

**End every worker session (mandatory — enforced cycle close):**
```bash
bash tools/run_post_agent_cycle.sh --issue <id> --agent <role> --commit $(git rev-parse HEAD)
```

**Cross-cutting factory features (before merge):**
```bash
bash tools/check_feature_integration.sh --remind   # docs/ops/qa/WORKFLOW_INTEGRATION.md
```

**PM-only session** (docs/issues on `main`):
```bash
bash tools/run_docs_ci_checks.sh
```

---


## 8. Subagent invocation (Cursor)

| Task | Subagent type | Model hint |
|------|---------------|------------|
| Codebase search | `explore` | — |
| PR / diff review | `bugbot` | readonly |
| Security on export/CD | `security-review` | readonly |
| Broad zone implementation | `generalPurpose` | with full handoff doc |

Resume agents only for **same role continuation** (e.g. Builder session 2 on same scene).

---


## 9. Definition of done (per issue)

- [ ] Acceptance gate IDs listed in issue and **all PASS**
- [ ] Evidence paths in issue or PR
- [ ] No `WARN` or `SKIP` counted as pass for milestone gates
- [ ] Issue labels updated: `status/done`, env label retained for audit
- [ ] PR merged to correct branch (`main` = docs only; `game/development` = code)
- [ ] Worker ran `bash tools/run_post_agent_cycle.sh` (no factory stall)
- [ ] Cross-cutting factory changes registered in `workflow_integration_registry.json` when applicable

---


## 10. Cross-refs

- `docs/ops/cheat-sheets/RR_CHEATSHEET.md` — **printable one-page R&R summary**
- `docs/ops/cheat-sheets/CONTROLS_CHEATSHEET.md` — **printable controls / enforcement summary**
- `docs/ops/agents/PROJECT_MANAGEMENT.md` — GitHub Issues + MCP
- `docs/ops/workflow/AGILE_WITHIN_PHASES.md` — sprint cadence inside each phase
- `docs/ops/ci-cd/ENVIRONMENTS.md` — dev/qa/uat/preprod/prod
- `docs/ops/qa/QA_REMEDIATION_LOOP.md` — fix iteration rules
- `AGENTS.md` — cloud bootstrap
