#!/usr/bin/env python3
"""L0_docs_index — validate docs/INDEX.yaml paths + redirects consistency."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
INDEX = DOCS / "INDEX.yaml"
REDIRECTS = DOCS / "_meta" / "redirects.json"
BOOT = DOCS / "ops" / "BOOT.md"
LLMS = DOCS / "llms.txt"


def _collect_quoted_paths(text: str) -> list[str]:
    """Collect docs/… and AGENTS.md path tokens from INDEX.yaml."""
    found: list[str] = []
    for match in re.finditer(r"- (docs/[\w./-]+|AGENTS\.md)", text):
        found.append(match.group(1))
    return found


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    if not INDEX.is_file():
        print("L0_docs_index FAIL: docs/INDEX.yaml missing")
        return 1
    if not BOOT.is_file():
        errors.append("docs/ops/BOOT.md missing")
    if not LLMS.is_file():
        errors.append("docs/llms.txt missing")
    if not (DOCS / "_meta" / "DOC_LIBRARY_ADR.md").is_file():
        errors.append("docs/_meta/DOC_LIBRARY_ADR.md missing")

    index_text = INDEX.read_text(encoding="utf-8")
    paths = _collect_quoted_paths(index_text)
    if len(paths) < 10:
        errors.append(f"INDEX.yaml yielded too few paths ({len(paths)})")

    seen: set[str] = set()
    for p in paths:
        if p in seen:
            continue
        seen.add(p)
        # never_autoload entries may be directories
        target = ROOT / p
        if p.endswith("/"):
            if not target.is_dir():
                errors.append(f"INDEX never_autoload dir missing: {p}")
            continue
        if not target.is_file():
            # allow directory prefixes listed without trailing slash
            if target.is_dir():
                continue
            errors.append(f"INDEX path missing: {p}")

    # Required top-level buckets
    for folder in ("design", "engineering", "ops", "briefs", "archive", "_meta"):
        if not (DOCS / folder).is_dir():
            errors.append(f"missing docs/{folder}/")

    # Redirects: old paths must not still exist as dirs (except intentional)
    if REDIRECTS.is_file():
        redirects = json.loads(REDIRECTS.read_text(encoding="utf-8"))
        legacy_tops = (
            "vision",
            "world",
            "gameplay",
            "art",
            "audio",
            "ui",
            "technical",
            "agents",
            "workflow",
            "ci-cd",
            "qa",
            "cheat-sheets",
            "sprints",
            "generation_briefs",
            "deprecated",
            "compliance",
            "pitch",
        )
        for name in legacy_tops:
            legacy = DOCS / name
            if legacy.exists():
                errors.append(f"legacy docs/{name} still present — expected move to new bucket")
        if len(redirects) < 50:
            warnings.append(f"redirects.json looks thin ({len(redirects)} entries)")
    else:
        errors.append("docs/_meta/redirects.json missing")

    # Stale path greps in always-on boot files
    for boot_file in (ROOT / ".cursorrules", ROOT / "AGENTS.md", BOOT):
        if not boot_file.is_file():
            continue
        text = boot_file.read_text(encoding="utf-8")
        for stale in (
            "docs/art/",
            "docs/qa/",
            "docs/agents/",
            "docs/technical/",
            "docs/workflow/",
            "docs/ci-cd/",
            "docs/vision/",
        ):
            if stale in text:
                errors.append(f"{boot_file.relative_to(ROOT)} still references {stale}")

    # Tool Path constants that must exist after the library reorg
    tool_dirs = (
        ROOT / "docs" / "briefs",
        ROOT / "docs" / "briefs" / "audio",
        ROOT / "docs" / "briefs" / "vo",
        ROOT / "docs" / "archive" / "pitch" / "illustrations",
        ROOT / "docs" / "archive" / "compliance",
    )
    for path in tool_dirs:
        if not path.is_dir():
            errors.append(f"tool-required docs path missing: {path.relative_to(ROOT)}")

    # Stale Path constructors still pointing at pre-reorg folders
    stale_path_snippets = (
        'ROOT / "docs" / "generation_briefs"',
        'ROOT / "docs" / "pitch" /',
        'ROOT / "docs" / "compliance"',
    )
    for py in (ROOT / "tools").glob("*.py"):
        if py.name.startswith("reorganize_docs") or py.name == "validate_docs_index.py":
            continue
        text = py.read_text(encoding="utf-8")
        for snippet in stale_path_snippets:
            if snippet in text:
                errors.append(f"{py.relative_to(ROOT)} still constructs {snippet}")

    # Frontmatter coverage on active docs (type required)
    skip_fm_names = {"README.md", "BOOT.md"}
    skip_fm_prefixes = (
        "archive/",
        "_meta/",
        "briefs/",
        "design/audio/audio_sheets/",
        "ops/sprints/",
        "ops/agents/automation_prompts/",
    )
    active = 0
    with_type = 0
    missing_fm: list[str] = []
    for md in sorted(DOCS.rglob("*.md")):
        rel = md.relative_to(DOCS).as_posix()
        if md.name in skip_fm_names or any(rel.startswith(p) for p in skip_fm_prefixes):
            continue
        active += 1
        text = md.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            missing_fm.append(rel)
            continue
        end = text.find("\n---\n", 4)
        block = text[4:end] if end > 0 else ""
        if re.search(r"(?m)^type:\s+\S+", block):
            with_type += 1
        else:
            missing_fm.append(f"{rel} (no type:)")
    coverage = (with_type / active) if active else 1.0
    if coverage < 0.8:
        errors.append(
            f"frontmatter type coverage {coverage:.0%} < 80% "
            f"({with_type}/{active}); missing e.g. {missing_fm[:5]}"
        )
    elif missing_fm:
        warnings.append(
            f"frontmatter incomplete on {len(missing_fm)} doc(s) "
            f"(coverage {coverage:.0%}) e.g. {missing_fm[:3]}"
        )

    # Hub packs exist after bible splits
    for rel in (
        "ops/qa/testing/l0.md",
        "ops/agents/mcp/install.md",
        "ops/workflow/ai_dev/testing_policy.md",
        "ops/cheat-sheets/rr/session.md",
        "ops/cheat-sheets/rr/golden_rules.md",
        "ops/cheat-sheets/controls/gates_by_branch.md",
        "design/art/characters/urashima.md",
        "design/audio/production/bgm_and_scene_map.md",
        "engineering/technical/data/story_spine.md",
        "design/art/rendering/lighting_fog.md",
        "design/art/model_qa/layers_workflow.md",
        "design/art/items/export_qa.md",
        "design/vision/narrative/character_voice.md",
        "ops/workflow/implementation/phase_1.md",
        "ops/agents/cloud_setup/setup_automations.md",
        "ops/workflow/agile/summary_why.md",
        "ops/agents/secrets/day_one_checklist.md",
        "design/world/levels/ruined_village.md",
        "ops/ci-cd/ci/required_gates.md",
        "ops/workflow/lifecycle/overview_time.md",
        "engineering/technical/gdscript_regen/principle_rr.md",
        "design/world/env_kits/ruined_village.md",
        "design/art/automation/zone_textures.md",
        "design/art/direction/palette.md",
        "design/art/visual_qa/judge_layers.md",
        "design/art/generation_readiness/characters_zones.md",
        "engineering/technical/tdd/principles_runtime.md",
        "engineering/technical/coding/naming.md",
        "ops/qa/remediation/levers_commands.md",
        "ops/qa/acceptance/gate_catalog.md",
    ):
        if not (DOCS / rel).is_file():
            errors.append(f"expected pack missing: docs/{rel}")

    # Task packs present in INDEX
    if "tasks:" not in index_text:
        errors.append("INDEX.yaml missing tasks: section")
    for task in (
        "zone_lighting",
        "combat_balance",
        "vo_gen",
        "steam_export",
        "water_shader",
        "factory_bootstrap",
        "model_qa",
        "level_layout",
        "secrets_setup",
        "visual_qa",
        "acceptance_ci",
        "audio_bgm",
        "ui_cinematics",
    ):
        if not re.search(rf"(?m)^  {re.escape(task)}:\s*$", index_text):
            errors.append(f"INDEX.yaml missing tasks.{task}")

    # tokens_est drift on INDEX-listed files (hubs + packs)
    drift_bad: list[str] = []
    for p in sorted(seen):
        if p.endswith("/") or p == "AGENTS.md":
            continue
        target = ROOT / p
        if not target.is_file():
            continue
        text = target.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            continue
        end = text.find("\n---\n", 4)
        block = text[4:end] if end > 0 else ""
        m = re.search(r"(?m)^tokens_est:\s*(\d+)", block)
        if not m:
            continue
        claimed = int(m.group(1))
        actual = max(100, target.stat().st_size // 4)
        # allow 25% or 80 tok slack (tiny hubs)
        if abs(claimed - actual) > max(80, int(actual * 0.25)):
            drift_bad.append(f"{p} tokens_est={claimed} size/4={actual}")
    if len(drift_bad) > 8:
        errors.append(
            f"tokens_est drift on {len(drift_bad)} INDEX paths "
            f"(e.g. {drift_bad[:3]})"
        )
    elif drift_bad:
        warnings.append(f"tokens_est mild drift on {len(drift_bad)} path(s)")

    if warnings:
        for w in warnings:
            print(f"WARN: {w}")

    if errors:
        print("L0_docs_index FAIL:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(
        f"L0_docs_index PASS — {len(seen)} INDEX paths ok, "
        f"frontmatter {with_type}/{active} ({coverage:.0%}), "
        f"buckets present, boot card + llms.txt ok"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
