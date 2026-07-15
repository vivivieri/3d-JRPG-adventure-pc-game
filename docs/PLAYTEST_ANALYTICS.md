# Playtest Analytics — gameplay-log analysis

**Version:** 1.0
**Status:** Dev-time QA tool (design data + analyzer on `main`; in-game logger is a `game/development` implementation task)
**Cross-refs:** `docs/FLOW_QA.md`, `docs/PACING_CHART.md`, `docs/GAME_FEEL.md`, `docs/COMBAT_SYSTEMS.md`, `docs/ENDING_DESIGN.md`, `docs/ACCEPTANCE_CRITERIA.md`, `docs/QA_REMEDIATION_LOOP.md`

---

## Purpose

Turn structured gameplay logs from playtests into **measured** pacing / combat / progression / ending metrics, so tuning decisions for this 2–3 hr single-player narrative JRPG are driven by data, not vibes. It feeds the existing flow-QA and remediation loop — a red metric **opens a remediation item** (change one lever, re-measure), it does **not** by itself block ship.

This is a **development** aid. It is deliberately *not* live-service / monetization analytics. Keep logs **local-only** during dev (see [Privacy](#privacy)).

**Authority for thresholds:** `game/data/qa/playtest_analytics_schema.json` (validated by the `L0_playtest_analytics` gate).

---

## Pipeline

```
Godot logger (autoload)  ──>  user://playtest/<run_id>.jsonl
                                        │
                     tools/analyze_playtest_logs.py
                                        │
     report (pacing / combat / progression / endings)  ──>  docs/QA_REMEDIATION_LOOP.md
```

---

## Event schema (JSONL)

One JSON object per line. Common fields on every event: `run_id`, `event`, `t` (seconds since `session_start`), optional `ts` (ISO-8601). Full definition + enums: `game/data/qa/playtest_analytics_schema.json`.

| Event | Key fields | Used for |
|-------|-----------|----------|
| `session_start` / `session_end` | `reason` (`quit`/`completed`/`crash`) | completion rate, drop-off |
| `scene_beat` | `scene` (`SC-00`…`SC-17`) | pacing vs `PACING_CHART` |
| `zone_enter` / `zone_exit` | `zone` | time-per-zone |
| `combat_start` / `combat_end` | `encounter`, `result`, `turns`, `max_turn_resolve_s` | balance, turn-feel |
| `player_death` | `encounter`, `zone` | difficulty spikes |
| `choice_made` | `choice_id`, `option` | branch usage |
| `puzzle_start` / `puzzle_solved` | `puzzle_id`, `duration_s`, `hints_used` | friction |
| `ending_reached` | `ending` (`rewind`/`anchor`/`drift`) | ending funnel |
| `progress` | `note` | **heartbeat** — emit periodically so an inactivity gap is real, not normal pacing |

> **Heartbeats matter.** The `stuck_hotspots` metric flags gaps between progress events longer than `stuck_seconds` (default 300s). Emit a `progress` heartbeat on a cadence (~30–60s) so a long gap means genuine confusion, not the normal minutes between story beats.

---

## Metrics & thresholds

All thresholds live in `playtest_analytics_schema.json` and cross-reference existing gates:

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

`FAIL` = completion/ending/no-combat-before-gate (hard rules); other flags are `WARN` (tuning signals). `WARN`/`FAIL` → open a remediation item per `docs/QA_REMEDIATION_LOOP.md`.

---

## Usage

```bash
# Analyze a directory of per-run logs, or a single multi-run JSONL file:
python3 tools/analyze_playtest_logs.py path/to/logs_dir
python3 tools/analyze_playtest_logs.py game/data/qa/examples/playtest_sample.jsonl

# Machine-readable report + fail the command on any hard FAIL:
python3 tools/analyze_playtest_logs.py logs_dir --json report.json --strict

# Generate synthetic sample logs (for demos / trying the tool):
python3 tools/analyze_playtest_logs.py --emit-sample /tmp/pt_logs --runs 6
```

A committed example lives at `game/data/qa/examples/playtest_sample.jsonl` (6 runs; demonstrates a caves-puzzle stuck hotspot and a Tide Keeper difficulty spike).

---

## In-game logger (implement on `game/development` via GDAI)

The logger is gameplay code, so it is built on `game/development` through the GodotPrompter → GDAI workflow (`.cursorrules` §0) — **not** hand-added to `main`. Reference autoload (`game/scripts/core/playtest_logger.gd`), registered as autoload `PlaytestLogger`:

```gdscript
extends Node
## Local-only JSONL playtest telemetry. No PII. See docs/PLAYTEST_ANALYTICS.md.

const ENABLED := true              # gate behind a debug/consent flag for builds
const HEARTBEAT_S := 45.0
const DIR := "user://playtest"

var _run_id: String
var _t0_ms: int
var _file: FileAccess
var _hb := 0.0

func _ready() -> void:
	if not ENABLED:
		set_process(false)
		return
	DirAccess.make_dir_recursive_absolute(DIR)
	_run_id = "%d_%d" % [Time.get_unix_time_from_system(), randi()]
	_t0_ms = Time.get_ticks_msec()
	_file = FileAccess.open("%s/%s.jsonl" % [DIR, _run_id], FileAccess.WRITE)
	log_event("session_start", {"build": ProjectSettings.get_setting("application/config/version", "dev")})

func _process(delta: float) -> void:
	_hb += delta
	if _hb >= HEARTBEAT_S:
		_hb = 0.0
		log_event("progress", {"note": "heartbeat"})

func log_event(event: String, fields: Dictionary = {}) -> void:
	if not ENABLED or _file == null:
		return
	var row := {"run_id": _run_id, "event": event, "t": (Time.get_ticks_msec() - _t0_ms) / 1000.0}
	row.merge(fields)
	_file.store_line(JSON.stringify(row))
	_file.flush()
```

Call sites (examples): `PlaytestLogger.log_event("scene_beat", {"scene": "SC-05"})`, `..."combat_end", {"encounter": id, "result": "win", "turns": n, "max_turn_resolve_s": m}`, `..."ending_reached", {"ending": "anchor"}`.

---

## Privacy

- **Local-only by default.** Logs write to `user://playtest/`; nothing leaves the machine.
- **No PII.** `run_id` is an opaque random id, never tied to identity. Forbidden fields: `player_name`, `email`, `ip`, `geo`, `machine_id`.
- **Uploading requires consent.** Any telemetry that leaves a tester's machine (or post-launch) needs explicit opt-in + a privacy notice, and Steam disclosure. Prefer collecting logs manually from consenting playtesters during dev.
