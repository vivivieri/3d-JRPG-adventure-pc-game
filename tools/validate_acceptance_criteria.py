#!/usr/bin/env python3
"""Validate acceptance_criteria.json and tool threshold alignment (docs/ACCEPTANCE_CRITERIA.md)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CRITERIA_PATH = ROOT / "game/data/qa/acceptance_criteria.json"
PLAYBOOK_PATH = ROOT / "game/data/qa/remediation_playbook.json"


def main() -> int:
    errors: list[str] = []
    if not CRITERIA_PATH.is_file():
        print(f"Missing {CRITERIA_PATH}", file=sys.stderr)
        return 2

    data = json.loads(CRITERIA_PATH.read_text(encoding="utf-8"))
    required_top = ("version", "global_rules", "gates", "jury", "invalid_pass_patterns")
    for key in required_top:
        if key not in data:
            errors.append(f"Missing top-level key: {key}")

    gr = data.get("global_rules", {})
    for key in ("warn_is_not_pass", "skip_is_not_pass", "jury_min_pass_models", "jury_min_confidence"):
        if key not in gr:
            errors.append(f"global_rules missing {key}")

    gates = data.get("gates", {})
    if not gates:
        errors.append("gates must be non-empty")

    for domain in ("visual", "model", "audio"):
        jury = data.get("jury", {}).get(domain)
        if not jury:
            errors.append(f"jury.{domain} missing")
            continue
        if not jury.get("criteria"):
            errors.append(f"jury.{domain}.criteria empty")
        if jury.get("min_confidence", 0) < 0.5:
            errors.append(f"jury.{domain}.min_confidence too low (<0.5)")

    # Palette thresholds match check_screenshot_palette.py defaults
    palette = gates.get("L2_visual_palette", {}).get("metrics", {})
    avg = palette.get("max_avg_anchor_dist", {}).get("value")
    bright = palette.get("max_bright_ratio", {}).get("value")
    if avg != 85.0:
        errors.append(f"L2_visual_palette max_avg_anchor_dist should be 85.0, got {avg}")
    if bright != 0.35:
        errors.append(f"L2_visual_palette max_bright_ratio should be 0.35, got {bright}")

    # Playbook has data + flow sections
    if PLAYBOOK_PATH.is_file():
        pb = json.loads(PLAYBOOK_PATH.read_text(encoding="utf-8"))
        for section in ("data", "flow", "technical"):
            if section not in pb:
                errors.append(f"remediation_playbook missing section: {section}")

    if errors:
        print("ACCEPTANCE CRITERIA VALIDATION FAILED", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(
        f"OK — {len(gates)} gates, {len(data.get('jury', {}))} jury domains, "
        f"jury_min_pass={gr.get('jury_min_pass_models')}, conf_min={gr.get('jury_min_confidence')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
