#!/usr/bin/env python3
"""Print role/task-scoped doc packs from docs/INDEX.yaml (agent progressive disclosure).

Supports:
  --issue     union sprint_board handoff_refs (+ briefs auto-attach)
  --task      union INDEX.yaml tasks.<id> pack
  --phase     drop optional docs whose frontmatter phase: list excludes N
  --budget    trim non-protected paths by tokens_est
  --report    write kept/deferred/token summary artifact
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
BRIEFS = ROOT / "docs" / "briefs"


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
    """Minimal YAML subset parser for boot/roles/tasks lists."""
    text = INDEX.read_text(encoding="utf-8")
    roles: dict[str, dict[str, list[str]]] = {}
    tasks: dict[str, dict[str, list[str]]] = {}
    boot: list[str] = []
    never: list[str] = []
    section: str | None = None
    name: str | None = None
    key: str | None = None
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if line.startswith("boot:"):
            section, name, key = "boot", None, None
            continue
        if line.startswith("never_autoload:"):
            section, name, key = "never", None, None
            continue
        if line.startswith("roles:"):
            section, name, key = "roles", None, None
            continue
        if line.startswith("tasks:"):
            section, name, key = "tasks", None, None
            continue
        if line.startswith("diataxis:") or line.startswith("folders:") or line.startswith(
            "authority_chain:"
        ):
            section, name, key = "skip", None, None
            continue
        if (
            section in ("roles", "tasks")
            and raw.startswith("  ")
            and not raw.startswith("    ")
            and line.strip().endswith(":")
        ):
            name = line.strip().rstrip(":")
            bucket = roles if section == "roles" else tasks
            bucket[name] = {"must_read": [], "optional": []}
            key = None
            continue
        if (
            section in ("roles", "tasks")
            and name
            and raw.startswith("    ")
            and line.strip().endswith(":")
        ):
            key = line.strip().rstrip(":")
            continue
        if line.strip().startswith("- "):
            item = line.strip()[2:].strip().strip("'\"")
            if section == "boot":
                boot.append(item)
            elif section == "never":
                never.append(item)
            elif section in ("roles", "tasks") and name and key in ("must_read", "optional"):
                bucket = roles if section == "roles" else tasks
                bucket[name][key].append(item)
    return {
        "boot": boot,
        "never_autoload": never,
        "roles": roles,
        "tasks": tasks,
    }


def _frontmatter(rel: str) -> dict[str, str]:
    path = ROOT / rel
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    block = text[4:end]
    out: dict[str, str] = {}
    for raw in block.splitlines():
        if ":" not in raw:
            continue
        key, _, val = raw.partition(":")
        out[key.strip()] = val.strip()
    return out


def _tokens_est(rel: str) -> int:
    fm = _frontmatter(rel)
    if "tokens_est" in fm and fm["tokens_est"].isdigit():
        return int(fm["tokens_est"])
    path = ROOT / rel
    if not path.is_file():
        return 0
    return max(100, path.stat().st_size // 4)


def _doc_phases(rel: str) -> list[int] | None:
    raw = _frontmatter(rel).get("phase")
    if not raw:
        return None
    nums = [int(x) for x in re.findall(r"\d+", raw)]
    return nums or None


def _issue_row(issue_id: str) -> dict | None:
    if not BOARD.is_file():
        return None
    board = json.loads(BOARD.read_text(encoding="utf-8"))
    needle = str(issue_id).strip()
    return next(
        (
            i
            for i in board.get("issues", [])
            if str(i.get("id") or "") == needle
            or str(i.get("github_issue") or "") == needle
        ),
        None,
    )


def _issue_doc_refs(row: dict) -> list[str]:
    refs: list[str] = []
    for item in row.get("handoff_refs") or []:
        if not isinstance(item, str):
            continue
        if item.startswith("docs/") or item == "AGENTS.md":
            refs.append(item)
    return refs


def _brief_catalog() -> dict[str, str]:
    """stem → docs/briefs/... path."""
    out: dict[str, str] = {}
    if not BRIEFS.is_dir():
        return out
    for path in BRIEFS.rglob("*.md"):
        if path.name.lower() == "readme.md":
            continue
        rel = path.relative_to(ROOT).as_posix()
        out[path.stem.lower()] = rel
    return out


def _match_briefs(row: dict) -> list[str]:
    """Attach generation briefs whose stem appears in title / refs / readiness id."""
    catalog = _brief_catalog()
    if not catalog:
        return []
    parts = [
        str(row.get("title") or ""),
        str(row.get("generation_readiness_id") or ""),
        " ".join(str(x) for x in (row.get("handoff_refs") or [])),
        " ".join(str(x) for x in (row.get("implementation_plan_tasks") or [])),
        str(row.get("docs_task") or ""),
    ]
    hay = " ".join(parts).lower().replace("-", "_")
    hay_compact = re.sub(r"[^a-z0-9]+", "", hay)
    matched: list[str] = []
    for stem, rel in sorted(catalog.items(), key=lambda kv: -len(kv[0])):
        stem_l = stem.lower()
        stem_compact = re.sub(r"[^a-z0-9]+", "", stem_l)
        if len(stem_compact) < 4:
            continue
        if re.search(rf"(?<![a-z0-9]){re.escape(stem_l)}(?![a-z0-9])", hay) or (
            stem_compact in hay_compact
        ):
            matched.append(rel)
    return _dedupe(matched)


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


def _filter_phase(
    paths: list[str], phase: int | None
) -> tuple[list[str], list[str]]:
    """Keep docs with no phase tag, or whose phase list includes current phase."""
    if phase is None:
        return paths, []
    kept: list[str] = []
    deferred: list[str] = []
    for path in paths:
        phases = _doc_phases(path)
        if phases is None or phase in phases:
            kept.append(path)
        else:
            deferred.append(path)
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


def _write_report(
    path: Path,
    *,
    role: str,
    issue: str | None,
    task: str | None,
    phase: int | None,
    budget: int,
    must_kept: list[str],
    opt_kept: list[str],
    deferred_budget: list[str],
    deferred_phase: list[str],
    briefs: list[str],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"role: {role}",
        f"issue: {issue or ''}",
        f"task: {task or ''}",
        f"phase: {phase if phase is not None else ''}",
        f"budget: {budget or 'unlimited'}",
        f"briefs_attached: {len(briefs)}",
        "",
        "# must_read",
    ]
    total = 0
    for p in must_kept:
        cost = _tokens_est(p)
        total += cost
        lines.append(f"{cost:5d}  {p}")
    if opt_kept:
        lines.append("")
        lines.append("# optional")
        for p in opt_kept:
            cost = _tokens_est(p)
            total += cost
            lines.append(f"{cost:5d}  {p}")
    if deferred_budget:
        lines.append("")
        lines.append("# deferred_over_budget")
        for p in deferred_budget:
            lines.append(f"{_tokens_est(p):5d}  {p}")
    if deferred_phase:
        lines.append("")
        lines.append("# deferred_out_of_phase")
        for p in deferred_phase:
            lines.append(f"{_tokens_est(p):5d}  {p}")
    lines.append("")
    lines.append(f"tokens_kept_est: {total}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("role", nargs="?", help="Role id from docs/INDEX.yaml")
    parser.add_argument("--list-roles", action="store_true")
    parser.add_argument("--list-tasks", action="store_true")
    parser.add_argument("--boot", action="store_true", help="Print boot paths only")
    parser.add_argument("--check", action="store_true", help="Verify listed paths exist")
    parser.add_argument("--issue", help="Union sprint_board handoff_refs + briefs for this issue")
    parser.add_argument("--task", help="Union INDEX.yaml tasks.<id> pack")
    parser.add_argument(
        "--phase",
        type=int,
        default=None,
        help="Filter optional docs by frontmatter phase: (default: issue.phase)",
    )
    parser.add_argument(
        "--budget",
        type=int,
        default=0,
        help="Max approximate tokens (frontmatter tokens_est); 0 = unlimited",
    )
    parser.add_argument(
        "--must-only",
        action="store_true",
        help="Omit role/task optional packs (issue/brief docs still included as must)",
    )
    parser.add_argument(
        "--report",
        help="Write kept/deferred/token summary to this path (e.g. artifacts/docs_pack_P1-01.txt)",
    )
    parser.add_argument(
        "--no-briefs",
        action="store_true",
        help="Disable brief auto-attach from issue title/refs",
    )
    args = parser.parse_args()

    data = _load_index()
    roles = data.get("roles") or {}
    tasks = data.get("tasks") or {}

    if args.list_roles:
        for name in sorted(roles):
            print(name)
        return 0

    if args.list_tasks:
        for name in sorted(tasks):
            print(name)
        return 0

    if args.boot and not args.role:
        paths = list(data.get("boot") or [])
        for path in paths:
            print(path)
        return _check(paths) if args.check else 0

    if not args.role:
        print(
            "usage: resolve_docs.py <role> [--issue ID] [--task ID] [--phase N] "
            "[--budget N] [--report PATH] [--must-only] | --list-roles | --list-tasks | --boot",
            file=sys.stderr,
        )
        return 2

    if args.role not in roles:
        print(f"unknown role: {args.role}", file=sys.stderr)
        print("known:", ", ".join(sorted(roles)), file=sys.stderr)
        return 1

    task_id = args.task
    row = _issue_row(args.issue) if args.issue else None
    if args.issue and row is None:
        print(f"[WARN] issue {args.issue} not on sprint board", file=sys.stderr)
    if row and not task_id:
        task_id = row.get("docs_task") or None

    if task_id and task_id not in tasks:
        print(f"[WARN] unknown task pack: {task_id}", file=sys.stderr)
        task_id = None

    phase = args.phase
    if phase is None and row and row.get("phase") is not None:
        try:
            phase = int(row["phase"])
        except (TypeError, ValueError) as exc:
            print(
                f"[WARN] issue {args.issue} has non-int phase={row.get('phase')!r} ({exc})",
                file=sys.stderr,
            )
            phase = None

    pack = roles[args.role]
    task_pack = tasks.get(task_id) if task_id else None
    boot = list(data.get("boot") or [])
    issue_docs = _issue_doc_refs(row) if row else []
    briefs = [] if args.no_briefs or not row else _match_briefs(row)

    task_must = list(task_pack.get("must_read") or []) if task_pack else []
    task_opt = list(task_pack.get("optional") or []) if task_pack else []

    # Boot → issue + briefs → task must → role must
    must = _dedupe(boot + issue_docs + briefs + task_must + list(pack.get("must_read") or []))
    optional: list[str] = []
    if not args.must_only:
        optional = _dedupe(task_opt + list(pack.get("optional") or []))
        optional = [p for p in optional if p not in must]

    # Phase filter applies to optional only (must/issue always kept)
    optional, deferred_phase = _filter_phase(optional, phase)

    print(f"# role: {args.role}")
    if args.issue:
        print(f"# issue: {args.issue}")
    if task_id:
        print(f"# task: {task_id}")
    if phase is not None:
        print(f"# phase: {phase}")
    if briefs:
        print(f"# briefs: {len(briefs)} auto-attached")
    if args.budget > 0:
        print(f"# budget: {args.budget} tokens (approx)")

    protected = _dedupe(boot + issue_docs + briefs)
    role_must = [p for p in must if p not in protected]
    label_bits = ["boot"]
    if issue_docs:
        label_bits.append("issue handoff_refs")
    if briefs:
        label_bits.append("briefs")
    if task_must:
        label_bits.append("task")
    print("# must_read (+ " + " + ".join(label_bits) + ")")

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

    deferred_budget = must_deferred + opt_deferred
    if deferred_budget:
        print("# deferred_over_budget")
        for path in deferred_budget:
            print(path)
    if deferred_phase:
        print("# deferred_out_of_phase")
        for path in deferred_phase:
            print(path)

    if args.report:
        _write_report(
            Path(args.report),
            role=args.role,
            issue=args.issue,
            task=task_id,
            phase=phase,
            budget=args.budget,
            must_kept=must_kept,
            opt_kept=opt_kept,
            deferred_budget=deferred_budget,
            deferred_phase=deferred_phase,
            briefs=briefs,
        )
        print(f"# report: {args.report}", file=sys.stderr)

    all_printed = must_kept + opt_kept
    if args.check:
        return _check(all_printed + deferred_budget + deferred_phase)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
