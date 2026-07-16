#!/usr/bin/env python3
"""Pre-delivery control gate — review before any outbound delivery.

Enforces that a delivery (e.g. Telegram report) only goes out when:
  1. configured automated checks PASS, and
  2. the required number of reviewer approvals are recorded (default 1, by QA),
     with separation of duties (an approver cannot be the producer).

Reviewers are shown an explicit review checklist so they know exactly what to
inspect. Every action (request / review / approve / deliver) is audited.
Reusable across delivery activities via game/data/qa/delivery_control.json.
See docs/workflow/DELIVERY_CONTROL.md.

Flow:
  producer:  analyze_...  --telegram            # creates a review request, HOLDS (no send)
  reviewer:  predelivery_gate.py review  --request <id>            # shows checklist + checks
  reviewer:  predelivery_gate.py approve --request <id> --actor qa # records approval
  producer:  analyze_...  --telegram            # sees approval for same content -> delivers
"""
from __future__ import annotations

import argparse
import hashlib
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


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# --------------------------------------------------------------------------- #
# Checks
# --------------------------------------------------------------------------- #
def _check_command(check: dict[str, Any]) -> tuple[str, str]:
    try:
        proc = subprocess.run(check["cmd"], shell=True, cwd=ROOT, capture_output=True, text=True, timeout=120)
    except Exception as exc:  # noqa: BLE001
        return FAIL, f"command error: {exc}"
    return (PASS, check.get("detail", check["cmd"])) if proc.returncode == 0 else (FAIL, f"exit {proc.returncode}: {check['cmd']}")


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
    if _OPS[op](actual, expected):
        return PASS, f"{field} {op} {expected} (actual {actual})"
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
                "detail": f"unknown delivery kind '{kind}'"}]}
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


# --------------------------------------------------------------------------- #
# Request store (pending review handshake)
# --------------------------------------------------------------------------- #
def _audit_dir(config: dict[str, Any]) -> Path:
    return ROOT / config.get("policy", {}).get("audit_dir", "artifacts/delivery_audit")


def _pending_dir(config: dict[str, Any]) -> Path:
    d = _audit_dir(config) / "pending"
    d.mkdir(parents=True, exist_ok=True)
    return d


def request_id(kind: str, artifacts: list[str], metrics: dict[str, Any]) -> str:
    """Content-derived id — stable across re-runs with the same result set."""
    basis = json.dumps(
        {"kind": kind, "artifacts": sorted(Path(a).name for a in artifacts), "metrics": {k: metrics[k] for k in sorted(metrics)}},
        sort_keys=True,
    )
    return f"{kind}-{hashlib.sha256(basis.encode()).hexdigest()[:8]}"


def load_request(rid: str, config: dict[str, Any]) -> dict[str, Any] | None:
    path = _pending_dir(config) / f"{rid}.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None


def save_request(req: dict[str, Any], config: dict[str, Any]) -> None:
    (_pending_dir(config) / f"{req['request_id']}.json").write_text(json.dumps(req, indent=2) + "\n", encoding="utf-8")


def create_request(kind, artifacts, metrics, producer, context, config) -> dict[str, Any]:
    rid = request_id(kind, artifacts, metrics)
    existing = load_request(rid, config)
    if existing:
        return existing
    spec = config.get("deliveries", {}).get(kind, {})
    req = {
        "request_id": rid,
        "kind": kind,
        "channel": spec.get("channel"),
        "producer": producer,
        "context": context or {},
        "artifacts": artifacts,
        "metrics": metrics,
        "review_checklist": spec.get("review_checklist", []),
        "status": "pending_review",
        "approvals": [],
        "created_at": _now(),
    }
    save_request(req, config)
    return req


def review_text(req: dict[str, Any], config: dict[str, Any]) -> str:
    ev = evaluate_delivery(req["kind"], req["artifacts"], req["metrics"], config)
    lines = [
        "=" * 66,
        f"REVIEW — {req['kind']} → {req.get('channel')}  (request {req['request_id']})",
        "=" * 66,
        f"Producer: {req.get('producer')} · Status: {req.get('status')} · Approvals: {len(req.get('approvals', []))}",
        "",
        "Automated checks:",
    ]
    icon = {PASS: "[PASS]", FAIL: "[FAIL]", WARN: "[WARN]"}
    for c in ev["checks"]:
        lines.append(f"  {icon.get(c['status'], '[??]')} {c['id']}: {c['detail']}")
    lines += ["", "Artifacts to inspect:"]
    lines += [f"  - {a}" for a in req["artifacts"]] or ["  (none)"]
    lines += ["", "Review checklist (confirm each before approving):"]
    lines += [f"  [ ] {item}" for item in req.get("review_checklist", [])] or ["  (none defined)"]
    lines += ["", f"Approve with: python3 tools/predelivery_gate.py approve --request {req['request_id']} --actor <role>"]
    return "\n".join(lines)


def approve_request(rid: str, actor: str, allow_metric_fail: bool, config: dict[str, Any]) -> dict[str, Any]:
    req = load_request(rid, config)
    if not req:
        return {"ok": False, "reason": f"no such request '{rid}'"}
    approval = config.get("policy", {}).get("approval", {})
    reviewer_roles = approval.get("reviewer_roles", [])
    if reviewer_roles and actor not in reviewer_roles:
        return {"ok": False, "reason": f"actor '{actor}' is not an approved reviewer role {reviewer_roles}"}
    if approval.get("separation_of_duties", True) and actor == req.get("producer"):
        return {"ok": False, "reason": f"separation of duties: producer '{actor}' cannot approve their own delivery"}
    if any(a["actor"] == actor for a in req.get("approvals", [])):
        return {"ok": False, "reason": f"actor '{actor}' already approved this request"}

    ev = evaluate_delivery(req["kind"], req["artifacts"], req["metrics"], config, allow_metric_fail)
    if ev["status"] == FAIL:
        return {"ok": False, "reason": "checks currently FAIL — cannot approve", "checks": ev["checks"]}

    req["approvals"].append({"actor": actor, "at": _now(), "allow_metric_fail": allow_metric_fail})
    required = approval.get("required_approvals", 1)
    if len(req["approvals"]) >= required:
        req["status"] = "approved"
        req["approved_at"] = _now()
    save_request(req, config)
    return {"ok": True, "status": req["status"], "approvals": len(req["approvals"]), "required": required, "request": req}


def mark_delivered(rid: str, config: dict[str, Any]) -> None:
    req = load_request(rid, config)
    if req:
        req["status"] = "delivered"
        req["delivered_at"] = _now()
        save_request(req, config)


# --------------------------------------------------------------------------- #
# Audit
# --------------------------------------------------------------------------- #
def _write_audit(record: dict[str, Any], config: dict[str, Any]) -> str | None:
    if not config.get("policy", {}).get("audit", True):
        return None
    d = _audit_dir(config)
    d.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = d / f"{ts}_{record['kind']}_{record['outcome']}.json"
    path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return str(path.relative_to(ROOT))


# --------------------------------------------------------------------------- #
# High-level gate (used by producers, e.g. the telemetry analyzer)
# --------------------------------------------------------------------------- #
def gate(
    kind: str,
    artifacts: list[str],
    metrics: dict[str, Any],
    *,
    confirmed: bool = False,
    allow_metric_fail: bool = False,
    actor: str | None = None,
    context: dict[str, Any] | None = None,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    config = config or load_config()
    policy = config.get("policy", {})
    approval = policy.get("approval", {})
    required = approval.get("required_approvals", 0)
    producer = actor or "producer"

    evaluation = evaluate_delivery(kind, artifacts, metrics, config, allow_metric_fail)
    checks_pass = evaluation["status"] == PASS
    channel = config.get("channels", {}).get(evaluation.get("channel") or "", {})
    require_conf = policy.get("require_confirmation", True) and channel.get("requires_confirmation", channel.get("external", False))

    rid = request_id(kind, artifacts, metrics)
    reason = ""
    review_command = f"python3 tools/predelivery_gate.py review --request {rid}"

    if policy.get("block_on_fail", True) and not checks_pass:
        allowed, outcome, reason = False, "blocked", "checks FAILED — delivery blocked"
    elif required >= 1:
        # Reviewer-approval handshake (separation of duties).
        req = load_request(rid, config)
        if req and req.get("status") == "approved":
            allowed, outcome, reason = True, "approved", f"approved by {[a['actor'] for a in req['approvals']]}"
        elif req and req.get("status") == "delivered":
            allowed, outcome, reason = False, "already_delivered", "this exact report was already delivered"
        else:
            create_request(kind, artifacts, metrics, producer, context, config)
            allowed, outcome = False, "pending_review"
            reason = (f"awaiting {required} approval ({', '.join(approval.get('reviewer_roles', [])) or 'reviewer'}) "
                      f"— request {rid}; reviewer: {review_command}")
    elif require_conf and not confirmed:
        allowed, outcome, reason = False, "preview", "preview only — re-run with --confirm to deliver"
    else:
        allowed, outcome, reason = True, "approved", "approved for delivery"

    record = {
        "generated_at": _now(),
        "kind": kind,
        "channel": evaluation.get("channel"),
        "request_id": rid,
        "producer": producer,
        "checks_status": evaluation["status"],
        "checks": evaluation["checks"],
        "artifacts": artifacts,
        "metrics": metrics,
        "allowed": allowed,
        "outcome": outcome,
        "reason": reason,
        "review_command": review_command,
    }
    record["audit_path"] = _write_audit(record, config)
    return record


def print_result(record: dict[str, Any]) -> None:
    icon = {PASS: "[PASS]", FAIL: "[FAIL]", WARN: "[WARN]"}
    print("=" * 64)
    print(f"Pre-delivery control — {record['kind']} → {record.get('channel')}  (request {record['request_id']})")
    print("=" * 64)
    for c in record["checks"]:
        print(f"{icon.get(c['status'], '[??]')} {c['id']}: {c['detail']}")
    print("-" * 64)
    verdict = "APPROVED ✅" if record["allowed"] else "HELD ⛔"
    print(f"{verdict} — {record['reason']}")
    if record.get("audit_path"):
        print(f"audit: {record['audit_path']}")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def _parse_metric(pairs: list[str]) -> dict[str, Any]:
    metrics: dict[str, Any] = {}
    for p in pairs or []:
        if "=" not in p:
            continue
        k, v = p.split("=", 1)
        for cast in (int, float):
            try:
                metrics[k] = cast(v)
                break
            except ValueError:
                metrics[k] = v
    return metrics


def main() -> int:
    ap = argparse.ArgumentParser(description="Pre-delivery control gate.")
    sub = ap.add_subparsers(dest="command", required=True)

    ev = sub.add_parser("evaluate", help="evaluate checks + approval state for a delivery")
    ev.add_argument("--kind", required=True)
    ev.add_argument("--artifact", action="append", default=[])
    ev.add_argument("--metric", action="append", default=[])
    ev.add_argument("--actor")

    rv = sub.add_parser("review", help="show a pending request's checklist + checks for a reviewer")
    rv.add_argument("--request", required=True)

    ap_ = sub.add_parser("approve", help="record a reviewer approval for a request")
    ap_.add_argument("--request", required=True)
    ap_.add_argument("--actor", required=True, help="reviewer role (e.g. qa)")
    ap_.add_argument("--allow-metric-fail", dest="allow_metric_fail", action="store_true")

    st = sub.add_parser("status", help="print a request's status")
    st.add_argument("--request", required=True)

    args = ap.parse_args()
    config = load_config()

    if args.command == "evaluate":
        record = gate(args.kind, args.artifact, _parse_metric(args.metric), actor=args.actor, config=config)
        print_result(record)
        return 0 if record["allowed"] else 1

    if args.command == "review":
        req = load_request(args.request, config)
        if not req:
            print(f"No such request: {args.request}", file=sys.stderr)
            return 2
        print(review_text(req, config))
        return 0

    if args.command == "approve":
        res = approve_request(args.request, args.actor, args.allow_metric_fail, config)
        if not res["ok"]:
            print(f"[approve] REJECTED — {res['reason']}", file=sys.stderr)
            return 1
        print(f"[approve] {args.actor} approved {args.request} — status={res['status']} "
              f"({res['approvals']}/{res['required']})")
        if res["status"] == "approved":
            print("Delivery released — re-run the producer (e.g. analyze_playtest_telemetry.py --telegram) to send.")
        return 0

    if args.command == "status":
        req = load_request(args.request, config)
        if not req:
            print(f"No such request: {args.request}", file=sys.stderr)
            return 2
        print(json.dumps({k: req[k] for k in ("request_id", "kind", "status", "producer", "approvals")}, indent=2))
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
