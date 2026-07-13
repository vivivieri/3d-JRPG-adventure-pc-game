# PM Agent Runbook — Mandatory Sprint Master Workflow

**Version:** 1.0  
**Role:** PM Agent / Sprint Master (same role — `sprint_phases.json` → `sprint_master.role = "pm"`)  
**Rule:** Execute **every step below in order**. Skip = orchestrator FAIL = project blocked.  
**Authority:** `docs/SPRINT_ORCHESTRATION.md`

---

## 0. You are the Sprint Master

You **create** sprint items, **dispatch** other agents in sequence, **verify** gates, **escalate** delays, and **carry forward** incomplete work. You do **not** write `.gd`, `.tscn`, or shaders.

---

## 1. Every PM session — run orchestrator first

```bash
bash tools/run_pm_orchestrator.sh
```

This runs all steps in `game/data/qa/pm_orchestrator_steps.json`:

| Step | What it enforces |
|------|------------------|
| 1 | `validate_sprint_phases.py` — active phase valid |
| 2 | `validate_sprint_board.py --strict` — board schema + pack alignment |
| 3 | `pm_sync_sprint_pack.py` — no missing IDs; carry_over_queue empty |
| 4 | `run_docs_ci_checks.sh` — docs/data baseline green |
| 5 | `pm_orchestrator_lib.py --dispatch` — next agent + stale/WIP checks |

**If exit ≠ 0:** STOP. Fix failures. Do not assign agents.

**On PASS:** read `artifacts/pm_orchestrator_report.json` → `next_dispatch`.

---

## 2. Dispatch the next agent

From orchestrator output:

```bash
# Example — use actual issue_id and agent from next_dispatch[0]
bash tools/run_agent_session_gate.sh architect P1-01
```

Tell the assigned agent (new Cursor session):

- Issue ID + link to `docs/sprints/Phase1-Sprint1-issues.md` section
- Acceptance gate IDs (from board)
- Handoff section (Architect → Builder when applicable)
- **They must pass session gate before coding**

Set GitHub issue: `status/in-progress`, `agent/<role>`.

Optional board update before dispatch:

```bash
python3 tools/pm_update_issue.py P1-01 --status in_progress --agent architect
```

---

## 3. After agent completes — close the loop

Agent must deliver: commit SHA, PR URL, gate evidence paths.

```bash
python3 tools/pm_update_issue.py P1-01 --status done --commit abc1234 --github-issue 42
bash tools/pm_emit_cycle_event.sh agent_cycle_complete --issue P1-01 --agent architect --commit abc1234
```

This **immediately triggers** the PM Automation webhook (no cron). PM re-runs orchestrator in a new Cloud Agent session.

Do **not** call `pm_emit_cycle_event` when PM only assigns work to another agent (worker emits when done).

---

## 4. When an agent is stale or unresponsive

Orchestrator FAIL on `stale_issues` or blocked deps.

```bash
bash tools/pm_emit_escalation.sh P1-02 remind    # post comment to GitHub issue
bash tools/pm_emit_escalation.sh P1-02 S1        # stronger escalation body
python3 tools/pm_update_issue.py P1-02 --escalation 2 --note "No commit 24h"
```

Re-dispatch same agent or reassign per R&R — do not mark `done` without gates.

---

## 5. Sprint planning — create / sync issues

### New sprint batch

1. Read `docs/IMPLEMENTATION_PLAN.md` §Phase N + `sprint_phases.json` exit gates.
2. Write `docs/sprints/Phase{N}-Sprint{K}-issues.md` (copy Phase1 template).
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

## 7. What PM must never do

- Mark gates PASS without QA evidence
- Let agents start without `run_agent_session_gate.sh` PASS
- Close GitHub issue without updating `sprint_board.json`
- Merge PR without `run_ci_checks.sh` green on `game/development`
- Write game code or edit `.tscn`

---

## 8. Quick reference

| Task | Command |
|------|---------|
| PM session start | `bash tools/run_pm_orchestrator.sh` |
| Agent clearance | `bash tools/run_agent_session_gate.sh <role> <issue_id>` |
| Update issue state | `python3 tools/pm_update_issue.py <id> --status done --commit <sha>` |
| Escalate | `bash tools/pm_emit_escalation.sh <id> <level>` |
| **End cycle → trigger PM** | `bash tools/pm_emit_cycle_event.sh agent_cycle_complete --issue <id> --agent <role> --commit <sha>` |
| Close sprint | `python3 tools/pm_close_sprint.py --next-sprint-number N` |
| Validate board | `python3 tools/validate_sprint_board.py --strict` |

---

## 9. Cross-refs

- `docs/SPRINT_ORCHESTRATION.md` — enforcement model
- `docs/MULTI_AGENT_TEAM.md` — handoff contracts
- `docs/sprints/Phase1-Sprint1-issues.md` — current issue bodies
- `game/data/qa/sprint_board.json` — live sprint state
