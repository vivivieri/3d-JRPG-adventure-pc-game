---
id: metrics-usage-logger
type: reference
phase: [1, 6]
audience: [qa, flow]
status: active
authority: qa
tokens_est: 936
summary: "Metrics, usage, in-game logger"
---
# Playtest Telemetry — Metrics, usage, in-game logger

**Hub:** [`PLAYTEST_TELEMETRY.md`](../PLAYTEST_TELEMETRY.md)

## Metrics & thresholds

All thresholds live in `playtest_telemetry_schema.json` and cross-reference existing gates:

| Metric | Threshold | Maps to |
|--------|-----------|---------|
| `completion_rate` | ≥ 80% runs completed | `L6_human_playtest.completion_percent` |
| `ending_coverage` | all of rewind/anchor/drift reached across runs | `L5_e2e_three_endings` |
| `avg_playtime` | 150 ± 45 min | `PACING_CHART` |
| `no_combat_before_gate` | no combat before `SC-05` | `PACING_CHART` design rule |
| `scene_pacing_drift` | per-beat arrival within ±12 min of target | `PACING_CHART` beat chart |
| `combat_difficulty` | avg deaths/run per encounter ≤ 3 | `COMBAT_SYSTEMS` |
| `combat_turn_resolve` | `max_turn_resolve_s` ≤ 3.0 | `feel_combat_turn_max` (`GAME_FEEL`) |
| `stuck_hotspots` | no > 300s inactivity gaps | `FLOW_QA` |

`FAIL` = completion/ending/no-combat-before-gate (hard rules); other flags are `WARN` (tuning signals). `WARN`/`FAIL` → open a remediation item per `docs/ops/qa/QA_REMEDIATION_LOOP.md`.

---


## Usage

```bash
# Analyze a directory of per-run logs, or a single multi-run JSONL file:
python3 tools/analyze_playtest_telemetry.py path/to/logs_dir
python3 tools/analyze_playtest_telemetry.py game/data/qa/examples/playtest_telemetry_sample.jsonl

# Machine-readable report + fail the command on any hard FAIL:
python3 tools/analyze_playtest_telemetry.py logs_dir --json report.json --strict

# Generate synthetic sample logs (for demos / trying the tool):
python3 tools/analyze_playtest_telemetry.py --emit-sample /tmp/pt_logs --runs 6

# Visual report — matplotlib charts + one-page Markdown:
python3 tools/analyze_playtest_telemetry.py logs_dir \
  --charts artifacts/telemetry_reports/charts \
  --report artifacts/telemetry_reports/latest.md

# Push summary + charts to the product owner's Telegram (opt-in + reviewed):
python3 tools/analyze_playtest_telemetry.py logs_dir --telegram             # creates a QA review request, HOLDS
python3 tools/analyze_playtest_telemetry.py logs_dir --telegram             # delivers when checks PASS
```

A committed example lives at `game/data/qa/examples/playtest_telemetry_sample.jsonl` (6 runs; demonstrates a caves-puzzle stuck hotspot and a Tide Keeper difficulty spike).

### Reports, charts & delivery

- **Charts** (`--charts DIR`, default `artifacts/telemetry_reports/charts`): pacing curve (arrival vs `PACING_CHART` target), avg deaths per encounter (with difficulty flag line), and the ending/completion funnel — rendered with `matplotlib` (Agg, headless).
- **Markdown report** (`--report PATH`): one-page summary with the metrics table + chart list, suitable for a stakeholder update.
- **Telegram** (`--telegram`): delivers the summary + chart images when **automated pre-delivery checks PASS** (`docs/ops/workflow/DELIVERY_CONTROL.md`). No human approval step.
- **Storage:** all outputs live under `artifacts/telemetry_reports/**`, which is **git-ignored** — charts, reports, and raw logs are **not** committed to GitHub (only the tools/schema/docs/sample are). Raw telemetry stays local by default (see [Privacy](#privacy)).

---


## In-game logger (implement on `game/development` via GDAI)

The logger is gameplay code, so it is built on `game/development` through the GodotPrompter → GDAI workflow (`.cursorrules` §0) — **not** hand-added to `main`. Reference autoload (`game/scripts/core/playtest_logger.gd`), registered as autoload `PlaytestLogger`:

```gdscript
extends Node
