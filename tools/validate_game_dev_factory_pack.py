#!/usr/bin/env python3
"""Validate packages/game-dev-factory MVP pack — L0_game_dev_factory_pack gate."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "packages/game-dev-factory"
TOOLS_PATHS = ROOT / "tools/factory_paths.py"
PACK_PATHS = PACK / "python/factory_paths.py"
TOOLS_ENV = ROOT / "tools/factory_env.sh"
PACK_ENV = PACK / "python/factory_env.sh"

REQUIRED = [
    "CONTROL_PLANE.md",
    "README.md",
    "python/factory_paths.py",
    "python/factory_env.sh",
    "schemas/README.md",
    "skills/pm-session/SKILL.md",
    "skills/worker-session/SKILL.md",
    "skills/factory-bootstrap/SKILL.md",
    "templates/sprint_board.template.json",
    "templates/sprint_phases.template.json",
    "templates/pm_orchestrator_steps.template.json",
    "templates/workflow_integration_registry.template.json",
    "templates/factory_watchdog.template.json",
]


def main() -> int:
    errors: list[str] = []
    if not PACK.is_dir():
        print(f"Missing pack dir {PACK}", file=sys.stderr)
        return 1

    for rel in REQUIRED:
        path = PACK / rel
        if not path.is_file():
            errors.append(f"missing {rel}")

    # Path helpers must stay synced (pack is portable mirror of live tools/)
    if TOOLS_PATHS.is_file() and PACK_PATHS.is_file():
        if TOOLS_PATHS.read_text(encoding="utf-8") != PACK_PATHS.read_text(encoding="utf-8"):
            errors.append("python/factory_paths.py out of sync with tools/factory_paths.py")
    else:
        errors.append("factory_paths.py missing in tools/ or pack")

    if TOOLS_ENV.is_file() and PACK_ENV.is_file():
        if TOOLS_ENV.read_text(encoding="utf-8") != PACK_ENV.read_text(encoding="utf-8"):
            errors.append("python/factory_env.sh out of sync with tools/factory_env.sh")
    else:
        errors.append("factory_env.sh missing in tools/ or pack")

    # Templates must be valid JSON and mention placeholders where expected
    for name in (
        "sprint_board.template.json",
        "sprint_phases.template.json",
        "pm_orchestrator_steps.template.json",
        "workflow_integration_registry.template.json",
        "factory_watchdog.template.json",
    ):
        path = PACK / "templates" / name
        if not path.is_file():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{name}: invalid JSON ({exc})")
            continue
        if not isinstance(data, dict) or "version" not in data:
            errors.append(f"{name}: must be object with version")

    control = PACK / "CONTROL_PLANE.md"
    if control.is_file():
        text = control.read_text(encoding="utf-8")
        for needle in (
            "FACTORY_DATA_DIR",
            "control plane",
            "run_post_agent_cycle",
            "Game plugin",
        ):
            if needle.lower() not in text.lower() and needle not in text:
                # case-sensitive for env; loose for prose
                if needle == "FACTORY_DATA_DIR" and needle not in text:
                    errors.append(f"CONTROL_PLANE.md must mention {needle}")
                elif needle != "FACTORY_DATA_DIR" and needle.lower() not in text.lower():
                    errors.append(f"CONTROL_PLANE.md must mention {needle}")

    # Live path resolver must default to this repo's layout
    sys.path.insert(0, str(ROOT / "tools"))
    import factory_paths as fp  # noqa: E402

    if fp.factory_data_dir() != (ROOT / "game/data/qa").resolve():
        errors.append(
            f"default FACTORY_DATA_DIR resolve mismatch: {fp.factory_data_dir()}"
        )
    if fp.factory_artifacts_dir() != (ROOT / "artifacts").resolve():
        errors.append(
            f"default FACTORY_ARTIFACTS_DIR resolve mismatch: {fp.factory_artifacts_dir()}"
        )

    # Override smoke (does not refresh import-time aliases — call functions)
    import os

    os.environ["FACTORY_DATA_DIR"] = "tmp/factory_data_override"
    os.environ["FACTORY_ARTIFACTS_DIR"] = "tmp/factory_artifacts_override"
    try:
        data = fp.factory_data_dir()
        arts = fp.factory_artifacts_dir()
        if data != (ROOT / "tmp/factory_data_override").resolve():
            errors.append(f"FACTORY_DATA_DIR override failed: {data}")
        if arts != (ROOT / "tmp/factory_artifacts_override").resolve():
            errors.append(f"FACTORY_ARTIFACTS_DIR override failed: {arts}")
    finally:
        os.environ.pop("FACTORY_DATA_DIR", None)
        os.environ.pop("FACTORY_ARTIFACTS_DIR", None)

    if errors:
        print("L0_game_dev_factory_pack FAIL", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print("L0_game_dev_factory_pack PASS")
    print(f"  pack={PACK}")
    print("  skills=pm-session,worker-session,factory-bootstrap")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
