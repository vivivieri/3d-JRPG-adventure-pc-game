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
    hooks = load("story/cinematic_hooks.json").get("hooks", [])
    hook_ids = {h["id"] for h in hooks}
    enc_ids = {e["id"] for e in encounters}
    vo_catalog = load("audio/vo_prompts.json")
    vo_clip_ids = set(vo_catalog.get("clips", {}).keys())
    dialogue_voice_ids: set[str] = set()

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
        hook = s.get("cinematic_hook")
        if hook and hook not in hook_ids:
            errors.append(f"scenes.json unknown cinematic_hook: {hook} ({s['scene_id']})")
        req = s.get("requires_flags") or {}
        if isinstance(req, dict):
            for fk in req.keys():
                if fk not in flags:
                    errors.append(f"scenes.json requires unknown flag: {fk} ({s['scene_id']})")

    # Dialogue on_complete flags + optional line requires_flags
    for block in dialogue["scenes"]:
        for fl in block.get("on_complete", {}).get("set_flags", []) or []:
            if fl not in flags:
                errors.append(f"dialogue sets unknown flag: {fl} ({block['scene_id']})")
        for line in block.get("lines", []) or []:
            req = line.get("requires_flags") or {}
            if isinstance(req, dict):
                for fk in req.keys():
                    if fk not in flags:
                        errors.append(f"dialogue line requires unknown flag: {fk} ({block['scene_id']})")
            vid = line.get("voice_id")
            if vid:
                dialogue_voice_ids.add(vid)
                if vid not in vo_clip_ids:
                    errors.append(f"dialogue voice_id missing from vo_prompts.json: {vid} ({block['scene_id']})")
                tier = line.get("vo_tier")
                if tier and vo_catalog.get("clips", {}).get(vid, {}).get("tier") != tier:
                    errors.append(f"dialogue vo_tier mismatch for {vid}: {tier}")

    for vid in vo_clip_ids - dialogue_voice_ids:
        errors.append(f"vo_prompts clip not used in dialogue: {vid}")

    # Cinematic hooks
    for hook in hooks:
        hid = hook.get("id", "?")
        if hook.get("scene_id") not in scene_ids:
            errors.append(f"cinematic_hooks unknown scene_id: {hook.get('scene_id')} ({hid})")
        for fl in hook.get("sets_flags", []) or []:
            if fl not in flags:
                errors.append(f"cinematic_hooks sets unknown flag: {fl} ({hid})")
        skip = hook.get("skip_if_flag")
        if skip and skip not in flags:
            errors.append(f"cinematic_hooks skip_if_flag unknown: {skip} ({hid})")
        req = hook.get("requires_flags") or {}
        if isinstance(req, dict):
            for fk in req.keys():
                if fk not in flags:
                    errors.append(f"cinematic_hooks requires unknown flag: {fk} ({hid})")
        for item in hook.get("requires_items", []) or []:
            if item not in items:
                errors.append(f"cinematic_hooks requires unknown item: {item} ({hid})")
        for step in hook.get("then", []) or []:
            if step.get("type") == "dialogue" and step.get("id") not in dialogue_ids:
                errors.append(f"cinematic_hooks then dialogue missing: {step.get('id')} ({hid})")
            if step.get("type") == "encounter" and step.get("id") not in enc_ids:
                errors.append(f"cinematic_hooks then encounter missing: {step.get('id')} ({hid})")

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
        hook = enc.get("cinematic_hook")
        if hook and hook not in hook_ids:
            errors.append(f"Encounter {enc['id']} unknown cinematic_hook: {hook}")
        for fl in enc.get("requires_flags", []) or []:
            if fl not in flags:
                errors.append(f"Encounter {enc['id']} requires unknown flag: {fl}")

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

    print(f"OK — {len(scene_ids)} scenes, {len(dialogue_ids)} dialogue blocks, {len(quests)} quests, {len(encounters)} encounters, {len(hooks)} cinematic hooks, {len(vo_clip_ids)} vo clips")
    return 0


if __name__ == "__main__":
    sys.exit(main())
