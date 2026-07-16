# ACE-Step prompt — `bgm_combat`

| Field | Value |
|-------|-------|
| Scene | standard encounters |
| Category | zone |
| Output | `game/assets/audio/bgm/bgm_combat.ogg` |
| Duration | 120 s |
| Loop | True |
| BPM | 108 |
| Key | D minor |

## Prompt

JRPG battle theme mid tension, light taiko and strings, restrained not heroic anime, 108 BPM instrumental combat loop seamless

## Negative

vocals, lyrics, singing, upbeat pop, EDM drop, heavy metal, bright cheerful, cartoon comedy, European fantasy brass, copyrighted melody

## ACE-Step Gradio / API

1. `bash tools/install_ace_step.sh`
2. `cd .cache/ace-step-1.5 && uv run acestep` (or `uv run acestep-api`)
3. Paste prompt; set duration/BPM/key; export WAV
4. `ffmpeg -i track.wav -c:a libvorbis -q:a 4 game/assets/audio/.../track.ogg`
5. `python3 tools/register_asset.py add ...`
