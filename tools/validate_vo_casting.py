#!/usr/bin/env python3
"""L0_vo_casting — ElevenLabs voice IDs must not stay PLACEHOLDER_* for ship phases.

On main (docs/data): WARN count only — casting is M5 work.
When VO_CASTING_REQUIRED=1 or --strict: FAIL if any PLACEHOLDER_* remains.
Authority: docs/vision/VO_HIT_LIST.md · docs/audio/AUDIO_PRODUCTION_GUIDE.md
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VO_PATH = ROOT / "game/data/audio/vo_prompts.json"


def collect_placeholders(obj: object, path: str, found: list[str]) -> None:
    if isinstance(obj, dict):
        for key, value in obj.items():
            collect_placeholders(value, f"{path}.{key}", found)
    elif isinstance(obj, list):
        for index, value in enumerate(obj):
            collect_placeholders(value, f"{path}[{index}]", found)
    elif isinstance(obj, str) and obj.startswith("PLACEHOLDER_"):
        found.append(f"{path}={obj}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate VO casting IDs")
    parser.add_argument("--strict", action="store_true", help="FAIL on PLACEHOLDER_* ids")
    args = parser.parse_args()

    strict = args.strict or os.environ.get("VO_CASTING_REQUIRED", "0") == "1"

    if not VO_PATH.is_file():
        print(f"[FAIL] missing {VO_PATH}", file=sys.stderr)
        return 1

    data = json.loads(VO_PATH.read_text(encoding="utf-8"))
    found: list[str] = []
    collect_placeholders(data, "vo_prompts", found)

    if not found:
        print("[PASS] L0_vo_casting — no PLACEHOLDER_* voice ids")
        return 0

    msg = f"{len(found)} PLACEHOLDER_* voice id(s) in {VO_PATH.relative_to(ROOT)}"
    if strict:
        print(f"[FAIL] L0_vo_casting — {msg}", file=sys.stderr)
        for item in found[:20]:
            print(f"  - {item}", file=sys.stderr)
        if len(found) > 20:
            print(f"  … and {len(found) - 20} more", file=sys.stderr)
        print(
            "Replace with real ElevenLabs voice ids — docs/vision/VO_HIT_LIST.md",
            file=sys.stderr,
        )
        return 1

    print(f"[WARN] L0_vo_casting — {msg} (OK on main until M5; set VO_CASTING_REQUIRED=1 to fail)")
    print("[PASS] L0_vo_casting — advisory only (not strict)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
