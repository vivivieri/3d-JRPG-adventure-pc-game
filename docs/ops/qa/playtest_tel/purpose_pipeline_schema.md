---
id: purpose-pipeline-schema
type: reference
phase: [1, 6]
audience: [qa, flow]
status: active
authority: qa
tokens_est: 697
summary: "Playtest Telemetry — Purpose, pipeline, schema — Turn structured gameplay logs from playtests into measured pacing / combat / progression / ending metrics, so t"
---
# Playtest Telemetry — Purpose, pipeline, schema

**Hub:** [`PLAYTEST_TELEMETRY.md`](../PLAYTEST_TELEMETRY.md)

## When to read

Use **Playtest Telemetry — Purpose, pipeline, schema** (roles: qa, flow) when you need this reference during the current task Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [Purpose](#purpose)
- [Pipeline](#pipeline)
- [Event schema (JSONL)](#event-schema-jsonl)


## Purpose

Turn structured gameplay logs from playtests into **measured** pacing / combat / progression / ending metrics, so tuning decisions for this 2–3 hr single-player narrative JRPG are driven by data, not vibes. It feeds the existing flow-QA and remediation loop — a red metric **opens a remediation item** (change one lever, re-measure), it does **not** by itself block ship.

This is a **development** capability. It is deliberately *not* live-service / monetization telemetry, and it does not adapt the game at runtime. Keep logs **local-only** during dev (see [Privacy](#privacy)).

**Authority for thresholds:** `game/data/qa/playtest_telemetry_schema.json` (validated by the `L0_playtest_telemetry` gate).

---


## Pipeline

```
Godot logger (autoload)  ──>  user://playtest/<run_id>.jsonl
                                        │
                     tools/analyze_playtest_telemetry.py
                                        │
     report (pacing / combat / progression / endings)  ──>  docs/ops/qa/QA_REMEDIATION_LOOP.md
```

---


## Event schema (JSONL)

One JSON object per line. Common fields on every event: `run_id`, `event`, `t` (seconds since `session_start`), optional `ts` (ISO-8601). Full definition + enums: `game/data/qa/playtest_telemetry_schema.json`.

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
