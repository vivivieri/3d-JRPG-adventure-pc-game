#!/usr/bin/env python3
"""Stamp missing phase: frontmatter on active docs using path heuristics."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

# First matching rule wins. phase list as ints.
RULES: list[tuple[re.Pattern[str], list[int]]] = [
    (re.compile(r"docs/ops/ci-cd/STEAM"), [8]),
    (re.compile(r"docs/ops/ci-cd/CD"), [8]),
    (re.compile(r"docs/ops/workflow/MILESTONES"), [0, 1, 2, 3, 4, 5, 6, 7, 8]),
    (re.compile(r"docs/design/art/model_qa/"), [5]),
    (re.compile(r"docs/design/art/MODEL_QA"), [5]),
    (re.compile(r"docs/design/art/rendering/"), [1, 5]),
    (re.compile(r"docs/design/art/RENDERING"), [1, 5]),
    (re.compile(r"docs/design/art/items/"), [2, 5]),
    (re.compile(r"docs/design/art/ITEMS"), [2, 5]),
    (re.compile(r"docs/design/art/VISUAL_QA"), [1, 5]),
    (re.compile(r"docs/design/art/ART_AUTOMATION"), [5]),
    (re.compile(r"docs/design/art/ART_DIRECTION"), [1, 5]),
    (re.compile(r"docs/design/art/CHARACTER"), [5]),
    (re.compile(r"docs/design/art/characters/"), [5]),
    (re.compile(r"docs/design/world/ENVIRONMENT"), [1, 5]),
    (re.compile(r"docs/design/gameplay/COMBAT"), [4]),
    (re.compile(r"docs/design/art/COMBAT"), [4]),
    (re.compile(r"docs/design/gameplay/SKILLS"), [4]),
    (re.compile(r"docs/design/gameplay/PROGRESSION"), [4]),
    (re.compile(r"docs/design/vision/VO_"), [3, 6]),
    (re.compile(r"docs/design/vision/narrative/"), [3, 6]),
    (re.compile(r"docs/design/vision/NARRATIVE"), [3, 6]),
    (re.compile(r"docs/design/vision/STORYBOARD"), [3, 6]),
    (re.compile(r"docs/design/vision/ENDING"), [6]),
    (re.compile(r"docs/design/audio/"), [1, 5]),
    (re.compile(r"docs/ops/agents/cloud_setup/"), [0, 1]),
    (re.compile(r"docs/ops/agents/CLOUD_AGENT"), [0, 1]),
    (re.compile(r"docs/ops/workflow/implementation/phase_"), []),  # set per-file below
]


def _has_phase(block: str) -> bool:
    return bool(re.search(r"(?m)^phase:\s*", block))


def _insert_phase(text: str, phases: list[int]) -> str | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    block = text[4:end]
    if _has_phase(block):
        return None
    phase_line = f"phase: [{', '.join(str(p) for p in phases)}]\n"
    # insert after audience or type
    new_block = block
    if re.search(r"(?m)^audience:", block):
        new_block = re.sub(r"(?m)^(audience:.*)$", r"\1\n" + phase_line.rstrip(), block, count=1)
        if new_block == block:
            new_block = block + "\n" + phase_line.rstrip()
    else:
        new_block = block.rstrip() + "\n" + phase_line.rstrip()
    return text[:4] + new_block + text[end:]


def main() -> int:
    updated = 0
    for md in sorted(DOCS.rglob("*.md")):
        rel = md.relative_to(ROOT).as_posix()
        if any(
            p in rel
            for p in (
                "/archive/",
                "/_meta/",
                "/briefs/",
                "/audio_sheets/",
                "/sprints/",
                "/automation_prompts/",
            )
        ):
            continue
        if md.name in {"README.md", "BOOT.md"}:
            continue
        text = md.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        # per-phase implementation packs
        m = re.search(r"implementation/phase_(\d+)\.md$", rel)
        if m:
            phases = [int(m.group(1))]
        else:
            phases = None
            for pattern, plist in RULES:
                if pattern.search(rel):
                    phases = plist
                    break
        if not phases:
            continue
        new_text = _insert_phase(text, phases)
        if new_text is None:
            continue
        md.write_text(new_text, encoding="utf-8")
        print(f"stamped phase {phases} → {rel}")
        updated += 1
    print(f"done — stamped {updated} docs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
