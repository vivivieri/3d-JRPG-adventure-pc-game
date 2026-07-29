#!/usr/bin/env python3
"""Docs library reorg v2 — Diátaxis-oriented top-level + agent router.

Moves domain folders under design/ / build/ / ops/ / briefs/ / archive/,
rewrites repo path references and relative markdown links, writes redirects.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

# old top-level folder under docs/ → new relative path under docs/
FOLDER_MAP: dict[str, str] = {
    "vision": "design/vision",
    "world": "design/world",
    "gameplay": "design/gameplay",
    "art": "design/art",
    "audio": "design/audio",
    "ui": "design/ui",
    "technical": "engineering/technical",
    "agents": "ops/agents",
    "workflow": "ops/workflow",
    "ci-cd": "ops/ci-cd",
    "qa": "ops/qa",
    "cheat-sheets": "ops/cheat-sheets",
    "sprints": "ops/sprints",
    "generation_briefs": "briefs",
    "deprecated": "archive/deprecated",
    "compliance": "archive/compliance",
    "pitch": "archive/pitch",
}

SKIP_REPLACE_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif",
    ".mp4",
    ".wav",
    ".ogg",
    ".glb",
    ".jsonl",
    ".bin",
    ".pyc",
}
SKIP_DIR_PARTS = {
    ".git",
    "node_modules",
    ".cache",
    "artifacts",
    "addons",
    "__pycache__",
}

LINK_RE = re.compile(r"(!?\[[^\]]*\])\(([^)]+)\)")


def map_docs_rel(rel: str) -> str:
    """Map old docs-relative path to new (posix)."""
    rel = rel.replace("\\", "/").lstrip("./")
    for old, new in sorted(FOLDER_MAP.items(), key=lambda x: -len(x[0])):
        if rel == old or rel.startswith(old + "/"):
            return new + rel[len(old) :]
    return rel


def old_abs_to_new(abs_path: Path) -> Path:
    try:
        rel = abs_path.resolve().relative_to(DOCS.resolve()).as_posix()
    except ValueError:
        return abs_path
    return DOCS / map_docs_rel(rel)


def git_mv(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not src.exists():
        print(f"skip missing {src.relative_to(ROOT)}")
        return
    if dst.exists():
        print(f"skip exists {dst.relative_to(ROOT)}")
        return
    # Cloud / overlay FS often rejects git-mv (EXDEV). Move then stage.
    shutil.move(str(src), str(dst))
    subprocess.run(["git", "add", "-A", str(src), str(dst)], cwd=ROOT, check=True)
    print(f"mv {src.relative_to(ROOT)} → {dst.relative_to(ROOT)}")


def collect_link_targets() -> dict[Path, list[tuple[str, str, Path]]]:
    """Before move: path → list of (full_match, url, resolved_target)."""
    out: dict[Path, list[tuple[str, str, Path]]] = {}
    for path in DOCS.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        entries: list[tuple[str, str, Path]] = []
        for match in LINK_RE.finditer(text):
            url = match.group(2).strip()
            if url.startswith(("http://", "https://", "#", "mailto:")):
                continue
            bare = url.split("#")[0].strip()
            if not bare:
                continue
            resolved = (path.parent / bare).resolve()
            entries.append((match.group(0), url, resolved))
        if entries:
            out[path.resolve()] = entries
    return out


def move_folders() -> dict[str, str]:
    redirects: dict[str, str] = {}
    for old, new in FOLDER_MAP.items():
        src = DOCS / old
        dst = DOCS / new
        # Already moved (re-run / partial recovery)
        if not src.exists() and dst.exists():
            print(f"already at docs/{new}")
            if dst.is_dir():
                for f in dst.rglob("*"):
                    if f.is_file():
                        new_rel = f"docs/{f.relative_to(DOCS).as_posix()}"
                        # Reconstruct old rel
                        suffix = f.relative_to(dst).as_posix()
                        old_rel = f"docs/{old}/{suffix}" if suffix != "." else f"docs/{old}"
                        redirects[old_rel] = new_rel
            redirects[f"docs/{old}"] = f"docs/{new}"
            redirects[f"docs/{old}/"] = f"docs/{new}/"
            continue
        if not src.exists():
            print(f"skip missing folder docs/{old}")
            continue
        if src.is_dir():
            for f in src.rglob("*"):
                if f.is_file():
                    old_rel = f"docs/{f.relative_to(DOCS).as_posix()}"
                    new_rel = f"docs/{map_docs_rel(f.relative_to(DOCS).as_posix())}"
                    redirects[old_rel] = new_rel
        git_mv(src, dst)
        redirects[f"docs/{old}"] = f"docs/{new}"
        redirects[f"docs/{old}/"] = f"docs/{new}/"
    return redirects


def should_scan(path: Path) -> bool:
    if not path.is_file():
        return False
    if path.suffix.lower() in SKIP_REPLACE_SUFFIXES:
        return False
    if any(part in SKIP_DIR_PARTS for part in path.parts):
        return False
    # Skip this script's own FOLDER_MAP source of truth? Still update comments OK.
    try:
        path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError) as exc:
        print(f"skip unreadable {path}: {exc}", file=sys.stderr)
        return False
    return True


def build_string_replacements() -> list[tuple[str, str]]:
    """Longest-first path string replacements for docs/<folder>/…"""
    pairs: list[tuple[str, str]] = []
    for old, new in FOLDER_MAP.items():
        pairs.append((f"docs/{old}/", f"docs/{new}/"))
        pairs.append((f"docs/{old}", f"docs/{new}"))  # bare folder refs
    # Sort by old length descending so longer paths win first
    pairs.sort(key=lambda x: len(x[0]), reverse=True)
    return pairs


def update_path_strings() -> int:
    """Replace docs/<old>/… paths; avoid false positives like docs/artifact."""
    # Only folder prefixes with trailing slash — longest first.
    prefixes = sorted(
        ((f"docs/{old}/", f"docs/{new}/") for old, new in FOLDER_MAP.items()),
        key=lambda x: len(x[0]),
        reverse=True,
    )
    # Bare folder tokens: docs/<old> not followed by letter/digit/_/-
    bare_patterns: list[tuple[re.Pattern[str], str]] = []
    for old, new in FOLDER_MAP.items():
        bare_patterns.append(
            (
                re.compile(rf"(?<![\w./])docs/{re.escape(old)}(?![\w./-])"),
                f"docs/{new}",
            )
        )
    bare_patterns.sort(key=lambda x: -len(x[1]))

    changed = 0
    for path in ROOT.rglob("*"):
        if not should_scan(path):
            continue
        if path.resolve() == Path(__file__).resolve():
            continue
        text = path.read_text(encoding="utf-8")
        original = text
        for old, new in prefixes:
            text = text.replace(old, new)
        for pat, repl in bare_patterns:
            text = pat.sub(repl, text)
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed += 1
            print(f"refs {path.relative_to(ROOT)}")
    return changed


def rewrite_relative_links(pre_links: dict[Path, list[tuple[str, str, Path]]]) -> int:
    """Fix markdown relative links using pre-move resolutions."""
    changed_files = 0
    # Map old resolved path → new path
    for old_path, entries in pre_links.items():
        new_path = old_abs_to_new(old_path)
        if not new_path.is_file():
            # Maybe path string replace already moved content under new path
            if not new_path.exists():
                print(f"warn missing after move: {new_path}")
                continue
        text = new_path.read_text(encoding="utf-8")
        original = text
        # Replace longer URLs first to avoid partial collisions
        for full, url, old_target in sorted(entries, key=lambda e: -len(e[1])):
            fragment = ""
            if "#" in url:
                bare, frag = url.split("#", 1)
                fragment = "#" + frag
            else:
                bare = url
            if not bare:
                continue
            new_target = old_abs_to_new(old_target)
            if not new_target.exists():
                # Target might be outside docs (e.g. ../AGENTS.md, steam/)
                # Keep relative recalculation from new_path to old_target if still exists
                if old_target.exists():
                    new_target = old_target
                else:
                    continue
            try:
                rel = Path(
                    __import__("os").path.relpath(str(new_target), start=str(new_path.parent))
                ).as_posix()
            except ValueError as exc:
                print(f"skip relpath {new_path} → {new_target}: {exc}", file=sys.stderr)
                continue
            new_url = rel + fragment
            old_full = full
            # Rebuild markdown link with same label
            label_end = full.rfind("](")
            if label_end < 0:
                continue
            label = full[: label_end + 1]  # includes ]
            replacement = f"{label}({new_url})"
            if old_full in text:
                text = text.replace(old_full, replacement)
        if text != original:
            new_path.write_text(text, encoding="utf-8")
            changed_files += 1
            print(f"links {new_path.relative_to(ROOT)}")
    return changed_files


def write_redirects(redirects: dict[str, str]) -> None:
    meta = DOCS / "_meta"
    meta.mkdir(parents=True, exist_ok=True)
    # Stable sorted YAML-ish via JSON for simplicity + yaml dump
    lines = [
        "# Auto-generated by tools/reorganize_docs_v2.py — old path → new path",
        "# Agents and link checkers: prefer docs/INDEX.yaml; use this for legacy refs.",
        "",
    ]
    for old in sorted(redirects, key=lambda s: (-len(s), s)):
        new = redirects[old]
        if old == new:
            continue
        lines.append(f"{old}: {new}")
    (meta / "redirects.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (meta / "redirects.json").write_text(
        json.dumps(redirects, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def main() -> int:
    print("==> collect pre-move link targets")
    pre_links = collect_link_targets()
    print(f"    {len(pre_links)} markdown files with links")

    print("==> move folders")
    redirects = move_folders()

    print("==> rewrite docs/ path strings repo-wide")
    n_refs = update_path_strings()

    print("==> rewrite relative markdown links")
    n_links = rewrite_relative_links(pre_links)

    print("==> write redirects map")
    write_redirects(redirects)

    print(
        f"Done. redirects={len(redirects)} ref_files={n_refs} link_files={n_links}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
