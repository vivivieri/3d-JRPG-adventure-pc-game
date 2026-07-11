#!/usr/bin/env python3
"""Generate structured remediation brief from QA jury JSON or technical checks.

docs/QA_REMEDIATION_LOOP.md — prevents infinite retry with same pipeline.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

PLAYBOOK_PATH = ROOT / "game/data/qa/remediation_playbook.json"

# Jury criterion keys → playbook keys
VISUAL_KEYS = (
    "v1_primitives_visible",
    "v2_muted_palette",
    "v3_npr_not_pbr",
    "v4_japanese_coastal",
    "v5_silhouette_readable",
    "v6_ui_clean",
)
MODEL_KEYS = (
    "m1_not_block_primitive",
    "m2_japanese_coastal_style",
    "m3_adult_not_chibi",
    "m4_silhouette_readable",
    "m5_sufficient_detail",
    "m6_matches_brief",
)
AUDIO_KEYS = (
    "a1_not_cheap_procedural",
    "a2_melancholy_coastal",
    "a3_not_upbeat_pop",
    "a4_instrumental_no_vocals",
    "a5_fits_scene_mood",
)

TECH_PATTERN_MAP = [
    (re.compile(r"tris.*below|below.*min|too few tris", re.I), "tris_below_min"),
    (re.compile(r"tris.*above|above.*max|too many tris", re.I), "tris_above_max"),
    (re.compile(r"texture", re.I), "textures_missing"),
    (re.compile(r"greybox|kenney|banned", re.I), "greybox_banned"),
    (re.compile(r"too small|likely empty|100 KB", re.I), "file_too_small"),
    (re.compile(r"LUFS|loudness", re.I), "lufs_out_of_range"),
    (re.compile(r"peak|clip", re.I), "peak_too_hot"),
    (re.compile(r"placeholder|generate_game_audio", re.I), "placeholder_audio"),
    (re.compile(r"palette|color distance|muted", re.I), "palette_drift"),
    (re.compile(r"BoxMesh|CapsuleMesh|primitive", re.I), "primitives_in_scene"),
]

DATA_ERROR_MAP = [
    (re.compile(r"unknown flag|sets unknown flag|requires unknown flag", re.I), "unknown_flag"),
    (re.compile(r"missing dialogue|references missing dialogue", re.I), "missing_dialogue"),
    (re.compile(r"unknown item|grants unknown|requires unknown item|Shop unknown", re.I), "unknown_item"),
    (re.compile(r"unknown enemy", re.I), "unknown_enemy"),
    (re.compile(r"cinematic_hook", re.I), "broken_cinematic_hook"),
    (re.compile(r"voice_id|vo_tier|vo_prompts", re.I), "vo_catalog_mismatch"),
]


def load_playbook() -> dict:
    return json.loads(PLAYBOOK_PATH.read_text(encoding="utf-8"))


def _failed_criteria_from_review(review: dict, keys: tuple[str, ...]) -> list[str]:
    failed = []
    for key in keys:
        val = review.get(key)
        if val is False:
            failed.append(key)
    return failed


def aggregate_jury_failures(report: dict) -> tuple[list[str], list[str], str]:
    """Return (failed_criteria, issue_strings, domain)."""
    reviews = [r for r in report.get("reviews", []) if not r.get("skipped") and not r.get("error")]
    if not reviews:
        return [], [], "unknown"

    # Detect domain from first review keys
    sample = reviews[0]
    if any(k in sample for k in VISUAL_KEYS):
        domain = "visual"
        keys = VISUAL_KEYS
    elif any(k in sample for k in MODEL_KEYS):
        domain = "model"
        keys = MODEL_KEYS
    elif any(k in sample for k in AUDIO_KEYS):
        domain = "audio"
        keys = AUDIO_KEYS
    else:
        # Audio jury may use custom keys — infer from issues text
        domain = "audio"
        keys = AUDIO_KEYS

    vote: dict[str, int] = {}
    all_issues: list[str] = []
    for rev in reviews:
        if rev.get("overall_pass"):
            continue
        for key in _failed_criteria_from_review(rev, keys):
            vote[key] = vote.get(key, 0) + 1
        for issue in rev.get("issues", []):
            if issue and issue not in all_issues:
                all_issues.append(str(issue))

    # Criterion failed in majority of failing models (or any if only 1 model)
    threshold = max(1, len([r for r in reviews if not r.get("overall_pass")]) // 2)
    failed = [k for k, c in vote.items() if c >= threshold]

    # Map audio jury freeform to playbook if no structured keys
    if domain == "audio" and not failed:
        text = " ".join(all_issues).lower()
        if "placeholder" in text or "sine" in text or "procedural" in text:
            failed.append("a1_not_cheap_procedural")
        elif "vocal" in text or "lyrics" in text:
            failed.append("a4_instrumental_no_vocals")
        elif "upbeat" in text or "edm" in text or "fanfare" in text:
            failed.append("a3_not_upbeat_pop")
        elif "mood" in text or "melanchol" in text or "coastal" in text:
            failed.append("a2_melancholy_coastal")

    return failed, all_issues, domain


def lookup_entries(playbook: dict, domain: str, codes: list[str]) -> list[dict]:
    section = playbook.get(domain, playbook.get("technical", {}))
    entries = []
    for code in codes:
        entry = section.get(code)
        if entry:
            entries.append({"code": code, **entry})
    return entries


def parse_technical_output(text: str) -> list[str]:
    codes: list[str] = []
    for line in text.splitlines():
        if "FAIL" not in line.upper():
            continue
        for pattern, code in TECH_PATTERN_MAP:
            if pattern.search(line) and code not in codes:
                codes.append(code)
    return codes


def run_technical_model(model_id: str) -> tuple[str, list[str]]:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools/check_model_technical.py"), "--model", model_id],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    codes = parse_technical_output(out)
    return out, codes


def run_technical_audio(track_id: str) -> tuple[str, list[str]]:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools/check_audio_technical.py"), "--track", track_id],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    codes = parse_technical_output(out)
    return out, codes


def parse_data_errors(text: str) -> list[str]:
    codes: list[str] = []
    for line in text.splitlines():
        for pattern, code in DATA_ERROR_MAP:
            if pattern.search(line) and code not in codes:
                codes.append(code)
    return codes


def run_validate_story() -> tuple[str, list[str]]:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools/validate_story_data.py")],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    issues = [ln.strip().lstrip("- ").strip() for ln in out.splitlines() if ln.strip().startswith("-")]
    codes = parse_data_errors(out)
    return out, codes, issues


def revision_log_path(asset_id: str, domain: str) -> Path:
    folder = {
        "visual": ROOT / "artifacts/visual_reviews",
        "model": ROOT / "artifacts/model_reviews",
        "audio": ROOT / "artifacts/audio_reviews",
        "flow": ROOT / "artifacts/flow_reviews",
        "data": ROOT / "artifacts/data_reviews",
    }.get(domain, ROOT / "artifacts/qa_reviews")
    return folder / asset_id / "revision_log.json"


def load_revision_log(path: Path) -> dict:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"asset_id": path.parent.name, "attempts": []}


def warn_repeat_lever(log: dict, lever: str, rules: dict) -> list[str]:
    warnings = []
    same = [a for a in log.get("attempts", []) if a.get("lever_changed") == lever]
    max_same = rules.get("max_same_lever_class", 2)
    if len(same) >= max_same:
        warnings.append(
            f"BLOCK: lever '{lever}' used {len(same)} times — must switch lever class or tool_tier (QA_REMEDIATION_LOOP.md §6)"
        )
    total = len(log.get("attempts", []))
    max_total = rules.get("max_attempts_per_asset", 3)
    if total >= max_total:
        warnings.append(
            f"ESCALATE: {total} attempts logged — human L6 or different primary tool required"
        )
    return warnings


def format_brief(
    asset_id: str,
    domain: str,
    failed_codes: list[str],
    entries: list[dict],
    issues: list[str],
    attempt_num: int,
    warnings: list[str],
) -> str:
    lines = [
        f"# QA Remediation Brief — {asset_id}",
        "",
        f"**Domain:** {domain}  ",
        f"**Attempt:** {attempt_num}  ",
        f"**Generated:** {datetime.now(timezone.utc).isoformat()}  ",
        "",
        "## Failed criteria",
        "",
    ]
    if failed_codes:
        for c in failed_codes:
            lines.append(f"- `{c}`")
    else:
        lines.append("- (see jury issues below)")
    lines.append("")

    if issues:
        lines.append("## Jury / lint issues")
        lines.append("")
        for i in issues[:8]:
            lines.append(f"- {i}")
        lines.append("")

    if warnings:
        lines.append("## Stop-rule warnings")
        lines.append("")
        for w in warnings:
            lines.append(f"- **{w}**")
        lines.append("")

    lines.append("## Required actions (change ONE lever this attempt)")
    lines.append("")
    levers_seen: set[str] = set()
    for entry in entries:
        code = entry.get("code", "")
        lever = entry.get("lever", "unknown")
        levers_seen.add(lever)
        lines.append(f"### `{code}` — lever: `{lever}`")
        lines.append("")
        lines.append(f"**Root cause:** {entry.get('root_cause', '')}")
        lines.append("")
        lines.append("**Do not repeat:**")
        lines.append(f"- {entry.get('do_not_repeat', '')}")
        lines.append("")
        lines.append("**Actions:**")
        for i, act in enumerate(entry.get("actions", []), 1):
            lines.append(f"{i}. {act}")
        lines.append("")
        lines.append(f"**Escalate if still failing:** {entry.get('escalate', '')}")
        lines.append("")

    if len(levers_seen) > 1:
        lines.append(
            "> Pick **one** lever class for this attempt. Do not combine prompt + mesh_ops in the same retry."
        )
        lines.append("")

    lines.append("## Next QA commands")
    lines.append("")
    if domain == "model":
        lines.extend(
            [
                "```bash",
                f"python3 tools/check_model_technical.py --model {asset_id}",
                f"python3 tools/render_model_turntable.py --model {asset_id}",
                f"python3 tools/review_model_vision.py --model {asset_id} --min-pass 2",
                "```",
            ]
        )
    elif domain == "visual":
        lines.extend(
            [
                "```bash",
                "bash tools/check_scene_visuals.sh",
                "python3 tools/check_screenshot_palette.py --zone <zone> --screenshot <png>",
                "python3 tools/review_screenshot_vision.py --screenshot <png> --zone <zone> --min-pass 2",
                "```",
            ]
        )
    elif domain == "audio":
        lines.extend(
            [
                "```bash",
                f"python3 tools/check_audio_technical.py --track {asset_id}",
                f"python3 tools/review_audio_vision.py --track {asset_id} --min-pass 2",
                "```",
            ]
        )
    elif domain == "data":
        lines.extend(
            [
                "```bash",
                "python3 tools/validate_story_data.py",
                "bash tools/run_unit_tests.sh",
                "```",
            ]
        )
    elif domain == "flow":
        lines.extend(
            [
                "```bash",
                "python3 tools/validate_story_data.py",
                f"bash tools/run_integration_tests.sh  # includes {asset_id} when implemented",
                "bash tools/run_e2e_playthrough.sh    # Phase 6+",
                "```",
            ]
        )
    lines.append("")
    doc = "docs/QA_REMEDIATION_LOOP.md" if domain in ("visual", "model", "audio") else "docs/FLOW_QA.md"
    lines.append("---")
    lines.append(f"See `{doc}` for industry refs and stop rules.")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="QA remediation brief (QA_REMEDIATION_LOOP.md)")
    ap.add_argument("--jury", type=Path, help="Path to *.jury.json from review_*_vision.py")
    ap.add_argument("--technical-model", dest="tech_model", metavar="ID")
    ap.add_argument("--technical-audio", dest="tech_audio", metavar="TRACK")
    ap.add_argument("--validate-story", action="store_true", help="Run validate_story_data.py and brief")
    ap.add_argument("--flow-scenario", metavar="ID", help="L4/L5 scenario id e.g. INT-QUEST-01")
    ap.add_argument("--visual-palette", action="store_true", help="Brief for palette_drift technical fail")
    ap.add_argument("--scene-primitives", action="store_true", help="Brief for BoxMesh lint fail")
    ap.add_argument("--zone", default="ruined_village", help="Zone for visual palette brief")
    ap.add_argument("--out", type=Path, help="Write brief markdown to file")
    ap.add_argument(
        "--log-attempt",
        action="store_true",
        help="Append attempt to artifacts/*/revision_log.json",
    )
    ap.add_argument("--asset-id", help="Override asset id for revision log")
    args = ap.parse_args()

    if not PLAYBOOK_PATH.is_file():
        print(f"Playbook missing: {PLAYBOOK_PATH}", file=sys.stderr)
        return 2

    playbook = load_playbook()
    rules = playbook.get("iteration_rules", {})
    domain = "unknown"
    asset_id = args.asset_id or "unknown"
    failed_codes: list[str] = []
    issues: list[str] = []
    tech_output = ""

    if args.jury:
        if not args.jury.is_file():
            print(f"Jury file not found: {args.jury}", file=sys.stderr)
            return 2
        report = json.loads(args.jury.read_text(encoding="utf-8"))
        failed_codes, issues, domain = aggregate_jury_failures(report)
        asset_id = args.asset_id or args.jury.stem.replace(".jury", "")
        entries = lookup_entries(playbook, domain, failed_codes)
    elif args.tech_model:
        domain = "model"
        asset_id = args.tech_model
        tech_output, failed_codes = run_technical_model(args.tech_model)
        issues = [ln.strip() for ln in tech_output.splitlines() if "FAIL" in ln]
        entries = lookup_entries(playbook, "technical", failed_codes)
    elif args.tech_audio:
        domain = "audio"
        asset_id = args.tech_audio
        tech_output, failed_codes = run_technical_audio(args.tech_audio)
        issues = [ln.strip() for ln in tech_output.splitlines() if "FAIL" in ln]
        entries = lookup_entries(playbook, "technical", failed_codes)
    elif args.validate_story:
        domain = "data"
        asset_id = args.asset_id or "story_data"
        tech_output, failed_codes, issues = run_validate_story()
        if not issues:
            issues = [ln.strip() for ln in tech_output.splitlines() if "FAILED" in ln or "error" in ln.lower()]
        entries = lookup_entries(playbook, "data", failed_codes)
        if not entries and issues:
            entries = lookup_entries(playbook, "data", ["unknown_flag"])
    elif args.flow_scenario:
        domain = "flow"
        asset_id = args.flow_scenario
        failed_codes = [args.flow_scenario]
        issues = [f"Integration/E2E scenario {args.flow_scenario} failed"]
        entries = lookup_entries(playbook, "flow", failed_codes)
        if not entries:
            entries = lookup_entries(playbook, "flow", ["INT-FIELD-01"])
            failed_codes = ["INT-FIELD-01"]
    elif args.visual_palette:
        domain = "visual"
        asset_id = args.asset_id or args.zone
        failed_codes = ["palette_drift"]
        issues = [f"Palette check failed for zone {args.zone}"]
        entries = lookup_entries(playbook, "technical", failed_codes)
    elif args.scene_primitives:
        domain = "visual"
        asset_id = args.asset_id or "scene_visual_lint"
        failed_codes = ["primitives_in_scene"]
        issues = ["check_scene_visuals.sh reported primitive meshes in player-facing .tscn"]
        entries = lookup_entries(playbook, "technical", failed_codes)
    else:
        ap.print_help()
        return 2

    log_path = revision_log_path(asset_id, domain)
    log = load_revision_log(log_path)
    attempt_num = len(log.get("attempts", [])) + 1

    warnings: list[str] = []
    for entry in entries:
        warnings.extend(warn_repeat_lever(log, entry.get("lever", ""), rules))

    brief = format_brief(asset_id, domain, failed_codes, entries, issues, attempt_num, warnings)
    print(brief)

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(brief, encoding="utf-8")
        print(f"\nWrote {args.out}", file=sys.stderr)

    if args.log_attempt:
        primary_lever = entries[0].get("lever", "unknown") if entries else "unknown"
        log.setdefault("asset_id", asset_id)
        log.setdefault("domain", domain)
        log.setdefault("attempts", []).append(
            {
                "attempt": attempt_num,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "failed_criteria": failed_codes,
                "lever_changed": primary_lever,
                "issues": issues[:5],
                "jury": str(args.jury) if args.jury else None,
            }
        )
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text(json.dumps(log, indent=2), encoding="utf-8")
        print(f"\nLogged attempt {attempt_num} → {log_path}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
