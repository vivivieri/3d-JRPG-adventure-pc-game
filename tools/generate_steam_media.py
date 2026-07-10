#!/usr/bin/env python3
"""Generate Steam marketing screenshots and a short trailer placeholder."""
import os
import subprocess

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "steam", "screenshots")
TRAILER = os.path.join(ROOT, "steam", "trailer.mp4")
AUDIO = os.path.join(ROOT, "game", "assets", "audio", "bgm", "village.ogg")

SHOTS = [
    ("01_village.png", "0x8B9DAF", "Ruined Village"),
    ("02_caves.png", "0x1A4A5A", "Tidal Caves"),
    ("03_combat.png", "0x2A3238", "Turn-Based Combat"),
    ("04_palace.png", "0xD4A55A", "Dragon Palace Gate"),
    ("05_endings.png", "0x1A1A3A", "Three Endings"),
]


def make_screenshot(name: str, color: str, title: str) -> None:
    path = os.path.join(OUT, name)
    tmp = path + ".tmp.png"
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-f", "lavfi", "-i", f"color=c={color}:s=1920x1080",
            "-frames:v", "1",
            tmp,
        ],
        check=True,
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-i", tmp,
            "-vf",
            f"drawbox=x=0:y=880:w=1920:h=200:color=black@0.55:t=fill,"
            f"drawtext=text='Tides of Urashima - {title}':fontsize=42:fontcolor=white:x=60:y=940",
            path,
        ],
        check=True,
    )
    os.remove(tmp)


def make_trailer() -> None:
    concat = os.path.join(OUT, "concat.txt")
    with open(concat, "w") as f:
        for name, _, _ in SHOTS:
            f.write(f"file '{name}'\n")
            f.write("duration 3\n")
        f.write(f"file '{SHOTS[-1][0]}'\n")
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", concat,
            "-vf", "scale=1920:1080",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-t", "15",
            os.path.join(OUT, "trailer_slideshow.mp4"),
        ],
        check=True,
        cwd=OUT,
    )
    if os.path.isfile(AUDIO):
        subprocess.run(
            [
                "ffmpeg", "-y", "-loglevel", "error",
                "-i", os.path.join(OUT, "trailer_slideshow.mp4"),
                "-i", AUDIO,
                "-c:v", "copy", "-c:a", "aac", "-shortest",
                TRAILER,
            ],
            check=True,
        )
    else:
        os.replace(os.path.join(OUT, "trailer_slideshow.mp4"), TRAILER)


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    for name, color, title in SHOTS:
        make_screenshot(name, color, title)
    make_trailer()
    print("Wrote screenshots to", OUT)
    print("Wrote trailer to", TRAILER)


if __name__ == "__main__":
    main()
