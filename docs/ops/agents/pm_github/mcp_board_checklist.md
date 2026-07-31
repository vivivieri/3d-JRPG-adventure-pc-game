---
id: mcp-board-checklist
type: how-to
phase: [0, 1]
audience: [pm]
status: active
authority: ops
tokens_est: 700
summary: "Optional MCP, board, PM checklist, refs"
---
# Project Management — Optional MCP, board, PM checklist, refs

**Hub:** [`PROJECT_MANAGEMENT.md`](../PROJECT_MANAGEMENT.md)

## 6. Optional MCP integrations

### Linear (P1 — sprint board)

**When:** Multiple parallel agents executing the **current implementation phase**.

**Model:** Phase-gated Agile — waterfall phases 0–8, 2-week cycles **inside** each phase. See `docs/ops/workflow/AGILE_WITHIN_PHASES.md`.

| Action | Linear MCP |
|--------|------------|
| Create tasks from phase | `spec-to-implementation` or `create-task` skill |
| Query open blockers | `database-query` |
| Active phase + gates | Read `game/data/qa/sprint_phases.json` |

**Setup:** Team `Tides of Urashima` · Projects `M1-core`, `M5-art`, `M6-steam` · Cycles named `Phase{N}-Sprint{K}`.

Do not duplicate `game/data/` into Linear — link to repo paths in issue descriptions.

### Notion (P2 — narrative / planning notes)

**When:** External stakeholders need non-git visibility.

| Action | Notion MCP |
|--------|------------|
| Playtest summary | `knowledge-capture` skill |
| Phase plan | `spec-to-implementation` skill |

**Not for:** Runtime stats, scene IDs, or gate thresholds — keep in repo.

### GitHub (P0 — no extra MCP)

Agents use `ManagePullRequest` + Issues via cloud task tools. Labels and templates provide structure.

---


## 7. GitHub Projects board (recommended columns)

| Column | WIP limit | Entry criteria |
|--------|-----------|----------------|
| Backlog | — | Issue created |
| Ready | 10 | Spec + gate IDs defined |
| In Progress | 3 | Agent assigned (`status/in-progress`) |
| QA | 5 | PR open, CI running |
| UAT | 2 | RC tagged |
| Done | — | Gates PASS + issue closed |

---


## 8. PM Agent checklist (start of sprint)

**Mandatory — enforced by orchestrator (not honor system):**

```bash
bash tools/run_pm_orchestrator.sh
```

See `docs/ops/agents/PM_AGENT_RUNBOOK.md` for full step list.

- [ ] `validate_sprint_board.py --strict` PASS (`L0_sprint_board`)
- [ ] `pm_sync_sprint_pack.py` PASS — pack ↔ board aligned
- [ ] `next_dispatch` assigned to one agent; session gate run
- [ ] After agent session: `pm_update_issue.py` + re-run orchestrator
- [ ] Sync `docs/ops/workflow/MILESTONES.md` with open issues
- [ ] No open `severity/S0` on `env/uat` or `env/preprod`
- [ ] RC tag planned with gate list
- [ ] Human UAT scheduled only if L5 PASS on RC commit

---


## 9. Cross-refs

- `docs/ops/qa/QA_AND_BUG_PROCESS.md` §3 — bug body template
- `docs/ops/agents/MULTI_AGENT_TEAM.md` — role handoffs
- `docs/ops/ci-cd/ENVIRONMENTS.md` — promotion rules
- `tools/qa_emit_remediation.sh` — structured failure briefs
