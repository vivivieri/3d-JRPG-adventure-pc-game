#!/usr/bin/env python3
"""Generate original procedural audio for Tides of Urashima.

Copyright: Original procedural synthesis — MIT License (see repository LICENSE).
No samples, loops, or recordings from third-party libraries are used.
"""
from __future__ import annotations

import math
import os
import random
import struct
import subprocess
import wave

import numpy as np

SR = 44100
OUT = os.path.join(os.path.dirname(__file__), "..", "game", "assets", "audio")
RNG = np.random.default_rng(2026)


def write_wav(path: str, samples: np.ndarray) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    clipped = np.clip(samples, -1.0, 1.0)
    frames = (clipped * 32767).astype(np.int16)
    with wave.open(path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(frames.tobytes())


def to_ogg(wav_path: str) -> None:
    ogg_path = wav_path.rsplit(".", 1)[0] + ".ogg"
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", wav_path, "-c:a", "libvorbis", "-q:a", "5", ogg_path],
        check=True,
    )
    os.remove(wav_path)


def t(length: float) -> np.ndarray:
    return np.linspace(0, length, int(SR * length), endpoint=False)


def fade_loop(samples: np.ndarray, fade_s: float = 2.0) -> np.ndarray:
    n = len(samples)
    fade = int(SR * fade_s)
    fade = min(fade, n // 4)
    env = np.ones(n)
    ramp = np.linspace(0, 1, fade)
    env[:fade] = ramp
    env[-fade:] = ramp[::-1]
    return samples * env


def lowpass(samples: np.ndarray, cutoff: float = 800.0) -> np.ndarray:
    """Simple one-pole low-pass."""
    rc = 1.0 / (2 * math.pi * cutoff)
    dt = 1.0 / SR
    alpha = dt / (rc + dt)
    out = np.zeros_like(samples)
    for i in range(1, len(samples)):
        out[i] = out[i - 1] + alpha * (samples[i] - out[i - 1])
    return out


def sine(freq: float, length: float, phase: float = 0.0) -> np.ndarray:
    tt = t(length)
    return np.sin(2 * math.pi * freq * tt + phase)


def tone(freq: float, length: float, attack: float = 0.02, decay: float = 0.3, volume: float = 0.5) -> np.ndarray:
    tt = t(length)
    env = np.exp(-decay * tt)
    env *= np.minimum(1.0, tt / max(attack, 1e-4))
    wave_ = sine(freq, length) * env * volume
    # breathy overtone for flute-like timbre
    wave_ += sine(freq * 2.01, length) * env * volume * 0.12
    wave_ += sine(freq * 0.5, length) * env * volume * 0.08
    return wave_


def pluck(freq: float, length: float = 1.2, volume: float = 0.35) -> np.ndarray:
    """Koto-like plucked string."""
    tt = t(length)
    env = np.exp(-3.5 * tt)
    s = np.zeros_like(tt)
    for h, amp in enumerate([1.0, 0.5, 0.25, 0.12], start=1):
        s += np.sin(2 * math.pi * freq * h * tt) * amp
    return s * env * volume / 2.0


def bell(freq: float, length: float = 2.5, volume: float = 0.4) -> np.ndarray:
    tt = t(length)
    env = np.exp(-1.8 * tt)
    s = np.sin(2 * math.pi * freq * tt) * env
    s += np.sin(2 * math.pi * freq * 2.4 * tt) * env * 0.35
    s += np.sin(2 * math.pi * freq * 3.8 * tt) * env * 0.15
    return s * volume


def taiko(length: float = 0.35, pitch: float = 80.0, volume: float = 0.55) -> np.ndarray:
    tt = t(length)
    env = np.exp(-7.0 * tt)
    body = np.sin(2 * math.pi * pitch * tt) * env
    noise = RNG.normal(0, 1, len(tt)) * np.exp(-22.0 * tt) * 0.35
    return (body + noise) * volume


def ocean_noise(length: float, volume: float = 0.08) -> np.ndarray:
    n = int(SR * length)
    raw = RNG.normal(0, 1, n)
    smoothed = lowpass(raw, 320)
    # slow swell
    swell = (np.sin(2 * math.pi * 0.08 * t(length)) + 1) * 0.5
    swell *= (np.sin(2 * math.pi * 0.03 * t(length) + 1.2) + 1) * 0.5
    return smoothed * swell * volume


def mix_at(dst: np.ndarray, src: np.ndarray, start: int, gain: float = 1.0) -> None:
    end = min(len(dst), start + len(src))
    length = end - start
    if length > 0:
        dst[start : start + length] += src[:length] * gain


# Pentatonic scales (Hz) — D minor pentatonic base
DMIN = [146.83, 174.61, 196.00, 220.00, 261.63, 293.66, 329.63]  # D3..E4
AMIN = [110.00, 130.81, 146.83, 164.81, 196.00, 220.00, 246.94]
PALACE = [164.81, 196.00, 246.94, 293.66, 329.63, 392.00, 440.00]


def compose_ambient(name: str, scale: list[float], duration: float, mood: dict) -> None:
    n = int(SR * duration)
    buf = np.zeros(n)
    buf += ocean_noise(duration, mood.get("ocean", 0.06))

    # Pad drones
    for i, f in enumerate(scale[:3]):
        drone = sine(f, duration, phase=i * 0.7) * mood.get("drone", 0.04)
        buf += drone

    # Melodic koto/shakuhachi phrases
    beat = mood.get("beat", 3.2)
    pos = int(SR * 1.5)
    note_idx = 0
    while pos < n - SR:
        freq = scale[note_idx % len(scale)]
        note_len = mood.get("note_len", 1.4)
        if mood.get("flute", False):
            note = tone(freq * mood.get("pitch_mul", 1.0), note_len, volume=mood.get("lead", 0.18))
        else:
            note = pluck(freq * mood.get("pitch_mul", 1.0), note_len, volume=mood.get("lead", 0.14))
        mix_at(buf, note, pos)
        note_idx += mood.get("step", 2)
        pos += int(SR * beat * RNG.uniform(0.85, 1.15))

    # Optional wind
    if mood.get("wind", 0) > 0:
        wind = lowpass(RNG.normal(0, 1, n), 600) * mood["wind"]
        buf += wind * (np.sin(2 * math.pi * 0.05 * t(duration)) * 0.5 + 0.5)

    buf = fade_loop(buf, mood.get("fade", 2.5))
    buf = np.tanh(buf * mood.get("drive", 1.2)) * mood.get("master", 0.55)
    write_wav(os.path.join(OUT, "bgm", f"{name}.wav"), buf)


def compose_combat(name: str, duration: float, boss: bool = False) -> None:
    n = int(SR * duration)
    buf = np.zeros(n)
    buf += ocean_noise(duration, 0.03 if not boss else 0.02)

    tempo = 0.55 if boss else 0.65
    scale = [82.41, 98.00, 110.00, 123.47, 146.83] if boss else [98.00, 116.54, 130.81, 146.83, 174.61]
    pos = 0
    beat_n = 0
    while pos < n - SR // 2:
        if beat_n % 4 == 0:
            mix_at(buf, taiko(0.4, 65 if boss else 75, 0.5 if boss else 0.38), pos)
        elif beat_n % 2 == 0:
            mix_at(buf, taiko(0.22, 120, 0.22), pos)
        if beat_n % 8 == 2:
            freq = scale[beat_n % len(scale)]
            mix_at(buf, pluck(freq, 0.9, 0.2), pos + int(SR * 0.05))
        beat_n += 1
        pos += int(SR * tempo)

    # Tension pad
    for f in scale[:3]:
        buf += sine(f, duration) * (0.06 if boss else 0.045)

    buf = fade_loop(buf, 1.8)
    buf = np.tanh(buf * (1.4 if boss else 1.1)) * (0.62 if boss else 0.52)
    write_wav(os.path.join(OUT, "bgm", f"{name}.wav"), buf)


def make_sfx() -> None:
    sfx_dir = os.path.join(OUT, "sfx")

    # Temple bell confirm
    write_wav(os.path.join(sfx_dir, "ui_confirm.wav"), bell(523.25, 0.35, 0.38)[: int(SR * 0.35)])

  # Soft woodblock cancel
    cancel = tone(220, 0.18, attack=0.001, decay=12, volume=0.3)
    cancel += tone(165, 0.18, attack=0.001, decay=14, volume=0.18)
    write_wav(os.path.join(sfx_dir, "ui_cancel.wav"), cancel)

    # Shell chime interact
    interact = pluck(659.25, 0.3, 0.32)
    mix_at(interact, pluck(783.99, 0.2, 0.2), int(SR * 0.08))
    write_wav(os.path.join(sfx_dir, "interact.wav"), interact[: int(SR * 0.3)])

    # Healing shimmer
    heal = bell(392, 0.55, 0.28)
    mix_at(heal, bell(494, 0.45, 0.22), int(SR * 0.15))
    write_wav(os.path.join(sfx_dir, "heal.wav"), heal[: int(SR * 0.55)])

    # Victory fanfare — ascending pentatonic
    victory = np.zeros(int(SR * 0.7))
    for i, f in enumerate([392, 494, 587, 659, 784]):
        mix_at(victory, pluck(f, 0.35, 0.28), int(SR * i * 0.12))
    write_wav(os.path.join(sfx_dir, "victory.wav"), victory)

    # Defeat — descending minor
    defeat = tone(196, 0.9, decay=1.2, volume=0.35)
    mix_at(defeat, tone(146.83, 0.9, decay=1.0, volume=0.3), int(SR * 0.2))
    write_wav(os.path.join(sfx_dir, "defeat.wav"), defeat[: int(SR * 0.9)])

    # Impact — noise + low thump
    hit_len = int(SR * 0.12)
    hit = RNG.normal(0, 1, hit_len) * np.exp(-35 * t(0.12))
    hit += sine(90, 0.12) * np.exp(-18 * t(0.12)) * 0.5
    write_wav(os.path.join(sfx_dir, "hit.wav"), hit * 0.45)

    # Sand footstep
    fs = RNG.normal(0, 1, int(SR * 0.06))
    fs = lowpass(fs, 400) * np.exp(-40 * t(0.06)) * 0.35
    write_wav(os.path.join(sfx_dir, "footstep.wav"), fs)

    # Item pickup — bright pluck
    item = pluck(440, 0.25, 0.3)
    mix_at(item, pluck(554.37, 0.18, 0.18), int(SR * 0.06))
    write_wav(os.path.join(sfx_dir, "item.wav"), item[: int(SR * 0.25)])

    # Equip — armor clink
    equip = tone(330, 0.15, decay=10, volume=0.25)
    mix_at(equip, tone(440, 0.12, decay=14, volume=0.2), int(SR * 0.02))
    mix_at(equip, RNG.normal(0, 0.15, int(SR * 0.15)) * np.exp(-30 * t(0.15)), int(SR * 0.04))
    write_wav(os.path.join(sfx_dir, "equip.wav"), equip)


def main() -> None:
    compose_ambient(
        "menu",
        AMIN,
        24.0,
        {"ocean": 0.1, "drone": 0.05, "flute": True, "lead": 0.16, "beat": 4.0, "wind": 0.02, "master": 0.5},
    )
    compose_ambient(
        "village",
        DMIN,
        28.0,
        {"ocean": 0.12, "drone": 0.045, "flute": True, "lead": 0.14, "beat": 3.6, "wind": 0.035, "master": 0.52},
    )
    compose_ambient(
        "caves",
        [98.0, 116.54, 130.81, 155.56, 174.61],
        22.0,
        {
            "ocean": 0.04,
            "drone": 0.06,
            "flute": True,
            "lead": 0.12,
            "beat": 4.5,
            "pitch_mul": 1.5,
            "wind": 0.05,
            "master": 0.48,
        },
    )
    compose_ambient(
        "palace",
        PALACE,
        26.0,
        {"ocean": 0.02, "drone": 0.055, "flute": False, "lead": 0.13, "beat": 3.2, "step": 1, "master": 0.5},
    )
    compose_combat("combat", 16.0, boss=False)
    compose_combat("boss", 18.0, boss=True)
    make_sfx()

    for root, _, files in os.walk(OUT):
        for f in files:
            if f.endswith(".wav"):
                to_ogg(os.path.join(root, f))
    print("Generated game audio in", OUT)


if __name__ == "__main__":
    main()
