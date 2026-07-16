# ACE-Step prompt — `cine_boss_wraith_intro`

| Field | Value |
|-------|-------|
| Scene | SC-09 Shore Wraith intro movie 5s |
| Category | boss_cinematic |
| Output | `game/assets/audio/stings/cine_boss_wraith_intro.ogg` |
| Duration | 8 s |
| Loop | False |
| BPM | 120 |
| Key | E minor |

## Prompt

cinematic boss intro sting, drowned spirit rises from pool, water surge and choir stab, horror coastal folklore, 5 to 8 seconds hero hit instrumental no vocals

## Negative

vocals, lyrics, singing, upbeat pop, EDM drop, heavy metal, bright cheerful, cartoon comedy, European fantasy brass, copyrighted melody

## ACE-Step Gradio / API

1. `bash tools/install_ace_step.sh`
2. `cd .cache/ace-step-1.5 && uv run acestep` (or `uv run acestep-api`)
3. Paste prompt; set duration/BPM/key; export WAV
4. `ffmpeg -i track.wav -c:a libvorbis -q:a 4 game/assets/audio/.../track.ogg`
5. `python3 tools/register_asset.py add ...`
