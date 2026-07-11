#!/usr/bin/env python3
"""Multi-model vision jury on 3D turntable renders (docs/MODEL_QA.md §M3b)."""
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

sys.path.insert(0, str(Path(__file__).resolve().parent))
from model_qa_lib import ROOT, load_catalog  # noqa: E402

VIEWS = ("front", "side", "back", "three_quarter")

REVIEW_SCHEMA = """Respond with ONLY valid JSON:
{
  "m1_not_block_primitive": true,
  "m2_japanese_coastal_style": true,
  "m3_adult_not_chibi": true,
  "m4_silhouette_readable": true,
  "m5_sufficient_detail": true,
  "m6_matches_brief": true,
  "overall_pass": true,
  "confidence": 0.8,
  "issues": ["short strings"],
  "summary": "one sentence"
}

Fail overall_pass if obvious grey box, European castle, chibi, or low-poly untextured kit."""


def build_prompt(model_id: str, meta: dict) -> str:
    return f"""You are a 3D model QA judge for Tides of Urashima — high-detail stylized Japanese coastal 3D (NOT chibi, NOT European fantasy, NOT untextured blocks).

Model ID: {model_id}
Category: {meta.get('category', '')}
Creative brief: {meta.get('bible', '')}

You receive FOUR turntable renders: front, side, back, three_quarter.

M1 — Obvious axis-aligned **block/cube** placeholder or untextured primitive?
M2 — Stylized **Japanese coastal** read — not European castle / generic MMORPG?
M3 — **Adult proportions** (head:body ~1:5) — not chibi?
M4 — **Silhouette readable** on three_quarter view?
M5 — **Enough geometric detail** for NPR hero asset — not a single low-poly lump?
M6 — Matches brief (costume/prop identity)?

{REVIEW_SCHEMA}"""


def _b64_image(path: Path) -> tuple[str, str]:
    data = path.read_bytes()
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    return mime, base64.standard_b64encode(data).decode("ascii")


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


def review_openai(prompt: str, images: list[tuple[str, str]]) -> dict:
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not key:
        return {"model": "openai/gpt-4o", "skipped": True, "reason": "OPENAI_API_KEY not set"}
    content: list[dict] = [{"type": "text", "text": prompt}]
    for label, (mime, b64) in zip(VIEWS, images):
        content.append({"type": "text", "text": f"View: {label}"})
        content.append({"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}})
    payload = {
        "model": "gpt-4o",
        "max_tokens": 900,
        "messages": [{"role": "user", "content": content}],
    }
    data = _http_json(
        "https://api.openai.com/v1/chat/completions",
        {"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        payload,
    )
    text = data["choices"][0]["message"]["content"]
    parsed = _parse_json_response(text)
    parsed["model"] = "openai/gpt-4o"
    return parsed


def review_gemini(prompt: str, images: list[tuple[str, str]]) -> dict:
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key:
        return {"model": "google/gemini-2.0-flash", "skipped": True, "reason": "GEMINI_API_KEY not set"}
    parts: list[dict] = [{"text": prompt}]
    for label, (mime, b64) in zip(VIEWS, images):
        parts.append({"text": f"View: {label}"})
        parts.append({"inline_data": {"mime_type": mime, "data": b64}})
    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {"maxOutputTokens": 900},
    }
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}"
    data = _http_json(url, {"Content-Type": "application/json"}, payload)
    text = data["candidates"][0]["content"]["parts"][0]["text"]
    parsed = _parse_json_response(text)
    parsed["model"] = "google/gemini-2.0-flash"
    return parsed


def review_anthropic(prompt: str, images: list[tuple[str, str]]) -> dict:
    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not key:
        return {"model": "anthropic/claude-sonnet-4-20250514", "skipped": True, "reason": "ANTHROPIC_API_KEY not set"}
    content: list[dict] = []
    for label, (mime, b64) in zip(VIEWS, images):
        media = "image/png" if mime == "image/png" else "image/jpeg"
        content.append(
            {
                "type": "image",
                "source": {"type": "base64", "media_type": media, "data": b64},
            }
        )
        content.append({"type": "text", "text": f"View: {label}"})
    content.append({"type": "text", "text": prompt})
    payload = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 900,
        "messages": [{"role": "user", "content": content}],
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
    return parsed


REVIEWERS = {"openai": review_openai, "gemini": review_gemini, "anthropic": review_anthropic}


def main() -> int:
    ap = argparse.ArgumentParser(description="Model turntable vision jury (MODEL_QA.md)")
    ap.add_argument("--model", required=True)
    ap.add_argument("--turntable-dir", type=Path, default=None)
    ap.add_argument("--models", default="openai,anthropic,gemini")
    ap.add_argument("--min-pass", type=int, default=2)
    ap.add_argument("--out-dir", type=Path, default=ROOT / "artifacts/model_reviews")
    args = ap.parse_args()

    catalog = load_catalog()
    if args.model not in catalog["models"]:
        raise SystemExit(f"Unknown model: {args.model}")

    meta = catalog["models"][args.model]
    tdir = args.turntable_dir or (ROOT / "artifacts/model_reviews" / args.model)
    images: list[tuple[str, str]] = []
    for view in VIEWS:
        path = tdir / f"{view}.png"
        if not path.is_file():
            print(f"Missing turntable view: {path}", file=sys.stderr)
            return 2
        images.append(_b64_image(path))

    prompt = build_prompt(args.model, meta)
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": args.model,
        "turntable_dir": str(tdir),
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
            result = fn(prompt, images)
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
        ok = bool(result.get("overall_pass"))
        if ok:
            passed += 1
        print(f"[{'PASS' if ok else 'FAIL'}] {result.get('model', name)}: {result.get('summary', '')}")

    out_path = args.out_dir / f"{args.model}.model_jury.json"
    report["active_models"] = active
    report["passed_models"] = passed
    report["consensus_pass"] = active >= args.min_pass and passed >= args.min_pass
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nWrote {out_path}")

    if active == 0:
        manual = args.out_dir / f"{args.model}.model_manual.json"
        manual.write_text(
            json.dumps(
                {
                    "mode": "manual_model_jury",
                    "model": args.model,
                    "turntable_dir": str(tdir),
                    "prompt": prompt,
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        print(f"No API keys. Manual jury: {manual}")
        return 2
    if report["consensus_pass"]:
        print(f"CONSENSUS PASS ({passed}/{active})")
        return 0
    print(f"CONSENSUS FAIL ({passed}/{active}, need {args.min_pass})")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
