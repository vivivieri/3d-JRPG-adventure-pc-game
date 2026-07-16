#!/usr/bin/env python3
"""One-shot docs folder regrouping — moves files and updates repo references."""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

# folder -> filenames (without .md)
GROUPS: dict[str, list[str]] = {
    "cheat-sheets": ["RR_CHEATSHEET", "CONTROLS_CHEATSHEET"],
    "vision": [
        "GDD",
        "STORYBOARD",
        "NARRATIVE_WRITING_GUIDE",
        "NARRATIVE_DENSITY",
        "VO_HIT_LIST",
        "ENDING_DESIGN",
        "REPLAY_DESIGN",
        "LORE_AND_ENVIRONMENTAL_STORY",
        "PACING_CHART",
        "STORYBOARD_ILLUSTRATIONS",
    ],
    "world": [
        "LEVEL_DESIGN",
        "WORLD_MAP_AND_FLOW",
        "ENVIRONMENT_KITS",
        "PUZZLE_DESIGN",
        "QUEST_AND_FLAGS",
    ],
    "gameplay": [
        "COMBAT_SYSTEMS",
        "SKILLS_BIBLE",
        "BOSS_DESIGNS",
        "ENCOUNTER_TABLE",
        "PROGRESSION_TUNING",
        "ITEMS_AND_ECONOMY",
        "TUTORIAL_DESIGN",
        "GAME_FEEL",
        "ACHIEVEMENTS",
    ],
    "technical": [
        "TECHNICAL_DESIGN",
        "DATA_ARCHITECTURE",
        "CODE_STYLE",
        "CODE_BASE_CLASS_RULES",
        "SAVE_AND_FAIL_STATES",
        "LOCALIZATION",
        "TECH_STACK",
        "PLUGIN_COMPATIBILITY",
        "SPEC_FIRST_DEVELOPMENT",
        "GDSCRIPT_REGENERATION",
    ],
    "ui": ["UI_UX_FLOW", "SETTINGS_ACCESSIBILITY", "CINEMATICS"],
    "art": [
        "ART_DIRECTION",
        "RENDERING_GUIDE",
        "CHARACTER_BIBLE",
        "ITEMS_3D_MODEL_GUIDE",
        "ART_AUTOMATION_PIPELINE",
        "GENERATION_READINESS",
        "VISUAL_QA",
        "MODEL_QA",
        "ASSET_COMPLIANCE",
        "LICENSES",
    ],
    "audio": ["AUDIO_DIRECTION", "AUDIO_PRODUCTION_GUIDE", "AUDIO_QA"],
    "qa": [
        "ACCEPTANCE_CRITERIA",
        "AI_TESTING_SPEC",
        "QA_AND_BUG_PROCESS",
        "QA_REMEDIATION_LOOP",
        "FLOW_QA",
        "PLAYTEST_SCRIPT",
        "PLAYTEST_TELEMETRY",
        "PERFORMANCE_BASELINE",
        "PLATFORM_SUPPORT",
        "SECURITY",
        "ESCALATION_POLICY",
        "SCREENSHOTS",
    ],
    "workflow": [
        "IMPLEMENTATION_PLAN",
        "BRANCHING",
        "MILESTONES",
        "AGILE_WITHIN_PHASES",
        "AI_DEV_WORKFLOW",
        "DELIVERY_CONTROL",
    ],
    "ci-cd": ["CI", "CD", "ENVIRONMENTS", "GITHUB_SETUP", "STEAM_RELEASE_CHECKLIST"],
    "agents": [
        "MULTI_AGENT_TEAM",
        "MULTI_AGENT_BRANCH_STRATEGY",
        "MCP_STACK",
        "SPRINT_ORCHESTRATION",
        "PM_AGENT_RUNBOOK",
        "PM_STAKEHOLDER_REPORTING",
        "PROJECT_MANAGEMENT",
        "FACTORY_WATCHDOG",
        "GDAI_CLOUD_SETUP",
        "PLUGIN_INSTALL_GUIDE",
        "CLOUD_AGENT_SETUP_RUNBOOK",
        "CLOUD_SNAPSHOT_LAUNCH",
        "CURSOR_SECRETS_SETUP",
    ],
    "deprecated": ["GDAI_REGEN_PLAN"],
}

SKIP_REPLACE_SUFFIXES = {".png", ".jpg", ".mp4", ".wav", ".glb", ".jsonl"}

REPLACEMENTS: list[tuple[str, str]] = []


def build_replacements() -> None:
    for folder, names in GROUPS.items():
        for name in names:
            old = f"docs/{name}.md"
            new = f"docs/{folder}/{name}.md"
            REPLACEMENTS.append((old, new))
    REPLACEMENTS.append(("docs/audio_sheets/", "docs/audio/audio_sheets/"))
    REPLACEMENTS.sort(key=lambda x: len(x[0]), reverse=True)


def git_mv(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not src.exists():
        print(f"skip missing {src}")
        return
    subprocess.run(["git", "mv", str(src), str(dst)], cwd=ROOT, check=True)


def move_files() -> None:
    for folder in GROUPS:
        (DOCS / folder).mkdir(parents=True, exist_ok=True)
    for folder, names in GROUPS.items():
        for name in names:
            git_mv(DOCS / f"{name}.md", DOCS / folder / f"{name}.md")
    if (DOCS / "audio_sheets").is_dir():
        git_mv(DOCS / "audio_sheets", DOCS / "audio" / "audio_sheets")


def should_scan(path: Path) -> bool:
    if not path.is_file():
        return False
    if path.suffix.lower() in SKIP_REPLACE_SUFFIXES:
        return False
    skip_dirs = {".git", "node_modules", ".cache", "artifacts"}
    return not any(part in skip_dirs for part in path.parts)


def update_references() -> int:
    changed = 0
    for path in ROOT.rglob("*"):
        if not should_scan(path):
            continue
        if path == Path(__file__).resolve():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        original = text
        for old, new in REPLACEMENTS:
            text = text.replace(old, new)
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed += 1
    return changed


def main() -> int:
    build_replacements()
    move_files()
    n = update_references()
    print(f"Moved docs into {len(GROUPS)} groups; updated references in {n} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
