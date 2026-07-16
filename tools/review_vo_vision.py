#!/usr/bin/env python3
"""Multi-model listen jury for P0 selective VO clips (docs/audio/AUDIO_QA.md §A5).

Requires OPENAI_API_KEY and/or GEMINI_API_KEY. Default gate locale: en.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from audio_brief_lib import format_emotional_context  # noqa: E402
from qa_acceptance_lib import evaluate_jury_consensus, normalize_jury_review  # noqa: E402
from review_audio_vision import (  # noqa: E402
    REVIEWERS,
    ogg_to_wav_b64,
)
from vo_qa_lib import (  # noqa: E402
    clip_meta,
    expected_line_text,
    load_vo_prompts,
    p0_listen_clips,
    resolve_vo_path,
)

REVIEW_SCHEMA = """Respond with ONLY valid JSON:
{
  "v1_not_robotic_placeholder": true,
  "v2_script_semantics_match": true,
  "v3_matches_direction": true,
  "v4_not_anime_exaggeration": true,
  "v5_fits_scene_mood": true,
  "v6_emotional_mood_matches": true,
  "v7_no_forbidden_tone": true,
  "overall_pass": true,
  "confidence": 0.8,
  "issues": ["short strings"],
  "summary": "one sentence"
}

Fail overall_pass if robotic TTS placeholder, wrong line meaning, anime squeal/exaggeration,
or emotional register contradicts the generation brief."""


def build_prompt(clip_id: str, locale: str, meta: dict, vo_clip: dict) -> str:
    emotional = format_emotional_context(clip_id, kind="vo")
    emotional_block = (
        f"\n\n### Emotional intent (generation brief)\n{emotional}\n"
        if emotional
        else ""
    )
    script = expected_line_text(clip_id, locale if locale != "zh-Hant" else "zh-Hant")
    script_block = f'\nExpected line ({locale}): "{script}"\n' if script else ""
    direction = vo_clip.get("direction", meta.get("direction", ""))
    return f"""You are a VO QA judge for Tides of Urashima — muted melancholy Japanese coastal JRPG.

Clip: {clip_id}
Scene: {meta.get('scene_id', '')}
Speaker: {meta.get('speaker', '')}
Locale: {locale}
Direction: {direction}
{script_block}{emotional_block}
Listen to the voice line and judge:

V1 — Sounds like intentional acted VO, NOT a cheap robotic placeholder or sine beep?
V2 — Spoken meaning matches the expected script (semantic match; exact wording not required for ja/zh)?
V3 — Performance matches direction above (tone, pacing, restraint)?
V4 — NOT bright anime heroine squeal, comic old man, or villain cackle?
V5 — Fits scene mood (coastal grief, palace wrongness, boss tragedy)?
V6 — Primary emotional mood matches the generation brief?
V7 — Does NOT exhibit forbidden tones from brief (fanservice breathiness, comedy cheer, horror gore)?

Note: V6/V7 judge art-direction emotional register — not subtitle timing or BGM duck mix.

{REVIEW_SCHEMA}"""


def write_vo_manual_packet(out_dir: Path, clip_id: str, locale: str, path: Path, prompt: str) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{clip_id}_{locale}"
    packet = {
        "mode": "manual_vo_jury",
        "clip": clip_id,
        "locale": locale,
        "audio": str(path),
        "prompt": prompt,
        "instructions": [
            "Listen in Cursor with 2+ different models using the prompt below.",
            "Pass if >= 2 return overall_pass: true.",
        ],
        "manual_reviews": [],
    }
    out = out_dir / f"{stem}.manual.json"
    out.write_text(json.dumps(packet, indent=2), encoding="utf-8")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Multi-LLM VO jury (AUDIO_QA.md §A5)")
    ap.add_argument("--clip", required=True, help="P0 clip id (e.g. sc00_urashima_01)")
    ap.add_argument("--locale", default="en", help="Gate locale (default en)")
    ap.add_argument("--dialect", default="", help="cant|cmn when locale zh-Hant")
    ap.add_argument("--models", default="openai,gemini")
    ap.add_argument("--min-pass", type=int, default=2)
    ap.add_argument("--out-dir", type=Path, default=ROOT / "artifacts/vo_reviews")
    args = ap.parse_args()

    if args.clip not in p0_listen_clips():
        print(f"WARN: {args.clip} not in p0_vo_clips; proceeding anyway.", file=sys.stderr)

    meta = clip_meta(args.clip)
    if not meta.get("hero_listen_review"):
        print(f"WARN: {args.clip} hero_listen_review is false", file=sys.stderr)

    vo_prompts = load_vo_prompts()
    vo_clip = vo_prompts.get("clips", {}).get(args.clip, {})
    dialect = args.dialect or None
    path = resolve_vo_path(args.clip, args.locale, dialect if args.locale == "zh-Hant" else None)
    if not path.is_file():
        print(f"VO file missing: {path}", file=sys.stderr)
        return 2

    prompt = build_prompt(args.clip, args.locale, meta, vo_clip)
    wav_b64 = ogg_to_wav_b64(path)
    stem = f"{args.clip}_{args.locale}" + (f"_{dialect}" if dialect else "")

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "clip": args.clip,
        "locale": args.locale,
        "dialect": dialect,
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
                result = normalize_jury_review(result, "vo")
        except Exception as exc:  # noqa: BLE001
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
    out_path = args.out_dir / f"{stem}.jury.json"
    consensus = evaluate_jury_consensus(report, "vo")
    report["acceptance"] = consensus
    report["active_models"] = consensus["active_models"]
    report["passed_models"] = consensus["passed_models"]
    report["consensus_pass"] = consensus["consensus_pass"]
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nWrote {out_path}")

    if active == 0:
        manual = write_vo_manual_packet(args.out_dir, args.clip, args.locale, path, prompt)
        print(f"No audio API keys. Manual jury: {manual}")
        print("SKIP is not PASS — see docs/qa/ACCEPTANCE_CRITERIA.md")
        return 2
    if report["consensus_pass"]:
        print(f"CONSENSUS PASS ({consensus['passed_models']}/{consensus['active_models']}, gate {consensus['gate_id']})")
        return 0
    print(f"CONSENSUS FAIL ({consensus['passed_models']}/{consensus['active_models']}, gate {consensus['gate_id']})")
    print(
        f"\nRemediation: python3 tools/qa_remediation_brief.py --jury {out_path} "
        f"--asset-id {args.clip} --log-attempt"
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
