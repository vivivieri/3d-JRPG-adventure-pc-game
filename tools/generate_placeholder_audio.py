#!/usr/bin/env python3
"""Generate placeholder CC0-style procedural audio for Tides of Urashima."""
import math
import os
import struct
import subprocess
import wave

SR = 44100
OUT = os.path.join(os.path.dirname(__file__), "..", "game", "assets", "audio")


def write_wav(path: str, samples) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with wave.open(path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        frames = b"".join(struct.pack("<h", max(-32767, min(32767, int(s * 32767)))) for s in samples)
        wf.writeframes(frames)


def ambient_loop(name: str, freqs, duration: float = 16.0, volume: float = 0.18) -> None:
    n = int(SR * duration)
    samples = []
    for i in range(n):
        t = i / SR
        v = 0.0
        for j, f in enumerate(freqs):
            v += math.sin(2 * math.pi * f * t + j) * (0.5 / len(freqs))
        fade = min(1.0, t / 1.5, (duration - t) / 1.5)
        samples.append(v * volume * fade)
    write_wav(os.path.join(OUT, "bgm", f"{name}.wav"), samples)


def sfx_tone(name: str, freq: float, duration: float = 0.12, volume: float = 0.35, decay: float = 8.0) -> None:
    n = int(SR * duration)
    samples = []
    for i in range(n):
        t = i / SR
        env = math.exp(-decay * t)
        v = math.sin(2 * math.pi * freq * t) * env * volume
        samples.append(v)
    write_wav(os.path.join(OUT, "sfx", f"{name}.wav"), samples)


def sfx_chord(name: str, freqs, duration: float = 0.35, volume: float = 0.28) -> None:
    n = int(SR * duration)
    samples = []
    for i in range(n):
        t = i / SR
        env = math.exp(-4.0 * t)
        v = sum(math.sin(2 * math.pi * f * t) for f in freqs) / len(freqs) * env * volume
        samples.append(v)
    write_wav(os.path.join(OUT, "sfx", f"{name}.wav"), samples)


def sfx_noise_hit(name: str, duration: float = 0.08, volume: float = 0.4) -> None:
    import random

    random.seed(42)
    n = int(SR * duration)
    samples = []
    for i in range(n):
        t = i / SR
        env = math.exp(-30.0 * t)
        v = (random.random() * 2 - 1) * env * volume
        samples.append(v)
    write_wav(os.path.join(OUT, "sfx", f"{name}.wav"), samples)


def to_ogg(wav_path: str) -> None:
    ogg_path = wav_path.rsplit(".", 1)[0] + ".ogg"
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", wav_path, "-c:a", "libvorbis", "-q:a", "4", ogg_path],
        check=True,
    )
    os.remove(wav_path)


def main() -> None:
    ambient_loop("menu", [110, 164, 220], duration=20.0, volume=0.14)
    ambient_loop("village", [98, 147, 196], duration=24.0, volume=0.16)
    ambient_loop("caves", [73, 110, 146], duration=20.0, volume=0.17)
    ambient_loop("palace", [130, 195, 260], duration=22.0, volume=0.15)
    ambient_loop("combat", [82, 123, 164], duration=12.0, volume=0.2)
    ambient_loop("boss", [65, 98, 131], duration=14.0, volume=0.22)

    sfx_tone("ui_confirm", 660, 0.1, 0.3)
    sfx_tone("ui_cancel", 330, 0.12, 0.25, 10.0)
    sfx_tone("interact", 520, 0.08, 0.28)
    sfx_chord("heal", [392, 494, 587], 0.4, 0.3)
    sfx_chord("victory", [523, 659, 784], 0.55, 0.32)
    sfx_tone("defeat", 180, 0.5, 0.35, 2.5)
    sfx_noise_hit("hit", 0.09, 0.38)
    sfx_tone("footstep", 90, 0.05, 0.12, 20.0)
    sfx_chord("item", [440, 554], 0.2, 0.26)
    sfx_chord("equip", [330, 415, 523], 0.25, 0.28)

    for root, _, files in os.walk(OUT):
        for f in files:
            if f.endswith(".wav"):
                to_ogg(os.path.join(root, f))
    print("Generated placeholder audio in", OUT)


if __name__ == "__main__":
    main()
