---
id: delivery-control
type: how-to
audience: [pm, architect]
status: active
authority: workflow
tokens_est: 495
---
# Delivery Control — pre-delivery automated gate

**Version:** 1.2
**Purpose:** No outbound delivery (Telegram report, stakeholder update, etc.) goes out until **automated checks pass**. No human reviewer approval step — CI-style gates only. Every delivery is audited.
**Authority:** `game/data/qa/delivery_control.json` · gate: `tools/predelivery_gate.py`
**Cross-refs:** `docs/ops/cheat-sheets/CONTROLS_CHEATSHEET.md`, `docs/ops/qa/PLAYTEST_TELEMETRY.md`, `docs/ops/agents/PM_STAKEHOLDER_REPORTING.md`

---

## Why

Outbound deliveries (Telegram telemetry summaries, etc.) run through the same discipline as merges: **automated checks only**. `required_approvals` is **0** — agents and scripts deliver when checks PASS.

## Flow

```
producer:  analyze_playtest_telemetry.py … --telegram   # checks PASS → delivers; FAIL → blocked
```

Optional legacy commands (`predelivery_gate.py review` / `approve`) remain for audit inspection but are **not required** when `required_approvals` is 0.

## Verdicts

| Situation | Verdict | Delivered? |
|-----------|---------|------------|
| A check FAILs | `HELD ⛔ blocked` | No |
| All checks PASS | `APPROVED ✅` | Yes |
| Same report already sent | `HELD ⛔ already_delivered` | No (dedupe) |
| Overridable metric FAIL | blocked unless `--allow-metric-fail` | Configurable |

## Config (`game/data/qa/delivery_control.json`)

- `policy.approval.required_approvals` — **0** (no human approval)
- `policy.require_confirmation` — **false** (no `--confirm` handshake)
- `policy.block_on_fail` — any FAIL check blocks delivery
- `deliveries.<kind>` — `checks[]`, `review_checklist` (reference for automated jury / future use)

Validated by `tools/validate_delivery_control.py` (gate `L0_delivery_control`). Audit under `artifacts/delivery_audit/` (git-ignored).

## Extending to other deliveries

Add an entry under `deliveries` with `channel`, `checks`, and call `predelivery_gate.gate(...)` from that delivery path.
