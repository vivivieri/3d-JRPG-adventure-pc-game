#!/usr/bin/env python3
"""Validate save_integrity.json and exercise HMAC round-trip (L0)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from save_integrity_lib import attach_integrity, load_spec, verify_save  # noqa: E402


def main() -> int:
    spec_path = ROOT / "game/data/qa/save_integrity.json"
    if not spec_path.is_file():
        print(f"[FAIL] missing {spec_path}")
        return 1

    spec = load_spec(str(spec_path))
    required = ("algorithm", "integrity_field", "signed_payload_fields", "pepper_source")
    for key in required:
        if key not in spec:
            print(f"[FAIL] save_integrity.json missing {key}")
            return 1

    sample = {
        "version": 1,
        "timestamp": "2026-07-16T00:00:00Z",
        "scene": "res://scenes/world/ruined_village.tscn",
        "spawn_marker": "default",
        "flags": {"met_roku": True},
        "party": {"level": 1},
        "inventory": {"gold": 0},
        "quests": {"active": []},
        "encounters_completed": [],
        "lore_read": [],
        "chests_opened": [],
        "tutorial_seen": [],
        "run_ending": None,
    }
    pepper = "unit-test-pepper"
    signed = attach_integrity(sample, pepper, spec)
    if not verify_save(signed, pepper, spec):
        print("[FAIL] save integrity round-trip failed")
        return 1

    tampered = dict(signed)
    tampered["inventory"] = {"gold": 99999}
    if verify_save(tampered, pepper, spec):
        print("[FAIL] tampered save incorrectly verified")
        return 1

    impl = ROOT / spec["implementation"]["gdscript"]
    port_status = "pending"
    helpers_path = ROOT / "game/data/code/helpers_registry.json"
    if helpers_path.is_file():
        helpers = json.loads(helpers_path.read_text(encoding="utf-8")).get("helpers", [])
        for h in helpers:
            if h.get("id") == "SaveIntegrity":
                port_status = h.get("port_status", "pending")
                break
    if port_status == "ported" and not impl.is_file():
        print(f"[FAIL] missing GDScript reference {impl} (SaveIntegrity port_status=ported)")
        return 1
    if port_status == "ported":
        print("[OK]   SaveIntegrity GDScript present")
    else:
        print(f"[SKIP] SaveIntegrity GDScript — port_status={port_status} (Phase 2 dispatch)")

    print(
        f"[OK]   save_integrity.json — {spec['algorithm']}, "
        f"{len(spec['signed_payload_fields'])} signed field(s)"
    )
    print("[OK]   HMAC round-trip + tamper rejection")
    print("[PASS] save integrity spec")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
