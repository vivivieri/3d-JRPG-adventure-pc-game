# ACE-Step prompt — `bgm_menu`

| Field | Value |
|-------|-------|
| Scene | Title screen |
| Category | opening |
| Output | `game/assets/audio/bgm/bgm_menu.ogg` |
| Duration | 150 s |
| Loop | True |
| BPM | 72 |
| Key | D minor |

## Prompt

melancholy Japanese coastal JRPG title theme, solo koto and sparse synth pad, distant ocean waves, slow 72 BPM, instrumental, no vocals, still and fateful, NieR restraint, seamless loop

## Negative

vocals, lyrics, singing, upbeat pop, EDM drop, heavy metal, bright cheerful, cartoon comedy, European fantasy brass, copyrighted melody

## ACE-Step Gradio / API

1. `bash tools/install_ace_step.sh`
2. `cd .cache/ace-step-1.5 && uv run acestep` (or `uv run acestep-api`)
3. Paste prompt; set duration/BPM/key; export WAV
4. `ffmpeg -i track.wav -c:a libvorbis -q:a 4 game/assets/audio/.../track.ogg`
5. `python3 tools/register_asset.py add ...`
