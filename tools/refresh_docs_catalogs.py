#!/usr/bin/env python3
"""Regenerate docs/{design,engineering,ops}/README.md catalogs from on-disk markdown."""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

BUCKETS = {
    "design": "Product design — vision, world, gameplay, art, audio, ui",
    "engineering": "Runtime architecture and coding standards",
    "ops": "Factory, workflow, CI/CD, QA process, cheat sheets",
}

SKIP_PARTS = {"audio_sheets", "automation_prompts", "sprints"}


def build_catalog(bucket: str, blurb: str) -> str:
    root = DOCS / bucket
    boot = "BOOT.md" if bucket == "ops" else "../ops/BOOT.md"
    lines = [
        f"# {bucket.title()} docs",
        "",
        f"{blurb}.",
        "",
        f"Hub: [`docs/README.md`](../README.md) · Router: [`docs/INDEX.yaml`](../INDEX.yaml) · "
        f"Boot: [`ops/BOOT.md`]({boot})",
        "",
        "| Path | Doc |",
        "|------|-----|",
    ]
    for md in sorted(root.rglob("*.md")):
        if md.name == "README.md":
            continue
        if any(part in SKIP_PARTS for part in md.parts):
            continue
        rel = md.relative_to(root).as_posix()
        lines.append(f"| [{rel}]({rel}) | `{md.stem}` |")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if catalogs differ from regenerated content (CI drift gate)",
    )
    args = parser.parse_args()
    dirty = False
    for bucket, blurb in BUCKETS.items():
        path = DOCS / bucket / "README.md"
        desired = build_catalog(bucket, blurb)
        if args.check:
            current = path.read_text(encoding="utf-8") if path.is_file() else ""
            if current != desired:
                print(f"[FAIL] docs/{bucket}/README.md is stale — run: python3 tools/refresh_docs_catalogs.py")
                dirty = True
            else:
                print(f"[OK]   docs/{bucket}/README.md")
        else:
            path.write_text(desired, encoding="utf-8")
            print(f"wrote docs/{bucket}/README.md")
    return 1 if dirty else 0


if __name__ == "__main__":
    raise SystemExit(main())
