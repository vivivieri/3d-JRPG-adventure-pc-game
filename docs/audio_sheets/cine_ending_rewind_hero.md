# ACE-Step prompt — `cine_ending_rewind_hero`

| Field | Value |
|-------|-------|
| Scene | SC-17a full cinematic crane shot |
| Category | ending |
| Output | `game/assets/audio/bgm/cine_ending_rewind_hero.ogg` |
| Duration | 120 s |
| Loop | False |
| BPM | 96 |
| Key | G major |

## Prompt

full ending cinematic hero orchestral score, festival crowd crane up figure dissolves, bittersweet triumph and loss, Japanese coastal folk instruments with strings, film ending not loop

## Negative

vocals, lyrics, singing, upbeat pop, EDM drop, heavy metal, bright cheerful, cartoon comedy, European fantasy brass, copyrighted melody

## ACE-Step Gradio / API

1. `bash tools/install_ace_step.sh`
2. `cd .cache/ace-step-1.5 && uv run acestep` (or `uv run acestep-api`)
3. Paste prompt; set duration/BPM/key; export WAV
4. `ffmpeg -i track.wav -c:a libvorbis -q:a 4 game/assets/audio/.../track.ogg`
5. `python3 tools/register_asset.py add ...`
