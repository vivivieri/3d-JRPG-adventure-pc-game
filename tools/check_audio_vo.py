#!/usr/bin/env python3
"""Technical VO QA: duration, loudness, locale paths (docs/audio/AUDIO_QA.md §A4)."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from check_audio_technical import check_file  # noqa: E402
from vo_qa_lib import (  # noqa: E402
    clip_meta,
    expected_line_text,
    load_catalog,
    locale_jobs,
    p0_listen_clips,
    resolve_vo_path,
)


def check_clip_locale(
    clip_id: str,
    locale: str,
    dialect: str | None,
    ship: bool,
    require_script: bool,
) -> tuple[bool, list[str]]:
    issues: list[str] = []
    ok = True
    meta = clip_meta(clip_id)
    path = resolve_vo_path(clip_id, locale, dialect)
    rel = str(path.relative_to(ROOT))
    tag = f"{clip_id}/{locale}" + (f"/{dialect}" if dialect else "")

    if require_script:
        script = expected_line_text(clip_id, locale if locale != "zh-Hant" else "zh-Hant")
        if not script:
            issues.append(f"FAIL: {tag} missing dialogue script for locale")
            return False, issues

    if not path.is_file():
        level = "FAIL" if ship else "WARN"
        issues.append(f"{level}: {tag} file missing ({rel})")
        return False if level == "FAIL" else True, issues

    file_ok, file_issues = check_file(path, None, ship=ship)
    for line in file_issues:
        issues.append(f"{tag}: {line}")
    if not file_ok:
        ok = False

    info_issues = _check_duration(path, meta, tag, ship)
    for line in info_issues:
        issues.append(line)
        if line.startswith("FAIL"):
            ok = False

    return ok, issues


def _check_duration(path: Path, meta: dict, tag: str, ship: bool) -> list[str]:
    from check_audio_technical import ffprobe_info

    issues: list[str] = []
    try:
        info = ffprobe_info(path)
        duration = float(info.get("format", {}).get("duration", 0))
    except Exception as exc:  # noqa: BLE001
        return [f"FAIL: {tag} ffprobe failed: {exc}"]

    max_sec = float(meta.get("max_duration_sec", 0) or 0)
    if max_sec <= 0:
        return issues
    if duration > max_sec:
        issues.append(
            f"FAIL: {tag} duration {duration:.2f}s > max {max_sec:.2f}s "
            f"(catalog max_duration_sec)"
        )
    elif duration > max_sec * 0.95:
        issues.append(
            f"WARN: {tag} duration {duration:.2f}s near max {max_sec:.2f}s — trim for duck headroom"
        )
    return issues


def main() -> int:
    ap = argparse.ArgumentParser(description="Technical VO QA (AUDIO_QA.md §A4)")
    ap.add_argument("--clip", action="append", dest="clips", default=[])
    ap.add_argument("--locale", default="en", help="Locale tag for single-clip check (default en)")
    ap.add_argument("--dialect", default="", help="cant|cmn when --locale zh-Hant")
    ap.add_argument("--all-p0", action="store_true", help="Check every locale job for P0 clips")
    ap.add_argument("--ship", action="store_true", help="M5 ship strictness")
    args = ap.parse_args()

    catalog = load_catalog()
    clip_ids = args.clips or (p0_listen_clips() if args.all_p0 else [])
    if not clip_ids:
        ap.print_help()
        return 2

    fail = 0
    for clip_id in clip_ids:
        meta = catalog.get("vo_clips", {}).get(clip_id)
        if not meta:
            print(f"Unknown clip: {clip_id}", file=sys.stderr)
            fail += 1
            continue

        if args.all_p0:
            jobs = locale_jobs(meta)
        else:
            dialect = args.dialect or None
            jobs = [(args.locale, dialect if args.locale == "zh-Hant" else None)]

        print(f"\n==> VO clip {clip_id} ({len(jobs)} locale job(s))")
        for locale, dialect in jobs:
            tag = f"{clip_id}/{locale}" + (f"/{dialect}" if dialect else "")
            print(f"  --- {tag}")
            ok, issues = check_clip_locale(
                clip_id,
                locale,
                dialect,
                ship=args.ship,
                require_script=True,
            )
            has_fail = any(i.startswith("FAIL") for i in issues)
            for line in issues:
                print(f"    {line}")
            if has_fail or not ok:
                print("    [FAIL] technical")
                fail += 1
            elif any(i.startswith("WARN") for i in issues):
                print("    [WARN] technical")
            else:
                print("    [PASS] technical")

    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
