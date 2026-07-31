---
id: automation-bcd
type: tutorial
audience: [pm, architect]
status: active
authority: ops
tokens_est: 456
summary: "On **success**, worker emits `agent_cycle_complete` — PM is not triggered by CI pass alone."
---
# Cloud Setup — Cursor Automations — Automations B–D

**Hub:** [`cursor_automations.md`](../cursor_automations.md)

### Automation B — **CI failure triage** (required)

| Trigger | **CI completed** — workflow `Game CI` — **failure** on `game/development` |
| Workflow | `.github/workflows/game-ci-failure-triage.yml` |
| Prompt | Run remediation; `bash tools/qa_emit_remediation.sh`; re-dispatch **same issue** via `agent_cycle_failed`; do not mark done |

On **success**, worker emits `agent_cycle_complete` — PM is not triggered by CI pass alone.


### Automation C — **Human UAT notify** (end of pipeline)

| Trigger | **Webhook** separate URL, or manual |
| Event | `uat_ready` only |
| Prompt | Post Slack/email/checklist link to `docs/ops/qa/PLAYTEST_SCRIPT.md`; do not run game code |


### Automation D — **Factory watchdog / human alert** (exception only)

| Field | Value |
|-------|--------|
| **Name** | `Factory — human alert` |
| **Trigger** | Webhook → `CURSOR_FACTORY_ALERT_WEBHOOK_URL` (separate from PM cycle webhook) |
| **Events** | `factory_halt`, recovery exhausted |
| **Prompt** | Notify project owner; link `artifacts/factory_health_report.json`; do **not** start workers |

**Scheduled monitoring (GitHub):** `.github/workflows/factory-watchdog.yml` runs every 2h, calls `run_factory_watchdog.sh --recover` **only when unhealthy**. This is stall insurance — not primary PM dispatch. See `docs/ops/agents/FACTORY_WATCHDOG.md`.

**PM webhook also handles `watchdog_recovery`** — same Automation A; add watchdog branch to PM prompt (see `docs/ops/agents/FACTORY_WATCHDOG.md` §5).

---
