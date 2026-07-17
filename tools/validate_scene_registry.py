#!/usr/bin/env python3
"""Validate scene_registry.json cross-refs (LEVEL_DESIGN, encounters, hooks, zones)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CODE = ROOT / "game" / "data" / "code"
DATA = ROOT / "game" / "data"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    registry = load_json(CODE / "scene_registry.json")
    encounters = {e["id"]: e for e in load_json(DATA / "encounters/story_encounters.json")["encounters"]}
    hooks = {h["id"]: h for h in load_json(DATA / "story/cinematic_hooks.json").get("hooks", [])}
    scenes_spine = {s["scene_id"]: s for s in load_json(DATA / "story/scenes.json")["scenes"]}
    zone_comp = load_json(DATA / "qa/zone_composition.json").get("zones", {})
    palette_zones = set(load_json(DATA / "world/zone_palettes.json").get("zones", {}).keys())

    catalog_scenes = registry.get("scenes", [])
    catalog_ids = {s.get("id") for s in catalog_scenes}
    trigger_exports: dict[str, str] = {}
    hook_triggers: set[str] = set()

    enc_name_re = re.compile(r"^EncounterTrigger_(enc_[a-z0-9_]+)$")

    for sc in catalog_scenes:
        sid = sc.get("id", "?")
        if sc.get("spec_status") != "specified":
            errors.append(f"scene {sid} not specified")
        nodes = sc.get("required_nodes") or []
        children = sc.get("required_children") or []
        if not nodes and not children:
            errors.append(f"scene {sid} missing required_nodes or required_children")

        zone_id = sc.get("zone_id")
        if zone_id and zone_id not in palette_zones:
            errors.append(f"scene {sid} zone_id not in zone_palettes.json: {zone_id}")

        for node in nodes:
            name = node.get("name", "")
            export = node.get("export") or {}
            if name.startswith("EncounterTrigger_"):
                match = enc_name_re.match(name)
                if not match:
                    errors.append(f"{sid}/{name}: EncounterTrigger name must be EncounterTrigger_<encounter_id>")
                    continue
                enc_id = match.group(1)
                exp_id = export.get("encounter_id")
                if not exp_id:
                    errors.append(f"{sid}/{name}: missing export.encounter_id")
                elif exp_id != enc_id:
                    errors.append(f"{sid}/{name}: export.encounter_id {exp_id} != node name {enc_id}")
                elif enc_id not in encounters:
                    errors.append(f"{sid}/{name}: unknown encounter_id {enc_id}")
                else:
                    trigger_exports[enc_id] = f"{sid}/{name}"

            if name.startswith("CinematicTrigger_"):
                hook_id = export.get("hook_id")
                if not hook_id:
                    errors.append(f"{sid}/{name}: missing export.hook_id")
                elif hook_id not in hooks:
                    errors.append(f"{sid}/{name}: unknown hook_id {hook_id}")
                else:
                    hook_triggers.add(hook_id)

            if node.get("type") == "ZoneTransition":
                target = export.get("target_zone")
                if not target:
                    errors.append(f"{sid}/{name}: ZoneTransition missing target_zone")
                elif target not in catalog_ids:
                    errors.append(f"{sid}/{name}: target_zone not in scene_registry: {target}")

    for enc_id, enc in encounters.items():
        if enc_id not in trigger_exports:
            errors.append(f"story_encounters {enc_id} has no EncounterTrigger in scene_registry")

    for hook_id in hooks:
        if hook_id not in hook_triggers:
            spine_refs = [s["scene_id"] for s in scenes_spine.values() if s.get("cinematic_hook") == hook_id]
            if not spine_refs:
                errors.append(f"cinematic_hooks {hook_id} not wired in scene_registry CinematicTrigger")

    router = registry.get("ending_router") or {}
    branch = router.get("branch_flag")
    ending_map = router.get("map") or {}
    if branch != "ending_chosen":
        errors.append("scene_registry ending_router.branch_flag must be ending_chosen")
    for ending_id, row in ending_map.items():
        zid = row.get("zone_id")
        if zid not in catalog_ids:
            errors.append(f"ending_router {ending_id} zone_id missing from scene_registry: {zid}")
        scene_id = row.get("scene_id")
        if scene_id not in scenes_spine:
            errors.append(f"ending_router {ending_id} scene_id missing from scenes.json: {scene_id}")

    for zid in zone_comp:
        if zid in palette_zones and zid not in catalog_ids:
            errors.append(f"zone_composition zone {zid} missing scene_registry entry")

    if errors:
        print("SCENE REGISTRY VALIDATION FAILED", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(
        f"OK — {len(catalog_scenes)} scenes, {len(trigger_exports)} encounter triggers, "
        f"{len(hook_triggers)} cinematic triggers, {len(ending_map)} ending routes"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
