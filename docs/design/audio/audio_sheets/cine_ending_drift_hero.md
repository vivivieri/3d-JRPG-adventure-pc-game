# ACE-Step prompt — `cine_ending_drift_hero`

## When to read

Use **ACE-Step prompt — `cine_ending_drift_hero`** when you need this reference during the current task Jump to a section below instead of reading end-to-end (3 sections).

## Jump to

- [Prompt](#prompt)
- [Negative](#negative)
- [ACE-Step Gradio / API](#ace-step-gradio-api)

| Field | Value |
|-------|-------|
| Scene | SC-17c pull back boat cinematic |
| Category | ending |
| Output | `game/assets/audio/bgm/cine_ending_drift_hero.ogg` |
| Duration | 135 s |
| Loop | False |
| BPM | 54 |
| Key | E minor |

## Prompt

final ending cinematic hero score tragic drift, Urashima rows into void sea palace below, emotional orchestral shakuhachi waves, slow 54 BPM film ending instrumental

## Negative

vocals, lyrics, singing, upbeat pop, EDM drop, heavy metal, bright cheerful, cartoon comedy, European fantasy brass, copyrighted melody

## ACE-Step Gradio / API

1. `bash tools/install_ace_step.sh`
2. `cd .cache/ace-step-1.5 && uv run acestep` (or `uv run acestep-api`)
3. Paste prompt; set duration/BPM/key; export WAV
4. `ffmpeg -i track.wav -c:a libvorbis -q:a 4 game/assets/audio/.../track.ogg`
5. `python3 tools/register_asset.py add ...`
