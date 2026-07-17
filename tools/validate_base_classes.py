#!/usr/bin/env python3
"""Validate game/data/code/base_classes.json (docs/technical/CODE_BASE_CLASS_RULES.md)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "game/data/code/base_classes.json"


def res_to_disk(res_path: str) -> Path:
    return ROOT / "game" / res_path.removeprefix("res://")


def main() -> int:
    if not PATH.is_file():
        print(f"Missing {PATH}", file=sys.stderr)
        return 1

    data = json.loads(PATH.read_text(encoding="utf-8"))
    errors: list[str] = []
    bases = data.get("bases", [])
    if not bases:
        errors.append("bases must be non-empty")

    ids: set[str] = set()
    base_ids: set[str] = set()
    for b in bases:
        if "id" not in b or "path" not in b:
            errors.append("each base needs id and path")
            break
        if b["id"] in ids:
            errors.append(f"duplicate base id: {b['id']}")
        ids.add(b["id"])
        base_ids.add(b["id"])
        if b.get("agent_rule") not in ("extend_only", "architect_only"):
            errors.append(f"invalid agent_rule for {b.get('id')}")

    comps = data.get("component_scenes", [])
    if not comps:
        errors.append("component_scenes must be non-empty")

    game_branch = (ROOT / "game/project.godot").is_file()
    active_phase = 0
    phases_path = ROOT / "game/data/qa/sprint_phases.json"
    if phases_path.is_file():
        active_phase = int(json.loads(phases_path.read_text(encoding="utf-8")).get("active_phase", 0))
    require_impl_on_disk = game_branch and active_phase >= 2

    for comp in comps:
        script = comp.get("script")
        if script and script not in base_ids:
            errors.append(
                f"component {comp.get('id')} references script {script} not in bases[]"
            )
        comp_path = comp.get("path")
        if comp_path and require_impl_on_disk:
            disk = res_to_disk(comp_path)
            if not disk.is_file():
                errors.append(f"component scene missing on disk: {comp_path}")

    for b in bases:
        if require_impl_on_disk:
            disk = res_to_disk(b["path"])
            if not disk.is_file():
                errors.append(f"base class path missing on disk: {b['path']}")
        if b.get("python_reference"):
            if not b.get("public_api"):
                errors.append(f"{b.get('id')}: public_api required when python_reference is set")
            py_path = ROOT / b["python_reference"]
            if not py_path.is_file():
                errors.append(f"{b.get('id')}: missing python_reference {b['python_reference']}")

    for own in data.get("architect_owns", []):
        if not own.startswith("res://"):
            errors.append(f"architect_owns entry must be res:// path: {own}")

    if errors:
        print("BASE CLASSES VALIDATION FAILED", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"OK — {len(bases)} bases, {len(comps)} component scenes", end="")
    if game_branch and active_phase < 2:
        print(" (impl on-disk checks deferred until phase 2+)")
    else:
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
