# ACE-Step prompt — `cine_ending_anchor_hero`

| Field | Value |
|-------|-------|
| Scene | SC-17b dawn wide cinematic |
| Category | ending |
| Output | `game/assets/audio/bgm/cine_ending_anchor_hero.ogg` |
| Duration | 105 s |
| Loop | False |
| BPM | 80 |
| Key | C major |

## Prompt

ending cinematic hero score anchor ending, dawn shore rebuild small figures planting tree, warm restrained hope not Disney, orchestral koto blend instrumental film outro

## Negative

vocals, lyrics, singing, upbeat pop, EDM drop, heavy metal, bright cheerful, cartoon comedy, European fantasy brass, copyrighted melody

## ACE-Step Gradio / API

1. `bash tools/install_ace_step.sh`
2. `cd .cache/ace-step-1.5 && uv run acestep` (or `uv run acestep-api`)
3. Paste prompt; set duration/BPM/key; export WAV
4. `ffmpeg -i track.wav -c:a libvorbis -q:a 4 game/assets/audio/.../track.ogg`
5. `python3 tools/register_asset.py add ...`
