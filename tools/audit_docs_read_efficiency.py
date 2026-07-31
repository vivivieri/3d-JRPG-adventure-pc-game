#!/usr/bin/env python3
"""Audit AI agent docs-pack reading efficiency (resolve_docs budget + skim aids).

Measures load/routing efficiency — not comprehension quality.
Authority: docs/_meta/DOC_LIBRARY_ADR.md § pack thinning / next effort.

Examples:
  python3 tools/audit_docs_read_efficiency.py
  python3 tools/audit_docs_read_efficiency.py --budget 12000 --out artifacts/docs_read_efficiency_audit
"""
from __future__ import annotations

import argparse
import json
import statistics
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from apply_docs_skim_aids import (  # noqa: E402
    DOCS,
    SKIP_NAMES,
    SKIP_PREFIXES,
    is_hub,
    parse_fm,
    strip_fm,
    summary_weak,
)

BOARD = ROOT / "game/data/qa/sprint_board.json"
RESOLVE = ROOT / "tools" / "resolve_docs.py"


def _tokens(path: str) -> int:
    p = ROOT / path if not path.startswith("/") else Path(path)
    if path == "AGENTS.md":
        p = ROOT / "AGENTS.md"
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"[WARN] audit token read failed for {path}: {exc}", file=sys.stderr)
        return 0
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end > 0:
            fm = parse_fm(text[: end + 5])
            if fm.get("tokens_est", "").isdigit():
                return int(fm["tokens_est"])
            text = text[end + 5 :]
    return max(1, len(text) // 4)


def _library_stats() -> dict:
    hubs = 0
    leaves = 0
    leaf_toks: list[int] = []
    hub_toks: list[int] = []
    when_n = jump_n = good_sum = weak_sum = 0
    for path in sorted(DOCS.rglob("*.md")):
        rel = path.relative_to(DOCS).as_posix()
        if any(rel.startswith(p) for p in SKIP_PREFIXES):
            continue
        if path.name in SKIP_NAMES:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        fm, body = strip_fm(text)
        meta = parse_fm(fm)
        tok = int(meta["tokens_est"]) if meta.get("tokens_est", "").isdigit() else max(1, len(body) // 4)
        if is_hub(body):
            hubs += 1
            hub_toks.append(tok)
            continue
        leaves += 1
        leaf_toks.append(tok)
        if "## When to read" in body:
            when_n += 1
        if "## Jump to" in body:
            jump_n += 1
        if summary_weak(meta.get("summary", "")):
            weak_sum += 1
        else:
            good_sum += 1
    leaf_toks.sort()
    hub_toks.sort()

    def pctile(vals: list[int], p: float) -> int:
        if not vals:
            return 0
        idx = min(len(vals) - 1, max(0, int(round((len(vals) - 1) * p))))
        return vals[idx]

    return {
        "hubs": hubs,
        "leaves": leaves,
        "hub_tok_p50": pctile(hub_toks, 0.5),
        "leaf_tok_p50": pctile(leaf_toks, 0.5),
        "leaf_tok_p90": pctile(leaf_toks, 0.9),
        "leaf_tok_max": max(leaf_toks) if leaf_toks else 0,
        "leaves_ge_1000": sum(1 for t in leaf_toks if t >= 1000),
        "leaves_ge_1200": sum(1 for t in leaf_toks if t >= 1200),
        "skim_when_pct": round(100.0 * when_n / leaves, 1) if leaves else 0.0,
        "jump_pct": round(100.0 * jump_n / leaves, 1) if leaves else 0.0,
        "good_summary_pct": round(100.0 * good_sum / leaves, 1) if leaves else 0.0,
        "weak_summary_pct": round(100.0 * weak_sum / leaves, 1) if leaves else 0.0,
    }


def _roles_tasks() -> tuple[list[str], list[str]]:
    import yaml  # type: ignore

    data = yaml.safe_load((ROOT / "docs" / "INDEX.yaml").read_text(encoding="utf-8"))
    return sorted(data.get("roles") or {}), sorted(data.get("tasks") or {})


def _phase1_issues() -> list[str]:
    if not BOARD.is_file():
        return []
    data = json.loads(BOARD.read_text(encoding="utf-8"))
    out = []
    for row in data.get("issues") or []:
        iid = str(row.get("id") or "")
        if iid.startswith("P1-"):
            out.append(iid)
    return sorted(out)


def _resolve(role: str, budget: int, *, task: str | None = None, issue: str | None = None) -> dict:
    report = ROOT / "artifacts" / f"_eff_tmp_{role}_{task or issue or 'bare'}.json"
    report.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["python3", str(RESOLVE), role, "--budget", str(budget), "--report", str(report)]
    if task:
        cmd.extend(["--task", task])
    if issue:
        cmd.extend(["--issue", issue])
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if proc.returncode != 0 or not report.is_file():
        return {
            "role": role,
            "task": task,
            "issue": issue,
            "error": (proc.stderr or proc.stdout or "resolve failed")[:300],
        }
    data = json.loads(report.read_text(encoding="utf-8"))
    report.unlink(missing_ok=True)

    must = data.get("must_read") or []
    opt = data.get("optional") or []
    deferred = data.get("deferred") or []
    must_tok = sum(int(x.get("tokens_est") or 0) for x in must)
    opt_tok = sum(int(x.get("tokens_est") or 0) for x in opt)
    def_tok = sum(int(x.get("tokens_est") or 0) for x in deferred)
    loaded = int(data.get("tokens_kept_est") or (must_tok + opt_tok))

    def _skim_counts(rows: list[dict]) -> tuple[int, int, int]:
        when = jump = n = 0
        for row in rows:
            path = row.get("path") or ""
            p = ROOT / path if path != "AGENTS.md" else ROOT / "AGENTS.md"
            try:
                body = p.read_text(encoding="utf-8", errors="replace")
            except OSError as exc:
                print(f"[WARN] audit skim read failed for {path}: {exc}", file=sys.stderr)
                continue
            n += 1
            if "## When to read" in body:
                when += 1
            if "## Jump to" in body:
                jump += 1
        return when, jump, n

    when, jump, n = _skim_counts(must + opt)
    useful = 0
    for row in deferred:
        tip = (row.get("summary") or "").strip()
        if tip and not summary_weak(tip):
            useful += 1

    return {
        "role": data.get("role") or role,
        "role_requested": data.get("role_requested") or role,
        "task": data.get("task") or task,
        "issue": issue,
        "must_n": len(must),
        "opt_n": len(opt),
        "def_n": len(deferred),
        "must_tok": must_tok,
        "opt_tok": opt_tok,
        "def_tok": def_tok,
        "loaded_tok": loaded,
        "budget": budget,
        "budget_headroom": budget - loaded,
        "pct_budget": round(100.0 * loaded / budget, 1) if budget else 0.0,
        "loaded_skim_pct": round(100.0 * when / n, 1) if n else 0.0,
        "loaded_jump_pct": round(100.0 * jump / n, 1) if n else 0.0,
        "deferred_useful_pct": round(100.0 * useful / len(deferred), 1) if deferred else 100.0,
    }


def _scenarios(roles: list[str], tasks: list[str], issues: list[str]) -> list[tuple[str, str | None, str | None]]:
    out: list[tuple[str, str | None, str | None]] = []
    # Bare roles (core agents)
    for role in ("architect", "qa", "builder", "pm", "flow", "visual"):
        if role in roles:
            out.append((role, None, None))
    # Key tasks
    for task in (
        "acceptance_ci",
        "factory_bootstrap",
        "zone_lighting",
        "water_shader",
        "visual_qa",
        "combat_balance",
    ):
        if task not in tasks:
            continue
        role = "qa" if task == "acceptance_ci" else "architect" if task in {"factory_bootstrap", "water_shader"} else "builder"
        if task == "visual_qa":
            role = "visual"
        if task == "combat_balance":
            role = "builder"
        out.append((role, task, None))
    # Phase-1 issues under architect (stress remap + unions)
    for issue in issues:
        if issue <= "P1-05":
            out.append(("architect", None, issue))
    # Dedupe while preserving order
    seen: set[tuple[str, str | None, str | None]] = set()
    uniq = []
    for row in out:
        if row in seen:
            continue
        seen.add(row)
        uniq.append(row)
    return uniq


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--budget", type=int, default=12000)
    ap.add_argument(
        "--out",
        default="artifacts/docs_read_efficiency_audit",
        help="Output prefix (writes .json + .md)",
    )
    args = ap.parse_args()

    lib = _library_stats()
    # Approximate full active library tokens
    full_tok = 0
    for path in DOCS.rglob("*.md"):
        rel = path.relative_to(DOCS).as_posix()
        if any(rel.startswith(p) for p in SKIP_PREFIXES):
            continue
        full_tok += _tokens(f"docs/{rel}")
    full_tok += _tokens("AGENTS.md")

    roles, tasks = _roles_tasks()
    issues = _phase1_issues()
    samples = []
    errors = 0
    for role, task, issue in _scenarios(roles, tasks, issues):
        row = _resolve(role, args.budget, task=task, issue=issue)
        if row.get("error"):
            errors += 1
            print(f"[WARN] {role} task={task} issue={issue}: {row['error']}", file=sys.stderr)
            continue
        samples.append(row)

    if not samples:
        print("no samples", file=sys.stderr)
        return 1

    def avg(key: str) -> float:
        return round(statistics.mean(s[key] for s in samples), 1)

    over = [s for s in samples if s["budget_headroom"] < 0]
    worst = sorted(samples, key=lambda s: -s["loaded_tok"])[:8]
    best = sorted(samples, key=lambda s: -s["budget_headroom"])[:5]
    avg_loaded = avg("loaded_tok")
    compression = 1.0 - (avg_loaded / full_tok) if full_tok else 0.0

    payload = {
        "budget": args.budget,
        "library": lib,
        "full_library_tok_approx": full_tok,
        "compression_vs_full_library_avg": round(compression, 4),
        "roles_n": len(roles),
        "tasks_n": len(tasks),
        "samples_ok": len(samples),
        "samples_err": errors,
        "averages": {
            "must_tok": avg("must_tok"),
            "opt_tok": avg("opt_tok"),
            "loaded_tok": avg_loaded,
            "def_tok": avg("def_tok"),
            "budget_headroom": avg("budget_headroom"),
            "loaded_skim_pct": avg("loaded_skim_pct"),
            "loaded_jump_pct": avg("loaded_jump_pct"),
            "deferred_useful_pct": avg("deferred_useful_pct"),
        },
        "worst_loaded": worst,
        "best_headroom": best,
        "over_budget": over,
        "samples": samples,
    }

    out_prefix = Path(args.out)
    if not out_prefix.is_absolute():
        out_prefix = ROOT / out_prefix
    if out_prefix.suffix in {".json", ".md"}:
        out_prefix = out_prefix.with_suffix("")
    out_prefix.parent.mkdir(parents=True, exist_ok=True)
    json_path = Path(str(out_prefix) + ".json")
    md_path = Path(str(out_prefix) + ".md")

    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Docs read-efficiency audit",
        "",
        f"Budget: `{args.budget}` · Full active library ≈ `{full_tok}` tok",
        "",
        "## Library structure",
        "",
        f"- Hubs: {lib['hubs']} (p50 hub ≈ {lib['hub_tok_p50']} tok)",
        f"- Leaves: {lib['leaves']} (p50={lib['leaf_tok_p50']}, p90={lib['leaf_tok_p90']}, max={lib['leaf_tok_max']})",
        f"- Leaves ≥1000 / ≥1200: {lib['leaves_ge_1000']} / {lib['leaves_ge_1200']}",
        f"- When to read coverage: {lib['skim_when_pct']}%",
        f"- Jump to coverage: {lib['jump_pct']}%",
        f"- Good summary coverage: {lib['good_summary_pct']}% (weak {lib['weak_summary_pct']}%)",
        "",
        "## resolve_docs pack efficiency (avg across samples)",
        "",
        f"- Must-read: **{payload['averages']['must_tok']}** tok",
        f"- Optional kept: **{payload['averages']['opt_tok']}** tok",
        f"- Loaded total: **{payload['averages']['loaded_tok']}** tok "
        f"({round(100.0 * avg_loaded / args.budget, 1)}% of budget)",
        f"- Deferred: **{payload['averages']['def_tok']}** tok "
        f"(useful tips {payload['averages']['deferred_useful_pct']}%)",
        f"- Headroom: **{payload['averages']['budget_headroom']}** tok",
        f"- Compression vs full library: **{round(compression * 100, 1)}%** fewer tokens loaded",
        f"- Loaded docs with When/Jump: {payload['averages']['loaded_skim_pct']}% / "
        f"{payload['averages']['loaded_jump_pct']}%",
        "",
        f"Over budget packs: {len(over)}",
        "",
        "## Heaviest packs",
        "",
        "| Role | Task/Issue | Loaded | Must | Opt | Deferred | Headroom |",
        "|------|------------|--------|------|-----|----------|----------|",
    ]
    for s in worst:
        label = s.get("issue") or s.get("task") or "—"
        lines.append(
            f"| {s.get('role_requested') or s['role']} | {label} | {s['loaded_tok']} | "
            f"{s['must_tok']} | {s['opt_tok']} | {s['def_tok']} | {s['budget_headroom']} |"
        )
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append(
        "- This audit measures **load/routing** efficiency (`resolve_docs` + skim aids), "
        "not whether agents reason correctly from the pack."
    )
    lines.append(
        "- Session adherence (enforced): session gate seeds must_read via "
        "`log_docs_read.py --from-pack`; post-cycle runs "
        "`check_docs_pack_adherence.py --strict`."
    )
    lines.append("")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    def _display(path: Path) -> str:
        try:
            return str(path.resolve().relative_to(ROOT))
        except ValueError:
            return str(path)

    print(f"wrote {_display(json_path)}")
    print(f"wrote {_display(md_path)}")
    print(
        f"avg_loaded={avg_loaded} headroom={payload['averages']['budget_headroom']} "
        f"good_summary={lib['good_summary_pct']}% over_budget={len(over)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
