---
id: rr-cheatsheet
type: reference
audience: [pm, builder, qa]
status: active
authority: ops
tokens_est: 458
summary: "Roles & responsibilities — load the pack for your session step"
---
# R&R Cheat Sheet

**Hub** — load only the pack for your current pass.

| Pack | Topic |
|------|-------|
| [`session.md`](rr/session.md) | Session startup |
| [`pick_work.md`](rr/pick_work.md) | How to pick work |
| [`performance_review.md`](rr/performance_review.md) | Performance review |
| [`qa_gates.md`](rr/qa_gates.md) | QA gate layers |
| [`golden_rules.md`](rr/golden_rules.md) | Golden rules |
| [`tools_roster.md`](rr/tools_roster.md) | Controls, tools, agent roster |
| [`workflow_handoff.md`](rr/workflow_handoff.md) | Workflow, situation→tool, handoffs |
| [`escalation_branch.md`](rr/escalation_branch.md) | Escalation, branch, sprint, forbidden |
| [`commands_hooks.md`](rr/commands_hooks.md) | Commands, factory hooks, related |
**Version:** 1.5
**Print this:** One-page reference for every agent session
**Companion:** `docs/ops/cheat-sheets/CONTROLS_CHEATSHEET.md` — how each role is **enforced** (CI, PR, branch protection)
**Authority:** `.cursorrules` §0–§1 · `docs/ops/agents/MCP_STACK.md` · `docs/ops/agents/MULTI_AGENT_TEAM.md` · `docs/ops/workflow/AGILE_WITHIN_PHASES.md` §11

---

## Factory hooks (names for L0_workflow_integration)

- `bash tools/run_post_agent_cycle.sh` — end every worker session
- `bash tools/run_factory_watchdog.sh` — stall recovery
- `docs/ops/agents/FACTORY_SETUP_GUIDE.md` — factory automations catalog
- `bash tools/pm_emit_stakeholder_report.sh` — stakeholder status
- `bash tools/run_alignment_audit.sh` — post-merge alignment; visuals `audit_radar_spec.png` + `audit_radar_build.png`
- `bash tools/run_candidate_tournament.sh` — optional L2.5 champion/challenger (`L2_candidate_select`)
