#!/usr/bin/env python3
"""Generate selective story VO via ElevenLabs API.

Reads voice_id lines from game/data/dialogue/chapter_01.json.
Casting and mix metadata from game/data/audio/vo_prompts.json.

Usage:
  python3 tools/generate_ai_vo.py --list
  python3 tools/generate_ai_vo.py --tier p0
  python3 tools/generate_ai_vo.py --clip sc03_yuzu_01 --locale ja
  python3 tools/generate_ai_vo.py --locale zh-Hant --dialect cant
  python3 tools/generate_ai_vo.py --locale zh-Hant --all-dialects
  python3 tools/generate_ai_vo.py --all

Requires:
  export ELEVENLABS_API_KEY=...
  Replace PLACEHOLDER_* voice IDs in vo_prompts.json
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIALOGUE_JSON = ROOT / "game/data/dialogue/chapter_01.json"
VO_PROMPTS = ROOT / "game/data/audio/vo_prompts.json"
MANIFEST = ROOT / "docs/asset_manifest.license.json"
VO_ROOT = ROOT / "game/assets/audio/voice"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dialogue_lines_by_voice_id() -> dict[str, dict]:
    data = load_json(DIALOGUE_JSON)
    out: dict[str, dict] = {}
    for scene in data.get("scenes", []):
        for line in scene.get("lines", []):
            vid = line.get("voice_id")
            if vid:
                out[str(vid)] = {
                    "scene_id": scene.get("scene_id"),
                    "speaker": line.get("speaker"),
                    "text": line.get("text", {}),
                    "tier": line.get("vo_tier", ""),
                }
    return out


def clips_for_tier(catalog: dict, tier: str) -> list[str]:
    tier = tier.lower()
    return [
        cid for cid, spec in catalog.get("clips", {}).items()
        if str(spec.get("tier", "")).lower() == tier
    ]


def vo_dialect_codes(catalog: dict) -> list[str]:
    return list(catalog.get("vo_dialects", {}).keys())


def resolve_elevenlabs_voice(char: dict, locale: str, dialect: str | None) -> str:
    if locale == "zh-Hant" and dialect:
        dv = char.get("dialect_voices", {})
        el_voice = str(dv.get(dialect, "")).strip()
        if el_voice and not el_voice.startswith("PLACEHOLDER"):
            return el_voice
    return str(char.get("elevenlabs_voice_id", ""))


def resolve_output_paths(locale: str, dialect: str | None, clip_id: str) -> tuple[Path, str]:
    if locale == "zh-Hant":
        if not dialect:
            raise ValueError("zh-Hant VO requires --dialect cant|cmn or --all-dialects")
        out = VO_ROOT / locale / dialect / f"{clip_id}.ogg"
        rel = f"game/assets/audio/voice/{locale}/{dialect}/{clip_id}.ogg"
    else:
        out = VO_ROOT / locale / f"{clip_id}.ogg"
        rel = f"game/assets/audio/voice/{locale}/{clip_id}.ogg"
    return out, rel


def locale_jobs(
    catalog: dict,
    locales: list[str],
    dialect: str | None,
    all_dialects: bool,
) -> list[tuple[str, str | None]]:
    jobs: list[tuple[str, str | None]] = []
    dialect_codes = vo_dialect_codes(catalog)
    for locale in locales:
        if locale == "zh-Hant":
            if all_dialects:
                for code in dialect_codes:
                    jobs.append((locale, code))
            elif dialect:
                jobs.append((locale, dialect))
            else:
                raise ValueError(
                    "zh-Hant requires --dialect cant|cmn or --all-dialects"
                )
        else:
            jobs.append((locale, None))
    return jobs


def elevenlabs_tts(
    api_key: str,
    voice_id: str,
    text: str,
    model_id: str,
    voice_settings: dict,
) -> bytes:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    payload = {
        "text": text,
        "model_id": model_id,
        "voice_settings": voice_settings,
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()


def mp3_to_ogg(mp3_path: Path, ogg_path: Path) -> None:
    ogg_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(mp3_path), "-c:a", "libvorbis", "-q:a", "6", str(ogg_path)],
        check=True,
        capture_output=True,
    )
    mp3_path.unlink(missing_ok=True)


def register_asset(rel_path: str, voice_id: str, locale: str, dialect: str | None) -> None:
    if not MANIFEST.exists():
        return
    label = f"{locale}/{dialect}" if dialect else locale
    data = load_json(MANIFEST)
    assets = data.setdefault("assets", [])
    for asset in assets:
        if asset.get("path") == rel_path:
            asset.update({
                "license": "COMMERCIAL_AI",
                "source": "ElevenLabs TTS (tools/generate_ai_vo.py)",
                "author": "ElevenLabs / project generation",
                "used_for": f"Selective VO: {voice_id} ({label})",
                "notes": "Verify ElevenLabs commercial terms before Steam ship",
            })
            break
    else:
        assets.append({
            "path": rel_path,
            "license": "COMMERCIAL_AI",
            "source": "ElevenLabs TTS (tools/generate_ai_vo.py)",
            "author": "ElevenLabs / project generation",
            "used_for": f"Selective VO: {voice_id} ({label})",
            "notes": "Verify ElevenLabs commercial terms before Steam ship",
        })
    data["updated"] = str(__import__("datetime").date.today())
    MANIFEST.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def generate_clip(
    clip_id: str,
    catalog: dict,
    lines: dict[str, dict],
    jobs: list[tuple[str, str | None]],
    api_key: str,
    dry_run: bool,
) -> bool:
    if clip_id not in catalog.get("clips", {}):
        print(f"Unknown clip: {clip_id}", file=sys.stderr)
        return False
    if clip_id not in lines:
        print(f"Missing voice_id in dialogue: {clip_id}", file=sys.stderr)
        return False

    clip = catalog["clips"][clip_id]
    line = lines[clip_id]
    speaker = str(line.get("speaker") or clip.get("speaker", ""))
    char = catalog.get("characters", {}).get(speaker)
    if not char:
        print(f"No character profile for speaker: {speaker} ({clip_id})", file=sys.stderr)
        return False

    model_id = str(catalog.get("model_id", "eleven_multilingual_v2"))
    voice_settings = char.get("voice_settings", {})
    ok = True

    for locale, dialect in jobs:
        text_obj = line.get("text", {})
        text = str(text_obj.get(locale, "")).strip()
        if not text:
            tag = f"{locale}/{dialect}" if dialect else locale
            print(f"  Skip {clip_id}/{tag}: no dialogue text", file=sys.stderr)
            ok = False
            continue

        el_voice = resolve_elevenlabs_voice(char, locale, dialect)
        if not el_voice or el_voice.startswith("PLACEHOLDER"):
            tag = f"{locale}/{dialect}" if dialect else locale
            print(
                f"  Skip {clip_id}/{tag}: set voice ID for '{speaker}' in vo_prompts.json",
                file=sys.stderr,
            )
            ok = False
            continue

        out, rel = resolve_output_paths(locale, dialect, clip_id)
        tag = f"{locale}/{dialect}" if dialect else locale
        print(f"  {clip_id} [{tag}] → {out.relative_to(ROOT)}")

        if dry_run:
            continue

        try:
            audio = elevenlabs_tts(api_key, el_voice, text, model_id, voice_settings)
        except (urllib.error.URLError, TimeoutError) as exc:
            print(f"  ElevenLabs error {clip_id}/{tag}: {exc}", file=sys.stderr)
            ok = False
            continue

        tmp_mp3 = out.with_suffix(".mp3")
        tmp_mp3.parent.mkdir(parents=True, exist_ok=True)
        tmp_mp3.write_bytes(audio)
        mp3_to_ogg(tmp_mp3, out)
        register_asset(rel, clip_id, locale, dialect)

    return ok


def print_catalog_summary(catalog: dict, locales: list[str]) -> None:
    all_clips = list(catalog.get("clips", {}).keys())
    dialect_count = len(vo_dialect_codes(catalog))
    standard = [loc for loc in locales if loc != "zh-Hant"]
    zh_hant = "zh-Hant" in locales
    standard_files = len(all_clips) * len(standard)
    dialect_files = len(all_clips) * dialect_count if zh_hant else 0
    print("Selective VO clips:")
    for tier in ("p0", "p1", "p2"):
        ids = clips_for_tier(catalog, tier)
        print(f"  {tier}: {len(ids)} — {', '.join(ids)}")
    print(f"\nTotal: {len(all_clips)} clips")
    if standard:
        print(f"  × {len(standard)} locales ({', '.join(standard)}) = {standard_files} files")
    if zh_hant:
        print(f"  × {dialect_count} zh-Hant dialects (cant, cmn) = {dialect_files} files")
    print(f"  = {standard_files + dialect_files} OGG files")


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate selective AI VO via ElevenLabs")
    ap.add_argument("--list", action="store_true", help="List clips by tier")
    ap.add_argument("--tier", action="append", dest="tiers", default=[], help="p0|p1|p2")
    ap.add_argument("--clip", action="append", dest="clips", default=[], help="voice_id")
    ap.add_argument("--locale", action="append", dest="locales", default=[], help="en|ja|zh|zh-Hant")
    ap.add_argument("--dialect", choices=["cant", "cmn"], help="VO dialect for zh-Hant")
    ap.add_argument("--all-dialects", action="store_true", help="Generate cant + cmn for zh-Hant")
    ap.add_argument("--all", action="store_true", help="All clips in catalog")
    ap.add_argument("--dry-run", action="store_true", help="Print plan only")
    args = ap.parse_args()

    if not VO_PROMPTS.exists():
        print(f"Missing {VO_PROMPTS}", file=sys.stderr)
        return 1

    catalog = load_json(VO_PROMPTS)
    lines = dialogue_lines_by_voice_id()
    all_clips = list(catalog.get("clips", {}).keys())
    default_locales = list(catalog.get("locales", ["en", "ja", "zh", "zh-Hant"]))
    locales = args.locales or default_locales

    if args.list:
        print_catalog_summary(catalog, locales)
        return 0

    try:
        jobs = locale_jobs(catalog, locales, args.dialect, args.all_dialects)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.all:
        selected = all_clips
    elif args.clips:
        selected = args.clips
    elif args.tiers:
        selected = []
        for tier in args.tiers:
            selected.extend(clips_for_tier(catalog, tier))
    else:
        ap.print_help()
        return 1

    api_key = os.environ.get("ELEVENLABS_API_KEY", "")
    if not api_key and not args.dry_run:
        print("Set ELEVENLABS_API_KEY (Cursor Secrets) or use --dry-run", file=sys.stderr)
        return 1

    err = 0
    for clip_id in selected:
        print(f"==> {clip_id}")
        if not generate_clip(clip_id, catalog, lines, jobs, api_key, args.dry_run):
            err = 1

    return err


if __name__ == "__main__":
    sys.exit(main())
