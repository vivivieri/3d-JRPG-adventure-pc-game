# ACE-Step prompt — `cine_boss_tide_keeper_intro`

| Field | Value |
|-------|-------|
| Scene | SC-15 Tide Keeper intro movie 6s |
| Category | boss_cinematic |
| Output | `game/assets/audio/stings/cine_boss_tide_keeper_intro.ogg` |
| Duration | 10 s |
| Loop | False |
| BPM | 84 |
| Key | A minor |

## Prompt

cinematic final boss intro hero score, tide keeper materializes from void sea throne, wide orchestral swell and clock tick undertone, tragic ruler 6 to 10 seconds instrumental

## Negative

vocals, lyrics, singing, upbeat pop, EDM drop, heavy metal, bright cheerful, cartoon comedy, European fantasy brass, copyrighted melody

## ACE-Step Gradio / API

1. `bash tools/install_ace_step.sh`
2. `cd .cache/ace-step-1.5 && uv run acestep` (or `uv run acestep-api`)
3. Paste prompt; set duration/BPM/key; export WAV
4. `ffmpeg -i track.wav -c:a libvorbis -q:a 4 game/assets/audio/.../track.ogg`
5. `python3 tools/register_asset.py add ...`
