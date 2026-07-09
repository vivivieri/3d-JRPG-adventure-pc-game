#!/usr/bin/env python3
"""Generate original stylized art assets for Tides of Urashima.

Low-poly coastal JRPG palette: muted fog, seaweed decay, biolume caves, coral palace.

Copyright: Original procedural output — MIT License (see repository LICENSE).
No third-party images, textures, or fonts are embedded except bundled Noto (OFL)
used only as a render tool for title text baked into PNG exports.
"""
from __future__ import annotations

import math
import os
import random
import subprocess
from typing import Tuple

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.join(os.path.dirname(__file__), "..")
ASSETS = os.path.join(ROOT, "game", "assets")
STEAM = os.path.join(ROOT, "steam")
RNG = random.Random(2026)

PALETTE = {
    "fog": "#8B9DAF",
    "wood": "#5C4A3A",
    "moss": "#3D5C4A",
    "rust": "#8B3A2A",
    "sand": "#C9B89A",
    "teal": "#1A4A5A",
    "biolume": "#4AE8D8",
    "stone": "#3A3A45",
    "coral": "#D4A55A",
    "crimson": "#8B2A3A",
    "ethereal": "#E8E4DC",
    "void": "#1A1A3A",
    "ink": "#1A1A2E",
    "hp": "#BF2E34",
    "mp": "#3A6EA8",
}


def noto_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Use bundled Noto (OFL) — never system fonts with unclear license."""
    fname = "NotoSans-Bold.ttf" if bold else "NotoSans-Regular.ttf"
    path = os.path.join(ASSETS, "fonts", fname)
    if os.path.isfile(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def hex_rgb(h: str) -> Tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def lerp(a: int, b: int, t: float) -> int:
    return int(a + (b - a) * t)


def lerp_color(c1: Tuple[int, int, int], c2: Tuple[int, int, int], t: float) -> Tuple[int, int, int]:
    return (lerp(c1[0], c2[0], t), lerp(c1[1], c2[1], t), lerp(c1[2], c2[2], t))


def noise_field(w: int, h: int, scale: float = 8.0) -> list[list[float]]:
    grid = [[RNG.random() for _ in range(w)] for _ in range(h)]
    out = [[0.0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            sx = int(x / scale)
            sy = int(y / scale)
            fx = (x / scale) - sx
            fy = (y / scale) - sy
            sx = min(sx, w - 2)
            sy = min(sy, h - 2)

            def smooth(t: float) -> float:
                return t * t * (3 - 2 * t)

            n00 = grid[sy][sx]
            n10 = grid[sy][sx + 1]
            n01 = grid[sy + 1][sx]
            n11 = grid[sy + 1][sx + 1]
            nx0 = n00 * (1 - smooth(fx)) + n10 * smooth(fx)
            nx1 = n01 * (1 - smooth(fx)) + n11 * smooth(fx)
            out[y][x] = nx0 * (1 - smooth(fy)) + nx1 * smooth(fy)
    return out


def make_tile_texture(name: str, base: str, accent: str, size: int = 256, grain: float = 0.2) -> None:
    c0 = hex_rgb(base)
    c1 = hex_rgb(accent)
    field = noise_field(size, size, scale=size / 16)
    img = Image.new("RGB", (size, size))
    px = img.load()
    for y in range(size):
        for x in range(size):
            n = field[y][x]
            # tileable edge fade
            edge = min(x, y, size - 1 - x, size - 1 - y) / (size * 0.15)
            edge = min(1.0, edge)
            t = n * grain + (1 - grain) * 0.5
            col = lerp_color(c0, c1, t)
            # subtle streaks
            streak = math.sin((x + y) * 0.08) * 0.05
            col = tuple(max(0, min(255, int(c + streak * 30))) for c in col)
            px[x, y] = col
    path = os.path.join(ASSETS, "textures", "zones", f"{name}.png")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)


def make_glow_texture(name: str, base: str, glow: str, size: int = 256) -> None:
    c0 = hex_rgb(base)
    g = hex_rgb(glow)
    field = noise_field(size, size, scale=size / 12)
    img = Image.new("RGB", (size, size))
    px = img.load()
    for y in range(size):
        for x in range(size):
            n = field[y][x]
            pulse = (math.sin(x * 0.12) * math.cos(y * 0.1) + 1) * 0.5
            t = n * 0.35 + pulse * 0.25
            col = lerp_color(c0, g, t)
            px[x, y] = col
    path = os.path.join(ASSETS, "textures", "zones", f"{name}.png")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)


def make_water_ripple_texture(size: int = 256) -> None:
    """Tileable water surface ripples."""
    c_deep = hex_rgb(PALETTE["teal"])
    c_shallow = hex_rgb("#3A8A9A")
    c_foam = hex_rgb("#6AB8C8")
    field = noise_field(size, size, scale=size / 10)
    field2 = noise_field(size, size, scale=size / 22)
    img = Image.new("RGBA", (size, size))
    px = img.load()
    for y in range(size):
        for x in range(size):
            n = field[y][x]
            n2 = field2[y][x]
            wave = math.sin((x + y) * 0.14) * 0.12 + math.sin(x * 0.09 - y * 0.11) * 0.1
            t = n * 0.55 + n2 * 0.35 + wave + 0.1
            t = max(0.0, min(1.0, t))
            col = lerp_color(c_deep, c_shallow, t)
            if t > 0.72:
                col = lerp_color(col, c_foam, (t - 0.72) / 0.28)
            alpha = int(180 + n2 * 60)
            px[x, y] = (*col, alpha)
    out = os.path.join(ASSETS, "textures", "zones", "water_ripple.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.save(out)
    print("  wrote", out)


def make_face_glow_texture(size: int = 128) -> None:
    """Soft spirit silhouette for underwater face VFX."""
    os.makedirs(os.path.join(ASSETS, "textures", "vfx"), exist_ok=True)
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2
    for r in range(size // 2, 0, -1):
        t = r / (size * 0.5)
        alpha = int(220 * (1.0 - t) ** 1.8)
        col = lerp_color(hex_rgb("#1A4A5A"), hex_rgb(PALETTE["biolume"]), 1.0 - t)
        draw.ellipse((cx - r, cy - r * 1.15, cx + r, cy + r * 1.15), fill=(*col, alpha))
    img = img.filter(ImageFilter.GaussianBlur(radius=2))
    out = os.path.join(ASSETS, "textures", "vfx", "face_glow.png")
    img.save(out)
    print("  wrote", out)


def ink_panel(size: Tuple[int, int], border_color: str, fill: Tuple[int, int, int, int]) -> Image.Image:
    w, h = size
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    bc = hex_rgb(border_color)
    draw.rounded_rectangle((4, 4, w - 5, h - 5), radius=10, fill=fill, outline=(*bc, 180), width=2)
    # ink wash corners
    wash = Image.new("RGBA", size, (0, 0, 0, 0))
    wd = ImageDraw.Draw(wash)
    for cx, cy in [(0, 0), (w, 0), (0, h), (w, h)]:
        wd.ellipse((cx - 40, cy - 40, cx + 40, cy + 40), fill=(20, 25, 35, 35))
    wash = wash.filter(ImageFilter.GaussianBlur(8))
    return Image.alpha_composite(img, wash)


def make_ui_assets() -> None:
    ui_dir = os.path.join(ASSETS, "ui")
    os.makedirs(ui_dir, exist_ok=True)

    panel = ink_panel((512, 256), PALETTE["biolume"], (*hex_rgb(PALETTE["ink"]), 215))
    panel.save(os.path.join(ui_dir, "panel_dialogue.png"))

    menu = ink_panel((640, 480), PALETTE["coral"], (*hex_rgb(PALETTE["ink"]), 230))
    menu.save(os.path.join(ui_dir, "panel_menu.png"))

    # HP / MP bars
    for name, color in [("hp_fill", PALETTE["hp"]), ("mp_fill", PALETTE["mp"])]:
        bar = Image.new("RGBA", (256, 24), (0, 0, 0, 0))
        d = ImageDraw.Draw(bar)
        c = hex_rgb(color)
        d.rounded_rectangle((0, 0, 255, 23), radius=4, fill=(*c, 255))
        # highlight
        d.rectangle((2, 2, 254, 8), fill=(min(255, c[0] + 40), min(255, c[1] + 40), min(255, c[2] + 40), 120))
        bar.save(os.path.join(ui_dir, f"bar_{name}.png"))

    bar_bg = Image.new("RGBA", (256, 24), (0, 0, 0, 0))
    d = ImageDraw.Draw(bar_bg)
    d.rounded_rectangle((0, 0, 255, 23), radius=4, fill=(30, 12, 12, 255), outline=(60, 30, 30, 255))
    bar_bg.save(os.path.join(ui_dir, "bar_bg.png"))

    # Combat intent icons 64x64
    icons = {
        "attack": ("#E8C878", [(32, 10), (20, 50), (32, 42), (44, 50)]),
        "defend": ("#6EC8C0", [(10, 28), (32, 12), (54, 28), (32, 52)]),
        "magic": ("#C878E8", [(32, 8), (40, 28), (56, 28), (44, 40), (48, 56), (32, 46), (16, 56), (20, 40), (8, 28), (24, 28)]),
        "skull": ("#D4A55A", None),
    }
    icon_dir = os.path.join(ui_dir, "icons")
    os.makedirs(icon_dir, exist_ok=True)
    for key, (col, poly) in icons.items():
        ic = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        d = ImageDraw.Draw(ic)
        c = hex_rgb(col)
        if key == "skull":
            d.ellipse((16, 14, 48, 44), fill=(*c, 230))
            d.rectangle((22, 44, 42, 52), fill=(*c, 230))
            d.ellipse((24, 24, 30, 32), fill=(20, 20, 30, 255))
            d.ellipse((34, 24, 40, 32), fill=(20, 20, 30, 255))
        else:
            d.polygon(poly, fill=(*c, 240))
        ic.save(os.path.join(icon_dir, f"intent_{key}.png"))


def draw_torii(draw: ImageDraw.ImageDraw, cx: int, cy: int, scale: float, color: Tuple[int, int, int]) -> None:
    w = int(8 * scale)
    h = int(50 * scale)
    draw.rectangle((cx - int(35 * scale), cy, cx - int(35 * scale) + w, cy + h), fill=color)
    draw.rectangle((cx + int(35 * scale) - w, cy, cx + int(35 * scale), cy + h), fill=color)
    draw.rectangle((cx - int(45 * scale), cy + int(8 * scale), cx + int(45 * scale), cy + int(8 * scale) + int(6 * scale)), fill=color)
    draw.rectangle((cx - int(35 * scale), cy + int(18 * scale), cx + int(35 * scale), cy + int(18 * scale) + int(4 * scale)), fill=hex_rgb(PALETTE["wood"]))


def make_main_menu_bg() -> None:
    w, h = 1920, 1080
    top = hex_rgb(PALETTE["fog"])
    bottom = hex_rgb(PALETTE["teal"])
    img = Image.new("RGB", (w, h))
    px = img.load()
    field = noise_field(w, h, scale=64)
    for y in range(h):
        t = y / h
        base = lerp_color(top, bottom, t ** 1.2)
        for x in range(w):
            n = field[y][x] * 0.08
            px[x, y] = tuple(max(0, min(255, int(c + (n - 0.04) * 80))) for c in base)

    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    # distant mountains
    pts = [(0, 700)]
    for i in range(12):
        pts.append((i * w // 11, 520 + RNG.randint(-40, 60)))
    pts += [(w, 680), (w, h), (0, h)]
    d.polygon(pts, fill=(40, 55, 65, 120))
    # ocean band
    d.rectangle((0, 720, w, h), fill=(26, 74, 90, 90))
  # waves
    for i in range(0, w, 120):
        d.arc((i, 760, i + 140, 820), 0, 180, fill=(74, 232, 216, 60), width=2)

    draw = ImageDraw.Draw(overlay)
    draw_torii(draw, w // 2, 620, 2.2, hex_rgb(PALETTE["rust"]))
    # submerged torii hint
    draw_torii(draw, w // 2 + 280, 780, 1.4, (*hex_rgb(PALETTE["rust"]), ))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    img = img.filter(ImageFilter.GaussianBlur(0.3))
    img.save(os.path.join(ASSETS, "ui", "main_menu_bg.png"))


def make_portrait(name: str, colors: Tuple[str, str, str], shape: str) -> None:
    """Stylized character portrait silhouette."""
    size = 256
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    bg = hex_rgb(colors[0])
    accent = hex_rgb(colors[1])
    skin = hex_rgb(colors[2])
    d.rounded_rectangle((8, 8, 248, 248), radius=12, fill=(*bg, 255), outline=(*accent, 200), width=2)

    if shape == "fisher":
        d.ellipse((88, 52, 168, 132), fill=(*skin, 255))
        d.polygon([(70, 140), (186, 140), (200, 230), (56, 230)], fill=(*hex_rgb(PALETTE["wood"]), 255))
        d.rectangle((100, 150, 156, 200), fill=(*accent, 255))
    elif shape == "maiden":
        d.ellipse((90, 50, 166, 126), fill=(*skin, 220))
        d.polygon([(72, 130), (184, 130), (196, 240), (60, 240)], fill=(*hex_rgb("#F0E8E0"), 200))
        d.rectangle((88, 180, 168, 240), fill=(*hex_rgb(PALETTE["crimson"]), 180))
        # spirit fade lower
        spirit = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        sd = ImageDraw.Draw(spirit)
        sd.rectangle((60, 190, 196, 248), fill=(*hex_rgb(PALETTE["biolume"]), 80))
        img = Image.alpha_composite(img, spirit)
        d = ImageDraw.Draw(img)
    elif shape == "diver":
        d.rounded_rectangle((78, 40, 178, 130), radius=20, fill=(*hex_rgb("#2A3A45"), 255))
        d.polygon([(64, 130), (192, 130), (204, 238), (52, 238)], fill=(*hex_rgb("#3A4A55"), 255))
        d.line((180, 80, 220, 50), fill=(*accent, 255), width=4)
    elif shape == "wraith":
        d.polygon([(128, 30), (200, 240), (56, 240)], fill=(*hex_rgb(PALETTE["stone"]), 220))
        d.ellipse((108, 60, 148, 100), fill=(*hex_rgb(PALETTE["biolume"]), 180))
    elif shape == "keeper":
        d.ellipse((70, 40, 186, 200), fill=(*hex_rgb(PALETTE["teal"]), 200))
        d.arc((40, 20, 216, 240), 200, 340, fill=(*hex_rgb(PALETTE["biolume"]), 200), width=6)

    path = os.path.join(ASSETS, "ui", "portraits", f"{name}.png")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path)


def make_icon() -> None:
    size = 512
    img = Image.new("RGBA", (size, size), hex_rgb(PALETTE["teal"]) + (255,))
    d = ImageDraw.Draw(img)
    # lacquer box
    d.rounded_rectangle((156, 120, 356, 360), radius=24, fill=hex_rgb(PALETTE["coral"]))
    d.rounded_rectangle((176, 140, 336, 340), radius=16, fill=hex_rgb(PALETTE["rust"]))
    # tide circle
    d.ellipse((106, 260, 406, 460), fill=(*hex_rgb(PALETTE["biolume"]), 200))
    d.arc((106, 260, 406, 460), 20, 160, fill=(*hex_rgb(PALETTE["ethereal"]), 180), width=8)
    img.save(os.path.join(ASSETS, "ui", "icon.png"))


def draw_title_card(img: Image.Image, title: str = "Tides of Urashima") -> Image.Image:
    draw = ImageDraw.Draw(img)
    font = noto_font(72, bold=True)
    sub = noto_font(28)
    w, h = img.size
    draw.text((w // 2, h - 120), title, fill=hex_rgb(PALETTE["ethereal"]), anchor="mm", font=font)
    draw.text((w // 2, h - 60), "A coastal JRPG folktale", fill=hex_rgb(PALETTE["fog"]), anchor="mm", font=sub)
    return img


def make_steam_capsules() -> None:
    specs = {
        "capsule_main.png": (1232, 706),
        "capsule_header.png": (920, 430),
        "capsule_small.png": (231, 87),
    }
    base_bg = Image.open(os.path.join(ASSETS, "ui", "main_menu_bg.png")).convert("RGB")
    for name, (w, h) in specs.items():
        img = base_bg.resize((w, h), Image.Resampling.LANCZOS)
        if name != "capsule_small.png":
            img = draw_title_card(img)
        # vignette
        vig = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        vd = ImageDraw.Draw(vig)
        vd.rectangle((0, 0, w, h), fill=(10, 20, 30, 60))
        img = Image.alpha_composite(img.convert("RGBA"), vig).convert("RGB")
        img.save(os.path.join(STEAM, name))


def make_screenshots() -> None:
    """Regenerate stylized screenshot placeholders."""
    shots = [
        ("01_village.png", PALETTE["fog"], PALETTE["sand"], "Ruined Village"),
        ("02_caves.png", PALETTE["teal"], PALETTE["biolume"], "Tidal Caves"),
        ("03_combat.png", PALETTE["void"], PALETTE["hp"], "Combat"),
        ("04_palace.png", PALETTE["void"], PALETTE["coral"], "Dragon Palace Gate"),
        ("05_endings.png", PALETTE["ink"], PALETTE["ethereal"], "Endings"),
    ]
    out = os.path.join(STEAM, "screenshots")
    os.makedirs(out, exist_ok=True)
    for fname, c1, c2, label in shots:
        w, h = 1280, 720
        top, bot = hex_rgb(c1), hex_rgb(c2)
        img = Image.new("RGB", (w, h))
        px = img.load()
        field = noise_field(w, h, 48)
        for y in range(h):
            t = y / h
            base = lerp_color(top, bot, t)
            for x in range(w):
                n = field[y][x]
                px[x, y] = tuple(max(0, min(255, int(c + (n - 0.5) * 40))) for c in base)
        d = ImageDraw.Draw(img)
        label_font = noto_font(36, bold=True)
        d.text((w // 2, h // 2), label, fill=hex_rgb(PALETTE["ethereal"]), anchor="mm", font=label_font)
        img.save(os.path.join(out, fname))


def make_trailer() -> None:
    """Slideshow of procedural screenshots + procedural village BGM (MIT)."""
    shots_dir = os.path.join(STEAM, "screenshots")
    audio = os.path.join(ASSETS, "audio", "bgm", "village.ogg")
    trailer = os.path.join(STEAM, "trailer.mp4")
    concat = os.path.join(shots_dir, "concat.txt")
    names = ["01_village.png", "02_caves.png", "03_combat.png", "04_palace.png", "05_endings.png"]
    with open(concat, "w") as f:
        for name in names:
            f.write(f"file '{name}'\n")
            f.write("duration 3\n")
        f.write(f"file '{names[-1]}'\n")
    slideshow = os.path.join(shots_dir, "trailer_slideshow.mp4")
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", concat,
            "-vf", "scale=1920:1080",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-t", "15",
            slideshow,
        ],
        check=True,
        cwd=shots_dir,
    )
    if os.path.isfile(audio):
        subprocess.run(
            [
                "ffmpeg", "-y", "-loglevel", "error",
                "-i", slideshow, "-i", audio,
                "-c:v", "copy", "-c:a", "aac", "-shortest",
                trailer,
            ],
            check=True,
        )
        os.remove(slideshow)
    else:
        os.replace(slideshow, trailer)


def main() -> None:
    make_tile_texture("village_ground", PALETTE["sand"], PALETTE["moss"])
    make_tile_texture("village_wood", PALETTE["wood"], PALETTE["rust"], grain=0.35)
    make_tile_texture("cave_stone", PALETTE["stone"], PALETTE["teal"])
    make_glow_texture("cave_algae", PALETTE["stone"], PALETTE["biolume"])
    make_tile_texture("palace_marble", PALETTE["ethereal"], PALETTE["coral"], grain=0.25)
    make_glow_texture("palace_gold", PALETTE["coral"], PALETTE["ethereal"])

    make_tile_texture("beach_sand", "#C4B48E", "#A89870", grain=0.28)
    make_water_ripple_texture()
    make_face_glow_texture()
    make_ui_assets()
    make_main_menu_bg()
    make_icon()

    portraits = [
        ("urashima", (PALETTE["teal"], PALETTE["rust"], "#D4B896"), "fisher"),
        ("yuzu", (PALETTE["void"], PALETTE["biolume"], "#E8D8C8"), "maiden"),
        ("roku", (PALETTE["stone"], PALETTE["biolume"], "#8A9AA8"), "diver"),
        ("shore_wraith", (PALETTE["teal"], PALETTE["biolume"], "#6A8A9A"), "wraith"),
        ("tide_keeper", (PALETTE["void"], PALETTE["coral"], "#4A8A9A"), "keeper"),
    ]
    for name, colors, shape in portraits:
        make_portrait(name, colors, shape)

    make_steam_capsules()
    make_screenshots()
    make_trailer()
    print("Generated game art in", ASSETS)


if __name__ == "__main__":
    main()
