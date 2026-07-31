---
id: dashboard-duty-troubleshoot
type: how-to
phase: [0, 1]
audience: [pm]
status: active
authority: ops
tokens_est: 727
summary: "Dashboard, duty, troubleshoot, alignment, refs"
---
# PM Stakeholder Reporting — Dashboard, duty, troubleshoot, alignment, refs

**Hub:** [`PM_STAKEHOLDER_REPORTING.md`](../PM_STAKEHOLDER_REPORTING.md)

## When to read

Use **PM Stakeholder Reporting — Dashboard, duty, troubleshoot, alignment, refs** (roles: pm) when executing this procedure Jump to a section below instead of reading end-to-end (5 sections).

## Jump to

- [6. HTML dashboard](#6-html-dashboard)
- [7. PM Agent duty (enforced)](#7-pm-agent-duty-enforced)
- [8. Troubleshooting](#8-troubleshooting)
- [9. Alignment audit (technical complement)](#9-alignment-audit-technical-complement)
- [10. Cross-refs](#10-cross-refs)


## 6. HTML dashboard

Open locally or download from Cloud Agent artifacts:

```bash
# After any report
xdg-open artifacts/stakeholder_dashboard.html   # Linux
open artifacts/stakeholder_dashboard.html       # macOS
```

Dark-themed single page — progress bar, issue table, full JSON for audit.

---


## 7. PM Agent duty (enforced)

After every worker cycle (enforced via `run_post_agent_cycle.sh`):

1. Done criteria + board update + cycle event → **closes session telemetry + stakeholder report + Telegram**
2. On sprint close: ensure `sprint_cycle_complete` event (Telegram sprint summary)
3. On phase review issue done: `pm_emit_stakeholder_report.sh --trigger phase_exit --telegram`

Skipping stakeholder report = incomplete PM handoff (cite `invalid_pass_patterns` in acceptance criteria).

---


## 8. Troubleshooting

| Symptom | Fix |
|---------|-----|
| No Telegram | Check `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID`; message bot first |
| HTTP 400 Bad Request | HTML parse error — check BotFather token; try `--no-telegram` and read `latest.md` |
| Empty dashboard | Run `bash tools/run_pm_orchestrator.sh` first (populates orchestrator report) |
| Report not on cycle | Ensure `pm_emit_cycle_event.sh` ran (not manual git only) |

---


## 9. Alignment audit (technical complement)

For **spec alignment** and **dispatch readiness** (not sprint schedule), run the standard alignment audit:

```bash
bash tools/run_alignment_audit.sh --trigger post_merge --note "PR #N"
```

Outputs: `artifacts/alignment_audits/latest.md`, `artifacts/alignment_dashboard.html`, history in `docs/archive/compliance/alignment_audit_history.json`.

**Management visuals (status):** prefer auto-generated `audit_exec_summary.png` for stakeholder slides; keep `audit_radar_spec.png` (design & preparation) and `audit_radar_build.png` (development & shipping) for stream detail. Do **not** use legacy `audit_radar_6axis.png` or `tides_mega_dashboard_all_radars.png` for executive readiness — see report § Management visuals.

See `docs/ops/qa/ALIGNMENT_AUDIT.md` — run alongside stakeholder report at phase exit.

---


## 10. Cross-refs

- `docs/ops/agents/CLOUD_AGENT_SETUP_RUNBOOK.md` — Automation secrets
- `docs/ops/agents/FACTORY_WATCHDOG.md` — factory health section in report
- `game/data/qa/stakeholder_report_config.json` — trigger toggles
