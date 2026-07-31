---
id: planning-close
type: how-to
audience: [pm]
status: active
authority: ops
tokens_est: 498
summary: "1. Read `docs/ops/workflow/IMPLEMENTATION_PLAN.md` §Phase N + `sprint_phases.json` exit gates."
---
# PM Runbook — Planning & Watchdog — Planning + close

**Hub:** [`planning_watchdog.md`](../planning_watchdog.md)

## When to read

Use **PM Runbook — Planning & Watchdog — Planning + close** (roles: pm) when executing this procedure Jump to a section below instead of reading end-to-end (5 sections).

## Jump to

- [5. Sprint planning — create / sync issues](#5-sprint-planning-create-sync-issues)
- [New sprint batch](#new-sprint-batch)
- [Missing issue detection](#missing-issue-detection)
- [Carry-over from previous sprint](#carry-over-from-previous-sprint)
- [6. Sprint close checklist](#6-sprint-close-checklist)


## 5. Sprint planning — create / sync issues

### New sprint batch

1. Read `docs/ops/workflow/IMPLEMENTATION_PLAN.md` §Phase N + `sprint_phases.json` exit gates.
2. Write `docs/ops/sprints/Phase{N}-Sprint{K}-issues.md` (copy Phase1 template).
3. Add all issues to `game/data/qa/sprint_board.json`:
   - `id`, `sequence`, `depends_on`, `agent_owner`, `acceptance_gate_ids`, `implementation_plan_tasks`
4. Set `active_sprint.id` = `Phase{N}-Sprint{K}`.
5. Run `bash tools/run_pm_orchestrator.sh` — must PASS before filing GitHub issues.
6. File GitHub issues from pack; set `github_issue` on board rows.

### Missing issue detection

`pm_sync_sprint_pack.py` compares pack markdown `## P1-XX` headers to board — **FAIL** if mismatch.

### Carry-over from previous sprint

```bash
python3 tools/pm_close_sprint.py --next-sprint-number 2 --dry-run   # preview
python3 tools/pm_close_sprint.py --next-sprint-number 2
```

Then update issue pack + board rows; clear `carry_over_queue`; re-run orchestrator.

---



## 6. Sprint close checklist

- [ ] All board issues `status: done` OR explicitly `carry_over` with next sprint filed
- [ ] `bash tools/run_pm_orchestrator.sh` → `sprint_complete: true`
- [ ] QA gate report archived in P1-06 / sprint review issue
- [ ] `carry_over_queue` empty
- [ ] Optional: `git tag v0.1.0-rc1` per `sprint_phases.json` uat_tag_pattern

---
