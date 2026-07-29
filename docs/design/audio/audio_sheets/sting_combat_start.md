# ACE-Step prompt — `sting_combat_start`

| Field | Value |
|-------|-------|
| Scene | combat enter |
| Category | stings |
| Output | `game/assets/audio/stings/sting_combat_start.ogg` |
| Duration | 2 s |
| Loop | False |
| BPM | 120 |
| Key | D minor |

## Prompt

JRPG combat start sting, quick ink-wash whoosh and drum hit, 0.8 seconds instrumental

## Negative

vocals, lyrics, singing, upbeat pop, EDM drop, heavy metal, bright cheerful, cartoon comedy, European fantasy brass, copyrighted melody

## ACE-Step Gradio / API

1. `bash tools/install_ace_step.sh`
2. `cd .cache/ace-step-1.5 && uv run acestep` (or `uv run acestep-api`)
3. Paste prompt; set duration/BPM/key; export WAV
4. `ffmpeg -i track.wav -c:a libvorbis -q:a 4 game/assets/audio/.../track.ogg`
5. `python3 tools/register_asset.py add ...`
