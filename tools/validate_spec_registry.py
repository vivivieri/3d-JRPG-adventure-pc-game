#!/usr/bin/env python3
"""Validate spec-first development registries and development-start gate."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "game" / "data"
CODE = DATA / "code"
VALID_STATUS = frozenset({"specified", "partial", "not_started", "missing"})


def load(rel: str) -> dict:
    with open(DATA / rel if not rel.startswith("game/") else ROOT / rel, encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    errors: list[str] = []
    registry = json.loads((CODE / "spec_registry.json").read_text(encoding="utf-8"))
    artifacts = {a["id"]: a for a in registry.get("artifacts", [])}
    blocking = registry.get("development_start", {}).get("blocking_artifact_ids", [])

    for aid in blocking:
        if aid not in artifacts:
            errors.append(f"development_start references unknown artifact: {aid}")
            continue
        art = artifacts[aid]
        if art.get("spec_status") != "specified":
            errors.append(
                f"SPEC_DEV_START blocked: {aid} is {art.get('spec_status')} (need specified)"
            )
        for p in art.get("paths", []) or []:
            full = ROOT / p
            if not full.exists():
                errors.append(f"Artifact {aid} missing path: {p}")

    for art in registry.get("artifacts", []):
        st = art.get("spec_status")
        if st not in VALID_STATUS:
            errors.append(f"Artifact {art.get('id')} invalid spec_status: {st}")

    # Autoload registry completeness
    autoloads = json.loads((CODE / "autoload_registry.json").read_text(encoding="utf-8"))
    for entry in autoloads.get("autoloads", []):
        eid = entry.get("id", "?")
        if entry.get("spec_status") != "specified":
            errors.append(f"Autoload {eid} not specified")
        if not entry.get("public_api") and not entry.get("signals"):
            errors.append(f"Autoload {eid} missing public_api or signals")
        sp = entry.get("script_path", "")
        if not sp.startswith("res://"):
            errors.append(f"Autoload {eid} invalid script_path")

    # Scene registry — phase 1–2 scenes must have required_nodes or required_children
    scenes = json.loads((CODE / "scene_registry.json").read_text(encoding="utf-8"))
    for sc in scenes.get("scenes", []):
        sid = sc.get("id", "?")
        if sc.get("spec_status") != "specified":
            errors.append(f"Scene {sid} not specified")
        if not sc.get("required_nodes") and not sc.get("required_children"):
            errors.append(f"Scene {sid} missing required_nodes or required_children")

    if errors:
        print("SPEC REGISTRY VALIDATION FAILED", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        print("\nPolicy: docs/technical/SPEC_FIRST_DEVELOPMENT.md", file=sys.stderr)
        return 1

    gate = registry.get("development_start", {}).get("gate_id", "SPEC_DEV_START")
    print(
        f"OK — {gate} gate pass ({len(blocking)} blocking artifacts specified, "
        f"{len(autoloads.get('autoloads', []))} autoloads, {len(scenes.get('scenes', []))} scenes catalogued)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
