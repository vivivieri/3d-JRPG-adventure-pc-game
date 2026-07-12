#!/usr/bin/env python3
"""Enforce CODE_BASE_CLASS_RULES — no rogue extends (docs/CODE_BASE_CLASS_RULES.md)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "game/data/code/base_classes.json"
SCRIPTS = ROOT / "game/scripts"
SCENES = ROOT / "game/scenes"

EXTENDS_RE = re.compile(r"^\s*extends\s+([A-Za-z0-9_]+)", re.MULTILINE)


def res_to_disk(res_path: str) -> Path:
    rel = res_path.removeprefix("res://")
    return ROOT / "game" / rel


def load_registry() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def native_extends_allowed(path: Path, native: str, registry: dict) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    for base in registry.get("bases", []):
        disk = res_to_disk(base["path"]).as_posix()
        if rel == disk and base.get("extends") == native:
            return True
    return False


def scan_gd(path: Path, registry: dict) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    for match in EXTENDS_RE.finditer(text):
        native = match.group(1)
        if native in ("RefCounted", "Resource", "Node2D", "Control", "EditorScript", "EditorScenePostImport"):
            continue
        if native in ("CharacterBody3D", "Area3D", "Node", "Node3D"):
            if not native_extends_allowed(path, native, registry):
                rel = path.relative_to(ROOT).as_posix()
                errors.append(
                    f"{rel} extends {native} directly — use a base class from base_classes.json"
                )
    return errors


def main() -> int:
    print("==> Base class compliance (CODE_BASE_CLASS_RULES.md)")
    print("")

    if not REGISTRY.is_file():
        print(f"[FAIL] missing {REGISTRY}", file=sys.stderr)
        return 1

    registry = load_registry()
    if not SCRIPTS.is_dir():
        print("[SKIP] game/scripts/ not present yet (docs-only baseline)")
        return 2

    errors: list[str] = []
    for gd in sorted(SCRIPTS.rglob("*.gd")):
        errors.extend(scan_gd(gd, registry))
    if SCENES.is_dir():
        for gd in sorted(SCENES.rglob("*.gd")):
            errors.extend(scan_gd(gd, registry))

    if errors:
        for e in errors:
            print(f"[FAIL] {e}")
        return 1

    print("[OK]   no forbidden native extends outside registered base classes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
