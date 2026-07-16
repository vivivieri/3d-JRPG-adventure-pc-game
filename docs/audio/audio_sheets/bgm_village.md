# ACE-Step prompt — `bgm_village`

| Field | Value |
|-------|-------|
| Scene | beach_shore, ruined_village |
| Category | zone |
| Output | `game/assets/audio/bgm/bgm_village.ogg` |
| Duration | 180 s |
| Loop | True |
| BPM | 66 |
| Key | E minor |

## Prompt

ruined coastal village field theme, empty dread and wind, shakuhachi lead low cello drone, muted grey sky, Japanese decay not bright, 66 BPM instrumental loop seamless

## Negative

vocals, lyrics, singing, upbeat pop, EDM drop, heavy metal, bright cheerful, cartoon comedy, European fantasy brass, copyrighted melody

## ACE-Step Gradio / API

1. `bash tools/install_ace_step.sh`
2. `cd .cache/ace-step-1.5 && uv run acestep` (or `uv run acestep-api`)
3. Paste prompt; set duration/BPM/key; export WAV
4. `ffmpeg -i track.wav -c:a libvorbis -q:a 4 game/assets/audio/.../track.ogg`
5. `python3 tools/register_asset.py add ...`
