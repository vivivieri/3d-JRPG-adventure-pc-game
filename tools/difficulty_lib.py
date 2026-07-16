"""Difficulty multipliers — reference for DifficultyService (docs/COMBAT_SYSTEMS.md §10)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DEFAULT_PATH = Path("game/data/combat/difficulty.json")


def load_catalog(path: str | Path = DEFAULT_PATH) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def active_mode_id(settings: dict[str, Any], catalog: dict[str, Any] | None = None) -> str:
    catalog = catalog or load_catalog()
    key = catalog["policy"]["hard_mode_setting"]
    return "hard" if settings.get(key) else "normal"


def mode_config(mode_id: str, catalog: dict[str, Any] | None = None) -> dict[str, Any]:
    catalog = catalog or load_catalog()
    return catalog["modes"][mode_id]


def scale_stat(base: int | float, stat: str, settings: dict[str, Any], catalog: dict[str, Any] | None = None) -> float:
    cfg = mode_config(active_mode_id(settings, catalog), catalog)
    key = f"enemy_{stat}_multiplier"
    if stat == "xp":
        key = "xp_multiplier"
    return float(base) * float(cfg[key])


def boss_shows_intent_preview(phase: int, is_boss: bool, settings: dict[str, Any], catalog: dict[str, Any] | None = None) -> bool:
    if not is_boss:
        return True
    cfg = mode_config(active_mode_id(settings, catalog), catalog)
    if phase >= 2:
        return bool(cfg["boss_intent_preview_in_phase_2_plus"])
    return cfg.get("boss_intent_preview_turns", 1) > 0


def tide_keeper_gate_hp_percent(settings: dict[str, Any], catalog: dict[str, Any] | None = None) -> float:
    cfg = mode_config(active_mode_id(settings, catalog), catalog)
    return float(cfg["tide_keeper_choice_gate_hp_percent"])


def is_hard_mode(settings: dict[str, Any], catalog: dict[str, Any] | None = None) -> bool:
    return active_mode_id(settings, catalog) == "hard"


def suggest_hard_after_clear(profile_meta: dict[str, Any], catalog: dict[str, Any] | None = None) -> bool:
    catalog = catalog or load_catalog()
    if not bool(catalog.get("policy", {}).get("suggest_hard_after_game_completed", True)):
        return False
    return bool(profile_meta.get("game_completed_once", False))


def scale_enemy_hp(base: int, settings: dict[str, Any], catalog: dict[str, Any] | None = None) -> int:
    return int(round(scale_stat(base, "hp", settings, catalog)))


def scale_enemy_atk(base: int, settings: dict[str, Any], catalog: dict[str, Any] | None = None) -> int:
    return int(round(scale_stat(base, "atk", settings, catalog)))


def scale_xp(base: int, settings: dict[str, Any], catalog: dict[str, Any] | None = None) -> int:
    return int(round(scale_stat(base, "xp", settings, catalog)))
