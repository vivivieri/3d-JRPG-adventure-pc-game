# ACE-Step prompt — `bgm_prologue`

| Field | Value |
|-------|-------|
| Scene | SC-00 opening movie |
| Category | opening |
| Output | `game/assets/audio/bgm/bgm_prologue.ogg` |
| Duration | 105 s |
| Loop | False |
| BPM | 60 |
| Key | A minor |

## Prompt

cinematic opening movie score, dark Urashima folklore, kappa turtle rescue myth, low strings and distant wordless choir pad, single temple bell, mythic and fateful 60 BPM, instrumental hero theme, no vocals, fade ending not loop

## Negative

vocals, lyrics, singing, upbeat pop, EDM drop, heavy metal, bright cheerful, cartoon comedy, European fantasy brass, copyrighted melody

## ACE-Step Gradio / API

1. `bash tools/install_ace_step.sh`
2. `cd .cache/ace-step-1.5 && uv run acestep` (or `uv run acestep-api`)
3. Paste prompt; set duration/BPM/key; export WAV
4. `ffmpeg -i track.wav -c:a libvorbis -q:a 4 game/assets/audio/.../track.ogg`
5. `python3 tools/register_asset.py add ...`
