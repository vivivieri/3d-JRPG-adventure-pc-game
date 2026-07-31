#!/usr/bin/env python3
"""Stamp missing summary: frontmatter from the first prose line after the title."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

SKIP = (
    "archive/",
    "_meta/",
    "briefs/",
    "design/audio/audio_sheets/",
    "ops/sprints/",
    "ops/agents/automation_prompts/",
)


def first_summary(body: str) -> str | None:
    lines = body.splitlines()
    # skip title + blanks + tables/code
    started = False
    for line in lines:
        if line.startswith("# "):
            started = True
            continue
        if not started:
            continue
        s = line.strip()
        if not s or s.startswith("#") or s.startswith("|") or s.startswith("```"):
            continue
        if s.startswith("**Hub**") or s.startswith("**Version**") or s.startswith("**Authority**"):
            continue
        s = re.sub(r"^\*\*[^*]+\*\*\s*—?\s*", "", s)
        s = re.sub(r"\s+", " ", s).strip().strip('"')
        if len(s) < 20:
            continue
        return s[:160]
    return None


def main() -> int:
    n = 0
    for md in sorted(DOCS.rglob("*.md")):
        rel = md.relative_to(DOCS).as_posix()
        if md.name in {"README.md", "BOOT.md"} or any(rel.startswith(p) for p in SKIP):
            continue
        text = md.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        end = text.find("\n---\n", 4)
        if end < 0:
            continue
        block = text[4:end]
        if re.search(r"(?m)^summary:\s*", block):
            continue
        body = text[end + 5 :]
        summary = first_summary(body)
        if not summary:
            continue
        safe = summary.replace('"', "'")
        # insert after tokens_est or status
        if re.search(r"(?m)^tokens_est:", block):
            new_block = re.sub(
                r"(?m)^(tokens_est:.*)$",
                rf'\1\nsummary: "{safe}"',
                block,
                count=1,
            )
        else:
            new_block = block.rstrip() + f'\nsummary: "{safe}"'
        md.write_text("---\n" + new_block + "\n---\n" + body, encoding="utf-8")
        n += 1
        print(f"summary → docs/{rel}")
    print(f"done — stamped {n} summaries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
