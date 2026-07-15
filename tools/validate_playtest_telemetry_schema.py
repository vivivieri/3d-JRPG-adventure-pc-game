#!/usr/bin/env python3
"""Validate game/data/qa/playtest_telemetry_schema.json — L0_playtest_telemetry gate.

Checks structure of the playtest telemetry schema and keeps its thresholds
aligned with the rest of the QA catalog (feel_thresholds.json combat turn time,
acceptance_criteria.json endings). See docs/PLAYTEST_TELEMETRY.md.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "game/data/qa/playtest_telemetry_schema.json"
FEEL_PATH = ROOT / "game/data/qa/feel_thresholds.json"
CRITERIA_PATH = ROOT / "game/data/qa/acceptance_criteria.json"

REQUIRED_TOP = ("version", "privacy", "log_format", "event_types", "progress_events", "thresholds", "scene_beats")
REQUIRED_THRESHOLDS = (
    "completion_rate_min_percent",
    "target_playtime_minutes",
    "stuck_seconds",
    "combat_turn_resolve_max_s",
    "encounter_avg_deaths_flag",
    "no_combat_before_scene",
    "scene_beat_drift_tolerance_min",
    "endings_required_coverage",
)


def main() -> int:
    if not SCHEMA_PATH.is_file():
        print(f"Missing {SCHEMA_PATH}", file=sys.stderr)
        return 1

    data = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    errors: list[str] = []

    for key in REQUIRED_TOP:
        if key not in data:
            errors.append(f"missing top-level key: {key}")

    # Event types well-formed + progress_events reference real events.
    event_names = {et.get("name") for et in data.get("event_types", [])}
    for et in data.get("event_types", []):
        if "name" not in et or "required" not in et:
            errors.append(f"event_type missing name/required: {et}")
    for required_event in ("session_start", "session_end", "scene_beat", "ending_reached"):
        if required_event not in event_names:
            errors.append(f"event_types missing core event: {required_event}")
    for pe in data.get("progress_events", []):
        if pe not in event_names:
            errors.append(f"progress_events references unknown event: {pe}")

    thresholds = data.get("thresholds", {})
    for key in REQUIRED_THRESHOLDS:
        if key not in thresholds:
            errors.append(f"thresholds missing {key}")

    # scene_beats sorted non-decreasing by target_min with unique ids.
    beats = data.get("scene_beats", [])
    seen_ids: set[str] = set()
    last_min = -1
    for b in beats:
        if "id" not in b or "target_min" not in b:
            errors.append(f"scene_beat missing id/target_min: {b}")
            continue
        if b["id"] in seen_ids:
            errors.append(f"duplicate scene_beat id: {b['id']}")
        seen_ids.add(b["id"])
        if b["target_min"] < last_min:
            errors.append(f"scene_beats not sorted by target_min at {b['id']}")
        last_min = b["target_min"]

    # no_combat_before_scene must reference a real beat id.
    gate_scene = thresholds.get("no_combat_before_scene", {}).get("value")
    if gate_scene and gate_scene not in seen_ids:
        errors.append(f"no_combat_before_scene '{gate_scene}' not in scene_beats")

    # Alignment: combat turn budget matches feel_thresholds feel_combat_turn_max.
    if FEEL_PATH.is_file():
        feel = json.loads(FEEL_PATH.read_text(encoding="utf-8"))
        turn = next((s for s in feel.get("scenarios", []) if s.get("id") == "feel_combat_turn_max"), None)
        schema_turn = thresholds.get("combat_turn_resolve_max_s", {}).get("value")
        if turn and schema_turn is not None and turn.get("max_seconds") != schema_turn:
            errors.append(
                f"combat_turn_resolve_max_s ({schema_turn}) != feel_thresholds feel_combat_turn_max.max_seconds ({turn.get('max_seconds')})"
            )

    # Alignment: endings match L5_e2e_three_endings gate.
    if CRITERIA_PATH.is_file():
        crit = json.loads(CRITERIA_PATH.read_text(encoding="utf-8"))
        l5 = crit.get("gates", {}).get("L5_e2e_three_endings", {}).get("pass", {}).get("endings_passed")
        endings = thresholds.get("endings_required_coverage", {}).get("value")
        if l5 and endings and set(l5) != set(endings):
            errors.append(f"endings_required_coverage {endings} != L5_e2e_three_endings {l5}")

    if errors:
        print("playtest_telemetry_schema.json validation FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"playtest_telemetry_schema.json: OK ({len(event_names)} event types, {len(beats)} scene beats)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
