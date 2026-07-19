#!/usr/bin/env python3
"""Generate copyright-safe procedural portrait placeholders (ORIGINAL).

Simple gradient + silhouette blocks — no external images.
GodotPrompter plans palette; output registered in asset manifest.

Usage:
  python3 tools/generate_procedural_portraits.py --all
  python3 tools/generate_procedural_portraits.py --id urashima_weary
"""
from __future__ import annotations

import argparse
import json
import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "game" / "assets" / "ui" / "portraits"
MANIFEST = ROOT / "docs" / "asset_manifest.license.json"
W, H = 256, 256

PALETTES: dict[str, tuple[tuple[int, int, int], tuple[int, int, int]]] = {
    "urashima_weary": ((66, 92, 120), (28, 48, 72)),
    "urashima_determined": ((72, 110, 145), (32, 58, 88)),
    "yuzu_gentle": ((210, 120, 150), (140, 70, 95)),
    "yuzu_sad": ((180, 100, 130), (110, 55, 80)),
    "roku_grim": ((70, 95, 75), (40, 58, 42)),
    "roku_urgent": ((85, 115, 80), (50, 72, 48)),
    "otohime_serene": ((120, 160, 200), (60, 90, 130)),
    "narrator": ((90, 100, 110), (45, 52, 60)),
}


def _png_rgb(path: Path, pixels: list[tuple[int, int, int]]) -> None:
    raw = b"".join(b"\x00" + bytes(p) for p in pixels)
    comp = zlib.compress(raw, 9)

    def chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", comp) + chunk(b"IEND", b"")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(png)


def generate_portrait(pid: str) -> Path:
    fg, bg = PALETTES.get(pid, ((100, 120, 140), (50, 60, 70)))
    pixels: list[tuple[int, int, int]] = []
    for y in range(H):
        for x in range(W):
            t = y / H
            r = int(bg[0] * (1 - t) + fg[0] * t)
            g = int(bg[1] * (1 - t) + fg[1] * t)
            b = int(bg[2] * (1 - t) + fg[2] * t)
            # face oval
            cx, cy, rx, ry = W // 2, int(H * 0.42), int(W * 0.28), int(H * 0.32)
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 < 1.0:
                r, g, b = fg
            pixels.append((r, g, b))
    out = OUT_DIR / f"{pid}.png"
    _png_rgb(out, pixels)
    if MANIFEST.exists():
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        rel = f"game/assets/ui/portraits/{pid}.png"
        if not any(a.get("path") == rel for a in data.get("assets", [])):
            data.setdefault("assets", []).append({
                "path": rel,
                "license": "ORIGINAL",
                "source": "Procedural (tools/generate_procedural_portraits.py)",
                "author": "Project tooling",
                "used_for": f"Dialogue portrait placeholder: {pid}",
            })
            MANIFEST.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--id", action="append", dest="ids", default=[])
    args = ap.parse_args()
    ids = list(PALETTES.keys()) if args.all else args.ids
    if not ids:
        ap.print_help()
        return 1
    for pid in ids:
        print(f"Generated {generate_portrait(pid)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
