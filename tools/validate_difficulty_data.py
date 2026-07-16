#!/usr/bin/env python3
"""Validate difficulty.json and settings schema alignment (L0)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from difficulty_lib import (  # noqa: E402
    active_mode_id,
    boss_shows_intent_preview,
    load_catalog,
    scale_stat,
    tide_keeper_gate_hp_percent,
)


def main() -> int:
    diff_path = ROOT / "game/data/combat/difficulty.json"
    settings_schema = ROOT / "game/data/settings/settings_schema.json"
    settings_defaults = ROOT / "game/data/settings/settings_defaults.json"

    for path in (diff_path, settings_schema, settings_defaults):
        if not path.is_file():
            print(f"[FAIL] missing {path}")
            return 1

    catalog = load_catalog(diff_path)
    schema = json.loads(settings_schema.read_text(encoding="utf-8"))
    defaults = json.loads(settings_defaults.read_text(encoding="utf-8"))

    hard_key = catalog["policy"]["hard_mode_setting"]
    if hard_key not in schema["fields"]:
        print(f"[FAIL] difficulty policy key {hard_key} missing from settings_schema.json")
        return 1
    if hard_key not in defaults["defaults"]:
        print(f"[FAIL] {hard_key} missing from settings_defaults.json")
        return 1
    if hard_key not in schema.get("achievement_settings_keys", []):
        print(f"[FAIL] {hard_key} must be in achievement_settings_keys")
        return 1

    normal = catalog["modes"]["normal"]
    hard = catalog["modes"]["hard"]
    for field in (
        "enemy_hp_multiplier",
        "enemy_atk_multiplier",
        "xp_multiplier",
        "tide_keeper_choice_gate_hp_percent",
    ):
        if field not in normal or field not in hard:
            print(f"[FAIL] modes missing {field}")
            return 1

    if hard["enemy_hp_multiplier"] <= normal["enemy_hp_multiplier"]:
        print("[FAIL] hard HP multiplier must exceed normal")
        return 1
    if hard["boss_intent_preview_in_phase_2_plus"]:
        print("[FAIL] hard mode must hide intents in boss phase 2+")
        return 1

    impl = ROOT / "game/scripts/core/difficulty_service.gd"
    if not impl.is_file():
        print(f"[FAIL] missing {impl}")
        return 1

    # Reference math spot-check
    assert active_mode_id({"hard_mode": False}) == "normal"
    assert active_mode_id({"hard_mode": True}) == "hard"
    assert round(scale_stat(100, "hp", {"hard_mode": True}), 2) == 115.0
    assert round(scale_stat(100, "atk", {"hard_mode": True}), 2) == 110.0
    assert boss_shows_intent_preview(2, True, {"hard_mode": True}) is False
    assert boss_shows_intent_preview(2, True, {"hard_mode": False}) is True
    assert tide_keeper_gate_hp_percent({"hard_mode": True}) == 0.15

    print(f"[OK]   difficulty.json — modes normal + hard")
    print(f"[OK]   settings schema includes {hard_key}")
    print("[OK]   multiplier reference checks")
    print("[PASS] difficulty data")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
