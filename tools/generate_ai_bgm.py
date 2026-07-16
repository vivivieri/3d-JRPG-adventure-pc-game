#!/usr/bin/env python3
"""Generate BGM via ACE-Step 1.5 prompts (MIT) with procedural fallback.

Reads track specs from game/data/audio/ace_step_prompts.json.
Writes prompt sheets to docs/audio/audio_sheets/ and optionally calls ACE-Step API.

Usage:
  python3 tools/generate_ai_bgm.py --list
  python3 tools/generate_ai_bgm.py --category opening
  python3 tools/generate_ai_bgm.py --category boss_cinematic --category ending
  python3 tools/generate_ai_bgm.py --track bgm_village --prompts-only
  python3 tools/generate_ai_bgm.py --category all --fallback
  python3 tools/generate_ai_bgm.py --track cine_opening_hero --api

ACE-Step API (optional): start with bash tools/install_ace_step.sh then:
  cd .cache/ace-step-1.5 && uv run acestep-api
  export ACESTEP_API_URL=http://127.0.0.1:8001
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROMPTS_JSON = ROOT / "game/data/audio/ace_step_prompts.json"
SHEETS_DIR = ROOT / "docs/audio_sheets"
MANIFEST = ROOT / "docs/asset_manifest.license.json"
PROCEDURAL = ROOT / "tools/generate_game_audio.py"

# Tracks with procedural fallback in generate_game_audio.py
PROCEDURAL_IDS = {
    "bgm_menu", "bgm_prologue", "cine_opening_hero",
    "bgm_village", "bgm_caves", "bgm_combat", "bgm_palace",
    "bgm_boss", "bgm_boss_tide_keeper_p2", "bgm_boss_tide_keeper_p3",
    "cine_boss_wraith_intro", "cine_boss_sentinel_intro", "cine_boss_tide_keeper_intro",
    "bgm_ending_rewind", "cine_ending_rewind_hero",
    "bgm_ending_anchor", "cine_ending_anchor_hero",
    "bgm_ending_drift", "cine_ending_drift_hero",
    "sting_boss_intro", "sting_combat_start", "sting_yuzu_join", "sting_choice_silence",
    "sfx_ui", "sfx_ui_confirm", "sfx_hit", "sfx_victory",
}


def load_catalog() -> dict:
    return json.loads(PROMPTS_JSON.read_text(encoding="utf-8"))


def tracks_for_categories(catalog: dict, categories: list[str]) -> dict[str, dict]:
    tracks = catalog["tracks"]
    if "all" in categories:
        return tracks
    out: dict[str, dict] = {}
    for tid, spec in tracks.items():
        if spec.get("category") in categories:
            out[tid] = spec
    return out


def write_prompt_sheet(track_id: str, spec: dict, catalog: dict) -> Path:
    SHEETS_DIR.mkdir(parents=True, exist_ok=True)
    path = SHEETS_DIR / f"{track_id}.md"
    neg = catalog.get("global_negative", "")
    lines = [
        f"# ACE-Step prompt — `{track_id}`",
        "",
        f"| Field | Value |",
        f"|-------|-------|",
        f"| Scene | {spec.get('scene', '—')} |",
        f"| Category | {spec.get('category', '—')} |",
        f"| Output | `{spec.get('output', '—')}` |",
        f"| Duration | {spec.get('duration_sec', '—')} s |",
        f"| Loop | {spec.get('loop', '—')} |",
        f"| BPM | {spec.get('bpm', '—')} |",
        f"| Key | {spec.get('key', '—')} |",
        "",
        "## Prompt",
        "",
        spec.get("prompt", ""),
        "",
        "## Negative",
        "",
        neg,
        "",
        "## ACE-Step Gradio / API",
        "",
        "1. `bash tools/install_ace_step.sh`",
        "2. `cd .cache/ace-step-1.5 && uv run acestep` (or `uv run acestep-api`)",
        "3. Paste prompt; set duration/BPM/key; export WAV",
        "4. `ffmpeg -i track.wav -c:a libvorbis -q:a 4 game/assets/audio/.../track.ogg`",
        "5. `python3 tools/register_asset.py add ...`",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def register_ace_asset(rel_path: str, track_id: str, used_for: str) -> None:
    if not MANIFEST.exists():
        return
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assets = data.setdefault("assets", [])
    for a in assets:
        if a.get("path") == rel_path:
            a.update({
                "license": "MIT",
                "source": "ACE-Step 1.5 (github.com/ace-step/ACE-Step-1.5)",
                "author": "ACE-Step / project generation",
                "used_for": used_for,
                "notes": f"AI BGM prototype: {track_id}; verify originality before ship",
            })
            break
    else:
        assets.append({
            "path": rel_path,
            "license": "MIT",
            "source": "ACE-Step 1.5 (github.com/ace-step/ACE-Step-1.5)",
            "author": "ACE-Step / project generation",
            "used_for": used_for,
            "notes": f"AI BGM prototype: {track_id}",
        })
    data["updated"] = str(__import__("datetime").date.today())
    MANIFEST.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def try_ace_step_api(track_id: str, spec: dict, catalog: dict, api_url: str) -> bool:
    """POST to ACE-Step REST API if server is running. Returns True on success."""
    payload = {
        "prompt": spec.get("prompt", ""),
        "negative_prompt": catalog.get("global_negative", ""),
        "duration": spec.get("duration_sec", 120),
        "bpm": spec.get("bpm"),
        "key": spec.get("key"),
        "instrumental": True,
    }
    url = api_url.rstrip("/") + "/v1/generate"
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=600) as resp:
            body = json.load(resp)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
        print(f"  ACE-Step API unavailable for {track_id}: {e}", file=sys.stderr)
        return False

    audio_path = body.get("audio_path") or body.get("path")
    if not audio_path:
        print(f"  ACE-Step API response missing audio path for {track_id}", file=sys.stderr)
        return False

    out = ROOT / spec["output"]
    out.parent.mkdir(parents=True, exist_ok=True)
    wav = Path(audio_path)
    if wav.suffix.lower() == ".ogg":
        subprocess.run(["cp", str(wav), str(out)], check=True)
    else:
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(wav), "-c:a", "libvorbis", "-q:a", "4", str(out)],
            check=True,
            capture_output=True,
        )
    register_ace_asset(spec["output"], track_id, spec.get("scene", track_id))
    print(f"  ACE-Step → {out}")
    return True


def run_procedural_fallback(track_id: str) -> bool:
    if track_id not in PROCEDURAL_IDS:
        print(f"  No procedural fallback for {track_id}", file=sys.stderr)
        return False
    subprocess.run([sys.executable, str(PROCEDURAL), "--track", track_id], check=True)
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description="ACE-Step BGM generation for Tides of Urashima")
    ap.add_argument("--list", action="store_true", help="List categories and track counts")
    ap.add_argument("--category", action="append", dest="categories", default=[],
                    help="zone|opening|boss|boss_cinematic|ending|stings|all")
    ap.add_argument("--track", action="append", dest="tracks", default=[], help="Specific track id")
    ap.add_argument("--prompts-only", action="store_true", help="Write docs/audio_sheets only")
    ap.add_argument("--api", action="store_true", help="Try ACE-Step REST API")
    ap.add_argument("--fallback", action="store_true", help="Procedural fallback where available")
    args = ap.parse_args()

    if not PROMPTS_JSON.exists():
        print(f"Missing {PROMPTS_JSON}", file=sys.stderr)
        return 1

    catalog = load_catalog()
    api_url = __import__("os").environ.get("ACESTEP_API_URL", "http://127.0.0.1:8001")

    if args.list:
        cats: dict[str, int] = {}
        for spec in catalog["tracks"].values():
            c = spec.get("category", "?")
            cats[c] = cats.get(c, 0) + 1
        print("ACE-Step track catalog:")
        for c, n in sorted(cats.items()):
            print(f"  {c}: {n} tracks")
        print(f"\nTotal: {len(catalog['tracks'])} tracks")
        print(f"Prompts: {PROMPTS_JSON}")
        return 0

    if args.tracks:
        selected = {tid: catalog["tracks"][tid] for tid in args.tracks if tid in catalog["tracks"]}
        missing = [t for t in args.tracks if t not in catalog["tracks"]]
        for m in missing:
            print(f"Unknown track: {m}", file=sys.stderr)
        if not selected:
            return 1
    elif args.categories:
        selected = tracks_for_categories(catalog, args.categories)
    else:
        ap.print_help()
        return 1

    err = 0
    for track_id, spec in selected.items():
        print(f"==> {track_id} ({spec.get('category')})")
        sheet = write_prompt_sheet(track_id, spec, catalog)
        print(f"  Sheet: {sheet.relative_to(ROOT)}")

        if args.prompts_only:
            continue

        ok = False
        if args.api:
            ok = try_ace_step_api(track_id, spec, catalog, api_url)
        if not ok and args.fallback:
            ok = run_procedural_fallback(track_id)
        if not ok and not args.prompts_only:
            print("  → Generate manually via ACE-Step Gradio or API (see sheet)")

    return err


if __name__ == "__main__":
    sys.exit(main())
