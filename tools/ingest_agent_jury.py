#!/usr/bin/env python3
"""Agent-driven jury ingest — key-free alternative to review_*_vision.py.

Instead of calling external vision APIs (OPENAI/ANTHROPIC/GEMINI), a Cursor QA
agent produces one verdict JSON per model by dispatching >=2 subagents pinned to
distinct Cursor models (each reviews the asset with the Read tool and returns the
domain checklist). This tool ingests those verdicts, applies the SAME acceptance
logic as the API jury (qa_acceptance_lib.normalize_jury_review +
evaluate_jury_consensus), and writes the canonical <stem>.jury.json.

Integrity is identical to the API path: overall_pass is recomputed from the
measurable criteria (not the model's self-report), confidence floor is enforced,
and consensus still requires >= jury_min_pass_models distinct models to pass.

See docs/qa/AGENT_JURY.md and docs/qa/ACCEPTANCE_CRITERIA.md.

Exit codes: 0=CONSENSUS PASS, 1=CONSENSUS FAIL, 2=insufficient reviews (SKIP).
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from qa_acceptance_lib import (  # noqa: E402
    evaluate_jury_consensus,
    jury_rules,
    normalize_jury_review,
)

DEFAULT_OUT_DIR = {
    "visual": ROOT / "artifacts" / "visual_reviews",
    "model": ROOT / "artifacts" / "model_reviews",
    "audio": ROOT / "artifacts" / "audio_reviews",
    "vo": ROOT / "artifacts" / "vo_reviews",
}


def _load_review(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: verdict must be a JSON object")
    if not data.get("model"):
        raise ValueError(f"{path}: verdict missing required 'model' field")
    return data


def _collect_reviews(reviews_dir: Path | None, review_files: list[Path]) -> list[tuple[Path, dict]]:
    paths: list[Path] = []
    if reviews_dir is not None:
        paths.extend(sorted(p for p in reviews_dir.glob("*.json") if not p.name.endswith(".jury.json")))
    paths.extend(review_files)
    out: list[tuple[Path, dict]] = []
    for p in paths:
        if not p.is_file():
            print(f"[ERR]  verdict file not found: {p}", file=sys.stderr)
            continue
        out.append((p, _load_review(p)))
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest agent-produced jury verdicts (docs/qa/AGENT_JURY.md)")
    parser.add_argument("--domain", required=True, choices=sorted(DEFAULT_OUT_DIR))
    parser.add_argument("--asset", required=True, type=Path, help="Reviewed asset path (for stem + metadata)")
    parser.add_argument("--reviews-dir", type=Path, help="Directory of per-model verdict JSON files")
    parser.add_argument("--review", action="append", type=Path, default=[], help="A per-model verdict JSON (repeatable)")
    parser.add_argument("--out", type=Path, help="Output jury.json (default artifacts/<domain>_reviews/<stem>.jury.json)")
    parser.add_argument("--min-pass", type=int, help="Override minimum passing models")
    args = parser.parse_args()

    rules = jury_rules(args.domain)
    reviews_raw = _collect_reviews(args.reviews_dir, args.review)
    if not reviews_raw:
        print("[SKIP] no agent verdict files provided — see docs/qa/AGENT_JURY.md", file=sys.stderr)
        return 2

    seen_models: set[str] = set()
    normalized: list[dict] = []
    for path, raw in reviews_raw:
        model = str(raw.get("model"))
        if model in seen_models:
            print(f"[ERR]  duplicate model '{model}' ({path.name}) — jury needs DISTINCT models", file=sys.stderr)
            continue
        seen_models.add(model)
        review = normalize_jury_review(dict(raw), args.domain)
        normalized.append(review)
        ok = bool(review.get("acceptance", {}).get("valid_pass"))
        print(f"[{'PASS' if ok else 'FAIL'}] {model}: {review.get('summary', '')}")
        if not ok:
            acc = review.get("acceptance", {})
            failed = [k for k, v in acc.get("criteria_results", {}).items() if not v]
            if failed:
                print(f"       failed: {', '.join(failed)}")

    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "mode": "agent_jury",
        "domain": args.domain,
        "asset": str(args.asset),
        "min_pass": args.min_pass if args.min_pass is not None else rules.get("min_pass_models"),
        "reviews": normalized,
    }
    consensus = evaluate_jury_consensus(report, args.domain)
    report["acceptance"] = consensus
    report["active_models"] = consensus["active_models"]
    report["passed_models"] = consensus["passed_models"]
    report["consensus_pass"] = consensus["consensus_pass"]

    out_dir = args.out.parent if args.out else DEFAULT_OUT_DIR[args.domain]
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = args.out if args.out else out_dir / f"{args.asset.stem}.jury.json"
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nWrote {out_path}")

    if consensus["active_models"] < consensus["min_active_models"]:
        print(
            f"[SKIP] only {consensus['active_models']} distinct model(s) — "
            f"need >= {consensus['min_active_models']} (docs/qa/ACCEPTANCE_CRITERIA.md)",
            file=sys.stderr,
        )
        return 2

    if consensus["consensus_pass"]:
        print(f"CONSENSUS PASS ({consensus['passed_models']}/{consensus['active_models']} models, gate {consensus['gate_id']})")
        return 0

    print(f"CONSENSUS FAIL ({consensus['passed_models']}/{consensus['active_models']} models, gate {consensus['gate_id']})")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
