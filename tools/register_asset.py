#!/usr/bin/env python3
"""Register or update assets in docs/asset_manifest.license.json.

Examples:
  python3 tools/register_asset.py add \\
    --path game/assets/models/characters/urashima/urashima.glb \\
    --license ORIGINAL \\
    --source "Custom Blender model" \\
    --author "Project team" \\
    --used-for "Protagonist field + combat model"

  python3 tools/register_asset.py add \\
    --path game/assets/audio/bgm/village.ogg \\
    --license CC0-1.0 \\
    --source "OpenGameArt" \\
    --source-url "https://opengameart.org/..." \\
    --author "Artist Name" \\
    --used-for "Village BGM" \\
    --attribution "Music by Artist Name (CC0)"

  python3 tools/register_asset.py list
  python3 tools/register_asset.py remove --path game/assets/foo.png
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "docs" / "asset_manifest.license.json"


def load_manifest() -> dict:
    with open(MANIFEST_PATH, encoding="utf-8") as f:
        return json.load(f)


def save_manifest(manifest: dict) -> None:
    manifest["updated"] = str(date.today())
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write("\n")


def cmd_list(manifest: dict) -> int:
    assets = manifest.get("assets", [])
    print(f"Manifest: {MANIFEST_PATH} ({len(assets)} entries)")
    print(f"Allowed: {', '.join(manifest.get('allowed_licenses', []))}")
    print()
    for i, a in enumerate(assets):
        path = a.get("glob") or a.get("path", "?")
        print(f"  [{i}] {path}")
        print(f"      license={a.get('license')}  source={a.get('source')}")
    return 0


def cmd_add(args: argparse.Namespace) -> int:
    manifest = load_manifest()
    allowed = set(manifest.get("allowed_licenses", []))
    banned = set(manifest.get("banned_licenses", []))

    if args.license in banned:
        print(f"ERROR: License '{args.license}' is banned. See docs/ASSET_COMPLIANCE.md", file=sys.stderr)
        return 1
    if args.license not in allowed:
        print(f"ERROR: License '{args.license}' not in allowed list.", file=sys.stderr)
        print(f"Allowed: {', '.join(sorted(allowed))}", file=sys.stderr)
        return 1

    path = args.path.replace("\\", "/")
    for entry in manifest.get("assets", []):
        if entry.get("path") == path or entry.get("glob") == path:
            print(f"ERROR: Entry already exists for {path}. Use 'update' or 'remove' first.", file=sys.stderr)
            return 1

    entry: dict = {
        "path": path if not args.glob else path,
        "license": args.license,
        "source": args.source,
        "source_url": args.source_url,
        "author": args.author,
        "date_added": str(date.today()),
        "used_for": args.used_for,
        "attribution": args.attribution,
    }
    if args.glob:
        entry["glob"] = args.glob
        if not args.glob.startswith(path.rstrip("/")):
            entry["glob"] = args.glob

    if args.source_url is None and args.license not in ("ORIGINAL", "COMMISSIONED", "MIT", "PUBLIC-DOMAIN"):
        print("WARNING: External assets should include --source-url to the official license page.", file=sys.stderr)

    manifest.setdefault("assets", []).append(entry)
    save_manifest(manifest)
    print(f"Registered: {path} ({args.license})")
    print("Next steps:")
    print("  1. Add row to docs/LICENSES.md")
    print("  2. Run: bash tools/check_asset_compliance.sh")
    return 0


def cmd_remove(args: argparse.Namespace) -> int:
    manifest = load_manifest()
    path = args.path.replace("\\", "/")
    before = len(manifest.get("assets", []))
    manifest["assets"] = [
        a for a in manifest.get("assets", [])
        if a.get("path") != path and a.get("glob") != path
    ]
    if len(manifest["assets"]) == before:
        print(f"ERROR: No entry found for {path}", file=sys.stderr)
        return 1
    save_manifest(manifest)
    print(f"Removed: {path}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage asset license manifest")
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="List manifest entries")
    p_list.set_defaults(func=lambda _a: cmd_list(load_manifest()))

    p_add = sub.add_parser("add", help="Register a new asset")
    p_add.add_argument("--path", required=True, help="Repo-relative file or directory path")
    p_add.add_argument("--glob", help="Glob pattern (e.g. game/assets/foo/**/*.png)")
    p_add.add_argument("--license", required=True, help="License ID from allowed list")
    p_add.add_argument("--source", required=True, help="Source name or description")
    p_add.add_argument("--source-url", default=None, help="Official license/source URL")
    p_add.add_argument("--author", required=True, help="Author or rights holder")
    p_add.add_argument("--used-for", required=True, help="In-game usage description")
    p_add.add_argument("--attribution", default=None, help="Credits line if required")
    p_add.set_defaults(func=cmd_add)

    p_rm = sub.add_parser("remove", help="Remove manifest entry by path/glob")
    p_rm.add_argument("--path", required=True)
    p_rm.set_defaults(func=cmd_remove)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
