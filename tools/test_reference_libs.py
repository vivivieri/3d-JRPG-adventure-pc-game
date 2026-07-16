#!/usr/bin/env python3
"""Tests for Python reference libs — parity baseline before GDScript ports."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from achievement_evaluator_lib import evaluate_catalog, load_catalog, trigger_met  # noqa: E402
from difficulty_lib import (  # noqa: E402
    boss_shows_intent_preview,
    is_hard_mode,
    load_catalog as load_difficulty,
    scale_enemy_hp,
    suggest_hard_after_clear,
    tide_keeper_gate_hp_percent,
)
from save_integrity_lib import attach_integrity, load_spec, sign_save, verify_save  # noqa: E402
from settings_store_lib import defaults, is_hard_mode as settings_hard, load_settings, set_value  # noqa: E402


class DifficultyLibTests(unittest.TestCase):
    def test_normal_mode_multipliers(self) -> None:
        settings = {"hard_mode": False}
        self.assertEqual(scale_enemy_hp(100, settings), 100)
        self.assertFalse(is_hard_mode(settings))

    def test_hard_mode_multipliers(self) -> None:
        settings = {"hard_mode": True}
        hp = scale_enemy_hp(100, settings)
        self.assertGreater(hp, 100)
        self.assertTrue(is_hard_mode(settings))

    def test_boss_intent_hard_phase2(self) -> None:
        catalog = load_difficulty()
        settings = {"hard_mode": True}
        self.assertFalse(boss_shows_intent_preview(2, True, settings, catalog))

    def test_tide_keeper_gate(self) -> None:
        self.assertAlmostEqual(tide_keeper_gate_hp_percent({"hard_mode": False}), 0.1)

    def test_suggest_hard(self) -> None:
        self.assertTrue(suggest_hard_after_clear({"game_completed_once": True}))


class SaveIntegrityLibTests(unittest.TestCase):
    def test_round_trip(self) -> None:
        spec = load_spec(str(ROOT / "game/data/qa/save_integrity.json"))
        save = {"version": 1, "flags": {"game_started": True}, "party": ["urashima"]}
        signed = attach_integrity(save, "test-pepper", spec)
        self.assertIn("_integrity", signed)
        self.assertTrue(verify_save(signed, "test-pepper", spec))
        tampered = dict(signed)
        tampered["flags"] = {"game_started": False}
        self.assertFalse(verify_save(tampered, "test-pepper", spec))


class SettingsStoreLibTests(unittest.TestCase):
    def test_defaults_load(self) -> None:
        d = defaults(ROOT / "game/data/settings/settings_defaults.json")
        self.assertIn("hard_mode", d)
        self.assertFalse(d["hard_mode"])

    def test_set_hard_mode(self) -> None:
        s = {"hard_mode": False}
        s2, changed = set_value("hard_mode", True, s)
        self.assertTrue(changed)
        self.assertTrue(settings_hard(s2))


class AchievementEvaluatorLibTests(unittest.TestCase):
    def test_flag_trigger(self) -> None:
        self.assertTrue(trigger_met({"flag": "game_started"}, {"game_started": True}, {}, {}))

    def test_hard_achievement(self) -> None:
        ach = load_catalog()
        flags = {"tide_keeper_defeated": True}
        settings = {"hard_mode": True}
        ids = evaluate_catalog(ach, flags, settings, {})
        self.assertIn("ACH_HARD_TIDE", ids)


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
