#!/usr/bin/env python3
"""Validate story-driven game data integrity.

Checks cross-references between story/scenes.json, flags.json, quests,
encounters, items, and dialogue scene IDs.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "game" / "data"


def load(rel: str) -> dict | list:
    with open(DATA / rel, encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    errors: list[str] = []
    scenes = load("story/scenes.json")["scenes"]
    flags = {f["id"] for f in load("story/flags.json")["flags"]}
    scene_ids = {s["scene_id"] for s in scenes}
    dialogue = load("dialogue/chapter_01.json")
    dialogue_ids = {s["scene_id"] for s in dialogue["scenes"]}
    items = {i["id"] for i in load("items/items.json")["items"]}
    encounters = load("encounters/story_encounters.json")["encounters"]
    quests = load("quests/main_quests.json")["quests"]

    # Dialogue scenes referenced in story spine
    for s in scenes:
        d = s.get("dialogue")
        if d and d not in dialogue_ids:
            errors.append(f"scenes.json references missing dialogue: {d}")
        for item in s.get("grants_items", []) or []:
            if item not in items:
                errors.append(f"scenes.json grants unknown item: {item}")
        for item in s.get("requires_items", []) or []:
            if item not in items:
                errors.append(f"scenes.json requires unknown item: {item}")
        for fl in s.get("sets_flags", []) or []:
            base = fl.split("=")[0] if "=" in fl else fl
            if "|" in base:
                for part in base.split("|"):
                    if part not in flags:
                        errors.append(f"Unknown flag in scenes.json: {part}")
            elif base not in flags:
                errors.append(f"Unknown flag in scenes.json: {fl}")

    # Encounters reference valid scenes and enemies
    enemy_ids = {e["id"] for e in load("enemies/enemies.json")["enemies"]}
    for enc in encounters:
        if enc["scene_id"] not in scene_ids:
            errors.append(f"Encounter {enc['id']} unknown scene: {enc['scene_id']}")
        for eid in enc["enemies"]:
            if eid not in enemy_ids:
                errors.append(f"Encounter {enc['id']} unknown enemy: {eid}")
        for item in enc.get("on_win", {}).get("grant_items", []) or []:
            if item not in items:
                errors.append(f"Encounter {enc['id']} grants unknown item: {item}")

    # Quest count
    if len(quests) != 5:
        errors.append(f"Expected 5 quests, found {len(quests)}")

    # Shop items exist
    shop = load("shop/roku_shop.json")
    for entry in shop.get("inventory", []):
        if entry["item_id"] not in items:
            errors.append(f"Shop unknown item: {entry['item_id']}")

    if errors:
        print("STORY DATA VALIDATION FAILED", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"OK — {len(scene_ids)} scenes, {len(dialogue_ids)} dialogue blocks, {len(quests)} quests, {len(encounters)} encounters")
    return 0


if __name__ == "__main__":
    sys.exit(main())
