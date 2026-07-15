#!/usr/bin/env python3
"""Pre-delivery control gate — review before any outbound delivery.

Enforces that a delivery (e.g. Telegram report) only goes out when:
  1. configured automated checks PASS, and
  2. a human explicitly confirms (external channels default to a safe preview).

Every attempt (preview, sent, or held) writes an audit record. Reusable across
delivery activities via game/data/qa/delivery_control.json.
See docs/DELIVERY_CONTROL.md.

Library:  gate(kind, artifacts, metrics, confirmed=..., allow_metric_fail=...)
CLI:      python3 tools/predelivery_gate.py --kind playtest_telemetry \
             --artifact a.png --metric fail_count=0 --metric parse_errors=0 [--confirm]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "game/data/qa/delivery_control.json"

PASS = "PASS"
FAIL = "FAIL"
WARN = "WARN"

_OPS = {
    "==": lambda a, b: a == b,
    "!=": lambda a, b: a != b,
    "<=": lambda a, b: a <= b,
    ">=": lambda a, b: a >= b,
    "<": lambda a, b: a < b,
    ">": lambda a, b: a > b,
}


def load_config() -> dict[str, Any]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def _check_command(check: dict[str, Any]) -> tuple[str, str]:
    cmd = check["cmd"]
    try:
        proc = subprocess.run(cmd, shell=True, cwd=ROOT, capture_output=True, text=True, timeout=120)
    except Exception as exc:  # noqa: BLE001
        return FAIL, f"command error: {exc}"
    return (PASS, check.get("detail", cmd)) if proc.returncode == 0 else (FAIL, f"exit {proc.returncode}: {cmd}")


def _check_artifacts(required: list[str], artifacts: list[str]) -> tuple[str, str]:
    have = {Path(a).name for a in artifacts}
    missing = [r for r in required if r not in have]
    if missing:
        return FAIL, f"missing artifacts: {', '.join(missing)}"
    return PASS, f"{len(required)} required artifact(s) present"


def _check_metric(check: dict[str, Any], metrics: dict[str, Any], allow_metric_fail: bool) -> tuple[str, str]:
    field = check["field"]
    op = check.get("op", "==")
    expected = check.get("value")
    actual = metrics.get(field)
    if actual is None:
        return WARN, f"metric '{field}' not provided"
    ok = _OPS[op](actual, expected)
    if ok:
        return PASS, f"{field} {op} {expected} (actual {actual})"
    # Failing metric — may be overridable after human review.
    if check.get("severity") == "block_overridable" and allow_metric_fail:
        return WARN, f"{field}={actual} violates {op}{expected} — OVERRIDDEN (--allow-metric-fail)"
    return FAIL, f"{field}={actual} violates {op}{expected}"


def evaluate_delivery(
    kind: str,
    artifacts: list[str],
    metrics: dict[str, Any],
    config: dict[str, Any],
    allow_metric_fail: bool = False,
) -> dict[str, Any]:
    deliveries = config.get("deliveries", {})
    if kind not in deliveries:
        return {"kind": kind, "status": FAIL, "checks": [{"id": "known_delivery", "status": FAIL,
                "detail": f"unknown delivery kind '{kind}' (define it in delivery_control.json)"}]}
    spec = deliveries[kind]
    results: list[dict[str, Any]] = []
    for check in spec.get("checks", []):
        ctype = check.get("type")
        if ctype == "command":
            status, detail = _check_command(check)
        elif ctype == "artifacts_exist":
            status, detail = _check_artifacts(spec.get("required_artifacts", []), artifacts)
        elif ctype == "metric":
            status, detail = _check_metric(check, metrics, allow_metric_fail)
        else:
            status, detail = WARN, f"unknown check type '{ctype}'"
        results.append({"id": check.get("id", ctype), "status": status, "detail": detail})
    status = FAIL if any(r["status"] == FAIL for r in results) else PASS
    return {"kind": kind, "channel": spec.get("channel"), "status": status, "checks": results}


def _write_audit(record: dict[str, Any], config: dict[str, Any]) -> str | None:
    if not config.get("policy", {}).get("audit", True):
        return None
    audit_dir = ROOT / config.get("policy", {}).get("audit_dir", "artifacts/delivery_audit")
    audit_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = audit_dir / f"{ts}_{record['kind']}_{record['outcome']}.json"
    path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    latest = audit_dir / f"latest_{record['kind']}.json"
    latest.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return str(path.relative_to(ROOT))


def gate(
    kind: str,
    artifacts: list[str],
    metrics: dict[str, Any],
    *,
    confirmed: bool = False,
    allow_metric_fail: bool = False,
    actor: str | None = None,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Evaluate checks + confirmation policy. Returns dict with `allowed` and `reason`."""
    config = config or load_config()
    policy = config.get("policy", {})
    evaluation = evaluate_delivery(kind, artifacts, metrics, config, allow_metric_fail)

    channel = config.get("channels", {}).get(evaluation.get("channel") or "", {})
    require_conf = policy.get("require_confirmation", True) and channel.get("requires_confirmation", channel.get("external", False))

    checks_pass = evaluation["status"] == PASS
    if policy.get("block_on_fail", True) and not checks_pass:
        allowed, reason, outcome = False, "checks FAILED — delivery blocked", "blocked"
    elif require_conf and not confirmed:
        allowed, reason, outcome = False, "preview only — checks pass; re-run with --confirm to deliver", "preview"
    else:
        allowed, reason, outcome = True, "approved for delivery", "approved"

    record = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "kind": kind,
        "channel": evaluation.get("channel"),
        "actor": actor or "agent",
        "confirmed": confirmed,
        "allow_metric_fail": allow_metric_fail,
        "checks_status": evaluation["status"],
        "checks": evaluation["checks"],
        "artifacts": artifacts,
        "metrics": metrics,
        "allowed": allowed,
        "reason": reason,
        "outcome": outcome,
    }
    audit_path = _write_audit(record, config)
    record["audit_path"] = audit_path
    return record


def print_result(record: dict[str, Any]) -> None:
    icon = {PASS: "[PASS]", FAIL: "[FAIL]", WARN: "[WARN]"}
    print("=" * 64)
    print(f"Pre-delivery control — {record['kind']} → {record.get('channel')}")
    print("=" * 64)
    for c in record["checks"]:
        print(f"{icon.get(c['status'], '[??]')} {c['id']}: {c['detail']}")
    print("-" * 64)
    verdict = "APPROVED ✅" if record["allowed"] else "HELD ⛔"
    print(f"{verdict} — {record['reason']}")
    if record.get("audit_path"):
        print(f"audit: {record['audit_path']}")


def _parse_metric(pairs: list[str]) -> dict[str, Any]:
    metrics: dict[str, Any] = {}
    for p in pairs or []:
        if "=" not in p:
            continue
        k, v = p.split("=", 1)
        try:
            metrics[k] = int(v)
        except ValueError:
            try:
                metrics[k] = float(v)
            except ValueError:
                metrics[k] = v
    return metrics


def main() -> int:
    ap = argparse.ArgumentParser(description="Pre-delivery control gate.")
    ap.add_argument("--kind", required=True, help="delivery kind from delivery_control.json")
    ap.add_argument("--artifact", action="append", default=[], help="artifact path (repeatable)")
    ap.add_argument("--metric", action="append", default=[], help="metric as name=value (repeatable)")
    ap.add_argument("--confirm", action="store_true", help="approve external delivery (default: preview)")
    ap.add_argument("--allow-metric-fail", dest="allow_metric_fail", action="store_true",
                    help="override an overridable metric FAIL after human review")
    ap.add_argument("--actor", help="who is approving (audit)")
    args = ap.parse_args()

    record = gate(
        args.kind,
        args.artifact,
        _parse_metric(args.metric),
        confirmed=args.confirm,
        allow_metric_fail=args.allow_metric_fail,
        actor=args.actor,
    )
    print_result(record)
    return 0 if record["allowed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
