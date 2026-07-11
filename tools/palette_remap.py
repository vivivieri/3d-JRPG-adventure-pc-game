#!/usr/bin/env python3
"""Remap generated texture hues toward zone palette rows in docs/ART_DIRECTION.md.

Post-process step for ComfyUI, GameLab, and Material Maker exports.
See docs/ART_AUTOMATION_PIPELINE.md §6.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Zone palette anchors (hex) — mirrors docs/ART_DIRECTION.md §1
ZONE_PALETTES: dict[str, list[str]] = {
    "ruined_village": ["#8B9DAF", "#5C4A3A", "#3D5C4A", "#8B3A2A", "#C9B89A"],
    "beach": ["#8B9DAF", "#C9B89A", "#3D5C4A", "#1A4A5A"],
    "tidal_caves": ["#1A4A5A", "#4AE8D8", "#3A3A45"],
    "palace_gate": ["#D4A55A", "#8B2A3A", "#E8E4DC", "#1A1A3A"],
}


def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _load_pillow():
    try:
        from PIL import Image
    except ImportError as exc:
        print(
            "palette_remap.py requires Pillow: pip install Pillow",
            file=sys.stderr,
        )
        raise SystemExit(2) from exc
    return Image


def remap_image(input_path: Path, output_path: Path, zone: str, strength: float) -> None:
    if zone not in ZONE_PALETTES:
        known = ", ".join(sorted(ZONE_PALETTES))
        raise SystemExit(f"Unknown zone '{zone}'. Known: {known}")

    Image = _load_pillow()
    anchors = [_hex_to_rgb(h) for h in ZONE_PALETTES[zone]]
    img = Image.open(input_path).convert("RGB")
    pixels = img.load()
    w, h = img.size
    strength = max(0.0, min(1.0, strength))

    for y in range(h):
        for x in range(w):
            r, g, b = pixels[x, y]
            # Nearest anchor in RGB space (simple v1 — sufficient for stylized NPR)
            best = min(
                anchors,
                key=lambda a: (r - a[0]) ** 2 + (g - a[1]) ** 2 + (b - a[2]) ** 2,
            )
            pixels[x, y] = (
                int(r + (best[0] - r) * strength),
                int(g + (best[1] - g) * strength),
                int(b + (best[2] - b) * strength),
            )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path)
    print(f"Wrote {output_path} (zone={zone}, strength={strength})")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Remap generated textures toward zone palette (ART_AUTOMATION_PIPELINE.md)."
    )
    parser.add_argument("--zone", required=True, help="Zone id (e.g. ruined_village)")
    parser.add_argument("--input", required=True, type=Path, help="Source PNG")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output PNG (default: overwrite --input)",
    )
    parser.add_argument(
        "--strength",
        type=float,
        default=0.35,
        help="Blend toward nearest palette anchor (0–1, default 0.35)",
    )
    args = parser.parse_args()
    out = args.output or args.input
    if not args.input.is_file():
        raise SystemExit(f"Input not found: {args.input}")
    remap_image(args.input, out, args.zone, args.strength)


if __name__ == "__main__":
    main()
