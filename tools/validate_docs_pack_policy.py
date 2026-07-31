#!/usr/bin/env python3
"""L0_docs_pack_policy — enforce docs pack standing policy (ADR amendment).

Locks outcomes of completed one-shot thinning/stamp/reorg scripts into CI so
those scripts can be removed without honor-system drift.

Authority: docs/_meta/DOC_LIBRARY_ADR.md § Amendment — Docs pack thinning
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
INDEX = DOCS / "INDEX.yaml"
TOOLS = ROOT / "tools"

# Completed bulk-thinning / reorg one-shots — must stay deleted.
FORBIDDEN_ONESHOTS = (
    "split_docs_round4.py",
    "split_docs_round5.py",
    "split_docs_round6.py",
    "split_docs_round7.py",
    "split_docs_round8.py",
    "split_docs_remaining.py",
    "split_fat_ops_docs.py",
    "split_hotpath_docs.py",
    "split_large_guides.py",
    "split_remaining_bibles.py",
    "enhance_docs_packs.py",
    "apply_docs_packs_frontmatter.py",
    "stamp_docs_phase.py",
    "stamp_doc_phases.py",
    "stamp_doc_summaries.py",
    "reorganize_docs.py",
    "reorganize_docs_v2.py",
)

SKIP_FM_NAMES = {"README.md", "BOOT.md"}
SKIP_FM_PREFIXES = (
    "archive/",
    "_meta/",
    "briefs/",
    "design/audio/audio_sheets/",
    "ops/sprints/",
    "ops/agents/automation_prompts/",
)

# Path → phase heuristics (from retired stamp_docs_phase.py) — documented for authors.
PHASE_RULES: list[tuple[str, list[int]]] = [
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

OPAQUE_NAME_RE = re.compile(
    r"(?:^|[_-])part_[ab](?:[_.-]|$)|(?:^|[_-])\(A\)|(?:^|[_-])\(B\)",
    re.I,
)


def _index_md_paths() -> list[str]:
    if not INDEX.is_file():
        return []
    text = INDEX.read_text(encoding="utf-8")
    return sorted(set(re.findall(r"- (docs/[\w./-]+\.md)", text)))


def _skip_rel(rel_under_docs: str) -> bool:
    name = Path(rel_under_docs).name
    if name in SKIP_FM_NAMES:
        return True
    return any(rel_under_docs.startswith(p) for p in SKIP_FM_PREFIXES)


def main() -> int:
    errors: list[str] = []

    # 1) Forbidden completed one-shots must not return
    for name in FORBIDDEN_ONESHOTS:
        path = TOOLS / name
        if path.is_file():
            errors.append(
                f"forbidden completed one-shot still present: tools/{name} "
                "(policy: DOC_LIBRARY_ADR — use packs/skim aids, not new split rounds)"
            )

    # 2) No opaque part_a / part_b / (A)/(B) pack filenames
    for md in DOCS.rglob("*.md"):
        rel = md.relative_to(DOCS).as_posix()
        if rel.startswith("archive/"):
            continue
        stem = md.stem
        if OPAQUE_NAME_RE.search(stem) or stem in {"part_a", "part_b"}:
            errors.append(f"opaque pack filename banned: docs/{rel}")
        # TOC-style filenames ending with _a / _b halves from round7/8
        if re.search(r"_part_[ab]$", stem, re.I):
            errors.append(f"opaque pack filename banned: docs/{rel}")

    # 3) INDEX-listed active docs must carry type/phase/summary/tokens_est
    #    (locks stamp + form_docs_frontmatter outcomes)
    missing_fields: list[str] = []
    checked = 0
    for path in _index_md_paths():
        rel = path[len("docs/") :] if path.startswith("docs/") else path
        if _skip_rel(rel):
            continue
        target = ROOT / path
        if not target.is_file():
            continue
        checked += 1
        text = target.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            missing_fields.append(f"{path} (no frontmatter)")
            continue
        end = text.find("\n---\n", 4)
        block = text[4:end] if end > 0 else ""
        for field in ("type", "phase", "summary", "tokens_est"):
            if not re.search(rf"(?m)^{field}:\s*\S+", block):
                missing_fields.append(f"{path} (missing {field}:)")
                break
    if missing_fields:
        errors.append(
            f"INDEX active docs missing required frontmatter fields "
            f"({len(missing_fields)}/{checked}): e.g. {missing_fields[:5]}"
        )

    # 4) Ongoing operator tools that replace one-shots must remain
    for keep in (
        "consolidate_docs_part_ab.py",
        "apply_docs_skim_aids.py",
        "fix_docs_frontmatter.py",
        "audit_docs_read_efficiency.py",
        "resolve_docs.py",
    ):
        if not (TOOLS / keep).is_file():
            errors.append(f"required docs tooling missing: tools/{keep}")

    if errors:
        print("L0_docs_pack_policy FAIL:")
        for e in errors:
            print(f"  - {e}")
        print(
            "\nAuthor hint — phase heuristics (retired stamp_docs_phase.py):\n"
            + "\n".join(f"  {needle} → {phases}" for needle, phases in PHASE_RULES)
            + "\n  (default → [1])"
        )
        return 1

    print(
        f"L0_docs_pack_policy PASS — no opaque packs, "
        f"{checked} INDEX docs have type/phase/summary/tokens_est, "
        f"{len(FORBIDDEN_ONESHOTS)} one-shots stay deleted"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
