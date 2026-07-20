#!/usr/bin/env python3
"""Error-handling lint — docs/technical/ERROR_HANDLING.md."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
GAME_SCRIPTS = ROOT / "game" / "scripts"

BASH_FORBIDDEN_RE = re.compile(r"&&\s+.+\s+\|\|\s+fail\b|&&\s+ok\b.+\|\|\s+fail\b")
PY_BARE_EXCEPT_RE = re.compile(r"^\s*except\s*:\s*$", re.MULTILINE)
PY_SILENT_EXCEPT_PASS_RE = re.compile(
    r"except\s+Exception[^:]*:\s*\n\s+pass\b",
    re.MULTILINE,
)
GD_EMPTY_PUSH_ERROR_RE = re.compile(r'push_error\s*\(\s*["\'][\s]*["\']\s*\)')
GD_BARE_PUSH_ERROR_RE = re.compile(r"push_error\s*\(\s*\)")
GD_RES_PATH_IN_PRINT_RE = re.compile(r'print\s*\([^)]*res://')


def run_ruff_error_rules() -> list[str]:
    proc = subprocess.run(
        ["ruff", "check", "tools/", "--select", "E722,S110,S112"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if proc.returncode == 0:
        return []
    return [line for line in proc.stdout.splitlines() if line.strip()]


def check_python_files(errors: list[str]) -> None:
    for path in sorted(TOOLS.glob("*.py")):
        rel = path.relative_to(ROOT).as_posix()
        raw = path.read_text(encoding="utf-8")
        if PY_BARE_EXCEPT_RE.search(raw):
            errors.append(f"{rel}: bare except — catch a specific exception type")
        if PY_SILENT_EXCEPT_PASS_RE.search(raw):
            errors.append(f"{rel}: silent except Exception: pass — log or re-raise")


def check_bash_scripts(errors: list[str]) -> None:
    for path in sorted(TOOLS.glob("*.sh")):
        rel = path.relative_to(ROOT).as_posix()
        raw = path.read_text(encoding="utf-8")
        head = "\n".join(raw.splitlines()[:20])
        if path.name.startswith(("check_", "run_")) and "set -euo pipefail" not in head:
            errors.append(f"{rel}: gate/run script must set -euo pipefail in first 20 lines")
        for line_no, line in enumerate(raw.splitlines(), 1):
            if BASH_FORBIDDEN_RE.search(line):
                errors.append(
                    f"{rel}:{line_no}: use if/else instead of && … || fail (ERROR_HANDLING.md §3.2)"
                )


def check_gdscript_files(errors: list[str]) -> int:
    if not GAME_SCRIPTS.is_dir():
        return 0

    checked = 0
    for path in sorted(GAME_SCRIPTS.rglob("*.gd")):
        rel = path.relative_to(ROOT).as_posix()
        raw = path.read_text(encoding="utf-8")
        checked += 1
        if GD_EMPTY_PUSH_ERROR_RE.search(raw) or GD_BARE_PUSH_ERROR_RE.search(raw):
            errors.append(f"{rel}: push_error requires a non-empty actionable message")
        if GD_RES_PATH_IN_PRINT_RE.search(raw):
            errors.append(f"{rel}: do not print res:// paths — player-facing leak risk")
        for match in re.finditer(r"push_error\s*\([^)]+\)", raw):
            start = match.end()
            window = raw[start : start + 240]
            lines = [ln.strip() for ln in window.splitlines()[:6] if ln.strip() and not ln.strip().startswith("#")]
            if not lines:
                continue
            first = lines[0]
            if first.startswith("return") or first.startswith("assert"):
                continue
            if first.startswith("await "):
                continue
            # Boot/load helpers must not continue after push_error.
            context_start = max(0, raw.rfind("\nfunc ", 0, match.start()))
            context = raw[context_start:match.start()]
            if re.search(r"\nfunc\s+(_ready|load_|boot_|_load)\b", context):
                errors.append(
                    f"{rel}: push_error in boot/load path should be followed by return "
                    f"(near: {match.group(0)[:60]})"
                )
    return checked


def main() -> int:
    errors: list[str] = []
    errors.extend(run_ruff_error_rules())
    check_python_files(errors)
    check_bash_scripts(errors)
    gd_count = check_gdscript_files(errors)

    if errors:
        print(f"[FAIL] L1_error_handling — {len(errors)} issue(s):")
        for err in errors[:40]:
            print(f"  - {err}")
        if len(errors) > 40:
            print(f"  … and {len(errors) - 40} more")
        return 1

    parts = ["tools/*.py", "tools/*.sh"]
    if gd_count:
        parts.append(f"{gd_count} GDScript file(s)")
    print(f"[PASS] L1_error_handling — {', '.join(parts)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
