# ACE-Step prompt — `bgm_boss_tide_keeper_p2`

| Field | Value |
|-------|-------|
| Scene | Tide Keeper phase 2 surge |
| Category | boss |
| Output | `game/assets/audio/bgm/bgm_boss_tide_keeper_p2.ogg` |
| Duration | 120 s |
| Loop | True |
| BPM | 144 |
| Key | A minor |

## Prompt

boss phase two tidal surge, faster 144 BPM, water percussion and choir hits, ominous rising energy, instrumental loop seamless

## Negative

vocals, lyrics, singing, upbeat pop, EDM drop, heavy metal, bright cheerful, cartoon comedy, European fantasy brass, copyrighted melody

## ACE-Step Gradio / API

1. `bash tools/install_ace_step.sh`
2. `cd .cache/ace-step-1.5 && uv run acestep` (or `uv run acestep-api`)
3. Paste prompt; set duration/BPM/key; export WAV
4. `ffmpeg -i track.wav -c:a libvorbis -q:a 4 game/assets/audio/.../track.ogg`
5. `python3 tools/register_asset.py add ...`
