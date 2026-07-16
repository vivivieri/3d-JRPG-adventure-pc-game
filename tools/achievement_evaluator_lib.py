"""Achievement trigger evaluation — reference for AchievementEvaluator GDScript."""
from __future__ import annotations

from pathlib import Path
from typing import Any

DEFAULT_CATALOG = Path("game/data/achievements/achievements.json")


def load_catalog(path: str | Path = DEFAULT_CATALOG) -> list[dict[str, Any]]:
    import json

    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return list(data.get("achievements", []))


def trigger_met(
    trigger: dict[str, Any],
    flags: dict[str, Any],
    settings: dict[str, Any],
    profile_meta: dict[str, Any],
) -> bool:
    if not trigger:
        return False

    if "flag" in trigger:
        if not bool(flags.get(str(trigger["flag"]), False)):
            return False
        setting_key = trigger.get("setting")
        if setting_key is not None and not bool(settings.get(str(setting_key), False)):
            return False
        return True

    if "all_flags" in trigger:
        return all(bool(flags.get(str(fl), False)) for fl in trigger["all_flags"])

    if "flag_equals" in trigger:
        for fk, fv in trigger["flag_equals"].items():
            if str(flags.get(str(fk), "")) != str(fv):
                return False
        return True

    if "meta_endings_count" in trigger:
        endings = profile_meta.get("endings_unlocked", [])
        return len(endings) >= int(trigger["meta_endings_count"])

    if "lore_count" in trigger:
        return int(profile_meta.get("lore_count", 0)) >= int(trigger["lore_count"])

    return False


def evaluate_catalog(
    achievements: list[dict[str, Any]],
    flags: dict[str, Any],
    settings: dict[str, Any],
    profile_meta: dict[str, Any],
) -> list[str]:
    unlocked: list[str] = []
    for ach in achievements:
        if not isinstance(ach, dict):
            continue
        trig = ach.get("trigger") or {}
        if trigger_met(trig, flags, settings, profile_meta):
            unlocked.append(str(ach.get("id", "")))
    return unlocked
