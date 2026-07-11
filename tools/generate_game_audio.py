#!/usr/bin/env python3
"""Generate copyright-safe procedural game audio (ORIGINAL / MIT).

All output is synthesized — no sampled copyrighted material.
Registers entries in docs/asset_manifest.license.json.

Usage:
  python3 tools/generate_game_audio.py --all
  python3 tools/generate_game_audio.py --track bgm_village --track sfx_ui_confirm
"""
from __future__ import annotations

import argparse
import json
import math
import struct
import subprocess
import sys
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIO_ROOT = ROOT / "game" / "assets" / "audio"
MANIFEST = ROOT / "docs" / "asset_manifest.license.json"

SAMPLE_RATE = 44100


def _sine(freq: float, t: float, amp: float = 1.0) -> float:
    return amp * math.sin(2.0 * math.pi * freq * t)


def _adsr(t: float, dur: float, a: float = 0.02, d: float = 0.05, s: float = 0.6, r: float = 0.1) -> float:
    if t < a:
        return t / a
    if t < a + d:
        return 1.0 - (1.0 - s) * ((t - a) / d)
    if t < dur - r:
        return s
    if t < dur:
        return s * (1.0 - (t - (dur - r)) / r)
    return 0.0


def synth_bgm(name: str, duration: float, freqs: list[float]) -> list[float]:
    samples: list[float] = []
    n = int(duration * SAMPLE_RATE)
    for i in range(n):
        t = i / SAMPLE_RATE
        v = 0.0
        for j, f in enumerate(freqs):
            v += _sine(f, t, 0.12 / (j + 1))
            v += _sine(f * 1.5, t, 0.06 / (j + 1))
        # gentle tremolo
        v *= 0.85 + 0.15 * math.sin(2.0 * math.pi * 0.25 * t)
        samples.append(max(-1.0, min(1.0, v * 0.35)))
    return samples


def synth_sfx(name: str, duration: float, freq: float) -> list[float]:
    samples: list[float] = []
    n = int(duration * SAMPLE_RATE)
    for i in range(n):
        t = i / SAMPLE_RATE
        env = _adsr(t, duration, a=0.005, d=0.08, s=0.0, r=0.04)
        v = _sine(freq, t, 1.0) * env
        if "hit" in name:
            v += _sine(freq * 0.5, t, 0.5) * env
        samples.append(max(-1.0, min(1.0, v)))
    return samples


TRACKS: dict[str, dict] = {
    "bgm_menu": {"kind": "bgm", "dur": 12.0, "freqs": [196, 294, 392]},
    "bgm_field": {"kind": "bgm", "dur": 16.0, "freqs": [174, 261, 349]},
    "bgm_village": {"kind": "bgm", "dur": 16.0, "freqs": [155, 233, 311]},
    "bgm_caves": {"kind": "bgm", "dur": 14.0, "freqs": [220, 330, 440]},
    "bgm_combat": {"kind": "bgm", "dur": 10.0, "freqs": [146, 220, 293]},
    "bgm_palace": {"kind": "bgm", "dur": 14.0, "freqs": [130, 196, 261]},
    "bgm_ending_rewind": {"kind": "bgm", "dur": 12.0, "freqs": [165, 247, 330]},
    "bgm_ending_anchor": {"kind": "bgm", "dur": 12.0, "freqs": [175, 262, 349]},
    "bgm_ending_drift": {"kind": "bgm", "dur": 12.0, "freqs": [147, 220, 294]},
    "sfx_ui": {"kind": "sfx", "dur": 0.12, "freq": 880},
    "sfx_ui_confirm": {"kind": "sfx", "dur": 0.15, "freq": 660},
    "sfx_hit": {"kind": "sfx", "dur": 0.18, "freq": 140},
    "sfx_victory": {"kind": "sfx", "dur": 0.6, "freq": 523},
}


def write_wav(path: Path, samples: list[float]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        frames = b"".join(struct.pack("<h", int(max(-1.0, min(1.0, s)) * 32767)) for s in samples)
        wf.writeframes(frames)


def wav_to_ogg(wav_path: Path, ogg_path: Path) -> None:
    ogg_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(wav_path), "-c:a", "libvorbis", "-q:a", "4", str(ogg_path)],
        check=True,
        capture_output=True,
    )
    wav_path.unlink(missing_ok=True)


def register_asset(rel_path: str, used_for: str) -> None:
    if not MANIFEST.exists():
        return
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assets = data.setdefault("assets", [])
    for a in assets:
        if a.get("path") == rel_path:
            return
    assets.append({
        "path": rel_path,
        "license": "ORIGINAL",
        "source": "Procedural synthesis (tools/generate_game_audio.py)",
        "author": "Project tooling",
        "used_for": used_for,
        "notes": "Copyright-safe; replace before final ship if desired",
    })
    data["updated"] = str(__import__("datetime").date.today())
    MANIFEST.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def generate_one(track_id: str) -> Path:
    spec = TRACKS[track_id]
    kind = spec["kind"]
    sub = "bgm" if kind == "bgm" else "sfx"
    out = AUDIO_ROOT / sub / f"{track_id}.ogg"
    wav_tmp = AUDIO_ROOT / sub / f".{track_id}.wav"
    if kind == "bgm":
        samples = synth_bgm(track_id, spec["dur"], spec["freqs"])
    else:
        samples = synth_sfx(track_id, spec["dur"], spec["freq"])
    write_wav(wav_tmp, samples)
    wav_to_ogg(wav_tmp, out)
    register_asset(f"game/assets/audio/{sub}/{track_id}.ogg", f"Procedural {kind}: {track_id}")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate procedural copyright-safe game audio")
    ap.add_argument("--all", action="store_true", help="Generate all defined tracks")
    ap.add_argument("--track", action="append", dest="tracks", default=[], help="Track id (repeatable)")
    args = ap.parse_args()

    ids = list(TRACKS.keys()) if args.all else args.tracks
    if not ids:
        ap.print_help()
        return 1

    for tid in ids:
        if tid not in TRACKS:
            print(f"Unknown track: {tid}", file=sys.stderr)
            return 1
        path = generate_one(tid)
        print(f"Generated {path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
