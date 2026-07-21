#!/usr/bin/env python3
"""Verify all shipped media files have documented, ship-safe licenses.

Scans game/assets/ and steam/ for media files and cross-checks against
docs/asset_manifest.license.json. Fails on:
  - Unlisted media files
  - Banned license IDs
  - Missing required manifest fields
  - Listed files with UNKNOWN license

Usage:
  python3 tools/verify_asset_licenses.py
  python3 tools/verify_asset_licenses.py --strict   # fail if scan paths missing
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "docs" / "asset_manifest.license.json"


def load_manifest() -> dict:
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        return json.load(f)


def normalize_path(rel: str) -> str:
    return rel.replace("\\", "/")


def path_matches_glob(rel: str, pattern: str) -> bool:
    """Match repo-relative paths against glob patterns (supports **)."""
    rel = normalize_path(rel)
    pattern = normalize_path(pattern)
    if fnmatch.fnmatch(rel, pattern):
        return True
    # pathlib-style ** fallback
    if "**" in pattern:
        prefix = pattern.split("**")[0].rstrip("/")
        if prefix and not rel.startswith(prefix):
            return False
        suffix = pattern.split("**")[-1].lstrip("/")
        if suffix:
            return fnmatch.fnmatch(Path(rel).name, suffix) or rel.endswith(suffix)
        return True
    return False


def build_coverage(manifest: dict) -> tuple[dict[str, dict], set[str], set[str]]:
    """Map each registered path/glob to its asset entry."""
    allowed_licenses = set(manifest.get("allowed_licenses", []))
    banned_licenses = set(manifest.get("banned_licenses", []))
    entries: list[dict] = manifest.get("assets", [])

    exact: dict[str, dict] = {}
    globs: list[tuple[str, dict]] = []

    for entry in entries:
        lic = entry.get("license", "UNKNOWN")
        if lic in banned_licenses:
            raise ValueError(f"Banned license in manifest for {entry.get('path')}: {lic}")
        if lic not in allowed_licenses:
            raise ValueError(f"Unrecognized license in manifest for {entry.get('path')}: {lic}")

        path = entry.get("path", "")
        glob_pat = entry.get("glob")
        if glob_pat:
            globs.append((glob_pat, entry))
        elif path:
            exact[normalize_path(path)] = entry

    return {"exact": exact, "globs": globs}, allowed_licenses, banned_licenses


def lookup_entry(rel: str, coverage: dict) -> dict | None:
    rel = normalize_path(rel)
    if rel in coverage["exact"]:
        return coverage["exact"][rel]
    for pattern, entry in coverage["globs"]:
        if path_matches_glob(rel, pattern):
            return entry
    return None


def iter_media_files(manifest: dict) -> list[str]:
    extensions = {e.lower() for e in manifest.get("media_extensions", [])}
    skip_names = set(manifest.get("skip_filenames", []))
    scan_paths = manifest.get("scan_paths", ["game/assets", "steam"])
    found: list[str] = []

    for scan in scan_paths:
        base = ROOT / scan
        if not base.is_dir():
            continue
        for dirpath, _, filenames in os.walk(base):
            for name in filenames:
                if name.endswith(".import") or name in skip_names:
                    continue
                ext = os.path.splitext(name)[1].lower()
                if ext not in extensions:
                    continue
                rel = normalize_path(str(Path(dirpath, name).relative_to(ROOT)))
                found.append(rel)
    return sorted(set(found))


def validate_manifest_schema(manifest: dict) -> list[str]:
    errors: list[str] = []
    required = ("path", "license", "source", "author", "date_added", "used_for")
    for i, entry in enumerate(manifest.get("assets", [])):
        if not entry.get("glob"):
            for field in required:
                if not entry.get(field):
                    errors.append(f"Manifest asset[{i}] missing '{field}': {entry.get('path', '?')}")
        if entry.get("license") == "UNKNOWN":
            errors.append(f"Manifest asset[{i}] has UNKNOWN license: {entry.get('path')}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify asset license compliance")
    parser.add_argument("--strict", action="store_true", help="Fail if scan paths are missing")
    args = parser.parse_args()

    if not MANIFEST_PATH.is_file():
        print(f"ERROR: Missing manifest: {MANIFEST_PATH}", file=sys.stderr)
        return 1

    manifest = load_manifest()
    schema_errors = validate_manifest_schema(manifest)
    if schema_errors:
        print("MANIFEST SCHEMA ERRORS", file=sys.stderr)
        for e in schema_errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    try:
        coverage, allowed, banned = build_coverage(manifest)
    except ValueError as exc:
        print(f"MANIFEST ERROR: {exc}", file=sys.stderr)
        return 1

    errors: list[str] = []
    warnings: list[str] = []

    scan_paths = manifest.get("scan_paths", [])
    for scan in scan_paths:
        if not (ROOT / scan).is_dir():
            msg = f"Scan path not present (no media to check): {scan}"
            if args.strict:
                errors.append(msg)
            else:
                warnings.append(msg)

    media_files = iter_media_files(manifest)
    covered: list[str] = []
    uncovered: list[str] = []

    for rel in media_files:
        entry = lookup_entry(rel, coverage)
        if entry is None:
            uncovered.append(rel)
        else:
            covered.append(rel)

    for rel in uncovered:
        errors.append(
            f"UNLISTED: {rel} — register with tools/register_asset.py and docs/art/LICENSES.md"
        )

    # Manifest entries for files that don't exist yet
    for rel, entry in coverage["exact"].items():
        if not rel.endswith("/") and not (ROOT / rel).exists():
            if not entry.get("glob"):
                msg = f"Manifest entry file not on disk yet: {rel}"
                if args.strict:
                    errors.append(msg)
                else:
                    warnings.append(msg)

    if errors:
        print("ASSET LICENSE CHECK FAILED", file=sys.stderr)
        print(f"Policy: {manifest.get('policy', 'docs/art/ASSET_COMPLIANCE.md')}", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        if warnings:
            print("\nWarnings:", file=sys.stderr)
            for w in warnings:
                print(f"  - {w}", file=sys.stderr)
        return 1

    print("ASSET LICENSE CHECK PASSED")
    print(f"  Policy: {manifest.get('policy')}")
    print(f"  Manifest: {MANIFEST_PATH.relative_to(ROOT)}")
    print(f"  Media files scanned: {len(media_files)}")
    print(f"  Covered by manifest: {len(covered)}")
    print(f"  Allowed license types: {len(allowed)}")
    if warnings:
        print(f"  Warnings: {len(warnings)} (paths not present on this branch)")
        for w in warnings:
            print(f"    - {w}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
