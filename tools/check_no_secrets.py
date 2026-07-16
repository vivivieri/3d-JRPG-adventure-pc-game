#!/usr/bin/env python3
"""Scan tracked files for accidental secret commits (L0_no_secrets)."""
from __future__ import annotations

import fnmatch
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "game/data/qa/ship_security.json"


def load_config() -> dict:
    data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return data.get("secret_scan") or {}


def tracked_files() -> list[str]:
    proc = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return []
    return [p for p in proc.stdout.split("\0") if p]


def allowed(path: str, allowlist: list[str]) -> bool:
    for pat in allowlist:
        if fnmatch.fnmatch(path, pat) or fnmatch.fnmatch(path, f"**/{pat}"):
            return True
    return False


def main() -> int:
    if not CONFIG_PATH.is_file():
        print(f"[FAIL] missing {CONFIG_PATH}")
        return 1

    cfg = load_config()
    allowlist = cfg.get("allowlist_globs") or []
    patterns = cfg.get("patterns") or []
    compiled = [(p["id"], re.compile(p["regex"])) for p in patterns if p.get("regex")]

    hits: list[str] = []
    for rel in tracked_files():
        if allowed(rel, allowlist):
            continue
        path = ROOT / rel
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for line_no, line in enumerate(text.splitlines(), start=1):
            for pid, rx in compiled:
                if rx.search(line):
                    hits.append(f"{rel}:{line_no}: pattern {pid}")
                    break

    if hits:
        print("[FAIL] possible secrets in tracked files:")
        for h in hits[:30]:
            print(f"  - {h}")
        if len(hits) > 30:
            print(f"  ... and {len(hits) - 30} more")
        return 1

    print(f"[PASS] no_secrets — scanned {len(tracked_files())} tracked file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
