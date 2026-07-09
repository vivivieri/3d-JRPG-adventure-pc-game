#!/usr/bin/env python3
"""Download curated CC0 high-poly models from Poly Haven (1k glTF)."""
from __future__ import annotations

import json
import os
import sys
import urllib.request

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "game", "assets", "models", "polyhaven")
API = "https://api.polyhaven.com/files"
UA = "TidesOfUrashima/1.0 (CC0 asset installer)"

# asset_id on polyhaven -> local alias used by PropLibrary
CURATED = {
    "island_tree_02": "tree_coastal_a",
    "island_tree_01": "tree_coastal_b",
    "coastal_cliff_04": "cliff_coastal",
    "boulder_01": "boulder_a",
    "rock_moss_set_01": "rocks_moss_a",
    "rock_moss_set_02": "rocks_moss_b",
    "dead_tree_trunk_02": "dead_trunk",
    "grass_bermuda_01": "grass_hd",
    "grass_medium_01": "grass_clump",
    "fern_02": "fern",
    "shrub_sorrel_01": "shrub_hd",
    "dry_branches_medium_01": "branches",
    "pine_tree_01": "pine_hd",
    "fir_tree_01": "fir_hd",
}

RESOLUTION = os.environ.get("POLYHAVEN_RES", "1k")


def fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def download(url: str, dest: str) -> None:
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if os.path.isfile(dest):
        return
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=300) as resp:
        data = resp.read()
    with open(dest, "wb") as f:
        f.write(data)


def collect_gltf_bundle(files_meta: dict, resolution: str) -> dict[str, str]:
    gltf_block = files_meta.get("gltf", {}).get(resolution, {}).get("gltf")
    if not gltf_block:
        raise KeyError(f"No glTF at resolution {resolution}")
    bundle: dict[str, str] = {"": gltf_block["url"]}
    for rel, info in gltf_block.get("include", {}).items():
        bundle[rel] = info["url"]
    return bundle


def install_asset(asset_id: str, alias: str) -> list[str]:
    meta = fetch_json(f"{API}/{asset_id}")
    bundle = collect_gltf_bundle(meta, RESOLUTION)
    asset_dir = os.path.join(OUT, alias)
    installed: list[str] = []
    for rel, url in bundle.items():
        filename = os.path.basename(url.split("?")[0])
        if rel == "":
            dest_name = f"{alias}_{RESOLUTION}.gltf"
            dest = os.path.join(asset_dir, dest_name)
        else:
            dest = os.path.join(asset_dir, rel.replace("/", os.sep))
            os.makedirs(os.path.dirname(dest), exist_ok=True)
        download(url, dest)
        installed.append(os.path.relpath(dest, os.path.join(ROOT, "game", "assets", "models")).replace("\\", "/"))
    # Pointer file for PropLibrary
    pointer = os.path.join(asset_dir, "model.path")
    with open(pointer, "w", encoding="utf-8") as f:
        f.write(f"polyhaven/{alias}/{alias}_{RESOLUTION}.gltf\n")
    return installed


def write_manifest(all_files: list[str]) -> None:
    manifest = {
        "license": "CC0 1.0",
        "source": "Poly Haven (polyhaven.com)",
        "resolution": RESOLUTION,
        "files": sorted(set(all_files)),
    }
    path = os.path.join(ROOT, "game", "assets", "models", "polyhaven_manifest.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")
    with open(os.path.join(OUT, "LICENSE_POLYHAVEN.txt"), "w", encoding="utf-8") as f:
        f.write("Poly Haven assets — CC0 1.0 (https://polyhaven.com/license)\n")


def main() -> int:
    all_files: list[str] = []
    for asset_id, alias in CURATED.items():
        print(f"Downloading {asset_id} -> {alias} ({RESOLUTION})...")
        try:
            files = install_asset(asset_id, alias)
            all_files.extend(files)
            print(f"  OK ({len(files)} files)")
        except Exception as exc:
            print(f"  FAILED: {exc}", file=sys.stderr)
            return 1
    write_manifest(all_files)
    print(f"Installed {len(CURATED)} Poly Haven models ({len(all_files)} files) to {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
