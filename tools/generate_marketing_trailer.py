#!/usr/bin/env python3
"""
Generate marketing trailer from pitch illustrations.

Usage:
  python3 tools/generate_marketing_trailer.py
  python3 tools/generate_marketing_trailer.py --output steam/trailer.mp4

Requires: ffmpeg, ffprobe
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ILLUSTRATIONS = ROOT / "docs" / "pitch" / "illustrations"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

W, H = 1920, 1080
FPS = 30

# (image relative to illustrations/, duration_sec, headline, subline, zoom_mode)
SEGMENTS: list[tuple[str | None, float, str, str, str]] = [
    (None, 2.5, "TIDES OF URASHIMA", "A dark Urashima Taro JRPG", "title"),
    ("characters/party_lineup.png", 4.0, "He left for three days.", "Centuries had passed.", "zoom_in"),
    ("scenes/SC-00_prologue.png", 3.5, "He saved a wounded spirit.", "Paradise gave him a lacquer box.", "pan_right"),
    ("scenes/SC-01_shore_arrival.png", 3.5, "The sea spat him ashore.", "Alone.", "zoom_in"),
    ("scenes/SC-02_ruined_village.png", 3.0, "His village was gone.", "", "pan_left"),
    ("scenes/SC-03_cracked_torii.png", 3.0, "You left. We waited.", "", "zoom_in"),
    ("scenes/SC-04_roku_shack.png", 3.0, "That box is not a gift.", "Do not open it.", "pan_right"),
    ("scenes/SC-05_salt_crab.png", 2.5, "Turn-based combat", "Speed - Skills - Strategy", "zoom_in"),
    ("scenes/SC-06_cave_entrance.png", 2.5, "Descend the Tidal Caves.", "", "pan_left"),
    ("scenes/SC-07_water_puzzle.png", 2.0, "", "", "zoom_out"),
    ("scenes/SC-08_deep_pool.png", 3.0, "The drowned remember.", "", "zoom_in"),
    ("scenes/SC-09_shore_wraith.png", 3.5, "Confront the Shore Wraith.", "Boss phases - Intent UI", "pan_right"),
    ("scenes/SC-10_yuzu_join.png", 2.5, "Spirits join the fight.", "", "zoom_in"),
    ("scenes/SC-11_otohime_flashback.png", 3.0, "Paradise was too perfect.", "", "pan_left"),
    ("scenes/SC-12_palace_gate.png", 3.5, "The Dragon Palace Gate.", "", "zoom_in"),
    ("scenes/SC-13_mirror.png", 3.0, "The box holds stolen years.", "", "pan_right"),
    ("scenes/SC-14_sentinel.png", 2.5, "", "", "zoom_in"),
    ("scenes/SC-15_tide_keeper.png", 3.0, "The Tide Keeper waits.", "", "pan_left"),
    ("scenes/SC-16_choice.png", 4.0, "Three endings. One choice.", "Who pays for stolen time?", "zoom_in"),
    ("scenes/SC-17a_rewind.png", 2.0, "REWIND", "Restore the village", "zoom_in"),
    ("scenes/SC-17b_anchor.png", 2.0, "ANCHOR", "Bind the spirits", "zoom_in"),
    ("scenes/SC-17c_drift.png", 2.0, "DRIFT", "Refuse the bargain", "zoom_in"),
    ("characters/party_lineup.png", 4.5, "2-3 hours - 3 endings", "Walk the shore. Answer the tide.", "zoom_out"),
]


def esc(text: str) -> str:
    """Escape text for ffmpeg drawtext."""
    return (
        text.replace("\\", "\\\\")
        .replace("'", "\\'")
        .replace(":", "\\:")
        .replace("%", "\\%")
    )


def zoom_filter(mode: str, frames: int) -> str:
    """Ken Burns style zoompan filter chain prefix (after scale+crop)."""
    d = frames
    s = f"{W}x{H}"
    if mode == "title":
        return f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}"
    if mode == "pan_right":
        z = f"zoompan=z='1.15':x='(iw-iw/zoom)*on/{d}':y='(ih-ih/zoom)/2':d={d}:s={s}:fps={FPS}"
    elif mode == "pan_left":
        z = f"zoompan=z='1.15':x='(iw-iw/zoom)*(1-on/{d})':y='(ih-ih/zoom)/2':d={d}:s={s}:fps={FPS}"
    elif mode == "zoom_out":
        z = f"zoompan=z='if(lte(zoom,1.0),1.25,max(1.0,zoom-0.002))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={d}:s={s}:fps={FPS}"
    else:  # zoom_in
        z = f"zoompan=z='min(zoom+0.0012,1.25)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={d}:s={s}:fps={FPS}"
    return f"scale={W*2}:{H*2}:force_original_aspect_ratio=increase,crop={W*2}:{H*2},{z}"


def drawtext_filters(headline: str, subline: str, title_card: bool = False) -> str:
    """Build drawtext filter chain."""
    parts: list[str] = []
    if title_card:
        parts.append(
            f"drawtext=fontfile={FONT}:text='{esc(headline)}':fontsize=72:fontcolor=white:"
            f"x=(w-text_w)/2:y=(h-text_h)/2-30:box=1:boxcolor=0x1A1A2A@0.85:boxborderw=24"
        )
        if subline:
            parts.append(
                f"drawtext=fontfile={FONT_REG}:text='{esc(subline)}':fontsize=36:fontcolor=0xC9B89A:"
                f"x=(w-text_w)/2:y=(h-text_h)/2+50"
            )
        return ",".join(parts)

    # Vignette for readability
    parts.append(f"drawbox=x=0:y=0:w=iw:h=180:color=black@0.55:t=fill")
    parts.append(f"drawbox=x=0:y=h-220:w=iw:h=220:color=black@0.65:t=fill")

    if headline:
        fs = 52 if len(headline) < 28 else 44
        parts.append(
            f"drawtext=fontfile={FONT}:text='{esc(headline)}':fontsize={fs}:fontcolor=white:"
            f"x=(w-text_w)/2:y=h-175"
        )
    if subline:
        parts.append(
            f"drawtext=fontfile={FONT_REG}:text='{esc(subline)}':fontsize=32:fontcolor=0x8B9DAF:"
            f"x=(w-text_w)/2:y=h-95"
        )
    return ",".join(parts)


def make_title_card(out: Path, duration: float, headline: str, subline: str) -> None:
    vf = (
        f"{drawtext_filters(headline, subline, title_card=True)},"
        f"fade=t=in:st=0:d=0.4,fade=t=out:st={duration-0.5}:d=0.5"
    )
    run_ffmpeg([
        "-y", "-f", "lavfi", "-i", f"color=c=0x1A1A2A:s={W}x{H}:d={duration}:r={FPS}",
        "-vf", vf, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-t", str(duration), str(out),
    ])


def make_clip(image: Path, out: Path, duration: float, headline: str, subline: str, zoom_mode: str) -> None:
    frames = int(duration * FPS)
    dt = drawtext_filters(headline, subline)
    vf = (
        f"{zoom_filter(zoom_mode, frames)},"
        f"{dt},"
        f"fade=t=in:st=0:d=0.35,fade=t=out:st={max(0, duration-0.45):.2f}:d=0.45"
    )
    run_ffmpeg([
        "-y", "-loop", "1", "-i", str(image),
        "-vf", vf,
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-t", str(duration), str(out),
    ])


def run_ffmpeg(args: list[str]) -> None:
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        raise RuntimeError(f"ffmpeg failed: {' '.join(cmd)}")


def concat_clips(clips: list[Path], out: Path) -> None:
    list_file = out.parent / "concat_list.txt"
    with list_file.open("w") as f:
        for c in clips:
            f.write(f"file '{c.resolve()}'\n")
    run_ffmpeg(["-y", "-f", "concat", "-safe", "0", "-i", str(list_file),
                "-c:v", "libx264", "-pix_fmt", "yuv420p", str(out)])


def make_audio(duration: float, out: Path) -> None:
    """Melancholy ambient bed via layered sines + fade."""
    dur = int(duration) + 1
    fc = (
        f"[0:a]volume=0.07,afade=t=in:st=0:d=2,afade=t=out:st={dur-3}:d=3[a0];"
        f"[1:a]volume=0.04,afade=t=in:st=0:d=2,afade=t=out:st={dur-3}:d=3[a1];"
        f"[2:a]volume=0.025,afade=t=in:st=0:d=2,afade=t=out:st={dur-3}:d=3[a2];"
        f"[3:a]volume=0.015,lowpass=f=400,afade=t=in:st=0:d=2,afade=t=out:st={dur-3}:d=3[a3];"
        f"[a0][a1][a2][a3]amix=inputs=4:duration=longest:dropout_transition=2[aout]"
    )
    run_ffmpeg([
        "-y",
        "-f", "lavfi", "-i", f"sine=frequency=55:duration={dur}",
        "-f", "lavfi", "-i", f"sine=frequency=82.5:duration={dur}",
        "-f", "lavfi", "-i", f"sine=frequency=110:duration={dur}",
        "-f", "lavfi", "-i", f"anoisesrc=color=brown:duration={dur},lowpass=f=300",
        "-filter_complex", fc,
        "-map", "[aout]",
        "-c:a", "aac", "-b:a", "192k",
        "-t", str(duration),
        str(out),
    ])


def mux_video_audio(video: Path, audio: Path, out: Path) -> None:
    run_ffmpeg([
        "-y", "-i", str(video), "-i", str(audio),
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        "-shortest", str(out),
    ])


def probe_duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(result.stdout.strip())


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate marketing trailer from pitch art")
    parser.add_argument("--output", type=Path, default=ROOT / "steam" / "trailer.mp4")
    args = parser.parse_args()

    if not shutil.which("ffmpeg"):
        print("ffmpeg not found", file=sys.stderr)
        return 1

    out_path: Path = args.output
    out_path.parent.mkdir(parents=True, exist_ok=True)

    total_dur = sum(s[1] for s in SEGMENTS)
    print(f"Generating {len(SEGMENTS)} segments (~{total_dur:.0f}s)…")

    with tempfile.TemporaryDirectory(prefix="trailer_") as tmp:
        tmp_path = Path(tmp)
        clips: list[Path] = []

        for i, (rel, dur, head, sub, zoom) in enumerate(SEGMENTS):
            clip = tmp_path / f"clip_{i:02d}.mp4"
            if rel is None:
                make_title_card(clip, dur, head, sub)
            else:
                img = ILLUSTRATIONS / rel
                if not img.exists():
                    print(f"Missing: {img}", file=sys.stderr)
                    return 1
                make_clip(img, clip, dur, head, sub, zoom)
            clips.append(clip)
            print(f"  [{i+1}/{len(SEGMENTS)}] {rel or 'title'} ({dur}s)")

        silent = tmp_path / "silent.mp4"
        concat_clips(clips, silent)

        vid_dur = probe_duration(silent)
        audio = tmp_path / "audio.aac"
        make_audio(vid_dur, audio)
        mux_video_audio(silent, audio, out_path)

    size_mb = out_path.stat().st_size / (1024 * 1024)
    print(f"Done: {out_path} ({vid_dur:.1f}s, {size_mb:.1f} MB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
