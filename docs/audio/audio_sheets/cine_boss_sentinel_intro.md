# ACE-Step prompt — `cine_boss_sentinel_intro`

| Field | Value |
|-------|-------|
| Scene | SC-14 Palace Sentinel intro movie 3s |
| Category | boss_cinematic |
| Output | `game/assets/audio/stings/cine_boss_sentinel_intro.ogg` |
| Duration | 5 s |
| Loop | False |
| BPM | 96 |
| Key | C minor |

## Prompt

cinematic boss intro, lacquer armored sentinel footsteps in void hall, metallic march and eye slit glow, 3 to 5 seconds instrumental sting no vocals

## Negative

vocals, lyrics, singing, upbeat pop, EDM drop, heavy metal, bright cheerful, cartoon comedy, European fantasy brass, copyrighted melody

## ACE-Step Gradio / API

1. `bash tools/install_ace_step.sh`
2. `cd .cache/ace-step-1.5 && uv run acestep` (or `uv run acestep-api`)
3. Paste prompt; set duration/BPM/key; export WAV
4. `ffmpeg -i track.wav -c:a libvorbis -q:a 4 game/assets/audio/.../track.ogg`
5. `python3 tools/register_asset.py add ...`
