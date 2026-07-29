#!/usr/bin/env python3
"""Documentation sync gate — L0_doc_sync.

Validates:
  1. Every active docs/**/*.md is indexed from hub text (README catalogs + INDEX.yaml).
  2. Hub README links resolve to real files.
  3. docs-CI runner gates match acceptance_criteria.json docs_ci_gates.

See docs/README.md, docs/ops/workflow/BRANCHING.md, docs/_meta/DOC_LIBRARY_ADR.md.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
README = DOCS / "README.md"
INDEX = DOCS / "INDEX.yaml"
RUNNER = ROOT / "tools/run_docs_ci_checks.sh"
CRITERIA = ROOT / "game/data/qa/acceptance_criteria.json"

EXCLUDE_PATHS = {
    "README.md",
    "SCREENSHOTS.md",
    "GDAI_REGEN_PLAN.md",
    "llms.txt",
}
EXCLUDE_PREFIXES = (
    "briefs/",
    "archive/",
    "_meta/",
    "ops/sprints/",
    "ops/agents/automation_prompts/",
    "design/audio/audio_sheets/",
)


def is_indexed_doc(rel: str) -> bool:
    if rel in EXCLUDE_PATHS or rel.endswith("/SCREENSHOTS.md") or rel == "SCREENSHOTS.md":
        return False
    if rel.endswith("/README.md"):
        return False
    return not rel.startswith(EXCLUDE_PREFIXES)


def hub_corpus() -> str:
    chunks: list[str] = []
    if README.is_file():
        chunks.append(README.read_text(encoding="utf-8"))
    if INDEX.is_file():
        chunks.append(INDEX.read_text(encoding="utf-8"))
    for path in DOCS.rglob("README.md"):
        rel = path.relative_to(DOCS).as_posix()
        if rel.startswith(("archive/", "briefs/", "_meta/")):
            continue
        chunks.append(path.read_text(encoding="utf-8"))
    return "\n".join(chunks)


def main() -> int:
    errors: list[str] = []
    corpus = hub_corpus()
    linked = set(re.findall(r"\(([\w./-]+\.md)\)", corpus))
    linked_resolved: set[str] = set()
    for link in linked:
        # Resolve relative to docs/ when not starting with ../
        if link.startswith("../"):
            continue
        target = (DOCS / link).resolve()
        if DOCS in target.parents or target.parent == DOCS:
            linked_resolved.add(link.replace("\\", "/"))

    for md in sorted(DOCS.rglob("*.md")):
        rel = md.relative_to(DOCS).as_posix()
        if not is_indexed_doc(rel):
            continue
        name = md.name
        stem = md.stem
        if name in corpus or rel in corpus or stem in corpus or rel in linked_resolved:
            continue
        errors.append(f"docs/{rel} is not indexed in README catalogs or INDEX.yaml")

    # README.md (root hub) links resolve.
    readme = README.read_text(encoding="utf-8")
    for link in re.findall(r"\(([\w./-]+\.md)\)", readme):
        if link.startswith("../"):
            continue
        target = DOCS / link
        if not target.is_file():
            errors.append(f"docs/README.md links missing file: {link}")

    runner_gates = re.findall(r'run_gate "([^"]+)"', RUNNER.read_text(encoding="utf-8"))
    dupes = sorted({g for g in runner_gates if runner_gates.count(g) > 1})
    if dupes:
        errors.append(f"duplicate run_gate ids in runner: {dupes}")
    crit = json.loads(CRITERIA.read_text(encoding="utf-8"))
    required = crit.get("docs_ci_gates", {}).get("required_gates", [])
    missing = sorted(set(runner_gates) - set(required))
    extra = sorted(set(required) - set(runner_gates))
    if missing:
        errors.append(f"gates run by runner but not in docs_ci_gates.required_gates: {missing}")
    if extra:
        errors.append(f"gates in required_gates but not run by runner: {extra}")

    indexed_count = sum(
        1 for md in DOCS.rglob("*.md") if is_indexed_doc(md.relative_to(DOCS).as_posix())
    )

    if errors:
        print("DOC SYNC FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(
        f"doc sync: OK ({indexed_count} active docs indexed via hubs/INDEX, "
        f"{len(set(runner_gates))} docs-CI gates aligned)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
