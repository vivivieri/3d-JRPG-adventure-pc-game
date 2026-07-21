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
HEADING_RE = re.compile(r"^(#{1,6})\s+\S")


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


def check_heading_levels(rel: str, lines: list[str], errors: list[str]) -> None:
    last_line = 0
    prev_level = 0
    for index, line in enumerate(lines, 1):
        match = HEADING_RE.match(line)
        if not match:
            continue
        level = len(match.group(1))
        if prev_level and level > prev_level + 1:
            gap = index - last_line - 1
            # Common doc scaffold: H1 title → version blurb → ### first section.
            allow_h1_h3 = prev_level == 1 and level == 3 and gap >= 2
            if not allow_h1_h3:
                errors.append(
                    f"{rel}:{index}: heading level jumps from H{prev_level} to H{level} — "
                    "increment by one (MARKDOWN_STYLE.md §3)"
                )
        last_line = index
        prev_level = 1 if level == 1 else level


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
        if line != line.rstrip():
            errors.append(f"{rel}:{index}: trailing whitespace")
        if SETEXT_RE.match(line) and index >= 2 and lines[index - 2].strip():
            errors.append(f"{rel}:{index}: setext heading underline — use ATX # headings")
            break

    check_heading_levels(rel, lines, errors)

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
        print(f"[FAIL] L1_markdown_style — {len(errors)} issue(s):", file=sys.stderr)
        for err in errors[:40]:
            print(f"  - {err}", file=sys.stderr)
        if len(errors) > 40:
            print(f"  … and {len(errors) - 40} more", file=sys.stderr)
        return 1

    print(f"[PASS] L1_markdown_style — {len(files)} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
