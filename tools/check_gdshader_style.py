#!/usr/bin/env python3
"""Godot shader style lint — docs/technical/SHADER_STYLE.md."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SEARCH_DIRS = (
    ROOT / "game" / "shaders",
    ROOT / "tools" / "godot_templates" / "shaders",
)

SNAKE_RE = re.compile(r"^[a-z][a-z0-9]*(_[a-z0-9]+)*\.gdshader$")


def collect_shaders() -> list[Path]:
    files: list[Path] = []
    for base in SEARCH_DIRS:
        if base.is_dir():
            files.extend(sorted(base.rglob("*.gdshader")))
    return files


def check_shader(path: Path, errors: list[str]) -> None:
    rel = path.relative_to(ROOT).as_posix()
    raw = path.read_text(encoding="utf-8")

    if not raw.endswith("\n"):
        errors.append(f"{rel}: missing trailing newline")

    if not SNAKE_RE.match(path.name):
        errors.append(f"{rel}: filename must be snake_case.gdshader")

    if not re.search(r"(?m)^shader_type\s+\w+\s*;", raw):
        errors.append(f"{rel}: missing shader_type declaration")

    if "shader_type spatial" in raw and "diffuse_toon" not in raw:
        errors.append(f"{rel}: spatial shader must include diffuse_toon in render_mode")

    if "METALLIC" in raw and "METALLIC = 0.0" not in raw.replace(" ", ""):
        # Allow if METALLIC assigned from uniform — warn on glossy defaults only
        if re.search(r"METALLIC\s*=\s*[^0]", raw) and "METALLIC = 0" not in raw:
            errors.append(f"{rel}: ship NPR shaders should set METALLIC = 0.0")


def main() -> int:
    files = collect_shaders()
    if not files:
        print("[SKIP] no .gdshader files found")
        return 0

    errors: list[str] = []
    for path in files:
        check_shader(path, errors)

    if errors:
        print(f"[FAIL] L1_gdshader_style — {len(errors)} issue(s):")
        for err in errors:
            print(f"  - {err}")
        return 1

    print(f"[PASS] L1_gdshader_style — {len(files)} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
