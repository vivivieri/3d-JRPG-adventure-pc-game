#!/usr/bin/env python3
"""Alignment audit engine — standard report, checklist, history, stakeholder dashboard.

Authority: docs/qa/ALIGNMENT_AUDIT.md
"""
from __future__ import annotations

import html
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "game/data/qa/alignment_audit_catalog.json"


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_catalog() -> dict[str, Any]:
    return load_json(CATALOG_PATH)


def _utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def git_branch() -> str:
    try:
        out = subprocess.check_output(
            ["bash", str(ROOT / "tools/git_branch_name.sh")],
            cwd=ROOT,
            text=True,
        )
        return out.strip() or "unknown"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def git_commit() -> str:
    try:
        return (
            subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True)
            .strip()
        )
    except subprocess.CalledProcessError:
        return "unknown"


def run_ci(branch: str) -> dict[str, Any]:
    script = "run_ci_checks.sh" if branch == "game/development" else "run_docs_ci_checks.sh"
    cmd = ["bash", str(ROOT / "tools" / script)]
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    output = (proc.stdout or "") + (proc.stderr or "")
    summary_m = re.search(r"==> Main CI summary: PASS=(\d+) FAIL=(\d+)", output)
    if not summary_m and "==> Game CI summary" in output:
        summary_m = re.search(r"==> Game CI summary: PASS=(\d+) FAIL=(\d+)", output)
    if summary_m:
        pass_n = int(summary_m.group(1))
        fail_n = int(summary_m.group(2))
    else:
        pass_n = len(re.findall(r"\[PASS\] (\S+)", output))
        fail_n = len(re.findall(r"\[FAIL\] (\S+)", output))
    skip_n = len(re.findall(r"\[SKIP\]", output))
    failed_ids = re.findall(r"\[FAIL\] (\S+)", output)
    passed_ids = re.findall(r"\[PASS\] (\S+)", output)
    return {
        "script": script,
        "exit_code": proc.returncode,
        "pass_count": pass_n,
        "fail_count": fail_n,
        "skip_count": skip_n,
        "passed_gate_ids": passed_ids,
        "failed_gate_ids": failed_ids,
        "pass_rate": round(pass_n / max(pass_n + fail_n, 1), 4),
        "output_tail": "\n".join(output.strip().splitlines()[-8:]),
    }


def parity_checks() -> dict[str, Any]:
    sr = load_json(ROOT / "game/data/code/scene_registry.json")
    enc_data = {
        e["id"]
        for e in load_json(ROOT / "game/data/encounters/story_encounters.json").get("encounters", [])
    }
    hooks_data = {
        h["id"] for h in load_json(ROOT / "game/data/story/cinematic_hooks.json").get("hooks", [])
    }
    enc_reg: set[str] = set()
    hook_reg: set[str] = set()
    for scene in sr.get("scenes", []):
        for node in scene.get("required_nodes", []):
            exp = node.get("export", {})
            if "encounter_id" in exp:
                enc_reg.add(exp["encounter_id"])
            if "hook_id" in exp:
                hook_reg.add(exp["hook_id"])

    flags = load_json(ROOT / "game/data/story/flags.json").get("flags", [])
    tutorial_flags = [f["id"] for f in flags if str(f.get("id", "")).startswith("tutorial_")]
    scenes = load_json(ROOT / "game/data/story/scenes.json").get("scenes", [])
    from_scenes = {
        f
        for s in scenes
        for f in s.get("sets_flags", [])
        if f.startswith("tutorial_")
    }
    dialogue_text = (ROOT / "game/data/dialogue/chapter_01.json").read_text(encoding="utf-8")
    from_dialogue = set(re.findall(r'"(tutorial_[a-z_]+)"', dialogue_text))
    from_enc: set[str] = set()
    for e in load_json(ROOT / "game/data/encounters/story_encounters.json").get("encounters", []):
        for f in e.get("on_win", {}).get("set_flags", []):
            if f.startswith("tutorial_"):
                from_enc.add(f)
    emitted = from_scenes | from_dialogue | from_enc
    missing_tutorials = sorted(set(tutorial_flags) - emitted)

    enc_ok = enc_reg == enc_data
    hooks_ok = hook_reg == hooks_data
    tutorials_ok = not missing_tutorials
    return {
        "encounters_registry": sorted(enc_reg),
        "encounters_data": sorted(enc_data),
        "encounters_ok": enc_ok,
        "hooks_registry": sorted(hook_reg),
        "hooks_data": sorted(hooks_data),
        "hooks_ok": hooks_ok,
        "tutorial_flags_expected": len(tutorial_flags),
        "tutorial_flags_emitted": len(emitted),
        "tutorial_flags_missing": missing_tutorials,
        "tutorials_ok": tutorials_ok,
        "parity_ok": enc_ok and hooks_ok and tutorials_ok,
    }


def stale_string_scan(catalog: dict[str, Any]) -> list[dict[str, Any]]:
    hits: list[dict[str, Any]] = []
    search_roots = [ROOT / "docs", ROOT / "game/data", ROOT / "tools"]
    patterns = catalog.get("stale_string_patterns", [])
    skip_files = {"game/data/qa/alignment_audit_catalog.json"}
    for root in search_roots:
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix not in {".md", ".json", ".py", ".gd", ".tscn"}:
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            rel = str(path.relative_to(ROOT))
            if rel in skip_files:
                continue
            for row in patterns:
                if re.search(row["pattern"], text, re.IGNORECASE):
                    hits.append(
                        {
                            "id": row["id"],
                            "severity": row["severity"],
                            "message": row["message"],
                            "path": rel,
                        }
                    )
    return hits


def _gate_passed(gate_id: str, ci: dict[str, Any]) -> bool:
    return gate_id in ci.get("passed_gate_ids", [])


def _metric_value(metric_id: str) -> float | int | None:
    if metric_id == "vo_hit_list":
        vo = load_json(ROOT / "game/data/audio/vo_prompts.json")
        return len(vo.get("clips", {}))
    if metric_id == "cinematic_hooks":
        return len(load_json(ROOT / "game/data/story/cinematic_hooks.json").get("hooks", []))
    if metric_id == "encounters_catalogued":
        return len(
            load_json(ROOT / "game/data/encounters/story_encounters.json").get("encounters", [])
        )
    if metric_id == "zone_palette_rows":
        return len(load_json(ROOT / "game/data/world/zone_palettes.json").get("zones", []))
    return None


def _signal_score(signal: dict[str, Any], ctx: dict[str, Any]) -> float:
    kind = signal.get("kind", "")
    ci = ctx["ci"]
    parity = ctx["parity"]
    branch = ctx["branch"]
    domain_scores = ctx.get("domain_scores", {})

    if kind == "parity":
        sid = signal["id"]
        if sid == "scene_registry_parity":
            return 10.0 if parity["encounters_ok"] else 0.0
        if sid == "hooks_parity":
            return 10.0 if parity["hooks_ok"] else 0.0
        if sid == "tutorial_flags":
            return 10.0 if parity["tutorials_ok"] else 3.0
        return 5.0

    if kind == "gate":
        return 10.0 if _gate_passed(signal["id"], ci) else 0.0

    if kind == "gate_optional":
        gid = signal["id"]
        if gid in ci.get("failed_gate_ids", []):
            return 0.0
        if gid in ci.get("passed_gate_ids", []):
            return 10.0
        return 2.0 if branch == "main" else 4.0

    if kind == "metric":
        val = _metric_value(signal["id"])
        target = float(signal.get("target", 1))
        if val is None:
            return 5.0
        return min(10.0, round(10.0 * float(val) / target, 2))

    if kind == "file_exists":
        return 10.0 if (ROOT / signal["path"]).is_file() else 0.0

    if kind == "ci_rate":
        return round(float(ci.get("pass_rate", 0)) * 10.0, 2)

    if kind == "spec_status_cap":
        spec = load_json(ROOT / "game/data/code/spec_registry.json")
        if signal["id"] == "impl_shaders_partial":
            row = next((a for a in spec.get("artifacts", []) if a.get("id") == "impl_shaders"), {})
            status = row.get("spec_status", "not_started")
            if status == "specified":
                return 10.0
            if status == "partial":
                return float(signal.get("cap", 8.5))
            return 4.0
        if signal["id"] == "impl_scenes_not_started":
            if branch == "main":
                return float(signal.get("cap", 6.5))
            row = next((a for a in spec.get("artifacts", []) if a.get("id") == "impl_scenes"), {})
            st = row.get("spec_status", "not_started")
            if st == "specified":
                return 8.0
            if st == "partial":
                return 6.0
            return 4.0
        return 5.0

    if kind == "branch_impl":
        has_pg = (ROOT / "game/project.godot").is_file()
        if branch == "main":
            return 1.5 if not has_pg else 4.0
        return 8.0 if has_pg else 2.0

    if kind == "domain_ref":
        ref = domain_scores.get(signal["id"], 5.0)
        return float(ref)

    return 5.0


def compute_domain_scores(catalog: dict[str, Any], ctx: dict[str, Any]) -> dict[str, float]:
    scores: dict[str, float] = {}
    for domain in catalog.get("domains", []):
        if domain.get("derive") == "mean_siblings":
            continue
        total_w = 0.0
        acc = 0.0
        for sig in domain.get("signals", []):
            w = float(sig.get("weight", 1.0))
            total_w += w
            acc += w * _signal_score(sig, {**ctx, "domain_scores": scores})
        scores[domain["id"]] = round(acc / max(total_w, 1e-9), 2)

    siblings = [d["id"] for d in catalog.get("domains", []) if d.get("derive") != "mean_siblings"]
    if siblings:
        scores["overall_production"] = round(sum(scores[s] for s in siblings) / len(siblings), 2)
    return scores


def build_recommendations(
    catalog: dict[str, Any],
    *,
    ci: dict[str, Any],
    parity: dict[str, Any],
    stale: list[dict[str, Any]],
    domain_scores: dict[str, float],
    branch: str,
    report_visuals: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    recs: list[dict[str, Any]] = []
    stale_blocking = [h for h in stale if h["severity"] == "blocking"]
    stale_doc = [h for h in stale if h["severity"] == "doc_nit"]

    for rule in catalog.get("recommendation_rules", []):
        when = rule.get("when", "")
        include = False
        if when == "always":
            include = True
        elif when == "ci_fail_count_gt":
            include = ci.get("fail_count", 0) > int(rule.get("value", 0))
        elif when == "parity_fail":
            include = not parity.get("parity_ok", True)
        elif when == "stale_blocking":
            include = bool(stale_blocking)
        elif when == "stale_doc_nit":
            include = bool(stale_doc)
        elif when == "branch_is":
            include = branch == rule.get("value")
        elif when == "domain_score_lt":
            dom = rule.get("domain", "")
            include = domain_scores.get(dom, 10.0) < float(rule.get("value", 10.0))
        elif when == "domain_score_lt_on_branch":
            if branch != rule.get("branch"):
                include = False
            else:
                dom = rule.get("domain", "")
                include = domain_scores.get(dom, 10.0) < float(rule.get("value", 10.0))
        elif when == "visuals_missing":
            min_present = int(rule.get("min_present", 1))
            present = sum(1 for v in (report_visuals or []) if v.get("present"))
            include = present < min_present

        if not include:
            continue
        recs.append(
            {
                "id": rule["id"],
                "priority": rule.get("priority", "P2"),
                "category": rule.get("category", "implementation"),
                "title": rule["title"],
                "action": rule["action"],
                "status": "open",
            }
        )

    # De-duplicate by id
    seen: set[str] = set()
    unique: list[dict[str, Any]] = []
    for r in recs:
        if r["id"] in seen:
            continue
        seen.add(r["id"])
        unique.append(r)
    order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    unique.sort(key=lambda x: (order.get(x["priority"], 9), x["id"]))
    return unique


def build_checklist(recommendations: list[dict[str, Any]], catalog: dict[str, Any]) -> dict[str, Any]:
    sections = catalog.get("checklist_template", {}).get("sections", [])
    by_cat: dict[str, list[dict[str, Any]]] = {s["id"]: [] for s in sections}
    for rec in recommendations:
        cat = rec.get("category", "implementation")
        if cat not in by_cat:
            by_cat[cat] = []
        by_cat[cat].append(rec)

    checklist_sections = []
    for sec in sections:
        items = by_cat.get(sec["id"], [])
        checklist_sections.append(
            {
                "id": sec["id"],
                "label": sec["label"],
                "must_clear_before_dispatch": sec.get("must_clear_before_dispatch", False),
                "items": items,
                "open_count": sum(1 for i in items if i.get("status") == "open"),
            }
        )
    blocking_open = sum(
        s["open_count"] for s in checklist_sections if s.get("must_clear_before_dispatch")
    )
    return {
        "sections": checklist_sections,
        "total_open": sum(s["open_count"] for s in checklist_sections),
        "blocking_open": blocking_open,
    }


def compute_verdict(
    catalog: dict[str, Any],
    *,
    ci: dict[str, Any],
    domain_scores: dict[str, float],
    checklist: dict[str, Any],
) -> str:
    th = catalog.get("verdict_thresholds", {})
    if th.get("fail_any_ci") and ci.get("fail_count", 0) > 0:
        return "FAIL"
    if checklist.get("blocking_open", 0) > int(th.get("aligned_max_blocking", 0)):
        return "AT_RISK"
    overall = domain_scores.get("overall_production", 0.0)
    if overall >= float(th.get("aligned_min_overall", 8.0)):
        return "ALIGNED"
    if overall >= float(th.get("at_risk_min_overall", 6.5)):
        return "AT_RISK"
    return "FAIL"


def scan_visual_inventory(catalog: dict[str, Any], source_dir: Path | None = None) -> list[dict[str, Any]]:
    """Check which catalogued visuals exist on disk (no copy)."""
    manifest: list[dict[str, Any]] = []
    for pack in catalog.get("visual_packs", []):
        for asset in pack.get("assets", []):
            fname = asset["filename"]
            src: Path | None = None
            if source_dir:
                candidate = source_dir / fname
                if not candidate.is_absolute():
                    candidate = ROOT / candidate
                if candidate.is_file():
                    src = candidate
            elif (ROOT / "docs/compliance/alignment_audit_visuals" / fname).is_file():
                src = ROOT / "docs/compliance/alignment_audit_visuals" / fname
            manifest.append(
                {
                    "pack_id": pack["id"],
                    "asset_id": asset["id"],
                    "label": asset["label"],
                    "filename": fname,
                    "present": src is not None,
                    "path": str(src.relative_to(ROOT)) if src else None,
                }
            )
    return manifest


def bundle_visuals(
    audit_dir: Path,
    catalog: dict[str, Any],
    source_dir: Path | None,
) -> list[dict[str, Any]]:
    visuals_dir = audit_dir / catalog.get("outputs", {}).get("visuals_subdir", "visuals")
    visuals_dir.mkdir(parents=True, exist_ok=True)
    manifest: list[dict[str, Any]] = []
    for pack in catalog.get("visual_packs", []):
        for asset in pack.get("assets", []):
            fname = asset["filename"]
            dest = visuals_dir / fname
            copied = False
            if source_dir and (source_dir / fname).is_file():
                shutil.copy2(source_dir / fname, dest)
                copied = True
            elif (ROOT / "docs/compliance/alignment_audit_visuals" / fname).is_file():
                shutil.copy2(ROOT / "docs/compliance/alignment_audit_visuals" / fname, dest)
                copied = True
            manifest.append(
                {
                    "pack_id": pack["id"],
                    "pack_title": pack["title"],
                    "asset_id": asset["id"],
                    "label": asset["label"],
                    "kind": asset.get("kind", "concept"),
                    "filename": fname,
                    "path": str(dest.relative_to(ROOT)) if dest.is_file() else None,
                    "present": dest.is_file(),
                    "copied": copied,
                }
            )
    return manifest


def build_report(
    *,
    trigger: str = "manual",
    note: str | None = None,
    visuals_from: Path | None = None,
    skip_ci: bool = False,
) -> dict[str, Any]:
    catalog = load_catalog()
    branch = git_branch()
    commit = git_commit()
    ci = {"pass_count": 0, "fail_count": 0, "skip_count": 0, "passed_gate_ids": [], "failed_gate_ids": []}
    if not skip_ci:
        ci = run_ci(branch)
    parity = parity_checks()
    stale = stale_string_scan(catalog)
    ctx = {"ci": ci, "parity": parity, "branch": branch}
    domain_scores = compute_domain_scores(catalog, ctx)
    visual_inventory = scan_visual_inventory(catalog, visuals_from)
    recommendations = build_recommendations(
        catalog,
        ci=ci,
        parity=parity,
        stale=stale,
        domain_scores=domain_scores,
        branch=branch,
        report_visuals=visual_inventory,
    )
    checklist = build_checklist(recommendations, catalog)
    verdict = compute_verdict(catalog, ci=ci, domain_scores=domain_scores, checklist=checklist)

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    audit_id = f"{ts}_{trigger}"

    report: dict[str, Any] = {
        "schema_version": 1,
        "audit_id": audit_id,
        "generated_at": _utcnow(),
        "trigger": trigger,
        "note": note,
        "branch": branch,
        "commit": commit,
        "verdict": verdict,
        "headline": f"Alignment audit — {verdict} ({branch} @ {commit})",
        "domain_scores": domain_scores,
        "ci_summary": {
            "script": ci.get("script"),
            "pass_count": ci.get("pass_count"),
            "fail_count": ci.get("fail_count"),
            "skip_count": ci.get("skip_count"),
            "failed_gate_ids": ci.get("failed_gate_ids", []),
        },
        "parity": parity,
        "stale_string_hits": stale,
        "recommendations": recommendations,
        "checklist": checklist,
        "visual_manifest": [],
    }
    return report


def report_to_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Tides of Urashima — Alignment Audit Report",
        "",
        f"**{report.get('headline')}**",
        f"Generated: {report.get('generated_at')} · Audit ID: `{report.get('audit_id')}`",
        f"Branch: `{report.get('branch')}` · Commit: `{report.get('commit')}`",
        "",
        f"## Verdict: **{report.get('verdict')}**",
        "",
        "## Domain scores (0–10)",
        "",
        "| Domain | Score |",
        "|--------|-------|",
    ]
    for dom_id, score in sorted(report.get("domain_scores", {}).items(), key=lambda x: -x[1]):
        label = dom_id.replace("_", " ").title()
        lines.append(f"| {label} | {score} |")

    ci = report.get("ci_summary", {})
    lines.extend(
        [
            "",
            "## CI summary",
            f"- Script: `{ci.get('script')}`",
            f"- PASS: **{ci.get('pass_count')}** · FAIL: **{ci.get('fail_count')}** · SKIP: {ci.get('skip_count')}",
        ]
    )
    if ci.get("failed_gate_ids"):
        lines.append(f"- Failed gates: `{', '.join(ci['failed_gate_ids'])}`")

    parity = report.get("parity", {})
    lines.extend(
        [
            "",
            "## Data parity",
            f"- Encounters: {'OK' if parity.get('encounters_ok') else 'FAIL'}",
            f"- Hooks: {'OK' if parity.get('hooks_ok') else 'FAIL'}",
            f"- Tutorial flags: {'OK' if parity.get('tutorials_ok') else 'FAIL'}",
        ]
    )

    lines.extend(["", "## Recommendation checklist", ""])
    for sec in report.get("checklist", {}).get("sections", []):
        if not sec.get("items"):
            continue
        lines.append(f"### {sec['label']} ({sec['open_count']} open)")
        for item in sec["items"]:
            lines.append(f"- [ ] **{item['priority']}** {item['title']} — {item['action']}")
        lines.append("")

    stale = report.get("stale_string_hits", [])
    if stale:
        lines.append("## Stale string hits")
        for h in stale[:20]:
            lines.append(f"- `{h['path']}` — {h['message']} ({h['severity']})")
        lines.append("")

    visuals = [v for v in report.get("visual_manifest", []) if v.get("present")]
    if visuals:
        lines.append("## Stakeholder visuals")
        for v in visuals:
            lines.append(f"- {v['label']}: `{v.get('path')}`")
        lines.append("")

    lines.append("---")
    lines.append("Authority: `docs/qa/ALIGNMENT_AUDIT.md` · Re-run: `bash tools/run_alignment_audit.sh`")
    return "\n".join(lines) + "\n"


def render_html_dashboard(report: dict[str, Any]) -> str:
    esc = html.escape
    scores = report.get("domain_scores", {})
    max_score = 10.0
    bars = []
    for dom_id, score in sorted(scores.items(), key=lambda x: -x[1]):
        label = dom_id.replace("_", " ").title()
        pct = min(100, int(100 * float(score) / max_score))
        bars.append(
            f'<div class="score-row"><span class="label">{esc(label)}</span>'
            f'<div class="bar"><div style="width:{pct}%"></div></div>'
            f'<span class="val">{score}</span></div>'
        )

    checklist_html = []
    for sec in report.get("checklist", {}).get("sections", []):
        if not sec.get("items"):
            continue
        items = "".join(
            f'<li><span class="pri">{esc(i["priority"])}</span> <strong>{esc(i["title"])}</strong>'
            f'<br/><small>{esc(i["action"])}</small></li>'
            for i in sec["items"]
        )
        checklist_html.append(
            f'<div class="card"><h2>{esc(sec["label"])} ({sec["open_count"]})</h2><ul>{items}</ul></div>'
        )

    gallery = []
    for v in report.get("visual_manifest", []):
        if v.get("present") and v.get("path"):
            gallery.append(
                f'<figure><img src="{esc(v["path"])}" alt="{esc(v["label"])}"/>'
                f'<figcaption>{esc(v["label"])}</figcaption></figure>'
            )
        else:
            gallery.append(
                f'<figure class="missing"><div class="ph">{esc(v["label"])}</div>'
                f'<figcaption>missing — bundle with --visuals-from</figcaption></figure>'
            )

    verdict = report.get("verdict", "?")
    verdict_class = verdict.lower().replace("_", "-")
    data = json.dumps(report, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Tides of Urashima — Alignment Dashboard</title>
  <style>
    :root {{ font-family: system-ui, sans-serif; background: #1a1f2e; color: #e8ecf0; }}
    body {{ max-width: 1100px; margin: 0 auto; padding: 1.5rem; }}
    h1 {{ font-size: 1.35rem; color: #b8c8d8; }}
    .verdict {{ display: inline-block; padding: 0.25rem 0.75rem; border-radius: 4px; font-weight: 700; }}
    .verdict.aligned {{ background: #1e4d3a; color: #7dcea0; }}
    .verdict.at-risk {{ background: #4d3a1e; color: #d4a880; }}
    .verdict.fail {{ background: #4d1e1e; color: #e88; }}
    .score-row {{ display: grid; grid-template-columns: 140px 1fr 40px; gap: 0.5rem; align-items: center; margin: 0.35rem 0; }}
    .bar {{ background: #2a3344; border-radius: 4px; height: 10px; overflow: hidden; }}
    .bar > div {{ background: linear-gradient(90deg, #4ae8d8, #d4a880); height: 100%; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; margin: 1rem 0; }}
    .card {{ background: #242b3a; padding: 1rem; border-radius: 8px; border: 1px solid #3a4556; }}
    .card h2 {{ margin: 0 0 0.5rem; font-size: 0.85rem; color: #8b9daf; text-transform: uppercase; }}
    .card ul {{ margin: 0; padding-left: 1.2rem; font-size: 0.9rem; }}
    .pri {{ color: #4ae8d8; font-size: 0.75rem; }}
    .gallery {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 0.75rem; }}
    figure {{ margin: 0; background: #242b3a; border-radius: 6px; overflow: hidden; border: 1px solid #3a4556; }}
    figure img {{ width: 100%; height: 120px; object-fit: cover; display: block; }}
    figure .ph {{ height: 120px; display: flex; align-items: center; justify-content: center; color: #8b9daf; font-size: 0.8rem; padding: 0.5rem; text-align: center; }}
    figcaption {{ font-size: 0.7rem; padding: 0.35rem; color: #8b9daf; }}
    pre {{ background: #12161f; padding: 1rem; overflow: auto; font-size: 0.7rem; border-radius: 6px; max-height: 320px; }}
  </style>
</head>
<body>
  <h1>Tides of Urashima — Alignment Dashboard</h1>
  <p>{esc(report.get("headline", ""))}</p>
  <p><span class="verdict {verdict_class}">{esc(verdict)}</span>
     <small> · {esc(report.get("generated_at", ""))} · {esc(report.get("branch", ""))} @ {esc(report.get("commit", ""))}</small></p>

  <h2>Domain scores</h2>
  {"".join(bars)}

  <h2>Recommendation checklist</h2>
  <div class="grid">{"".join(checklist_html) or "<p>No open recommendations.</p>"}</div>

  <h2>Stakeholder visuals</h2>
  <div class="gallery">{"".join(gallery) or "<p>No visuals bundled.</p>"}</div>

  <h2>Raw JSON</h2>
  <pre id="data"></pre>
  <script>
    const report = {data};
    document.getElementById("data").textContent = JSON.stringify(report, null, 2);
  </script>
</body>
</html>
"""


def update_history_index(report: dict[str, Any], catalog: dict[str, Any], stamped_path: str) -> None:
    hist_path = ROOT / catalog.get("outputs", {}).get(
        "history_index", "docs/compliance/alignment_audit_history.json"
    )
    history = load_json(hist_path)
    if "audits" not in history:
        history = {
            "schema_version": 1,
            "authority": "docs/qa/ALIGNMENT_AUDIT.md",
            "audits": [],
        }
    entry = {
        "audit_id": report["audit_id"],
        "generated_at": report["generated_at"],
        "branch": report["branch"],
        "commit": report["commit"],
        "verdict": report["verdict"],
        "overall_score": report["domain_scores"].get("overall_production"),
        "ci_pass": report["ci_summary"]["pass_count"],
        "ci_fail": report["ci_summary"]["fail_count"],
        "blocking_open": report["checklist"]["blocking_open"],
        "recommendation_count": len(report["recommendations"]),
        "report_json": stamped_path,
    }
    history["audits"] = [a for a in history.get("audits", []) if a.get("audit_id") != entry["audit_id"]]
    history["audits"].append(entry)
    history["audits"].sort(key=lambda x: x.get("generated_at", ""))
    keep = int(catalog.get("outputs", {}).get("history_keep", 100))
    history["audits"] = history["audits"][-keep:]
    history["latest"] = entry
    save_json(hist_path, history)


def write_outputs(
    report: dict[str, Any],
    catalog: dict[str, Any],
    *,
    visuals_from: Path | None = None,
) -> dict[str, str]:
    outputs = catalog.get("outputs", {})
    out_dir = ROOT / outputs.get("artifacts_dir", "artifacts/alignment_audits")
    audit_dir = out_dir / report["audit_id"]
    audit_dir.mkdir(parents=True, exist_ok=True)

    report["visual_manifest"] = bundle_visuals(audit_dir, catalog, visuals_from)

    stamped_json = audit_dir / "report.json"
    save_json(stamped_json, report)

    latest_json = ROOT / outputs.get("latest_json", "artifacts/alignment_audits/latest.json")
    latest_md = ROOT / outputs.get("latest_markdown", "artifacts/alignment_audits/latest.md")
    latest_html = ROOT / outputs.get("latest_html", "artifacts/alignment_dashboard.html")

    save_json(latest_json, report)
    latest_md.write_text(report_to_markdown(report), encoding="utf-8")
    latest_html.write_text(render_html_dashboard(report), encoding="utf-8")

    # Copy markdown + html into stamped folder
    (audit_dir / "report.md").write_text(report_to_markdown(report), encoding="utf-8")
    (audit_dir / "dashboard.html").write_text(render_html_dashboard(report), encoding="utf-8")

    stamped_rel = str(stamped_json.relative_to(ROOT))
    update_history_index(report, catalog, stamped_rel)

    # Trim artifact history folders
    keep = int(outputs.get("history_keep", 100))
    dirs = sorted([d for d in out_dir.iterdir() if d.is_dir()], key=lambda p: p.name)
    for old in dirs[:-keep]:
        shutil.rmtree(old, ignore_errors=True)

    return {
        "json": str(latest_json.relative_to(ROOT)),
        "markdown": str(latest_md.relative_to(ROOT)),
        "html": str(latest_html.relative_to(ROOT)),
        "stamped": stamped_rel,
        "audit_dir": str(audit_dir.relative_to(ROOT)),
    }


def emit_audit(
    *,
    trigger: str = "manual",
    note: str | None = None,
    visuals_from: str | None = None,
    skip_ci: bool = False,
) -> dict[str, Any]:
    catalog = load_catalog()
    vdir = Path(visuals_from) if visuals_from else None
    report = build_report(trigger=trigger, note=note, visuals_from=vdir, skip_ci=skip_ci)
    paths = write_outputs(report, catalog, visuals_from=vdir)
    return {"report": report, "paths": paths}


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Run alignment audit and emit stakeholder report.")
    parser.add_argument("--trigger", default="manual", help="Audit trigger label")
    parser.add_argument("--note", default=None, help="Optional note in report")
    parser.add_argument("--visuals-from", default=None, help="Directory of PNG visuals to bundle")
    parser.add_argument("--skip-ci", action="store_true", help="Skip CI run (faster; scores approximate)")
    args = parser.parse_args(argv)

    result = emit_audit(
        trigger=args.trigger,
        note=args.note,
        visuals_from=args.visuals_from,
        skip_ci=args.skip_ci,
    )
    report = result["report"]
    paths = result["paths"]
    print(f"OK — verdict={report['verdict']} overall={report['domain_scores'].get('overall_production')}")
    print(f"  CI: PASS={report['ci_summary']['pass_count']} FAIL={report['ci_summary']['fail_count']}")
    print(f"  Checklist: {report['checklist']['total_open']} open ({report['checklist']['blocking_open']} blocking)")
    print(f"  JSON: {paths['json']}")
    print(f"  Markdown: {paths['markdown']}")
    print(f"  HTML: {paths['html']}")
    print(f"  History: docs/compliance/alignment_audit_history.json")
    return 0 if report["verdict"] != "FAIL" else 1


if __name__ == "__main__":
    sys.exit(main())
