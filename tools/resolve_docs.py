#!/usr/bin/env python3
"""Print role-scoped doc packs from docs/INDEX.yaml (agent progressive disclosure).

Supports issue handoff_refs union and optional token budget trimming.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "INDEX.yaml"
BOARD = ROOT / "game/data/qa/sprint_board.json"


def _load_index() -> dict:
    try:
        import yaml  # type: ignore
    except ImportError as exc:
        print(f"PyYAML unavailable ({exc}); using stdlib INDEX parser", file=sys.stderr)
        return _load_index_stdlib()
    data = yaml.safe_load(INDEX.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(f"invalid INDEX: {INDEX}")
    return data


def _load_index_stdlib() -> dict:
    text = INDEX.read_text(encoding="utf-8")
    roles: dict[str, dict[str, list[str]]] = {}
    boot: list[str] = []
    never: list[str] = []
    section: str | None = None
    role: str | None = None
    key: str | None = None
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if line.startswith("boot:"):
            section, role, key = "boot", None, None
            continue
        if line.startswith("never_autoload:"):
            section, role, key = "never", None, None
            continue
        if line.startswith("roles:"):
            section, role, key = "roles", None, None
            continue
        if (
            section == "roles"
            and raw.startswith("  ")
            and not raw.startswith("    ")
            and line.strip().endswith(":")
        ):
            role = line.strip().rstrip(":")
            roles[role] = {"must_read": [], "optional": []}
            key = None
            continue
        if section == "roles" and role and raw.startswith("    ") and line.strip().endswith(":"):
            key = line.strip().rstrip(":")
            continue
        if line.strip().startswith("- "):
            item = line.strip()[2:].strip().strip("'\"")
            if section == "boot":
                boot.append(item)
            elif section == "never":
                never.append(item)
            elif section == "roles" and role and key in ("must_read", "optional"):
                roles[role][key].append(item)
    return {"boot": boot, "never_autoload": never, "roles": roles}


def _tokens_est(rel: str) -> int:
    path = ROOT / rel
    if not path.is_file():
        return 0
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end > 0:
            block = text[4:end]
            match = re.search(r"(?m)^tokens_est:\s*(\d+)", block)
            if match:
                return int(match.group(1))
    # ~4 chars/token heuristic
    return max(100, path.stat().st_size // 4)


def _issue_doc_refs(issue_id: str) -> list[str]:
    if not BOARD.is_file():
        return []
    board = json.loads(BOARD.read_text(encoding="utf-8"))
    needle = str(issue_id).strip()
    row = next(
        (
            i
            for i in board.get("issues", [])
            if str(i.get("id") or "") == needle
            or str(i.get("github_issue") or "") == needle
        ),
        None,
    )
    if not row:
        print(f"[WARN] issue {issue_id} not on sprint board", file=sys.stderr)
        return []
    refs: list[str] = []
    for item in row.get("handoff_refs") or []:
        if not isinstance(item, str):
            continue
        if item.startswith("docs/") or item == "AGENTS.md":
            refs.append(item)
    return refs


def _dedupe(paths: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for path in paths:
        if path in seen:
            continue
        seen.add(path)
        out.append(path)
    return out


def _apply_budget(paths: list[str], budget: int) -> tuple[list[str], list[str]]:
    """Keep paths in order until budget exhausted. Always keep first path if any."""
    kept: list[str] = []
    deferred: list[str] = []
    used = 0
    for path in paths:
        cost = _tokens_est(path)
        if kept and used + cost > budget:
            deferred.append(path)
            continue
        kept.append(path)
        used += cost
    return kept, deferred


def _check(paths: list[str]) -> int:
    missing = [p for p in paths if not (ROOT / p).is_file()]
    if missing:
        print("MISSING:", file=sys.stderr)
        for item in missing:
            print(f"  - {item}", file=sys.stderr)
        return 1
    print(f"ok — {len(paths)} paths exist", file=sys.stderr)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("role", nargs="?", help="Role id from docs/INDEX.yaml")
    parser.add_argument("--list-roles", action="store_true")
    parser.add_argument("--boot", action="store_true", help="Print boot paths only")
    parser.add_argument("--check", action="store_true", help="Verify listed paths exist")
    parser.add_argument("--issue", help="Union sprint_board handoff_refs docs for this issue")
    parser.add_argument(
        "--budget",
        type=int,
        default=0,
        help="Max approximate tokens (frontmatter tokens_est); 0 = unlimited",
    )
    parser.add_argument(
        "--must-only",
        action="store_true",
        help="Omit role optional pack (issue docs still included as must)",
    )
    args = parser.parse_args()

    data = _load_index()
    roles = data.get("roles") or {}

    if args.list_roles:
        for name in sorted(roles):
            print(name)
        return 0

    if args.boot and not args.role:
        paths = list(data.get("boot") or [])
        for path in paths:
            print(path)
        return _check(paths) if args.check else 0

    if not args.role:
        print(
            "usage: resolve_docs.py <role> [--issue ID] [--budget N] [--must-only] | --list-roles | --boot",
            file=sys.stderr,
        )
        return 2

    if args.role not in roles:
        print(f"unknown role: {args.role}", file=sys.stderr)
        print("known:", ", ".join(sorted(roles)), file=sys.stderr)
        return 1

    pack = roles[args.role]
    boot = list(data.get("boot") or [])
    issue_docs = _issue_doc_refs(args.issue) if args.issue else []
    # Boot → issue handoff (highest task-specific priority) → role must_read
    must = _dedupe(boot + issue_docs + list(pack.get("must_read") or []))
    optional = [] if args.must_only else list(pack.get("optional") or [])
    optional = [p for p in optional if p not in must]

    print(f"# role: {args.role}")
    if args.issue:
        print(f"# issue: {args.issue}")
    if args.budget > 0:
        print(f"# budget: {args.budget} tokens (approx)")

    # Always keep boot + issue handoff; budget only trims role must/optional.
    protected = _dedupe(boot + issue_docs)
    role_must = [p for p in must if p not in protected]
    print("# must_read (+ boot" + (" + issue handoff_refs" if issue_docs else "") + ")")
    if args.budget > 0:
        protected_cost = sum(_tokens_est(p) for p in protected)
        role_budget = max(0, args.budget - protected_cost)
        role_kept, must_deferred = _apply_budget(role_must, role_budget)
        must_kept = protected + role_kept
    else:
        must_kept, must_deferred = must, []
    for path in must_kept:
        print(path)

    remaining_budget = 0
    if args.budget > 0:
        remaining_budget = max(0, args.budget - sum(_tokens_est(p) for p in must_kept))

    opt_kept: list[str] = []
    opt_deferred: list[str] = []
    if optional:
        if args.budget > 0:
            opt_kept, opt_deferred = _apply_budget(optional, remaining_budget)
        else:
            opt_kept = optional
        if opt_kept:
            print("# optional")
            for path in opt_kept:
                print(path)

    deferred = must_deferred + opt_deferred
    if deferred:
        print("# deferred_over_budget")
        for path in deferred:
            print(path)

    all_printed = must_kept + opt_kept
    if args.check:
        return _check(all_printed + deferred)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
