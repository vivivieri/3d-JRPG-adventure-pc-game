"""Player settings persistence — reference for SettingsStore GDScript."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DEFAULTS_PATH = Path("game/data/settings/settings_defaults.json")
# GDScript uses user://settings.json — tests pass an override path.
DEFAULT_USER_PATH = Path("user_settings.json")


def defaults(path: str | Path = DEFAULTS_PATH) -> dict[str, Any]:
    p = Path(path)
    if not p.is_file():
        return {"hard_mode": False}
    data = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return {"hard_mode": False}
    defs = data.get("defaults")
    if not isinstance(defs, dict):
        return {"hard_mode": False}
    return dict(defs)


def load_settings(
    user_path: str | Path = DEFAULT_USER_PATH,
    defaults_path: str | Path = DEFAULTS_PATH,
    cache: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if cache is not None and cache:
        return dict(cache)
    merged = defaults(defaults_path)
    up = Path(user_path)
    if up.is_file():
        parsed = json.loads(up.read_text(encoding="utf-8"))
        if isinstance(parsed, dict):
            merged.update(parsed)
    return merged


def save_settings(
    settings: dict[str, Any],
    user_path: str | Path = DEFAULT_USER_PATH,
) -> None:
    Path(user_path).write_text(json.dumps(settings, indent="\t"), encoding="utf-8")


def get_value(
    key: str,
    settings: dict[str, Any],
    fallback: Any = None,
) -> Any:
    return settings[key] if key in settings else fallback


def set_value(
    key: str,
    value: Any,
    settings: dict[str, Any],
) -> tuple[dict[str, Any], bool]:
    """Returns (new_settings, hard_mode_changed)."""
    prior_hard = bool(settings.get("hard_mode", False))
    out = dict(settings)
    out[key] = value
    changed = key == "hard_mode" and bool(value) != prior_hard
    return out, changed


def is_hard_mode(settings: dict[str, Any]) -> bool:
    return bool(settings.get("hard_mode", False))
