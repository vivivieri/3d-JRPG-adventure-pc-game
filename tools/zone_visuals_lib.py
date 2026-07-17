"""Zone environment presets — reference for ZoneVisuals (docs/art/RENDERING_GUIDE.md §13)."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

DEFAULT_PALETTE_PATH = Path("game/data/world/zone_palettes.json")
HEX_RE = re.compile(r"^#?([0-9A-Fa-f]{6})$")


def load_catalog(path: str | Path = DEFAULT_PALETTE_PATH) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if "zones" not in data:
        raise ValueError("zone_palettes.json missing zones")
    return data


def hex_to_color(hex_value: str) -> tuple[float, float, float, float]:
    cleaned = hex_value.strip().upper()
    match = HEX_RE.match(cleaned if cleaned.startswith("#") else f"#{cleaned}")
    if not match:
        return (1.0, 0.0, 1.0, 1.0)
    raw = match.group(1)
    r = int(raw[0:2], 16) / 255.0
    g = int(raw[2:4], 16) / 255.0
    b = int(raw[4:6], 16) / 255.0
    return (r, g, b, 1.0)


def get_preset(zone_key: str, catalog: dict[str, Any] | None = None) -> dict[str, Any]:
    catalog = catalog or load_catalog()
    zones = catalog.get("zones", {})
    preset = zones.get(zone_key)
    if not isinstance(preset, dict):
        return {}
    return dict(preset)


def defaults(catalog: dict[str, Any] | None = None) -> dict[str, Any]:
    catalog = catalog or load_catalog()
    raw = catalog.get("defaults", {})
    if not isinstance(raw, dict):
        return {}
    return dict(raw)


def build_environment(
    zone_key: str,
    catalog: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return Environment-equivalent settings for GDScript build_environment()."""
    catalog = catalog or load_catalog()
    preset = get_preset(zone_key, catalog)
    if not preset:
        raise KeyError(f"unknown zone_id: {zone_key}")
    cfg = defaults(catalog)

    sky_horizon = str(preset.get("sky_horizon", "#B8D0E0"))
    ground_horizon = str(preset.get("ground_horizon", "#6A8A9A"))
    ground_r, ground_g, ground_b, _ = hex_to_color(ground_horizon)
    darken = float(cfg.get("ground_bottom_darken", 0.2))

    return {
        "background_mode": "sky",
        "tonemap_mode": str(cfg.get("tonemap_mode", "filmic")),
        "ambient_light_source": str(cfg.get("ambient_light_source", "color")),
        "ambient_light_color": hex_to_color(sky_horizon),
        "ambient_light_energy": float(cfg.get("ambient_light_energy", 0.4)),
        "fog_enabled": True,
        "fog_light_color": hex_to_color(str(preset.get("fog_color", "#8B9DAF"))),
        "fog_density": float(preset.get("fog_density", 0.008)),
        "fog_sky_affect": float(cfg.get("fog_sky_affect", 0.85)),
        "aerial_perspective": float(preset.get("aerial_perspective", cfg.get("fog_sky_affect", 0.85))),
        "glow_enabled": bool(preset.get("glow_enabled", True)),
        "glow_intensity": float(preset.get("glow_intensity", 0.35)),
        "glow_blend_mode": str(cfg.get("glow_blend_mode", "softlight")),
        "volumetric_fog_enabled": bool(preset.get("volumetric_fog_enabled", False)),
        "volumetric_fog_density": float(cfg.get("volumetric_fog_density", 0.02)),
        "procedural_sky": {
            "sky_top_color": hex_to_color(str(preset.get("sky_top", "#4A7A9A"))),
            "sky_horizon_color": hex_to_color(sky_horizon),
            "ground_horizon_color": (ground_r, ground_g, ground_b, 1.0),
            "ground_bottom_color": (
                ground_r * (1.0 - darken),
                ground_g * (1.0 - darken),
                ground_b * (1.0 - darken),
                1.0,
            ),
            "sun_angle_max": float(cfg.get("procedural_sky_sun_angle_max", 28.0)),
        },
    }


def directional_settings(zone_key: str, catalog: dict[str, Any] | None = None) -> dict[str, Any]:
    catalog = catalog or load_catalog()
    preset = get_preset(zone_key, catalog)
    cfg = defaults(catalog)
    rot = preset.get("directional_rotation_deg", [35, -45, 0])
    if not isinstance(rot, list):
        rot = [35, -45, 0]
    rz = float(rot[2]) if len(rot) > 2 else 0.0
    return {
        "light_color": hex_to_color(str(preset.get("directional_color", "#B8C8D8"))),
        "shadow_enabled": bool(cfg.get("directional_shadow_enabled", True)),
        "rotation_degrees": [float(rot[0]), float(rot[1]), rz],
    }


def fill_light_settings(zone_key: str, catalog: dict[str, Any] | None = None) -> dict[str, Any]:
    catalog = catalog or load_catalog()
    preset = get_preset(zone_key, catalog)
    cfg = defaults(catalog)
    return {
        "light_color": hex_to_color(str(preset.get("fill_color", "#D4A880"))),
        "light_energy": float(cfg.get("fill_light_energy", 0.8)),
        "omni_range": float(cfg.get("fill_light_omni_range", 12.0)),
    }


def apply_to_scene(
    zone_key: str,
    catalog: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Canonical zone entry — returns all settings Builder wires in the scene."""
    catalog = catalog or load_catalog()
    if not get_preset(zone_key, catalog):
        raise KeyError(f"unknown zone_id: {zone_key}")
    return {
        "zone_id": zone_key,
        "environment": build_environment(zone_key, catalog),
        "directional": directional_settings(zone_key, catalog),
        "fill_light": fill_light_settings(zone_key, catalog),
        "node_names": {
            "world_environment": str(
                defaults(catalog).get("world_environment_node_name", "WorldEnvironment")
            ),
            "directional_light": str(
                defaults(catalog).get("directional_light_node_name", "DirectionalLight3D")
            ),
            "fill_light_group": str(defaults(catalog).get("fill_light_group", "zone_fill_light")),
        },
    }
