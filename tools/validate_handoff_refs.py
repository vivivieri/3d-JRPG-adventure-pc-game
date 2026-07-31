#!/usr/bin/env python3
"""L0_handoff_refs — validate sprint_board handoff_refs doc paths.

Fails when active issues reference missing docs, archive/sprint never-autoload
paths, or (soft) docs that appear nowhere in INDEX.yaml packs.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOARD = ROOT / "game/data/qa/sprint_board.json"
INDEX = ROOT / "docs" / "INDEX.yaml"

ACTIVE = {"todo", "ready", "in_progress", "blocked", "review", "queued", "dispatched"}
CLOSED = {"done", "closed", "cancelled", "canceled", "shipped", "complete", "completed"}


def _index_paths() -> set[str]:
    text = INDEX.read_text(encoding="utf-8")
    return set(re.findall(r"- (docs/[\w./-]+|AGENTS\.md)", text))


def _never_prefixes() -> list[str]:
    # briefs are never_autoload for boot but allowed in handoff_refs
    return [
        "docs/archive/",
        "docs/ops/sprints/",
        "docs/design/audio/audio_sheets/",
        "docs/_meta/redirects",
    ]


def main() -> int:
    if not BOARD.is_file():
        print("L0_handoff_refs FAIL: sprint_board.json missing")
        return 1
    if not INDEX.is_file():
        print("L0_handoff_refs FAIL: docs/INDEX.yaml missing")
        return 1

    board = json.loads(BOARD.read_text(encoding="utf-8"))
    index_paths = _index_paths()
    never = _never_prefixes()
    errors: list[str] = []
    warnings: list[str] = []
    checked = 0

    for issue in board.get("issues") or []:
        status = str(issue.get("status") or "").lower()
        if status in CLOSED:
            continue
        if status and status not in ACTIVE and status not in {"", "open"}:
            # unknown status — still validate
            pass
        iid = issue.get("id") or "?"
        refs = issue.get("handoff_refs") or []
        if not isinstance(refs, list) or not refs:
            warnings.append(f"{iid}: no handoff_refs")
            continue
        for ref in refs:
            if not isinstance(ref, str):
                errors.append(f"{iid}: non-string handoff_ref {ref!r}")
                continue
            if ref.startswith("tools/") or ref.startswith("game/") or ref.startswith("scripts/"):
                # non-doc refs — existence optional
                continue
            if ref != "AGENTS.md" and not ref.startswith("docs/"):
                warnings.append(f"{iid}: non-docs handoff_ref {ref}")
                continue
            checked += 1
            target = ROOT / ref
            if not target.is_file():
                errors.append(f"{iid}: missing {ref}")
                continue
            if any(ref.startswith(p) for p in never):
                errors.append(f"{iid}: never_autoload path in handoff_refs: {ref}")
                continue
            if ref.startswith("docs/") and ref not in index_paths and not ref.startswith(
                "docs/briefs/"
            ):
                # packs under hubs may not be listed — warn only if not under a known pack dir
                packish = any(
                    f"/{seg}/" in ref
                    for seg in (
                        "testing",
                        "mcp",
                        "ai_dev",
                        "rr",
                        "characters",
                        "production",
                        "data",
                        "narrative",
                        "implementation",
                        "cloud_setup",
                        "items",
                        "rendering",
                        "model_qa",
                    )
                )
                if not packish:
                    warnings.append(f"{iid}: {ref} not listed in INDEX.yaml")

        docs_task = issue.get("docs_task")
        if docs_task:
            # ensure task exists in INDEX
            if not re.search(rf"(?m)^  {re.escape(str(docs_task))}:\s*$", INDEX.read_text(encoding="utf-8")):
                errors.append(f"{iid}: docs_task={docs_task!r} missing from INDEX.yaml tasks:")

    if warnings:
        for w in warnings:
            print(f"WARN: {w}")
    if errors:
        print("L0_handoff_refs FAIL:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"L0_handoff_refs PASS — checked {checked} doc refs on active issues")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
