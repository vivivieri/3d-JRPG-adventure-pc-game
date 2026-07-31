#!/usr/bin/env python3
"""Recalibrate tokens_est + rewrite useless summary: fields on active docs."""
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


def summary_useless(raw: str) -> bool:
    s = raw.strip().strip("\"'")
    if not s or len(s) < 20:
        return True
    if s.startswith(("**Version", "**Hub", "**Authority", "**Problem", "**Purpose", "**Print")):
        return True
    if s.startswith("[`") and "](" in s:
        return True
    if re.search(r"\[`[^`]+`\]\([^)]+\)", s) and len(s) < 80:
        return True
    return False


def derive_summary(body: str) -> str:
    for line in body.splitlines():
        s = line.strip()
        if not s or s.startswith("#") or s.startswith("|") or s.startswith("```"):
            continue
        if s.startswith(("**Hub", "**Version", "**Authority", "**Cross", "> Full detail")):
            continue
        s = re.sub(r"^\*\*[^*]+\*\*\s*—?\s*", "", s)
        s = re.sub(r"\s+", " ", s).strip()
        if summary_useless(s):
            continue
        if len(s) >= 20:
            return s[:160].replace('"', "'")
    # fall back to first H1/H2 words
    for line in body.splitlines():
        if line.startswith("#"):
            return re.sub(r"^#+\s*", "", line).strip()[:160].replace('"', "'")
    return "Doc pack — see hub TOC"


def patch_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return False
    end = text.find("\n---\n", 4)
    if end < 0:
        return False
    block = text[4:end]
    body = text[end + 5 :]
    tokens = max(100, path.stat().st_size // 4)
    # Prefer body-based estimate after rewrite
    tokens = max(100, (len(block) + len(body) + 40) // 4)

    lines = block.splitlines()
    out_lines: list[str] = []
    has_tokens = False
    has_summary = False
    summary_val = derive_summary(body)
    for line in lines:
        if line.startswith("tokens_est:"):
            out_lines.append(f"tokens_est: {tokens}")
            has_tokens = True
        elif line.startswith("summary:"):
            raw = line.split(":", 1)[1].strip().strip("\"'")
            if summary_useless(raw):
                out_lines.append(f'summary: "{summary_val}"')
            else:
                out_lines.append(line)
            has_summary = True
        else:
            out_lines.append(line)
    if not has_tokens:
        out_lines.append(f"tokens_est: {tokens}")
    if not has_summary:
        out_lines.append(f'summary: "{summary_val}"')
    new_block = "\n".join(out_lines)
    new_text = f"---\n{new_block}\n---\n{body}"
    if not new_text.endswith("\n"):
        new_text += "\n"
    # recompute tokens after final
    tokens = max(100, len(new_text) // 4)
    new_text = re.sub(r"(?m)^tokens_est:\s*\d+", f"tokens_est: {tokens}", new_text, count=1)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def main() -> int:
    changed = 0
    for md in sorted(DOCS.rglob("*.md")):
        rel = md.relative_to(DOCS).as_posix()
        if md.name in SKIP_NAMES or any(rel.startswith(p) for p in SKIP_PREFIXES):
            continue
        if patch_file(md):
            changed += 1
            print(f"patched {rel}")
    print(f"done — {changed} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
