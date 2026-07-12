#!/usr/bin/env python3
"""
Generate marketing trailer from pitch illustrations.

Usage:
  python3 tools/generate_marketing_trailer.py
  python3 tools/generate_marketing_trailer.py --locale ja
  python3 tools/generate_marketing_trailer.py --all-locales

Requires: ffmpeg, ffprobe, numpy
"""

from __future__ import annotations

import argparse
import json
import shutil
import struct
import subprocess
import sys
import tempfile
import wave
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ILLUSTRATIONS = ROOT / "docs" / "pitch" / "illustrations"
LOCALES_FILE = ROOT / "steam" / "trailer_locales.json"
BGM_PATH = ROOT / "steam" / "trailer_bgm.ogg"

W, H = 1920, 1080
FPS = 30
SAMPLE_RATE = 44100

ALL_LOCALES = ["en", "ja", "zh", "zh-Hant"]
CJK_LOCALES = frozenset({"ja", "zh", "zh-Hant"})

FONT_CANDIDATES: dict[str, list[tuple[str, str]]] = {
    "en": [
        (
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ),
    ],
    "ja": [
        (
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        ),
    ],
    "zh": [
        (
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        ),
    ],
    "zh-Hant": [
        (
            str(ROOT / "game" / "assets" / "fonts" / "NotoSansTC-Bold.otf"),
            str(ROOT / "game" / "assets" / "fonts" / "NotoSansTC-Regular.otf"),
        ),
        (
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        ),
    ],
}

LOCALE_OUTPUTS: dict[str, Path] = {
    "en": ROOT / "steam" / "trailer.mp4",
    "ja": ROOT / "steam" / "trailer_ja.mp4",
    "zh": ROOT / "steam" / "trailer_zh.mp4",
    "zh-Hant": ROOT / "steam" / "trailer_zh-Hant.mp4",
}


def resolve_locale_fonts(locale: str) -> tuple[str, str]:
    """Pick first available bold/regular font pair for a locale."""
    for bold, regular in FONT_CANDIDATES.get(locale, FONT_CANDIDATES["en"]):
        if Path(bold).exists() and Path(regular).exists():
            return bold, regular
    raise FileNotFoundError(f"No fonts found for locale {locale}")


def esc(text: str) -> str:
    """Escape text for ffmpeg drawtext."""
    return (
        text.replace("\\", "\\\\")
        .replace("'", "\\'")
        .replace(":", "\\:")
        .replace("%", "\\%")
    )


def load_segments(locale: str) -> list[tuple[str | None, float, str, str, str]]:
    """Load segment metadata and localized on-screen text."""
    data = json.loads(LOCALES_FILE.read_text(encoding="utf-8"))
    segments: list[tuple[str | None, float, str, str, str]] = []
    for i, seg in enumerate(data["segments"]):
        text_map: dict[str, Any] = seg["text"]
        if locale not in text_map:
            raise KeyError(f"Segment {i}: missing locale {locale!r} in trailer_locales.json")
        text = text_map[locale]
        headline = text[0] if len(text) > 0 else ""
        subline = text[1] if len(text) > 1 else ""
        segments.append((seg["image"], float(seg["duration"]), headline, subline, seg["zoom"]))
    return segments


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


def headline_fontsize(headline: str, locale: str) -> int:
    if locale in CJK_LOCALES:
        if len(headline) <= 12:
            return 52
        if len(headline) <= 18:
            return 44
        return 38
    return 52 if len(headline) < 28 else 44


def drawtext_filters(
    headline: str,
    subline: str,
    font_bold: str,
    font_reg: str,
    locale: str,
    title_card: bool = False,
) -> str:
    """Build drawtext filter chain."""
    parts: list[str] = []
    if title_card:
        title_fs = 64 if locale in CJK_LOCALES else 72
        sub_fs = 34 if locale in CJK_LOCALES else 36
        parts.append(
            f"drawtext=fontfile={font_bold}:text='{esc(headline)}':fontsize={title_fs}:fontcolor=white:"
            f"x=(w-text_w)/2:y=(h-text_h)/2-30:box=1:boxcolor=0x1A1A2A@0.85:boxborderw=24"
        )
        if subline:
            parts.append(
                f"drawtext=fontfile={font_reg}:text='{esc(subline)}':fontsize={sub_fs}:fontcolor=0xC9B89A:"
                f"x=(w-text_w)/2:y=(h-text_h)/2+50"
            )
        return ",".join(parts)

    parts.append("drawbox=x=0:y=0:w=iw:h=180:color=black@0.55:t=fill")
    parts.append("drawbox=x=0:y=h-220:w=iw:h=220:color=black@0.65:t=fill")

    if headline:
        fs = headline_fontsize(headline, locale)
        parts.append(
            f"drawtext=fontfile={font_bold}:text='{esc(headline)}':fontsize={fs}:fontcolor=white:"
            f"x=(w-text_w)/2:y=h-175"
        )
    if subline:
        sub_fs = 30 if locale in CJK_LOCALES and len(subline) > 24 else 32
        parts.append(
            f"drawtext=fontfile={font_reg}:text='{esc(subline)}':fontsize={sub_fs}:fontcolor=0x8B9DAF:"
            f"x=(w-text_w)/2:y=h-95"
        )
    return ",".join(parts)


def make_title_card(
    out: Path,
    duration: float,
    headline: str,
    subline: str,
    font_bold: str,
    font_reg: str,
    locale: str,
) -> None:
    vf = (
        f"{drawtext_filters(headline, subline, font_bold, font_reg, locale, title_card=True)},"
        f"fade=t=in:st=0:d=0.4,fade=t=out:st={duration-0.5}:d=0.5"
    )
    run_ffmpeg([
        "-y", "-f", "lavfi", "-i", f"color=c=0x1A1A2A:s={W}x{H}:d={duration}:r={FPS}",
        "-vf", vf, "-c:v", "libx264", "-pix_fmt", "yuv420p", "-t", str(duration), str(out),
    ])


def make_clip(
    image: Path,
    out: Path,
    duration: float,
    headline: str,
    subline: str,
    zoom_mode: str,
    font_bold: str,
    font_reg: str,
    locale: str,
) -> None:
    frames = int(duration * FPS)
    dt = drawtext_filters(headline, subline, font_bold, font_reg, locale)
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


def write_wav(path: Path, samples: np.ndarray, sample_rate: int = SAMPLE_RATE) -> None:
    """Write mono float samples as 16-bit PCM WAV."""
    clipped = np.clip(samples, -1.0, 1.0)
    pcm = (clipped * 32767).astype(np.int16)
    with wave.open(str(path), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(struct.pack(f"<{len(pcm)}h", *pcm))


def generate_bgm_wav(duration: float, out: Path) -> None:
    """
    Procedural melancholy JRPG trailer score.

  Pentatonic pad, sparse koto-like melody, soft taiko pulse, ocean undertone.
    """
    n = int(duration * SAMPLE_RATE)
    t = np.arange(n, dtype=np.float64) / SAMPLE_RATE
    audio = np.zeros(n, dtype=np.float64)

    # E minor pentatonic palette (shore / Urashima mood)
    pad_freqs = [82.41, 110.0, 164.81, 196.0, 220.0, 293.66]
    for i, freq in enumerate(pad_freqs):
        lfo = 0.55 + 0.45 * np.sin(2 * np.pi * (0.018 + i * 0.004) * t + i * 0.7)
        audio += 0.045 * lfo * np.sin(2 * np.pi * freq * t)

    # Slow harmonic swell every ~16s
    swell = 0.5 + 0.5 * np.sin(2 * np.pi * t / 16.0)
    audio *= 0.85 + 0.15 * swell

    # Sparse pentatonic melody (koto pluck)
    melody = [293.66, 329.63, 293.66, 246.94, 220.0, 246.94, 196.0, 220.0,
              246.94, 293.66, 329.63, 293.66, 246.94, 220.0, 196.0, 164.81]
    phrase_len = duration / len(melody)
    for i, freq in enumerate(melody):
        start = int(i * phrase_len * SAMPLE_RATE)
        seg_n = max(1, int(phrase_len * 0.85 * SAMPLE_RATE))
        end = min(n, start + seg_n)
        if start >= n:
            break
        seg_t = np.arange(end - start, dtype=np.float64) / SAMPLE_RATE
        pluck = np.exp(-seg_t * 2.8) * (0.11 + 0.04 * np.sin(2 * np.pi * freq * seg_t * 0.5))
        audio[start:end] += pluck * np.sin(2 * np.pi * freq * seg_t)
        # octave shimmer
        audio[start:end] += 0.03 * pluck * np.sin(2 * np.pi * freq * 2 * seg_t)

    # Soft taiko pulse on half-notes
    beat_interval = 2.0
    beat_times = np.arange(0, duration, beat_interval)
    for beat in beat_times:
        start = int(beat * SAMPLE_RATE)
        beat_n = int(0.18 * SAMPLE_RATE)
        end = min(n, start + beat_n)
        if start >= n:
            break
        beat_t = np.arange(end - start, dtype=np.float64) / SAMPLE_RATE
        pulse = np.exp(-beat_t * 22) * np.sin(2 * np.pi * (58 + beat * 0.01) * beat_t)
        audio[start:end] += 0.07 * pulse

    # Ocean undertone (filtered noise via summed sines)
    ocean = np.zeros(n, dtype=np.float64)
    for f in [0.4, 0.7, 1.1, 1.6]:
        ocean += np.sin(2 * np.pi * f * t + np.sin(2 * np.pi * 0.09 * t) * 1.5)
    audio += 0.012 * ocean

    # Fade in/out
    fade = int(3.5 * SAMPLE_RATE)
    fade = min(fade, n // 4)
    if fade > 0:
        ramp_in = np.linspace(0.0, 1.0, fade)
        ramp_out = np.linspace(1.0, 0.0, fade)
        audio[:fade] *= ramp_in
        audio[-fade:] *= ramp_out

    peak = np.max(np.abs(audio))
    if peak > 0:
        audio = audio / peak * 0.82

    write_wav(out, audio)


def ensure_bgm(duration: float, out: Path = BGM_PATH, force: bool = False) -> Path:
    """Generate trailer BGM once and cache as OGG."""
    if out.exists() and not force:
        return out

    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="trailer_bgm_") as tmp:
        wav = Path(tmp) / "bgm.wav"
        generate_bgm_wav(duration, wav)
        run_ffmpeg([
            "-y", "-i", str(wav),
            "-c:a", "libvorbis", "-q:a", "6",
            "-t", str(duration),
            str(out),
        ])
    return out


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


def build_trailer(
    locale: str,
    out_path: Path,
    segments: list[tuple[str | None, float, str, str, str]],
    bgm_path: Path,
) -> float:
    font_bold, font_reg = resolve_locale_fonts(locale)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    total_dur = sum(s[1] for s in segments)
    print(f"[{locale}] Generating {len(segments)} segments (~{total_dur:.0f}s) -> {out_path.name}")

    with tempfile.TemporaryDirectory(prefix=f"trailer_{locale}_") as tmp:
        tmp_path = Path(tmp)
        clips: list[Path] = []

        for i, (rel, dur, head, sub, zoom) in enumerate(segments):
            clip = tmp_path / f"clip_{i:02d}.mp4"
            if rel is None:
                make_title_card(clip, dur, head, sub, font_bold, font_reg, locale)
            else:
                img = ILLUSTRATIONS / rel
                if not img.exists():
                    raise FileNotFoundError(f"Missing illustration: {img}")
                make_clip(img, clip, dur, head, sub, zoom, font_bold, font_reg, locale)
            clips.append(clip)
            print(f"  [{i+1}/{len(segments)}] {rel or 'title'} ({dur}s)")

        silent = tmp_path / "silent.mp4"
        concat_clips(clips, silent)
        vid_dur = probe_duration(silent)
        mux_video_audio(silent, bgm_path, out_path)

    size_mb = out_path.stat().st_size / (1024 * 1024)
    print(f"[{locale}] Done: {out_path} ({vid_dur:.1f}s, {size_mb:.1f} MB)")
    return vid_dur


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate marketing trailer from pitch art")
    parser.add_argument("--locale", choices=ALL_LOCALES, default="en",
                        help="On-screen text language (default: en)")
    parser.add_argument("--all-locales", action="store_true",
                        help="Render en, ja, zh, and zh-Hant trailers")
    parser.add_argument("--output", type=Path, default=None,
                        help="Output path (single-locale mode only)")
    parser.add_argument("--regen-bgm", action="store_true",
                        help="Regenerate cached BGM even if trailer_bgm.ogg exists")
    args = parser.parse_args()

    if not shutil.which("ffmpeg"):
        print("ffmpeg not found", file=sys.stderr)
        return 1
    if not LOCALES_FILE.exists():
        print(f"Missing locale data: {LOCALES_FILE}", file=sys.stderr)
        return 1

    locales = ALL_LOCALES if args.all_locales else [args.locale]
    segments_by_locale = {loc: load_segments(loc) for loc in locales}
    duration = sum(s[1] for s in segments_by_locale[locales[0]])

    try:
        bgm_path = ensure_bgm(duration, force=args.regen_bgm)
        print(f"BGM: {bgm_path} ({probe_duration(bgm_path):.1f}s)")
    except Exception as exc:
        print(f"BGM generation failed: {exc}", file=sys.stderr)
        return 1

    for locale in locales:
        out = args.output if args.output and not args.all_locales else LOCALE_OUTPUTS[locale]
        try:
            build_trailer(locale, out, segments_by_locale[locale], bgm_path)
        except (FileNotFoundError, RuntimeError) as exc:
            print(exc, file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
