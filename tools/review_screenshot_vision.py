#!/usr/bin/env python3
"""Multi-model vision jury for game screenshots (docs/VISUAL_QA.md §2G).

Calls configured vision LLM APIs with the same ART_DIRECTION checklist.
Ship gate: >= min_pass of configured models must return overall_pass=true.

Environment (Cursor Secrets):
  OPENAI_API_KEY     → gpt-4o (vision)
  ANTHROPIC_API_KEY  → claude-sonnet-4-20250514 (vision)
  GEMINI_API_KEY     → gemini-2.0-flash (vision)

Without API keys: writes a review packet for manual jury in Cursor (2+ models).
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from qa_acceptance_lib import evaluate_jury_consensus, normalize_jury_review  # noqa: E402

ZONE_CONTEXT = {
    "ruined_village": "Ruined Japanese fishing village hub. Muted fog grey #8B9DAF, weathered wood #5C4A3A.",
    "beach": "Coastal beach transition. Pale sand #C9B89A, muted sky.",
    "tidal_caves": "Dark tidal caves. Deep teal #1A4A5A, biolume cyan #4AE8D8 accents.",
    "palace_gate": "Dragon Palace gate. Coral gold #D4A55A, void sky #1A1A3A — not European castle.",
}

REVIEW_SCHEMA = """Respond with ONLY valid JSON (no markdown fences):
{
  "v1_primitives_visible": false,
  "v2_muted_palette": true,
  "v3_npr_not_pbr": true,
  "v4_japanese_coastal": true,
  "v5_silhouette_readable": true,
  "v6_ui_clean": true,
  "overall_pass": true,
  "confidence": 0.85,
  "issues": ["short bullet strings"],
  "summary": "one sentence"
}

Fail overall_pass if ANY v1-v6 is false for this screenshot type. Zone screenshots: v6 may be true if no UI visible."""


def build_prompt(zone: str, scene: str, view: str) -> str:
    ctx = ZONE_CONTEXT.get(zone, f"Zone: {zone}")
    return f"""You are a visual QA judge for Tides of Urashima — a muted, melancholy stylized Japanese coastal 3D JRPG (NOT bright Ghibli, NOT photoreal PBR, NOT chibi).

Scene: {scene} | Zone: {zone} | Camera: {view}
Zone palette: {ctx}

Analyze the screenshot. Answer each criterion from visible evidence only:

V1 — Any obvious grey/brown axis-aligned BOX primitives (placeholder cubes) as hero props or buildings?
V2 — Muted coastal palette (fog, decay) — not candy-bright sunny anime?
V3 — Stylized NPR/toon read — not glossy realistic PBR or photographic HDRI sky?
V4 — Japanese coastal / ryūgū motifs — no European medieval castle look?
V5 — Key silhouettes (torii, character, gate) readable at this camera distance?
V6 — UI clean: no pink missing-font boxes, no clipped text (N/A if no UI in frame)?

{REVIEW_SCHEMA}"""


def _read_image_b64(path: Path) -> tuple[str, str]:
    data = path.read_bytes()
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    return mime, base64.standard_b64encode(data).decode("ascii")


def _parse_json_response(text: str) -> dict:
    text = text.strip()
    fence = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.DOTALL)
    if fence:
        text = fence.group(1)
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError(f"No JSON object in model response: {text[:200]}")
    return json.loads(text[start : end + 1])


def _http_json(url: str, headers: dict, payload: dict, timeout: int = 120) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def review_openai(prompt: str, mime: str, b64: str) -> dict:
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        return {"model": "openai/gpt-4o", "skipped": True, "reason": "OPENAI_API_KEY not set"}
    payload = {
        "model": "gpt-4o",
        "max_tokens": 800,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
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
    parsed["model"] = "openai/gpt-4o"
    parsed["raw"] = text
    return parsed


def review_anthropic(prompt: str, mime: str, b64: str) -> dict:
    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not key:
        return {"model": "anthropic/claude-sonnet-4-20250514", "skipped": True, "reason": "ANTHROPIC_API_KEY not set"}
    media = "image/png" if mime == "image/png" else "image/jpeg"
    payload = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 800,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {"type": "base64", "media_type": media, "data": b64},
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    }
    data = _http_json(
        "https://api.anthropic.com/v1/messages",
        {
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        },
        payload,
    )
    text = data["content"][0]["text"]
    parsed = _parse_json_response(text)
    parsed["model"] = "anthropic/claude-sonnet-4-20250514"
    parsed["raw"] = text
    return parsed


def review_gemini(prompt: str, mime: str, b64: str) -> dict:
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        return {"model": "google/gemini-2.0-flash", "skipped": True, "reason": "GEMINI_API_KEY not set"}
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": mime, "data": b64}},
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
    parsed["raw"] = text
    return parsed


REVIEWERS = {
    "openai": review_openai,
    "anthropic": review_anthropic,
    "gemini": review_gemini,
}


def write_manual_packet(
    out_dir: Path,
    screenshot: Path,
    zone: str,
    scene: str,
    view: str,
    prompt: str,
) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = screenshot.stem
    packet = {
        "mode": "manual_jury",
        "screenshot": str(screenshot),
        "zone": zone,
        "scene": scene,
        "view": view,
        "prompt": prompt,
        "instructions": [
            "Open this screenshot in Cursor with 2+ different vision-capable models.",
            "Paste the prompt field to each model separately.",
            "Record each JSON response in manual_reviews[] below.",
            "Pass if >= 2 models return overall_pass: true.",
        ],
        "manual_reviews": [],
    }
    path = out_dir / f"{stem}.manual.json"
    path.write_text(json.dumps(packet, indent=2), encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Multi-LLM vision jury (VISUAL_QA.md §2G)")
    parser.add_argument("--screenshot", required=True, type=Path)
    parser.add_argument("--zone", required=True)
    parser.add_argument("--scene", default="unknown")
    parser.add_argument("--view", default="gameplay")
    parser.add_argument(
        "--models",
        default="openai,anthropic,gemini",
        help="Comma-separated reviewers to invoke",
    )
    parser.add_argument(
        "--min-pass",
        type=int,
        default=2,
        help="Minimum models that must pass (default 2)",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=ROOT / "artifacts" / "visual_reviews",
    )
    args = parser.parse_args()

    if not args.screenshot.is_file():
        print(f"Screenshot not found: {args.screenshot}", file=sys.stderr)
        return 2

    prompt = build_prompt(args.zone, args.scene, args.view)
    mime, b64 = _read_image_b64(args.screenshot)
    selected = [m.strip() for m in args.models.split(",") if m.strip()]

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "screenshot": str(args.screenshot),
        "zone": args.zone,
        "scene": args.scene,
        "view": args.view,
        "min_pass": args.min_pass,
        "reviews": [],
    }

    active = 0
    passed = 0
    for name in selected:
        fn = REVIEWERS.get(name)
        if not fn:
            print(f"Unknown model key: {name}", file=sys.stderr)
            return 2
        try:
            result = fn(prompt, mime, b64)
            if not result.get("skipped") and not result.get("error"):
                result = normalize_jury_review(result, "visual")
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
        status = "PASS" if ok else "FAIL"
        issues = result.get("issues", [])
        print(f"[{status}] {result.get('model', name)}: {result.get('summary', '')}")
        acc = result.get("acceptance", {})
        if acc and not ok:
            failed = [k for k, v in acc.get("criteria_results", {}).items() if not v]
            if failed:
                print(f"       acceptance: failed {', '.join(failed)}")
        for issue in issues[:3]:
            print(f"       - {issue}")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    out_path = args.out_dir / f"{args.screenshot.stem}.jury.json"
    consensus = evaluate_jury_consensus(report, "visual")
    report["acceptance"] = consensus
    report["active_models"] = consensus["active_models"]
    report["passed_models"] = consensus["passed_models"]
    report["consensus_pass"] = consensus["consensus_pass"]
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nWrote {out_path}")

    if active == 0:
        manual = write_manual_packet(args.out_dir, args.screenshot, args.zone, args.scene, args.view, prompt)
        print(f"No vision API keys configured. Manual jury packet: {manual}")
        print("Set OPENAI_API_KEY / ANTHROPIC_API_KEY / GEMINI_API_KEY in Cursor Secrets, or run manual jury in Cursor.")
        print("SKIP is not PASS — see docs/ACCEPTANCE_CRITERIA.md")
        return 2

    if report["consensus_pass"]:
        print(f"CONSENSUS PASS ({consensus['passed_models']}/{consensus['active_models']} models, gate {consensus['gate_id']})")
        return 0

    print(f"CONSENSUS FAIL ({consensus['passed_models']}/{consensus['active_models']} models, gate {consensus['gate_id']})")
    print(f"\nRemediation: python3 tools/qa_remediation_brief.py --jury {out_path} --log-attempt")
    print("See docs/QA_REMEDIATION_LOOP.md — change ONE lever before rebuild.")
    print("See docs/ACCEPTANCE_CRITERIA.md — PASS requires measurable criteria met.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
