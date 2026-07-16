#!/usr/bin/env python3
"""Escalate an issue up the anti-infinite-loop ladder and notify the Product Owner.

Ladder (game/data/qa/escalation_policy.json):
  dev<->QA (capped) -> arbitration (Architect / Design Authority) -> Product Owner.

Usage:
  # dev<->QA cap exceeded -> hand to the Architect/SA for arbitration:
  python3 tools/pm_escalate.py --issue P1-02 --to arbitration --reopens 3 --reason "QA keeps failing L2_feel_smoke"

  # arbitration can't resolve / needs a business decision -> Product Owner (Telegram):
  python3 tools/pm_escalate.py --issue P1-02 --to product_owner \
      --root-cause requirement_conflict --reason "PACING vs COMBAT specs conflict for SC-12"

  # record the Product Owner's decision when it comes back:
  python3 tools/pm_escalate.py --issue P1-02 --record-decision amend_requirement --by "product_owner" --rationale "cut SC-12 second wraith"

See docs/qa/ESCALATION_POLICY.md.
"""
from __future__ import annotations

import argparse
import html
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "game/data/qa/escalation_policy.json"

sys.path.insert(0, str(ROOT / "tools"))


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_policy() -> dict[str, Any]:
    return json.loads(POLICY_PATH.read_text(encoding="utf-8"))


def _tier(policy: dict[str, Any], tid: str) -> dict[str, Any]:
    return next((t for t in policy.get("ladder", []) if t.get("id") == tid), {})


def _record(policy: dict[str, Any], record: dict[str, Any]) -> str:
    out_dir = ROOT / policy.get("decision_record", {}).get("dir", "artifacts/escalations")
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = out_dir / f"{ts}_{record['issue_id']}_{record['tier']}.json"
    path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    (out_dir / f"latest_{record['issue_id']}.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return str(path.relative_to(ROOT))


def _notify_product_owner(policy: dict[str, Any], record: dict[str, Any]) -> tuple[bool, str]:
    import pm_stakeholder_report_lib as sr
    config = sr.load_config()
    po = _tier(policy, "product_owner")
    opts = " | ".join(po.get("decision_types", []))
    gh = config.get("repo_links", {}).get("github", "")
    lines = [
        "🛎️ <b>Tides of Urashima — Product Owner decision needed</b>",
        f"Issue: <b>{html.escape(record['issue_id'])}</b>",
        f"Escalated from: {html.escape(record.get('from_tier', 'arbitration'))}",
        f"Root cause: {html.escape(str(record.get('root_cause_class') or 'n/a'))}",
        f"Reason: {html.escape(record.get('reason', ''))}",
        f"Decision options: {html.escape(opts)}",
    ]
    if gh:
        lines.append(f'<a href="{html.escape(gh)}">GitHub</a>')
    return sr.send_telegram("\n".join(lines), config)


def main() -> int:
    ap = argparse.ArgumentParser(description="Escalate an issue up the ladder / notify Product Owner.")
    ap.add_argument("--issue", required=True)
    ap.add_argument("--to", choices=["arbitration", "product_owner"], help="tier to escalate to")
    ap.add_argument("--from-tier", dest="from_tier", help="tier being escalated from")
    ap.add_argument("--root-cause", dest="root_cause", help="root cause class (arbitration classification)")
    ap.add_argument("--reason", default="", help="short description of the dispute/blocker")
    ap.add_argument("--reopens", type=int, help="reopen count (for dev<->QA cap check)")
    ap.add_argument("--record-decision", dest="decision", help="record a Product Owner decision (a decision_type)")
    ap.add_argument("--by", help="who decided (for --record-decision)")
    ap.add_argument("--rationale", default="", help="decision rationale")
    ap.add_argument("--no-telegram", action="store_true", help="do not send Telegram (record only)")
    args = ap.parse_args()

    policy = load_policy()

    # Record a Product Owner decision coming back.
    if args.decision:
        po = _tier(policy, "product_owner")
        if args.decision not in po.get("decision_types", []):
            print(f"Invalid decision '{args.decision}'. Allowed: {po.get('decision_types')}", file=sys.stderr)
            return 2
        record = {
            "issue_id": args.issue, "tier": "product_owner", "root_cause_class": args.root_cause,
            "decision": args.decision, "decided_by": args.by or "product_owner",
            "rationale": args.rationale, "at": _now(),
        }
        path = _record(policy, record)
        print(f"[escalate] recorded PO decision '{args.decision}' for {args.issue} -> {path}")
        print("Next: PM applies the decision (amend design/data + reset acceptance) and re-dispatches, or closes.")
        return 0

    if not args.to:
        print("error: --to {arbitration|product_owner} or --record-decision required", file=sys.stderr)
        return 2

    # Validate root cause against policy (when escalating with a classification).
    if args.root_cause:
        classes = _tier(policy, "arbitration").get("classify_root_cause", [])
        if args.root_cause not in classes:
            print(f"Invalid root cause '{args.root_cause}'. Allowed: {classes}", file=sys.stderr)
            return 2

    dq_cap = _tier(policy, "dev_qa_loop").get("cap", {}).get("max_reopens")
    record = {
        "issue_id": args.issue, "tier": args.to, "from_tier": args.from_tier or ("dev_qa_loop" if args.to == "arbitration" else "arbitration"),
        "root_cause_class": args.root_cause, "reason": args.reason, "reopens": args.reopens,
        "status": "pending_decision" if args.to == "product_owner" else "pending_arbitration",
        "at": _now(),
    }
    path = _record(policy, record)

    if args.to == "arbitration":
        cap_note = ""
        if args.reopens is not None and dq_cap is not None and args.reopens >= dq_cap:
            cap_note = f" (reopen cap {dq_cap} reached)"
        print(f"[escalate] {args.issue} -> ARBITRATION{cap_note} — owner: Architect / Design Authority (SA)")
        print(f"           record: {path}")
        print("Architect: classify root cause, then resolve or escalate:product_owner. "
              "Only the arbiter/PO may change the requirement.")
        return 0

    # product_owner
    print(f"[escalate] {args.issue} -> PRODUCT OWNER — record: {path}")
    if args.no_telegram:
        print("[escalate] Telegram suppressed (--no-telegram).")
        return 0
    ok, detail = _notify_product_owner(policy, record)
    print(f"[escalate] Telegram to Product Owner: {'sent' if ok else 'FAILED'} — {detail}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
