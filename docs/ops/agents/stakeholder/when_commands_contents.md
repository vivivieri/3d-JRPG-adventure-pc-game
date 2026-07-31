---
id: when-commands-contents
type: how-to
phase: [0, 1]
audience: [pm]
status: active
authority: ops
tokens_est: 504
summary: "Wired in `tools/pm_emit_cycle_event.sh` — every cycle event emits a stakeholder report."
---
# PM Stakeholder Reporting — When reports fire, commands, contents

**Hub:** [`PM_STAKEHOLDER_REPORTING.md`](../PM_STAKEHOLDER_REPORTING.md)

## When to read

Use **PM Stakeholder Reporting — When reports fire, commands, contents** (roles: pm) when executing this procedure Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [3. When reports fire (automatic)](#3-when-reports-fire-automatic)
- [4. PM manual commands](#4-pm-manual-commands)
- [5. Report contents](#5-report-contents)


## 3. When reports fire (automatic)

| Event | Telegram default | Report kind |
|-------|------------------|-------------|
| `agent_cycle_complete` | **Yes** | micro_cycle |
| `agent_cycle_failed` | **Yes** | failure alert |
| `sprint_cycle_complete` | **Yes** | sprint summary |
| `phase_exit` | **Yes** | phase exit |
| `uat_ready` | **Yes** | UAT handoff |
| `watchdog_recovery` / `mcp_blocked` | **Yes** | factory alert |
| `pm_session` (orchestrator end) | No (artifacts only) | dispatch snapshot |

Wired in `tools/pm_emit_cycle_event.sh` — every cycle event emits a stakeholder report.

PM orchestrator step 10 writes `pm_session` report (dashboard refresh without Telegram spam).

---


## 4. PM manual commands

```bash
# After sprint review (P1-06) — phase exit to product owner
bash tools/pm_emit_stakeholder_report.sh --trigger phase_exit --telegram

# Force Telegram on any trigger
bash tools/pm_emit_stakeholder_report.sh --trigger pm_session --telegram

# Artifacts only
bash tools/pm_emit_stakeholder_report.sh --trigger agent_cycle_complete --issue P1-01 --agent architect --no-telegram
```

---


## 5. Report contents

- Sprint progress (% done, issue table)
- Active phase + exit gates
- Last cycle (issue, agent, commit, **session duration + tokens** when `CURSOR_API_KEY` set)
- Next dispatch from orchestrator
- Factory health (watchdog, halt, session budget)
- Agent session telemetry summary (`cycle.session_telemetry` in JSON)
- Blockers / stale issues
- GitHub links

---
