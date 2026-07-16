# ACE-Step prompt — `bgm_palace`

| Field | Value |
|-------|-------|
| Scene | dragon_palace_gate |
| Category | zone |
| Output | `game/assets/audio/bgm/bgm_palace.ogg` |
| Duration | 180 s |
| Loop | True |
| BPM | 84 |
| Key | B minor |

## Prompt

sterile beautiful dragon palace gate, ethereal harp and choir pad unsettling perfect fifth, coral gold void sky, ryūgū palace not European castle, 84 BPM instrumental loop

## Negative

vocals, lyrics, singing, upbeat pop, EDM drop, heavy metal, bright cheerful, cartoon comedy, European fantasy brass, copyrighted melody

## ACE-Step Gradio / API

1. `bash tools/install_ace_step.sh`
2. `cd .cache/ace-step-1.5 && uv run acestep` (or `uv run acestep-api`)
3. Paste prompt; set duration/BPM/key; export WAV
4. `ffmpeg -i track.wav -c:a libvorbis -q:a 4 game/assets/audio/.../track.ogg`
5. `python3 tools/register_asset.py add ...`
