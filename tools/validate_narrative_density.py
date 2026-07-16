#!/usr/bin/env python3
"""Validate narrative pattern density against ship budgets (L0 gate).

Prevents over-application of combat barks, quiet beats, flag callbacks, and
inspect lines in a 2–3 hour game. Policy: docs/NARRATIVE_DENSITY.md
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "game" / "data"


def load(rel: str) -> dict | list:
    with open(DATA / rel, encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    errors: list[str] = []
    policy = load("narrative/narrative_density.json")
    budgets = policy["budgets"]
    scenes = {s["scene_id"]: s for s in load("story/scenes.json")["scenes"]}
    dialogue = {b["scene_id"]: b for b in load("dialogue/chapter_01.json")["scenes"]}
    enemies = {e["id"]: e for e in load("enemies/enemies.json")["enemies"]}

    # --- combat_barks ---
    cb = budgets["combat_barks"]
    require_tiers = set(cb["require_for_tiers"])
    forbid_bs_tiers = set(cb["forbid_battle_start_tiers"])
    bs_allow = set(cb["battle_start_allowlist_enemy_ids"])
    tutorial_ids = set(cb.get("tutorial_enemy_ids", []))
    bark_count = 0

    for eid, enemy in enemies.items():
        barks = enemy.get("combat_barks")
        tier = enemy.get("tier", "normal")
        if barks:
            bark_count += 1
            skills = barks.get("skills") or {}
            if len(skills) > cb["max_skill_barks_per_enemy"]:
                errors.append(
                    f"Enemy {eid}: {len(skills)} skill barks exceeds max "
                    f"{cb['max_skill_barks_per_enemy']}"
                )
            if barks.get("battle_start"):
                if tier in forbid_bs_tiers and eid not in bs_allow:
                    errors.append(
                        f"Enemy {eid} (tier {tier}) has battle_start bark — "
                        f"forbidden except allowlist {sorted(bs_allow)}"
                    )
            if eid in tutorial_ids and barks.get("battle_start"):
                errors.append(f"Tutorial enemy {eid} must not have battle_start bark")
        elif tier in require_tiers:
            errors.append(f"Enemy {eid} (tier {tier}) missing combat_barks")

    if bark_count > cb["max_enemies_with_barks"]:
        errors.append(
            f"{bark_count} enemies have combat_barks; max is {cb['max_enemies_with_barks']}"
        )

    # --- quiet beats ---
    qb = budgets["quiet_beats"]
    exclude_types = set(qb["exclude_scene_types"])
    quiet_by_act: Counter[str] = Counter()
    quiet_by_zone: Counter[str] = Counter()
    quiet_total = 0

    for sid, block in dialogue.items():
        meta = scenes.get(sid)
        if not meta or meta.get("type") in exclude_types:
            continue
        for line in block.get("lines", []) or []:
            if (
                line.get("speaker") == qb["speaker"]
                and line.get("emotion") == qb["emotion"]
            ):
                act = meta.get("act", "?")
                zone = meta.get("zone") or "none"
                quiet_by_act[act] += 1
                quiet_by_zone[zone] += 1
                quiet_total += 1

    for act, limit in qb["max_per_act"].items():
        count = quiet_by_act.get(act, 0)
        if count > limit:
            errors.append(f"Act {act}: {count} quiet beats exceeds max {limit}")

    if quiet_total > qb["max_total"]:
        errors.append(f"{quiet_total} quiet beats total exceeds max {qb['max_total']}")

    # --- flag callbacks ---
    fc = budgets["flag_callbacks"]
    callbacks_per_scene: Counter[str] = Counter()
    flag_uses: Counter[str] = Counter()

    for sid, block in dialogue.items():
        for line in block.get("lines", []) or []:
            req = line.get("requires_flags") or {}
            if isinstance(req, dict) and req:
                callbacks_per_scene[sid] += 1
                for fk in req:
                    flag_uses[fk] += 1

    for sid, count in callbacks_per_scene.items():
        if count > fc["max_lines_per_scene"]:
            errors.append(
                f"Scene {sid}: {count} flag-callback lines exceeds max "
                f"{fc['max_lines_per_scene']}"
            )

    for fk, count in flag_uses.items():
        if count > fc["max_reuse_per_flag"]:
            errors.append(
                f"Flag {fk} used in {count} callback lines; max reuse is "
                f"{fc['max_reuse_per_flag']}"
            )

    # --- inspect scenes ---
    ins = budgets["inspect_scenes"]
    inspect_by_zone: Counter[str] = Counter()

    for sid, meta in scenes.items():
        if meta.get("type") != "inspect":
            continue
        zone = meta.get("zone") or "none"
        inspect_by_zone[zone] += 1
        block = dialogue.get(sid)
        if not block:
            errors.append(f"Inspect scene {sid} has no dialogue block")
            continue
        lines = block.get("lines", []) or []
        if len(lines) > ins["max_total_lines"]:
            errors.append(
                f"Inspect {sid}: {len(lines)} lines exceeds max {ins['max_total_lines']}"
            )
        pc_speakers = {"urashima", "yuzu", "roku", "otohime", "shore_wraith", "tide_keeper"}
        narr_before_pc = 0
        for line in lines:
            if line.get("speaker") in pc_speakers:
                break
            if line.get("speaker") == "narrator":
                narr_before_pc += 1
        if narr_before_pc < ins["min_narrator_lines_before_pc"]:
            errors.append(
                f"Inspect {sid}: need >= {ins['min_narrator_lines_before_pc']} narrator "
                f"lines before PC speaks (village-life pattern)"
            )

    # --- choice subtext_warm ---
    cf = budgets["choice_flavor"]
    allowed = set(cf["subtext_warm_allowed_scenes"])

    for sid, block in dialogue.items():
        warm_count = 0
        for choice in block.get("choices", []) or []:
            if choice.get("subtext_warm"):
                warm_count += 1
                if sid not in allowed:
                    errors.append(f"Scene {sid}: subtext_warm only allowed in {sorted(allowed)}")
        if warm_count > cf["max_subtext_warm_per_scene"]:
            errors.append(
                f"Scene {sid}: {warm_count} subtext_warm choices exceeds max "
                f"{cf['max_subtext_warm_per_scene']}"
            )

    # --- zone caps ---
    for zone, caps in budgets["zones"].items():
        if inspect_by_zone.get(zone, 0) > caps["max_inspect_scenes"]:
            errors.append(
                f"Zone {zone}: {inspect_by_zone[zone]} inspect scenes exceeds max "
                f"{caps['max_inspect_scenes']}"
            )
        if quiet_by_zone.get(zone, 0) > caps["max_quiet_beats"]:
            errors.append(
                f"Zone {zone}: {quiet_by_zone[zone]} quiet beats exceeds max "
                f"{caps['max_quiet_beats']}"
            )

    if errors:
        print("NARRATIVE DENSITY VALIDATION FAILED", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        print("\nPolicy: docs/NARRATIVE_DENSITY.md", file=sys.stderr)
        return 1

    print(
        f"OK — narrative density within budget "
        f"({bark_count} bark enemies, {quiet_total} quiet beats, "
        f"{sum(inspect_by_zone.values())} inspect scenes)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
