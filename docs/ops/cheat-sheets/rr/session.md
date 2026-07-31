---
id: session
type: reference
phase: [0, 1]
audience: [pm, builder, qa]
status: active
authority: ops
tokens_est: 653
summary: "bash tools/ensure_mcp_stack.sh"
---
# R&R — session-startup-every-run

**Hub:** [`RR_CHEATSHEET.md`](../RR_CHEATSHEET.md)

## Session startup (every run)

```bash
bash tools/ensure_mcp_stack.sh
bash tools/check_mcp_ready.sh          # Builder, Flow, Debugger
bash tools/check_rr_compliance.sh      # All roles touching game/
```

**PM-only (`main` docs/issues):**
```bash
bash tools/run_pm_orchestrator.sh      # Sprint Master — required
bash tools/run_docs_ci_checks.sh       # includes L0_spec_refinement_scope
```

**Spec refinement (`main` — no implementation):**
```bash
# Allowed: docs/, game/data/, game/locale/, tools/*_lib.py
# Forbidden: game/scripts/, game/scenes/, project.godot
bash tools/check_spec_refinement_scope.sh
```

**Architect / Builder / QA (before sprint issue work):**
```bash
bash tools/run_agent_session_gate.sh <role> <issue_id>   # opens session telemetry automatically
```

**End every worker session (mandatory — enforced cycle close):**
```bash
bash tools/run_post_agent_cycle.sh --issue <id> --agent <role> --commit $(git rev-parse HEAD)
```

**QA with gate evidence:**
```bash
bash tools/run_post_agent_cycle.sh --issue <id> --agent qa --commit $(git rev-parse HEAD) \
  --gate <gate_id> --artifact <path>
```

**Factory watchdog (stall recovery):**
```bash
bash tools/run_factory_watchdog.sh              # health check
bash tools/run_factory_watchdog.sh --recover    # trigger PM via watchdog_recovery
```

**Stakeholder status (auto on cycle close; manual):**
```bash
bash tools/pm_emit_stakeholder_report.sh --trigger phase_exit --telegram
```

**Alignment audit (post-merge / phase exit):**
```bash
bash tools/run_alignment_audit.sh --trigger post_merge --note "PR #N"
# Management status: audit_radar_spec.png + audit_radar_build.png (auto-generated). Ignore mega dashboard.
```

**Long sessions — heartbeat (feeds telemetry + watchdog):**
```bash
bash tools/pm_record_heartbeat.sh --agent <role> --issue <id> --note "progress note"
```

**Factory Analyst — sprint efficiency rollup:**
```bash
python3 tools/analyze_agent_session_telemetry.py   # → artifacts/agent_session_reports/
```

**Zone tournament (L2.5 pre-merge — champion/challenger, non-ship):**
```bash
bash tools/run_candidate_tournament.sh --challenger artifacts/candidates/<issue>/challenger_runN.json
# Policy: docs/ops/qa/CANDIDATE_TOURNAMENT.md
```

**One-time:** `CURSOR_API_KEY` in Cursor Secrets for auto token logging — `docs/ops/agents/CURSOR_SECRETS_SETUP.md` §8

---

