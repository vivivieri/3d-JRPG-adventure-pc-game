# Delivery Control — pre-delivery review gate

**Version:** 1.1
**Purpose:** No outbound delivery (Telegram report, stakeholder update, etc.) goes out until automated checks pass **and** a designated reviewer (default **QA**) approves. The reviewer is shown an explicit checklist so it knows exactly what to review. Every action is audited.
**Authority:** `game/data/qa/delivery_control.json` · gate: `tools/predelivery_gate.py`
**Cross-refs:** `docs/cheat-sheets/CONTROLS_CHEATSHEET.md`, `docs/cheat-sheets/RR_CHEATSHEET.md`, `docs/qa/PLAYTEST_TELEMETRY.md`, `docs/agents/PM_STAKEHOLDER_REPORTING.md`

---

## Why

We already gate merges and ships (CI, phase gates, remediation loop). Outbound **deliveries** deserve the same discipline: a report must be reviewed and verified before it reaches a stakeholder. This adds a lightweight, reusable **producer → reviewer → deliver** handshake with separation of duties and an audit trail.

## Roles & policy

- **Producer** — the agent/tool that generates the report (e.g. the telemetry analyzer).
- **Reviewer** — the role that approves delivery. Default: **QA** (`policy.approval.reviewer_roles`). Required approvals: **1** (`required_approvals`).
- **Separation of duties** — an approver cannot be the producer (`separation_of_duties: true`), mirroring the Architect≠Builder rule in `docs/cheat-sheets/RR_CHEATSHEET.md`.

## Flow

```
producer:  analyze_playtest_telemetry.py … --telegram        # creates a review request, HOLDS (no send)
reviewer:  predelivery_gate.py review  --request <id>         # shows checks + checklist + artifacts
reviewer:  predelivery_gate.py approve --request <id> --actor qa   # records approval (separation of duties enforced)
producer:  analyze_playtest_telemetry.py … --telegram        # same content now approved -> delivers, then marks delivered
```

The `request_id` is **content-derived** (kind + artifact names + metrics), so a producer re-run with the *same* result set maps to the same request the reviewer approved. If the results change, the id changes and a **fresh approval** is required.

## What the reviewer sees (so it knows what to review)

`predelivery_gate.py review --request <id>` prints:
1. **Automated check results** (schema valid, charts present, no parse errors, no FAIL metric).
2. **Artifacts to inspect** (the chart paths).
3. **The review checklist** — the `review_checklist` for that delivery in `delivery_control.json`, e.g. for `playtest_telemetry`: charts match the summary numbers, WARN/FAIL flags are expected or acknowledged, no PII, sample size adequate, correct channel/timing.

## Verdicts

| Situation | Verdict | Delivered? |
|-----------|---------|-----------|
| A check FAILs | `HELD ⛔ blocked` | No |
| Checks pass, no approval yet | `HELD ⛔ pending_review` | No — reviewer must approve |
| Approval by producer or non-reviewer role | approve `REJECTED` | No |
| Required approvals recorded (QA) | `APPROVED ✅` | Yes (on next producer run) |
| Same report already sent | `HELD ⛔ already_delivered` | No (dedupe) |
| Overridable metric FAIL + reviewer `approve … --allow-metric-fail` | approved (WARN) | Yes (after review) |

## Config (`game/data/qa/delivery_control.json`)

- `policy.approval` — `required_approvals` (1), `separation_of_duties` (true), `reviewer_roles` (`["qa"]`).
- `policy.block_on_fail` — any FAIL check blocks delivery.
- `channels.<name>.external` / `requires_confirmation` — which channels need review.
- `deliveries.<kind>` — `channel`, `required_artifacts`, `review_checklist` (what the reviewer confirms), and `checks[]` (`command` | `artifacts_exist` | `metric`; `severity: block_overridable` allows `--allow-metric-fail`).

Validated by `tools/validate_delivery_control.py` (gate `L0_delivery_control`, run in `main` docs CI). Audit + pending requests live under `artifacts/delivery_audit/` (git-ignored).

## Extending to other deliveries

Add an entry under `deliveries` (e.g. `stakeholder_report`) with its channel, `review_checklist`, and `checks`, then call `predelivery_gate.gate(kind, artifacts, metrics, actor=…, context=…)` from that delivery path. The automated PM factory cycle sends keep their own trigger gating and are unaffected unless explicitly wired in.
