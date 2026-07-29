# ACE-Step prompt — `bgm_ending_rewind`

| Field | Value |
|-------|-------|
| Scene | SC-17a Rewind ending movie |
| Category | ending |
| Output | `game/assets/audio/bgm/bgm_ending_rewind.ogg` |
| Duration | 105 s |
| Loop | False |
| BPM | 96 |
| Key | G major |

## Prompt

ending movie hero score bittersweet festival, village restored time lapse, shamisen and crowd ambience swell, emotional rewind fate, 96 BPM instrumental no loop fade out

## Negative

vocals, lyrics, singing, upbeat pop, EDM drop, heavy metal, bright cheerful, cartoon comedy, European fantasy brass, copyrighted melody

## ACE-Step Gradio / API

1. `bash tools/install_ace_step.sh`
2. `cd .cache/ace-step-1.5 && uv run acestep` (or `uv run acestep-api`)
3. Paste prompt; set duration/BPM/key; export WAV
4. `ffmpeg -i track.wav -c:a libvorbis -q:a 4 game/assets/audio/.../track.ogg`
5. `python3 tools/register_asset.py add ...`
