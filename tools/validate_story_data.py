#!/usr/bin/env python3
"""Validate story-driven game data integrity.

Checks cross-references between story/scenes.json, flags.json, quests,
encounters, items, and dialogue scene IDs.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "game" / "data"
REQUIRED_LOCALES = ("en", "ja", "zh", "zh-Hant")


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

    # scene_registry hook_id exports must exist in cinematic_hooks
    scene_registry = load("code/scene_registry.json")
    for sc in scene_registry.get("scenes", []):
        for node in sc.get("required_nodes", []) or []:
            export = node.get("export") or {}
            hook = export.get("hook_id")
            if hook and hook not in hook_ids:
                errors.append(
                    f"scene_registry unknown hook_id: {hook} ({sc.get('id')}/{node.get('name')})"
                )

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

    # Flag enum values (for choice validation)
    flag_defs = {f["id"]: f for f in load("story/flags.json")["flags"]}

    # Dialogue on_complete flags + optional line requires_flags
    for block in dialogue["scenes"]:
        for fl in block.get("on_complete", {}).get("set_flags", []) or []:
            if fl not in flags:
                errors.append(f"dialogue sets unknown flag: {fl} ({block['scene_id']})")
        for choice in block.get("choices", []) or []:
            sf = choice.get("set_flags") or {}
            if isinstance(sf, dict):
                for fk, fv in sf.items():
                    if fk not in flags:
                        errors.append(f"dialogue choice sets unknown flag: {fk} ({block['scene_id']})")
                    else:
                        allowed = flag_defs[fk].get("values")
                        if allowed and fv not in allowed:
                            errors.append(f"dialogue choice sets invalid enum value: {fk}={fv} ({block['scene_id']})")
            for field in ("subtext", "subtext_warm"):
                text_obj = choice.get(field)
                if text_obj:
                    if not isinstance(text_obj, dict):
                        errors.append(f"dialogue choice {choice.get('id')} {field} must be locale object ({block['scene_id']})")
                    else:
                        for loc in REQUIRED_LOCALES:
                            if not str(text_obj.get(loc, "")).strip():
                                errors.append(
                                    f"dialogue choice {choice.get('id')} {field} missing locale: {loc} "
                                    f"({block['scene_id']})"
                                )
            warm_req = choice.get("subtext_warm_requires_flags") or {}
            if warm_req and not choice.get("subtext_warm"):
                errors.append(
                    f"dialogue choice {choice.get('id')} subtext_warm_requires_flags without subtext_warm "
                    f"({block['scene_id']})"
                )
            if isinstance(warm_req, dict):
                for fk, fv in warm_req.items():
                    if fk not in flags:
                        errors.append(
                            f"dialogue choice subtext_warm_requires_flags unknown flag: {fk} ({block['scene_id']})"
                        )
                    else:
                        allowed = flag_defs[fk].get("values")
                        if allowed and fv not in allowed:
                            errors.append(
                                f"dialogue choice subtext_warm invalid enum: {fk}={fv} ({block['scene_id']})"
                            )
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
            stype = step.get("type")
            if stype == "dialogue" and step.get("id") not in dialogue_ids:
                errors.append(f"cinematic_hooks then dialogue missing: {step.get('id')} ({hid})")
            if stype == "encounter" and step.get("id") not in enc_ids:
                errors.append(f"cinematic_hooks then encounter missing: {step.get('id')} ({hid})")
            if stype == "load_ending":
                branch = step.get("branch_flag")
                if branch not in flags:
                    errors.append(f"cinematic_hooks load_ending unknown branch_flag: {branch} ({hid})")
                router = load("code/scene_registry.json").get("ending_router", {})
                if router.get("branch_flag") != branch:
                    errors.append(f"cinematic_hooks load_ending branch_flag mismatch with scene_registry ({hid})")

    # scenes.json encounter field ↔ story_encounters.json
    for s in scenes:
        enc_ref = s.get("encounter")
        if enc_ref and enc_ref not in enc_ids:
            errors.append(f"scenes.json unknown encounter: {enc_ref} ({s['scene_id']})")
        if enc_ref:
            enc_row = next((e for e in encounters if e["id"] == enc_ref), None)
            if enc_row and enc_row.get("scene_id") != s["scene_id"]:
                errors.append(
                    f"scenes.json encounter scene mismatch: {s['scene_id']} -> {enc_ref} "
                    f"(encounter scene_id {enc_row.get('scene_id')})"
                )

    # Tutorial flags declared in flags.json must be set somewhere in data
    tutorial_flags = {
        f["id"]
        for f in flag_defs.values()
        if f["id"].startswith("tutorial_") and f.get("type") == "bool"
    }
    emitted_tutorial: set[str] = set()
    for block in dialogue["scenes"]:
        for fl in block.get("on_complete", {}).get("set_flags", []) or []:
            if fl in tutorial_flags:
                emitted_tutorial.add(fl)
    for enc in encounters:
        for fl in enc.get("on_win", {}).get("set_flags", []) or []:
            if fl in tutorial_flags:
                emitted_tutorial.add(fl)
    for s in scenes:
        for fl in s.get("sets_flags", []) or []:
            if fl in tutorial_flags:
                emitted_tutorial.add(fl)
    for missing in sorted(tutorial_flags - emitted_tutorial):
        errors.append(f"tutorial flag never emitted in story data: {missing}")

    # Encounters reference valid scenes and enemies
    enemies_data = load("enemies/enemies.json")["enemies"]
    enemy_ids = {e["id"] for e in enemies_data}
    # Duplicate grant guard (DATA_ARCHITECTURE §8)
    encounter_grants: dict[str, str] = {}
    for enc in encounters:
        for item in enc.get("on_win", {}).get("grant_items", []) or []:
            encounter_grants[item] = enc["id"]

    for enc in encounters:
        if enc["scene_id"] not in scene_ids:
            errors.append(f"Encounter {enc['id']} unknown scene: {enc['scene_id']}")
        for eid in enc["enemies"]:
            if eid not in enemy_ids:
                errors.append(f"Encounter {enc['id']} unknown enemy: {eid}")
        for item in enc.get("on_win", {}).get("grant_items", []) or []:
            if item not in items:
                errors.append(f"Encounter {enc['id']} grants unknown item: {item}")
        for fl in enc.get("on_win", {}).get("set_flags", []) or []:
            if fl not in flags:
                errors.append(f"Encounter {enc['id']} on_win sets unknown flag: {fl}")
        for fl in enc.get("on_phase_trigger", {}).get("set_flags", []) or []:
            if fl not in flags:
                errors.append(f"Encounter {enc['id']} on_phase_trigger sets unknown flag: {fl}")
        hook = enc.get("cinematic_hook")
        if hook and hook not in hook_ids:
            errors.append(f"Encounter {enc['id']} unknown cinematic_hook: {hook}")
        for fl in enc.get("requires_flags", []) or []:
            if fl not in flags:
                errors.append(f"Encounter {enc['id']} requires unknown flag: {fl}")

    # Skills: enemy kits, AI weights, drops; party skills/unlocks/limits
    skill_ids = {s["id"] for s in load("skills/skills.json")["skills"]}
    for en in enemies_data:
        for sk in en.get("skills", []) or []:
            if sk not in skill_ids:
                errors.append(f"Enemy {en['id']} unknown skill: {sk}")
        ai = en.get("ai") or {}
        weight_lists = [ai.get("weights") or []] + [p.get("weights") or [] for p in ai.get("phases", []) or []]
        for weights in weight_lists:
            for w in weights:
                if w.get("skill_id") not in skill_ids:
                    errors.append(f"Enemy {en['id']} AI references unknown skill: {w.get('skill_id')}")
        for drop in en.get("rewards", {}).get("drops", []) or []:
            iid = drop.get("item_id")
            if iid not in items:
                errors.append(f"Enemy {en['id']} drops unknown item: {iid}")
            elif iid in encounter_grants:
                errors.append(
                    f"Enemy {en['id']} drops {iid} but encounter "
                    f"{encounter_grants[iid]} already grants it (DATA_ARCHITECTURE §8)"
                )
        # combat_barks: locales + skill keys must match enemy kit (DATA_ARCHITECTURE §18)
        barks = en.get("combat_barks") or {}
        enemy_skills = set(en.get("skills", []) or [])

        def check_bark_text(label: str, text_obj: object) -> None:
            if not isinstance(text_obj, dict):
                errors.append(f"Enemy {en['id']} combat_barks {label} must be a locale object")
                return
            for loc in REQUIRED_LOCALES:
                if not str(text_obj.get(loc, "")).strip():
                    errors.append(f"Enemy {en['id']} combat_barks {label} missing locale: {loc}")

        for key in ("battle_start", "on_defeat"):
            if key in barks:
                check_bark_text(key, barks[key])
        for sk_id, text_obj in (barks.get("skills") or {}).items():
            if sk_id not in enemy_skills:
                errors.append(f"Enemy {en['id']} combat_barks references skill not in kit: {sk_id}")
            if sk_id not in skill_ids:
                errors.append(f"Enemy {en['id']} combat_barks unknown skill: {sk_id}")
            check_bark_text(f"skills.{sk_id}", text_obj)
        phase_thresholds = {p.get("hp_threshold") for p in en.get("phases", []) or []}
        for phase_bark in barks.get("phases", []) or []:
            threshold = phase_bark.get("hp_threshold")
            if threshold is not None and phase_thresholds and threshold not in phase_thresholds:
                errors.append(
                    f"Enemy {en['id']} combat_barks phase hp_threshold {threshold} "
                    f"not in phases[]"
                )
            check_bark_text(f"phases[{threshold}]", phase_bark.get("text"))

    party = load("characters/party.json")["characters"]
    char_ids = {c["id"] for c in party}
    for ch in party:
        for sk in ch.get("starting_skills", []) or []:
            if sk not in skill_ids:
                errors.append(f"Character {ch['id']} unknown starting skill: {sk}")
        for unlock in ch.get("skill_unlocks", []) or []:
            if unlock.get("skill_id") not in skill_ids:
                errors.append(f"Character {ch['id']} unknown skill unlock: {unlock.get('skill_id')}")
        limit = ch.get("limit_skill")
        if limit and limit not in skill_ids:
            errors.append(f"Character {ch['id']} unknown limit skill: {limit}")

    # Quest count + stage completion flags
    if len(quests) != 5:
        errors.append(f"Expected 5 quests, found {len(quests)}")
    for q in quests:
        for stage in q.get("stages", []) or []:
            comp = stage.get("completion") or {}
            for fl in [comp.get("flag")] if comp.get("flag") else []:
                if fl not in flags:
                    errors.append(f"Quest {q['id']} stage {stage.get('id')} unknown flag: {fl}")
            for fl in comp.get("all_flags", []) or []:
                if fl not in flags:
                    errors.append(f"Quest {q['id']} stage {stage.get('id')} unknown flag: {fl}")
        for item in q.get("rewards", {}).get("items", []) or []:
            if item not in items:
                errors.append(f"Quest {q['id']} rewards unknown item: {item}")
            elif item in encounter_grants:
                errors.append(
                    f"Quest {q['id']} rewards item {item} but encounter "
                    f"{encounter_grants[item]} already grants it (DATA_ARCHITECTURE §8)"
                )

    # Shop items + scroll skills exist
    shop = load("shop/roku_shop.json")
    for entry in shop.get("inventory", []):
        if entry["item_id"] not in items:
            errors.append(f"Shop unknown item: {entry['item_id']}")
    for scroll in shop.get("scrolls", []) or []:
        if scroll.get("skill_id") not in skill_ids:
            errors.append(f"Shop scroll unknown skill: {scroll.get('skill_id')}")
        if scroll.get("character_id") not in char_ids:
            errors.append(f"Shop scroll unknown character: {scroll.get('character_id')}")

    # Achievements: trigger flags exist
    achievements = load("achievements/achievements.json")["achievements"]
    settings_schema = load("settings/settings_schema.json")
    allowed_settings = set(settings_schema.get("achievement_settings_keys", []))
    for ach in achievements:
        trig = ach.get("trigger") or {}
        setting_key = trig.get("setting")
        if setting_key and setting_key not in allowed_settings:
            errors.append(f"Achievement {ach['id']} unknown setting key: {setting_key}")
        if setting_key and setting_key not in settings_schema.get("fields", {}):
            errors.append(f"Achievement {ach['id']} setting not in schema: {setting_key}")
        for fl in [trig.get("flag")] if trig.get("flag") else []:
            if fl not in flags:
                errors.append(f"Achievement {ach['id']} unknown flag: {fl}")
        for fl in trig.get("all_flags", []) or []:
            if fl not in flags:
                errors.append(f"Achievement {ach['id']} unknown flag: {fl}")
        for fk, fv in (trig.get("flag_equals") or {}).items():
            if fk not in flags:
                errors.append(f"Achievement {ach['id']} unknown flag: {fk}")
            else:
                allowed = flag_defs[fk].get("values")
                if allowed and fv not in allowed:
                    errors.append(f"Achievement {ach['id']} invalid enum value: {fk}={fv}")

    # Every enum flag must be written somewhere (dialogue choice or scene)
    enum_flags = {f["id"] for f in flag_defs.values() if f.get("type") == "enum"}
    written_enums: set[str] = set()
    for block in dialogue["scenes"]:
        for choice in block.get("choices", []) or []:
            for fk in (choice.get("set_flags") or {}).keys():
                written_enums.add(fk)
    for missing in sorted(enum_flags - written_enums):
        errors.append(f"Enum flag never set by any dialogue choice: {missing}")

    # Items story_grant resolves to "new_game", a real scene_id, or a real lore entry
    lore_ids = {e["id"] for e in load("lore/lore_entries.json")["entries"]}
    for item in load("items/items.json")["items"]:
        grant = item.get("story_grant")
        if grant and grant != "new_game" and grant not in scene_ids and grant not in lore_ids:
            errors.append(
                f"Item {item['id']} story_grant is not 'new_game', a known scene_id, "
                f"or a known lore entry: {grant}"
            )

    # Locale completeness (en / ja / zh / zh-Hant) in inline i18n objects
    locale_files = [
        ("dialogue/chapter_01.json", dialogue),
        ("items/items.json", load("items/items.json")),
        ("lore/lore_entries.json", load("lore/lore_entries.json")),
        ("quests/main_quests.json", load("quests/main_quests.json")),
        ("shop/roku_shop.json", load("shop/roku_shop.json")),
    ]

    def check_locales(obj, path: str, rel: str) -> None:
        if isinstance(obj, dict):
            if "zh" in obj and isinstance(obj["zh"], str):
                hant = str(obj.get("zh-Hant", "")).strip()
                if not hant:
                    errors.append(f"{rel}: missing zh-Hant at {path}")
            for k, v in obj.items():
                check_locales(v, f"{path}.{k}" if path else k, rel)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                check_locales(item, f"{path}[{i}]", rel)

    for rel, data in locale_files:
        check_locales(data, "", rel)

    # Ending gallery — three philosophies, no best-ending badge (REPLAY_DESIGN.md §4)
    gallery_path = DATA / "narrative" / "ending_gallery.json"
    if gallery_path.is_file():
        gallery = load("narrative/ending_gallery.json")
        ending_enum = flag_defs.get("ending_chosen", {}).get("values") or []
        gallery_ids: set[str] = set()
        for entry in gallery.get("endings", []) or []:
            eid = entry.get("id", "?")
            gallery_ids.add(eid)
            chosen = entry.get("ending_chosen")
            if chosen not in ending_enum:
                errors.append(f"ending_gallery {eid} ending_chosen invalid: {chosen}")
            sid = entry.get("scene_id")
            if sid not in scene_ids:
                errors.append(f"ending_gallery {eid} unknown scene_id: {sid}")
            for field in ("title", "philosophy_blurb"):
                text_obj = entry.get(field)
                if not isinstance(text_obj, dict):
                    errors.append(f"ending_gallery {eid} missing {field}")
                    continue
                for loc in REQUIRED_LOCALES:
                    if not str(text_obj.get(loc, "")).strip():
                        errors.append(f"ending_gallery {eid} {field} missing locale: {loc}")
        if ending_enum and gallery_ids != set(ending_enum):
            errors.append(
                f"ending_gallery endings must cover ending_chosen values: "
                f"missing {set(ending_enum) - gallery_ids}, extra {gallery_ids - set(ending_enum)}"
            )
    else:
        errors.append("Missing game/data/narrative/ending_gallery.json")

    # combat_barks locale pass (inline i18n on enemy entries)
    for en in enemies_data:
        if en.get("combat_barks"):
            check_locales(en["combat_barks"], en["id"], "enemies/enemies.json")

    # translations.csv — required keys for skills, enemies, combat
    csv_path = ROOT / "game" / "locale" / "translations.csv"
    if not csv_path.is_file():
        errors.append("Missing game/locale/translations.csv")
    else:
        with open(csv_path, encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            rows = {row["keys"]: row for row in reader if row.get("keys")}
        required_locales = ("en", "ja", "zh", "zh-Hant")

        def require_csv_key(key: str) -> None:
            if key not in rows:
                errors.append(f"translations.csv missing key: {key}")
                return
            for loc in required_locales:
                if not str(rows[key].get(loc, "")).strip():
                    errors.append(f"translations.csv empty {loc} for key: {key}")

        for skill in load("skills/skills.json")["skills"]:
            sid = skill["id"]
            require_csv_key(f"skill.{sid}.name")
            require_csv_key(f"skill.{sid}.desc")
        for enemy in load("enemies/enemies.json")["enemies"]:
            require_csv_key(f"enemy.{enemy['id']}.name")
        for combat_key in (
            "action_attack",
            "action_skill",
            "damage_dealt",
            "heal",
            "victory",
            "defeat",
        ):
            require_csv_key(f"combat.{combat_key}")
        for status in ("poison", "regen", "stun", "def_up", "def_down"):
            require_csv_key(f"status.{status}")

    # Marketing trailer locale completeness
    trailer_locales_path = ROOT / "steam" / "trailer_locales.json"
    if trailer_locales_path.is_file():
        trailer_data = json.loads(trailer_locales_path.read_text(encoding="utf-8"))
        trailer_locales = trailer_data.get("locales", [])
        for i, seg in enumerate(trailer_data.get("segments", [])):
            text_map = seg.get("text", {})
            for loc in trailer_locales:
                if loc not in text_map:
                    errors.append(f"trailer_locales.json segment {i}: missing locale {loc}")

    if errors:
        print("STORY DATA VALIDATION FAILED", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"OK — {len(scene_ids)} scenes, {len(dialogue_ids)} dialogue blocks, {len(quests)} quests, {len(encounters)} encounters, {len(hooks)} cinematic hooks, {len(vo_clip_ids)} vo clips")
    return 0


if __name__ == "__main__":
    sys.exit(main())
