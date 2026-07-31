---
id: github-timeline
type: how-to
audience: [pm, builder]
phase: [0, 1]
status: active
authority: agents
tokens_est: 407
summary: "Cloud Agent Setup — GitHub path & timeline — covers 7. GitHub workflow (secondary path); 8. Full factory timeline (example Phase 1)"
---
# Cloud Agent Setup — GitHub path & timeline

**Hub:** [`CLOUD_AGENT_SETUP_RUNBOOK.md`](../CLOUD_AGENT_SETUP_RUNBOOK.md)

## When to read

Use **Cloud Agent Setup — GitHub path & timeline** (roles: pm, builder) when executing this procedure Jump to a section below instead of reading end-to-end (2 sections).

## Jump to

- [7. GitHub workflow (secondary path)](#7-github-workflow-secondary-path)
- [8. Full factory timeline (example Phase 1)](#8-full-factory-timeline-example-phase-1)


## 7. GitHub workflow (secondary path)

`.github/workflows/agent-cycle-pm.yml`:

- **Primary:** `repository_dispatch` from `pm_emit_cycle_event.sh` (when `gh` available)
- **Secondary:** `workflow_run` after **Game CI** success **only if** `artifacts/.cycle_pending` exists (prevents idle CI→PM loops)

Add repo secret: `CURSOR_PM_CYCLE_WEBHOOK_URL` (same URL as Cursor Automation webhook).

---


## 8. Full factory timeline (example Phase 1)

| Step | Actor | Action |
|------|-------|--------|
| 0 | You | One-time snapshot + secrets + Automation A webhook |
| 1 | You | Manual PM run OR `pm_emit_cycle_event.sh` with `agent_cycle_complete` bootstrap |
| 2 | PM | `run_pm_orchestrator.sh` → dispatch **P1-00** |
| 3 | PM/Architect | P1-00 bootstrap → emit `agent_cycle_complete` |
| 4 | PM (webhook) | dispatch **P1-01** Architect |
| 5 | Architect | session gate → shaders → PR → emit event |
| 6 | PM (webhook) | dispatch **P1-02** Builder |
| … | … | repeat until `sprint_complete` |
| N | PM | `sprint_cycle_complete` → Phase1-Sprint2 |
| … | … | phases 1–6 automated L0–L5 |
| End | PM | `uat_ready` → **you** run L6 playtest |

---
