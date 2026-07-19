#!/usr/bin/env python3
"""Markdown style lint — docs/technical/MARKDOWN_STYLE.md."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SKIP_DIR_PARTS = (
    "alignment_audit_reports",
    "artifacts",
)
SKIP_FILES = {
    "docs/compliance/COMPLIANCE_REPORT.md",
}

LINK_RE = re.compile(r"\]\(([^)]+)\)")
SKIP_LINK_PREFIXES = ("http://", "https://", "#", "mailto:")
SETEXT_RE = re.compile(r"^(=+|-+)\s*$")


def collect_markdown_files() -> list[Path]:
    files: list[Path] = []
    for pattern in ("docs/**/*.md", "AGENTS.md", "game/data/README.md", ".github/**/*.md"):
        files.extend(ROOT.glob(pattern))
    out: list[Path] = []
    seen: set[Path] = set()
    for path in sorted(files):
        rel = path.relative_to(ROOT).as_posix()
        if rel in SKIP_FILES:
            continue
        if any(part in path.parts for part in SKIP_DIR_PARTS):
            continue
        if "deprecated" in path.parts:
            continue
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        out.append(path)
    return out


def strip_fenced_code(raw: str) -> str:
    """Remove fenced code blocks so language samples may use tabs."""
    parts = re.split(r"(?ms)^```.*?^```\s*$", raw)
    return "\n".join(parts)


def check_file(path: Path, errors: list[str]) -> None:
    rel = path.relative_to(ROOT).as_posix()
    raw = path.read_text(encoding="utf-8")
    prose = strip_fenced_code(raw)

    if not raw.endswith("\n"):
        errors.append(f"{rel}: missing trailing newline")

    if "\t" in prose:
        errors.append(f"{rel}: tab character forbidden in prose — use spaces")

    lines = raw.splitlines()
    for index, line in enumerate(lines, 1):
        if SETEXT_RE.match(line) and index >= 2 and lines[index - 2].strip():
            errors.append(f"{rel}:{index}: setext heading underline — use ATX # headings")
            break

    for match in LINK_RE.finditer(raw):
        target = match.group(1).split("#")[0].strip()
        if not target or target.startswith(SKIP_LINK_PREFIXES):
            continue
        resolved = (path.parent / target).resolve()
        if not resolved.exists():
            errors.append(f"{rel}: broken relative link → {target}")


def main() -> int:
    files = collect_markdown_files()
    if not files:
        print("[SKIP] no markdown files found")
        return 0

    errors: list[str] = []
    for path in files:
        check_file(path, errors)

    if errors:
        print(f"[FAIL] L1_markdown_style — {len(errors)} issue(s):")
        for err in errors[:40]:
            print(f"  - {err}")
        if len(errors) > 40:
            print(f"  … and {len(errors) - 40} more")
        return 1

    print(f"[PASS] L1_markdown_style — {len(files)} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
