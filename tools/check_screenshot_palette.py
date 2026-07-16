#!/usr/bin/env python3
"""Check viewport screenshot palette against zone anchors (docs/art/VISUAL_QA.md §2D)."""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

# Mirrors docs/art/ART_DIRECTION.md §1 + tools/palette_remap.py
ZONE_PALETTES: dict[str, list[tuple[int, int, int]]] = {
    "ruined_village": [
        (0x8B, 0x9D, 0xAF),
        (0x5C, 0x4A, 0x3A),
        (0x3D, 0x5C, 0x4A),
        (0x8B, 0x3A, 0x2A),
        (0xC9, 0xB8, 0x9A),
    ],
    "beach": [(0x8B, 0x9D, 0xAF), (0xC9, 0xB8, 0x9A), (0x3D, 0x5C, 0x4A), (0x1A, 0x4A, 0x5A)],
    "tidal_caves": [(0x1A, 0x4A, 0x5A), (0x4A, 0xE8, 0xD8), (0x3A, 0x3A, 0x45)],
    "palace_gate": [
        (0xD4, 0xA5, 0x5A),
        (0x8B, 0x2A, 0x3A),
        (0xE8, 0xE4, 0xDC),
        (0x1A, 0x1A, 0x3A),
    ],
}


def _load_pillow():
    try:
        from PIL import Image
    except ImportError as exc:
        print("check_screenshot_palette.py requires Pillow", file=sys.stderr)
        raise SystemExit(2) from exc
    return Image


def _dist(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def _min_anchor_dist(rgb: tuple[int, int, int], anchors: list[tuple[int, int, int]]) -> float:
    return min(_dist(rgb, a) for a in anchors)


def analyze(path: Path, zone: str, max_avg_dist: float, max_bright: float) -> int:
    if zone not in ZONE_PALETTES:
        known = ", ".join(sorted(ZONE_PALETTES))
        print(f"Unknown zone '{zone}'. Known: {known}", file=sys.stderr)
        return 2
    if not path.is_file():
        print(f"Screenshot not found: {path}", file=sys.stderr)
        return 2

    Image = _load_pillow()
    img = Image.open(path).convert("RGB")
    w, h = img.size
    anchors = ZONE_PALETTES[zone]

    # 8x8 grid sample (skip extreme edges)
    xs = [int(w * i / 9) for i in range(1, 9)]
    ys = [int(h * j / 9) for j in range(1, 9)]
    dists: list[float] = []
    bright_hits = 0
    pixels = img.load()
    for y in ys:
        for x in xs:
            r, g, b = pixels[x, y]
            dists.append(_min_anchor_dist((r, g, b), anchors))
            # Candy-bright guard: very high saturation + value
            if max(r, g, b) > 220 and (max(r, g, b) - min(r, g, b)) > 80:
                bright_hits += 1

    avg = sum(dists) / len(dists)
    bright_ratio = bright_hits / len(dists)
    print(f"zone={zone} screenshot={path}")
    print(f"  samples={len(dists)} avg_anchor_dist={avg:.2f} bright_pixel_ratio={bright_ratio:.2f}")

    ok = True
    if avg > max_avg_dist:
        print(f"  FAIL: avg distance {avg:.2f} > {max_avg_dist} (palette drift / default grey?)")
        ok = False
    if bright_ratio > max_bright:
        print(f"  FAIL: bright ratio {bright_ratio:.2f} > {max_bright} (candy-bright?)")
        ok = False
    if ok:
        print("  PASS")
        return 0
    return 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Screenshot palette check (VISUAL_QA.md)")
    parser.add_argument("--zone", required=True)
    parser.add_argument("--screenshot", required=True, type=Path)
    parser.add_argument(
        "--max-avg-dist",
        type=float,
        default=85.0,
        help="Max mean RGB distance to nearest zone anchor (default 85)",
    )
    parser.add_argument(
        "--max-bright-ratio",
        type=float,
        default=0.35,
        help="Max fraction of candy-bright samples (default 0.35)",
    )
    args = parser.parse_args()
    raise SystemExit(analyze(args.screenshot, args.zone, args.max_avg_dist, args.max_bright_ratio))


if __name__ == "__main__":
    main()
