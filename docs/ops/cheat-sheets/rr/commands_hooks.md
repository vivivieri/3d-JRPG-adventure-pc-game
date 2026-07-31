---
id: commands-hooks
type: reference
phase: [0, 1]
audience: [pm, builder, qa]
status: active
authority: ops
tokens_est: 775
summary: "R&R Cheat Sheet — Commands, factory hooks, related — bash tools/run_ci_checks.sh              # game/development full CI"
---
# R&R Cheat Sheet — Commands, factory hooks, related

**Hub:** [`RR_CHEATSHEET.md`](../RR_CHEATSHEET.md)

## When to read

Use **R&R Cheat Sheet — Commands, factory hooks, related** (roles: pm, builder, qa) when you need this reference during the current task Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [Quick commands](#quick-commands)
- [Factory hooks (names for L0_workflow_integration)](#factory-hooks-names-for-l0_workflow_integration)
- [Related docs (full detail)](#related-docs-full-detail)


## Quick commands

```bash
bash tools/run_ci_checks.sh              # game/development full CI
bash tools/run_docs_ci_checks.sh         # main docs/data CI
bash tools/check_rr_compliance.sh        # L0 — Builder R&R
bash tools/check_l3_gdai_built.sh        # L3 — scene diff needs .gdai_built
bash tools/run_cd_gates.sh --channel rc  # pre-export
bash tools/check_asset_compliance.sh     # before commit with assets
bash tools/run_perf_review_checks.sh     # L2 — perf thresholds catalog
python3 tools/validate_story_data.py     # L0_story_data
```

---



## Factory hooks (names for L0_workflow_integration)

| Hook | Command / artifact |
|------|--------------------|
| Close session | `bash tools/run_post_agent_cycle.sh` |
| Watchdog | `bash tools/run_factory_watchdog.sh` |
| Factory setup | `FACTORY_SETUP_GUIDE` · `docs/ops/agents/FACTORY_SETUP_GUIDE.md` |
| Stakeholder | `bash tools/pm_emit_stakeholder_report.sh` |
| Alignment | `bash tools/run_alignment_audit.sh` · `audit_radar_spec.png` |
| Tournament | `bash tools/run_candidate_tournament.sh` |


## Related docs (full detail)

| Doc | Contents |
|-----|----------|
| `.cursorrules` §0–§1 | Hard rules, combined workflow |
| **`docs/engineering/technical/CODE_BASE_CLASS_RULES.md`** | **Extend-only code bases** + license-safe 3D sources |
| **`docs/ops/cheat-sheets/CONTROLS_CHEATSHEET.md`** | **Enforcement** — CI, PR templates, branch protection |
| `docs/ops/agents/MCP_STACK.md` | Full toolchain, install, troubleshooting |
| `docs/ops/agents/MULTI_AGENT_TEAM.md` | Handoffs, parallel patterns, definition of done |
| `docs/ops/workflow/AGILE_WITHIN_PHASES.md` | Sprint facilitator, AI-native cadence |
| **`docs/ops/agents/SPRINT_ORCHESTRATION.md`** | **Enforced dispatch** — no self-assign |
| **`docs/ops/agents/PM_AGENT_RUNBOOK.md`** | PM session steps, stale escalation |
| **`docs/ops/qa/AGENT_SESSION_TELEMETRY.md`** | **Auto token/duration logging** — factory integration §9 |
| `docs/ops/sprints/Phase1-Sprint1-issues.md` | Active sprint issue bodies |
| `docs/ops/qa/ACCEPTANCE_CRITERIA.md` | Gate thresholds |
| **`docs/ops/qa/PERFORMANCE_BASELINE.md`** | **Hardware + environment baseline for perf evidence** |
| **`docs/ops/qa/AI_TESTING_SPEC.md`** | **L0–L6 test layers, screenshots, E2E video** |
| **`docs/design/art/VISUAL_QA.md`** | **Screenshot + vision jury procedure** |
| `docs/ops/ci-cd/CI.md` | GitHub Actions gate matrix |
| `docs/ops/ci-cd/GITHUB_SETUP.md` | PAT + `setup_github_project.sh` |
| `docs/ops/workflow/AI_DEV_WORKFLOW.md` | Extended command reference |
