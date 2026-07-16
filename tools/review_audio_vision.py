#!/usr/bin/env python3
"""Multi-model listen jury for hero BGM tracks (docs/AUDIO_QA.md §A3).

Requires OPENAI_API_KEY and/or GEMINI_API_KEY. Anthropic has no audio input in v1.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from qa_acceptance_lib import evaluate_jury_consensus, normalize_jury_review  # noqa: E402
from audio_brief_lib import format_emotional_context  # noqa: E402

PROMPTS = ROOT / "game/data/audio/ace_step_prompts.json"

HERO_TRACKS = [
    "bgm_village",
    "bgm_caves",
    "bgm_palace",
    "cine_opening_hero",
    "cine_ending_rewind_hero",
    "cine_ending_anchor_hero",
    "cine_ending_drift_hero",
    "bgm_boss",
]

REVIEW_SCHEMA = """Respond with ONLY valid JSON:
{
  "a1_not_cheap_procedural": true,
  "a2_melancholy_coastal": true,
  "a3_not_upbeat_pop": true,
  "a4_instrumental_no_vocals": true,
  "a5_fits_scene_mood": true,
  "a6_emotional_mood_matches": true,
  "a7_no_forbidden_tone": true,
  "overall_pass": true,
  "confidence": 0.8,
  "issues": ["short strings"],
  "summary": "one sentence"
}

Fail overall_pass if cheap sine-wave placeholder, upbeat adventure, EDM, vocals, wrong mood,
or emotional register contradicts the generation brief (comedy cheer, horror gore, bright Ghibli)."""


def load_track_meta(track_id: str) -> dict:
    data = json.loads(PROMPTS.read_text(encoding="utf-8"))
    meta = data.get("tracks", {}).get(track_id)
    if not meta:
        raise SystemExit(f"Unknown track: {track_id}")
    return meta


def build_prompt(track_id: str, meta: dict) -> str:
    emotional = format_emotional_context(track_id, kind="audio")
    emotional_block = (
        f"\n\n### Emotional intent (generation brief — compliance only, NOT in-game mix feel)\n{emotional}\n"
        if emotional
        else ""
    )
    return f"""You are an audio QA judge for Tides of Urashima — a muted melancholy Japanese coastal JRPG (NOT upbeat adventure, NOT EDM, NOT bright Ghibli).

Track: {track_id}
Scene: {meta.get('scene', '')}
Category: {meta.get('category', '')}
Creative brief: {meta.get('prompt', '')}
{emotional_block}
Listen to the audio and judge:

A1 — Sounds like composed game BGM, NOT a cheap procedural sine/beep placeholder?
A2 — Melancholy, coastal, restrained (NieR / coastal decay mood)?
A3 — NOT upbeat pop, heroic anime fanfare, or party music?
A4 — Instrumental — no vocals or lyrics?
A5 — Fits the scene/category described above?
A6 — Primary emotional mood matches the generation brief emotional intent?
A7 — Does NOT exhibit forbidden tones from brief (comedy cheer, horror gore, bright anime, EDM)?

Note: A6/A7 judge art-direction emotional register — not player enjoyment or mix ducking.

{REVIEW_SCHEMA}"""


def ogg_to_wav_b64(ogg_path: Path) -> str:
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        wav_path = Path(tmp.name)
    try:
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-i",
                str(ogg_path),
                "-ar",
                "44100",
                "-ac",
                "1",
                str(wav_path),
            ],
            check=True,
        )
        return base64.standard_b64encode(wav_path.read_bytes()).decode("ascii")
    finally:
        wav_path.unlink(missing_ok=True)


def _parse_json_response(text: str) -> dict:
    text = text.strip()
    fence = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL)
    if fence:
        text = fence.group(1)
    start, end = text.find("{"), text.rfind("}")
    if start == -1:
        raise ValueError(f"No JSON in response: {text[:200]}")
    return json.loads(text[start : end + 1])


def _http_json(url: str, headers: dict, payload: dict, timeout: int = 180) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def review_openai(prompt: str, wav_b64: str) -> dict:
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        return {"model": "openai/gpt-4o-audio-preview", "skipped": True, "reason": "OPENAI_API_KEY not set"}
    payload = {
        "model": "gpt-4o-audio-preview",
        "max_tokens": 800,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "input_audio", "input_audio": {"data": wav_b64, "format": "wav"}},
                ],
            }
        ],
    }
    data = _http_json(
        "https://api.openai.com/v1/chat/completions",
        {"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        payload,
    )
    text = data["choices"][0]["message"]["content"]
    parsed = _parse_json_response(text)
    parsed["model"] = "openai/gpt-4o-audio-preview"
    return parsed


def review_gemini(prompt: str, wav_b64: str) -> dict:
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        return {"model": "google/gemini-2.0-flash", "skipped": True, "reason": "GEMINI_API_KEY not set"}
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": "audio/wav", "data": wav_b64}},
                ]
            }
        ],
        "generationConfig": {"maxOutputTokens": 800},
    }
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}"
    data = _http_json(url, {"Content-Type": "application/json"}, payload)
    text = data["candidates"][0]["content"]["parts"][0]["text"]
    parsed = _parse_json_response(text)
    parsed["model"] = "google/gemini-2.0-flash"
    return parsed


REVIEWERS = {"openai": review_openai, "gemini": review_gemini}


def write_manual_packet(out_dir: Path, track_id: str, path: Path, prompt: str) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    packet = {
        "mode": "manual_audio_jury",
        "track": track_id,
        "audio": str(path),
        "prompt": prompt,
        "instructions": [
            "Listen in Cursor with 2+ different models using the prompt below.",
            "Pass if >= 2 return overall_pass: true.",
        ],
        "manual_reviews": [],
    }
    out = out_dir / f"{track_id}.manual.json"
    out.write_text(json.dumps(packet, indent=2), encoding="utf-8")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Multi-LLM audio jury (AUDIO_QA.md)")
    ap.add_argument("--track", required=True, help=f"Hero track id (e.g. bgm_village). Hero set: {', '.join(HERO_TRACKS)}")
    ap.add_argument("--models", default="openai,gemini")
    ap.add_argument("--min-pass", type=int, default=2)
    ap.add_argument("--out-dir", type=Path, default=ROOT / "artifacts/audio_reviews")
    args = ap.parse_args()

    if args.track not in HERO_TRACKS:
        print(f"WARN: {args.track} not in hero jury list; proceeding anyway.", file=sys.stderr)

    meta = load_track_meta(args.track)
    path = ROOT / meta["output"]
    if not path.is_file():
        print(f"Audio file missing: {path}", file=sys.stderr)
        return 2

    prompt = build_prompt(args.track, meta)
    wav_b64 = ogg_to_wav_b64(path)

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "track": args.track,
        "audio": str(path),
        "min_pass": args.min_pass,
        "reviews": [],
    }

    active = passed = 0
    for name in [m.strip() for m in args.models.split(",") if m.strip()]:
        fn = REVIEWERS.get(name)
        if not fn:
            print(f"Unknown reviewer: {name}", file=sys.stderr)
            return 2
        try:
            result = fn(prompt, wav_b64)
            if not result.get("skipped") and not result.get("error"):
                result = normalize_jury_review(result, "audio")
        except (urllib.error.URLError, urllib.error.HTTPError, ValueError, KeyError, json.JSONDecodeError) as exc:
            result = {"model": name, "error": str(exc), "overall_pass": False}
        report["reviews"].append(result)
        if result.get("skipped"):
            print(f"[SKIP] {result.get('model', name)}: {result.get('reason', '')}")
            continue
        if result.get("error"):
            print(f"[ERR]  {name}: {result['error']}")
            continue
        active += 1
        ok = bool(result.get("acceptance", {}).get("valid_pass", result.get("overall_pass")))
        if ok:
            passed += 1
        print(f"[{'PASS' if ok else 'FAIL'}] {result.get('model', name)}: {result.get('summary', '')}")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    out_path = args.out_dir / f"{args.track}.jury.json"
    consensus = evaluate_jury_consensus(report, "audio")
    report["acceptance"] = consensus
    report["active_models"] = consensus["active_models"]
    report["passed_models"] = consensus["passed_models"]
    report["consensus_pass"] = consensus["consensus_pass"]
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nWrote {out_path}")

    if active == 0:
        manual = write_manual_packet(args.out_dir, args.track, path, prompt)
        print(f"No audio API keys. Manual jury: {manual}")
        print("SKIP is not PASS — see docs/ACCEPTANCE_CRITERIA.md")
        return 2
    if report["consensus_pass"]:
        print(f"CONSENSUS PASS ({consensus['passed_models']}/{consensus['active_models']}, gate {consensus['gate_id']})")
        return 0
    print(f"CONSENSUS FAIL ({consensus['passed_models']}/{consensus['active_models']}, gate {consensus['gate_id']})")
    print(
        f"\nRemediation: python3 tools/qa_remediation_brief.py --jury {out_path} "
        f"--asset-id {args.track} --log-attempt"
    )
    print("See docs/QA_REMEDIATION_LOOP.md — change ONE lever before rebuild.")
    print("See docs/ACCEPTANCE_CRITERIA.md — PASS requires measurable criteria met.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
