# Delivery Control — pre-delivery review gate

**Version:** 1.0
**Purpose:** No outbound delivery (Telegram report, stakeholder update, etc.) goes out until automated checks pass **and** a human explicitly confirms. Everything is reviewable, and every attempt is audited.
**Authority:** `game/data/qa/delivery_control.json` · gate: `tools/predelivery_gate.py`
**Cross-refs:** `docs/CONTROLS_CHEATSHEET.md`, `docs/PLAYTEST_TELEMETRY.md`, `docs/PM_STAKEHOLDER_REPORTING.md`

---

## Why

We already gate merges and ships (CI, phase gates, remediation loop). Outbound **deliveries** deserve the same discipline: a report should be reviewed and verified before it reaches a stakeholder. This control adds a lightweight, reusable "review → approve → deliver" checkpoint with an audit trail.

## How it works

For any delivery `kind` defined in `delivery_control.json`, the gate:

1. **Runs automated checks** — e.g. config/schema valid (`command`), required charts rendered (`artifacts_exist`), and report metrics within bounds (`metric`, e.g. `parse_errors == 0`, `fail_count == 0`).
2. **Requires explicit confirmation** — external channels (e.g. `telegram`) default to a **preview** (dry-run). Nothing is sent until `--confirm` is passed by a human who reviewed the output.
3. **Writes an audit record** — every attempt (`preview` / `approved` / `blocked`) is written to `artifacts/delivery_audit/` (git-ignored) with checks, metrics, actor, and outcome.

### Verdicts

| Situation | Verdict | Delivered? |
|-----------|---------|-----------|
| A check FAILs | `HELD ⛔ blocked` | No |
| Checks pass, no `--confirm` | `HELD ⛔ preview` | No (review first) |
| Checks pass + `--confirm` | `APPROVED ✅` | Yes |
| Overridable metric FAIL + `--confirm --allow-metric-fail` | `APPROVED ✅` (WARN) | Yes (after human review) |

## Usage

Standalone:

```bash
python3 tools/predelivery_gate.py --kind playtest_telemetry \
  --artifact pacing_curve.png --artifact deaths_by_encounter.png --artifact ending_funnel.png \
  --metric fail_count=0 --metric parse_errors=0 [--confirm] [--allow-metric-fail] [--actor you]
```

Integrated (telemetry): `--telegram` now runs the gate automatically —

```bash
python3 tools/analyze_playtest_telemetry.py logs_dir --telegram             # preview — reviews, does NOT send
python3 tools/analyze_playtest_telemetry.py logs_dir --telegram --confirm    # deliver after review
```

## Config (`game/data/qa/delivery_control.json`)

- `policy.require_confirmation` — external delivery needs `--confirm` (default `true`).
- `policy.block_on_fail` — any FAIL check blocks delivery.
- `channels.<name>.external` / `requires_confirmation` — which channels need review.
- `deliveries.<kind>.checks[]` — `command` | `artifacts_exist` | `metric` (with `op`/`value`; `severity: block_overridable` allows `--allow-metric-fail` after review).

Validated by `tools/validate_delivery_control.py` (gate `L0_delivery_control`, run in `main` docs CI).

## Extending to other deliveries

Add a new entry under `deliveries` (e.g. `stakeholder_report`) with its channel + checks, then call `predelivery_gate.gate(kind, artifacts, metrics, confirmed=...)` from that delivery path before sending. The gate is delivery-agnostic; the automated PM factory cycle events keep their own trigger gating and are unaffected unless explicitly wired in.
