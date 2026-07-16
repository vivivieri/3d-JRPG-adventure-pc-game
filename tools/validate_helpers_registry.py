#!/usr/bin/env python3
"""Validate helpers_registry.json and cross-refs to autoload + reference libs."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CODE = ROOT / "game" / "data" / "code"
VALID_KINDS = frozenset({"autoload", "refcounted"})


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def signal_key(sig: str | dict) -> str:
    if isinstance(sig, dict):
        name = sig.get("name", "")
        args = sig.get("args", [])
        return f"{name}({', '.join(args)})"
    return str(sig)


def main() -> int:
    errors: list[str] = []
    helpers_path = CODE / "helpers_registry.json"
    if not helpers_path.is_file():
        print("HELPERS REGISTRY MISSING", file=sys.stderr)
        return 1

    registry = load_json(helpers_path)
    helpers = registry.get("helpers", [])
    helper_ids = {h.get("id") for h in helpers}
    order = registry.get("regeneration_order", [])

    if not order:
        errors.append("regeneration_order is empty")
    for hid in order:
        if hid not in helper_ids:
            errors.append(f"regeneration_order references unknown helper: {hid}")
    for hid in helper_ids:
        if hid and hid not in order:
            errors.append(f"helper {hid} missing from regeneration_order")

    for helper in helpers:
        hid = helper.get("id", "?")
        kind = helper.get("kind")
        if kind not in VALID_KINDS:
            errors.append(f"{hid}: invalid kind {kind!r}")

        gd_path = helper.get("gdscript_path", "")
        if not gd_path.startswith("res://scripts/core/"):
            errors.append(f"{hid}: gdscript_path must be res://scripts/core/*.gd")

        py_ref = helper.get("python_reference")
        if py_ref:
            full = ROOT / py_ref
            if not full.is_file():
                errors.append(f"{hid}: python_reference missing: {py_ref}")

        for rel in helper.get("data_ref", []) or []:
            if not (ROOT / rel).is_file():
                errors.append(f"{hid}: data_ref missing: {rel}")

        if kind == "autoload" and hid == "EventBus":
            signals = helper.get("signals", [])
            if not signals:
                errors.append("EventBus: signals list required")
            for sig in signals:
                if not isinstance(sig, dict) or not sig.get("name"):
                    errors.append(f"EventBus: invalid signal entry: {sig!r}")
        elif kind == "refcounted":
            api = helper.get("public_api", [])
            if not api:
                errors.append(f"{hid}: public_api required for refcounted helper")

    # Cross-check EventBus signals with autoload_registry
    autoload_path = CODE / "autoload_registry.json"
    if autoload_path.is_file():
        autoloads = load_json(autoload_path).get("autoloads", [])
        event_bus = next((a for a in autoloads if a.get("id") == "EventBus"), None)
        event_helper = next((h for h in helpers if h.get("id") == "EventBus"), None)
        if event_bus and event_helper:
            reg_sigs = {signal_key(s) for s in event_bus.get("signals", [])}
            help_sigs = {signal_key(s) for s in event_helper.get("signals", [])}
            if reg_sigs != help_sigs:
                missing_in_autoload = help_sigs - reg_sigs
                extra_in_autoload = reg_sigs - help_sigs
                if missing_in_autoload:
                    errors.append(
                        f"EventBus signals in helpers_registry not in autoload_registry: "
                        f"{sorted(missing_in_autoload)}"
                    )
                if extra_in_autoload:
                    errors.append(
                        f"EventBus signals in autoload_registry not in helpers_registry: "
                        f"{sorted(extra_in_autoload)}"
                    )

    policy = registry.get("policy_ref", "")
    policy_path = ROOT / policy
    if policy and not policy_path.is_file():
        errors.append(f"policy_ref missing: {policy}")

    rr = registry.get("roles_and_responsibilities", {})
    if not rr:
        errors.append("roles_and_responsibilities block required")
    else:
        workflows = rr.get("workflows", [])
        required_workflow_ids = {
            "spec_and_python_reference",
            "gdscript_port",
            "autoload_wireup",
            "parity_verification",
            "dispatch",
        }
        found_ids = {w.get("id") for w in workflows}
        missing_wf = required_workflow_ids - found_ids
        if missing_wf:
            errors.append(f"roles_and_responsibilities missing workflows: {sorted(missing_wf)}")
        dispatch = rr.get("dispatch_by_phase", [])
        if not dispatch:
            errors.append("roles_and_responsibilities.dispatch_by_phase is empty")
        for entry in dispatch:
            for hid in entry.get("helpers", []):
                if hid not in helper_ids:
                    errors.append(f"dispatch_by_phase references unknown helper: {hid}")

    for helper in helpers:
        hid = helper.get("id", "?")
        owners = helper.get("owners", {})
        if not owners.get("spec") or not owners.get("gdscript"):
            errors.append(f"{hid}: owners.spec and owners.gdscript required")
        if helper.get("kind") == "autoload" and owners.get("autoload_registration") != "builder":
            errors.append(f"{hid}: autoload must set owners.autoload_registration=builder")

    if errors:
        print("HELPERS REGISTRY VALIDATION FAILED", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        print("\nPolicy: docs/technical/GDSCRIPT_REGENERATION.md", file=sys.stderr)
        return 1

    print(
        f"OK — {len(helpers)} helpers specified, regeneration_order={len(order)}, "
        f"policy={policy}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
