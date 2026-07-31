#!/usr/bin/env python3
"""PM docs-pack preflight — dry-run resolve_docs for next_dispatch before workers.

Fails when packs are empty, paths missing, or protected docs exceed budget badly.
Writes artifacts/docs_preflight_report.json.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "artifacts/pm_orchestrator_report.json"
OUT = ROOT / "artifacts/docs_preflight_report.json"
BOARD = ROOT / "game/data/qa/sprint_board.json"
BUDGET = int(os.environ.get("AGENT_DOCS_BUDGET", "12000"))


def _role_for(agent: str) -> str:
    agent = (agent or "builder").replace("agent/", "")
    known = {
        "architect",
        "builder",
        "builder_zone",
        "builder_combat",
        "qa",
        "flow",
        "release",
        "visual",
        "pm",
        "narrative",
        "audio",
    }
    return agent if agent in known else "builder"


def _targets() -> list[dict]:
    targets: list[dict] = []
    if REPORT.is_file():
        data = json.loads(REPORT.read_text(encoding="utf-8"))
        for row in data.get("next_dispatch") or []:
            targets.append(
                {
                    "issue_id": row.get("issue_id") or row.get("id"),
                    "agent": row.get("agent") or row.get("agent_owner") or "builder",
                }
            )
    if not targets and BOARD.is_file():
        board = json.loads(BOARD.read_text(encoding="utf-8"))
        for issue in board.get("issues") or []:
            status = str(issue.get("status") or "").lower()
            if status in {"done", "closed", "cancelled", "canceled"}:
                continue
            if status in {"todo", "ready", "in_progress", "queued", "dispatched", ""}:
                targets.append(
                    {
                        "issue_id": issue.get("id"),
                        "agent": issue.get("agent_owner") or "builder",
                    }
                )
    # unique by issue
    seen: set[str] = set()
    out: list[dict] = []
    for t in targets:
        iid = str(t.get("issue_id") or "")
        if not iid or iid in seen:
            continue
        seen.add(iid)
        out.append(t)
    return out[:8]


def _run(role: str, issue: str) -> dict:
    report_path = ROOT / "artifacts" / f"docs_pack_{issue}.txt"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable,
        str(ROOT / "tools/resolve_docs.py"),
        role,
        "--issue",
        issue,
        "--budget",
        str(BUDGET),
        "--report",
        str(report_path),
        "--check",
    ]
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    stdout = proc.stdout or ""
    stderr = proc.stderr or ""
    lines = [ln for ln in stdout.splitlines() if ln.strip() and not ln.startswith("#")]
    tokens = None
    if report_path.is_file():
        for ln in report_path.read_text(encoding="utf-8").splitlines():
            if ln.startswith("tokens_kept_est:"):
                try:
                    tokens = int(ln.split(":", 1)[1].strip())
                except ValueError as exc:
                    print(f"[WARN] bad tokens_kept_est in {report_path}: {exc}", file=sys.stderr)
    deferred = [ln for ln in stdout.splitlines() if ln.startswith("# deferred")]
    return {
        "issue_id": issue,
        "role": role,
        "exit_code": proc.returncode,
        "paths": lines,
        "path_count": len(lines),
        "tokens_kept_est": tokens,
        "has_deferred": bool(deferred),
        "report": str(report_path.relative_to(ROOT)),
        "stderr": stderr.strip()[-500:],
        "stdout_head": "\n".join(stdout.splitlines()[:20]),
    }


def main() -> int:
    targets = _targets()
    results = []
    errors: list[str] = []
    warnings: list[str] = []
    for t in targets:
        iid = str(t["issue_id"])
        role = _role_for(str(t["agent"]))
        result = _run(role, iid)
        results.append(result)
        if result["exit_code"] != 0:
            errors.append(f"{iid}/{role}: resolve_docs --check failed")
        elif result["path_count"] < 2:
            errors.append(f"{iid}/{role}: pack too thin ({result['path_count']} paths)")
        if result.get("tokens_kept_est") and result["tokens_kept_est"] > BUDGET * 1.25:
            warnings.append(
                f"{iid}/{role}: tokens_kept_est {result['tokens_kept_est']} >> budget {BUDGET}"
            )
        # protected overflow: if BOOT missing from output
        if "docs/ops/BOOT.md" not in result["paths"] and "AGENTS.md" not in result["paths"]:
            errors.append(f"{iid}/{role}: boot docs missing from pack")

    payload = {
        "budget": BUDGET,
        "targets": len(targets),
        "results": results,
        "errors": errors,
        "warnings": warnings,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    for w in warnings:
        print(f"WARN: {w}")
    if errors:
        print("L0/PM docs_pack_preflight FAIL:")
        for e in errors:
            print(f"  - {e}")
        print(f"Report: {OUT}")
        return 1
    print(f"docs_pack_preflight PASS — {len(results)} dispatch target(s); report {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
