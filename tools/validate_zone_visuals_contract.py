#!/usr/bin/env python3
"""Validate ZoneVisuals registry ↔ Python reference parity."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "game/data/code/base_classes.json"
LIB = ROOT / "tools/zone_visuals_lib.py"


def load_lib():
    spec = importlib.util.spec_from_file_location("zone_visuals_lib", LIB)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {LIB}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    errors: list[str] = []
    data = json.loads(BASE.read_text(encoding="utf-8"))
    zv = next((b for b in data.get("bases", []) if b.get("id") == "ZoneVisuals"), None)
    if not zv:
        errors.append("ZoneVisuals missing from base_classes.json")
        return 1

    if not LIB.is_file():
        errors.append(f"missing python reference: {LIB}")
    else:
        lib = load_lib()
        for entry in zv.get("public_api", []):
            name = entry.get("name")
            if not name:
                continue
            if entry.get("static") is False:
                continue
            if not hasattr(lib, name):
                errors.append(f"zone_visuals_lib missing public_api method: {name}")

        required_helpers = ("directional_settings", "fill_light_settings", "defaults", "load_catalog")
        for name in required_helpers:
            if not hasattr(lib, name):
                errors.append(f"zone_visuals_lib missing helper: {name}")

        bundle = lib.apply_to_scene("ruined_village")
        for key in ("environment", "directional", "fill_light", "node_names"):
            if key not in bundle:
                errors.append(f"apply_to_scene bundle missing key: {key}")

    expected = {
        "apply_to_scene",
        "build_environment",
        "hex_to_color",
        "get_preset",
        "directional_settings",
        "fill_light_settings",
    }
    api_names = {e.get("name") for e in zv.get("public_api", [])}
    if "apply_zone_visuals" not in api_names:
        errors.append("ZoneVisuals public_api missing: apply_zone_visuals")
    for name in sorted(expected - api_names):
        errors.append(f"ZoneVisuals public_api missing: {name}")

    if errors:
        print("ZONE VISUALS CONTRACT VALIDATION FAILED", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print("OK — ZoneVisuals registry ↔ zone_visuals_lib contract")
    return 0


if __name__ == "__main__":
    sys.exit(main())
