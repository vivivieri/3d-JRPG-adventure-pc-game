#!/usr/bin/env python3
"""Validate game/data/qa/agent_session_telemetry_schema.json — L0_agent_session_telemetry gate."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "game/data/qa/agent_session_telemetry_schema.json"
SAMPLE_PATH = ROOT / "game/data/qa/examples/agent_session_telemetry_sample.jsonl"

REQUIRED_TOP = (
    "version",
    "privacy",
    "storage",
    "log_format",
    "event_types",
    "task_categories",
    "efficiency_thresholds",
    "analysis_dimensions",
    "rollup_metrics",
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

    event_names = {et.get("name") for et in data.get("event_types", [])}
    for required in ("session_start", "session_progress", "session_end", "session_failed", "session_token_backfill"):
        if required not in event_names:
            errors.append(f"missing event type: {required}")

    cats = data.get("task_categories", [])
    cat_ids = {c.get("id") for c in cats}
    if "other" not in cat_ids:
        errors.append("task_categories must include 'other' fallback")

    dims = set(data.get("analysis_dimensions", []))
    for required_dim in ("agent_role", "task_category", "issue_id", "outcome"):
        if required_dim not in dims:
            errors.append(f"analysis_dimensions missing: {required_dim}")

    # Sample JSONL parses and references valid event names
    if SAMPLE_PATH.is_file():
        for i, line in enumerate(SAMPLE_PATH.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"sample line {i}: invalid JSON ({exc})")
                continue
            ev = row.get("event")
            if ev not in event_names:
                errors.append(f"sample line {i}: unknown event {ev!r}")
            cat = row.get("task_category")
            if cat and cat not in cat_ids:
                errors.append(f"sample line {i}: unknown task_category {cat!r}")

    if errors:
        print("agent_session_telemetry_schema.json validation FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(
        f"agent_session_telemetry_schema.json: OK "
        f"({len(event_names)} event types, {len(cat_ids)} task categories)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
