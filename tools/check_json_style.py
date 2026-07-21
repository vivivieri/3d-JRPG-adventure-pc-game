#!/usr/bin/env python3
"""JSON format/style lint for game/data/**/*.json — JSON_DATA_STYLE.md."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "game" / "data"

# Config JSON outside game/data — format-only (no key naming rules).
EXTRA_JSON_GLOBS = (
    ".cursor/environment.json",
    ".cursor/mcp.json.example",
    "steam/trailer_locales.json",
)

LOCALE_KEYS = frozenset({"en", "ja", "zh", "zh-Hant", "_comment"})
KEY_OK = re.compile(
    r"^("
    r"[a-z][a-z0-9]*(_[a-z0-9]+)*|"
    r"SC-\d+[a-z]?|"
    r"L[0-9]_[a-z0-9_]+|"
    r"M[0-9]_[a-z0-9_]+|"
    r"INT-[A-Z0-9][A-Z0-9-]*|"
    r"E2E-[A-Z0-9][A-Z0-9-]*|"
    r"P[0-9]+-[0-9]+|"
    r"[IVX]+|"
    r"\d+|"
    r"label_[a-zA-Z0-9-]+"
    r")$"
)


def key_allowed(key: str) -> bool:
    return key in LOCALE_KEYS or bool(KEY_OK.match(key))


def check_keys(obj: object, path: str, errors: list[str]) -> None:
    if isinstance(obj, dict):
        for key, value in obj.items():
            if not key_allowed(key):
                errors.append(f"{path}: key '{key}' does not match JSON_DATA_STYLE naming")
            check_keys(value, f"{path}.{key}", errors)
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            check_keys(value, f"{path}[{index}]", errors)


def check_format(path: Path, errors: list[str]) -> None:
    raw = path.read_text(encoding="utf-8")
    if not raw.endswith("\n"):
        errors.append(f"{path}: missing trailing newline")
    if "\t" in raw:
        errors.append(f"{path}: tab character forbidden — use 2-space indent")
    for line_no, line in enumerate(raw.splitlines(), 1):
        if not line or not line.startswith(" "):
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent % 2 != 0:
            errors.append(f"{path}:{line_no}: indent must be multiples of 2 spaces")
            break
    try:
        json.loads(raw)
    except json.JSONDecodeError as exc:
        errors.append(f"{path}: invalid JSON — {exc}")


def collect_json_files() -> tuple[list[Path], list[Path]]:
    """Return (game/data files, extra config files)."""
    data_files: list[Path] = []
    if DATA.is_dir():
        data_files = sorted(DATA.rglob("*.json"))
    extra_files: list[Path] = []
    for rel in EXTRA_JSON_GLOBS:
        path = ROOT / rel
        if path.is_file():
            extra_files.append(path)
    return data_files, extra_files


def main() -> int:
    data_files, extra_files = collect_json_files()
    if not data_files and not extra_files:
        print("[SKIP] no JSON files to lint")
        return 0

    errors: list[str] = []
    for path in data_files + extra_files:
        check_format(path, errors)
        rel = str(path.relative_to(ROOT))
        if any(rel in err and "invalid JSON" in err for err in errors):
            continue
        if path in data_files:
            data = json.loads(path.read_text(encoding="utf-8"))
            check_keys(data, rel, errors)

    if errors:
        print(f"[FAIL] L1_json_style — {len(errors)} issue(s):", file=sys.stderr)
        for err in errors[:40]:
            print(f"  - {err}", file=sys.stderr)
        if len(errors) > 40:
            print(f"  … and {len(errors) - 40} more", file=sys.stderr)
        return 1

    detail = f"{len(data_files)} game/data + {len(extra_files)} config" if extra_files else f"{len(data_files)}"
    print(f"[PASS] L1_json_style — {detail} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
