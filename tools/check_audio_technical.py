#!/usr/bin/env python3
"""Technical audio QA: format, loudness, duration, placeholder detection (docs/audio/AUDIO_QA.md §A2)."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = ROOT / "game/data/audio/ace_step_prompts.json"
MANIFEST = ROOT / "docs/asset_manifest.license.json"

PROCEDURAL_SOURCE = "generate_game_audio.py"

# AUDIO_PRODUCTION_GUIDE.md §8
SPECS = {
    "bgm": {"lufs": -16.0, "lufs_tol": 4.0, "peak_max": -1.0},
    "stings": {"lufs": None, "lufs_tol": 0.0, "peak_max": -3.0},
    "sfx": {"lufs": None, "lufs_tol": 0.0, "peak_max": -6.0},
    "voice": {"lufs": -18.0, "lufs_tol": 4.0, "peak_max": -3.0},
    "amb": {"lufs": -22.0, "lufs_tol": 4.0, "peak_max": -6.0},
}


def load_prompts() -> dict:
    return json.loads(PROMPTS.read_text(encoding="utf-8"))


def track_output_path(track_id: str, prompts: dict) -> Path | None:
    meta = prompts.get("tracks", {}).get(track_id)
    if not meta:
        return None
    return ROOT / meta["output"]


def bus_for_path(rel: str) -> str:
    if rel.startswith("game/assets/audio/bgm/"):
        return "bgm"
    if rel.startswith("game/assets/audio/stings/"):
        return "stings"
    if rel.startswith("game/assets/audio/voice/"):
        return "voice"
    if rel.startswith("game/assets/audio/amb/"):
        return "amb"
    return "sfx"


def is_procedural_placeholder(rel_path: str) -> bool:
    if not MANIFEST.is_file():
        return False
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for entry in data.get("assets", []):
        if entry.get("path") == rel_path:
            source = entry.get("source", "")
            return PROCEDURAL_SOURCE in source
    return False


def ffprobe_info(path: Path) -> dict:
    cmd = [
        "ffprobe",
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        str(path),
    ]
    out = subprocess.check_output(cmd, text=True)
    return json.loads(out)


def ebur128(path: Path) -> tuple[float | None, float | None]:
    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-nostats",
        "-i",
        str(path),
        "-filter_complex",
        "ebur128=peak=true",
        "-f",
        "null",
        "-",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    text = proc.stderr
    lufs_match = re.search(r"Integrated loudness:\s*\n\s*I:\s*([-\d.]+)\s*LUFS", text)
    peak_match = re.search(r"True peak:\s*\n\s*Peak:\s*([-\d.]+)\s*dBFS", text)
    lufs = float(lufs_match.group(1)) if lufs_match else None
    peak = float(peak_match.group(1)) if peak_match else None
    return lufs, peak


def check_file(path: Path, track_id: str | None, ship: bool) -> tuple[bool, list[str]]:
    issues: list[str] = []
    ok = True
    rel = str(path.relative_to(ROOT))

    if is_procedural_placeholder(rel):
        msg = f"{rel} is dev procedural placeholder (generate_game_audio.py)"
        if ship:
            issues.append(f"FAIL: {msg}")
            ok = False
        else:
            issues.append(f"WARN: {msg}")

    try:
        info = ffprobe_info(path)
    except (subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        return False, [f"ffprobe failed: {exc}"]

    fmt = info.get("format", {})
    duration = float(fmt.get("duration", 0))
    audio_streams = [s for s in info.get("streams", []) if s.get("codec_type") == "audio"]
    if not audio_streams:
        return False, ["no audio stream"]

    stream = audio_streams[0]
    sample_rate = int(stream.get("sample_rate", 0))
    channels = int(stream.get("channels", 0))
    codec = stream.get("codec_name", "")

    if codec != "vorbis":
        issues.append(f"WARN: codec is {codec}, expected vorbis ogg")
    if sample_rate != 44100:
        issues.append(f"FAIL: sample rate {sample_rate}, expected 44100")
        ok = False
    if channels not in (1, 2):
        issues.append(f"FAIL: channels {channels}, expected 1 or 2")
        ok = False

    prompts = load_prompts()
    if track_id and track_id in prompts.get("tracks", {}):
        expected = prompts["tracks"][track_id].get("duration_sec")
        if expected:
            lo, hi = expected * 0.5, expected * 1.5
            if not (lo <= duration <= hi):
                issues.append(
                    f"WARN: duration {duration:.1f}s outside expected {expected}s ±50%"
                )

    bus = bus_for_path(rel)
    spec = SPECS[bus]
    lufs, peak = ebur128(path)

    if peak is not None and peak > spec["peak_max"]:
        issues.append(f"FAIL: true peak {peak:.1f} dBTP > max {spec['peak_max']:.1f}")
        ok = False

    if spec["lufs"] is not None and lufs is not None:
        target = spec["lufs"]
        tol = spec["lufs_tol"]
        if abs(lufs - target) > tol:
            # Downgrade to WARN for procedural placeholders in dev
            level = "FAIL" if ship and not is_procedural_placeholder(rel) else "WARN"
            issues.append(
                f"{level}: integrated {lufs:.1f} LUFS, target {target:.1f} ±{tol:.1f}"
            )
            if level == "FAIL":
                ok = False

    return ok, issues


def main() -> int:
    ap = argparse.ArgumentParser(description="Technical audio QA (AUDIO_QA.md)")
    ap.add_argument("--track", action="append", dest="tracks", default=[])
    ap.add_argument("--all-present", action="store_true", help="Check every existing ogg under game/assets/audio/")
    ap.add_argument("--ship", action="store_true", help="M5 ship strictness (fail placeholders)")
    args = ap.parse_args()

    prompts = load_prompts()
    paths: list[tuple[str | None, Path]] = []

    if args.all_present:
        audio_root = ROOT / "game/assets/audio"
        for ogg in sorted(audio_root.rglob("*.ogg")):
            track_id = ogg.stem
            paths.append((track_id if track_id in prompts.get("tracks", {}) else None, ogg))
    elif args.tracks:
        for track_id in args.tracks:
            p = track_output_path(track_id, prompts)
            if not p:
                print(f"Unknown track: {track_id}", file=sys.stderr)
                return 2
            paths.append((track_id, p))
    else:
        ap.print_help()
        return 2

    fail = 0
    for track_id, path in paths:
        print(f"\n==> {track_id or path.name} ({path.relative_to(ROOT)})")
        if not path.is_file():
            print("  [FAIL] file missing")
            fail += 1
            continue
        ok, issues = check_file(path, track_id, ship=args.ship)
        has_fail = False
        for line in issues:
            print(f"  {line}")
            if line.startswith("FAIL"):
                has_fail = True
        if has_fail or not ok:
            print("  [FAIL] technical")
            fail += 1
        elif any(line.startswith("WARN") for line in issues):
            print("  [WARN] technical (dev placeholders OK)")
        else:
            print("  [PASS] technical")

    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
