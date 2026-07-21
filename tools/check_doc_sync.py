#!/usr/bin/env python3
"""Documentation sync gate — L0_doc_sync.

Validates:
  1. Every grouped docs/**/*.md is linked from docs/README.md (hub index).
  2. README index links resolve to real files.
  3. docs-CI runner gates match acceptance_criteria.json docs_ci_gates.

See docs/README.md, docs/workflow/BRANCHING.md.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
README = DOCS / "README.md"
RUNNER = ROOT / "tools/run_docs_ci_checks.sh"
CRITERIA = ROOT / "game/data/qa/acceptance_criteria.json"

# Not required in hub index (nested indexes or historical).
EXCLUDE_PATHS = {
    "README.md",
    "SCREENSHOTS.md",
    "GDAI_REGEN_PLAN.md",
}
EXCLUDE_PREFIXES = (
    "generation_briefs/",
    "sprints/",
    "compliance/",
    "pitch/",
    "audio/audio_sheets/",
)


def is_indexed_doc(rel: str) -> bool:
    if rel in EXCLUDE_PATHS or rel.endswith("/SCREENSHOTS.md") or rel == "SCREENSHOTS.md":
        return False
    return not rel.startswith(EXCLUDE_PREFIXES)


def main() -> int:
    errors: list[str] = []
    readme = README.read_text(encoding="utf-8")
    linked = set(re.findall(r"\(([\w./-]+\.md)\)", readme))
    linked_resolved = set()
    for link in linked:
        target = (DOCS / link).resolve()
        if DOCS in target.parents or target.parent == DOCS:
            linked_resolved.add(link.replace("\\", "/"))

    # 1. Every grouped doc appears in hub index (by path suffix).
    for md in sorted(DOCS.rglob("*.md")):
        rel = md.relative_to(DOCS).as_posix()
        if not is_indexed_doc(rel):
            continue
        name = md.name
        if name not in readme and rel not in linked_resolved:
            errors.append(f"docs/{rel} is not linked from docs/README.md index")

    # 2. README links resolve.
    for link in sorted(linked):
        if link.startswith("../"):
            continue
        target = DOCS / link
        if not target.is_file():
            errors.append(f"docs/README.md links missing file: {link}")

    # 3. Runner gates == docs_ci_gates.required_gates.
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

    indexed_count = sum(1 for md in DOCS.rglob("*.md") if is_indexed_doc(md.relative_to(DOCS).as_posix()))

    if errors:
        print("DOC SYNC FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(
        f"doc sync: OK ({indexed_count} grouped docs indexed, "
        f"{len(set(runner_gates))} docs-CI gates aligned)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
