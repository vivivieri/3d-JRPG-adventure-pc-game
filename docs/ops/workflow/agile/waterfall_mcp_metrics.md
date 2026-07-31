---
id: waterfall-mcp-metrics
type: how-to
phase: [0, 1, 8]
audience: [pm, architect]
status: active
authority: workflow
tokens_est: 538
summary: "Waterfall bounds, MCP, metrics"
---
# Agile Within Phases — Waterfall bounds, MCP, metrics

**Hub:** [`AGILE_WITHIN_PHASES.md`](../AGILE_WITHIN_PHASES.md)

## 7. What stays waterfall (do not agile-ify)

| Decision | Authority |
|----------|-----------|
| Phase order 1→8 | `IMPLEMENTATION_PLAN.md` |
| Story scenes, flags, dialogue | `game/data/` |
| Art rebuild after gameplay | Phase 7 before Phase 8 |
| Merge to `main` | Once at M6 ship |
| Three endings scope | `ENDING_DESIGN.md` — not deferred |
| License / compliance | `ASSET_COMPLIANCE.md` |

Change these only via explicit doc + data PR to `main`, not via sprint backlog reprioritization.

---


## 8. Linear MCP — agent commands

After authenticating Linear in Cursor:

| Intent | Skill / action |
|--------|----------------|
| Create sprint tasks from phase | `spec-to-implementation` or `create-task` |
| Query open blockers | `database-query` / Linear search |
| Log retro notes | `knowledge-capture` (optional Notion) |

**PM Agent sprint start checklist:**

1. Read `game/data/qa/sprint_phases.json` → `active_phase`
2. Read `IMPLEMENTATION_PLAN.md` §Phase N task table
3. Create Linear cycle `Phase{N}-Sprint{K}`
4. Create issues (≤10) with gate IDs + agent labels
5. Mirror critical issues to GitHub for CI linkage

---


## 9. Metrics (optional, lightweight)

| Metric | Source | Use |
|--------|--------|-----|
| CI pass rate | GitHub Actions | Sprint health |
| Open S0/S1 count | GitHub labels | Block release |
| Gate failure rate | `env/qa` issues | Remediation focus |
| Cycle completion | Linear | Velocity trend (inform WIP, not deadlines) |

Do not use velocity to skip phase gates.

---


## 10. Cross-refs

- `docs/ops/agents/PROJECT_MANAGEMENT.md` — labels, GitHub setup
- `docs/ops/ci-cd/GITHUB_SETUP.md` — labels/milestones script
- `docs/ops/agents/MULTI_AGENT_TEAM.md` — role handoffs
- `docs/ops/ci-cd/ENVIRONMENTS.md` — dev → qa → uat promotion
- `game/data/qa/sprint_phases.json` — phase ↔ Linear ↔ gates catalog

---
