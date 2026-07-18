#!/usr/bin/env python3
"""Champion/challenger tournament library — docs/qa/CANDIDATE_TOURNAMENT.md."""
from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
HARNESS_PATH = ROOT / "game/data/qa/golden_harness.json"
RUBRICS_PATH = ROOT / "game/data/qa/evaluation_rubrics.json"
POLICY_PATH = ROOT / "game/data/qa/candidate_tournament_policy.json"
ZONE_PATH = ROOT / "game/data/qa/zone_composition.json"
REGISTRY_PATH = ROOT / "artifacts/candidates/champion_registry.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def resolve_capture_path(scope: dict[str, Any], capture: dict[str, Any], manifest: dict[str, Any]) -> Path | None:
    captures = manifest.get("captures") or {}
    cap_id = capture.get("id", "")
    if cap_id in captures:
        return ROOT / captures[cap_id]
    if capture.get("path"):
        return ROOT / capture["path"]
    path_key = capture.get("path_key")
    if path_key:
        zone_id = scope.get("zone_composition_id", "")
        zones = load_json(ZONE_PATH).get("zones", {}) if ZONE_PATH.is_file() else {}
        zone_row = zones.get(zone_id, {})
        rel = zone_row.get(path_key)
        if rel:
            return ROOT / rel
    return None


def run_palette_check(palette_zone: str, screenshot: Path, thresholds: dict[str, float]) -> dict[str, Any]:
    cmd = [
        sys.executable,
        str(ROOT / "tools/check_screenshot_palette.py"),
        "--zone",
        palette_zone,
        "--screenshot",
        str(screenshot),
        "--max-avg-dist",
        str(thresholds.get("max_avg_anchor_dist", 85.0)),
        "--max-bright-ratio",
        str(thresholds.get("max_bright_ratio", 0.35)),
    ]
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    return {
        "command": " ".join(cmd),
        "exit_code": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
        "pass": proc.returncode == 0,
    }


def load_jury_report(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def jury_criterion_score(report: dict[str, Any] | None, domain: str, criterion_id: str) -> float | None:
    if not report:
        return None
    reviews = report.get("reviews") or []
    if not reviews and "acceptance" in report:
        reviews = [report]
    hits = 0
    total = 0
    for review in reviews:
        acceptance = review.get("acceptance") or {}
        results = acceptance.get("criteria_results") or {}
        if criterion_id in results:
            total += 1
            if results[criterion_id]:
                hits += 1
        elif criterion_id in review and isinstance(review[criterion_id], bool):
            total += 1
            if review[criterion_id]:
                hits += 1
    if total == 0:
        return None
    return hits / total


def jury_confidence_mean(report: dict[str, Any] | None) -> float | None:
    if not report:
        return None
    reviews = report.get("reviews") or []
    if not reviews and report.get("confidence") is not None:
        return float(report["confidence"])
    confs = [float(r.get("confidence", 0) or 0) for r in reviews if r.get("confidence") is not None]
    if not confs:
        return None
    return sum(confs) / len(confs)


def compute_soft_score(manifest: dict[str, Any], rubrics: dict[str, Any]) -> dict[str, Any]:
    jury_paths = manifest.get("jury") or {}
    axis_scores: dict[str, float] = {}
    weighted_sum = 0.0
    weight_total = 0.0

    for axis in rubrics.get("axes", []):
        axis_id = axis["id"]
        weight = float(axis.get("weight", 0))
        score: float | None = None

        if axis.get("source") == "jury_confidence_mean":
            confs: list[float] = []
            for report in jury_paths.values():
                val = jury_confidence_mean(load_jury_report(ROOT / report) if isinstance(report, str) else None)
                if val is not None:
                    confs.append(val)
            if confs:
                score = sum(confs) / len(confs)
        else:
            jury_map = axis.get("jury_criteria") or {}
            partials: list[float] = []
            for domain, criteria in jury_map.items():
                report_path = jury_paths.get(domain)
                report = load_jury_report(ROOT / report_path) if isinstance(report_path, str) else None
                for crit in criteria:
                    val = jury_criterion_score(report, domain, crit)
                    if val is not None:
                        partials.append(val)
            if partials:
                score = sum(partials) / len(partials)

        if score is not None:
            axis_scores[axis_id] = round(score, 4)
            weighted_sum += score * weight
            weight_total += weight

    overall = round(weighted_sum / weight_total, 4) if weight_total else 0.0
    return {"axis_scores": axis_scores, "soft_score": overall, "weight_applied": round(weight_total, 4)}


def gate_status(manifest: dict[str, Any], gate_id: str) -> str:
    gates = manifest.get("gates") or {}
    return str(gates.get(gate_id, "MISSING")).upper()


def check_hard_gates(manifest: dict[str, Any], hard_gates: list[str]) -> dict[str, Any]:
    results: dict[str, str] = {}
    failures: list[str] = []
    for gid in hard_gates:
        status = gate_status(manifest, gid)
        results[gid] = status
        if status != "PASS":
            failures.append(gid)
    return {
        "results": results,
        "pass": len(failures) == 0,
        "failures": failures,
    }


def run_harness_checks(scope_id: str, manifest: dict[str, Any], harness: dict[str, Any]) -> dict[str, Any]:
    scope = harness.get("scopes", {}).get(scope_id)
    if not scope:
        return {"pass": False, "error": f"unknown scope: {scope_id}", "captures": []}

    thresholds = harness.get("palette_thresholds", {})
    palette_zone = scope.get("palette_zone_key", scope_id)
    capture_results: list[dict[str, Any]] = []
    failures: list[str] = []

    for capture in scope.get("captures", []):
        path = resolve_capture_path(scope, capture, manifest)
        row: dict[str, Any] = {
            "id": capture.get("id"),
            "label": capture.get("label"),
            "path": str(path.relative_to(ROOT)) if path else None,
            "required": bool(capture.get("required_for_promotion", False)),
        }
        if not path or not path.is_file():
            row["status"] = "SKIP"
            row["pass"] = not row["required"]
            if row["required"]:
                failures.append(f"missing_required_capture:{capture.get('id')}")
        else:
            palette = run_palette_check(palette_zone, path, thresholds)
            row["palette_check"] = palette
            row["pass"] = palette["pass"]
            row["status"] = "PASS" if palette["pass"] else "FAIL"
            if not palette["pass"] and row["required"]:
                failures.append(f"palette_fail:{capture.get('id')}")
        capture_results.append(row)

    return {
        "scope_id": scope_id,
        "captures": capture_results,
        "pass": len(failures) == 0,
        "failures": failures,
    }


@dataclass
class ComparisonResult:
    scope_id: str
    issue_id: str
    champion: dict[str, Any] | None
    challenger: dict[str, Any]
    hard_gates: dict[str, Any]
    harness: dict[str, Any]
    challenger_soft: dict[str, Any]
    champion_soft: dict[str, Any] | None
    verdict: str
    promote: bool
    reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": "1.0",
            "generated_at": utc_now_iso(),
            "gate_id": "L2_candidate_select",
            "scope_id": self.scope_id,
            "issue_id": self.issue_id,
            "champion": self.champion,
            "challenger": {
                "label": self.challenger.get("label"),
                "commit_sha": self.challenger.get("commit_sha"),
                "agent_role": self.challenger.get("agent_role"),
            },
            "hard_gates": self.hard_gates,
            "golden_harness": self.harness,
            "soft_scores": {
                "challenger": self.challenger_soft,
                "champion": self.champion_soft,
            },
            "verdict": self.verdict,
            "promote_challenger": self.promote,
            "reasons": self.reasons,
        }


def load_registry(path: Path | None = None) -> dict[str, Any]:
    reg_path = path or REGISTRY_PATH
    if not reg_path.is_file():
        return {"version": "1.0", "champions": {}}
    return load_json(reg_path)


def get_champion(scope_id: str, registry: dict[str, Any] | None = None) -> dict[str, Any] | None:
    registry = registry or load_registry()
    return (registry.get("champions") or {}).get(scope_id)


def compare_champion_challenger(
    challenger: dict[str, Any],
    *,
    scope_id: str | None = None,
    registry: dict[str, Any] | None = None,
) -> ComparisonResult:
    harness = load_json(HARNESS_PATH)
    rubrics = load_json(RUBRICS_PATH)
    scope_id = scope_id or challenger.get("scope_id") or ""
    issue_id = challenger.get("issue_id", "")
    scope = harness.get("scopes", {}).get(scope_id, {})
    hard_gate_ids = scope.get("hard_gates", [])

    champion_row = get_champion(scope_id, registry)
    champion_manifest = champion_row if champion_row else None

    hard = check_hard_gates(challenger, hard_gate_ids)
    harness_result = run_harness_checks(scope_id, challenger, harness)
    challenger_soft = compute_soft_score(challenger, rubrics)
    champion_soft = compute_soft_score(champion_manifest, rubrics) if champion_manifest else None

    reasons: list[str] = []
    promote = False
    verdict = "reject_challenger"

    if not hard["pass"]:
        reasons.append(f"hard_gate_veto:{','.join(hard['failures'])}")
    elif not harness_result["pass"]:
        reasons.append(f"golden_harness_fail:{','.join(harness_result['failures'])}")
    elif champion_manifest is None:
        promote = True
        verdict = "promote_challenger"
        reasons.append("no_incumbent_champion")
    else:
        c_score = challenger_soft.get("soft_score", 0.0)
        k_score = (champion_soft or {}).get("soft_score", 0.0)
        if c_score > k_score:
            promote = True
            verdict = "promote_challenger"
            reasons.append(f"soft_score_win:{c_score}>{k_score}")
        elif c_score == k_score:
            verdict = "keep_champion"
            reasons.append(f"soft_score_tie:{c_score}=={k_score}")
        else:
            verdict = "keep_champion"
            reasons.append(f"soft_score_loss:{c_score}<{k_score}")

    return ComparisonResult(
        scope_id=scope_id,
        issue_id=issue_id,
        champion=champion_manifest,
        challenger=challenger,
        hard_gates=hard,
        harness=harness_result,
        challenger_soft=challenger_soft,
        champion_soft=champion_soft,
        verdict=verdict,
        promote=promote,
        reasons=reasons,
    )


def write_comparison_artifact(result: ComparisonResult, issue_id: str) -> Path:
    out_dir = ROOT / "artifacts/candidates" / issue_id
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_path = out_dir / f"comparison_{ts}.json"
    out_path.write_text(json.dumps(result.to_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return out_path
