# ACE-Step prompt — `bgm_caves`

| Field | Value |
|-------|-------|
| Scene | tidal_caves |
| Category | zone |
| Output | `game/assets/audio/bgm/bgm_caves.ogg` |
| Duration | 210 s |
| Loop | True |
| BPM | 78 |
| Key | F# minor |

## Prompt

tidal cave exploration, wonder and unease, bioluminescent water bells synth pad, dripping cavern atmosphere, 78 BPM instrumental seamless loop, no vocals

## Negative

vocals, lyrics, singing, upbeat pop, EDM drop, heavy metal, bright cheerful, cartoon comedy, European fantasy brass, copyrighted melody

## ACE-Step Gradio / API

1. `bash tools/install_ace_step.sh`
2. `cd .cache/ace-step-1.5 && uv run acestep` (or `uv run acestep-api`)
3. Paste prompt; set duration/BPM/key; export WAV
4. `ffmpeg -i track.wav -c:a libvorbis -q:a 4 game/assets/audio/.../track.ogg`
5. `python3 tools/register_asset.py add ...`
