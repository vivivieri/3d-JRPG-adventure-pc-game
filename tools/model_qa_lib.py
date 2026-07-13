#!/usr/bin/env python3
"""GLB helpers for model QA (docs/MODEL_QA.md)."""
from __future__ import annotations

import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "game/data/models/qa_catalog.json"
MANIFEST = ROOT / "docs/asset_manifest.license.json"

BANNED_PATH_RE = (
    "models/nature/",
    "models/castle/",
    "/kenney",
    "kenney_",
)


def load_catalog() -> dict:
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def model_path(model_id: str, catalog: dict | None = None) -> Path:
    cat = catalog or load_catalog()
    meta = cat["models"][model_id]
    return ROOT / meta["path"]


def parse_glb(path: Path) -> tuple[dict, bytes]:
    data = path.read_bytes()
    if len(data) < 12:
        raise ValueError("file too small for GLB")
    magic, _version, _length = struct.unpack_from("<4sII", data, 0)
    if magic != b"glTF":
        raise ValueError("not a GLB file")
    offset = 12
    json_len, json_type = struct.unpack_from("<I4s", data, offset)
    offset += 8
    if json_type != b"JSON":
        raise ValueError("missing JSON chunk")
    gltf = json.loads(data[offset : offset + json_len])
    offset += json_len
    bin_data = b""
    if offset + 8 <= len(data):
        bin_len, bin_type = struct.unpack_from("<I4s", data, offset)
        if bin_type == b"BIN\x00":
            offset += 8
            bin_data = data[offset : offset + bin_len]
    return gltf, bin_data


def count_triangles(gltf: dict) -> int:
    accessors = gltf.get("accessors", [])
    total = 0
    for mesh in gltf.get("meshes", []):
        for prim in mesh.get("primitives", []):
            if prim.get("mode", 4) != 4:
                continue
            if "indices" in prim:
                count = accessors[prim["indices"]].get("count", 0)
                total += count // 3
            elif "attributes" in prim and "POSITION" in prim["attributes"]:
                count = accessors[prim["attributes"]["POSITION"]].get("count", 0)
                total += count // 3
    return total


def count_images(gltf: dict) -> int:
    return len(gltf.get("images", []))


def animation_durations_ms(gltf: dict, bin_data: bytes) -> dict[str, int]:
    """Max keyframe time per named animation clip (milliseconds)."""
    import struct

    accessors = gltf.get("accessors", [])
    buffer_views = gltf.get("bufferViews", [])
    durations: dict[str, int] = {}

    for anim in gltf.get("animations", []):
        name = (anim.get("name") or "").strip()
        if not name:
            continue
        max_t = 0.0
        for channel in anim.get("channels", []):
            sampler_idx = channel.get("sampler")
            if sampler_idx is None:
                continue
            sampler = gltf["samplers"][sampler_idx]
            input_idx = sampler.get("input")
            if input_idx is None:
                continue
            acc = accessors[input_idx]
            bv = buffer_views[acc["bufferView"]]
            offset = bv.get("byteOffset", 0) + acc.get("byteOffset", 0)
            count = acc.get("count", 0)
            for i in range(count):
                t = struct.unpack_from("<f", bin_data, offset + i * 4)[0]
                max_t = max(max_t, float(t))
        durations[name] = int(round(max_t * 1000.0))

    return durations


def is_greybox_source(rel_path: str) -> bool:
    lower = rel_path.lower()
    if any(p in lower for p in BANNED_PATH_RE):
        return True
    if not MANIFEST.is_file():
        return False
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for entry in data.get("assets", []):
        if entry.get("path") == rel_path:
            src = (entry.get("source", "") + entry.get("used_for", "")).lower()
            if "kenney" in src or "greybox" in src:
                return True
    return False
