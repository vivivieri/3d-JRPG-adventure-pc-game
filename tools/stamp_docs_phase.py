#!/usr/bin/env python3
"""Stamp phase: frontmatter on active docs lacking it (heuristic by path)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

SKIP_PREFIXES = (
    "archive/",
    "_meta/",
    "briefs/",
    "design/audio/audio_sheets/",
    "ops/sprints/",
    "ops/agents/automation_prompts/",
)
SKIP_NAMES = {"README.md", "BOOT.md"}

# path substring → phase list
RULES: list[tuple[str, list[int]]] = [
    ("design/art/", [1, 5]),
    ("design/world/", [1, 5]),
    ("design/gameplay/", [2, 3]),
    ("design/ui/", [1, 5]),
    ("design/audio/", [1, 5]),
    ("design/vision/", [1, 6]),
    ("engineering/technical/", [1, 2, 3, 4, 5, 6]),
    ("ops/qa/", [1, 6]),
    ("ops/ci-cd/", [6, 8]),
    ("ops/workflow/", [0, 1, 8]),
    ("ops/agents/", [0, 1]),
    ("ops/cheat-sheets/", [0, 1]),
]


def infer_phase(rel: str) -> list[int]:
    for needle, phases in RULES:
        if rel.startswith(needle):
            return phases
    return [1]


def main() -> int:
    stamped = 0
    for md in sorted(DOCS.rglob("*.md")):
        rel = md.relative_to(DOCS).as_posix()
        if md.name in SKIP_NAMES or any(rel.startswith(p) for p in SKIP_PREFIXES):
            continue
        text = md.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        end = text.find("\n---\n", 4)
        if end < 0:
            continue
        block = text[4:end]
        if re.search(r"(?m)^phase:", block):
            continue
        phases = infer_phase(rel)
        phase_line = f"phase: [{', '.join(str(p) for p in phases)}]"
        # insert after audience or type line
        lines = block.splitlines()
        out: list[str] = []
        inserted = False
        for line in lines:
            out.append(line)
            if not inserted and (
                line.startswith("audience:") or line.startswith("type:")
            ):
                out.append(phase_line)
                inserted = True
        if not inserted:
            out.append(phase_line)
        new_block = "\n".join(out)
        md.write_text(f"---\n{new_block}\n---\n{text[end + 5 :]}", encoding="utf-8")
        stamped += 1
        print(f"phase {phases} → {rel}")
    print(f"stamped {stamped} docs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
