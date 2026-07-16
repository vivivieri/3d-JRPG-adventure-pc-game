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
from zone_visuals_lib import (  # noqa: E402
    apply_to_scene,
    build_environment,
    get_preset,
    hex_to_color,
    load_catalog as load_zone_palettes,
)


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


class ZoneVisualsLibTests(unittest.TestCase):
    def test_hex_to_color_parses_village_fog(self) -> None:
        r, g, b, a = hex_to_color("#8B9DAF")
        self.assertAlmostEqual(r, 0.545098, places=4)
        self.assertAlmostEqual(g, 0.615686, places=4)
        self.assertAlmostEqual(b, 0.686275, places=4)
        self.assertEqual(a, 1.0)

    def test_ruined_village_preset_has_directional(self) -> None:
        catalog = load_zone_palettes(str(ROOT / "game/data/world/zone_palettes.json"))
        preset = get_preset("ruined_village", catalog)
        self.assertEqual(preset.get("directional_color"), "#B8C8D8")
        self.assertEqual(preset.get("fog_density"), 0.008)

    def test_build_environment_fog_enabled(self) -> None:
        catalog = load_zone_palettes(str(ROOT / "game/data/world/zone_palettes.json"))
        env = build_environment("ruined_village", catalog)
        self.assertTrue(env["fog_enabled"])
        self.assertEqual(env["tonemap_mode"], "filmic")
        self.assertTrue(env["glow_enabled"])
        self.assertTrue(env["volumetric_fog_enabled"])

    def test_apply_to_scene_unknown_zone(self) -> None:
        catalog = load_zone_palettes(str(ROOT / "game/data/world/zone_palettes.json"))
        with self.assertRaises(KeyError):
            apply_to_scene("not_a_zone", catalog)

    def test_apply_to_scene_ruined_village(self) -> None:
        catalog = load_zone_palettes(str(ROOT / "game/data/world/zone_palettes.json"))
        bundle = apply_to_scene("ruined_village", catalog)
        self.assertEqual(bundle["zone_id"], "ruined_village")
        self.assertEqual(bundle["node_names"]["world_environment"], "WorldEnvironment")
        self.assertEqual(bundle["directional"]["rotation_degrees"][0], 35.0)


def main() -> int:
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
