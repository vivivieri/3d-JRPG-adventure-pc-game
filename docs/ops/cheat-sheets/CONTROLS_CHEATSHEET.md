---
id: controls-cheatsheet
type: reference
phase: [0, 1]
audience: [pm, builder, qa, release]
status: active
authority: ops
tokens_est: 416
summary: "How roles are enforced — load gates or PR controls for your branch"
---
# Controls Cheat Sheet

**Hub** — load only the pack for your current pass.

| Pack | Topic |
|------|-------|
| [`golden_stack.md`](controls/golden_stack.md) | Golden rules + control stack |
| [`gates_by_branch.md`](controls/gates_by_branch.md) | Automated gates by branch |
| [`roles_l3.md`](controls/roles_l3.md) | Per-role controls + L3 split |
| [`pr_session_ship.md`](controls/pr_session_ship.md) | PR, session, ship/CD |
| [`remediation_done.md`](controls/remediation_done.md) | Remediation, DoD, verify, related |
**Version:** 1.5
**Print this:** One-page reference for automated + process controls
**Companion:** `docs/ops/cheat-sheets/RR_CHEATSHEET.md` v1.1 (who does what — includes per-role **control hook** column)
**Authority:** `docs/ops/ci-cd/CI.md` · `game/data/qa/acceptance_criteria.json` · `docs/ops/agents/PROJECT_MANAGEMENT.md`

---

## Factory control anchors (L0_workflow_integration)

| Gate / control | Command / id |
|----------------|--------------|
| Session cycle | `run_post_agent_cycle.sh` · `L0_agent_session_telemetry` |
| Watchdog | `run_factory_watchdog.sh` · `L0_factory_watchdog` |
| Automations | `FACTORY_SETUP_GUIDE` · `L0_factory_automations` |
| Stakeholder | `pm_emit_stakeholder_report.sh` · `L0_stakeholder_report` |
| Alignment | `run_alignment_audit.sh` · `L0_alignment_audit_catalog` · `audit_radar_spec.png` |
| Candidate tournament | `run_candidate_tournament.sh` · `L2_candidate_select` |
| Portable factory pack | `game-dev-factory` · `FACTORY_DATA_DIR` · `L0_game_dev_factory_pack` |
