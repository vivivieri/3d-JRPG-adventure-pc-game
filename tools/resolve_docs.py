#!/usr/bin/env python3
"""Print role-scoped doc packs from docs/INDEX.yaml (agent progressive disclosure)."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "INDEX.yaml"


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
    """Tiny YAML subset loader for INDEX.yaml when PyYAML is unavailable."""
    text = INDEX.read_text(encoding="utf-8")
    # Prefer json redirects sibling? No — parse roles via line scan.
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
        if section == "roles" and raw.startswith("  ") and not raw.startswith("    ") and line.strip().endswith(":"):
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("role", nargs="?", help="Role id from docs/INDEX.yaml")
    parser.add_argument("--list-roles", action="store_true")
    parser.add_argument("--boot", action="store_true", help="Print boot paths only")
    parser.add_argument("--check", action="store_true", help="Verify listed paths exist")
    args = parser.parse_args()

    data = _load_index()
    roles = data.get("roles") or {}

    if args.list_roles:
        for name in sorted(roles):
            print(name)
        return 0

    if args.boot or not args.role:
        paths = list(data.get("boot") or [])
        if args.role and args.role in roles:
            pack = roles[args.role]
            paths = list(data.get("boot") or []) + list(pack.get("must_read") or [])
        elif args.role and args.role not in roles:
            print(f"unknown role: {args.role}", file=sys.stderr)
            print("known:", ", ".join(sorted(roles)), file=sys.stderr)
            return 1
        elif not args.boot and not args.role:
            print("usage: resolve_docs.py <role> | --list-roles | --boot", file=sys.stderr)
            return 2
    else:
        if args.role not in roles:
            print(f"unknown role: {args.role}", file=sys.stderr)
            print("known:", ", ".join(sorted(roles)), file=sys.stderr)
            return 1
        pack = roles[args.role]
        paths = list(data.get("boot") or []) + list(pack.get("must_read") or [])
        optional = list(pack.get("optional") or [])
        print(f"# role: {args.role}")
        print("# must_read (+ boot)")
        for p in paths:
            print(p)
        if optional:
            print("# optional")
            for p in optional:
                print(p)
        if args.check:
            return _check(paths + optional)
        return 0

    for p in paths:
        print(p)
    if args.check:
        return _check(paths)
    return 0


def _check(paths: list[str]) -> int:
    missing = []
    for p in paths:
        path = ROOT / p
        if not path.is_file():
            missing.append(p)
    if missing:
        print("MISSING:", file=sys.stderr)
        for m in missing:
            print(f"  - {m}", file=sys.stderr)
        return 1
    print(f"ok — {len(paths)} paths exist", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
