#!/usr/bin/env python3
"""Map git-changed docs to INDEX role/task packs (session reload hint).

Usage:
  python3 tools/docs_pack_impact.py
  python3 tools/docs_pack_impact.py --base origin/main
  python3 tools/docs_pack_impact.py --files docs/design/art/RENDERING_GUIDE.md
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "docs" / "INDEX.yaml"


def _load_packs() -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(INDEX.read_text(encoding="utf-8"))
    except Exception:
        # fallback: parse listed paths under roles/tasks
        text = INDEX.read_text(encoding="utf-8")
        roles: dict[str, list[str]] = {}
        tasks: dict[str, list[str]] = {}
        section = None
        name = None
        for raw in text.splitlines():
            line = raw.split("#", 1)[0].rstrip()
            if line.startswith("roles:"):
                section, name = "roles", None
                continue
            if line.startswith("tasks:"):
                section, name = "tasks", None
                continue
            if line.startswith("diataxis:"):
                section = None
                continue
            if (
                section in ("roles", "tasks")
                and raw.startswith("  ")
                and not raw.startswith("    ")
                and line.strip().endswith(":")
            ):
                name = line.strip().rstrip(":")
                (roles if section == "roles" else tasks)[name] = []
                continue
            if line.strip().startswith("- ") and name and section in ("roles", "tasks"):
                item = line.strip()[2:].strip()
                if item.startswith("docs/") or item == "AGENTS.md":
                    (roles if section == "roles" else tasks)[name].append(item)
        return roles, tasks

    roles = {
        k: list((v or {}).get("must_read") or []) + list((v or {}).get("optional") or [])
        for k, v in (data.get("roles") or {}).items()
    }
    tasks = {
        k: list((v or {}).get("must_read") or []) + list((v or {}).get("optional") or [])
        for k, v in (data.get("tasks") or {}).items()
    }
    return roles, tasks


def _changed_files(base: str | None, files: list[str]) -> list[str]:
    if files:
        return files
    cmd = ["git", "diff", "--name-only"]
    if base:
        cmd.append(base)
    try:
        out = subprocess.check_output(cmd, cwd=ROOT, text=True)
    except subprocess.CalledProcessError as exc:
        print(f"[FAIL] git diff failed: {exc}", file=sys.stderr)
        return []
    return [ln.strip() for ln in out.splitlines() if ln.strip()]


def _matches(changed: str, listed: str) -> bool:
    if changed == listed:
        return True
    # hub ↔ pack: docs/design/art/RENDERING_GUIDE.md ↔ docs/design/art/rendering/...
    if listed.endswith(".md"):
        # CHARACTER_BIBLE → characters/
        stem = Path(listed).stem
        parent = str(Path(listed).parent)
        # conventional pack folders
        candidates = [
            f"{parent}/{stem.lower()}/",
            f"{parent}/rendering/" if "RENDERING" in stem else "",
            f"{parent}/model_qa/" if stem == "MODEL_QA" else "",
            f"{parent}/items/" if "ITEMS" in stem else "",
            f"{parent}/characters/" if "CHARACTER" in stem else "",
            f"{parent}/production/" if "AUDIO_PRODUCTION" in stem else "",
            f"{parent}/narrative/" if "NARRATIVE" in stem else "",
            f"{parent}/implementation/" if stem == "IMPLEMENTATION_PLAN" else "",
            f"{parent}/cloud_setup/" if "CLOUD_AGENT" in stem else "",
            f"{parent}/agile/" if "AGILE" in stem else "",
            f"{parent}/secrets/" if "SECRETS" in stem else "",
            f"{parent}/levels/" if stem == "LEVEL_DESIGN" else "",
            f"{parent}/ci/" if stem == "CI" else "",
            f"{parent}/lifecycle/" if "LIFECYCLE" in stem else "",
            f"{parent}/gdscript_regen/" if "GDSCRIPT" in stem else "",
            f"{parent}/data/" if stem == "DATA_ARCHITECTURE" else "",
        ]
        for c in candidates:
            if c and changed.startswith(c):
                return True
    # listed pack path prefix
    if listed.endswith("/") and changed.startswith(listed):
        return True
    if changed.startswith(str(Path(listed).parent) + "/") and Path(listed).stem.lower() in changed:
        return False
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", help="git diff base ref (default: unstaged+staged vs HEAD)")
    parser.add_argument("--files", nargs="*", help="Explicit file list instead of git diff")
    args = parser.parse_args()

    roles, tasks = _load_packs()
    changed = [
        f
        for f in _changed_files(args.base, args.files or [])
        if f.startswith("docs/") or f == "AGENTS.md" or f == "docs/INDEX.yaml"
    ]
    if not changed:
        print("# no docs changes")
        return 0

    print("# changed")
    for f in changed:
        print(f)

    hit_roles: dict[str, list[str]] = {}
    hit_tasks: dict[str, list[str]] = {}
    for f in changed:
        for role, paths in roles.items():
            for p in paths:
                if _matches(f, p) or f == p:
                    hit_roles.setdefault(role, []).append(f)
                    break
            else:
                # also: any pack file under a hub owned by role via path prefix heuristics
                for p in paths:
                    if f.startswith(str(Path(p).parent) + "/") and Path(p).name.replace(
                        ".md", ""
                    ).lower() in f.lower().replace("_", ""):
                        hit_roles.setdefault(role, []).append(f)
                        break
        for task, paths in tasks.items():
            for p in paths:
                if _matches(f, p) or f == p:
                    hit_tasks.setdefault(task, []).append(f)
                    break

    # INDEX.yaml change → all packs
    if "docs/INDEX.yaml" in changed:
        hit_roles = {r: changed for r in roles}
        hit_tasks = {t: changed for t in tasks}

    if hit_roles:
        print("# roles_to_reload")
        for role in sorted(hit_roles):
            print(f"{role}: {', '.join(sorted(set(hit_roles[role])))}")
    if hit_tasks:
        print("# tasks_to_reload")
        for task in sorted(hit_tasks):
            print(f"{task}: {', '.join(sorted(set(hit_tasks[task])))}")
    if not hit_roles and not hit_tasks:
        print("# no INDEX pack hits — treat as optional/context only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
